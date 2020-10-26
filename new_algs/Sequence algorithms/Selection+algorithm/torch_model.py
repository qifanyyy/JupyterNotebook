import torch as th
import torch_geometric as pyg
from torch_geometric.nn import global_add_pool, global_max_pool,\
                               global_mean_pool
from torch_geometric.utils import softmax, scatter_
from torch_geometric.nn import GINConv, MessagePassing
from torch.nn import functional as F
import copy


class GraphModule(th.nn.Module):

    __keys__ = ['x', 'edge_index', 'edge_attr', 'batch', 'global_inp']

    def __init__(self):
        super().__init__()
        self._bind = {}

    def forward_bind(self):
        pass

    def _map_args(self, args, kwargs):
        D = {}
        keys = self.__keys__

        for i, a in enumerate(args):
            D[keys[i]] = a
        D.update(kwargs)
        return D

    def prepare_args(self, args, kwargs):
        args = self._map_args(args, kwargs)
        D = {}
        for k, v in args.items():
            if k in self._bind:
                D[self._bind[k]] = v
        return D

    def forward(self, *args, **kwargs):
        D = self.prepare_args(args, kwargs)
        return self.forward_bind(**D)


class AttentionReadout(GraphModule):

    def __init__(self):
        super().__init__()

    def attention_bind(self):
        pass

    def attention(self, *args, **kwargs):
        args = self.prepare_args(args, kwargs)
        return self.attention_bind(**args)


class ConvolveAndReadout(AttentionReadout):

    def __init__(self, conv=None, readout=None):
        super().__init__()
        self.conv = conv
        self.readout = readout
        self._bind = {x: x for x in ['x', 'edge_index', 'edge_attr',
                                     'batch', 'global_inp']}

    def forward_bind(self, x, edge_index, edge_attr, batch, global_inp):
        if self.conv is not None:
            x = self.conv(x, edge_index, edge_attr, batch, global_inp)

        if self.readout is not None:
            readout = self.readout(x, edge_index, edge_attr, batch, global_inp)
            return x, readout

        return x

    def attention_bind(self, x, edge_index, edge_attr, batch, global_inp):
        if self.readout is None or\
            not isinstance(self.readout, AttentionReadout):
            return None

        if self.conv is not None:
            x = self.conv(x, edge_index, edge_attr, batch, global_inp)

        readout = self.readout.attention(x, edge_index, edge_attr,
                                         batch, global_inp)
        return readout


class StandardReadout(GraphModule):

    def __init__(self, method):
        super().__init__()
        self.method = method
        self._bind = {'x': 'x', 'batch': 'batch'}

    def forward_bind(self, x, batch):

        if self.method == 'add':
            return global_add_pool(x, batch)

        if self.method == 'mean':
            return global_mean_pool(x, batch)

        if self.method == 'max':
            return global_max_pool(x, batch)

        raise ValueError("Unknown method %s" % self.method)


class OutputModel(th.nn.Module):

    def __init__(self, layers, readout_dims, pipes={}):
        super().__init__()
        self.readout_dims = readout_dims
        self.out_dim = self.calc_dims()
        self.pipes = pipes

        for i, layer in enumerate(layers):
            self.add_module(str(i), layer)

    def calc_dims(self):
        pass

    def compose(self, readouts):
        pass

    def forward(self, data, return_attention=False):

        kwargs = {
            'x': data.x,
            'edge_index': data.edge_index,
            'edge_attr': data.edge_attr,
            'batch': data.batch,
            'global_inp': data.category
        }

        att = []
        readouts = []

        for i, layer in self._modules.items():
            i = int(i)
            rdim = self.readout_dims[i]
            r = None

            if rdim <= 0:
                x = layer(**kwargs)
            else:
                x, r = layer(**kwargs)

            if return_attention:
                att.append(
                    layer.attention(**kwargs)
                    if isinstance(layer, AttentionReadout)
                    else None
                )

            kwargs['x'] = x

            if i in self.pipes:
                kwargs['readout'] = r
                pipe = self.pipes[i]
                kwargs = pipe.apply(kwargs)
                r = kwargs['readout']
                del kwargs['readout']

            if r is not None:
                readouts.append(r)

        if return_attention:
            return self.compose(readouts), att

        return self.compose(readouts)


class ConcatModel(OutputModel):

    def calc_dims(self):
        dim = 0

        for r in self.readout_dims:
            dim += r

        if dim <= 0:
            raise ValueError("Need at least one readout layer")
        return dim

    def compose(self, readouts):
        if len(readouts) == 1:
            return readouts[0]
        return th.cat(readouts, dim=1)


class EmbeddingLayer(GraphModule):

    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.lin = th.nn.Linear(in_channels, out_channels)
        self._bind = {'x': 'x'}

    def forward_bind(self, x):
        out = self.lin(x)
        out = F.relu(out)
        return out


class SparseEmbeddingLayer(th.nn.Module):

    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.embed = th.nn.EmbeddingBag(in_channels, out_channels, mode="sum")
        self.norm = th.nn.LayerNorm(out_channels)

    def forward(self, data):
        out = self.embed(
            data.sparse_index, data.offset, data.weight
        )
        out = self.norm(out)
        return out


class ConditionalGlobalAttention(th.nn.Module):

    def __init__(self, in_channels, cond_channels):
        super().__init__()
        self.query_embed = th.nn.Linear(cond_channels, in_channels)
        self.scale = th.sqrt(th.tensor(in_channels, dtype=th.float))

    def attention(self, x, batch, condition, size=None):
        size = batch[-1].item() + 1 if size is None else size

        query = self.query_embed(condition.float())[batch, :]
        attention = (x * query).sum(dim=1)
        attention = attention / self.scale
        attention = softmax(attention, batch, size)
        return attention

    def forward(self, x, batch, condition, size=None):

        x = x.unsqueeze(-1) if x.dim() == 1 else x
        attention = self.attention(x, batch, condition, size)
        attention = attention.unsqueeze(1).repeat(1, x.shape[1])

        out = scatter_('add', attention * x, batch, size)
        return out


class CGALayer(AttentionReadout):

    def __init__(self, in_dim, global_dim):
        super().__init__()
        self._bind = {'x': 'x', 'batch': 'batch', 'global_inp': 'condition'}
        self._cga = ConditionalGlobalAttention(in_dim, global_dim)

    def forward_bind(self, x, batch, condition):
        return self._cga.forward(x, batch, condition)

    def attention_bind(self, x, batch, condition):
        return self._cga.attention(x, batch, condition)


class LayerBuilder:

    def __init__(self, in_channels, out_channels):
        self.in_channels = in_channels
        self.out_channels = out_channels

    def default_build(self):
        pass

    def build(self, config):
        pass


def select_layer(type):
    if type == 'gin':
        return GINBuilder

    if type == 'maxmin':
        return MaxMinBuilder

    if type == 'edge_gin':
        return EdgeGINBuilder

    raise ValueError("Unknown type %s" % type)


class ConvLayer(GraphModule):

    def __init__(self, conv):
        super().__init__()
        self.conv = conv
        self._bind = {'x': 'x', 'edge_index': 'edge_index'}

    def forward_bind(self, x, edge_index):
        return self.conv(x, edge_index)


class GINMLP(th.nn.Module):

    def __init__(self, in_channel, hidden, out_channel, dropout,
                 batch_norm):
        super().__init__()

        seq = []
        for i, h in enumerate(hidden):
            drop = dropout[i]
            hid = hidden[i]
            b = batch_norm[i]
            seq.extend(self._build_layer(in_channel, hid, drop, b))
            in_channel = hid
        seq.append(th.nn.Linear(in_channel, out_channel))
        self.sequence = th.nn.Sequential(*seq)

    def _norm_layer(self, type, channel):
        if type is True or type == 'batch':
            return th.nn.BatchNorm1d(channel)

        if type == 'layer':
            return th.nn.LayerNorm(channel)
        raise ValueError("Unknown norm type %s." % type)

    def _build_layer(self, in_channel, out_channel, dropout, batch_norm):
        if batch_norm:
            return [
                th.nn.Linear(in_channel, out_channel),
                self._norm_layer(batch_norm, out_channel),
                th.nn.Dropout(p=dropout),
                th.nn.ReLU()
            ]
        return [
            th.nn.Linear(in_channel, out_channel),
            th.nn.Dropout(p=dropout),
            th.nn.ReLU()
        ]

    def forward(self, x):
        return self.sequence(x)


class GINBuilder(LayerBuilder):

    def __init__(self, in_channels, out_channels):
        super().__init__(in_channels, out_channels)

    def build_mlp(self, config, in_channel, out_channel):
        if 'hidden' not in config:
            return config, th.nn.Linear(in_channel, out_channel)

        config = copy.deepcopy(config)

        hidden = config['hidden']
        del config['hidden']
        if not isinstance(hidden, list):
            hidden = [hidden]

        dropout = 0.5
        if 'dropout' in config:
            dropout = config['dropout']
            del config['dropout']
        if not isinstance(dropout, list):
            dropout = [dropout]*len(hidden)

        batch_norm = True
        if 'batch_norm' in config:
            batch_norm = config['batch_norm']
            del config['batch_norm']
        if not isinstance(batch_norm, list):
            batch_norm = [batch_norm]*len(hidden)

        return config, GINMLP(in_channel, hidden, out_channel,
                              dropout, batch_norm)

    def build(self, config):
        if 'hidden' not in config:
            raise ValueError("Need a hidden definition in GIN config")
        config, mlp = self.build_mlp(config, self.in_channels,
                                     self.out_channels)
        config['nn'] = mlp
        return ConvLayer(GINConv(**config))

    def default_build(self):
        return self.build({
            'hidden': 32
        })


class MaxMinLayer(GraphModule):

    def __init__(self, in_channel, out_channel, mi, mx):
        super().__init__()
        assert in_channel == out_channel

        self.min = mi
        self.max = mx
        self._bind = {'x': 'x'}

    def forward_bind(self, x):
        x = th.clamp(x, self.min, self.max)
        x = (x - self.min)/(self.max - self.min)
        return x


class MaxMinBuilder(LayerBuilder):

    def build(self, config):
        return MaxMinLayer(self.in_channels, self.out_channels,
                           config[0], config[1])

    def default_build(self):
        return self.build([0, 255])


class EdgeAttention(th.nn.Module):

    def __init__(self, nn):
        super().__init__()
        self.nn = nn

    def forward(self, x, edge_index, edge_attr):
        row, col = edge_index
        x = x.unsqueeze(-1) if x.dim() == 1 else x

        x_row, x_col = x.index_select(0, row), x.index_select(0, col)
        out = th.cat([x_row, x_col, edge_attr.float()], dim=1)
        out = self.nn(out)
        out = scatter_('add', out, row, dim_size=x.size(0))

        return out


class EdgeGIN(MessagePassing):

    def __init__(self, gin_nn, edge_nn):
        super().__init__()
        self.nn = gin_nn
        self.edge = EdgeAttention(edge_nn)

    def forward(self, x, edge_index, edge_attr):

        x = x.unsqueeze(-1) if x.dim() == 1 else x
        x_e = self.edge(x, edge_index, edge_attr)
        out = self.nn(x + self.propagate(edge_index, x=x_e))
        return out

    def message(self, x_j):
        return x_j


class EdgeGINLayer(GraphModule):

    def __init__(self, edge_gin):
        super().__init__()
        self.conv = edge_gin
        self._bind = {k: k for k in ['x', 'edge_index', 'edge_attr']}

    def forward_bind(self, x, edge_index, edge_attr):
        return self.conv(x, edge_index, edge_attr)


class EdgeGINBuilder(GINBuilder):

    def build(self, config):
        config = copy.copy(config)
        gin_config = {'hidden': 32}
        if 'gin' in config:
            gin_config = config['gin']
            del config['gin']

        edge_in = 3
        if 'edge_dim' in config:
            edge_in = config['edge_dim']
            del config['edge_dim']
        edge_in = 2*self.in_channels + edge_in

        edge_config = {}
        if 'edge' in config:
            edge_config = config['edge']
            del config['edge']

        gin_config, gin_mlp = self.build_mlp(
            gin_config, self.in_channels, self.out_channels
        )

        edge_config, edge_mlp = self.build_mlp(
            edge_config, edge_in, self.in_channels
        )

        config['gin_nn'] = gin_mlp
        config['edge_nn'] = edge_mlp

        edge_gin = EdgeGIN(**config)
        return EdgeGINLayer(edge_gin)

    def default_build(self):
        return self.build({})


def build_node_conv(config, node_dim, edge_dim, global_dim):
    type = config['type']
    dim = config['node_dim']

    if type == 'embedding':
        return EmbeddingLayer(node_dim, dim), dim

    try:
        layer = select_layer(type)
        if layer is not None:
            layer = layer(node_dim, dim)
            if isinstance(layer, LayerBuilder):
                if 'build' in config:
                    layer = layer.build(config['build'])
                else:
                    layer = layer.default_build()
            return layer, dim
    except ValueError:
        pass

    raise ValueError("Unknown node convolution %s" % type)


def build_readout(config, node_dim, edge_dim, global_dim):
    standard = set(['add', 'max', 'mean'])

    if config['type'] in standard:
        return StandardReadout(config['type']), node_dim

    if config['type'] == 'cga':
        return CGALayer(node_dim, global_dim), node_dim


def build_output(config, layers, readout_dims, pipes):
    type = config['type']

    model = None
    if type == 'concatinate':
        model = ConcatModel(layers, readout_dims, pipes=pipes)

    if model is None:
        raise ValueError("Unknown type output type %s" % type)

    return model, model.out_dim


def build_layer(config, node_dim, edge_dim, global_dim):

    conv = None
    if 'node_conv' in config:
        conv, node_dim = build_node_conv(config['node_conv'], node_dim,
                                         edge_dim, global_dim)

    readout = None
    readout_dim = 0
    if 'readout' in config:
        readout, readout_dim = build_readout(
            config['readout'], node_dim, edge_dim, global_dim
        )

    layer = ConvolveAndReadout(conv, readout)

    return layer, node_dim, readout_dim


class PipeOperation:

    def __init__(self, ops):
        self._ops = ops

    def apply(self, kwargs):

        updates = []
        for operation in self._ops:
            updates.append(operation(kwargs))

        kwargs = copy.copy(kwargs)
        for up in updates:
            kwargs.update(up)

        return kwargs


class SingleToSingle:

    def __init__(self, key1, key2):
        self.key1 = key1
        self.key2 = key2

    def __call__(self, kwargs):
        key1 = self.key1
        key2 = self.key2
        if kwargs[key1] is None:
            return {key2: kwargs[key1]}
        if kwargs[key2] is None:
            return {key2: kwargs[key1]}
        R = th.cat([kwargs[key1].float(), kwargs[key2].float()], dim=1)
        return {key2: R}


def build_pipe_impl(key1, single1, key2, single2):

    if not single1:
        raise ValueError("Pipe input requires non variable size")

    if single2:
        return SingleToSingle(key1, key2)
    else:
        raise NotImplementedError


def build_pipe(config, node_dim, edge_dim, global_dim, readout_dim):

    lookup = {
        'r': ('readout', readout_dim, True),
        'n': ('x', node_dim, False),
        'e': ('edge_index', edge_dim, False),
        'g': ('global_inp', global_dim, True)
    }

    pipes = []

    for op in config.split(';'):
        if '->' in op:
            op1, op2 = op.split('->')
            op1 = op1.strip()
            op2 = op2.strip()

            key1, dim1, single1 = lookup[op1]
            key2, dim2, single2 = lookup[op2]

            pipe = build_pipe_impl(key1, single1, key2, single2)

            if op2 == 'r':
                readout_dim = dim1 + dim2
            elif op2 == 'g':
                global_dim = dim1 + dim2

            pipes.append(pipe)

    return PipeOperation(pipes), node_dim, edge_dim, global_dim, readout_dim


def build_model_from_config(config):
    if 'node_input' not in config:
        raise ValueError("Need feature dim for nodes!")
    if 'layers' not in config:
        raise ValueError("At least one readout layer is required.")

    node_dim = config['node_input']
    edge_dim = 0

    if 'edge_input' in config:
        edge_dim = config['edge_input']

    global_dim = 0
    if 'global_input' in config:
        global_dim = config['global_input']

    layers = []
    readout_dims = []
    pipes = {}

    for i, layer_config in enumerate(config['layers']):
        layer, node_dim, readout_dim = build_layer(
            layer_config, node_dim, edge_dim, global_dim
        )

        if 'pipe' in layer_config:
            pipe, node_dim, edge_dim, global_dim, readout_dim =\
                    build_pipe(layer_config['pipe'], node_dim, edge_dim,
                               global_dim, readout_dim)
            pipes[i] = pipe

        layers.append(layer)
        readout_dims.append(readout_dim)

    out_config = {'type': 'concatinate'}

    if 'global_output' in config:
        out_config = config['global_output']

    return build_output(out_config, layers, readout_dims, pipes)


if __name__ == '__main__':

    model = {
        'ast_type': 'bag',
        'dropout': 0.1,
        'augment': False,
        'node_input': 148,
        'edge_input': 3,
        'global_input': 4,
        'layers': [
            {
                'node_conv': {
                    'type': 'embedding',
                    'node_dim': 32
                },
                'readout': {
                    'type': 'cga'
                },
                'pipe': 'r->g; g->r'
            },
            {
                'node_conv': {
                    'type': 'gin',
                    'node_dim': 32,
                    'build': {
                        'hidden': 32,
                        'dropout': 0.1
                    }
                },
                'readout': {
                    'type': 'cga'
                }
            }
        ],
        'global_output': {
            'type': 'concatinate'
        }
    }
    m = build_model_from_config(model)
    print(m)

import torch as th

from torch_geometric.data import Data, Batch

import copy
import networkx as nx
from networkx.algorithms.dag import topological_sort

from tasks.torch.modules import create_handler


class ComputationNode:

    def __init__(self):
        self._in = {}
        self._out = {}

    def get_inputs(self):
        return self._in.keys()

    def get_outputs(self):
        return self._out.keys()


class GraphSourceNode(ComputationNode):

    def __init__(self, node_input, **kwargs):
        super().__init__()
        out = {}

        if node_input is None:
            raise ValueError("Requires node_input config!")
        out['x'] = node_input

        if 'edge_input' in kwargs:
            out['edge_attr'] = kwargs['edge_input']
            del kwargs['edge_input']

        if 'global_input' in kwargs:
            out['category'] = kwargs['global_input']
            del kwargs['global_input']

        out['edge_index'] = 2
        out['batch'] = 1
        self._out = out
        self._config = kwargs


class SourceNode(ComputationNode):

    def __init__(self, input, **kwargs):
        super().__init__()
        out = {}

        if input is None:
            raise ValueError("Requires input config!")
        out['forward'] = input

        self._out = out
        self._config = kwargs


class SinkNode(ComputationNode):

    def __init__(self):
        super().__init__()
        self._in['input'] = None


class ModuleNode(ComputationNode):

    def __init__(self, handler):
        super().__init__()
        self._handler = handler

    def get_inputs(self):
        return self._handler.get_inputs()

    def get_outputs(self):
        return self._handler.get_outputs()


class GraphModule(th.nn.Module):

    def __init__(self, modules, funcs, sequence):
        super().__init__()

        self.activation = th.nn.ModuleDict(modules)
        self.funcs = funcs
        self._sequence = sequence
        self._callback = []

    def register_callback(self, cb):
        self._callback.append(cb)

    def _execute(self, action, kwargs):

        if action == 'standard_start':
            return {'forward': kwargs['input']}

        if action == 'graph_start':
            data = kwargs['input']
            out = {}
            out.update(data.__dict__)
            return out

        if action == 'output':
            return kwargs['input']

        if action in self.funcs:
            return self.funcs[action](**kwargs)

        module = self.activation[action]

        for cb in self._callback:
            tmp = cb(module, kwargs)
            if tmp is not None:
                kwargs = tmp

        return module(**kwargs)

    def forward(self, input):

        start = self._sequence[0]
        tmp = self._execute(start[1], {'input': input})
        state = {}

        for k, V in start[2].items():
            for v in V:
                state[v] = tmp[k]

        for i in range(1, len(self._sequence)):

            bind, module, out = self._sequence[i]

            local_args = {}

            for k, v in bind.items():
                if v not in local_args:
                    local_args[v] = []
                local_args[v].append(state[k])

            for k, e in list(local_args.items()):
                if len(e) > 1:
                    local_args[k] = th.cat([_e.float() for _e in e], dim=1)
                else:
                    local_args[k] = e[0]

            for f in bind.keys():
                del state[f]

            o = self._execute(module, local_args)

            if isinstance(o, tuple):
                o, r = o
                o = {'forward': o, 'readout': r}
            else:
                o = {'forward': o}

            for k, S in out.items():
                val = o[k]
                for _o in S:
                    state[_o] = val

        return state['__out__']


def assign_sizes(graph):

    flow = ['source']
    seen = set([])

    while len(flow) > 0:
        act = flow.pop()

        if act in seen:
            continue

        compile = True
        for u, _ in graph.in_edges(act):
            if u not in seen:
                compile = False
                break

        if not compile:
            continue

        seen.add(act)

        un = graph.nodes[act]['module']

        if isinstance(un, ModuleNode):
            handler = un._handler
            for k, v in un._in.items():
                handler.bind_input(k, v)

            for k in un.get_outputs():
                un._out[k] = handler.get_output_size(k)

        for _, v, k, to in graph.out_edges(act, keys=True, data='to'):
            vn = graph.nodes[v]['module']

            in_size = un._out[k]
            if to not in vn._in:
                vn._in[to] = 0
            if vn._in[to] is None:
                vn._in[to] = 0
            vn._in[to] += in_size
            flow.append(v)


def unique_edges(graph):

    i = 0
    for u, v, k in graph.edges(keys=True):
        graph.edges[u, v, k]['identifier'] = 'e_%d' % i
        i += 1


def execution_sequence(graph):

    unique_edges(graph)

    sequence = []

    for n in topological_sort(graph):
        node = graph.nodes[n]
        mod = node['module']

        bind = {}
        out = {}

        action = None
        if isinstance(mod, SourceNode):
            action = 'standard_start'
        elif isinstance(mod, GraphSourceNode):
            action = 'graph_start'
        elif isinstance(mod, SinkNode):
            action = 'output'
            out['forward'] = ['__out__']
        else:
            action = n

        for _, _, D in graph.in_edges(n, data=True):
            bind[D['identifier']] = D['to']

        for _, _, k, id in graph.out_edges(n, data='identifier', keys=True):
            if k not in out:
                out[k] = []
            out[k].append(id)

        sequence.append((bind, action, out))

    return sequence


class ComputationGraph:

    def __init__(self, src):
        self._graph = nx.MultiDiGraph()
        self._graph.add_node('source', module=src)
        self._graph.add_node('sink', module=SinkNode())
        self.config = src._config

    def add_module(self, key, module):

        if key in set(['source', 'sink']):
            raise ValueError("Key %s is a reserved key." % key)

        if not isinstance(module, dict):
            module = {'type': module}

        if 'type' not in module:
            raise ValueError("Require module type got %s" % str(module))
        mod = module['type']
        del module['type']

        handler = create_handler(mod, module)
        self._graph.add_node(key, module=ModuleNode(handler))

    def add_binding(self, src_id, sink_id, src_out='forward', sink_in='input'):
        if src_id not in self._graph or sink_id not in self._graph:
            raise ValueError("Nodes are unknown (%s, %s)" % (src_id, sink_id))

        src = self._graph.nodes[src_id]['module']
        sink = self._graph.nodes[sink_id]['module']

        if src_out not in src.get_outputs():
            p = ', '.join(src.get_outputs())
            raise ValueError("source [%s] has not output of id \"%s\" [Options: %s]" % (src_id, src_out, p))

        if sink_in not in sink.get_inputs():
            p = ', '.join(sink.get_inputs())
            raise ValueError("sink [%s] has not input of id \"%s\" [Options: %s]" % (sink_id, sink_in, p))

        self._graph.add_edge(src_id, sink_id, key=src_out, to=sink_in)

    def compile(self):
        assign_sizes(self._graph)

        modules = {}
        funcs = {}
        for n in self._graph:
            m = self._graph.nodes[n]['module']
            if isinstance(m, ModuleNode):
                handler = m._handler
                if handler.is_function():
                    funcs[n] = handler.build()
                else:
                    modules[n] = handler.build()

        seq = execution_sequence(self._graph)

        module_seq = []

        for _, act, _ in seq:
            if act in modules:
                module_seq.append(
                    [act, modules[act]]
                )

        return GraphModule(module_seq, funcs, seq)

    def __getstate__(self):
        out = {}
        src = self._graph.nodes['source']['module']
        out.update(src._config)

        if 'forward' in src._out:
            out['input'] = src._out['forward']
        else:
            out['node_input'] = src._out['x']

            if 'category' in src._out:
                out['global_input'] = src._out['category']

            if 'edge_attr' in src._out:
                out['edge_input'] = src._out['edge_attr']

        modules = {}
        for node in self._graph:
            if node not in set(['source', 'sink']):
                N = self._graph.nodes[node]['module']
                modules[node] = N._handler.__getstate__()
        out['modules'] = modules

        edges = []

        for src, sink, src_out, sink_in in self._graph.edges(data='to', keys=True):
            edges.append([src, src_out, sink_in, sink])
        out['bind'] = edges

        return out


def build_source(config):
    if 'input' in config:
        return SourceNode(**config)

    if 'node_input' in config:
        return GraphSourceNode(**config)


def build_graph(config):
    config = copy.deepcopy(config)

    modules = {}
    if 'modules' in config:
        modules = config['modules']
        del config['modules']

    edges = []
    if 'bind' in config:
        edges = config['bind']
        del config['bind']

    src = build_source(config)

    graph = ComputationGraph(src)

    for id, mod in modules.items():
        graph.add_module(id, mod)

    for src, src_out, sink_in, sink in edges:
        graph.add_binding(src, sink, src_out, sink_in)

    return graph


if __name__ == '__main__':
    config = {
        'input': 32,
        'modules': {
            'm0': {'type': 'torch::Linear', 'dim': 32},
            'm1': 'torch::ReLU',
            'm2': {'type': 'torch::Linear', 'dim': 32},
            'm3': 'torch::ReLU',
            'm4': {'type': 'readout', 'method': 'add'}
        },
        'bind': [
            ['source', 'forward', 'input', 'm0'],
            ['m0', 'forward', 'input', 'm1'], ['m1', 'forward', 'input', 'm2'],
            ['m2', 'forward', 'input', 'm3'],
            ['m3', 'forward', 'input', 'sink']
        ]
    }
    graph = build_graph({
        'node_input': 1,
        'global_input': 4,
        'modules': {
            'm0': {'type': 'tasks::Embedding', 'node_dim': 1},
            'm1': 'tasks::cga',
            'm2': {'type': 'torch::Linear', 'out_channels': 91, 'bias': False}
        },
        'bind': [
            ['source', 'x', 'x', 'm0'],
            ['m0', 'forward', 'x', 'm1'],
            ['source', 'category', 'condition', 'm1'],
            ['source', 'batch', 'batch', 'm1'],
            ['m1', 'forward', 'input', 'm2'],
            ['m2', 'forward', 'input', 'sink']
        ]
    })

    graph = graph.compile()
    print(graph)

    print(graph(Batch.from_data_list(
        [Data(
            x=th.tensor([[1.0], [0.5]], dtype=th.float),
            category=th.tensor([[1, 0, 0, 0]], dtype=th.float)
        )]
    )))

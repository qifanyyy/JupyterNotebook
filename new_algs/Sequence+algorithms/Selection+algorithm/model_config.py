import copy
from tasks.data import proto_data


def layer_module(config):
    config = copy.deepcopy(config)
    type = config['type']
    # del config['type']

    if type == 'linear':
        config['type'] = 'torch::Linear'
        return config, ['x']

    if type == 'embed':
        config['type'] = 'tasks::Embedding'
        return config, ['x']

    if type == 'ex_entry':
        config['type'] = 'mx::Entry'
        return config, ['x']

    if type == 'con_gin':
        cfg = {'type': 'mx::ConGIN', 'node_dim': config['node_dim'],
               'hidden': config['hidden']}
        return cfg, ['x', 'edge_index', 'edge_attr']

    if type == 'dense_gin':
        cfg = {'type': 'dense::DenseGIN', 'node_dim': config['node_dim'],
               'hidden': config['hidden']}
        return cfg, ['x', 'edge_index', 'edge_attr']

    if type == 'dense_egin':
        cfg = {'type': 'dense::DenseEGIN', 'node_dim': config['node_dim'],
               'hidden': config['hidden']}
        return cfg, ['x', 'edge_index', 'edge_attr']

    if type == 'edge_gin':
        cfg = {'type': 'tasks::CEdgeGIN', 'node_dim': config['node_dim']}
        gin = {}
        if 'hidden' in config:
            gin['hidden'] = config['hidden']
            if 'dropout' in config:
                gin['dropout'] = config['dropout']
            if 'norm' in config:
                gin['norm'] = config['norm']
            else:
                gin['norm'] = False
        cfg['gin_nn'] = gin
        edge = {}
        if 'edge_hidden' in config:
            edge['hidden'] = config['edge_hidden']
            if 'edge_dropout' in config:
                edge['dropout'] = config['edge_dropout']
            if 'edge_norm' in config:
                edge['norm'] = config['edge_norm']
            else:
                edge['norm'] = False
        cfg['edge_nn'] = edge
        return cfg, ['x', 'edge_index', 'edge_attr']

    if type == 'simple_edge_gin':
        cfg = {'type': 'tasks::CSEdgeGIN', 'node_dim': config['node_dim']}
        gin = {}
        if 'hidden' in config:
            gin['hidden'] = config['hidden']
            if 'dropout' in config:
                gin['dropout'] = config['dropout']
            if 'norm' in config:
                gin['norm'] = config['norm']
            else:
                gin['norm'] = False
        cfg['gin_nn'] = gin
        return cfg, ['x', 'edge_index', 'edge_attr']

    if type == 'att_edge_gin':
        cfg = {'type': 'tasks::CAEdgeGIN', 'node_dim': config['node_dim']}
        gin = {}
        if 'hidden' in config:
            gin['hidden'] = config['hidden']
            if 'dropout' in config:
                gin['dropout'] = config['dropout']
            if 'norm' in config:
                gin['norm'] = config['norm']
            else:
                gin['norm'] = False
        cfg['gin_nn'] = gin
        return cfg, ['x', 'edge_index', 'edge_attr']

    if type == 'gin':
        cfg = {'type': 'tasks::CGIN', 'node_dim': config['node_dim']}
        gin = {}
        if 'hidden' in config:
            gin['hidden'] = config['hidden']
            if 'dropout' in config:
                gin['dropout'] = config['dropout']
            if 'norm' in config:
                gin['norm'] = config['norm']
            else:
                gin['norm'] = False
        cfg['gin_nn'] = gin
        return cfg, ['x', 'edge_index']

    if type == 'gcn':
        cfg = {'type': 'geo::GCNConv', 'node_dim': config['node_dim']}
        return cfg, ['x', 'edge_index']

    if type == 'sage':
        cfg = {'type': 'geo::SAGEConv', 'node_dim': config['node_dim']}
        return cfg, ['x', 'edge_index']

    if type == 'gat':
        cfg = {'type': 'geo::GATConv', 'node_dim': config['node_dim'],
               'dropout': 0.8}
        return cfg, ['x', 'edge_index']

    if type == 'res_gcn':
        cfg = {'type': 'dense::ResGCN',
               'bottleneck': config['bottleneck']}
        return cfg, ['x', 'edge_index', 'edge_attr']

    return config, ['x', 'edge_index', 'edge_attr']


def readout_module(type, config):

    if type == 'cga':
        if 'aggr' in config:
            return {
                'type': 'tasks::cga',
                'aggr': config['aggr']
            }
        return 'tasks::cga'

    if type == 'add':
        return 'geo::global_add_pool'

    if type == 'max':
        return 'geo::global_max_pool'

    if type == 'ex_cga':
        return {'type': 'mx::cga', 'out_channels': config['hid_channels']}

    return type


def layered_to_model(config):

    idc = 0
    layers = []
    readouts = []
    modules = {}
    bind = []
    current = 'source'

    for i, L in enumerate(config['layers']):
        id = 'm%i' % idc
        idc += 1
        layers.append(id)
        modules[id], req = layer_module(L)

        for r in req:
            if r == 'x':
                out = 'forward'
                if current == 'source':
                    out = 'x'
                bind.append([
                    current, out, 'x', id
                ])
            else:
                bind.append([
                    'source', r, r, id
                ])
        current = id

    for i, L in enumerate(config['readout']):
        type = L['type']
        of = i
        if 'of' in L:
            of = L['of']
        cond = []
        if 'cond' in L:
            cond = L['cond']

        id = 'm%i' % idc
        idc += 1
        modules[id] = readout_module(type, L)

        bind.append(['source', 'batch', 'batch', id])

        if type == 'cga' or type == 'ex_cga':
            bind.append(['source', 'category', 'condition', id])

        bind.append([layers[of], 'forward', 'x', id])

        if type == 'cga' or type == 'ex_cga':
            for pos in cond:
                if pos < len(readouts):
                    bind.append([
                        readouts[pos], 'forward', 'condition', id
                    ])
        readouts.append(id)

    for r in readouts:
        bind.append(
            [r, 'forward', 'input', 'sink']
        )

    return {'modules': modules, 'bind': bind}


def get_info(dataset_path, dataset_key='train'):

    dataset = proto_data.GraphDataset(
        dataset_path, dataset_key, shuffle=False
    )
    example = dataset[0]

    info = {
        'node_input': example.x.shape[1],
        'edge_input': example.edge_attr.shape[1],
        'global_input': example.category.shape[1],
        'y': example.y.shape[1]
    }
    return info


def build_global(global_att, config, out):

    cfg = {
        'type': 'tasks::ReadoutClf',
        'node_dim': out
    }

    if 'dropout' in global_att:
        drop = global_att['dropout']
        if drop > 0:
            cfg['dropout'] = drop

    if 'norm' in global_att:
        norm = global_att['norm']
        cfg['norm'] = norm

    config['modules']['clf'] = cfg

    if 'constraint' in global_att:
        gc = global_att['constraint']
        if gc:
            config['bind'].append(['source', 'category', 'input', input])

    input = 'clf'
    bind = []
    for B in config['bind']:
        if B[3] == 'sink':
            bind.append([B[0], B[1], 'input', input])
        else:
            bind.append(B)
    bind.append([input, 'forward', 'input', 'sink'])
    config['bind'] = bind


def partial_to_model_bs(config, out):
    global_att = {}

    for k, v in list(config.items()):
        if k.startswith('global_'):
            global_att[k[7:]] = v
            del config[k]

    if 'layers' in config:
        config = layered_to_model(config)

    build_global(global_att, config, out)

    return config


def partial_to_model(config, dataset_path, dataset_key='train'):

    global_att = {}

    for k, v in list(config.items()):
        if k.startswith('global_'):
            global_att[k[7:]] = v
            del config[k]

    if 'layers' in config:
        config = layered_to_model(config)

    info = get_info(dataset_path, dataset_key)
    out = info['y']
    del info['y']

    config.update(info)

    build_global(global_att, config, out)

    return config


def micro_to_partial(config):
    type = config['type']

    if type == 'edge_cga':
        layers = config['layer']
        num_layer = int((len(layers)+1)/2)
        Ls = []
        readout = []
        for i in range(num_layer):
            if i == 0:
                Ls.append({
                    'type': 'embed',
                    'node_dim': layers[0]
                })
            else:
                p = i * 2 - 1
                hid = layers[p]
                out = layers[p + 1]
                Ls.append({
                    'type': 'edge_gin',
                    'node_dim': out,
                    'hidden': hid,
                    'dropout': 0.1,
                    'norm': True
                })
            readout.append({'type': 'cga'})
        return {
            'layers': Ls,
            'readout': readout
        }

    if type == 'dense_gin':
        edge = True
        if 'edge' in config:
            edge = config['edge']
        m = 4
        if 'bm' in config:
            m = config['bm']
        Ls = [{
                'type': 'mx::DenseEdgeGIN',
                'node_dim': config['out'],
                'growth': config['growth'],
                "embed_size": config['embed_size'],
                "layers": config['layers'],
                'edge': edge,
                "bm": m
               }]
        cga = True
        if 'cga' in config:
            cga = config['cga']

        if cga:
            aggr = 'mean'
            if 'cga_aggr' in config:
                aggr = config['cga_aggr']
            readout = [
                {
                    'type': 'cga',
                    'aggr': aggr
                }
            ]
        else:
            readout = [{
                'type': 'add'
            }]
        cfg = {
            'layers': Ls,
            'readout': readout
        }

        for k, v in config.items():
            if k.startswith('global'):
                cfg[k] = v
        return cfg

    raise ValueError("Unknown Type: %s" % type)


if __name__ == '__main__':

    config = {
        'type': 'edge_cga',
        'layer': [32, 16, 8]
    }

    print(layered_to_model(micro_to_partial(config)))

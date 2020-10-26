from urllib.parse import quote_plus
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, BulkWriteError
import json
import gridfs
from tqdm import tqdm
import networkx as nx
import numpy as np

from graph_nets import graphs
from graph_nets import utils_np

__db__ = None
__client__ = {}


def setup_client(url, auth=None):
    global __client__
    if url not in __client__:
        if auth is not None:
            uri = 'mongodb://%s:%s@%s/%s' % (
                quote_plus(auth['username']),
                quote_plus(auth['password']),
                url,
                auth['authSource']
            )
        else:
            uri = 'mongodb://%s/' % url

        __client__[url] = MongoClient(uri)
    return __client__[url]


def start_mongo():
    with open("auth.json", "r") as a:
        auth = json.load(a)

    mongodb = auth["mongodb"]
    return setup_client(mongodb["url"], mongodb["auth"])


def _get_db():
    global __db__
    if __db__ is None:
        __db__ = start_mongo()
    return __db__.graph_db


def is_forward_and_parse(e):
    if e.endswith('|>'):
        return e[:-2], True
    return e[2:], False


def parse_dfs_nx(R):
    if R is None:
        return nx.MultiDiGraph()
    graph = nx.MultiDiGraph()

    for _R in R:
        graph.add_node(_R[0], label=_R[2])
        graph.add_node(_R[1], label=_R[4])
        e_label, forward = is_forward_and_parse(_R[3])
        if forward:
            graph.add_edge(_R[0], _R[1], key=e_label)
        else:
            graph.add_edge(_R[1], _R[0], key=e_label)

    return graph


def load_graph(graph_id):
    db = _get_db()
    g = db.graphs.find_one({'label_id': graph_id})

    if g is None:
        return None

    fs = gridfs.GridFS(db)
    Js = fs.get(g['minDFS']).read().decode('utf-8')
    return json.loads(Js)


def update():
    db = _get_db()
    F = db.graphs.find(filter={'label_id': {'$exists': False}}, projection=['file'])
    for L in tqdm(F, total=F.count()):
        id = L['_id']
        if 'file' not in L:
            continue

        file = L['file']
        file = file.replace("/home/cedricr/ranking/svcomp18/sv-benchmarks/../sv-benchmarks/c/", "")
        file = file.replace(".", "_")
        file = file.replace("/", "_")
        db.graphs.update_one({'_id': id}, {'$set': {'label_id': file}})


def index():
    db = _get_db()

    index = {'counter': 0}

    F = db.wl_graphs.find(filter={'iteration': 0, 'depth': 5, 'data': {'$exists': True}}, projection=['data'])
    for L in tqdm(F, total=F.count()):

        for k in L['data'].keys():
            if k not in index:
                index[k] = index['counter']
                index['counter'] += 1

    with open("index.json", "w") as o:
        json.dump(index, o, indent=4)


def _better(A, B):
    if A['solve'] > B['solve']:
        return True
    if A['time'] >= 900:
        return False
    return A['time'] < B['time']


def ranking(D):
    count = {k: 0 for k in D.keys()}

    for i1, (tool1, K1) in enumerate(D.items()):
        for i2, (tool2, K2) in enumerate(D.items()):
            if i1 < i2:
                if _better(K1, K2):
                    count[tool1] += 1
                elif _better(K2, K1):
                    count[tool2] += 1
                else:
                    count[tool1] += 0.5
                    count[tool2] += 0.5

    count = sorted(list(count.items()), key=lambda X: X[1], reverse=True)
    out = []

    for i, (k, v) in enumerate(count):
        if i > 0:
            if v == count[i - 1][1]:
                if not isinstance(out[-1], list):
                    out[-1] = [out[-1]]
                out[-1].append(k)
            else:
                out.append(k)
        else:
            out.append(k)

    return out


def graph_labels(taskType=None):
    db = _get_db()
    filter = {}
    if not(taskType is None):
        filter['type'] = taskType
    labels = db.labels.find(filter, sort=[('graph_id', 1)])

    current_label = None
    current_type = None

    M = {
        'true': 1,
        'unknown': 0,
        'false': -1
    }

    for L in labels:
        if current_label is None:
            current_label = L['graph_id']
            current_type = L['type']
            graph_label = {}
        elif current_label != L['graph_id'] or current_type != L['type']:
            r = ranking(graph_label)
            yield (current_label, current_type, r)
            current_label = L['graph_id']
            current_type = L['type']
            graph_label = {}

        graph_label[L['tool']] = {
            'solve': M[L['solve']],
            'time': L['time']
        }


def stream_graph_label(taskType=None):
    for (graph_id, type, rank) in graph_labels(taskType):
        G = load_graph(graph_id)

        if G is None:
            print("Unknown id %s." % graph_id)
            continue

        yield (G, type, rank)


def load_wl0(graph_id):
    db = _get_db()
    cursor = db.wl_graphs.find_one(
        {
            'graph_id': graph_id,
            'iteration': 0,
            'depth': 5
        }
    )

    if cursor is None:
        return None

    return cursor['data']


def stream_wl0(taskType=None):
    for (graph_id, type, rank) in graph_labels(taskType):
        G = load_wl0(graph_id)

        if G is None:
            print("Unknown id %s." % graph_id)
            continue

        yield (G, type, rank)


def stream_wl0_to_file(taskType=None):
    data = []
    labels = []

    for (graph, type, rank) in tqdm(stream_wl0(), total=6232):
        data.append(graph)
        labels.append(rank)

    with open("data.json", "w") as o:
        json.dump(data, o, indent=4)

    with open("labels.json", "w") as o:
        json.dump(labels, o, indent=4)


def _simple_linear(graph, root, ast_index, ast_count, depth):
    index = {n: i for i, n in enumerate(graph.nodes())}
    ast_rev = {v: k for k, v in ast_index.items()}

    A = np.zeros((len(index), len(index)))
    D = np.zeros((len(index),))
    X = []

    for n, label in graph.nodes(data='label'):
        x = np.zeros((ast_count,))
        x[ast_index[label]] = 1
        X.append(x)

        A[index[n], index[n]] = 1

    for u, v in graph.edges():
        A[index[u], index[v]] = 1
        A[index[v], index[u]] = 1

    D = np.sum(A, axis=1)
    D = np.diag(1/np.sqrt(D))
    S = D.dot(A).dot(D)

    X = np.vstack(X)

    S = np.linalg.matrix_power(S, depth)
    X = S.dot(X)

    return X[index[root], :]


def _compress_node2(graph, n, ast_index, ast_count):
    ast_set = set([])

    queue = [n]

    while len(queue) > 0:
        k = queue.pop()

        ast_set.add(k)

        for u, _, label in graph.in_edges(k, keys=True):
            if label == 's':
                queue.append(u)

    G_ast = graph.subgraph(ast_set)
    vec = _simple_linear(G_ast, n, ast_index, ast_count, 6)

    graph.nodes[n]['features'] = vec

    ast_set.remove(n)

    return ast_set


def _compress_node(graph, n, ast_index, ast_count):
    ast_set = set([])

    queue = [n]

    while len(queue) > 0:
        k = queue.pop()

        for u, _, label in graph.in_edges(k, keys=True):
            if label == 's':
                ast_set.add(u)
                queue.append(u)

    label_vec = np.zeros((ast_count,))
    pos_ast = [n]
    pos_ast.extend(list(ast_set))

    for ast in pos_ast:
        node = graph.nodes[ast]
        label_vec[ast_index[node['label']]] += 1

    graph.nodes[n]['features'] = label_vec

    return ast_set


def compress_graph(graph, ast_index, ast_count):
    if 'count' not in ast_index:
        ast_index['count'] = 0

    for n in graph.nodes():
        node = graph.nodes[n]
        label = node['label']
        if label not in ast_index:
            ast_index[label] = ast_index['count']
            ast_index['count'] += 1

    if ast_index['count'] > ast_count:
        raise ValueError("Detect at least %i AST labels" % ast_index['count'])

    cfg_nodes = set([])

    for u, v, label in graph.edges(keys=True):
        if label == 'cfg':
            cfg_nodes.add(u)
            cfg_nodes.add(v)

    ast = set([])
    for cfg_node in cfg_nodes:
        ast = ast.union(
            _compress_node2(graph, cfg_node, ast_index, ast_count)
        )

    graph.remove_nodes_from(ast)

    feature_index = {
        'cfg': 0,
        'dd': 1,
        'cd': 2
    }

    for u, v, key in graph.edges(keys=True):
        feature = np.zeros((3,))
        feature[feature_index[key]] = 1
        graph.edges[u, v, key]['features'] = feature


def stream_compress_label(ast_index, ast_count, taskType=None):
    for (graph_id, type, rank) in graph_labels(taskType):
        G = load_graph(graph_id)

        if G is None:
            print("Unknown id %s." % graph_id)
            continue

        G = parse_dfs_nx(G)
        l = len(G.nodes())
        compress_graph(G, ast_index, ast_count)
        print("Compression: %f" % ((l - len(G.nodes())) / float(l)))

        yield (G, type, rank)


def to_custom_dict(graph):
    count = 0
    node_index = {}

    node_array = []

    for n, features in graph.nodes(data='features'):
        node_index[n] = count
        count += 1

        node_embed = []
        for i in range(features.shape[0]):
            val = features[i]
            if val > 0:
                node_embed.append((i, val))
        node_array.append(node_embed)

    # node_array = np.vstack(node_array)

    feature_index = {
        'cfg': 0,
        'dd': 1,
        'cd': 2
    }

    edges = []

    for u, v, key in graph.edges(keys=True):
        uix = node_index[u]
        vix = node_index[v]
        keyix = feature_index[key]
        edges.append((uix, vix, keyix))

    return {
        'nodes': node_array,
        'edges': edges
    }


def print_graphs_tuple(graphs_tuple):
    print("Shapes of `GraphsTuple`'s fields:")
    print(graphs_tuple.map(lambda x: x if x is None else x.shape, fields=graphs.ALL_FIELDS))
    print("\nData contained in `GraphsTuple`'s fields:")
    print("globals:\n{}".format(graphs_tuple.globals))
    print("nodes:\n{}".format(graphs_tuple.nodes))
    print("edges:\n{}".format(graphs_tuple.edges))
    print("senders:\n{}".format(graphs_tuple.senders))
    print("receivers:\n{}".format(graphs_tuple.receivers))
    print("n_node:\n{}".format(graphs_tuple.n_node))
    print("n_edge:\n{}".format(graphs_tuple.n_edge))


if __name__ == '__main__':
    ast_index = {}
    ast_count = 39
    i = 1
    for graph, type, rank in stream_compress_label(ast_index, ast_count, taskType="reachability"):

        D = to_custom_dict(graph)

        # D['nodes'] = D['nodes'].tolist()

        with open('graph.json', 'w') as o:
            json.dump(D, o)

        i -= 1
        if i <= 0:
            break
    print(ast_index['count'])

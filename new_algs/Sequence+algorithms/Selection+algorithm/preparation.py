import taskflow as tsk
from taskflow import task_definition
from taskflow.distributed import openRemoteSession

from tasks.data.dataset_tasks import load_graph

import numpy as np
import json
import random
from gridfs import GridFS
import time
import traceback

from bson.objectid import ObjectId
import hashlib


def subsample_graph(graph, root, size):

    if size > len(graph.nodes()):
        return list(graph.nodes())

    # print("Has to subsample as %i > %i (%s)" % (len(graph.nodes()), size, str(graph.nodes[root]['label'])))

    depths = {}
    seen = set([])

    queue = [(root, 0)]

    while len(queue) > 0:
        node, depth = queue.pop()

        if node in seen:
            continue

        if depth not in depths:
            depths[depth] = []

        depths[depth].append(node)
        seen.add(node)

        for v, _ in graph.in_edges(node):
            queue.append((v, depth + 1))

    sample = []

    i = 0
    while i < len(depths) and len(sample) + len(depths[i]) <= size:
        sample.extend(depths[i])
        i += 1

    if i < len(depths) and size - len(sample) > 0:
        sample.extend(random.sample(depths[i], size - len(sample)))

    return sample


def _simple_linear(graph, root, ast_index, ast_count, depth, sub_sample=50, verbose=False):
    index = {n: i for i, n in enumerate(subsample_graph(graph, root, sub_sample))}

    A = np.zeros((len(index), len(index)))
    D = np.zeros((len(index),))
    X = []

    for n in index.keys():
        label = graph.nodes[n]['label']
        x = np.zeros((ast_count,))
        x[ast_index[label]] = 1
        X.append(x)

        A[index[n], index[n]] = 1

    for u, v in graph.edges(index.keys()):
        if v not in index:
            continue
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


def compress_graph(graph, ast_index, ast_count, compress_func):
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
    max_ast = 0
    for cfg_node in cfg_nodes:
        comp = compress_func(graph, cfg_node, ast_index, ast_count)
        max_ast = max(max_ast, len(comp))
        ast = ast.union(
            comp
        )

    graph.remove_nodes_from(ast)

    for n in graph.nodes():
        node = graph.nodes[n]
        if 'features' not in node:
            node['features'] = np.zeros((ast_count,))
            node['features'][ast_index[node['label']]] = 1

    feature_index = {
        'cfg': 0,
        'dd': 1,
        'cd': 2,
        'cd_f': 2,
        'cd_t': 2
    }

    for u, v, key in graph.edges(keys=True):
        if key == 'du':
            continue
        feature = np.zeros((3,))
        feature[feature_index[key]] = 1
        graph.edges[u, v, key]['features'] = feature

    return max_ast


def to_custom_dict(graph, attr={}, return_index=False):
    count = 0
    node_index = {}

    node_array = []
    attr_array = []

    for n, features in graph.nodes(data='features'):
        node_index[n] = count
        count += 1

        if features is None:
            continue

        node_embed = []
        for i in range(features.shape[0]):
            val = features[i]
            if val > 0:
                node_embed.append((i, val))
        node_array.append(node_embed)

        if len(attr) > 0:
            if n in attr:
                attr_array.append(attr[n])
            else:
                attr_array.append(None)

    # node_array = np.vstack(node_array)

    feature_index = {
        'cfg': 0,
        'dd': 1,
        'cd': 2,
        'cd_f': 2,
        'cd_t': 2
    }

    edges = []

    for u, v, key in graph.edges(keys=True):
        if key == 'du':
            continue
        uix = node_index[u]
        vix = node_index[v]
        keyix = feature_index[key]
        edges.append((uix, vix, keyix))

    res = {
        'nodes': node_array,
        'edges': edges
    }

    if len(attr_array) > 0:
        res['attributes'] = attr_array

    if return_index:
        return res, node_index

    return res


def collect_statistics(db, G, task_info):
    name = G.graph['name']

    graph_stats = db.graph_statistics

    if graph_stats.find_one({'name': name,
                            'competition': task_info['svcomp']}) is not None:
        print("Statistics for %s already exists." % name)
        return

    ast_nodes = 0
    cfg_nodes = 0
    cfg_edges = 0
    pdg_edges = 0
    max_in_degree = 0
    max_out_degree = 0

    for n in G:
        if '_' in n:
            ast_nodes += 1
            continue
        else:
            cfg_nodes += 1

        max_in_degree = max(max_in_degree, G.in_degree(n) - 1)
        max_out_degree = max(max_out_degree, G.out_degree(n))

    for u, v, k in G.edges(keys=True):
        if '_' in u:
            continue
        if '_' in v:
            continue
        if 'cfg' == k:
            cfg_edges += 1
        else:
            pdg_edges += 1

    try:
        graph_stats.insert_one({
            'name': name,
            'competition': task_info['svcomp'],
            'ast_nodes': ast_nodes,
            'cfg_nodes': cfg_nodes,
            'cfg_edges': cfg_edges,
            'pdg_edges': pdg_edges,
            'max_in_degree': max_in_degree,
            'max_out_degree': max_out_degree
        })
    except Exception:
        print("Fail stats")
        traceback.print_exc()
        pass


@task_definition()
def load_svcomp_ids(competition, env=None):

    svcomp = env.get_db().svcomp

    g = set([])
    ids = []
    for f in svcomp.find({"svcomp": competition, 'graph_ref': {"$exists": 1}},
                         ['_id', 'name']):
        if f['name'] in g:
            continue
        g.add(f['name'])
        ids.append(f['_id'])

    return ids


@task_definition(timeout=600)
def ast_features_graph(task_id, sub_sample, env=None):
    graph = load_graph(task_id, env)

    db = env.get_db()
    task_info = db.svcomp.find_one({'_id': task_id})

    print("Statistics")
    collect_statistics(db, graph, task_info)

    ast_graph = db.ast_graph
    cache = db.cache

    id = graph.graph['reference']

    ast = ast_graph.find_one({'_id': id})

    if ast is not None:
        print("Already found ast_graph for id %s [comp: %s]" % (id, ast['competition']))
        return ast['_id']

    ast_index = {}
    ast_count = 158
    p = cache.find_one({'_id': 'ast_index'})

    if p is not None:
        ast_index = p['value']
        ast_count = ast_index['count']

    print("Start")
    try:

        start_time = time.time()

        ma = compress_graph(graph, ast_index, ast_count, _compress_node2)

        graph_repr = json.dumps(
            to_custom_dict(graph)
        )

        run_time = time.time() - start_time

        graph_id = ObjectId()

        try:
            print("Insert")
            ast_graph.insert_one({
                '_id': id,
                'name': graph.graph['name'],
                'sub_sample': sub_sample,
                'max_ast': ma,
                'competition': task_info['svcomp'],
                'run_time': run_time,
                'graph_ref': graph_id
            })
            fs = GridFS(env.get_db())
            fs.put(
                graph_repr.encode('utf-8'), _id=graph_id,
                name=graph.graph['name'],
                app_type="ast_graph"
            )
        except Exception:
            traceback.print_exc()
            print("Fail")

    finally:
        cache.update_one({'_id': 'ast_index'},
                         {'$set': {'value': ast_index}},
                         upsert=True)


@task_definition(timeout=600)
def ast_features_bag(task_id, sub_sample, env=None):
    graph = load_graph(task_id, env)

    db = env.get_db()

    task_info = db.svcomp.find_one({'_id': task_id})
    collect_statistics(db, graph, task_info)

    ast_graph = db.ast_bag
    cache = db.cache

    id = graph.graph['reference']

    ast = ast_graph.find_one({'_id': id})

    if ast is not None:
        print("Already found ast bag for id %s [comp: %s]" % (id, ast['competition']))
        return ast['_id']

    ast_index = {}
    ast_count = 158
    p = cache.find_one({'_id': 'ast_index'})

    if p is not None:
        ast_index = p['value']
        ast_count = ast_index['count']

    try:

        start_time = time.time()

        ma = compress_graph(graph, ast_index, ast_count, _compress_node)

        graph_repr = json.dumps(
            to_custom_dict(graph)
        )

        run_time = time.time() - start_time

        graph_id = ObjectId()

        try:
            ast_graph.insert_one({
                '_id': id,
                'name': graph.graph['name'],
                'sub_sample': sub_sample,
                'competition': task_info['svcomp'],
                'max_ast': ma,
                'run_time': run_time,
                'graph_ref': graph_id
            })
            fs = GridFS(env.get_db())
            fs.put(
                graph_repr.encode('utf-8'), _id=graph_id,
                name=graph.graph['name'],
                app_type="ast_bag"
            )
        except Exception:
            traceback.print_exc()

    finally:
        cache.update_one({'_id': 'ast_index'},
                         {'$set': {'value': ast_index}},
                         upsert=True)


def run_wl_node(graph, n, depth, label={}):

    core_node = graph.nodes[n]

    if 'depth' in core_node and core_node['depth'] > depth:
        return None

    neigh = []

    for _, v, k in graph.in_edges(n, keys=True):
        node = graph.nodes[v]
        if 'depth' in node and node['depth'] > depth:
            continue
        if v in label:
            L = label[v]
        else:
            L = node['label']
        neigh.append(k+"_"+str(L))

    neigh = sorted(neigh)

    if n in label:
        core = label[n]
    else:
        core = core_node['label']

    neigh.insert(0, core)

    ret = '_'.join(neigh)
    return hashlib.blake2b(ret.encode('utf-8')).hexdigest()


def run_wl(graph, depth, label={}):
    next_label = {}
    count = {}

    for n in graph:
        L = run_wl_node(graph, n, depth, label)
        if L is None:
            continue
        next_label[n] = L
        if L not in count:
            count[L] = 0
        count[L] += 1

    return count, next_label


def count_wl(graph, depth):
    count = {}

    for n in graph:
        L = graph.nodes[n]['label']
        if L not in count:
            count[L] = 0
        count[L] += 1

    return count


@task_definition(timeout=600)
def wl_features_bag(task_id, iteration, depth, env=None):
    graph = load_graph(task_id, env)

    db = env.get_db()
    task_info = db.svcomp.find_one({'_id': task_id})

    collect_statistics(db, graph, task_info)

    ast_graph = db.wl_features

    id = graph.graph['reference']

    ast = ast_graph.find_one({'_id': id})

    if ast is not None:
        print("Already found wl features for id %s [comp: %s]" % (id, ast['competition']))
        return ast['_id']

    start_time = time.time()

    its = [count_wl(graph, depth)]
    label = {}
    for _ in range(iteration):
        c, label = run_wl(graph, depth, label)
        its.append(c)

    run_time = time.time() - start_time

    try:

        fs = GridFS(env.get_db())
        refs = [fs.put(
            json.dumps(it).encode('utf-8'), name=graph.graph['name'],
            app_type="wl_feature", iteration=i
        ) for i, it in enumerate(its)]

        ast_graph.insert_one({
            '_id': id,
            'run_time': run_time,
            'name': task_info['name'],
            'competition': task_info['svcomp'],
            'max_depth': depth,
            'wl_refs': refs
        })

    except Exception:
        traceback.print_exc()


if __name__ == '__main__':
    ids = load_svcomp_ids("2019")
    id_it = tsk.fork(ids)
    cgraph = ast_features_graph(id_it, 5000)
    cbag = ast_features_bag(id_it, 5000)
    wl = wl_features_bag(id_it, 5, 5)
    m = tsk.merge([cgraph])

    with openRemoteSession(
        session_id="317e3bb0-caf4-4f57-9975-0e782371a866"
    ) as sess:
        sess.run(m)

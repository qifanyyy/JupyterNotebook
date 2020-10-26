import taskflow as tsk
from taskflow import task_definition, backend

from tasks.dataset_tasks import load_graph

import numpy as np
import json
import random
from gridfs import GridFS
import time
import traceback

from bson.objectid import ObjectId
import hashlib


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
            node['features'] = np.zeros((ast_count,), dtype=np.uint64)
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


def to_custom_dict(graph):
    count = 0
    node_index = {}

    node_array = []

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

    return {
        'nodes': node_array,
        'edges': edges
    }


@task_definition()
def ast_features_bag(task_id, sub_sample, env=None):
    graph = load_graph(task_id, env)

    db = env.get_db()
    cache = db.cache

    ast_index = {}
    ast_count = 158
    p = cache.find_one({'_id': 'ast_index'})

    if p is not None:
        ast_index = p['value']
        ast_count = ast_index['count']

    compress_graph(graph, ast_index, ast_count, _compress_node)

    return to_custom_dict(graph)


if __name__ == '__main__':
    with backend.openLocalSession(auto_join=True) as sess:
        sess.run(
            ast_features_bag(
                ObjectId('74035f92e3c4af2f87680e0d'),
                5000
            )
        )

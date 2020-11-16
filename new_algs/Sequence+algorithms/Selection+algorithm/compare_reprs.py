from taskflow import config as cfg
from urllib.parse import quote_plus
from pymongo import MongoClient

import argparse
from gridfs import GridFS
from tqdm import tqdm
import os
import json
import numpy as np

import torch as th
from torch_geometric.data import Data, Batch
from torch_geometric.nn import global_add_pool


__config__ = None

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
    config = get_config()

    if len(config) == 0:
        return None

    if 'execution' not in config:
        return None

    auth = config['execution']
    mongodb = auth["mongodb"]
    return setup_client(mongodb["url"], mongodb["auth"])


def get_db():
    global __db__
    if __db__ is None:
        __db__ = start_mongo()

    config = get_config()
    if 'execution' not in config:
        return None

    return __db__[__config__['execution']['mongodb']['database']]


def get_config():
    global __config__

    if __config__ is None:
        __config__ = cfg.load_config(failing_default={})

    return __config__


def _map_to_vec(D, index):
    vec = np.zeros(index['count'], dtype=np.uint64)

    for d, c in D.items():
        if d not in index:
            print("Unknown label %s" % d)
            continue
        vec[index[d]] = c

    return vec


def load_wl(db, name, comp, index):
    fs = GridFS(db)
    files = db['fs.files']

    f = files.find_one({'name': name, 'competition': comp, 'app_type': 'code_graph'})
    if f is None:
        raise ValueError("Wl %s is non-existing." % name)

    wl = db.wl_features.find_one({'_id': f['_id']})
    fs_file = fs.get(wl['wl_refs'][0])
    D = json.loads(fs_file.read().decode('utf-8'))
    return _map_to_vec(D, index)


def _bag_to_vec(bag, index):
    vec = np.zeros(index['count'], dtype=np.uint64)

    for node in bag['nodes']:
        for p, v in node:
            vec[p] += v

    return vec


def load_bag(db, name, comp, index):
    fs = GridFS(db)
    graphs = db.ast_bag

    f = graphs.find_one({'name': name, 'competition': comp})

    if f is None:
        raise ValueError("Graph %s is non-existing." % name)

    file = fs.get(f['graph_ref']).read().decode('utf-8')
    file = json.loads(file)

    return _bag_to_vec(file, index)


def create_data(data, features):

    nrow = []
    ncol = []
    ncont = []

    for i, feat in enumerate(data['nodes']):
        for p, v in feat:
            nrow.append(i)
            ncol.append(p)
            ncont.append(v)

    nodes_len = max(nrow)+1
    index = th.LongTensor([nrow, ncol])
    nodes = th.FloatTensor(ncont)

    x = th.sparse.FloatTensor(index, nodes, th.Size([nodes_len, features]))
    x = x.to_dense()

    return Data(x=x)


def load_bag_th(db, name, comp, index):
    fs = GridFS(db)
    graphs = db.ast_bag

    f = graphs.find_one({'name': name, 'competition': comp})

    if f is None:
        raise ValueError("Graph %s is non-existing." % name)

    file = fs.get(f['graph_ref']).read().decode('utf-8')
    file = json.loads(file)

    data = create_data(file, index['count'])
    batch = Batch.from_data_list([data])

    return global_add_pool(batch.x, batch.batch).numpy()


def compare(name, vec0, vec1):

    c = np.linalg.norm(vec0 - vec1)
    if c > 0:
        dif = vec0 - vec1
        dif = dif.nonzero()[0]
        s = ''
        for i in range(dif.shape[0]):
            pos = dif[i]
            a = vec0[pos]
            b = vec1[pos]
            s = s + "[%d] wl %d != bag %d\n" % (pos, a, b)
        print("%s: \n %s" % (name, s))


parser = argparse.ArgumentParser()
parser.add_argument("split_key")

args = parser.parse_args()

db = get_db()
split = db.data_split

sp = split.find_one({'key': args.split_key})
search = set.union(set(sp['train']), set(sp['test']))

cache = db.cache

ast_index = cache.find_one({'_id': 'ast_index'})
if ast_index is None:
    ast_index = {}
else:
    ast_index = ast_index['value']

comp = sp['competition']

for s in tqdm(search):
    try:
        vec0 = load_wl(db, s, comp, ast_index)
        vec1 = load_bag_th(db, s, comp, ast_index)
        compare(s, vec0, vec1)
    except ValueError:
        print("%s is missing" % s)

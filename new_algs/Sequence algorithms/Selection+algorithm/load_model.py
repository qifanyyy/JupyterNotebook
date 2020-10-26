from taskflow import config as cfg
from urllib.parse import quote_plus
from pymongo import MongoClient

from gridfs import GridFS
from tqdm import tqdm
from bson.objectid import ObjectId
from tasks.torch_model import build_model_from_config
from tasks.torch_execute import tensor_len, model_seq
import torch as th
import os
import json

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


def get_experiment_info():
    db = get_db()
    models = db.torch_models

    options = {}

    for o in models.find({}, ['dataset', 'model_key', 'spearmann']):
        key = (o['dataset'], o['model_key'])
        if key in options:
            opt = options[key]
            if o['spearmann']['mean'] > opt['score']:
                opt['id'] = o['_id']
                opt['score'] = o['spearmann']['mean']
        else:
            options[key] = {'id': o['_id'], 'score': o['spearmann']['mean']}

    ret = {}
    for k, v in options.items():
        if k[0] not in ret:
            ret[k[0]] = {}
        if k[1] not in ret[k[0]]:
            ret[k[0]][k[1]] = (str(v['id']), v['score'])
    return ret


def load_model(id):
    db = get_db()
    models = db.torch_models

    f = models.find_one({'_id': ObjectId(id)})
    if f is None:
        raise ValueError("Unknown model %s" % id)

    fs = GridFS(db)
    with open("model.th", "wb") as o:
        o.write(fs.get(f['model_ref']).read())


def get_ast_index():
    db = get_db()
    cache = db.cache

    a = cache.find_one({'_id': 'ast_index'})
    with open("ast.json", "w") as o:
        json.dump(a['value'], o)


if __name__ == '__main__':
    get_ast_index()

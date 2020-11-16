from taskflow import config as cfg
from urllib.parse import quote_plus
from pymongo import MongoClient

import argparse
from gridfs import GridFS
from tqdm import tqdm
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


db = get_db()
graph = db.wl_features
stat = db.kernels

sizes = {}
cursor = stat.find({'run_time': {'$exists': 1}}, ['kernel_id', 'run_time'])

times = {}

for obj in tqdm(cursor, total=cursor.count()):
    kernel_id = obj['kernel_id']
    if '2018' in kernel_id:
        if 'add' in kernel_id:
            _, ix = kernel_id.split('_', 1)
            _, ix = ix.split('_', 1)
            ix, _ = ix.split('_', 1)
            if int(ix) <= 2:
                times[kernel_id] = obj['run_time']
        elif 'norm' in kernel_id:
            ix = int(kernel_id[-1])
            if ix <= 2:
                times[kernel_id] = obj['run_time']
        else:
            _, ix = kernel_id.split('_', 1)
            ix, _ = ix.split('_', 1)
            if int(ix) <= 2:
                times[kernel_id] = obj['run_time']

kernel_time = 0.0
for t in times.values():
    kernel_time += t
print(kernel_time / 8456)

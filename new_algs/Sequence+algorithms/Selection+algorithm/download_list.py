import os
from taskflow import config as cfg
from urllib.parse import quote_plus
from pymongo import MongoClient

import argparse
from gridfs import GridFS
from tqdm import tqdm

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("list")
    parser.add_argument("out")

    args = parser.parse_args()
    name = args.list

    db = get_db()
    graph = db.data_split

    cat = ['overall', 'reachability', 'termination', 'memory', 'overflow']

    for c in cat:
        for i in range(10):
            kname = name + "_%s_%i" % (c, i)
            print(kname)

            obj = graph.find_one({'key': kname})

            if obj is None:
                print("Key %s does not exists")

            train = os.path.join(args.out, kname+"_train.txt")
            test = os.path.join(args.out, kname+"_test.txt")

            with open(train, "w") as o:
                for n in tqdm(obj['train']):
                    o.write(n+"\n")

            with open(test, "w") as o:
                for n in tqdm(obj['test']):
                    o.write(n+"\n")

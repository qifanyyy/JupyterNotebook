from taskflow import config as cfg
from urllib.parse import quote_plus
from pymongo import MongoClient

import argparse
from gridfs import GridFS
from tqdm import tqdm
import json
import shutil
from tasks.torch.model_config import partial_to_model_bs, micro_to_partial

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
    parser.add_argument("config")
    parser.add_argument("result")
    parser.add_argument("model")
    args = parser.parse_args()

    dataset = "rank18_overall_0"

    db = get_db()

    with open(args.config, "r") as i:
        config = json.load(i)

    with open(args.result, "r") as i:
        result = json.load(i)

    model_config = config['model']

    if 'type' in model_config:
        model_config = micro_to_partial(model_config)

    info = {
        "node_input": 148,
        "edge_input": 3,
        "global_input": 4
    }

    model_config.update(info)

    if 'layers' in model_config:
        model_config = partial_to_model_bs(model_config, 45)
        model_config.update(info)

    print("Upload model")
    fs = GridFS(db)
    file = fs.new_file(model=config['name'],
                       dataset_key=dataset,
                       app_type='torch_model',
                       encoding="utf-8")

    try:
        with open(args.model, "rb") as i:
            shutil.copyfileobj(i, file)
    finally:
        file.close()

    insert = {
        'experiment': config['name'],
        'dataset': dataset,
        'competition': '2018',
        'category': None,
        'experiment_def': {'model': model_config},
        'model_ref': file._id,
        'tools': config['tools']
    }

    insert.update(result)

    print("Upload result")
    models = db.torch_experiment
    models.insert_one(insert)

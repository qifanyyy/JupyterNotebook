from taskflow import config as cfg
from urllib.parse import quote_plus
from pymongo import MongoClient

from gridfs import GridFS
from tqdm import tqdm
from bson.objectid import ObjectId
import json
import numpy as np

from sklearn.model_selection import KFold
from tasks.utils import train_utils as tu

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


def dict_to_set(D):
    D = D['index']
    del D['counter']
    return set([
        n.replace("/", "_").replace(".", "_")
        for n in D.keys()
    ])


def create_split(key, category=None):

    db = get_db()
    data_split = db.data_split

    with open("svcomp18.json", "r") as i:
        sv = json.load(i)
    sv = dict_to_set(sv)

    get_names = tu.retrieve_benchmark_names(db, "2018", category=category)

    names = set([])
    for name in tqdm(get_names):
        if name in sv:
            names.add(name)

    names = np.array(list(names))

    kf = KFold(n_splits=10, shuffle=True)

    name_split = [
        ["%s_%i" % (key, i), names[train].tolist(), names[test].tolist()]
        for i, (train, test) in enumerate(kf.split(names))
    ]

    for id, names_train, names_test in name_split:
        test_ratio = len(names_test) / (len(names_train) + len(names_test))
        data_split.insert_one({
            'key': id, 'competition': "2018",
            'category': category,
            'test_ratio': test_ratio, 'train': names_train, 'test': names_test,
            'train_size': len(names_train), 'test_size': len(names_test),
            'crossval': key
        })


def get_stats(key):
    db = get_db()
    data_split = db.data_split
    stats = db.graph_statistics

    obj = data_split.find_one({"crossval": key})

    names = set.union(set(obj['train']), set(obj['test']))

    nodes = []
    edges = []

    search = ['unreach-call', '-termination_', '-no-overflow', 'valid-']

    for n in tqdm(names):
        stat = stats.find_one({'name': n, 'competition': '2018'})
        if stat is None:
            continue
        for s in search:
            if s in n:
                nodes.append(
                    stat['cfg_nodes']
                )
                edges.append(
                    stat['cfg_edges'] + stat['pdg_edges']
                )

    print("Size: %i" % len(nodes))
    print("Nodes: %f (+- %f)" % (np.mean(nodes), np.std(nodes)))
    print("Edges: %f (+- %f)" % (np.mean(edges), np.std(edges)))


if __name__ == '__main__':
    get_stats("rank18_overall")

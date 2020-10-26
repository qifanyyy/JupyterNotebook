import argparse
import os
import json
import numpy as np
from tqdm import tqdm
import lmdb
import traceback
import shutil
import zipfile


from tasks.utils import train_utils as tu
from tasks.data import proto_data as ptd


def info_gen(ranks, Ix, cat=None):
        for task, V in tqdm(ranks.items()):
            if task not in Ix:
                continue
            for category, rank in V.items():
                if len(rank) == 0:
                    continue
                if cat is not 'all' and category is not cat:
                    continue
                yield (task, category, rank)


def load_task(base_path, task):
    graph = os.path.join(base_path, 'graphs', task+".json")

    if not os.path.exists(graph):
        raise ValueError("Graph does not exists: %s" % task)

    with open(graph, "r") as i:
        return json.load(i)


def rank_to_vec(rank, tools=None):

    ri = {}

    for i, r in enumerate(rank):
        if isinstance(r, list):
            for _r in r:
                ri[_r] = i
        else:
            ri[r] = i

    if tools is None:
        tools = list(ri.keys())

    n = len(tools)
    pref = np.zeros((int(n*(n-1)/2)))
    for i in range(n-1):
        for j in range(i+1, n):
            t1 = tools[i]
            t2 = tools[j]
            p = tu.index(i, j, n)

            d = ri[t1] - ri[t2]
            if d < 0:
                pref[p] = 1
            elif d > 0:
                pref[p] = 0
            else:
                pref[p] = 0.5
    return pref, tools


def get_name(index_path):
    name = os.path.basename(index_path)
    name, _ = name.split('.')
    print(name)
    return name


def to_lmdb(name, ranks, index, cat=None):
    cat_name = cat
    if cat_name is None:
        cat_name = 'all'
    out = os.path.join(args.base_path,
                       name)

    if not os.path.exists(out):
        os.makedirs(out)

    tools = None

    with lmdb.open(out, map_size=1048576*100000,
                   sync=False,
                   metasync=False,
                   map_async=True,
                   writemap=True,
                   max_dbs=2) as lm:
        with lm.begin(write=True) as txn:
            train_db = lm.open_db('data'.encode('ascii'), txn)
            train_i = 0
            for task, cat, rank in tqdm(info_gen(ranks, index, cat_name)):
                try:
                    file = load_task(args.base_path, task)

                    pref, tools = rank_to_vec(rank, tools)
                    data = ptd.create_data(file, cat, pref)
                    data_ser = data.SerializeToString()
                    id = 'graph_%d' % train_i
                    txn.put(
                        id.encode('ascii'),
                        data_ser,
                        db=train_db
                    )
                    train_i += 1

                except Exception:
                    traceback.print_exc()
                    continue

        lm.sync(True)
        return out


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            root_ = os.path.basename(os.path.normpath(root))
            print(root_)
            ziph.write(os.path.join(root, file), arcname=os.path.join(root_,
                                                                      file))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('index')
    parser.add_argument('rank_index')
    parser.add_argument('base_path')

    parser.add_argument("-c", '--category', type=int, default=-1)

    args = parser.parse_args()

    cats = ['reachability', 'termination', 'memory', 'overflow']

    cat = None
    if args.category >= 0:
        cat = cats[args.category]

    with open(args.index, 'r') as i:
        Ix = set([k[:-1] for k in i.readlines()])

    with open(args.rank_index, 'r') as i:
        ranks = json.load(i)

    name = get_name(args.index)

    db = to_lmdb(name, ranks, Ix, cat)

    tmp = os.path.abspath(os.path.join(db, "..", "tmp"))
    base = os.path.basename(os.path.normpath(db))
    target = os.path.abspath(os.path.join(db, "..", base+".zip"))

    os.makedirs(tmp)

    print("Copying %s..." % db)
    cdb = lmdb.open(db)
    cdb.copy(tmp, compact=True)

    print("Deleting %s..." % db)
    shutil.rmtree(db)

    print("Moving tmp...")
    shutil.move(tmp, db)

    print("Zip to %s" % target)
    zipf = zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED)
    zipdir(db, zipf)
    zipf.close()

    print("Deleting %s..." % db)
    shutil.rmtree(db)

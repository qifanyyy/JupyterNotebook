import taskflow as tsk
from taskflow import task_definition, backend
from taskflow.distributed import openRemoteSession
from tasks.baseline import logistic_regression as loader

from tasks.utils import train_utils as tu

import os
from gridfs import GridFS
from bson.objectid import ObjectId
from pymongo import UpdateOne
from tqdm import tqdm
import json
import numpy as np
from scipy.sparse import coo_matrix
from tqdm import trange
from time import time
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score


def _localize_wl(fs, wl_col, id, iteration, depth, index):
    wl_item = wl_col.find_one({'_id': id, 'max_depth': depth})

    if wl_item is None:
        raise ValueError("Unknown id %s for depth %d." % (str(id), depth))

    wl_refs = wl_item['wl_refs']
    if iteration >= len(wl_refs):
        raise ValueError("ID %s exists not for iteration %d" % (str(id), iteration))

    D = json.loads(fs.get(wl_refs[iteration]).read().decode('utf-8'))
    R = {}

    for p, v in D.items():
        if p not in index:
            index[p] = index['count']
            index['count'] += 1
        R[index[p]] = v
    return R


def _bag_to_vec(bag, n):
    vec = np.zeros(n, dtype=np.uint64)

    for p, v in bag.items():
        vec[p] = v

    return vec


def _localize_wls(db, ids, iteration, depth, ast_index):
    wl = db.wl_features
    fs = GridFS(db)

    result = {}
    for id in ids:
        result[id] = _localize_wl(fs, wl, id, iteration,
                                  depth, ast_index)

    for id in ids:
        D = _bag_to_vec(result[id], ast_index['count'])
        result[id] = D

    return result


@task_definition()
def load_wl_ids(competition, env=None):

    if env is None:
        raise ValueError("train_test_split needs an execution context")

    db = env.get_db()
    wl = db.wl_features

    wls = wl.find({'competition': competition}, ['_id'])
    return [w['_id'] for w in wls]


@task_definition()
def dual_scatter(iterable, n, index=False):
    print("Scatter")
    sc = [[] for _ in range(n)]

    for i, value in enumerate(iterable):
        sc[i % n].append(value)

    dual = []
    for i in range(n):
        for j in range(i, n):
            if index:
                dual.append([i, j, sc[i], sc[j]])
            else:
                dual.append([sc[i], sc[j]])

    return dual


@task_definition()
def concat_strs(a, b, c=None, d=None, e=None, f=None, g=None):
    return '_'.join([str(l) for l in [a, b, c, d, e, f, g] if l is not None])


@task_definition()
def task_tuple(a, b, c=None, d=None, e=None, f=None, g=None):
    return (l for l in [a, b, c, d, e, f, g] if l is not None)


def to_matrix(ids, wls):
    r = [wls[id] for id in ids]
    r = np.vstack(r)
    return r


def _jaccard_between(X, Y):

    min_sum = np.minimum(X, Y).sum(axis=1, dtype=np.float64)
    max_sum = np.maximum(X, Y).sum(axis=1, dtype=np.float64)

    return min_sum / max_sum


def jaccard_kernel(X):
    row = list(range(X.shape[0]))
    columns = list(range(X.shape[0]))
    data = [1] * X.shape[0]

    for i in trange(1, X.shape[0]):
        X_index = np.arange(i, X.shape[0])
        Y_index = np.arange(0, X.shape[0] - i)
        X_slice = X[X_index, :]
        Y_slice = X[Y_index, :]
        S = _jaccard_between(X_slice, Y_slice)
        S = list(S.flat)
        row.extend(X_index.data)
        columns.extend(Y_index.data)
        data.extend(S)
        row.extend(Y_index.data)
        columns.extend(X_index.data)
        data.extend(S)

    return coo_matrix((data, (row, columns))).toarray()


def jaccard_pair(X, Y):
    stack = []

    if X.shape[0] < Y.shape[0]:
        return jaccard_pair(Y, X).transpose()

    for i in trange(Y.shape[0]):
        yix = [i]*X.shape[0]
        Yix = Y[yix, :]
        B = _jaccard_between(X, Yix)
        B = np.reshape(B, [B.shape[0], 1])
        stack.append(B)

    return np.hstack(stack)


def single_kernel(wls, ids):
    X = to_matrix(ids, wls)
    return jaccard_kernel(X)


def pair_kernel(wls, row_ids, col_ids):
    X = to_matrix(row_ids, wls)
    Y = to_matrix(col_ids, wls)
    return jaccard_pair(X, Y)


class LazyKernel:

    def __init__(self, db, info):
        self._db = db
        self._info = info

    def load(self):
        fs = GridFS(self._db)
        transpose = self._info['transpose']
        obj_id = self._info['kernel_ref']

        K = np.array(
            json.loads(
                fs.get(obj_id).read().decode('utf-8')
            )
        )

        if transpose:
            K = K.transpose()
        return K


def load_kernel(db, _id, lazy=False):
    kernel = db.kernels

    id_search = isinstance(_id, ObjectId)

    f = kernel.find_one({'_id': _id} if id_search else {'kernel_id': _id})
    if f is None:
        raise ValueError("Unknown id %s." % (str(_id)))

    kernel = LazyKernel(db, f)

    if not lazy:
        kernel = kernel.load()

    return f, kernel


@task_definition()
def wl_kernel(id, iteration, depth, row_ids, col_ids=None,
              dual=False, index_hint=None, env=None):
    if env is None:
        raise ValueError("train_test_split needs an execution context")

    if col_ids is None:
        col_ids = row_ids

    db = env.get_db()
    kernel = db.kernels

    if dual:
        f1 = kernel.find_one({'kernel_id': id})
        f2 = kernel.find_one({'kernel_id': id+"_t"})
        if f1 is not None and f2 is not None:
            return f1['_id'], f2['_id']
    else:
        f = kernel.find_one({'kernel_id': id})

        if f is not None:
            return f['_id']
    print("Kernel %s" % id)

    ast_index = {'count': 0}

    ids = set.union(set(row_ids), set(col_ids))
    corner = len(ids) > len(row_ids) or len(ids) > len(col_ids)
    wls = _localize_wls(db, ids, iteration, depth, ast_index)

    start = time()
    if corner:
        K = pair_kernel(wls, row_ids, col_ids)
    else:
        K = single_kernel(wls, row_ids)
    run_time = time() - start

    fs = GridFS(db)
    fid = fs.put(
        json.dumps(K.tolist()).encode('utf-8'),
        iteration=iteration, depth=depth, kernel_id=id
    )

    entry = {
        'kernel_id': id,
        'transpose': False,
        'kernel_ref': fid,
        'iteration': iteration,
        'depth': depth,
        'row_ids': row_ids,
        'col_ids': col_ids,
        'run_time': run_time
    }

    if index_hint is not None:
        entry['index'] = index_hint

    id1 = kernel.insert_one(entry).inserted_id

    if dual:
        del entry['_id']
        entry['kernel_id'] = id+'_t'
        entry['transpose'] = True
        entry['row_ids'] = col_ids
        entry['col_ids'] = row_ids
        id2 = kernel.insert_one(entry).inserted_id
        return id1, id2
    else:
        return id1


def check_compatible(i1, i2):
    if ('index' in i1 or 'index' in i2) and\
            not ('index' in i1 and 'index' in i2):
        raise ValueError("Both kernel have to contain an index or none.")

    if 'index' in i1:
        ix1 = i1['index']
        ix2 = i2['index']

        if ix1 != ix2:
            raise ValueError("Incompatible index %s != %s" % (str(ix1),
                                                              str(ix2)))


@task_definition()
def add_wl_kernel(add_id, id1, id2, dual=False, env=None):

    db = env.get_db()
    kernel = db.kernels

    if dual:
        f1 = kernel.find_one({'kernel_id': add_id})
        f2 = kernel.find_one({'kernel_id': add_id+"_t"})
        if f1 is not None and f2 is not None:
            return f1['_id'], f2['_id']
    else:
        f = kernel.find_one({'kernel_id': add_id})

        if f is not None:
            return f['_id']

    i1, K1 = load_kernel(db, id1)
    i2, K2 = load_kernel(db, id2)

    check_compatible(i1, i2)

    print("Kernel %s + %s -> %s" % (i1['kernel_id'], i2['kernel_id'], add_id))

    start_time = time()

    K = K1 + K2

    run_time = time() - start_time

    fs = GridFS(db)
    fid = fs.put(
        json.dumps(K.tolist()).encode('utf-8'),
        iteration=i1['iteration'], depth=i1['depth'], kernel_id=add_id
    )

    entry = i1
    entry.update({
        'kernel_id': add_id,
        'transpose': False,
        'kernel_ref': fid,
        'run_time': run_time
    })

    del entry['_id']

    id1 = kernel.insert_one(entry).inserted_id

    if dual:
        del entry['_id']
        entry['kernel_id'] = add_id+'_t'
        entry['transpose'] = True
        tmp = entry['row_ids']
        entry['row_ids'] = entry['col_ids']
        entry['col_ids'] = tmp
        id2 = kernel.insert_one(entry).inserted_id
        return id1, id2
    else:
        return id1


@task_definition()
def normalize_wl_kernel(norm_id, id, env=None):

    db = env.get_db()
    kernel = db.kernels

    f = kernel.find_one({'kernel_id': norm_id})

    if f is not None:
        return f['_id']

    info, GR = load_kernel(db, id)

    print("Kernel norm( %s ) -> %s" % (info['kernel_id'], norm_id))

    start_time = time()

    D = np.diag(1/np.sqrt(GR.diagonal()))

    GR = D.dot(GR).dot(D)

    run_time = time() - start_time

    fs = GridFS(db)
    fid = fs.put(
        json.dumps(GR.tolist()).encode('utf-8'),
        iteration=info['iteration'], depth=info['depth'], kernel_id=norm_id
    )

    entry = info
    entry.update({
        'kernel_id': norm_id,
        'transpose': False,
        'kernel_ref': fid,
        'run_time': run_time
    })

    del entry['_id']

    return kernel.insert_one(entry).inserted_id


def index_to_coordinate(index):
    if '_' not in index:
        raise ValueError(
                "Need another format. Expected \"number_number\" got %s" % index)
    coo = index.split('_')
    return int(coo[0]), int(coo[1])


def merge_ix_list(ix_list):
    L = []
    seen = set([])

    for X in ix_list:
        if X[0] in seen:
            continue
        seen.add(X[0])
        L.append(X)

    betw = [X[1] for X in sorted(L, key=lambda X: X[0])]

    o = []
    for b in betw:
        o.extend(b)
    return o


def _merge_wl_kernel(db, ids):
    o = []

    for id in ids:
        try:
            o.extend(id)
        except Exception:
            o.append(id)
    ids = o

    matrix = []

    row_ids = []
    col_ids = []

    iteration = 0
    depth = 0
    name = ""

    for id in ids:
        info, K = load_kernel(db, id, lazy=True)

        index = None
        if 'index' in info:
            index = info['index']

        if index is None:
            raise ValueError('Expected an index hint. Run wl_kernel with index_hint option')

        i0, i1 = index_to_coordinate(index)

        if info['transpose']:
            tmp = i0
            i0 = i1
            i1 = tmp

        if len(matrix) <= i0:
            matrix.extend([None]*(i0 - len(matrix) + 1))

        if matrix[i0] is None:
            matrix[i0] = []

        if len(matrix[i0]) <= i1:
            matrix[i0].extend([None]*(i1 - len(matrix[i0]) + 1))

        if matrix[i0][i1] is not None:
            continue

        K = K.load()

        name = '_'.join(info['kernel_id'].split('_')[:-2])
        iteration = info['iteration']
        depth = info['depth']

        row_ids.append((i0, info['row_ids']))
        col_ids.append((i1, info['col_ids']))

        matrix[i0][i1] = K

    tmp = []
    for V in matrix:
        tmp.append(np.hstack(V))
    del matrix
    K = np.vstack(tmp)
    del tmp

    row_ids = merge_ix_list(row_ids)
    col_ids = merge_ix_list(col_ids)

    return name, iteration, depth, row_ids, col_ids, K


@task_definition()
def wl_merge_kernel(ids, env=None):
    if len(ids) == 0:
        return None

    db = env.get_db()
    kernel = db.kernels

    t = []
    try:
        t.extend(ids[0])
    except Exception:
        t.append(ids[0])

    f = kernel.find_one({'_id': t[0]})
    if f is None:
        raise ValueError("Unknown id %s." % (str(ids[0])))

    id = '_'.join(f['kernel_id'].split('_')[:-2])
    f = kernel.find_one({'kernel_id': id})
    if f is not None:
        return f['_id']

    _, iteration, depth, row_ids, col_ids, K = _merge_wl_kernel(db, ids)

    print("Merge kernel to %s" % id)

    fs = GridFS(db)
    fid = fs.put(
        json.dumps(K.tolist()).encode('utf-8'),
        iteration=iteration, depth=depth, kernel_id=id
    )

    entry = {
        'kernel_id': id,
        'transpose': False,
        'kernel_ref': fid,
        'iteration': iteration,
        'depth': depth,
        'row_ids': row_ids,
        'col_ids': col_ids
    }

    return kernel.insert_one(entry).inserted_id


def scattered_kernel(id, iteration, depth, ids, num_batches=20):
    sc_ids = dual_scatter(ids, num_batches, index=True)
    sc_id = tsk.fork(sc_ids)
    kernel = wl_kernel(concat_strs(id, sc_id[0], sc_id[1]), iteration, depth,
                       sc_id[2], sc_id[3], dual=True,
                       index_hint=concat_strs(
                            sc_id[0], sc_id[1]
                       ))
    kernels = tsk.merge([kernel])[0]
    return wl_merge_kernel(kernels)


def sv_scattered_kernels(name, iterations, depth, ids, num_batches=20):
    iterations = iterations + 1
    sc_ids = dual_scatter(ids, num_batches, index=True)
    sc_id = tsk.fork(sc_ids)
    kernels = []
    for iteration in range(iterations):
        kernel = wl_kernel(concat_strs(name, iteration, sc_id[0], sc_id[1]),
                           iteration, depth, sc_id[2], sc_id[3], dual=True,
                           index_hint=concat_strs(
                                sc_id[0], sc_id[1]
                           ))
        kernels.append(kernel)
    sum_kernels = [kernels[0]]
    for i in range(1, iterations):
        sum_kernels.append(
            add_wl_kernel(
                concat_strs('add', name, i, sc_id[0], sc_id[1]),
                sum_kernels[i - 1][0], kernels[i][0], dual=True
            )
        )

    norm_kernels = []
    for i in range(iterations):
        merge_kernel = sum_kernels[i]
        merge_kernel = tsk.merge([merge_kernel])[0]
        merge_kernel = wl_merge_kernel(merge_kernel)
        norm_kernels.append(
            normalize_wl_kernel(
                concat_strs('norm', name, i),
                merge_kernel
            )
        )
    return norm_kernels


def sv_sum_kernels(name, iterations, depth, ids, num_batches=20):
    iterations = iterations + 1
    sc_ids = dual_scatter(ids, num_batches, index=True)
    sc_id = tsk.fork(sc_ids)
    kernels = []
    for iteration in range(iterations):
        kernel = wl_kernel(concat_strs(name, iteration, sc_id[0], sc_id[1]),
                           iteration, depth, sc_id[2], sc_id[3], dual=True,
                           index_hint=concat_strs(
                                sc_id[0], sc_id[1]
                           ))
        kernels.append(kernel)
    sum_kernels = [kernels[0]]
    for i in range(1, iterations):
        sum_kernels.append(
            add_wl_kernel(
                concat_strs('add', name, i, sc_id[0], sc_id[1]),
                sum_kernels[i - 1][0], kernels[i][0], dual=True
            )
        )
    sum_kernels = tsk.merge(sum_kernels)
    return sum_kernels


@task_definition()
def present_kernel(id, env=None):
    info, K = load_kernel(env.get_db(), id)
    return K


def load_kernel_str(db, _id):
    kernel = db.kernels

    id_search = isinstance(_id, ObjectId)

    f = kernel.find_one({'_id': _id} if id_search else {'kernel_id': _id})
    if f is None:
        raise ValueError("Unknown id %s." % (str(_id)))

    fs = GridFS(db)
    obj_id = f['kernel_ref']

    K = fs.get(obj_id).read().decode('utf-8')

    return f, K


def get_names(db, ids):

    pos = {k: i for i, k in enumerate(ids) if isinstance(k, ObjectId)}

    lookup = db['fs.files']

    cur = lookup.find({'app_type': 'code_graph'}, ['_id', 'name'])

    for obj in tqdm(cur, total=cur.count()):
        if obj['_id'] in pos:
            ids[pos[obj['_id']]] = obj['name']
    return ids


def load_kernel_cached(db, kernel_id, path):

    path = os.path.join(path, kernel_id)

    if not os.path.exists(path):
        os.makedirs(path)

    info_p = os.path.join(path, 'info.json')
    kernel_p = os.path.join(path, 'kernel.json')

    if not os.path.exists(kernel_p):
        info, kernel = load_kernel_str(db, kernel_id)

        del info['_id']
        del info['kernel_ref']

        get_names(db, info['row_ids'])
        get_names(db, info['col_ids'])
        with open(info_p, 'w') as o:
            json.dump(info, o)

        with open(kernel_p, 'w') as o:
            o.write(kernel)
        kernel = json.loads(kernel)

    else:

        with open(info_p, "r") as o:
            info = json.load(o)

        with open(kernel_p, "r") as o:
            kernel = json.load(o)

    transpose = info['transpose']
    kernel = np.array(
        kernel
    )

    if transpose:
        kernel = kernel.transpose()

    return info, kernel


def load_kernel_sliced(db, kernel_id, train_index, test_index, cache):
    info, K = load_kernel_cached(db, kernel_id, cache)
    idx = {k: i for i, k in enumerate(info['row_ids'])}
    trix = {k: idx[k] for k in train_index if k in idx}
    teix = {k: idx[k] for k in test_index if k in idx}

    tr_slice = [trix[k] for k in train_index if k in trix]
    te_slice = [teix[k] for k in test_index if k in teix]

    return trix, K[tr_slice, :][:, tr_slice], teix, K[te_slice, :][:, tr_slice]


def extract_svm(train_index, svc):
    coefs = {}

    coef = svc.dual_coef_
    minix = len(train_index) + 1
    mix = 0
    for i in range(coef.shape[1]):
        ix = svc.support_[i]
        mix = max(mix, ix)
        minix = min(minix, ix)
        print((i, ix, len(train_index)))
        # print(train_index[ix])
        # coefs[train_index[ix]] = coef[0, i]

    print("Min: %i Max: %i" % (minix, mix))
    exit()
    return {
        'coef': coefs,
        'intercept': svc.intercept_[0]
    }


def train_svm(kernel, label, C=[0.01]):

    clf = SVC(kernel="precomputed", probability=True)

    D = {'C': C}
    gclf = GridSearchCV(clf, D, cv=10, scoring='f1', n_jobs=-1, refit=False)

    gclf.fit(kernel, label)

    param = gclf.best_params_

    param['kernel'] = 'precomputed'
    param['probability'] = True

    clf = SVC(**param)
    clf.fit(kernel, label)

    return clf


@task_definition()
def svm_train_test(key, tools, kernel_id, train_index, test_index, competition,
                   category=None, C=None, raw_result=False, env=None):
    if env is None:
        raise ValueError("train_test_split needs an execution context")

    db = env.get_db()
    lr = db.experiments

    f = lr.find_one({'key': key, 'type': 'kernel_svm'})

    if f is not None:
        return f['spearmann_mean'], f['spearmann_std']

    print("Localize train data")
    tix = train_index
    train_index, train_kernel, test_index, test_kernel = load_kernel_sliced(
        db, kernel_id, train_index, test_index, env.get_cache_dir()
    )

    train_labels = loader._localize_label(
        db, os.path.join(env.get_cache_dir(), key, "train", 'label.json'),
        get_names(db, train_index.keys()),
        competition, tools, category
    )
    train_labels = loader.expand_and_label(train_labels)

    print("Localize test data")
    test_labels = loader._localize_label(
        db, os.path.join(env.get_cache_dir(), key, "test", 'label.json'),
        get_names(db, test_index.keys()),
        competition, tools,
        category
    )
    test_bin_labels = loader.expand_and_label(test_labels, full=True)
    test_labels = loader.stack_label(test_labels)

    pred = []
    quality = []

    if C is None:
        C = [0.001, 0.01, 0.1, 1.0, 100, 1000]

    for t_index, t_labels in train_labels:
        print("Train clf %i" % (len(pred) + 1))
        te_index, te_labels = test_bin_labels[len(pred)]

        u = np.unique(t_labels)
        if u.shape[0] == 1:
            v = 0 if u[0] == 0.0 else 1
            p = np.array([v]*te_index.shape[0])
        else:
            clf = train_svm(train_kernel[t_index, :][:, t_index], t_labels, C)
            print("Finished training")
            test = test_kernel[te_index, :][:, t_index]
            p = clf.predict_proba(test)[:, 1]

        sc_ix = np.where(te_labels != 0.5)
        q = accuracy_score(te_labels[sc_ix], p[sc_ix].round())
        quality.append(q)
        print("Accuracy %i: %f" % (len(pred), q))
        pred.append(p)

    pred = np.vstack(pred).transpose()
    scores = loader.rank_score(test_labels, pred, tools)

    if raw_result:

        scores = {
            k: scores[i] for i, k in enumerate(test_index)
        }

        lr.insert_one({
            'key': key,
            'competition': competition,
            'category': category,
            'type': 'kernel_svm',
            'train_size': len(train_index),
            'test_size': pred.shape[0],
            'kernel_id': kernel_id,
            'binary_accuracies': quality,
            'mean_acc': np.mean(quality),
            'spearmann_raw': scores,
        })

        return scores

    mean_score = np.mean(scores)
    std_score = np.std(scores)

    print("Spearmann: %f (std: %f)" % (mean_score, std_score))

    lr.insert_one({
        'key': key,
        'competition': competition,
        'category': category,
        'type': 'kernel_svm',
        'train_size': len(train_index),
        'test_size': pred.shape[0],
        'kernel_id': kernel_id,
        'binary_accuracies': quality,
        'mean_acc': np.mean(quality),
        'spearmann_mean': mean_score,
        'spearmann_std': std_score
    })

    return mean_score, std_score


@task_definition()
def annotate_duplicates(kernel_id, competition, env=None):

    db = env.get_db()
    stat = db.graph_statistics
    info, K = load_kernel_cached(db, kernel_id,
                                 env.get_cache_dir())

    row, col = np.where(K >= 0.9999999)

    updates = []

    for i in trange(row.shape[0]):
        pos = row[i]
        cpos = col[i]
        if pos != cpos:
            id = info['row_ids'][pos]
            dup = info['col_ids'][cpos]
            updates.append(
                UpdateOne({'name': id, 'competition': competition},
                          {'$set': {'duplicate': dup}})
            )
    stat.bulk_write(updates)


@task_definition()
def percent_duplicate(competition, env=None):
    stat = env.get_db().graph_statistics

    cur1 = stat.find({'competition': competition})
    cur2 = stat.find({'competition': competition, 'duplicate': {'$exists': 1}, 'name': {'$regex': '^(?!.*eca-rers2012).*$'}})

    print("Duplicate: %f" % (cur2.count()/cur1.count()))


if __name__ == '__main__':
    res = []
    for i in range(10):
        dataset_key = 'rank18_overall_%i' % i
        lr_key = 'rank18_overall_2018_2_it_%i' % i
        limit = 10000
        competition = "2018"
        category = None

        condition = {}
        for key in ['cfg_nodes', 'cfg_edges', 'pdg_edges']:
            condition[key] = limit

        filter = tu.filter_by_stat(competition, condition)
        split = tu.train_test(dataset_key, competition, category=category,
                              test_ratio=0.2, filter=filter)
        cov = tu.tool_coverage(
                competition, filter=split[0], category=category
        )
        tools = tu.covered_tools(
            dataset_key, competition, cov, min_coverage=0.8
        )

        train_index, test_index = split[0], split[1]

        lr = svm_train_test(
            lr_key, tools, 'norm_2018_2', train_index, test_index,
            competition, category, C=[0.001, 0.01, 0.1, 1.0, 100, 1000]
        )

        with backend.openLocalSession(auto_join=True) as sess:
            mean, _ = sess.run(lr)
            res.append(mean)

    print("Acc: %f (+- %f)" % (np.mean(res), np.std(res)))

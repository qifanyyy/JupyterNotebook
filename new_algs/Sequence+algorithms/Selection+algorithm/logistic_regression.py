import taskflow as tsk
from taskflow import task_definition, backend

from tasks.utils import train_utils as tu

import os
import numpy as np
from gridfs import GridFS
import json
from tqdm import tqdm
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from tasks.utils.rank_scores import spearmann_score


def _map_to_vec(D, index):
    vec = np.zeros(index['count'], dtype=np.uint64)

    for d, c in D.items():
        if d not in index:
            print("Unknown label %s" % d)
            continue
        vec[index[d]] = c

    return vec


def _localize_data(db, path, index, competition):

    if os.path.isfile(path):
        data = np.loadtxt(path, delimiter=",")
        with open(path+".ix", "r") as i:
            index = json.load(i)
        return index, data

    stack = [None] * len(index)

    fs = GridFS(db)
    files = db['fs.files']
    cache = db.cache

    ast_index = cache.find_one({'_id': 'ast_index'})
    if ast_index is None:
        ast_index = {}
    else:
        ast_index = ast_index['value']

    n_index = {t: i for i, t in enumerate(index)}

    cur = files.find({'competition': competition, 'app_type': 'code_graph'})

    for obj in tqdm(cur, total=cur.count()):
        if obj['name'] in n_index:
            wl = db.wl_features.find_one({'_id': obj['_id']})
            if wl is None:
                continue
            fs_file = fs.get(
                wl['wl_refs'][0]
            )
            D = json.loads(
                fs_file.read().decode("utf-8")
            )
            stack[n_index[obj['name']]] = _map_to_vec(D, ast_index)

    n_index = []
    n_stack = []

    for i, D in enumerate(stack):
        if D is not None:
            n_index.append(index[i])
            n_stack.append(D)

    del stack
    stack = np.vstack(n_stack)
    del n_stack

    np.savetxt(path, stack, delimiter=",")
    with open(path+".ix", "w") as i:
        index = json.dump(n_index, i)

    return n_index, stack


def _localize_label(db, path, index, competition, tools, category=None):

    if os.path.isfile(path):
        with open(path, "r") as i:
            return json.load(i)

    base = os.path.dirname(path)
    if not os.path.isdir(base):
        os.makedirs(base)

    index = {t: i for i, t in enumerate(index)}

    labels = tu.get_labels(db, competition, category, index)
    out = {}

    for category, D in labels.items():
        if category not in out:
            out[category] = {}
        for name, V in D.items():
            pref = tu.get_preferences(V, tools)
            out[category][name] = {
                'pref': pref.tolist(),
                'pos': index[name]
            }

    with open(path, "w") as o:
        json.dump(out, o, indent=4)
    return out


def _localize_dataset(db, path, index, competition, tools, category=None):

    if not os.path.exists(path):
        os.makedirs(path)

    data_path = os.path.join(path, "data.csv")
    label_path = os.path.join(path, "label.json")

    index, data = _localize_data(db, data_path, index, competition)
    labels = _localize_label(db, label_path, index, competition, tools,
                             category)

    return index, data, labels


def prepare_train_data(train_data):

    scaler = StandardScaler()
    train_data = scaler.fit_transform(train_data)

    def transform(X):
        return scaler.transform(X)
    return transform, train_data


def expand_and_label(labels, full=False, index=False):

    plac_label = []

    for category, D in labels.items():
        for name, V in D.items():
            pos = V['pos']
            pref = V['pref']

            for i, p in enumerate(pref):
                if i >= len(plac_label):
                    plac_label.append(([], [], []))
                if p != 0.5 or full:
                    plac_label[i][0].append(pos)
                    plac_label[i][1].append(p)

    plac_label = [
        (np.array(x[0]), np.array(x[1])) for x in plac_label
    ]

    return plac_label


def stack_label(labels):

    plac_label = []

    for category, D in labels.items():
        for name, V in D.items():
            pref = V['pref']
            plac_label.append(pref)

    return np.vstack(plac_label)


def rank_score(y_true, y_pred, tools):

    return [
        spearmann_score(
            tu.get_ranking(y_pred[i, :], tools, False), tu.get_ranking(y_true[i, :], tools)
        )
        for i in range(y_true.shape[0])
    ]


@task_definition()
def lr_train_test(key, tools, train_index, test_index, competition,
                  category=None, raw_result=False, env=None):
    if env is None:
        raise ValueError("train_test_split needs an execution context")

    db = env.get_db()
    lr = db.experiments

    f = lr.find_one({'key': key, 'type': 'logistic_regression'})

    print((key))

    if f is not None:
        return f['spearmann_mean'], f['spearmann_std']

    print("Localize train data")
    train_index, train_data, train_labels = _localize_dataset(
        db, os.path.join(env.get_cache_dir(), key, "train"),
        train_index, competition, tools,
        category
    )

    print("Prepare train data")
    transform, train_data = prepare_train_data(
        train_data
    )
    train_labels = expand_and_label(train_labels)

    print("Localize test data")
    test_index, test_data, test_labels = _localize_dataset(
        db, os.path.join(env.get_cache_dir(), key, "test"),
        test_index,  competition, tools,
        category
    )

    print("Transform test")
    test_data = transform(test_data)

    test_bin_labels = expand_and_label(test_labels, full=True)
    test_labels = stack_label(test_labels)

    pred = []
    quality = []

    for t_index, t_labels in train_labels:
        clf = LogisticRegression(solver='liblinear')
        print("Train clf %i" % (len(pred) + 1))
        te_index, te_labels = test_bin_labels[len(pred)]

        u = np.unique(t_labels)
        if u.shape[0] == 1:
            v = 0 if u[0] == 0.0 else 1
            p = np.array([v]*te_index.shape[0])
        else:
            clf.fit(train_data[t_index, :], t_labels)
            print("Finished training")
            test = test_data[te_index, :]
            p = clf.predict_proba(test)[:, 1]

        sc_ix = np.where(te_labels != 0.5)
        q = accuracy_score(te_labels[sc_ix], p[sc_ix].round())
        quality.append(q)
        print("Accuracy %i: %f" % (len(pred), q))
        pred.append(p)

    pred = np.vstack(pred).transpose()
    scores = rank_score(test_labels, pred, tools)

    if raw_result:

        scores = {
            k: scores[i] for i, k in enumerate(test_index)
        }

        lr.insert_one({
            'key': key,
            'competition': competition,
            'category': category,
            'type': 'logistic_regression',
            'train_size': len(train_index),
            'test_size': pred.shape[0],
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
        'type': 'logistic_regression',
        'train_size': len(train_index),
        'test_size': pred.shape[0],
        'binary_accuracies': quality,
        'mean_acc': np.mean(quality),
        'spearmann_mean': mean_score,
        'spearmann_std': std_score
    })

    return mean_score, std_score


if __name__ == '__main__':
    res = []
    for i in range(10):
        dataset_key = 'rank18_overflow_%i' % i
        lr_key = 'rank18_overflow_lr2_%i' % i
        limit = 10000
        competition = "2018"
        category = "overflow"

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

        train_index, dex = split[0], split[1]

        lr = lr_train_test(
            lr_key, tools, train_index, dex,
            competition, category
        )

        with backend.openLocalSession() as sess:
            mean, _ = sess.run(lr).join()
            res.append(mean)

    print("Acc: %f (+- %f)" % (np.mean(res), np.std(res)))

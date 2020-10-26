import argparse
import json
from glob import glob
import os
import numpy as np


def get_dirs(path):
    return [
        f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))
    ]


def get_type(path):
    types = ['overall', 'reachability', 'termination', 'memory', 'overflow']

    for t in types:
        if t in path:
            return t


def get_it(path):
    it = [str(i) for i in range(10)]
    for i in it:
        if i in path:
            return int(i)


def get_keys(type):
    keys = [
        'spearmann',
        'spearmann_reachability',
        'spearmann_termination',
        'spearmann_memory',
        'spearmann_overflow'
    ]

    mapping = {
        'overall': [0, 1, 2, 3, 4],
        'reachability': [1],
        'termination': [2],
        'memory': [3],
        'overflow': [4]
    }

    return [keys[t] for t in mapping[type]]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("checkpoints")

    args = parser.parse_args()

    checkpoint = args.checkpoints

    models = {}

    for exp in get_dirs(checkpoint):
        type = get_type(exp)
        it = get_it(exp)
        path = os.path.join(checkpoint, exp)
        print("Load models for type %s in iteration %i" % (type, it))

        for model in get_dirs(path):
            model_path = os.path.join(path, model)
            test_path = os.path.join(model_path, "test.json")

            if not os.path.isfile(test_path):
                print("Model %s is not finished. Skip" % model)
                continue

            with open(test_path, "r") as i:
                test = json.load(i)

            if model not in models:
                models[model] = {}
            model_dict = models[model]
            if type not in model_dict:
                model_dict[type] = {}
            type_dict = model_dict[type]

            for k in get_keys(type):
                if k not in type_dict:
                    type_dict[k] = []
                type_dict[k].append(test[k]['mean'])

    for model, V in models.items():
        print("%s: " % model)
        for type, D in V.items():
            print("\t%s:" % type)

            for acc_type, acc in D.items():
                print("\t\t%s: %f (+- %f) [num: %i]" % (acc_type, np.mean(acc), np.std(acc), len(acc)))

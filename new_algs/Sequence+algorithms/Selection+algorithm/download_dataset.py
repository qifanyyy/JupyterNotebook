import os
import sys
import argparse
import json
from tqdm import tqdm
from glob import glob
import traceback as tb

import torch as th
from torch_geometric.data import Data

from tasks.data import dataset_tasks as dt
from tasks.data import preparation as p
from tasks.data import proto_data as ptd

from parse_code import parse_c_code


def _node_repr(nodes):
    row = []
    column = []
    content = []
    for i, feat in enumerate(nodes):
        for pos, v in feat:
            row.append(i)
            column.append(pos)
            content.append(v)
    return row, column, content


def _edge_repr(edges):
    row = []
    column = []
    content = []
    for u, v, e in edges:
        row.append(u)
        column.append(v)
        content.append(e)
    return row, column, content


def _attr_repr(attrs):
    row = []
    col = []

    for D in attrs:
        if D is None:
            row.append(-1)
            col.append(-1)
        else:
            row.append(D[0])
            col.append(D[1])

    return row, col


def create_data_bag(G, ast_index, pos={}, ast_graph=False):

    p.compress_graph(
        G, ast_index, ast_index['count'],
        p._compress_node2 if ast_graph else p._compress_node
    )

    G, node_index = p.to_custom_dict(G, attr=pos, return_index=True)

    return G


def load_and_fix(path):
    with open(path, "r") as i:
        F = i.read()
    F = F.replace(', ,', ',')
    return json.loads(F)


def transform_code(file_path, out_path, ast_index):

    if os.path.isfile(out_path):
        return

    tmp_path = os.path.abspath(out_path+".json")
    file_path = os.path.abspath(file_path)

    path, pos, _ = parse_c_code(file_path, tmp_path)

    if os.path.isfile(pos):
        os.remove(pos)

    G = load_and_fix(path)

    G = dt.parse_dfs_nx_alt(G)
    data = create_data_bag(G, ast_index)

    with open(out_path, "w") as o:
        json.dump(data, o, indent=4)

    if os.path.isfile(path):
        os.remove(path)


def index_path(base_dir, filter_path=None):
    F = load_filter(filter_path)
    bp = os.path.join(base_dir, "svcomp-git", "sv-benchmarks", "c")

    out = {}

    for D in glob(os.path.join(bp, "*")):
        if os.path.isdir(D):
            for G in ['.c', '.i']:
                for f in glob(os.path.join(D, '*'+G)):
                    if os.path.isfile(f):
                        k = f.replace(bp+"/", "")
                        k = k.replace("/", "_").replace(".", "_")
                        if F(k):
                            out[k] = f

    print("Detected %i paths." % len(out))
    return out


def load_filter(path):

    if path is None or not os.path.exists(path):
        def taut(k):
            return True
        return taut

    print("Load filter %s" % path)
    with open(path, "r") as i:
        F = [k[:-1] for k in i.readlines()]

    F = set(F)

    def test(k):
        return k in F
    return test


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("competition_year")
    parser.add_argument("base_dir")
    parser.add_argument("ast_path")
    parser.add_argument("-f", "--filter")

    args = parser.parse_args()

    print("Download SV-Comp dataset from %s" % args.base_dir)
    path = dt.prepare_svcomp_git(
        args.competition_year,
        args.base_dir
    )

    index = index_path(args.base_dir, args.filter)

    aim_path = os.path.join(args.base_dir, "graphs")

    with open(args.ast_path, "r") as i:
        ast = json.load(i)

    print('Start transform...')
    for k, path in tqdm(index.items()):
        out = os.path.join(aim_path, k+".json")
        try:
            transform_code(path, out, ast)
        except Exception:
            print("Cannot transform %s" % k)
            tb.print_exc()

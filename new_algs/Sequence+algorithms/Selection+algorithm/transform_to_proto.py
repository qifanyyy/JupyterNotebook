import argparse
from tqdm import tqdm

import os
import torch as th
from tasks import graph_data_pb2 as gd

from glob import glob
import lmdb


def to_proto(D):
    svgraph = gd.SVGraph()
    nodes = svgraph.nodes

    x = D.x
    for i in range(x.shape[1]):
        nodes.row.append(x[0, i])
        nodes.column.append(x[1, i])
        nodes.content.append(x[2, i])

    edge_index = D.edge_index
    attr = D.edge_attr

    edges = svgraph.edges
    for i in range(edge_index.shape[1]):
        edges.row.append(edge_index[0, i])
        edges.column.append(edge_index[1, i])

        at = attr[i, :]
        if at[0] == 1:
            edges.types.append(gd.Edges.EdgeType.CFG)
        elif at[1] == 1:
            edges.types.append(gd.Edges.EdgeType.DD)
        elif at[2] == 1:
            edges.types.append(gd.Edges.EdgeType.CD)

    y = D.y
    for i in range(y.shape[0]):
        svgraph.preferences.append(y[i])

    return svgraph


parser = argparse.ArgumentParser()
parser.add_argument("source")
parser.add_argument("target")

args = parser.parse_args()

with lmdb.open(args.target, map_size=1048576*100000,
               map_async=True,
               writemap=True) as lm:
    with lm.begin(write=True) as txn:

        for path in tqdm(sorted(glob(args.source+"*.pt"))):
            category = None
            if '_reachability' in path:
                category = gd.SVGraph.Category.reachability
            elif '_termination' in path:
                category = gd.SVGraph.Category.termination
            elif '_memory' in path:
                category = gd.SVGraph.Category.memory
            elif '_overflow' in path:
                category = gd.SVGraph.Category.overflow

            id = path.replace(args.source, "").replace(".pt", "")

            D = th.load(path)
            proto = to_proto(D)
            proto.category = category

            txn.put(id.encode('ascii'), proto.SerializeToString(), append=True)
    lm.sync()

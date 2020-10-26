from tasks.data import dataset_tasks as dt
from tasks.data import preparation as p
from tasks.data import proto_data as ptd

import os
import time
import torch as th
from torch_geometric.data import Data


def parse_c_code(file_path, out_path):

    if 'PESCO_PATH' not in os.environ:
        raise ValueError(
                    "Environment variable PESCO_PATH has to be defined!")
    if not os.path.isfile(file_path):
        raise ValueError("Some problem occur while accessing file %s." % file_path)

    pesco_path = os.environ['PESCO_PATH']
    out_pos = out_path+".pos"

    start_time = time.time()

    dt.run_pesco(
        pesco_path,
        file_path,
        out_path,
        pos_path=out_pos
    )

    run_time = time.time() - start_time

    if not os.path.exists(out_path):
        raise ValueError(
            "Pesco doesn't seem to be correctly configured! No output for %s" % file_path
        )

    return out_path, out_pos, run_time


def create_networkx(file_path):
    pass


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


def create_data_bag(G, ast_index, category, pos={}, ast_graph=False):

    p.compress_graph(
        G, ast_index, ast_index['count'],
        p._compress_node2 if ast_graph else p._compress_node
    )

    G, node_index = p.to_custom_dict(G, attr=pos, return_index=True)

    row, col, cont = _node_repr(G['nodes'])
    nodes_len = max(row) + 1
    index = th.LongTensor([row, col])
    nodes = th.FloatTensor(cont)

    x = th.sparse.FloatTensor(
        index, nodes, th.Size([nodes_len, ast_index['count']])
    )
    del row, col, cont, index, nodes
    x = x.to_dense()

    row, col, cont = _edge_repr(G['edges'])

    edge_index = th.LongTensor([row, col])
    edge_attr = th.tensor([
        ptd.edge_type_to_tensor_unsafe(t) for t in cont
    ])

    del row, col, cont

    row, col = _attr_repr(G['attributes'])
    attr = th.LongTensor([row, col])

    cat = th.tensor(ptd.plain_category_to_tensor(category), dtype=th.int32)

    return Data(x=x, edge_index=edge_index, edge_attr=edge_attr,
                category=cat, position=attr), node_index

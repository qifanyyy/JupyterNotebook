import taskflow as tsk
from taskflow import task_definition

from tasks.data import graph_data_pb2 as gd
from tasks.utils import train_utils

import torch as th
from torch.utils.data import Dataset
from torch_geometric.data import Data, InMemoryDataset

import os
import lmdb
import random
from gridfs import GridFS
from tqdm import tqdm, trange
import json
import traceback


def select_category(category):
    if category == 'reachability':
        category = gd.SVGraph.Category.Value('reachability')
    elif category == 'termination':
        category = gd.SVGraph.Category.Value('termination')
    elif category == 'memory':
        category = gd.SVGraph.Category.Value('memory')
    elif category == 'overflow':
        category = gd.SVGraph.Category.Value('overflow')
    return category


def select_edge_type(type_id):
    if type_id == 0:
        return gd.Edges.EdgeType.Value('CFG')
    elif type_id == 1:
        return gd.Edges.EdgeType.Value('DD')
    elif type_id == 2:
        return gd.Edges.EdgeType.Value('CD')


def create_data(data, category, preference):

    svgraph = gd.SVGraph()
    nodes = svgraph.nodes

    for i, feat in enumerate(data['nodes']):
        for p, v in feat:
            nodes.row.append(i)
            nodes.column.append(p)
            nodes.content.append(v)

    edges = svgraph.edges

    n = len(data['nodes'])

    for u, v, e in data['edges']:
        if u >= n or v >= n:
            print("WARN: Edge is out of bounds (%d, %d) != %d" % (u, v, n))
            continue
        edges.row.append(u)
        edges.column.append(v)
        edges.types.append(select_edge_type(e))

    y = preference
    for i in range(y.shape[0]):
        svgraph.preferences.append(y[i])

    svgraph.category = select_category(category)

    return svgraph


@task_definition()
def download_plain_lmdb(name, tools, competition, index, category=None,
                        ast_bag=False, filter=None, env=None):

    cat_name = category
    if cat_name is None:
        cat_name = 'all'
    out = os.path.join(env.get_cache_dir(),
                       name)

    if os.path.exists(os.path.join(out, 'data.mdb')):
        return out

    if not os.path.exists(out):
        os.makedirs(out)

    db = env.get_db()

    index = set(index)

    graph = db.ast_graph
    if ast_bag:
        graph = db.ast_bag

    cur = graph.find({'competition': competition},
                     no_cursor_timeout=True)

    fs = GridFS(db)

    labels = train_utils.get_labels(db, competition, category=category)

    filter = train_utils.build_filter_func(filter)

    with lmdb.open(out, map_size=1048576*100000,
                   sync=False,
                   metasync=False,
                   map_async=True,
                   writemap=True,
                   max_dbs=2) as lm:
        with lm.begin(write=True) as txn:
            try:
                train_db = lm.open_db('data'.encode('ascii'), txn)
                train_i = 0
                for obj in tqdm(cur, total=cur.count()):

                    if obj['name'] not in index:
                        continue

                    try:
                        file = fs.get(obj['graph_ref']).read().decode('utf-8')
                        file = json.loads(file)

                        for cat, lookup in labels.items():
                            if obj['name'] in lookup:
                                if not filter(obj['name']):
                                    continue
                                pref = lookup[obj['name']]
                                pref = train_utils.get_preferences(pref, tools)
                                data = create_data(file, cat, pref)
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
            finally:
                cur.close()

        lm.sync(True)
    return out


@task_definition()
def download_lmdb(tools, competition, train, test, category=None,
                  ast_bag=False, filter=None, env=None):

    cat_name = category
    if cat_name is None:
        cat_name = 'all'
    ast = 'bag' if ast_bag else 'graph'
    out = os.path.join(env.get_cache_dir(),
                       '%s_%s_%s' % (competition, cat_name, ast))

    if os.path.exists(os.path.join(out, 'data.mdb')):
        return out

    if not os.path.exists(out):
        os.makedirs(out)

    db = env.get_db()

    train = set(train)
    test = set(test)

    graph = db.ast_graph
    if ast_bag:
        graph = db.ast_bag

    cur = graph.find({'competition': competition},
                     no_cursor_timeout=True)

    fs = GridFS(db)

    labels = train_utils.get_labels(db, competition, category=category)

    filter = train_utils.build_filter_func(filter)

    with lmdb.open(out, map_size=1048576*100000,
                   sync=False,
                   metasync=False,
                   map_async=True,
                   writemap=True,
                   max_dbs=2) as lm:
        with lm.begin(write=True) as txn:
            try:
                train_db = lm.open_db('train'.encode('ascii'), txn)
                test_db = lm.open_db('test'.encode('ascii'), txn)
                train_i = 0
                test_i = 0
                for obj in tqdm(cur, total=cur.count()):

                    train_t = obj['name'] in train
                    test_t = obj['name'] in test

                    if not train_t and not test_t:
                        continue

                    try:
                        file = fs.get(obj['graph_ref']).read().decode('utf-8')
                        file = json.loads(file)

                        for cat, lookup in labels.items():
                            if obj['name'] in lookup:
                                if train_t and not filter(obj['name']):
                                    continue
                                pref = lookup[obj['name']]
                                pref = train_utils.get_preferences(pref, tools)
                                data = create_data(file, cat, pref)
                                data_ser = data.SerializeToString()
                                id = 'graph_%d' % (train_i if train_t else test_i)
                                txn.put(
                                    id.encode('ascii'),
                                    data_ser,
                                    db=(train_db if train_t else test_db)
                                )
                                if train_t:
                                    train_i += 1
                                else:
                                    test_i += 1

                    except Exception:
                        traceback.print_exc()
                        continue
            finally:
                cur.close()

        lm.sync(True)
    return out


def bin_to_proto(bin):
    graph = gd.SVGraph()
    graph.ParseFromString(bin)
    return graph


def edge_type_to_tensor(type):

    if type == gd.Edges.EdgeType.Value('CFG'):
        return [1, 0, 0]

    if type == gd.Edges.EdgeType.Value('DD'):
        return [0, 1, 0]

    if type == gd.Edges.EdgeType.Value('CD'):
        return [0, 0, 1]

    raise ValueError("Type %s not supported yet" % str(type))


def edge_type_to_tensor_unsafe(type):

    E = [0]*3
    E[type] = 1
    return E


def edges_to_tensor_unsafe(edge_attr):
    col = th.arange(len(edge_attr))
    index = th.LongTensor([edge_attr, col])
    sp = th.sparse.FloatTensor(
        index, th.full((len(edge_attr),), 1), th.Size([3, len(edge_attr)])
    )
    return sp.to_dense().transpose(0, 1)


def plain_category_to_tensor(cat):

    if cat == 'reachability':
        return [[1, 0, 0, 0]]

    if cat == 'termination':
        return [[0, 1, 0, 0]]

    if cat == 'memory':
        return [[0, 0, 1, 0]]

    if cat == 'overflow':
        return [[0, 0, 0, 1]]

    raise ValueError("Category %s not supported." % str(cat))


def category_to_tensor(cat):

    if cat == gd.SVGraph.Category.Value('reachability'):
        return [[1, 0, 0, 0]]

    if cat == gd.SVGraph.Category.Value('termination'):
        return [[0, 1, 0, 0]]

    if cat == gd.SVGraph.Category.Value('memory'):
        return [[0, 0, 1, 0]]

    if cat == gd.SVGraph.Category.Value('overflow'):
        return [[0, 0, 0, 1]]

    raise ValueError("Category %s not supported." % str(cat))


def proto_to_data(proto, features=148):

    nodes_len = max(proto.nodes.row)+1
    index = th.LongTensor([proto.nodes.row, proto.nodes.column])
    nodes = th.FloatTensor(proto.nodes.content)

    x = th.sparse.FloatTensor(index, nodes, th.Size([nodes_len, features]))
    del index, nodes
    x = x.to_dense()

    edge_index = th.LongTensor([proto.edges.row, proto.edges.column])
    edge_attr = th.tensor(
       [edge_type_to_tensor_unsafe(t) for t in proto.edges.types],
       dtype=th.int32
    )

    y = th.tensor(proto.preferences, dtype=th.float)
    y = y.unsqueeze(0)
    cat = th.tensor(category_to_tensor(proto.category), dtype=th.int32)

    return Data(x=x, edge_index=edge_index, edge_attr=edge_attr,
                y=y, category=cat)


def proto_to_sparse(proto, features=148):

    offset = th.LongTensor(proto.nodes.row)
    _, offset = th.unique_consecutive(offset, return_counts=True)
    offset = th.cat((th.LongTensor([0]), offset[:-1]), 0)

    index = th.LongTensor(proto.nodes.column)
    nodes = th.FloatTensor(proto.nodes.content)

    edge_index = th.LongTensor([proto.edges.row, proto.edges.column])
    edge_attr = th.tensor(
       [edge_type_to_tensor_unsafe(t) for t in proto.edges.types],
       dtype=th.int32
    )

    y = th.tensor(proto.preferences, dtype=th.float)
    y = y.unsqueeze(0)
    cat = th.tensor(category_to_tensor(proto.category), dtype=th.int32)

    return Data(sparse_index=index, offset=offset,
                weight=nodes,
                edge_index=edge_index, edge_attr=edge_attr,
                y=y, category=cat)


def proto_to_flat(proto, features=148):

    nodes_len = max(proto.nodes.row)+1
    index = th.LongTensor([proto.nodes.row, proto.nodes.column])
    nodes = th.FloatTensor(proto.nodes.content)

    x = th.sparse.FloatTensor(index, nodes, th.Size([nodes_len, features]))
    del index, nodes
    x = x.to_dense()

    y = th.tensor(proto.preferences, dtype=th.float)
    y = y.unsqueeze(0)

    return Data(x=x, y=y)


def bin_to_data(bin):
    return proto_to_data(bin_to_proto(bin))


class LMDBDataset(Dataset):

    def __init__(self, root, base_db, shuffle=False, transform=None,
                 slice_index=None):
        self._env = lmdb.open(root,
                              max_readers=1,
                              readonly=True,
                              lock=False,
                              readahead=False,
                              meminit=False,
                              max_dbs=2)

        self._db = self._env.open_db(key=base_db.encode('ascii'), create=False)
        with self._env.begin(write=False, db=self._db) as txn:
            self._len = txn.stat()['entries']
        self._indices = list(range(self._len))
        if slice_index is not None:
            self._indices = slice_index
        self._transform = transform
        if shuffle:
            random.shuffle(self._indices)

    def __name__(self):
        return 'LMDBDataset'

    def __len__(self):
        return self._len

    def __getitem__(self, index):

        if isinstance(index, slice):
            slice_ix = self._indices[index]
            return SliceDataset(self, slice_ix)

        assert index < len(self), 'index range error for ix: %i' % index
        graph_key = 'graph_%d' % (self._indices[index])

        with self._env.begin(write=False, db=self._db) as txn:
            graph_bin = txn.get(graph_key.encode('ascii'))

        if self._transform is not None:
            graph_bin = self._transform(graph_bin)

        return graph_bin

    def __repr__(self):
        return "%s(%d)" % (self.__name__(), len(self))


class SliceDataset(Dataset):

    def __init__(self, delegate, slice):
        self._slice = slice
        self._delegate = delegate

    def __len__(self):
        return len(self._slice)

    def __getitem__(self, index):
        if isinstance(index, slice):
            slice_ix = self._slice[index]
            return SliceDataset(self._delegate, slice_ix)

        assert index <= len(self)

        ix = self._slice[index]
        return self._delegate[ix]

    def __name__(self):
        return self._delegate.__name__()

    def __repr__(self):
        return "%s(%d)" % (self.__name__(), len(self))


class BufferedDataset(Dataset):

    def __init__(self, delegate):
        self._delegate = delegate
        self._buffer = {}

    def __len__(self):
        return len(self._delegate)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return BufferedDataset(self._delegate[index])

        assert index <= len(self)

        if index not in self._buffer:
            self._buffer[index] = self._delegate[index]
        return self._buffer[index]

    def __name__(self):
        return self._delegate.__name__()

    def __repr__(self):
        return "%s(%d)" % (self.__name__(), len(self))


class GraphDataset(LMDBDataset):

    def __init__(self, root, base_db, shuffle=False, transform=None,
                 sparse=False):

        def chain_transform(x):

            x = bin_to_data(x)

            if transform is not None:
                return transform(x)
            return x

        def chain_transform_sparse(x):

            x = proto_to_sparse(bin_to_proto(x))

            if transform is not None:
                return transform(x)
            return x

        t = chain_transform_sparse if sparse else chain_transform

        super().__init__(root, base_db, shuffle, transform=t)

    def __name__(self):
        return 'GraphDataset'


class GraphFlatDataset(LMDBDataset):

    def __init__(self, root, base_db, shuffle=False, transform=None):

        def chain_transform(x):
            x = proto_to_flat(bin_to_proto(x))
            if transform is not None:
                return transform(x)
            return x

        super().__init__(root, base_db, shuffle, transform=chain_transform)

    def __name__(self):
        return 'GraphDataset'


class InMemGraphDataset(InMemoryDataset):

    def __init__(self, root, base_db, shuffle=False, transform=None):
        self.base_db = base_db
        self.shuffle = shuffle
        super().__init__(root, transform=transform, pre_transform=bin_to_data)
        self.data, self.slices = th.load(self.processed_paths[0])

    def __name__(self):
        return 'InMemGraphDataset'

    @property
    def processed_file_names(self):
        return ['data.pt']

    def _download(self):
        pass

    def process(self):
        data = LMDBDataset(
            self.root, self.base_db, self.shuffle, transform=self.pre_transform
        )

        data_points = []
        print("Load data into memory...")

        for i in trange(len(data)):
            data_points.append(data[i])

        print("Collate data...")
        data, slices = self.collate(data_points)
        th.save((data, slices), self.processed_paths[0])

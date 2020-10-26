import taskflow as tsk
from taskflow import task_definition, backend

from tasks.utils import train_utils

import os
from tqdm import tqdm
from gridfs import GridFS
import json
import traceback
from glob import glob

import torch as th
from torch_geometric.data import Data, Dataset


def create_data(data, category, preference):

    nodes_row = []
    nodes_col = []
    nodes = []
    for i, feat in enumerate(data['nodes']):
        for p, v in feat:
            nodes_row.append(i)
            nodes_col.append(p)
            nodes.append(v)

    nodes_row = th.FloatTensor(nodes_row)
    nodes_col = th.FloatTensor(nodes_col)
    nodes = th.FloatTensor(nodes)

    nodes = th.stack([nodes_row, nodes_col, nodes])

    source = []
    target = []
    edges = []

    for u, v, e in data['edges']:
        E = [0] * 3
        E[e] = 1
        edges.append(E)
        source.append(u)
        target.append(v)

    edge_index = th.tensor([source, target], dtype=th.long)
    edge_attr = th.tensor(edges, dtype=th.float)
    y = th.tensor(preference, dtype=th.float)

    return Data(x=nodes, y=y, edge_index=edge_index, edge_attr=edge_attr)


@task_definition()
def download(tools, competition, train, test, category=None, env=None):

    db = env.get_db()

    train = set(train)
    test = set(test)

    graph = db.ast_graph

    cur = graph.find({'competition': competition})

    fs = GridFS(db)
    cat_name = category
    if cat_name is None:
        cat_name = 'all'
    out = os.path.join(env.get_cache_dir(), 'processed', '%s_%s_%s.pt')

    labels = train_utils.get_labels(db, competition, category=category)

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
                    pref = lookup[obj['name']]
                    pref = train_utils.get_preferences(pref, tools)
                    save_path = out % (obj['name'], competition, cat)
                    data = create_data(file, cat, pref)
                    th.save(data, save_path)

        except Exception:
            traceback.print_exc()
            continue


class GraphDataset(Dataset):
    def __init__(self, root, transform=None, pre_transform=None):
        super(GraphDataset, self).__init__(root, transform, pre_transform)
        dir = self.processed_dir
        self._processed = [
            s.replace(dir, "") for s in glob(os.path.join(dir, "*.pt"))
        ]

    @property
    def raw_file_names(self):
        return []

    @property
    def processed_file_names(self):
        return self._processed

    def __len__(self):
        return len(self.processed_file_names)

    def _download(self):
        pass

    def _process(self):
        pass

    def _transform(self, x):
        index = x[:2, :].long()
        val = x[2, :]
        size = th.Size([th.max(index[0, :]) + 1, 148])
        x = th.sparse_coo_tensor(index, val, size).to_dense()
        return x

    def get(self, idx):
        path = self.processed_file_names[idx]
        path = os.path.join(self.processed_dir, "."+path)
        data = th.load(path)
        data.x = self._transform(data.x)
        return data


if __name__ == '__main__':

    dataset_key = 'initial_test'
    lr_key = "initial_reachability_0"
    competition = "2019"
    category = "reachability"

    tools, train_index, test_index = train_utils.get_svcomp_train_test(
        dataset_key, competition, category, test_ratio=0.2
    )

    down = download(tools, competition, train_index, test_index, category)

    with backend.openLocalSession() as sess:
        sess.run(
            down
        )

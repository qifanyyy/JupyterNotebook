import taskflow as tsk
from taskflow import task_definition, backend

from tasks.utils import train_utils, rank_scores, element_scores
from tasks.data import proto_data
from tasks.torch_model import build_model_from_config

import torch as th
from torch_geometric.data import DataLoader
from torch.nn import functional as F
from gridfs import GridFS

import numpy as np
import time
import os
import math
import shutil
import random


class TrainLogger:

    def __init__(self):
        pass

    def start_epoch(self, epoch_id):
        self._epoch_start = time.time()

    def end_epoch(self, epoch_id):
        print("Epoch %d Time %f" % (epoch_id, (time.time() - self._epoch_start)))

    def iteration(self, it, train_loss, val_loss=None, val_scores={}):
        txt = "Iteration %d Train Loss %f" % (it, train_loss)
        if val_loss is not None:
            txt = txt + (" Val Loss %f" % val_loss)
        for k, v in val_scores.items():
            txt = txt + " Val %s %f" % (k, v)
        print(txt)


class Rank_BCE(th.nn.Module):

    def __init__(self):
        super().__init__()
        self.loss = th.nn.BCEWithLogitsLoss(reduction='none')

    def forward(self, x, y):

        filt = th.abs(2 * y - 1)
        loss = self.loss(x, y)
        loss = filt * loss
        return loss.mean()


class Kendall_Loss(th.nn.Module):

    def __init__(self, eps=1e-08):
        super().__init__()
        self.act = th.nn.Tanh()
        self.eps = eps

    def forward(self, p, y):

        y = 2 * y - 1
        p = self.act(p)

        loss = -y * p
        return loss.mean()


class Relational_Log_Loss(th.nn.Module):

    def __init__(self, eps=1e-08):
        super().__init__()
        self.act = th.nn.Tanh()
        self.eps = eps

    def forward(self, p, y):

        y = 2 * y - 1
        p = self.act(p)

        c = 1 + y*p
        c = c.clamp(self.eps)

        scale = 1 / math.log(2)

        loss = y*y - scale * th.log(c)
        return loss.mean()


def reduce(L, reduction):

    if reduction == 'mean':
        return L.mean()
    if reduction == 'sum':
        return L.sum()
    return L


class MaskedLoss(th.nn.Module):

    def __init__(self, loss, reduction='mean'):
        super().__init__()
        self.loss = loss
        self.reduction = reduction

    def forward(self, p, y):

        _y = 2*y - 1
        _y = _y * _y

        L = _y * self.loss(p, y)

        return reduce(L, self.reduction)


class HingeLoss(th.nn.Module):

    def __init__(self, margin=1.0, reduction='mean'):
        super().__init__()
        self.reduction = reduction
        self.margin = margin

    def forward(self, p, y):

        y = 2*y - 1
        L = F.relu(self.margin - y * p)
        return reduce(L, self.reduction)


def build_model_io(base_dir):

    def identity(state, filename=""):
        return state

    if base_dir is None:
        return identity, identity

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    def save(state, filename="checkpoint.pth.tar"):
        path = os.path.join(base_dir, filename)
        th.save(state, path)

    def load_best(state, filename="checkpoint.pth.tar"):
        path = os.path.join(base_dir, filename)
        m = th.load(path)
        if m['score'] > state['score']:
            return m
        else:
            return state

    return save, load_best


def select_loss(loss_type):

    if loss_type == 'rank_bce':
        return Rank_BCE(), True

    if loss_type == 'kendall':
        return Kendall_Loss(), True

    if loss_type == 'relational':
        return Relational_Log_Loss(), True

    if loss_type == 'hinge':
        return MaskedLoss(HingeLoss(reduction=None)), True

    raise ValueError("Unknown loss function %s." % loss_type)


def rank_preprocessor(score):

    def inner_score(pred, target, labels):
        p = train_utils.get_ranking(pred, labels)
        t = train_utils.get_ranking(target, labels)
        return score(p, t)

    return inner_score


def element_preprocessor(score, pos):

    def inner_score(pred, target, labels):
        p = pred[pos]
        t = target[pos]
        return score(p, t)

    return inner_score


def select_score(type):

    if ':' in type:
        t, p = type.split(':')

        try:
            score = element_scores.select_score(t)
            pos = int(p)
            return element_preprocessor(score, pos)
        except ValueError:
            pass

    rank_score = rank_scores.select_score(type, {}, {})
    return rank_preprocessor(rank_score)


def score(scores, pred, target, classes=15):
    labels = ['%d' % i for i in range(classes)]
    avg_score = {k: [] for k in scores}
    score_func = {k: select_score(k) for k in scores}
    for i in range(pred.shape[0]):
        p = pred[i, :]
        t = target[i, :]
        for k in scores:
            avg_score[k].append(score_func[k](p, t, labels))

    R = {k: th.tensor(avg_score[k], dtype=th.float) for k in scores}
    return R


def tensor_len(classes):
    if isinstance(classes, int):
        n = classes
    else:
        n = len(classes)
    return int(n * (n - 1) / 2)


def setup_optimizer(config, model):
    optim_type = config['type']
    del config['type']

    if optim_type.lower() == 'adam':
        return th.optim.Adam(model.parameters(), **config)

    if optim_type.lower() == 'rmsprop':
        return th.optim.RMSprop(model.parameters(), **config)

    raise ValueError("Unknown optimizer %s" % optim_type)


def setup_sheduler(config, optim, model):
    scheduler = None
    if 'scheduler' in config:
        scheduler = th.optim.lr_scheduler.StepLR(
            optim, **config['scheduler']
        )
    return scheduler


def setup_optim_sheduler(config, model):
    optim = setup_optimizer(config['optimizer'], model)
    scheduler = setup_sheduler(config, optim, model)
    return optim, scheduler


def train_iteration(model, batch, loss_func, optimizer):
    optimizer.zero_grad()
    out = model(batch)
    loss = loss_func(out, batch.y)
    loss.backward()
    optimizer.step()
    return loss.item()


def validate_model(model, validate_loader, loss_func, device,
                   valid_scores=None, logit=False, classes=15):
    model.eval()
    val_loss = []
    val_scores = {}
    if valid_scores:
        val_scores = {k: [] for k in valid_scores}

    for batch in validate_loader:
        batch = batch.to(device)
        out = model(batch)
        loss = loss_func(out, batch.y)
        val_loss.extend(
            [loss.item()]*batch.num_graphs
        )

        if valid_scores:
            if logit:
                out = th.sigmoid(out)
            sc = score(valid_scores, out, batch.y, classes=classes)
            for k, a in sc.items():
                val_scores[k].append(a)

    if valid_scores:
        for k in list(val_scores.keys()):
            ts = val_scores[k]
            ts = th.cat(ts)
            val_scores[k] = ts.mean().item()

    model.train()
    return np.mean(val_loss), val_scores


def train_model(config, model, train_loader, device, valid_loader=None,
                validate_step=10, valid_score=None, cache_dir=None):
    model.train()

    save_func, load_func = build_model_io(cache_dir)

    logger = TrainLogger()
    loss_func, logit = select_loss(config['loss'])
    loss_func = loss_func.to(device)
    optimizer, sheduler = setup_optim_sheduler(config, model)

    best_score = 0.0

    for ep in range(config['epoch']):
        logger.start_epoch(ep)

        for i, batch in enumerate(train_loader):
            batch = batch.to(device)
            train_loss = train_iteration(model, batch, loss_func,
                                         optimizer)
            valid_loss = None
            scores = {}
            if valid_loader is not None and i % validate_step == 0:
                valid_loss, scores =\
                        validate_model(model, valid_loader, loss_func, device,
                                       [valid_score], logit,
                                       len(config['tools']))
                score = scores[valid_score]
                logger.iteration(i, train_loss, valid_loss, scores)

                if score > best_score:
                    save_func({'model': model, 'epoch': ep, 'score': score})

        logger.end_epoch(ep)
        if sheduler is not None:
            sheduler.step()

    model = load_func({'model': model,
                      'epoch': config['epoch'], 'score': 0.0})['model']

    return model, logit


def test_model(config, model, test_loader, device):
    model.eval()
    test_scores = config['scores']
    classes = len(config['tools'])
    test_scoring = {k: [] for k in test_scores}

    for batch in test_loader:
        batch = batch.to(device)
        out = model(batch)

        if config['logit']:
            out = th.sigmoid(out)
        sc = score(test_scores, out, batch.y, classes=classes)
        for k, a in sc.items():
            test_scoring[k].append(a)

    for k in list(test_scoring.keys()):
        ts = test_scoring[k]
        ts = th.cat(ts)
        test_scoring[k] = {
            'mean': ts.mean().item(),
            'std': ts.std().item()
            }

    return test_scoring


def store_model(db, config, model, tools, base_path, eval):
    base_path = os.path.join(base_path, "model.th")
    th.save(model.state_dict(), base_path)

    model_key = config['model_key']
    key = config['key']
    dataset = config['dataset']['key']

    fs = GridFS(db)
    file = fs.new_file(model=model_key,
                       dataset_key=dataset,
                       experiment=key,
                       app_type='torch_model',
                       encoding="utf-8")

    try:
        with open(base_path, "rb") as i:
            shutil.copyfileobj(i, file)
    finally:
        file.close()

    insert = {
        'experiment': key,
        'model_key': model_key,
        'dataset': config['dataset']['key'],
        'competition': config['dataset']['competition'],
        'category': config['dataset']['category'],
        'model_def': config['model'],
        'model_ref': file._id,
        'tools': tools
    }

    insert.update(eval)

    models = db.torch_models
    models.insert_one(insert)


def graph_augmention(options=[0, 1, 2, 5, 6]):

    def select_filter(option):
        select = {
            1: [0],
            2: [1, 2],
            3: [0, 2],
            4: [0, 1],
            5: [2],
            6: [1]
        }
        return select[option]

    def augment(data):
        option = random.choice(options)

        if option == 0:
            return data

        filter = select_filter(option)
        edge_attr = data.edge_attr.numpy()
        edge_attr_t = edge_attr.transpose()
        edge_index = data.edge_index.numpy()

        pos = []
        for f in filter:
            pos.append(
                np.where(edge_attr_t[f] == 1)[0]
            )
        pos = np.hstack(pos)
        edge_attr = edge_attr[pos, :]
        edge_index = edge_index[:, pos]
        data.edge_index = th.tensor(edge_index)
        data.edge_attr = th.tensor(edge_attr)
        return data

    return augment


def dataset_transform(config):
    config = config['model']

    transform = None
    if 'augment' in config:
        aug = config['augment']
        options = [0, 1, 2, 5, 6]
        if isinstance(aug, list):
            options = aug
            aug = True
        if aug:
            transform = graph_augmention(options)

    return transform


def model_seq(config, base, final):
    if 'dropout' in config:
        return th.nn.Sequential(base,
                                th.nn.Dropout(config['dropout']),
                                final)
    return th.nn.Sequential(base, final)


# Configuration:
#  {
#   'training': {'epoch': 10, 'batch': 32, 'shuffle':True}
#   }
#
#
@task_definition()
def execute_model(tools, config, dataset_path, env=None):

    sparse = False
    if 'sparse' in config:
        sparse = config['sparse']
    config['model']['sparse'] = sparse

    train_dataset = proto_data.BufferedDataset(
                        proto_data.GraphDataset(dataset_path, 'train',
                                                shuffle=True,
                                                sparse=sparse,
                                                transform=dataset_transform(config)))

    validate_size = int(len(train_dataset) * config['training']['validate'])
    valid_dataset = train_dataset[:validate_size]
    train_dataset = train_dataset[validate_size:]

    train_config = config['training']

    loader_config = {
        'shuffle': train_config['shuffle'],
        'batch_size': train_config['batch'],
        'num_workers': 6
    }

    model, out_channels = build_model_from_config(config['model'])

    final = th.nn.Linear(out_channels, tensor_len(tools))
    model = model_seq(config['model'], model, final)
    print(model)

    device = th.device('cuda' if th.cuda.is_available() else 'cpu')
    model = model.to(device)
    train_loader = DataLoader(train_dataset, **loader_config)
    val_loader = DataLoader(valid_dataset, batch_size=32, num_workers=6)

    train_config['tools'] = tools
    # Train model
    model, logit = train_model(train_config, model, train_loader, device,
                               valid_loader=val_loader, validate_step=1000,
                               valid_score=train_config['validate_score'],
                               cache_dir=env.get_cache_dir())

    test_dataset = proto_data.GraphDataset(dataset_path, 'test', sparse=sparse)
    test_config = config['testing']
    test_config['tools'] = tools
    test_config['logit'] = logit
    eval = test_model(test_config,
                      model,
                      DataLoader(test_dataset, **loader_config),
                      device)
    for k, v in eval.items():
        print("Test %s: %f (std: %f)" % (k, v['mean'], v['std']))

    if 'model_key' in config:
        store_model(env.get_db(), config, model, tools,
                    env.get_cache_dir(), eval)


def is_bag(config):
    config = config['model']

    is_bag = True
    if 'ast_type' in config:
        is_bag = config['ast_type'] == 'bag'

    return is_bag


def build_model(config):
    tools, train, test = train_utils.get_svcomp_train_test(
        **config['dataset']
    )
    dataset = proto_data.download_lmdb(
        tools, config['dataset']['competition'],
        train, test, category=config['dataset']['category'],
        ast_bag=is_bag(config)
    )
    return execute_model(tools, config, dataset)


if __name__ == '__main__':
    config = {
        'key': 'test_0',
        'sparse': False,
        'model_key': 'edge_gin_a1_hinge',
        'dataset': {
            'key': '2019_all_categories_all_10000',
            'competition': '2019',
            'category': 'reachability',
            'test_ratio': 0.2,
            'min_tool_coverage': 0.8
        },
        'training': {
            'epoch': 200,
            'batch': 32,
            'shuffle': True,
            'loss': 'hinge',
            'validate': 0.1,
            'validate_score': 'spearmann',
            'optimizer': {
                'type': 'adam', 'lr': 0.01, 'betas': [0.9, 0.98],
                'eps': 1e-09
            },
            'scheduler': {
                'step_size': 50,
                'gamma': 0.5
            }
        },
        'testing': {
            'scores': ['spearmann', 'accuracy:0', 'accuracy:32', 'accuracy:15']
        },
        'model': {
            'ast_type': 'bag',
            'dropout': 0.1,
            'augment': False,
            'node_input': 148,
            'edge_input': 3,
            'global_input': 4,
            'layers': [
                {
                    'node_conv': {
                        'type': 'embedding',
                        'node_dim': 32
                    },
                    'readout': {
                        'type': 'cga'
                    }
                },
                {
                    'node_conv': {
                        'type': 'edge_gin',
                        'node_dim': 32,
                        'edge_dim': 3,
                        'build': {
                            'gin': {
                                'hidden': 32,
                                'dropout': 0.1
                            }
                        }
                    },
                    'readout': {
                        'type': 'cga'
                    }
                }
            ],
            'global_output': {
                'type': 'concatinate'
            }
        }
    }
    train_test = build_model(config)
    with backend.openLocalSession() as sess:
        sess.run(train_test)

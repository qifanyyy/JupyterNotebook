import taskflow as tsk
from taskflow import task_definition, backend

from tasks.utils import train_utils
from tasks.data import proto_data

from tasks.torch.train import build_training
from tasks.torch.graph import build_graph
from tasks.torch.execute import build_visdom_log
from tasks.torch.model_config import partial_to_model, micro_to_partial

import math


@task_definition()
def execute_model(tools, config, dataset_path, ret=None, env=None):

    model_config = config['model']

    if 'type' in model_config:
        model_config = micro_to_partial(model_config)

    if 'layers' in model_config:
        model_config = partial_to_model(model_config, dataset_path)

    model = build_graph(model_config).compile()
    train = build_training(config['train'], model)
    config['model'] = model_config

    visdom = build_visdom_log(config)

    print(train)

    max_it = 0
    for epoch, it, train_loss, val_loss, val_score in train.train_iter(
                                                        tools, dataset_path
                                                    ):

        opt = train.optimizer.optim
        lr = opt.param_groups[0]['lr']
        max_it = max(max_it, it)
        real_it = max_it*epoch + it
        if real_it % 10 == 0:
            print('It %i Lr %f' % (real_it, lr))
            visdom(epoch, lr, train_loss, val_loss, val_score)

        if lr > 10 and train_loss > 1.0:
            exit()


def build_filter(competition, filter_config):
    condition = {}
    for key, limit in filter_config.items():
        condition[key] = limit

    filter = train_utils.filter_by_stat(competition, condition)
    return filter


def build_model(config):
    dataset = config['dataset']
    ast_type = "bag"

    if 'ast_type' in dataset:
        ast_type = dataset['ast_type']
        del dataset['ast_type']

    ast_type = ast_type == 'bag'

    filter = None

    if 'filter' in dataset:
        filter = build_filter(dataset['competition'], dataset['filter'])
        del dataset['filter']

    tools, train, test = train_utils.get_svcomp_train_test(
        **dataset
    )

    dataset = proto_data.download_lmdb(
        tools, dataset['competition'],
        train, test, category=dataset['category'],
        ast_bag=ast_type, filter=filter
    )
    return execute_model(tools, config, dataset)


if __name__ == '__main__':

    config = {
        'name': 'lr_test',
        'model': {
            'layers': [
                {'type': 'embed', 'node_dim': 64},
                {'type': 'edge_gin',
                 'node_dim': 64,
                 'hidden': 32,
                 'dropout': 0.1,
                 'norm': True
                 }
            ],
            'readout': [
                {'type': 'cga'},
                {'type': 'cga'}
            ]
        },
        'dataset': {
            'key': 'rank18_memory_0',
            'competition': '2018',
            'category': 'memory',
            'test_ratio': 0.2,
            'min_tool_coverage': 0.8,
            'ast_type': 'bag'
        },
        'train': {
            'loss': 'masked::HingeLoss',
            'epoch': 200,
            'batch': 32,
            'shuffle': True,
            'augment': False,
            'optimizer': {'type': 'torch::Adam', 'lr': 1e-4,
                          'betas': [0.9, 0.98], 'eps': 1e-09},
            'scheduler': {
                'type': 'torch::StepLR', 'mode': 'step',
                'step_size': 10, 'gamma': 1.05
            }
        },
        'test': {'type': 'category', 'scores': 'spearmann'}
    }

    train_test = build_model(config)
    with backend.openLocalSession() as sess:
        sess.run(train_test)

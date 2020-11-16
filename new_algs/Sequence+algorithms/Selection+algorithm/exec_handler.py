import taskflow as tsk
from taskflow import task_definition, backend

from tasks.torch.execute import build_model

import shutil
import os


def translate_loss(loss_id):

    if loss_id == 'hinge':
        return "masked::HingeLoss"

    if loss_id == 'bce':
        return 'tasks::Rank_BCE'

    if loss_id == 'relational':
        return 'tasks::Relational_Log_Loss'


@task_definition()
def cfg_egin_execute(config, env=None):

    model_layers = [{
        'type': 'embed', 'node_dim': config['embed_size']
    }]

    for i in range(config['model_depth']):
        model_layers.append({
            'type': 'edge_gin',
            'node_dim': config['embed_size'],
            'hidden': config['hidden_size'],
            'norm': True,
            'dropout': 0.1
        })

    model_readout = [{'type': 'cga'} for i in range(len(model_layers))]

    model = {
        'layers': model_layers,
        'readout': model_readout
    }

    cfg = {
        'model': model,
        'dataset': {
            'key': config['dataset_key'],
            'competition': config['competition'],
            'category': config['category'],
            'test_ratio': 0.2,
            'min_tool_coverage': 0.8,
            'ast_type': 'bag'
        },
        'train': {
            'loss': translate_loss(config['loss_func']),
            'epoch': config['epoch'],
            'batch': config['batch_size'],
            'shuffle': True,
            'augment': False,
            'optimizer': {
                'type': 'torch::Adam', 'lr': 0.01,
                'betas': [0.9, 0.98],
                'eps': 1e-9
            },
            'scheduler': {
                'type': 'tasks::SuperConverge', 'mode': 'step',
                'warmup': 40, 'd_model': 32
            },
            'validate': {
                'checkpoint_step': 0,
                'score': 'spearmann',
                'split': 0.1
            }
        },
        'test': {'type': 'category', 'scores': 'spearmann'}
    }

    if 'name' in config:
        cfg['name'] = config['name']

    task = build_model(cfg)
    with backend.openLocalSession() as sess:
        res = sess.run(task)

    shutil.rmtree(env.get_cache_dir())
    os.makedirs(env.get_cache_dir())

    return res


@task_definition()
def egin_execute(name, dataset_key, competition,
                 model_depth, embed_size, hidden_size,
                 batch_size, loss_func,
                 epoch=50, category=None):

    model_layers = [{
        'type': 'embed', 'node_dim': embed_size
    }]

    for i in range(model_depth):
        model_layers.append({
            'type': 'edge_gin',
            'node_dim': embed_size,
            'hidden': hidden_size,
            'norm': True,
            'dropout': 0.1
        })

    model_readout = [{'type': 'cga'} for i in range(len(model_layers))]

    model = {
        'layers': model_layers,
        'readout': model_readout
    }

    config = {
        'model': model,
        'dataset': {
            'key': dataset_key,
            'competition': competition,
            'category': category,
            'test_ratio': 0.2,
            'min_tool_coverage': 0.8,
            'ast_type': 'bag'
        },
        'train': {
            'loss': translate_loss(loss_func),
            'epoch': epoch,
            'batch': batch_size,
            'shuffle': True,
            'augment': False,
            'optimizer': {
                'type': 'torch::Adam', 'lr': 0.01,
                'betas': [0.9, 0.98],
                'eps': 1e-9
            },
            'scheduler': {
                'type': 'torch::CosineAnnealingLR', 'mode': 'epoch',
                'T_max': epoch, 'eta_min': 0.0001
            },
            'validate': {
                'checkpoint_step': 0,
                'score': 'spearmann',
                'split': 0.1
            }
        },
        'test': {'type': 'category', 'scores': 'spearmann'}
    }

    task = build_model(config)
    with backend.openLocalSession() as sess:
        return sess.run(task)

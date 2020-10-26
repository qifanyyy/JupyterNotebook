import optuna

from taskflow import backend


import taskflow as tsk
from taskflow import task_definition, backend

import torch as th

from tasks.utils import train_utils
from tasks.data import proto_data

from tasks.torch.train import build_training, print_log
from tasks.torch.graph import build_graph
from tasks.torch.test import build_test
from tasks.torch.model_config import partial_to_model, micro_to_partial

import time


@task_definition()
def execute_model(tools, config, dataset_path, trial, ret=None, env=None):

    model_config = config['model']

    if 'type' in model_config:
        model_config = micro_to_partial(model_config)

    if 'layers' in model_config:
        model_config = partial_to_model(model_config, dataset_path)

    model = build_graph(model_config).compile()
    train = build_training(config['train'], model)
    config['model'] = model_config

    print(train)

    start_time = time.time()
    best_val = 100
    for epoch, it, train_loss, val_loss, val_score in train.train_iter(
                                                        tools, dataset_path
                                                    ):

        if val_loss is not None:
            print_log(
                epoch, it, train_loss, val_loss, val_score
            )
            best_val = min(1.0 - val_score, best_val)
            trial.report(best_val, epoch)
            print("Time: %f sec" % (time.time() - start_time))
            start_time = time.time()

            if trial.should_prune():
                raise optuna.structs.TrialPruned()

    return best_val


def build_filter(competition, filter_config):
    condition = {}
    for key, limit in filter_config.items():
        condition[key] = limit

    filter = train_utils.filter_by_stat(competition, condition)
    return filter


def build_model(config, trial, ret=None):
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
    return execute_model(tools, config, dataset, trial, ret=ret)


def train_score(trial):

    lr = trial.suggest_loguniform('lr', 1e-5, 1)

    weight_decay = trial.suggest_loguniform('weight_decay', 1e-12, 1e-3)

    config = {
        'model': {
            'layers': [
                {'type': 'embed', 'node_dim': 8},
            ],
            'readout': [
                {'type': 'cga'}
            ]
        },
        'dataset': {
            'key': 'rank18_reachability_0',
            'competition': '2018',
            'category': 'reachability',
            'test_ratio': 0.2,
            'min_tool_coverage': 0.8,
            'ast_type': 'bag'
        },
        'train': {
            'loss': "tasks::Rank_BCE",
            'epoch': 20,
            'batch': 32,
            'shuffle': 42,
            'augment': False,
            'optimizer': {'type': 'torch::Adam', 'lr': lr,
                          'weight_decay': weight_decay},
            'scheduler': {
                'type': 'torch::StepLR', 'mode': 'epoch',
                'step_size': 5, 'gamma': 0.1
            },
            'validate': {
                'checkpoint_step': 0,
                'score': 'spearmann',
                'split': 0.03
            }
        }
    }

    train_test = build_model(config, trial, ret='spearmann')
    with backend.openLocalSession() as sess:
        mean = sess.run(train_test).join()
    return mean


study = optuna.create_study(pruner=optuna.pruners.MedianPruner())
study.optimize(train_score, n_trials=200)

print(study.best_params)
print(1.0 - study.best_value)

import taskflow as tsk
from taskflow import task_definition, backend
import numpy as np

from tasks.utils import train_utils as tu
from tasks.data import proto_data
from tasks.torch.execute import execute_model
from tasks.baseline.kernel_based import svm_train_test
from tasks.baseline.logistic_regression import lr_train_test
from taskflow.distributed import openRemoteSession


@task_definition()
def flag(name, A, B=None, C=None, D=None):
    return "_".join(x for x in [name, A, B, C, D] if x is not None)


def gc_conf_to_gin(config):

    test = config['test']

    if test.startswith("category_"):
        test = {'type': 'category', 'scores': test[9:]}

    gc_conf = config['graph_conv']

    return {
        'model': gc_conf['model'],
        'dataset': config['dataset'],
        'train': gc_conf['train'],
        'test': test
    }


def run_graph_conv(key, config, tools, train, test, ast_type):

    dataset = config['dataset']

    dataset = proto_data.download_lmdb(
        tools, dataset['competition'],
        train, test, category=dataset['category'],
        ast_bag=ast_type
    )

    cfg = gc_conf_to_gin(config)
    name = flag(key, 'gc')
    return execute_model(tools, cfg, dataset, name=name, ret='spearmann')


def run_svm_kernel(key, config, tools, train, test):
    dataset = config['dataset']
    competition = dataset['competition']
    category = None

    if 'category' in dataset:
        category = dataset['category']

    cfg = config['svm_kernel']
    name = flag(key, 'svm', cfg['kernel'])

    C = None
    if 'C' in cfg:
        C = cfg['C']

    return svm_train_test(
        name, tools, cfg['kernel'], train, test,
        competition, category=category
    )


def run_lr(key, config, tools, train, test):
    dataset = config['dataset']
    competition = dataset['competition']
    category = None

    if 'category' in dataset:
        category = dataset['category']

    name = flag(key, 'lr')

    return lr_train_test(
        name, tools, train, test,
        competition, category=category
    )


@task_definition()
def calc_cross_score(key, results, cross=False, env=None):

    db = env.get_db()
    cross_result = db.exp_result

    f = cross_result.find_one({"key": key})

    if f is not None:
        return f['mean'], f['std']

    if not cross:
        cross_result.insert_one({
            'key': key, 'mean': results[0], 'std': results[1]
        })
        return results[0], results[1]

    print(results)
    res = [r[0] for r in results]

    mean, std = np.mean(res), np.std(res)

    cross_result.insert_one({
        'key': key, 'mean': mean, 'std': std
    })

    return mean, std


def run_test(config):

    if 'dataset' not in config:
        raise ValueError("Need to specify dataset config!")

    ast_type = "bag"

    dataset = config['dataset']
    if 'ast_type' in dataset:
        ast_type = dataset['ast_type']
        del dataset['ast_type']

    ast_type = ast_type == 'bag'

    dataset['ret_key'] = True

    tools, train, test, key = tu.get_svcomp_train_test(
        **dataset
    ) if 'test_ratio' in dataset else tu.get_svcomp_cv(**dataset)

    cross = 'test_ratio' not in dataset

    name = config['name']

    jobs = []

    if 'graph_conv' in config:
        gc = run_graph_conv(
            key, config, tools, train, test, ast_type
        )
        gc = tsk.merge([gc])[0]
        jobs.append(
            calc_cross_score(
                "%s_gc" % name, gc, cross=cross
            )
        )

    if 'svm_kernel' in config:
        gc = run_svm_kernel(
            key, config, tools, train, test
        )
        gc = tsk.merge([gc])[0]
        jobs.append(
            calc_cross_score(
                "%s_kernel" % name, gc, cross=cross
            )
        )

    if 'logistic_regression' in config:
        gc = run_lr(
            key, config, tools, train, test
        )
        gc = tsk.merge([gc])[0]
        jobs.append(
            calc_cross_score(
                "%s_lr" % name, gc, cross=cross
            )
        )

    return jobs


if __name__ == '__main__':
    config = {
            'name': "test_cv_2",
            'test': "category_spearmann",
            'dataset': {
                'key': '2019_cv_all_10000',
                'competition': '2019',
                'category': None,
                'cv': 10,
                'min_tool_coverage': 0.8,
                'ast_type': 'bag'
            },
            'graph_conv': {
                'global_constraint': True,
                'model': {
                    'layers': [
                        {'type': 'embed', 'node_dim': 64},
                        {'type': 'edge_gin',
                         'node_dim': 64,
                         'hidden': 64,
                         'dropout': 0.1,
                         'norm': True
                         }
                    ],
                    'readout': [
                        {'type': 'cga'},
                        {'type': 'cga'}
                    ]
                },
                'train': {
                    'loss': 'tasks::Rank_BCE',
                    'epoch': 200,
                    'batch': 32,
                    'shuffle': True,
                    'augment': False,
                    'optimizer': {'type': 'torch::Adam', 'lr': 0.01,
                                  'betas': [0.9, 0.98], 'eps': 1e-09},
                    'scheduler': {
                        'type': 'tasks::SuperConverge', 'mode': 'step',
                        'warmup': 40, 'd_model': 32
                    },
                    'validate': {
                        'checkpoint_step': 0,
                        'score': 'spearmann',
                        'split': 0.1
                    }
                }
            },
            'svm_kernel': {
                'kernel': 'norm_2019_1'
            },
            'logistic_regression': True
        }
    task = run_test(config)
    with openRemoteSession(
        session_id="317e3bb0-caf4-4f57-9975-0e782371a866"
    ) as sess:
        sess.run(task)

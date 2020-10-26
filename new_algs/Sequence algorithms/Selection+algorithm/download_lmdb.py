import taskflow as tsk
from taskflow import backend
import argparse

from tasks.utils import train_utils
from tasks.data import proto_data


def build_filter(competition, filter_config):
    condition = {}
    for key, limit in filter_config.items():
        condition[key] = limit

    filter = train_utils.filter_by_stat(competition, condition)
    return filter


def build_lmdb(name, config, ret=None):
    dataset = config
    ast_type = "bag"

    if 'ast_type' in dataset:
        ast_type = dataset['ast_type']
        del dataset['ast_type']

    ast_type = ast_type == 'bag'

    filter = None

    if 'filter' in dataset:
        filter = build_filter(dataset['competition'], dataset['filter'])
        del dataset['filter']

    test_choice = config['test']
    del config['test']

    tools, train, test = train_utils.get_svcomp_train_test(
        **dataset
    )

    index = test if test_choice else train

    dataset = proto_data.download_plain_lmdb(
        name, tools, dataset['competition'],
        index, category=dataset['category'],
        ast_bag=ast_type, filter=filter
    )
    return dataset


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--category', '-c', default=None)
    parser.add_argument('--split', '-s', default=0, type=int)
    parser.add_argument('--test', '-t', default=False, action='store_true')
    parser.add_argument('--filter', '-f', default=None)

    args = parser.parse_args()

    prefix = 'overall'

    if args.category == 'reach':
        prefix = 'reachability'
    elif args.category == 'term':
        prefix = 'termination'
    elif args.category == 'mem':
        prefix = 'memory'
    elif args.category == 'over':
        prefix = 'overflow'

    category = None
    if prefix != 'overall':
        category = prefix

    split = args.split

    name = 'rank18_%s_%i' % (prefix, split)

    config = {
        'key': name,
        'competition': '2018',
        'category': category,
        'test_ratio': 0.2,
        'min_tool_coverage': 0.8,
        'ast_type': 'bag',
        'test': args.test
    }

    name = name + "_" + ('test' if args.test else 'train')

    if args.filter:
        size = -1
        filter = args.filter
        name = name + "_" + filter
        mult = 1
        label = filter[-1]

        if label == 'k':
            mult = 1e+3
            filter = filter[:-1]
        elif label == 'm':
            mult = 1e+6
            filter = filter[:-1]
        filter = int(filter) * mult

        config['filter'] = {
            'cfg_nodes': filter,
            'cfg_edges': filter,
            'pdg_edges': filter
        }

    print('Download %s ...' % name)

    with backend.openLocalSession() as sess:
        sess.run(
            build_lmdb(name, config)
        )

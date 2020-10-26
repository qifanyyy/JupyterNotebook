import torch as th

from tasks.utils import train_utils
from tasks.data import proto_data

from tasks.torch.train import build_training, print_log
from tasks.torch.graph import build_graph
from tasks.torch.test import build_test
from tasks.torch.model_config import partial_to_model, micro_to_partial

import time
import os
from glob import glob

import argparse
import json
from zipfile import ZipFile
import shutil


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
        if m['score'] < state['score']:
            return m
        else:
            return state

    return save, load_best


def get_checkpoint_dir(config, path):
    if path is None:
        return None

    name = config['name']

    out_path = os.path.join(path, name)

    if not os.path.isdir(out_path):
        os.makedirs(out_path)

    return out_path


def save_stat(epoch, it, train_loss, val_loss, val_score, config,
              checkpoint_path=None):
    if checkpoint_path is None:
        return

    stat_file = os.path.join(checkpoint_path, 'statistics.csv')

    with open(stat_file, 'a+') as o:
        o.write("%i\t%i\t%f\t%f\t%f\n" % (epoch, it, train_loss,
                                          val_loss, val_score))


def print_stat(epoch, it, train_loss, val_loss, val_score):
    text = "Epoch: %i It:%i Train: %f Val: %f Val(score): %f\n" % (epoch, it, train_loss,
                                                                   val_loss, val_score)

    print(text)


def process_loss(epoch, it, train_loss, val_loss, val_score, config,
                 checkpoint_path=None):

    checkpoint_path = get_checkpoint_dir(config, checkpoint_path)

    if val_loss is None:
        val_loss = -1.0
        val_score = -1.0
    else:
        print_stat(epoch, it, train_loss, val_loss, val_score)

    save_stat(epoch, it, train_loss, val_loss, val_score,
              config, checkpoint_path)


def save_checkpoint(epoch, it, train, config, checkpoint_path=None):

    checkpoint_path = get_checkpoint_dir(config, checkpoint_path)

    if checkpoint_path is None:
        return

    path = os.path.join(checkpoint_path, 'epoch_%i.th' % (epoch))

    state = train.optimizer.checkpoint()
    state['epoch'] = epoch

    th.save(state, path)


def resume_or_start(config, model, checkpoint_path):
    checkpoint_path = get_checkpoint_dir(config, checkpoint_path)

    state = None

    if checkpoint_path is not None:

        paths = glob(os.path.join(checkpoint_path, 'epoch_*.th'))

        if len(paths) > 0:
            paths = [(os.path.basename(p), p) for p in paths]
            paths = [(int(p[0][6:-3]), p[1]) for p in paths]
            paths = sorted(paths, key=lambda X: X[0], reverse=True)

            epoch, path = paths[0]
            state = th.load(path)

            print("Resume training at epoch: %i" % state['epoch'])

    train = build_training(config['train'], model, data_key='data')

    if state is not None:
        train.resume(**state)

    return train


def prepare_dataset(path):

    if not path.endswith('.zip'):
        return path, False

    out_path = path[:-4]
    out_path, rest = os.path.split(out_path)

    if not os.path.exists(out_path):
        os.makedirs(out_path)

    with ZipFile(path, 'r') as zipObj:
        zipObj.extractall(out_path)

    return os.path.join(out_path, rest), True


def train_model(tools, config, dataset_path, checkpoint_path=None):

    print('Prepare dataset...')
    dataset_path, cleanup = prepare_dataset(dataset_path)

    model_config = config['model']

    if 'type' in model_config:
        model_config = micro_to_partial(model_config)

    if 'layers' in model_config:
        model_config = partial_to_model(model_config, dataset_path, 'data')

    print("Compile model...")
    model = build_graph(model_config).compile()
    print("Create train process...")
    train = resume_or_start(config, model, checkpoint_path)

    config['model'] = model_config

    print(train)

    start_time = time.time()

    print('Start training...')
    for epoch, it, train_loss, val_loss, val_score in train.train_iter(
                                                        tools, dataset_path
                                                    ):
        if val_loss is not None:
            process_loss(epoch, it, train_loss, val_loss, val_score,
                         config, checkpoint_path)
            save_checkpoint(epoch, it, train, config,
                            checkpoint_path)

            print("Epoch time: %f sec" % (time.time() - start_time))
            start_time = time.time()

    print("Finished training...")

    if cleanup:
        print("Cleanup...")
        shutil.rmtree(dataset_path)

    return model


def test_model(tools, config, dataset_path, model, checkpoint_path=None):

    print('Prepare test dataset...')
    dataset_path, cleanup = prepare_dataset(dataset_path)

    print("Start test...")
    test = build_test(config['test'], data_key='data')

    test_res = test(tools, model, dataset_path)
    test_res['num_params'] = sum(p.numel() for p in model.parameters())

    test_time = test_res['test_time']
    graphs = test_res['num_graphs']
    time_per_graph = (test_time / graphs)

    for k, v in test_res.items():
        if k not in ['test_time', 'num_graphs']:
            print("%s: %s" % (k, str(v)))

    print("Test time: %f (%f pG)" % (test_time, time_per_graph))

    checkpoint = get_checkpoint_dir(config, checkpoint_path)

    if checkpoint is not None:
        path = os.path.join(checkpoint, 'test.json')
        with open(path, "w") as o:
            json.dump(test_res, o, indent=4)

    if cleanup:
        print("Cleanup...")
        shutil.rmtree(dataset_path)

    return test_res


def run(config, train_file, test_file, checkpoint=None):

    model = train_model(
        config['tools'],
        config, train_file,
        checkpoint
    )

    if 'test' in config:
        test_model(config['tools'], config,
                   test_file, model, checkpoint)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('config')
    parser.add_argument('train_file')
    parser.add_argument('test_file')
    parser.add_argument("--checkpoint", '-c')

    args = parser.parse_args()

    config = args.config
    train_file = args.train_file
    test_file = args.test_file
    checkpoint = args.checkpoint

    if not os.path.exists(config):
        print("Unknown config: %s" % config)
        exit()

    with open(config, "r") as i:
        config = json.load(i)

    run(config, train_file, test_file, checkpoint)

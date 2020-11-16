import argparse
import os
import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scenario_name', type=str, default='OPENML-WEKA-2017')
    parser.add_argument('--output_dir', type=str, default=os.path.expanduser('~/experiments/as_insights/ASAPv2'))
    parser.add_argument('--n_repetitions', type=int, default=1)
    parser.add_argument('--n_folds', type=int, default=10)
    parser.add_argument('--n_seeds', type=int, default=3)

    return parser.parse_args()


def run(args):
    path = os.path.join(args.output_dir, "%s_r%d_f%d_s%d.csv" % (args.scenario_name,
                                                                 args.n_repetitions,
                                                                 args.n_folds,
                                                                 args.n_seeds))
    frame = pd.read_csv(path)
    del frame['fold']
    del frame['repetition']
    frame = frame.groupby(by=['scenario_name', 'seed', 'strategy_name']).agg('mean')
    print(frame)


if __name__ == '__main__':
    run(parse_args())

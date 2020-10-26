import argparse
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str, default=os.path.expanduser('~/experiments/as_insights/ASAPv2'))
    parser.add_argument('--output_dir', type=str, default=os.path.expanduser('~/experiments/as_insights/'))
    return parser.parse_args()


def run(args):
    all_results = None
    for scenario_filename in os.listdir(args.input_dir):
        scenario_filepath = os.path.join(args.input_dir, scenario_filename)
        scenario_results = pd.read_csv(scenario_filepath)
        if all_results is None:
            all_results = scenario_results
        else:
            all_results = pd.concat([all_results, scenario_results], axis=0)
        del_column = 'Unnamed: 0'
        if del_column in all_results.columns.values:
            del all_results[del_column]

    # all_results = all_results.groupby(by=['scenario_name', 'strategy_name', 'seed']).mean()
    # del all_results['repetition']
    # del all_results['fold']
    all_results = all_results.reset_index()
    fig, ax = plt.subplots()
    sns.boxplot(x="scenario_name", y='PAR10_score', hue="strategy_name", data=all_results, ax=ax)
    ax.set(yscale="log")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(args.output_dir, 'ASAPv2-PAR10.png'))


if __name__ == '__main__':
    run(parse_args())

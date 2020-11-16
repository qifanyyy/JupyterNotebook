import argparse
import json
import os
from tqdm import tqdm
import shutil

from tasks.data import dataset_tasks as dt
from tasks.utils import train_utils as tu


def load_svcomp(competition_year, out):

    p = os.path.join(out, "svcomp_%s.json" % competition_year)

    if os.path.exists(p):
        with open(p, 'r') as i:
            return json.load(i)

    url = "https://sv-comp.sosy-lab.org/%s/results/results-verified/All-Raw.zip" % competition_year

    path = "./svcomp/svcomp_%s.zip" % competition_year

    path = os.path.join(out, path)
    dt.create_folder(path)

    if not os.path.exists(path):
        dt._download_file(url, path)

    if not os.path.exists(path):
        raise ValueError("Something went wrong for competition: %s" % competition_year)

    comp = dt.read_svcomp_data(path)
    print('Reindex for tasks ids...')
    comp = sort_for_task(comp)

    with open(p, "w") as o:
        json.dump(comp, o, indent=4)

    return comp


def sort_for_task(comp):

    out = {}

    for category, V1 in comp.items():
        for tool, V2 in V1.items():
            for task, label in V2.items():
                entry = {}
                entry['label'], entry['time'] = tu.parse_label(
                    label['status'], label['cputime'], label['ground_truth']
                )

                if task not in out:
                    out[task] = {}
                to = out[task]
                if category not in to:
                    to[category] = {}
                co = to[category]
                co[tool] = entry

    return out


def load_filter(path):

    if path is None or not os.path.exists(path):
        def taut(k):
            return True
        return taut

    print("Load filter %s" % path)
    with open(path, "r") as i:
        F = [k[:-1] for k in i.readlines()]

    F = set(F)

    def test(k):
        return k in F
    return test


def rank_tasks(comp, filter_path=None):
    filt = load_filter(filter_path)
    out = {}

    for task, V in tqdm(comp.items()):
        for category, labels in V.items():
            tools = [t for t in labels.keys() if filt(t)]
            pref = tu.get_preferences(labels, tools)
            rank = tu.get_ranking(pref, tools)

            if task not in out:
                out[task] = {}
            out[task][category] = rank

    return out


def cleanup(base_path, year):

    ddir = os.path.join(base_path, "svcomp")
    if os.path.isdir(ddir):
        shutil.rmtree(ddir)

    info = os.path.join(base_path, "svcomp_%s.json" % year)
    if os.path.isfile(info):
        os.remove(info)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("competition_year")
    parser.add_argument("out")
    parser.add_argument("-f", "--filter", default=None)

    args = parser.parse_args()

    competition_year = args.competition_year
    tmp = args.out

    comp = load_svcomp(competition_year, tmp)
    comp = rank_tasks(comp, args.filter)

    with open(os.path.join(tmp, "svcomp_%s_rank.json" % competition_year), "w") as o:
        json.dump(comp, o, indent=4)

    print("Cleanup..")
    cleanup(args.out, competition_year)

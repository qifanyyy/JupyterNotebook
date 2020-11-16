import json
import argparse
import numpy as np
import matplotlib.pyplot as plt
import os


def unify(times):
    ix = None

    for tool, time in times.items():
        if ix is None:
            ix = set(time.keys())
        else:
            ix = set.intersection(ix, set(time.keys()))

    print("Intersection: %i elements" % len(ix))

    for tool, time in times.items():
        keys = set(time.keys())
        keys = set.difference(keys, ix)

        for k in keys:
            del time[k]


def mean(T):
    out = {}

    for k, V in T.items():
        out[k] = np.mean(V)

    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("old")

    args = parser.parse_args()

    with open(args.input, "r") as i:
        T = json.load(i)

    with open(args.old, "r") as i:
        To = json.load(i)

    first = 'VAS-CoRe'
    second = 'WLJ*'

    M = {first: T, second: To}
    unify(M)

    colors = ['r', 'g', 'k', 'y', 'm', 'c']
    lines = ['', '--', '-.', ':']
    tools = set(['cpa-seq', '2ls', 'esbmc-kind', 'esbmc-incr', 'cbmc', 'symbiotic', 'utaipan', 'ukojak', 'depthk', 'uautomizer'])

    f = plt.figure()
    for tool in [second, first]:
        times = M[tool]

        size = []
        ts = []

        if tool == second:
            print(times)
            times = {k: [v + 0.9074863316658656 for v in V] for k, V in times.items()}

        times = sorted(times.items(), key=lambda X: int(X[0]))

        for n, T in times:
            n = int(n)
            size.extend([n]*len(T))
            ts.extend(T)

        x = np.array(size)
        y = np.array(ts)

        plt.plot(x, y, label=tool)

    plt.xlabel("Number of cfg nodes")
    plt.ylabel("Time in s")
    plt.legend()
    plt.show()

    f.savefig("time_pure_prediction.pdf", bbox_inches='tight')

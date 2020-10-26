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


def reindex(times):
    out = {}

    for k, V in times.items():
        tmp = {}
        for tk, v in V.items():
            tmp[
                tk.replace('.', '_').replace('/', '_')
            ] = v
        out[k] = tmp
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("core")
    parser.add_argument("wlj")
    parser.add_argument("wlj2")
    parser.add_argument("E")

    args = parser.parse_args()

    with open(args.core, "r") as i:
        T = json.load(i)

    with open(args.wlj, "r") as i:
        To = json.load(i)

    with open(args.wlj2, "r") as i:
        T2 = json.load(i)

    with open(args.E, "r") as i:
        E = json.load(i)

    first = 'VAS-CoRe'
    second = 'WLJ'
    third = 'WLJ*'

    M = {first: T, second: To,'E': E}
    M = reindex(M)
    E = M['E']
    del M['E']

    colors = ['r', 'g', 'k', 'y', 'm', 'c']
    lines = ['', '--', '-.', ':']
    tools = set(['cpa-seq', '2ls', 'esbmc-kind', 'esbmc-incr', 'cbmc', 'symbiotic', 'utaipan', 'ukojak', 'depthk', 'uautomizer'])

    times = {}
    for tool, T in M.items():
        if tool not in times:
            times[tool] = {}
        time = times[tool]
        for k, v in T.items():
            if k not in E:
                continue
            f = os.path.basename(k)
            v = min([v, 900])
            if 'unreach-call' in f and 'unreach-call' in E[k]:
                time['S_'+k] = v
            if 'termination' in f and 'termination' in E[k]:
                time['T_'+k] = v
            if 'no-overflow' in f and 'no-overflow' in E[k]:
                time['O_'+k] = v
            if 'valid-' in f and 'valid-memsafety' in E[k]:
                time['M_'+k] = v

    unify(times)

    time = times[second]
    time = list(time.items())
    time = sorted(time, key=lambda X: X[1])
    index = {k[0]: i for i, k in enumerate(time)}

    for tool, time in list(times.items()):
        T = sorted(time.items(), key=lambda X: X[1])
        T = [x[1] for x in T]
        times[tool] = T

    P = [('S_', 'unreach-call'), ('O_', 'no-overflow'), ('T_', 'termination'), ('M_', 'valid-memsafety')]

    otherTime = {}

    for k, V in E.items():
        for p in P:
            if p[0]+k not in index:
                continue

            L = V[p[1]]

            for tool, label in L.items():
                if tool == "name":
                    continue
                if tool not in otherTime:
                    otherTime[tool] = []
                otherTime[tool].append(float(label['time']))

    f = plt.figure()

    c = 0
    over = 0
    for k, v in otherTime.items():
        if k not in tools:
            continue
        otherTime[k] = sorted(v)
        x = np.arange(len(otherTime[k]))
        y = np.array([min([x, 900]) for i, x in enumerate(otherTime[k])])
        plt.plot(x, y, colors[c]+lines[over], label=k)
        c += 1
        if c >= len(colors):
            over += 1
            c = 0

    for tool in [first]:
        time = times[tool]
        x = np.arange(len(time))
        y = np.array(time)
        plt.plot(x, y, color='tab:orange', label=tool)
    plt.axhline(xmin=0, y=60, color='k')
    plt.xlabel("Number of processed programs")
    plt.ylabel("Time in s")
    plt.legend()
    plt.show()

    f.savefig("quantil_time_vas.pdf", bbox_inches='tight')

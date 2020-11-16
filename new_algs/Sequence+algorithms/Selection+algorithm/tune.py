import os
import numpy as np
import re
from operator import itemgetter
from tqdm import tqdm

times = np.array([1, 2, 4, 8, 16, 30, 60, 120, 240])
instancesPerTimePerSize = 10
sizes = np.array([62, 125, 250, 500, 1000, 2000, 4000, 8000]*instancesPerTimePerSize)
sizes = sizes.reshape(instancesPerTimePerSize, -1)
sizes = np.swapaxes(sizes, 0, 1)
sizes = sizes.flatten()

path = os.path.abspath(os.path.join(os.path.pardir, 'tuning'))
files = os.listdir(path)

possibilites = set()

def get_lower_bound(i):
    with open(os.path.join(path, str(i) + "_byArea.log")) as l:
        return int(l.readline().split(" ")[1])

lower_bounds = [get_lower_bound(i) for i in range(sizes.size)]

def f(name, t, res):
    a = int(name.split("_")[0])
    idx = "_".join(".".join(name.split(".")[:-1]).split("_")[1:])
    if idx not in res:
        res[idx] = 0
    with open(os.path.join(path, name)) as log:
        i = t[0]
        lines = [[int(x) for x in l.split(" ")] for l in log.readlines()]
        tts, vvs = zip(*lines)
        j = 0
        while i < t[1]:
            tt, vv = tts[j], vvs[j]
            if j+1 == len(lines) or tts[j+1] > times[i]*1e9:
                # res[idx]+=1 #DEBUG
                res[idx]+=vv/lower_bounds[a]
                i+=1
            else:
                j+=1 

def instances_group(a, t, s):
    assert(t[0] < t[1])
    assert(s[0] < s[1])
    s = (s[0]*instancesPerTimePerSize, s[1]*instancesPerTimePerSize)
    res = dict()
    arr = [name for name in files if re.search(a+"_", name) and s[0] <= int(name.split("_")[0]) < s[1]]
    print("{}, {}-{}s, {}-{} rectangles".format(a, times[t[0]], times[t[1]-1], sizes[s[0]], sizes[s[1]-1]))
    for name in tqdm(arr):
        f(name, t, res)
    r = [(x[0], x[1]/(t[1]-t[0])/(s[1]-s[0])) for x in res.items()]
    r.sort(key=itemgetter(1))
    print(r)
    possibilites.add(r[0][0])

def single_algorithm(a):
    instances_group(a, (0, 9), (0, 8))
    instances_group(a, (0, 5), (0, 4))
    instances_group(a, (0, 5), (4, 8))
    instances_group(a, (5, 9), (0, 4))
    instances_group(a, (5, 9), (4, 8))

algorithms = ["BLmls", "BLsa", "BLts", "BLts2", "SHsa", "graspBldh", "graspBldw", "graspBlda"]
for a in algorithms:
    single_algorithm(a)


# instances_group("BLsa", (0, 5), (4, 8))
# instances_group("BLsa", (0, 5), (0, 4))
# instances_group("SHsa", (0, 5), (0, 4))

print(possibilites)
print(len(possibilites))

# f("13_BLsa_0.995282_100_1.log", (0, 1), dict())

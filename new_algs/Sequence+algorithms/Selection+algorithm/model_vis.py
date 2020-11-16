import numpy as np

import matplotlib
matplotlib.use('TKAgg')

import matplotlib.pyplot as plt
import matplotlib.cm as mplcm
import matplotlib.colors as colors
import random


def load_labels():
    clusters = []
    labels = []
    with open('cluster.txt', "r") as i:
        for s in i:
            label, cluster = s.split(':')
            try:
                cluster = int(cluster[:-1])
            except Exception:
                cluster = random.randint(5, 10000)
            cluster = 0 if cluster < 5 else 1
            labels.append(label)
            clusters.append(cluster)
    return labels, clusters


def load_colors(cluster):
    cm = plt.get_cmap('copper')
    un = np.unique(cluster)
    cNorm  = colors.Normalize(vmin=0, vmax=un.shape[0]-1)
    scalarMap = mplcm.ScalarMappable(norm=cNorm, cmap=cm)
    M = {un[k]: scalarMap.to_rgba(k) for k in range(un.shape[0])}
    return [M[c] for c in cluster]


def load_colors2(cluster):
    return [(1.0, 0, 0, 0.7) if c == 1 else (0, 0.0, 1.0, 0.7) for c in cluster]


def slice_index(cluster):
    clix = []

    for i, k in enumerate(cluster):
        if k < 5:
            clix.append(i)
    return clix


X0 = np.loadtxt('tsne.csv')
X1 = np.loadtxt('tsne_uniform.csv')
label, cluster = load_labels()
colors = load_colors2(cluster)

plt.subplot(121)
plt.scatter(X1[:, 0], X1[:, 1], c=colors)

cluster = np.array(cluster)

plt.subplot(122)
for i in range(2):
    ix = np.where(cluster == i)[0]
    col = [c for j, c in enumerate(colors) if j in ix]
    plt.scatter(X0[ix, 0], X0[ix, 1], c=col, label="type" if i == 0 else 'other')

for i, l in enumerate(label):
    if l == 'FLOAT' or l == 'DOUBLE' or l == 'INT':
        plt.annotate(l, (X0[i, 0], X0[i, 1]))

plt.legend()
plt.show()

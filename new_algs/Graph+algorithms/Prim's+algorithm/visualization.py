import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import comb
from sklearn.metrics.cluster import adjusted_rand_score
import sys

# colors for each class.
LABEL_COLOR_MAP = {
    1 : 'b',
    2 : 'g',
    3 : 'r',
    4 : 'c',
    5 : 'm',
    6 : 'y',
    7 : 'k'
}

# rand index implementation.
def rand_index_score(truth, labels):
    comb_TP_FP = np.sum(comb(np.bincount(truth), 2))
    comb_TP_FN = np.sum(comb(np.bincount(labels), 2))

    A = np.c_[(truth, labels)]

    tp = np.sum(comb(np.bincount(A[A[:, 0] == i, 1]), 2).sum() for i in set(truth))

    fp = comb_TP_FP - tp
    fn = comb_TP_FN - tp
    tn = comb(len(A), 2) - tp - fp - fn
    return (tp + tn) / (tp + fp + fn + tn)

# method = 'k' or 'p'.
method = str(sys.argv[1]).rstrip()

# rand index implementation = 1 (rand index) or 2 (adjusted rand index - scikit-learn).
cluster_eval_mode = int(sys.argv[2])

# dataset.
f = np.loadtxt("../input/data.txt", delimiter="\t")

labels = None
if method == 'k':
    labels = np.loadtxt("../output/kruskal_classes.txt", delimiter="\n", dtype=int)

if method == 'p':
    labels = np.loadtxt("../output/prim_classes.txt", delimiter="\n", dtype=int)

# ground truth labels.
truth = np.loadtxt("../input/classes.txt", delimiter="\n", dtype=int)

# x and y arrays for scatterplot.
x = np.zeros([788])
y = np.zeros([788])

for i in range(788):
    x[i] = f[i][0]
    y[i] = f[i][1]

if cluster_eval_mode == 1:
    print ("Rand Index: " + str(rand_index_score(truth, labels)))

if cluster_eval_mode == 2:
    print ("Adjusted Rand Index: " + str(adjusted_rand_score(truth, labels)))

# show scatterplot
label_color = [LABEL_COLOR_MAP[l] for l in labels]
#plt.plot(x, y)
plt.scatter(x, y, c=label_color)
plt.show()



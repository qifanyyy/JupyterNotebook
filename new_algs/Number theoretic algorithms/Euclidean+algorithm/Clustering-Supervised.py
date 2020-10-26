#Andrew Lang

from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy

data = pd.read_csv('./unbalance.txt', sep=' ')
data = np.array(data)

# data = pd.read_csv('./MopsiLocationsUntil2012-Finland.txt', sep=',')
# data = np.array(data)

def plot(data, centroids):
    plt.scatter(data[:,0],data[:,1])
    plt.scatter(centroids[:, 0], centroids[:, 1])

#Cluster value can be assumed to be 8 (default value)

clusterCount = 8

def entropy(labels):
    info = pd.read_csv('./unbalance-gt.pa', header=None, index_col=False)[0]
    prob = np.zeros((8,8))
    total = np.zeros((8,8))

    for pred, actual in zip(labels, info):
        total[pred-1][actual-1] += 1

    prob = [[val / sum(total[cluster]) for val in total[cluster]] for cluster in range(clusterCount)]

    countLabels = np.zeros((8))
    for x in labels:
        countLabels[x] += 1

    entropyVals = scipy.stats.entropy(prob)
    
    totalEntropy = 0
    for x in range(len(entropyVals)):
        totalEntropy += ((countLabels[x] / len(labels)) * entropyVals[x])
    print("total Entropy: " , totalEntropy)

cluster = KMeans(n_clusters=8).fit(data)
plot(data, cluster.cluster_centers_)

labels = np.array(cluster.labels_)

entropy(labels)

plt.show()
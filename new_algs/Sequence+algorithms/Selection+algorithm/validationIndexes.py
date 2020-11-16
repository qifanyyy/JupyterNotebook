''' ===================== HYBRID SELECTION STRATEGY (HSS) ======================
        Universidade Federal de Sao Carlos - UFSCar, Sorocaba - SP - Brazil

        Master of Science Project       Artificial Intelligence

        Prof. Tiemi Christine Sakata    (tiemi@ufscar.br)
        Author: Vanessa Antunes         (tunes.vanessa@gmail.com)
   
    ============================================================================ '''

import numpy as np
import math
from sklearn.neighbors import NearestNeighbors
from scipy.spatial import distance
from scipy.stats.stats import pearsonr

def centroid(cluster):
    cent = []
    length = len(cluster)

    for _ in range(0, cluster.shape[1]):
        cent.append(np.sum(cluster[:,_]) / length)

    return cent


def variance(partition, dataset):
    dVar = 0

    # Gets the number of clusters in this partition
    lim = int(max(partition['cluster'])) + 1

    minimo = int(min(partition['cluster']))

    for cluster in range(minimo, lim):
        
        # Seleciona os objetos que perencem ao cluster "cluster"
        aux = partition['cluster']==cluster
        X = dataset[aux]
        cent = centroid(X[:]['atrib'])
        varPartial = sum(distance.euclidean(X[obj]['atrib'], cent) for obj in range(0, len(X)))

        dVar += varPartial
    return round(math.sqrt(dVar/len(dataset)), 6)


def connectivity(partition, dataset):
    con = 0
    
    # Number of nearest neighbors is the lesser between 5% of the partition and 10
    numberOfNn = min(int(0.05 * len(partition)), 10)

    # Gets the number of clusters in this partition
    lim = int(max(partition['cluster'])) + 1

    minimo = int(min(partition['cluster']))

    for cluster in range(minimo, lim):
        conPartial = 0

        # Seleciona os objetos que perencem ao cluster "cluster"
        aux = partition['cluster']==cluster
        X = dataset[aux]

        nbrs = NearestNeighbors(n_neighbors=numberOfNn, algorithm='ball_tree').fit(dataset[:]['atrib'])
        distances, indices = nbrs.kneighbors(X[:]['atrib']) # seleciona ele mesmo como um de seus vizinhos

        for obj in range(0, len(X)):
            aux = np.not_equal(partition['cluster'][indices[obj]], cluster)
            conPartial += sum(1.0 / (j + 1) if (aux[j]) else 0 for j in range(0, numberOfNn))
                    
        con += conPartial

    return con

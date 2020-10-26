''' ===================== HYBRID SELECTION STRATEGY (HSS) ======================
        Universidade Federal de Sao Carlos - UFSCar, Sorocaba - SP - Brazil

        Master of Science Project       Artificial Intelligence

        Prof. Tiemi Christine Sakata    (tiemi@ufscar.br)
        Author: Vanessa Antunes         (tunes.vanessa@gmail.com)
   
    ============================================================================ '''

import numpy as np
import math
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn import cluster
from sklearn.neighbors import kneighbors_graph
from sklearn.preprocessing import StandardScaler
from scipy.stats import pearsonr

from scipy.cluster.hierarchy import linkage, fcluster

def region_division_k(X, Y, Name, algorithm, percentage):

    dataK = []
    for x, y in zip(X,Y):
        if len(dataK) > 0:
            dataK = np.append(dataK, [[x,y]], axis=0)
        else:
            dataK = np.array([[x,y]])

    numClusters = int(math.ceil(len(X) * percentage))

    return clustering(dataK, algorithm, numClusters)


def clustering(dataK, alg, numClusters):
    
    # normalize dataset for easier parameter selection
    dataK = StandardScaler().fit_transform(dataK)
    aux = int(round(len(dataK)*0.05))

    # region division algorithm: 1- kmeans, 2- single-link, 3- complete-link, 4- average-link, 5- ward
    if alg == '1':
        print 'kmeans'
        #n_init: numero de inicializacoes com diferente valor de k
        algorithm = cluster.KMeans(n_clusters=numClusters, n_init=30)
        algorithm.fit(dataK)
        if hasattr(algorithm, 'labels_'):
            y_pred = algorithm.labels_.astype(np.int)
        else:
            y_pred = algorithm.predict(dataK)

        return y_pred

    if alg == '2':
        print 'single-link'
        Z = linkage(dataK, method='single', metric='euclidean')

    elif alg == '3':
        print 'complete-link'
        Z = linkage(dataK, method='complete', metric='euclidean')

    elif alg == '4':
        print 'average-link'
        Z = linkage(dataK, method='average', metric='euclidean')

    else: # alg == '5':
        print 'ward'
        Z = linkage(dataK, method='ward', metric='euclidean')

    return fcluster(Z, numClusters, criterion='maxclust')


''' Organizes solutions divided by regions. '''
def solutionsPerRegion(reduced_p_frontX, reduced_p_frontY, reduced_p_frontName, y_pred):
    mydt = np.dtype([('id', np.str_, 100),  ('atrib', np.float32, (2,))])

    uni = np.unique(y_pred)
    reg = [[]] * len(uni)
    for _ in range(0, len(uni)):
        aux = y_pred == uni[_]
        auxx = np.where(aux)

        for x in auxx[0]:
            if len(reg[_]) > 0:
                reg[_] = np.insert(reg[_], len(reg[_]), (reduced_p_frontName[x], [reduced_p_frontX[x], reduced_p_frontY[x]]), axis=0)
            else:
                reg[_] = np.array([(reduced_p_frontName[x], [reduced_p_frontX[x], reduced_p_frontY[x]])], dtype = mydt)
        #selection(reg)
    return reg


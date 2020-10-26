import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import euclidean_distances
from scipy.stats import kurtosis, skew, zscore
import time

def get_distance_metafeatures(dataset_name, df):
    start = time.time()
    record = {'dataset': dataset_name.split('.')[0]}
    distance_vector = []
    for i,vec in enumerate(euclidean_distances(df)):
        for j, value in enumerate(vec):
            if i!=j:
                distance_vector.append(value)
    distance_vector = np.array(distance_vector)
    distance_vector = MinMaxScaler().fit_transform(distance_vector.reshape(-1, 1)).reshape(-1)
    zscores = np.absolute(zscore(distance_vector))
    
    record['MD1'] = np.mean(distance_vector)
    record['MD2'] = np.var(distance_vector)
    record['MD3'] = np.std(distance_vector)
    record['MD4'] = skew(distance_vector)
    record['MD5'] = kurtosis(distance_vector)
    record['MD6'] = np.logical_and(distance_vector>=0, distance_vector<=0.1).sum() / distance_vector.shape[0] * 100
    record['MD7'] = np.logical_and(distance_vector>0.1, distance_vector<=0.2).sum() / distance_vector.shape[0] * 100
    record['MD8'] = np.logical_and(distance_vector>0.2, distance_vector<=0.3).sum() / distance_vector.shape[0] * 100
    record['MD9'] = np.logical_and(distance_vector>0.3, distance_vector<=0.4).sum() / distance_vector.shape[0] * 100
    record['MD10'] = np.logical_and(distance_vector>0.4, distance_vector<=0.5).sum() / distance_vector.shape[0] * 100
    record['MD11'] = np.logical_and(distance_vector>0.5, distance_vector<=0.6).sum() / distance_vector.shape[0] * 100
    record['MD12'] = np.logical_and(distance_vector>0.6, distance_vector<=0.7).sum() / distance_vector.shape[0] * 100
    record['MD13'] = np.logical_and(distance_vector>0.7, distance_vector<=0.8).sum() / distance_vector.shape[0] * 100
    record['MD14'] = np.logical_and(distance_vector>0.8, distance_vector<=0.9).sum() / distance_vector.shape[0] * 100
    record['MD15'] = np.logical_and(distance_vector>0.9, distance_vector<=1).sum() / distance_vector.shape[0] * 100
    record['MD16'] = np.logical_and(zscores >= 0, zscores<1).sum() / zscores.shape[0] * 100
    record['MD17'] = np.logical_and(zscores >= 1, zscores<2).sum() / zscores.shape[0] * 100
    record['MD18'] = np.logical_and(zscores >= 2, zscores<3).sum() / zscores.shape[0] * 100
    record['MD19'] = (zscores >= 3).sum() / zscores.shape[0] * 100
    end = time.time()
    return record, (df.shape[0], df.shape[1], end-start)

    
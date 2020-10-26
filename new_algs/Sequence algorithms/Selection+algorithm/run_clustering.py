import sys
import pandas as pd
from Utils.preprocessing import preprocess
from Algorithms.dbscan import get_dbscan
from Algorithms.khmeans import get_khmeans
from Algorithms.kmeans import get_Kmeans
from Algorithms.mst import get_mst
from Algorithms.single_linkage import get_single_linkage
from Algorithms.eac import get_EAC
from Algorithms.psc import get_psc
from Metrics.metrics import get_internal_measures
from Utils.dataset_values import DatasetValues
import os
import pickle
import json
import numpy as np
from scipy.stats import rankdata

def run(filename: str, dataframe: pd.DataFrame, algname: str, K=None):

    if algname == "dbscan":
        labels = get_dbscan(dataframe)
    elif algname == "khmeans":
        labels = get_khmeans(dataframe, K, 50)
    elif algname == "kmeans":
        labels = get_Kmeans(dataframe, K, 50)
    elif algname == "mst":
        labels = get_mst(dataframe)
    elif algname == "SL":
        labels = get_single_linkage(dataframe)
    elif algname == "eac":
        labels = get_EAC(dataframe)
    elif algname == "psc":
        labels = get_psc(dataframe, K)
    values = DatasetValues(dataframe, labels)
    measures = get_internal_measures(values)
    save_path = os.path.join(os.getcwd(), 'Results', filename.split('/')[-1])
    json.dump(measures, open(save_path + "_" + algname + ".json", 'w'))
    pickle.dump(labels, open(save_path + "_" + algname + ".clusters", 'wb'))

    return measures, labels

def get_ranking(measures):
    ranks = np.zeros(len(measures))
    ranks += rankdata(np.array([m['DB'] for m in measures]))
    ranks += rankdata(-1*np.array([m['SIL'] for m in measures]))
    ranks += rankdata(-1*np.array([m['CH'] for m in measures]))
    ranks += rankdata(-1*np.array([m['DU'] for m in measures]))
    ranks += rankdata(-1*np.array([m['BP'] for m in measures]))
    ranks += rankdata(-1*np.array([m['MC'] for m in measures]))
    ranks += rankdata(np.array([m['HL'] for m in measures]))
    ranks += rankdata(np.array([m['HKK'] for m in measures]))
    # ranks += rankdata(np.array([m['FR'] for m in measures]))
    # ranks += rankdata(-1*np.array([m['GK'] for m in measures]))

    ranks /= 8
    return ranks

def main(filename):
    dataframe = pd.read_csv(filename, header=None)
    dataframe = preprocess(dataframe)
    f_name = filename.split('\\')[-1].split('.')[0]
    measures, labels = [], []
    # Algorithm without K
    measure, label = run(f_name, dataframe, "dbscan")
    measures.append(measure)
    labels.append(label)
    measure, label = run(f_name, dataframe, "mst")
    measures.append(measure)
    labels.append(label)
    measure, label = run(f_name, dataframe, "SL")
    measures.append(measure)
    labels.append(label)
    measure, label = run(f_name, dataframe, "eac")
    measures.append(measure)
    labels.append(label)

    rankings = get_ranking(measures)
    best = np.argmin(rankings)
    K = len(np.unique(labels[best]))
    # Algorithms with K
    measure, label = run(f_name, dataframe, "khmeans", K)
    measures.append(measure)
    labels.append(label)
    measure, label = run(f_name, dataframe, "kmeans", K)
    measures.append(measure)
    labels.append(label)
    measure, label = run(f_name, dataframe, "psc", K)
    measures.append(measure)
    labels.append(label)

    final_rankings = get_ranking(measures)
    final_rankings = np.append(final_rankings, f_name)
    return final_rankings

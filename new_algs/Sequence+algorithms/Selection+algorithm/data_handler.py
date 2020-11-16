#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 18:05:38 2017

@author: rahul
"""

import config
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale


def read_data():
    if config.VERSION == 'PARKINSON':
        data = pd.read_csv(config.DATASET_FILEPATH, sep='\t', header=None)
        dataX = data.iloc[:, :-1]
        dataY = data.iloc[:, -1]
    elif config.VERSION == 'GERMAN':
        data = pd.read_csv(config.DATASET_FILEPATH, sep=',')
        dataX = data.iloc[:, 1:]
        dataY = data.iloc[:, 0]

    dataX = scale(dataX)
    dataX = pd.DataFrame(dataX)
    return dataX, dataY


def read_train_data():
    data = pd.read_csv(config.TRAIN_DATASET_FILEPATH, sep='\t', header = None)
    dataX = data.iloc[:, :-1]
    dataY = data.iloc[:, -1]
    return dataX, dataY


def read_test_data():
    data = pd.read_csv(config.TEST_DATASET_FILEPATH, sep='\t', header = None)
    dataX = data.iloc[:, :-1]
    dataY = data.iloc[:, -1]
    return dataX, dataY


def dataset_with_feature_subset(feature_subset):
    dataX, dataY = read_data()
    drop_index = [i for i, x in enumerate(feature_subset) if x == 0]
    dataX = dataX.drop(dataX.columns[drop_index], axis=1)
    return dataX, dataY


def train_test_set(dataX, dataY):
    trainX, testX, trainY, testY = train_test_split(dataX, dataY, test_size = config.TEST_SIZE)
    return trainX, trainY, testX, testY

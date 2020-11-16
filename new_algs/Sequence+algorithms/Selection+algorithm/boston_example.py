# -*- coding: utf-8 -*-
"""
Created on Tue May 26 18:35:38 2020

@author: Murat Cihan Sorkun

Feature Selection by Genetic Algorithm: An example on Boston dataset 
"""

from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
import numpy as np 
import genetic


boston_dataset = load_boston()
X_train, X_test, y_train, y_test = train_test_split(boston_dataset.data, boston_dataset.target, train_size=0.75, test_size=0.25, random_state=0)
#inject some noise by adding randomly generated features
noisy_features = np.random.uniform(0, 5, size=(len(boston_dataset.data), 17))
boston_noisy_data = np.hstack((boston_dataset.data, noisy_features))
X_train, X_test, y_train, y_test = train_test_split(boston_noisy_data, boston_dataset.target, train_size=0.75, test_size=0.25, random_state=42)


population_size=20
num_of_generations=50
mut_ratio=0.5

#select features from genetic algorithm
selected_features=genetic.select_features(X_train,y_train,population_size,num_of_generations,mut_ratio,"reg",verbose=1)

X_train_selected=genetic.transform_data(X_train,selected_features)
X_test_selected=genetic.transform_data(X_test,selected_features)

print("\nTotal generated features:",boston_noisy_data.shape[1])
print("\nTotal selected features from genetic algorithm:",X_train_selected.shape[1])

print("\nTraining models by neural networks..")
model=MLPRegressor(activation='tanh', hidden_layer_sizes=(100), max_iter=10000, solver='adam')

model.fit(X_train, y_train)
default_score=model.score(X_test, y_test)
print("\nTest score(R2) without feature selection:",default_score)

model.fit(X_train_selected, y_train)
genetic_score=model.score(X_test_selected, y_test)
print("Test score(R2) with genetic selection:",genetic_score)

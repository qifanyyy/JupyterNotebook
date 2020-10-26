#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 19:49:49 2019

@author: ashwathcs
"""
import pandas as pd
import numpy as np
import math
import operator
error = 0 
def train_test_split(dataset, split):
    dataset= dataset.values
    training_idx = np.random.randint(dataset.shape[0], size = int((1-split) * len(dataset)))
    test_idx = np.random.randint(dataset.shape[0], size = int(split * len(dataset)))
    train,test = dataset[training_idx,:], dataset[test_idx,:]
    return (train, test)

def euclidian_distance(x, y):
    sum = 0
    x = x[0:-1]#Exempt the quality column
    y = y[0:-1]
    for i in range(len(x)):
        sum+= (x[i] - y[i])**2
    return math.sqrt(sum)

def nearest_neighbours(trainset, test_instance, k):
    dist = []
    for x in trainset:
        distance = euclidian_distance(x, test_instance)
        dist.append((x,distance))
    #Sort the dist based on the value of distance 
    dist.sort(key=operator.itemgetter(1),reverse = False)
    neighbours = []
    for i in range(k):
        neighbours.append(dist[i][0])
    return neighbours

def category(neighbours):
    #Find the quality of wine by finding the average of the k neighbours
    quality = []
    for i in neighbours:
        quality.append(i[-1]) #Get the quality of the neighbours
    return sum(quality) / len(quality) 

def predict_class(trainset, test_instance, neighbours):
    #Quality predicted by the algorithm
    quality_category = round(category(neighbours))
    #Quality from the test set
    expected = test_instance[-1]
    global error
    if(quality_category!=expected):
         error+=1 #increment error to find the Accuracy
    print('quality predicted: ', quality_category, '-> expected quality: ',expected)

dataset=pd.read_csv('winequality-red.csv')
train, test = train_test_split(dataset, 0.4)
k = 5
for test_instance in test:
    neighbours = nearest_neighbours(train, test_instance, k)
    predict_class(train, test_instance, neighbours)
accuracy = ((len(dataset) - error) / len(dataset)) * 100
print("Accuracy : ",accuracy)

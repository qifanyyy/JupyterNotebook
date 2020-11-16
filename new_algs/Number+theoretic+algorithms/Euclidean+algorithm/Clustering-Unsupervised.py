#Andrew Lang

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import random

#unbalance data
data_unbalance = pd.read_csv('./unbalance.txt', sep=' ')
data_unbalance = np.array(data_unbalance)

#Finland data
data_Finland = pd.read_csv('./MopsiLocationsUntil2012-Finland.txt', sep=',')
data_Finland = np.array(data_Finland)

#Joensuu data
data_Joensuu = pd.read_csv('./MopsiLocations2012-Joensuu.txt', sep=',')
data_Joensuu = np.array(data_Joensuu)


def plot(data, centroids):
    plt.scatter(data[:,0],data[:,1])
    plt.scatter(centroids[:, 0], centroids[:, 1])

#Calculates the distance between a given point and its associated centroid
def EuclideanDistance(point, cent):
    dist = 0.0
    for x in range(len(point)):
        dist += (point[x] - cent[x])**2
    return math.sqrt(dist)

#Calculates the centroids and which points are in which cluster
def kmeans(dataset, k, reassign=True):
    iterations = 0
    maxIterations = 50

    #centroids are random points to begin
    centroids = []
    for x in range(0,k):
        centroids += [random.choice(dataset)]

    #runs through program for specified number of iterations
    while(iterations < maxIterations):
        iterations += 1

        data_distances = np.zeros(len(dataset))
        data_labels = np.zeros(len(dataset))

        #calcuates distance between each datapoint and their associated centroid
        for i in range(len(dataset)):
            centroid_distances = np.zeros((k))
            for x in range(0,k):
                centroid_distances[x] = EuclideanDistance(dataset[i], centroids[x])
            distance_index = centroid_distances.tolist().index(min(centroid_distances))
            data_distances[i] = min(centroid_distances)
            data_labels[i] = distance_index

        #this will sum up the total distances between datapoints
        totalSum = np.zeros((k, k))
        totalIndices = np.zeros((k))
        for x in range(len(dataset)):
            index = int(data_labels[x])
            totalSum[index][0] += dataset[x][0]
            totalSum[index][1] += dataset[x][1]
            totalIndices[index] += 1

        #now to calcuate the new centroids and check if the totalSum is valid
        for x in range(len(totalIndices)):
            ind = -1
            for i in range(len(totalSum)):
                if totalSum[x][i] == 0:
                    ind = x
            if ind != -1:
                centroids[x][0] = (totalSum[x][0] / totalIndices[x])
                centroids[x][1] = (totalSum[x][1] / totalIndices[x])
            else:
                centroids[x] = random.choice(dataset)
        
        if reassign == True:
            #this needs to have euclidean distance between all points in order for it to work so it will have to be an 8x8 matrix of euclid distances
            centroid_Euclid = np.zeros((8,8))
            for x in range(len(centroids)):
                for i in range(len(centroids)):
                    #in order to not get 0 in the array
                    if x == i:
                        centroid_Euclid[x][i] = 999999
                    else:
                        centroid_Euclid[x][i] = EuclideanDistance(centroids[x], centroids[i])
            
            for x in range(len(centroid_Euclid)):
                for i in range(len(centroid_Euclid)):
                    if centroid_Euclid[x][i] <= 40000:
                        centroids[x] = random.choice(dataset)
    return centroids

#reassign needs to be False for Joensuu and Finland, True for unbalanced
finalCentroids = kmeans(data_Joensuu, 4, reassign=False)
finalCentroids = np.array(finalCentroids)
print(finalCentroids)
plot(data_Joensuu, finalCentroids)

plt.show()
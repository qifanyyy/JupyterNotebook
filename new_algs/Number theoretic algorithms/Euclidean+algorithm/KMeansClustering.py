# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 21:42:47 2017

@author: Jyoti
"""
import pandas as pd
import math
import random
import plotly
import numpy
from plotly.graph_objs import Scatter, Scatter3d, Layout


def readData():
    """Read Data From csv files"""
    f = input("Enter the csv file name from which data is to be read : ")
    csv_data = pd.DataFrame.from_csv(f, index_col = None)
    number_of_attributes=input("Enter the number of attributes for kmeans clustering : ")
    number_of_attributes = int(number_of_attributes)
    attribute_arr=list()
    for i in range(0,number_of_attributes):
        attr = input("Enter the attribute name : ")
        attribute_arr.append(attr)
    attribute_list = csv_data[attribute_arr] 
    data1 = attribute_list[attribute_arr[0]]
    data2 = attribute_list[attribute_arr[1]]
    data3 = attribute_list[attribute_arr[2]]
    points=list()
    for i in range(0,len(data1)):
         arr=numpy.array([data1[i],data2[i],data3[i]])    
         points.append(DataPointObject(arr.tolist()))   
    num_clusters = input("Enter number of clusters : ")     
    return points, number_of_attributes, int(num_clusters)
    
def main():
    points=list()
    points, dimensions, num_clusters = readData()
    print("Dimensions : ", dimensions)
    #Applying KMeans Clutering on data
    clusters = computekmeansAlgo(points, num_clusters)
    #Output the clusters
    for i, c in enumerate(clusters):
        for p in c.points:
            print(" Cluster: ", i, "\t Data :", p)
    # Display clusters using plotly
    print("Plotting the k-means cluster on browser....")
    plotKMeansCluster(clusters, dimensions)

class DataPointObject(object):
    """Data point extracted from excel file"""
    def __init__(self, coords):        
        self.coords = coords
        self.n = len(coords)
    def __repr__(self):
        return str(self.coords)

class Cluster(object):
    def __init__(self, points):
        if len(points) == 0:
            raise Exception("Cluster is empty")

        # The points that belong to this cluster
        self.points = points
        self.centroid = self.findCentroid()

    def __repr__(self):
        return str(self.points)

    def updateData(self, points):
        """Returns the distance between the previous centroid and the new after
        recalculating and storing the new centroid."""
        old_centroid = self.centroid
        self.points = points
        self.centroid = self.findCentroid()
        shift = calcEuclideanDistance(old_centroid, self.centroid)
        return shift

    def findCentroid(self):
        """FInd the centroid for clustering data """
        numPoints = len(self.points)
        # Get a list of all coordinates in this cluster
        coords = [p.coords for p in self.points]
        # Reformat that so all x's are together, all y'z etc.
        unzipped = zip(*coords)
        # Calculate the mean for each dimension
        centroid_coords = [math.fsum(dList)/numPoints for dList in unzipped]
        return DataPointObject(centroid_coords)

def computekmeansAlgo(points, k):
    # Pick out k random points to use as our initial centroids
    initial = random.sample(points, k)
    cutoff = 0.2
    # Create k clusters using those centroids
    # Note: Cluster takes lists, so we wrap each point in a list here.
    clusters = [Cluster([p]) for p in initial]
    # Loop through the dataset until the clusters stabilize
    loopCounter = 0
    while True:
        lists = [[] for _ in clusters]
        clusterCount = len(clusters)
        loopCounter += 1
        # For every point in the dataset ...
        for p in points:
            # Get the distance between that point and the centroid of the first cluster.
            smallest_distance = calcEuclideanDistance(p, clusters[0].centroid)
            # Set the cluster this point belongs to
            clusterIndex = 0
            # For the remainder of the clusters ...
            for i in range(clusterCount - 1):
                # calculate the distance of that point to each other cluster's
                # centroid.
                distance = calcEuclideanDistance(p, clusters[i+1].centroid)

                if distance < smallest_distance:
                    smallest_distance = distance
                    clusterIndex = i+1
            #After finding the smallest distance, classify the datapoint into clusters
            lists[clusterIndex].append(p)
        
        biggest_shift = 0.0
        # For each cluster
        for i in range(clusterCount):
            #Finding how far the centroid has shifted
            shift = clusters[i].updateData(lists[i])
            # Keep track of the largest move from all cluster centroid updates
            biggest_shift = max(biggest_shift, shift)
        #If the centroids are not moving much, we stop the process
        if biggest_shift < cutoff:
            print("Finally Converged after %s iterations" % loopCounter)
            break
    return clusters

def plotKMeansCluster(data, dimensions):
    """Plots the kmeans output and displays it on web browser"""
    axisList = []
    for i, c in enumerate(data):
        cluster_data = []
        for point in c.points:
            cluster_data.append(point.coords)
        axis = {}
        centroid = {}
        if dimensions == 2:
            print("Displaying graph with 2 dimensions....")
            axis['x'], axis['y'] = zip(*cluster_data)
            axis['mode'] = 'markers'
            axis['marker'] = {}
            axis['marker']['symbol'] = i
            axis['marker']['size'] = 12
            axis['name'] = "Cluster " + str(i)
            axisList.append(Scatter(**axis))
            centroid['x'] = [c.centroid.coords[0]]
            centroid['y'] = [c.centroid.coords[1]]
            centroid['mode'] = 'markers'
            centroid['marker'] = {}
            centroid['marker']['symbol'] = i
            centroid['marker']['color'] = 'rgb(200,10,10)'
            centroid['name'] = "Centroid " + str(i)
            axisList.append(Scatter(**centroid))
        else:
            print("Displaying graph with 3 dimensions....")
            symbols = ["circle","square","diamond","circle-open","square-open","diamond-open","cross", "x"]
            axis['x'], axis['y'], axis['z'] = zip(*cluster_data)
            axis['mode'] = 'markers'
            axis['marker'] = {}
            axis['marker']['symbol'] = symbols[i]
            axis['marker']['size'] = 12
            axis['name'] = "Cluster " + str(i)
            axisList.append(Scatter3d(**axis))
            centroid['x'] = [c.centroid.coords[0]]
            centroid['y'] = [c.centroid.coords[1]]
            centroid['z'] = [c.centroid.coords[2]]
            centroid['mode'] = 'markers'
            centroid['marker'] = {}
            centroid['marker']['symbol'] = symbols[i]
            centroid['marker']['color'] = 'rgb(200,10,10)'
            centroid['name'] = "Centroid " + str(i)
            axisList.append(Scatter3d(**centroid))
    ##Plot the Kmeans output on web browser page        
    #title = "K-means clustering" % str(len(data))
    title = "K-means clustering with %s clusters" % str(len(data))
    plotly.offline.plot({"data": axisList,"layout": Layout(title=title)})

def calcEuclideanDistance(a, b):
    """Calculate Euclidean distance between two n-dimensional points."""
    if a.n != b.n:
       raise Exception("POints with different dimensions encountered!")
    difference = 0.0
    for i in range(a.n):
        squareDifference = pow((a.coords[i]-b.coords[i]), 2)
        difference += squareDifference
    distance = math.sqrt(difference)
    return distance

if __name__ == "__main__":
    main()

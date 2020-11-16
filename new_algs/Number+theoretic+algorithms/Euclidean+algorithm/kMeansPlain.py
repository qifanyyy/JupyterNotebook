import math
import random
import time
import operator
from math import*
from Tkinter import *

######################################################################
# This section contains functions for loading CSV (comma separated values)
# files and convert them to a dataset of instances.
# Each instance is a tuple of attributes. The entire dataset is a list
# of tuples.
######################################################################

# Loads a CSV files into a list of tuples.
# Ignores the first row of the file (header).
# Numeric attributes are converted to floats, nominal attributes
# are represented with strings.
# Parameters:
#   fileName: name of the CSV file to be read
# Returns: a list of tuples

def loadCSV(fileName, noOfFeatures):
    fileHandler = open(fileName, "rt")
    lines = fileHandler.readlines()
    fileHandler.close()
    del lines[0] # remove the header
    dataset = []
    for line in lines:
        instance = lineToTuple(line)
        dataset.append(instance[:noOfFeatures])
    return dataset

# Converts a comma separated string into a tuple
# Parameters
#   line: a string
# Returns: a tuple
def lineToTuple(line):
    # remove leading/trailing witespace and newlines
    cleanLine = line.strip()
    # get rid of quotes
    cleanLine = cleanLine.replace('"', '')
    # separate the fields
    lineList = cleanLine.split(",")

    # convert strings into numbers
    stringsToNumbers(lineList)
    lineTuple = tuple(lineList)
    return lineTuple

# Destructively converts all the string elements representing numbers
# to floating point numbers.
# Parameters:
#   myList: a list of strings
# Returns None
def stringsToNumbers(myList):
    for i in range(len(myList)):
        if (isValidNumberString(myList[i])):
            myList[i] = float(myList[i])

# Checks if a given string can be safely converted into a positive float.
# Parameters:
#   s: the string to be checked
# Returns: True if the string represents a positive float, False otherwise
def isValidNumberString(s):
  if len(s) == 0:
    return False
  if  len(s) > 1 and s[0] == "-":
      s = s[1:]
  for c in s:
    if c not in "0123456789.":
      return False
  return True


######################################################################
# This section contains functions for clustering a dataset
# using the k-means algorithm.
######################################################################

def distance (instance1, instance2):
    #result = euclidean_default(instance1, instance2)
    #result = euclidean_similarity(instance1, instance2)
    #result = cosine_similarity(instance1, instance2)
    result = jaccard_similarity(instance1, instance2)
    return result

def euclidean_default(instance1, instance2):
    if instance1 == None or instance2 == None:
        return float("inf")
    sumOfSquares = 0
    #print ("Instance 1 length " + str(len(instance1)))
    for i in range(1, len(instance1)):
        #print instance1[i]
        sumOfSquares += (instance1[i] - instance2[i])**2
    #print "Sum of Squares "
    #print sumOfSquares
    return sumOfSquares

def euclidean_similarity(instance1, instance2):
    if instance1 == None or instance2 == None:
        return float("inf")
    sumOfSquares = 0
    for i in range(1, len(instance1)):
        #print instance1[i]
        sumOfSquares += (instance1[i] - instance2[i])**2
    #convert to similarity
    result = round((1/( 1 + sumOfSquares)),3)
    #print ("Euclidean similarity " + str(result))
    return result

def square_rooted(x):
    return round(sqrt(sum([a*a for a in x])),3)

def cosine_similarity(article1,article2):
    if article1 == None or article2 == None:
        return float("inf")

    numerator = 0
    denominator1 = 0
    denominator2 = 0

    for i in range(1, len(article1)):
        numerator += article1[i] * article2[i]
        denominator1 += article1[i] * article1[i]
        denominator2 += article2[i] * article2[i]

    denominator = sqrt(denominator1) * sqrt(denominator2) 
    # numerator = sum(a*b for a,b in zip(article1[:-1],article2[:-1]))
    # denominator = square_rooted(article1[:-1])*square_rooted(article2[:-1])
    if denominator == 0 :
        result = float('inf')
    else:
        result = round(numerator/float(denominator),3)

    #print ("Cosine similarity " + str(result))
    return result

def jaccard_similarity(article1, article2):
    if article1 == None or article2 == None:
        return float("inf")

    numerator = 0
    denominator = 0
    for index in range(1, len(article1)):
        #for b in article2:
        if article2[index] >= article1[index]:
            numerator += article1[index]
            denominator += article2[index]
        else:
            numerator += article2[index]
            denominator +=article1[index]

    if denominator == 0:
        result = float('inf')
    else:
        result = round(numerator/float(denominator),3)

    #print ("Jaccard similarity " + str(result))
    return result


def meanInstance(name, instanceList):
    numInstances = len(instanceList)
    #print ("Number of instances: " + str(numInstances))
    if (numInstances == 0):
        return
    numAttributes = len(instanceList[0])
    #print ("Number of attributes: " + str(instanceList[0][0]))
    means = [name] + [0] * (numAttributes - 1)
    #print means
    for instance in instanceList:
        for i in range(1, numAttributes):
        	means[i] += instance[i]
    for i in range(1, numAttributes):
        means[i] /= float(numInstances)
    #print ("Means: " + str(means))
    return tuple(means)

def assign(instance, centroids):
    minDistance = distance(instance, centroids[0])
    minDistanceIndex = 0
    for i in range(1, len(centroids)):
        d = distance(instance, centroids[i])
        if (d < minDistance):
            minDistance = d
            minDistanceIndex = i
    return minDistanceIndex

def createEmptyListOfLists(numSubLists):
    myList = []
    for i in range(numSubLists):
        myList.append([])
    return myList

def assignAll(instances, centroids):
    clusters = createEmptyListOfLists(len(centroids))
    for instance in instances:
        clusterIndex = assign(instance, centroids)
        clusters[clusterIndex].append(instance)
    return clusters

def computeCentroids(clusters):
    centroids = []
    for i in range(len(clusters)):
        name = "centroid" + str(i)
        centroid = meanInstance(name, clusters[i])
        #print (" Mean Centroid : " + str(i) +" " + str(centroid))
        centroids.append(centroid)
    return centroids

def kmeans(instances, k, animation=False, initCentroids=None):
    result = {}
    if (initCentroids == None or len(initCentroids) < k):
        # randomly select k initial centroids
        random.seed(time.time())
        centroids = random.sample(instances, k)
    else:
        centroids = initCentroids

    print ("Initial Centroids ")
    for i in range(len(centroids)):
        print ("Initial Centroid " + str(i) +"   "+ str(centroids[i]))

    prevCentroids = []

    iteration = 0
    while (centroids != prevCentroids and iteration <= 500):
        iteration += 1
        #print iteration
        clusters = assignAll(instances, centroids)
        prevCentroids = centroids
        centroids = computeCentroids(clusters)

        # for i in range(len(centroids)):
        #     print ("Intermediate: " + str(i)+" " + str(centroids[i]))

        #print ("Centroids " +  str(len(centroids[0])) +" " + str(centroids[0]))
        withinss = computeWithinss(clusters, centroids)
    result["clusters"] = clusters
    result["centroids"] = centroids
    result["withinss"] = withinss
    return result

def computeWithinss(clusters, centroids):
    result = 0

    for i in range(len(centroids)):
        centroid = centroids[i]
        cluster = clusters[i]
        #print centroid
        #print ("Centroid length: " + str(i)+ " " + str(len(centroids[i])))
        #print centroids[i]
        for instance in cluster:
            result += distance(centroid, instance)
    return result

# Repeats k-means clustering n times, and returns the clustering
# with the smallest withinss
def repeatedKMeans(instances, k, n):
    bestClustering = {}
    bestClustering["withinss"] = float("inf")
    for i in range(1, n+1):
        print ("k-means trial %d," % i ,)
        trialClustering = kmeans(instances, k)
        print ("withinss: %.1f" % trialClustering["withinss"])
        if trialClustering["withinss"] < bestClustering["withinss"]:
            bestClustering = trialClustering
            minWithinssTrial = i
    print ("Trial with minimum withinss:", minWithinssTrial)
    return bestClustering


######################################################################
# This section contains functions for visualizing datasets and
# clustered datasets.
######################################################################

def printTable(instances):
    for instance in instances:
        if instance != None:
            line = str(len(instance))+" " + instance[0] + "\t"
            for i in range(1, len(instance)):
                line += "%.2f " % instance[i]
            print (line)

def extractAttribute(instances, index):
    result = []
    for instance in instances:
        result.append(instance[index])
    return result


def mergeClusters(clusters):
    result = []
    for cluster in clusters:
        result.extend(cluster)
    return result


def saveClustersAndCentroid(clusterNum, centroid, currCluster):
	#with open("EuclideanDefaultGeneral/euclideanDefaultcluster_%s.txt" % str(clusterNum) , 'w') as f:
    #with open("EuclideanSimilarityGeneral/euclideanSimcluster_%s.txt" % str(clusterNum) , 'w') as f:
    #with open("CosineSimilarityGeneral/cosineSimcluster_%s.txt" % str(clusterNum) , 'w') as f:
    with open("JaccardSimilarityGeneral/jaccardSimcluster_%s.txt" % str(clusterNum) , 'w') as f:
        if(centroid != None):
            for i in range(len(centroid)):
            	if i > 0:
                    f.write(str(round(centroid[i],5))+",")
                else:
                    f.write(str(centroid[i])+",")
            f.write("\n")
        for clusterMember in currCluster:
            for i in range(len(clusterMember)):
                f.write(str(round(clusterMember[i], 5))+",")
            f.write("\n")
    f.close()

def saveCentroidsToAFile(centroid):
	#with open("EuclideanSimilarityGeneral/euclideanSimCentroids.csv", 'a') as f:
	#with open("CosineSimilarityGeneral/cosineSimCentroids.csv", 'a') as f:
	with open("JaccardSimilarityGeneral/jaccardSimCentroids.csv", 'a') as f:
	#with open("EuclideanDefaultGeneral/euclideanDefaultCentroids.csv", 'a') as f:
		if(centroid != None):
			for i in range(len(centroid)):
				if i > 0:
					f.write(str(round(centroid[i],5))+",")	
				else:
					f.write(str(centroid[i])+",")
			f.write("\n")
    


######################################################################
# Test code
######################################################################

#dataset = loadCSV("output/")
dataset = loadCSV("article_word_freq2.csv", 50)
#dataset = loadCSV("tshirts-G.csv")
# print dataset[:3]
# dataset = loadCSV("/home/davide/15-110/datasets/tshirts-H.csv")
# dataset = loadCSV("/home/davide/15-110/datasets/tshirts-I.csv")
# dataset = loadCSV("/home/davide/15-110/datasets/tshirts-J.csv")
# dataset = loadCSV("data/tshirts-G-nooutliers.csv")
# showDataset2D(dataset)

noOfClusters = 5
clustering = kmeans(dataset, noOfClusters)
# for i in range(0, noOfClusters):
#     print ("Size of Cluster " + str(i) +" " + str(len(clustering["clusters"][i])))
#     saveClustersAndCentroid(i, clustering["centroids"][i], clustering["clusters"][i])
#     saveCentroidsToAFile(clustering["centroids"][i])

printTable(clustering["centroids"])

print (clustering["withinss"])

#import findspark
#findspark.init()

import os, sys
from pyspark import SparkContext
import time
import math
import Queue
import collections
from collections import OrderedDict
import operator

import networkx as nx
from networkx import connected_component_subgraphs
from networkx import number_connected_components
from networkx import connected_components
import community
#from networkx.algorithms.community import best_partition
#from community import community_louvain
#import community.community_louvain as community

start = time.time()
sc = SparkContext(appName="AnkithaR")

#inputFile = "E:/USC/DataMining/Assignment/Assignment4/Assignment_04/Description/data/ratings.csv"
#inputFile = "ratings.csv"
inputFile = sys.argv[1]
fileContents = sc.textFile(inputFile)
RDD = fileContents.zipWithIndex().filter(lambda (row,index): index > 0).keys().map(lambda x:x.split(','))
RDDUserToMovie = RDD.map(lambda x : (int(x[0]),int(x[1]))).groupByKey().sortByKey().map(lambda x : (x[0],set(x[1]))).collect()

listOfEdges = []
lenOfRDDUserToMovie = len(RDDUserToMovie)
for i in range(lenOfRDDUserToMovie-1):
    for j in range(i+1,lenOfRDDUserToMovie):
        commonMovies = RDDUserToMovie[i][1] & RDDUserToMovie[j][1]
        if len(commonMovies) >= 9:
            listOfEdges.append((RDDUserToMovie[i][0],RDDUserToMovie[j][0]))
            
GraphBFS=nx.Graph()
GraphBFS.add_edges_from(listOfEdges)
partition = community.best_partition(GraphBFS)

dictComm = {0:[],1:[],2:[]}
for i in partition.keys():
    if partition[i] == 0:
        dictComm[0].append(i)
    elif partition[i] == 1:
        dictComm[1].append(i)
    else:
        dictComm[2].append(i)
        
#f2 = open("E:/USC/DataMining/Assignment/Assignment4/tmp/Ankitha_Radhakrishna_Community_Task3.txt",'w')
f2 = open("Ankitha_Radhakrishna_Community_Task3.txt",'w')
strComm2 = ""
for j in dictComm.keys():
    ls = dictComm[j]
    strComm2 += str(sorted(ls))+"\n"
f2.write(strComm2)
f2.close()

mod = community.modularity(partition,GraphBFS)
print mod


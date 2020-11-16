from pyspark import SparkContext
from random import randint
import itertools
import collections
import sys
import csv
import math
import time
import numpy

import scipy as sp

inputfile = sys.argv[1]

sc = SparkContext('local[10]','task1')

tt = time.time()

data = sc.textFile(inputfile)

rdd = data.map( lambda x: x.split(',') )\
            .filter( lambda x: 'userId' not in x )\
            .map( lambda x: ( int(x[1]) , [int(x[0])] ) )\
            .reduceByKey( lambda x,y: x+y )\
            .collect()

edgelist = {}

for each in rdd:    
    comb = list(itertools.combinations(each[1],2))
    for pair in comb:
        if(pair in edgelist):
            edgelist[pair]+=1
        else:
            edgelist[pair]=1


for key,value in edgelist.items():
    if (edgelist[key] < 9):  
        del edgelist[key]
    
        

import networkx as nx

G = nx.Graph()

G.add_edges_from(edgelist.keys())


d = {}

for key in edgelist:
    d[key]=0 


#dictionary of edges
edgebetweenness = nx.algorithms.centrality.edge_betweenness_centrality(G, k=None, normalized=False, weight=None, seed=None)
eb = {}
for each in edgebetweenness:
    eb[edgebetweenness[each]] = each

eblist = sorted(eb.items(),reverse=True)

# print eblist

A = nx.adjacency_matrix(G)
b = A.toarray()


m =  G.number_of_edges()
# print len(edgelist)


degree = G.degree()
degreedict = dict(degree)

# print degreedict

nodes = G.nodes
n = len(nodes)


# a= [0]*(n+1)
# for i in range(n+1):
#     a[i] = [0] * (n+1)

a={}


for i in range(1,n+1):
    for j in range(1,n+1):
        a[(i,j)] = b[i-1][j-1] - (degreedict[i]*degreedict[j])/(2.0*m)


no_of_comm = 0
mod = -1


for edge in eblist:
    
    t = edge[1]

    G.remove_edge(*t)
    newcomm = list(nx.connected_components(G))
    
    no_of_comm2 = len(newcomm)

    if no_of_comm2 > no_of_comm:
        no_of_comm = no_of_comm2
        
        summ=0
        
        # ttt = time.time()
        for comm in newcomm:
            # commlist = list(itertools.combinations(comm,2))
            #for pair in commlist:
            for i in comm:
                for j in comm: 
                    summ += a[(i,j)]
            
        mod1 = (summ/(2.0*m))
        
        # print time.time() - ttt


        if( mod1 > mod ):
            mod = mod1
            finallist = newcomm


# print mod
# print finallist

finallist2 = []

for each in finallist:
    finallist2 += [sorted(each)]

finallist2 =sorted(finallist2)

print (time.time()-tt)
    
# print finallist2


outputfile = open("Snehal_Shirgure_Community.txt","w+")

for each in finallist2:
    outputfile.write( str(each) )
    outputfile.write("\n")
outputfile.close()





from pyspark import SparkContext
from random import randint
import itertools
import collections
import sys
import csv
import math
import time
import numpy

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
from networkx.algorithms import community


G = nx.Graph()



G.add_edges_from(edgelist.keys())



#dictionary of edges
edgebetweenness = nx.algorithms.centrality.edge_betweenness_centrality(G, k=None, normalized=False, weight=None, seed=None)
eb = {}
for each in edgebetweenness:
    eb[edgebetweenness[each]] = each

eblist = sorted(eb.items(),reverse=True)

        

A = nx.adjacency_matrix(G)
b = A.toarray()

m =  G.number_of_edges()

degree = G.degree()
degreedict = dict(degree)

nodes = G.nodes
n = len(nodes)
a={}

for i in range(1,n+1):
    for j in range(1,n+1):
        a[(i,j)] = b[i-1][j-1] - (degreedict[i]*degreedict[j])/(2.0*m)


no_of_comm = 0
mod = -1

communities_generator = community.girvan_newman(G)

for edge in eblist:
    
    next_level_communities = next(communities_generator)
    finallist = sorted(map(sorted, next_level_communities))
    # print finallist
    summ=0

    for comm in finallist:
        for i in comm:
            for j in comm: 
                summ += a[(i,j)]
        
    mod1 = (summ/(2.0*m))
    
    # print time.time() - ttt

    if( mod1 > mod ):
        mod = mod1
        finallist2 = sorted(map(sorted, next_level_communities))

print mod


outputfile = open("Snehal_Shirgure_Bonus.txt","w+")

for each in finallist2:
    outputfile.write( str(each) )
    outputfile.write("\n")
outputfile.close()




# outputfile = open("Snehal_Shirgure_Bonus.txt","w+")

# for each in finallist2:
#     outputfile.write( str(each) )
#     outputfile.write("\n")
# outputfile.close()





# comm = list(community.girvan_newman(G))

# print comm


# from networkx import edge_betweenness_centrality as betweenness

# def most_central_edge(G):
#     centrality = betweenness(G, weight=None)
#     return max(centrality, key=centrality.get)


# for edge in edgelist:
    
#     G.remove_edge(*edge)
#     comp = list(community.girvan_newman(G, most_valuable_edge=most_central_edge))
#     maxlen = len(comp)





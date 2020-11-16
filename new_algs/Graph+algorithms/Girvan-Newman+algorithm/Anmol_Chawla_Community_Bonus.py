import networkx as nx
from networkx.algorithms import community
from pyspark import SparkContext
from collections import defaultdict
from collections import OrderedDict
import sys
import os
from itertools import chain, combinations
from operator import add
from itertools import izip
from pyspark.sql import SparkSession
import itertools
import time
import math
from collections import OrderedDict
from collections import Counter
from random import randint
import networkx as nx
from networkx import edge_betweenness_centrality
import itertools
#from networkx import girvan_newman

# Setup
sc = SparkContext('local[*]','bo')

# Input arguments
ipfile = sys.argv[1]
filename = "Anmol_Chawla_Community_Bonus.txt"



data = sc.textFile(ipfile)



# Check if set makes a differnece or not
top  = data.first()
data = data.filter(lambda x : x != top).cache()
usermovie = data.map(lambda line:line.split(",")).map(lambda x:(int(x[0]),int(x[1]))).groupByKey().sortByKey().map(lambda x:( x[0],set(x[1]))  ).filter(lambda x: len(x[1]) >= 9).collect()
users = data.map(lambda line:line.split(",") ).map(lambda x: (int(x[0]),1) ).distinct().sortByKey().map(lambda x: x[0])

# Finding pairs which are an edge
edges = []
for i in range(len(usermovie)):
  for j in range(len(usermovie)):
    if ( (usermovie[i][0] != usermovie[j][0]) and (len(usermovie[i][1].intersection(usermovie[j][1])) >= 9 ) ):
      hold = (usermovie[i][0], usermovie[j][0])
      edges.append(hold)

# Running BFS and finding betweeness
OG = nx.Graph()
OG.add_edges_from(edges)


start = time.time()
G = OG.copy()
communities_generator = nx.algorithms.community.girvan_newman(G)
for i in range(4):
  solution = tuple(sorted(i) for i in next(communities_generator))
stop = time.time()
print("Time:",(stop-start))

with open(filename, 'w') as caseop:
	for i in solution:
		hold = str(i).replace(" ","")
		print(hold)
		caseop.write("{}\n".format(hold))
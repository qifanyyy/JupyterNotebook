import pyspark
import csv
import sys
from pyspark import SparkContext
import collections
from itertools import combinations
import itertools
import networkx as nx
from networkx import edge_betweenness_centrality as betweenness 
from networkx.algorithms.community.centrality import girvan_newman
import time






sc = SparkContext("local[*]",appName="inf553")
sc.setLogLevel("ERROR")



filename=sys.argv[1]
MaxCom=4
rdd = sc.textFile(filename) 
rdd = rdd.mapPartitions(lambda x: csv.reader(x))
header = rdd.first() #extract header
data = rdd.filter(lambda row: row != header)   #filter out header

t0 = time.time()



data = data.map(lambda x:(int(x[0]),int(x[1])))
data=data.groupByKey().map(lambda x: (x[0],list(x[1]))).sortBy(lambda x: x[0])
datas=data.collect()





nodes=[]
for i,j in datas:
    for k,l in datas:
        if i!=k:
            if len(set(j).intersection(l))>8:
                nodes.append((i,k))


# In[224]:


G = nx.Graph()
G.add_edges_from(nodes)



originalGraph=G.copy()


degree=dict(originalGraph.degree())
Kij=dict()
for i in list(combinations(degree.iterkeys(),2)):
    Kij[(i[0],i[1])]=degree[i[0]]*degree[i[1]]

def most_central_edge(G):
    centrality = betweenness(G, weight='weight')
    return max(centrality, key=centrality.get)




comp = girvan_newman(G)#, most_valuable_edge=most_central_edge)
limited = itertools.takewhile(lambda c: len(c) <= MaxCom, comp)


for i in limited:
	Answer=i

#Answer=list(limited)[:-1]

#print(len(Answer))  

t1 = time.time()

total = t1-t0
print total




finans=map(lambda x:list(x),Answer)
finans.sort(key=lambda x: x[0])
with open('Tanay_Shankar_Community_Library.txt', 'wb') as f: 
    for i in finans:
        f.write(str(i))
        f.write('\n')
f.close()


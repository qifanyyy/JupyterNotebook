from pyspark import SparkContext
from random import randint
import itertools
import collections
import sys
import csv
import math
import time

inputfile = sys.argv[1]

sc = SparkContext('local[10]','task1')

t = time.time()

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


edgebetweenness = nx.algorithms.centrality.edge_betweenness_centrality(G, k=None, normalized=False, weight=None, seed=None)

ordereddict2 = collections.OrderedDict(sorted(edgebetweenness.items()))

outputfile2 = open("Snehal_Shirgure_Betweenness.txt","w+")

for key,value in ordereddict2.iteritems():
    outputfile2.write("("+str(key[0])+","+str(key[1])+","+str(value)+")")
    outputfile2.write("\n")
outputfile2.close()


print "Time--"
print time.time()-t




# d ={}

# d[('A','B')]=0
# d[('C','B')]=0
# d[('D','B')]=0
# d[('D','E')]=0
# d[('D','G')]=0
# d[('E','F')]=0
# d[('F','G')]=0
# d[('H','G')]=0
# d[('I','G')]=0
# d[('H','I')]=0
# d[('E','H')]=0

# G.add_edge('A','B')
# G.add_edge('C','B')
# G.add_edge('D','B')
# G.add_edge('D','G')
# G.add_edge('F','G')
# G.add_edge('E','D')
# G.add_edge('E','F')
# G.add_edge('E','H')
# G.add_edge('H','I')
# G.add_edge('I','G')
# G.add_edge('H','G')

# nodes = G.nodes

# for start in nodes:

#     # print "START--"
#     # print start 

#     parents = {}
#     labels = {}
#     credit ={}


#     for n in nodes:
#         labels[n]=0

#     def bfs_connected_component(graph, start):
   
#         explored = {}
#         result= []
    
#         queue = collections.deque()
#         queue.append(start)
#         labels[start] = 1.0

#         while queue:
            
#             node = queue.popleft()
#             if node not in explored:
                
#                 explored[node]=1
#                 result.append(node)
#                 neighbours = graph[node]
#                 credit[node] = 1.0
                
#                 for neighbour in neighbours:
#                     queue.append(neighbour)
                    
#                     if neighbour not in explored:
        
#                         if neighbour not in parents:
#                             parents[neighbour]=[node]
#                         else:
#                             parents[neighbour]+=[node]

#                         if(node==start):
#                             labels[neighbour]=1.0
#                         else:
#                             labels[neighbour]+=labels[node]

#         return result

    

#     bfs =  bfs_connected_component(G,start)
    
#     print bfs
#     print "parents----"
#     print parents
#     print labels

#     for i in range(len(bfs)-1,0,-1):
#         # print i
#         currnode = bfs[i]
        
#         parent = parents[currnode]
        
        
#         for each in parent:
            
#             weight = credit[currnode]*(labels[each]/labels[currnode])
#             credit[each] += weight

#             print currnode
#             print each
#             print weight

#             if (currnode,each) in d:
#                 d[(currnode,each)]+=weight
    
#             if (each,currnode) in d:
#                 d[(each,currnode)]+=weight

#     del parents
#     del labels
#     del credit
 
# # print d

# # d2 = {}
# # for pair in d:
# #     d2[(int(pair[0]),int(pair[1]))] = d[pair]


# ordereddict = collections.OrderedDict(sorted(d.items()))

# outputfile = open("Snehal_Shirgure_Betweenness-mycode.txt","w+")

# for key,value in ordereddict.iteritems():
#     outputfile.write(str(key[0])+", "+str(key[1])+", "+str(value/2))
#     outputfile.write("\n")
# outputfile.close()










# def all_paths(graph, start, goal):
#     queue = [(start, [start])]
    
#     result =[]

#     while queue:
#         (v, path) = queue.pop(0)
            
#         graphlist = set(graph[v].keys()) - set(path)

#         for next in graphlist:
#             if next == goal:
#                 result += [path + [next]]
#             else:
#                 queue.append((next, path + [next])) 
                
#     return result


# def removebiglist(allpathlist,minlen):
#     list1 =[]

#     for each in allpathlist:
#         if(len(each)==minlen):
#             list1+=[each]
    
#     return list1



# for start in nodes:

#     for nextnode in nodes:
#         if nextnode!=start:
            
#             allpathlist = all_paths(G, start, nextnode)
#             # print allpathlist

#             minlen = len(min(allpathlist,key=len))
#             # print minlen

#             finallist = removebiglist(allpathlist,minlen)
#             # print finallist

#             weight = 1/float(len(finallist))
#             # print weight

#             for each in finallist:
#                 for i in range(len(each)-1):
#                     pair = (each[i],each[i+1])
#                     if pair in d:
#                         d[pair]+=weight
#                     else:
#                         pair = (each[i+1],each[i])
#                         if pair in d:
#                             d[pair]+=weight   

# # print d

# ordereddict1 = collections.OrderedDict(sorted(d.items()))

# outputfile = open("Snehal_Shirgure_Betweenness-mycode.txt","w+")

# for key,value in ordereddict1.iteritems():
#     outputfile.write(str(key[0])+", "+str(key[1])+", "+str(value))
#     outputfile.write("\n")
# outputfile.close()





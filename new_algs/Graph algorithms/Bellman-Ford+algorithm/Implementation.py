
# coding: utf-8

# In[37]:

#Representation of Example Graphs
'''
The three graphs are represented using 3 dictionaries
from lightly to highly coupled. The second one is
illustrated in the other attached sheet.
'''
graph1 = {
    'a': {'b': -1, 'c': 4},
    'b': {'c': 3, 'd': 2, 'e': 2},
    'c': {},
    'd': {'b': 1, 'c': 5},
    'e': {'d': -3}
         }
graph2 = {
    'A': {'B': 5, 'D': 10},
    'B': {'A': 5, 'D': 6, 'C': 2},
    'D': {'A': 10,'B': 6,'C':2, 'E': 5 },
    'C': {'B': 2, 'E': 4, 'F': 8,'D':2},
    'E': {'D': 5, 'C': 4, 'F': 3},
    'F': {'E': 3, 'C': 8}
        }
graph3= {
    'B': {'A': 5, 'D': 1, 'G': 2},
    'A': {'B': 5, 'D': 3, 'E': 12, 'F' :5},
    'D': {'B': 1, 'G': 1, 'E': 1, 'A': 3},
    'G': {'B': 2, 'D': 1, 'C': 2},
    'C': {'G': 2, 'E': 1, 'F': 16},
    'E': {'A': 12, 'D': 1, 'C': 1, 'F': 2},
    'F': {'A': 5, 'E': 2, 'C': 16}
    }


# In[55]:

#Implementation of Bellman Ford
import pdb
import time
"""
PREPARED BY:SUKANTI NAYAK
The Bellman-Ford algorithm
Graph API:
iter(graph) gives all nodes
iter(graph[u]) gives neighbours of u
graph[u][v] gives weight of edge (u, v)
"""
#Find time to run the code
start_time = time.time()
# Step 1: For each node prepare the destination and predecessor
def initialize(graph, source):
    d = {} # Stands for destination
    p = {} # Stands for next hop
    for node in graph:
        d[node] = float('Inf') # initialisation to infinity
        p[node] = None
    d[source] = 0 # For the source we know how to reach
    return d, p
#Step 2:Run the Bellman-Ford algorithm
def bellman_ford(graph, source):
    countloop=0
    d, p = initialize(graph, source)
    for i in range(len(graph)-1): #Run this until is converges
        for u in graph:
            for v in graph[u]: #For each neighbour of u
                if d[v] > d[u] + graph[u][v]:
                # Record this lower distance
                    d[v] = d[u] + graph[u][v]
                    p[v] = u
                countloop=countloop+1
    # Step 3: check for negative-weight cycles
    for u in graph:
        for v in graph[u]:
            assert d[v] <= d[u] + graph[u][v]
    return d,p,countloop


# In[56]:

"""
PREPARED BY:SUKANTI NAYAK
The DIJKSTRA algorithm
Graph topology and cost is stored in a dictionary
"""
#Find time to run the code
import time
start_time = time.time()
def dijkstra(graph,source):
    #Find all nodes as dictinary keys
    nodes=graph.keys();
    #let unvisted is a dictionary that sores unvisited nodes and cost from source
    unvisited = {node: float("inf") for node in nodes}
    #Let visited is a dictionary contains the visted nodes
    visited = {}
    current =source
    currentCost = 0
    unvisited[current] = currentCost
    #To find the next hop, p is used
    p = {} # Stands for next hop
    for node in graph:
        p[node] = None
    countloop=0
    #continue the loop until unvisited is empty
    while True:
        #Find the neighbours and cost from current nodes
        for neighbour, cost in graph[current].items():
            countloop=countloop+1
            if neighbour not in unvisited: continue
            #Find the new cost
            newCost = currentCost + cost
            #Update cost if current cost> newcost
            if unvisited[neighbour] > newCost:
                unvisited[neighbour] = newCost
                p[neighbour]=current
        visited[current] = currentCost
        #delete the current node from unvisited list
        del unvisited[current]
        if not unvisited: break
        #sort the unvisited list to find the node with min cost
        candidates = [node for node in unvisited.items() if node[1]]
        current, currentCost = sorted(candidates, key = lambda x: x[1])[0]
    return (visited,p,countloop)


# In[57]:

#widest shortest implementation of bellman ford
import pdb
import time
"""
PREPARED BY:SUKANTI NAYAK
The Widest Shortest implemetation of Bellman-Ford algorithm
"""
#Find time to run the code
start_time = time.time()
# Step 1: For each node prepare the destination and predecessor
def initialize2(graph, source):
    d = {} # Stands for destination
    p = {} # Stands for next hop
    for node in graph:
        d[node] = float("-infinity") # initialisation to MINUS infinity
        p[node] = None
    d[source] = float("infinity") # For the source we know how to reach
    return d, p
#Step 2:Run the Bellman-Ford algorithm
def widestbellman_ford(graph, source):
    countloop=0
    d, p = initialize2(graph, source)
    for i in range(len(graph)-1): #Run this until is converges
        for u in graph:
            for v in graph[u]: #For each neighbour of u
                if d[v] < min( d[u], graph[u][v]):
                    # Record this lower distance
                    d[v] = min( d[u], graph[u][v])
                    p[v] = u
                countloop=countloop+1
    return d, p,countloop


# In[58]:

#Widest shrtest implementation of DIjkstra
"""
PREPARED BY:SUKANTI NAYAK
The widest shortest DIJKSTRA algorithm
Graph topology and cost is stored in a dictionary
"""
#Find time to run the code
import time
start_time = time.time()
def widestdijkstra(graph,source):
    #Find all nodes as dictinary keys
    nodes=graph.keys();
    #let unvisted is a dictionary that sores unvisited nodes and cost from source
    unvisited = {node: float("-infinity") for node in nodes}
    #Let visited is a dictionary contains the visted nodes
    visited = {}
    current =source
    currentCost = float("infinity")
    unvisited[current] = currentCost
    #To find the next hop p is used
    p = {} # Stands for next hop
    for node in graph:
        p[node] = None
    countloop=0
    #continue the loop until unvisited is empty
    while True:
        #Find the neighbours and cost from current nodes
        for neighbour, cost in graph[current].items():
            countloop=countloop+1
            if neighbour not in unvisited: continue
            #Find the new cost
            newCost = min(currentCost,cost)
            #Update cost if current cost< newcost
            if unvisited[neighbour] < newCost:
                unvisited[neighbour] = newCost
                p[neighbour]=current
        visited[current] = currentCost
        #delete the current node from unvisited list
        del unvisited[current]
        if not unvisited: break
        #sort the unvisited list to find the node with min cost
        candidates = [node for node in unvisited.items() if node[1]]
        current, currentCost = sorted(candidates, key = lambda x: x[1])[0]
    return (visited,p,countloop)


# In[71]:

#MAIN MODULE
#Call the bellman_ford function with source node as A for graph 2
d, p,countloop = bellman_ford(graph2, 'A')
#print the cost and next hop
print("_________________________________________________________")
print("!!!!!!!!!!!! ROUTING TABLE AT SOURCE NODE A !!!!!!!!!!!!!")
print("_________________________________________________________")
print("[ D   C   N ]")
print("------------")
for i,j,k in zip(d.keys(),d.values(),p.values()):
    print(i,j,k)
print("( BELLMAN FORD:Time to run = %s seconds)" % (time.time() - start_time))
print("BELLMAN FORD:No of loop iterations:= ",countloop)
print("_________________________________________________________")
#Call the Widest bellman_ford function with source node as A for graph 2
d,p,countloop=widestbellman_ford(graph2, 'A')
d['A']=0
#print the cost and next hop
print("[ D   C   N ]")
print("------------")
for i,j,k in zip(d.keys(),d.values(),p.values()):
    print(i,j,k)
print("( W-BELLMAN FORD:Time to run = %s seconds) " % (time.time() - start_time))
print("W-BELLMAN FORD:No of loop iterations:= ",countloop)
print("_________________________________________________________")
#Call the DIJKSTRA function with source node as A for graph2
d,p,countloop=dijkstra(graph2, 'A')
#print the cost and next hop
print("[ D   C   N ]")
print("------------")
for i,j,k in zip(d.keys(),d.values(),p.values()):
    print(i,j,k)
print("( DIJKSTRA:Time to run = %s seconds) " % (time.time() - start_time))
print("DIJKSTRA:No of loop iterations:= ",countloop)
print("_________________________________________________________")
#Call the WIDEST DIJKSTRA function with source node as A for graph2
d,p,countloop=widestdijkstra(graph2, 'A')
d['A']=0
#print the cost and next hop
print("[ D   C   N ]")
print("------------")
for i,j,k in zip(d.keys(),d.values(),p.values()):
    print(i,j,k)
print("( W-DIJKSTRA:Time to run = %s seconds)" % (time.time() - start_time))
print("W-DIJKSTRA:No of loop iterations:= ",countloop)
print("_________________________________________________________")


# In[66]:

#run with different graphs
LOOP1=[]
print("____________________________________________________________")
print("---Bellman ford performace in loosly connected graph---")
d, p,countloop = bellman_ford(graph1, 'a')
#print the cost and next hop
print("[ D C N ]")
for i,j,k in zip(d.keys(),d.values(),p.values()):
    print(i,j,k)
print("No of loop iterations:= ",countloop)
LOOP1.append(countloop)
print("____________________________________________________________")
print("---Bellman ford performace in medium connected graph---")
d, p,countloop = bellman_ford(graph2, 'A')
#print the cost and next hop
print("[ D C N ]")
for i,j,k in zip(d.keys(),d.values(),p.values()):
    print(i,j,k)
print("No of loop iterations:= ",countloop)
LOOP1.append(countloop)
print("____________________________________________________________")
print("---Bellman ford performace in tightly connected graph---")
d, p,countloop = bellman_ford(graph3, 'A')
#print the cost and next hop
print("[ D C N ]")
for i,j,k in zip(d.keys(),d.values(),p.values()):
    print(i,j,k)
print("No of loop iterations:= ",countloop)
LOOP1.append(countloop)
LOOP2=[]
print("____________________________________________________________")
print ("---Dijkstra performace in loosly connected graph:---")
print("[ D C N ]")
d,p,countloop=dijkstra(graph1, 'a')
for i,j,k in zip(d.keys(),d.values(),p.values()):
    print(i,j,k)
print("No of loop iterations:= ",countloop)
LOOP2.append(countloop)
print("____________________________________________________________")
print ("---Dijkstra performace in medium connected graph:---")
d, p,countloop = bellman_ford(graph2, 'A')
print("[ D C N ]")
d,p,countloop=dijkstra(graph2,'A')
for i,j,k in zip(d.keys(),d.values(),p.values()):
    print(i,j,k)
print("No of loop iterations:= ",countloop)
LOOP2.append(countloop)
#print the cost and next hop
print("____________________________________________________________")
print ("---Dijkstra performace in tightly connected graph:---")
d, p,countloop = bellman_ford(graph3, 'A')
print("[ D C N ]")
d,p,countloop=dijkstra(graph3,'A')
for i,j,k in zip(d.keys(),d.values(),p.values()):
    print(i,j,k)
print("No of loop iterations:= ",countloop)
LOOP2.append(countloop)
print("____________________________________________________________________")
print ("No of Loops by Bellman-Ford and Dijkstra for respective graphs are")
print ("Bellman Ford :",LOOP1)
print ("Dijkstra     :",LOOP2)
print("____________________________________________________________________")


# In[63]:

#PLOT THE GRAPH TO COMPARE THE PERFORMANCE
import numpy as np
import matplotlib.pyplot as plt
N = 3
ind = np.arange(N) # the x locations for the groups
width = 0.27 # the width of the bars
fig = plt.figure()
ax = fig.add_subplot(111)
yvals = [4, 9, 2]
rects1 = ax.bar(ind, LOOP1, width, color='r',label='Bellman Ford')
zvals = [1,2,3]
rects2 = ax.bar(ind+width, LOOP2, width, color='g',label='Dijkstra')
plt.title("Performance Comparision of Bellmanford VS Dijkstra")
ax.set_ylabel('No of Loops')
ax.set_xlabel('(No of nodes-No oflinks)')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('5-8', '6-18', '7-24') )
ax.legend(loc='upper left')
def autolabel(rects):
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*h, '%d'%int(h),                ha='center', va='bottom')
autolabel(rects1)
autolabel(rects2)
plt.show()


# It can be noticed that with increase in node size and edges, the bell man is performing worse than Dijkstra with increase in node and links.

# In[62]:

#Dijkstra vs BellmanFord Complexity comparision
import random
import math
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')
"""
PREPARED BY:SUKANTI NAYAK
The comparision of Complexity of BF and Dijkstra
"""
n=random.sample(range(100), 30)
# N=no of nodes in sorted order
N=sorted(n)
#No of links=No of nodes
L=N
B=[];D=[]
#Calculate complexity
for l,n in zip(L,N):
    B.append(l*n);
    D.append(l+n*(math.log( n )) )
plt.plot(N,B,'r*--',label="Bellman")
plt.plot(N,D,'b*--',label="Dijkstra")
plt.title("Complexity curve of Bellmanford VS Dijkstra")
plt.xlabel("No of nodes=No of Links")
plt.ylabel("Big O complexity")
plt.legend(loc="upper left")
plt.show()


# In[ ]:




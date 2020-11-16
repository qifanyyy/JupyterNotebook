# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 02:02:49 2017

@author: swarnalathaa
"""

import pandas as pd




xl = pd.read_excel("file_name.xlsx","sheet1")

node1 = xl['Node1'].values.tolist()
node2 = xl['Node2'].values.tolist()
weight = xl['Weights'].values.tolist()

xl1 = pd.read_excel("file_name.xlsx","sheet2")
names = xl1['Name'].values.tolist()

# creating adjacency matrix to be used in shortest distance calculation
if max(node1)>max(node2):
    v = max(node1)+1
else:
    v = max(node2)+1


Matrix1 = [[0 for x in range(v)] for y in range(v)] 
    
for i in range(0,len(node1)-1):
    r = node1[i]
    c = node2[i]
    Matrix1[r][c] = weight[i]


# creatinf adjacency matrix for the quickest path calculation
Matrix2 = [[0 for x in range(v)] for y in range(v)] 
    
for i in range(0,len(node1)-1):
    r = node1[i]
    c = node2[i]
    Matrix2[r][c] = 1
    


# minimum distance function to be used in Djikstra algorithm
def min_distance(dist,q):
    min_val = float("Inf")
    min_index = -1
    
    for i in range(len(dist)):
        if dist[i] < min_val and i in q:
            min_val = dist[i]
            min_index = i
    return min_index

# function to print the path
def printPath(parent, j,names):
        if parent[j] == -1:
            print(names[j],)
            return
        printPath(parent,parent[j],names)
        print(names[j],)
 
def printSolution(src,dest,dist, parent,names):
        #src = 0
        #print("Vertex: %d --> %d" %(src,dest))
        #print("\n%d --> %d \t\t%d \t\t\t\t\t" % (src, dest, dist[dest])),
        print("Distance: %d" % dist[dest])
        print("path")
        printPath(parent,dest,names)  

# Dijkstra algorithm to calculate shortest and quickest path
def Dijkstra (graph,src,dest,names):
    r = len(graph)
    c = len(graph[0])
    
    dist = [float("Inf")]*r
    
    parents = [-1]*r
    
    dist[src] = 0
    q = []
    
    for i in range(0,r):
        q.append(i)
    
    while q:
        
        u = min_distance(dist,q)
        q.remove(u)
        
        for j in range(c):
            if graph[u][j] and j in q:
                if dist[u] +graph[u][j] < dist[j]:
                    dist[j] = dist[u] + graph[u][j]
                    parents[j] = u
                    
    printSolution(src,dest,dist,parents,names)
 
 
print("call funtion short_distance() to find the shortest and quickest distance between two stations")
# function to be called to find the shortest and quickest distance between the path       
def short_distance():
    src_name = input("Enter the source name:")
    dest_name = input("Enter the destination name:")
    
    src_index = names.index(src_name)
    dest_index = names.index(dest_name)
    print("shortest path between the station is : ")
    Dijkstra(Matrix1,src_index,dest_index,names)
    
    print("quickest path between the station is :")
    Dijkstra(Matrix2,src_index,dest_index,names)

 
    
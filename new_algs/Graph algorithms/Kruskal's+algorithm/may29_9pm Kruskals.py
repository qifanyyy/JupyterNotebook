# -*- coding: utf-8 -*-
"""
Created on Tue May 29 20:43:27 2018


#Learned from GeeksforGeeks
# Python program for Kruskal's algorithm to find
# Minimum Spanning Tree of a given connected, 
# undirected and weighted graph
 
from collections import defaultdict
 
#Class to represent a graph
class Graph:
 
    def __init__(self,graph_dic = {}):  
        self.graph_dic = graph_dic # default dictionary to store graph
        
    def vertices (self):
        vertices = []
        for u in self.graph_dic:
            if u not in vertices:
                vertices.append(u)
            for v in self.graph_dic[u]:
                if v not in vertices:
                    vertices.append(v)
        print ('vertices_', vertices)
          # gives number of vertices 
        return vertices   
               
   
    def generate_edges_weight_list(self):
        graph = []
        for u in self.graph_dic:
            for v in self.graph_dic[u]:
                for t in range(self.graph_dic[u][v]):
                    w = self.graph_dic[u][v]
                    edge_weight = [u,v,w]
                    if [u, v, w ] not in graph:
                        graph.append(edge_weight)
        print ('graph_', graph)
                    
        return graph    
 
    # A utility function to find set of an element i
    # (uses path compression technique)
    def find(self, parent, vertex):
        if parent[vertex] != vertex:
            parent[vertex] = self.find(parent, parent[vertex])
        return parent[vertex]
 
    # A function that does union of two sets of x and y
    # (uses union by rank)
    def union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        print ('xroot', xroot)
        yroot = self.find(parent, y)
        print ('yroot', yroot)
 
        # Attach smaller rank tree under root of 
        # high rank tree (Union by Rank)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
 
        # If ranks are same, then make one as root 
        # and increment its rank by one
        else :
            parent[yroot] = xroot
            rank[xroot] += 1
            print('parent[yroot]', parent[yroot])
            print('rank[xroot]', rank[xroot])
            
        
 
    # The main function to construct MST using Kruskal's 
        # algorithm
    def KruskalMST(self):
 
        result =[] #This will store the resultant MST
 
        i = 0 # An index variable, used for sorted edges
        e = 0 # An index variable, used for result[]
 
            # Step 1:  Sort all the edges in non-decreasing 
                # order of their
                # weight. 
        
        graph_ = self.generate_edges_weight_list()
        graph_ =  sorted(graph_,key=lambda item: item[2])
        print ('sorted graph in the increasing order of weight', graph_)
 
        parent = {} ; rank = {}
        
        vertices = self.vertices()
        print ('vertices', vertices)
        V = len(vertices)
        print('V', V)
 
        # Create V subsets with single elements
        for vertex in vertices:
            parent[vertex] = vertex
            rank[vertex] = vertex
        print ('parent', parent)
     
        # Number of edges to be taken is equal to V-1
        while e < V -1 :
 
            # Step 2: Pick the smallest edge and increment 
                    # the index for next iteration
            u,v,w =  graph_[i]
            i = i + 1
            x = self.find(parent, u)
            print ('parent_x', x)
            print('node u', u)
            y = self.find(parent ,v)
            print ('parent_y', y)
            print('node v', v)
 
            # If including this edge does't cause cycle, 
                        # include it in result and increment the index
                        # of result for next edge
            if x != y:
                e = e + 1    
                result.append([u,v,w])
                self.union(parent, rank, x, y)            
            # Else discard the edge
        print ('result', result)
        outdict = defaultdict(dict)
        for u, v, w in result:
            outdict[u][v] = w
        print('outdict',  outdict)
        # print the contents of result[] to display the built MST
        print ("Following are the edges in the constructed MST")
        for u,v,weight  in result:
            #print str(u) + " -- " + str(v) + " == " + str(weight)
            print ("%s -- %s == %d" % (u,v,weight))
 
# Driver code
g = Graph({0: {1: 10, 2: 6, 3: 5}, 1: {3: 15}, 2: {3: 4}})
g.KruskalMST()

m = Graph({'A': {'B': 10, 'C': 6, 'D': 5}, 'B': {'D': 15}, 'C': {'D': 4}})
m.KruskalMST()

 

#This code is made by help from GeeksforGeeks code by Neelam Yadav

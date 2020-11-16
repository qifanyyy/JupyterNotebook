# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 08:17:28 2017

@author: sachin
"""
class DisjointSet(dict):
    ## used to add the vertices
    def add(self, item):
        self[item] = item
    ##find is used to check if two ends of edges are same or not
    def find(self, item):
        parent = self[item]
        while self[parent] != parent:
            parent = self[parent]
        self[item] = parent
        return parent
    ##Unin is used to merge two two separate components
    def union(self, item1, item2):
        self[item2] = self[item1]

##function which will generates the Minimal Spanning Tree
def kruskal( nodes, sorted_edge ):
    forest = DisjointSet()
    mst = []
    for n in nodes:
        forest.add( n )
    no_edges = len(nodes) - 1 ##contains number of edges which is 1 less then the number of vertices
    ##Loop until all edges
    for edge in sorted_edge:
        src, dest, _ = edge
        t1 = forest.find(src)
        t2 = forest.find(dest)
        ##if T1 and T2 are from 2 different componets the add the edge
        if t1 != t2:
            mst.append(edge)
            no_edges -= 1
            if no_edges == 0:
                return mst
            forest.union(t1, t2)

##Kruskal function and Disjoint Class---> 
##referenced from:https: //programmingpraxis.com/2010/04/06/minimum-spanning-tree-kruskals-algorithm/
## and modified little
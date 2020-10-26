#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 11:50:38 2018

@author: brian
"""

def cost(G, e):
    return G.edge_dict()[e]



def initialize_tree(starting_vertex):
    return ({starting_vertex}, [])



def incidentEdges(G, T):
    temp_edges = []
    for e in G.edge_set():
        for v in T[0]:
            if e not in T[1] and v in e:
                temp_edges.append(e)
    return temp_edges

    

def valid_incidentEdges(G, T):
    temp_edges = []
    for e in incidentEdges(G, T):
        if e[0] not in T[0] or e[1] not in T[0]:
            temp_edges.append(e)
    return temp_edges



def findMinEdge(G, T):
    E = valid_incidentEdges(G, T)
    minimum = E[0]
    for e in E:
        if cost(G,e) < cost(G, minimum):
            minimum = e
    return minimum


def update_tree(G, T):
    e = findMinEdge(G,T)
    T[1].append(e)
    T[0].add(e[0])
    T[0].add(e[1])

    path(e[0], e, e[1])

paths = []
def path(v1, e, v2):
    paths.append(v1)
    paths.append(e)
    paths.append(v2)
    
def printPath():
    print('Path', paths)
 
    


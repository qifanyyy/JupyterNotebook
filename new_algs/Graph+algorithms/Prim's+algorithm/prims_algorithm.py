#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 13:36:53 2018

@author: brian
"""

from prims_functions import cost, update_tree, initialize_tree, printPath
from Weighted_Graph import *

def Prims(textfile, starting_vertex = 0, show_cost = False, show_path = False, show = False):
    G = Weighted_Graph(textfile)
    T = initialize_tree(starting_vertex)
    
    if show == True:
        G.draw_graph()
        #G.draw_subgraph(T)
    
    while T[0] != G.vertex_set():
        update_tree(G, T)
        if show == True:
            G.draw_subgraph(T)
    
    if show_path == True:
        printPath()    
        
    if show_cost == True:
        c = 0
        for e in T[1]:
            c += cost(G, e)
        print('Optimal tree cost:', c)
        
    return T

#Prims('graph4.txt', starting_vertex = 0, show_cost = True, show_path = True, show = True)
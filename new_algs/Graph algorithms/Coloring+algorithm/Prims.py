import networkx as nx
import math
"""
Finds minimum spanning tree of graph using Prim's Algorithm.
Arguments: G - reference to networkx graph
Return: minimumSpanningTreeEdges - list of edges of MST
Note: G 
        - can't have self loops
"""
def primsAlgorithm(G):
    # create mstNodes and mstEdges that keeps track of nodes and edges included in minimum spanning tree
    mstNodes = list()
    mstEdges = list()
    # create unvisited dictionary
    unvisited = {}
    # assign infinity to all nodes except one
    for i, n in enumerate(G.nodes()):
        if i == 0:
            unvisited[n] = 0
        else:
            unvisited[n] = math.inf

    # while mst doesn't include all nodes
    while len(unvisited) != 0:
        # pick node u with minimum value that is not in mstNodes yet
        minValue = math.inf
        for node in unvisited:
            if unvisited[node] < minValue and node not in mstNodes:
                nodeU = node

        # include node u to mst
        mstNodes.append(nodeU)
        # update key value of all adjacent nodes of node u
        # go through adjacent nodes
        for neighbor in G.neighbors(nodeU):
            # if weight of edge u-v is less than previous key
            if G.edges[nodeU, neighbor]['weight'] < unvisited[neighbor]:
                # update key value to weight of u-v
                unvisited[neighbor] = G.edges[nodeU, neighbor]['weight']
    return mstEdges


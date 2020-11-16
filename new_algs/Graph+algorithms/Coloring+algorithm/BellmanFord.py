import networkx as nx
import math
"""
Computes DISTANCE AND PATH from startNode to the every other node in graph using Dijkstras Algorithm.
Arguments: G - reference to networkx graph, startNode - node from which search starts
Return: visited - dictionary of all nodes and their distance from startNode 
        path - dictionary of visited nodes and path to the from startNode
        
Time complexity: O(v * e)

Note: G 
        - can have negative edges' weights
"""
def bellmanFordAlgorithm(G, startNode):
    distance = {}
    path = {}

    # initialize distance from all nodes as infinity, empty path
    for n in G.nodes():
        # distance from startNode to startNode is 0, path is "StartNode"
        if n == startNode:
            distance[startNode] = 0
            path[startNode] = [startNode]
            continue
        distance[n] = math.inf
        path[n] = []

    # relax all edges (n - 1) times because simple shortest path can visit max (n - 1) node
    for i in range(0, len(G.nodes()) - 1):
        # for every edge
        for e in G.edges():
            # find out source and target nodes of edge
            sourceNode, targetNode = e
            # if current distance of target node is greater than distance of source node + weight of edge
            if distance[targetNode] > distance[sourceNode] + G[sourceNode, targetNode]['weight']:
                # update distance of target node
                distance[targetNode] = distance[sourceNode] + G[sourceNode, targetNode]['weight']
                path[targetNode] = path[sourceNode].extend(targetNode)

    # find out if there is negative weight cycle in graph
    # - if we iterate through all edges and get shorter distance -> there is negative cycle in the graph
    for e in G.edges():
        # find out source and target nodes of edge
        sourceNode, targetNode = e
        if distance[targetNode] > distance[sourceNode] + G[sourceNode, targetNode]['weight']:
            # set distance to infinity and delete target node from path
            distance[targetNode] = math.inf
            del path[targetNode]

    return (distance, path)

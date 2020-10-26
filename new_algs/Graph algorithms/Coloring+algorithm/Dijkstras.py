import networkx as nx
import math

"""
Computes DISTANCE AND PATH from startNode to the every other node in graph using Dijkstras Algorithm.

Arguments: G - reference to networkx graph, startNode - node from which search starts
Return: visited - dictionary of all nodes and their distance from startNode 
        path - dictionary of visited nodes and path to the from startNode
        
Time complexity: Depends on the implementation (data structure used)
                        - With Adjacency List and Priority Queue: O((v + e) log v)
                        - With matrix and Priority Queue: O(v^2 + e log v)
                        - With Fibonacci Heap and Adjacency List: O(e + v log v)

Note: G must be
        - weighted (weights must be positive)
      If G has more components
        - unreachable components won't appear in path dictionary
        - values of unreachable components in visited dictionary is infinity
"""
def dijkstrasAlgorithm(G, startNode):
    # initialize dictionaries
    visited = {startNode : 0}
    distance = {}
    path = dict()
    path[startNode] = [startNode]

    # assign "infinity" values to all nodes, except startNode
    for node in G.nodes():
        if node == startNode:
            continue
        distance[node] = math.inf

    # select first node
    node = startNode
    # repeat while every node hasn't been visited
    while True:
        # update values of node’s neighbors
        for neighbor in G.neighbors(node):
            # check if neighbor has not been visited
            nodeVisited = True
            for n in distance:
                if n == neighbor:
                    nodeVisited = False
                    break
            if nodeVisited == True:
                continue
            # compute new distance
            newDistance = visited[node] + G.edges[node, neighbor]['weight']
            if newDistance < distance[neighbor]:
                distance[neighbor] = newDistance
                # compute new path
                newPath = path[node].copy()
                newPath.append(neighbor)
                path[neighbor] = newPath

        # exit when every node has been visited
        if bool(distance) == False:
            break
        # choose new node
        smallestValue = math.inf
        for n in distance:
            if distance[n] <= smallestValue:
                smallestValue = distance[n]
                node = n
        # move node to visited
        visited.update({node : smallestValue})
        # delete node in distance
        del distance[node]

    print(visited)
    print(path)

    return (visited, path)

"""
Dijkstra's algorithm works similarly as Prim's algorithms for minimum spanning tree.
If we want to use Dijkstra's algorithm to find shortest path from A to B, we can stop when B is in visited.
If we want to use Dijkstra's algorithm to find minimum spanning tree, we have to let it find shortest path to all nodes.
The only difference is that in Prim's, we can choose our source node - when using Dijkstra's, it is given.
"""

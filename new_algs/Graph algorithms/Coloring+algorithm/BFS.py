import networkx as nx

"""
Computes DISTANCE AND PATH from startNode to the every other node in graph using Breadth First Search.

Arguments: G - reference to networkx graph, startNode - node from which search starts
Returns: distance - dictionary of all nodes and their distance from startNode
        path - dictionary of visited nodes and path to the from startNode
        
Time complexity: depends on the implementation (data structure used)
                        - Adjacency Matrix O(v^2)
                        - Adjacency List O(v + e)

Note: G 
        - can't have loops
        - is unweighted graph (when weighted graph is passed, it will process it as unweighted)
"""
def breadthFirstSearch(G, startNode):
    # initialize dictionaries and lists
    visited = []
    queue = [startNode]
    path = {}
    path[startNode] = [startNode]

    # repeat until queue is not empty
    while len(queue) != 0:
        # choose next node from queue
        node = queue[0]
        # for every neighbor of the node
        for neighbor in G.neighbors(node):
            # if neighbor not in visited
            if neighbor not in visited:
                # if neighbor is not already in queue, append it to queue
                if neighbor not in queue:
                    queue.append(neighbor)
            # if neighbor is in visited
            else:
                continue
            # update path for neighbor
            if neighbor not in path:
                newPath = path[node].copy()
                newPath.append(neighbor)
                path[neighbor] = newPath
        # add node to visited
        visited.append(node)
        # delete node from queue
        del queue[0]

    # compute shortest path to visited nodes
    distance = {}
    for n in path:
        distance[n] = len(path[n]) - 1

    # if graph has more components, set distance to unvisited nodes to 1000 (infinity)
    for n in G.nodes():
        if n not in distance:
            distance[n] = 1000

    print(distance)
    print(path)

    return (distance, path)

"""
NOTES
- used for shortest path and minimum spanning tree for unweighted graph
- real life application
    - peer to peer networks - to find neighbor nodes
    - crawlers in search engines - build website index using it
    - GPS navigation systems
    - broadcasting in network - broadcasted packet follows BFS to reach all nodes
    - garbage collection - used in copying garbage collection
- in other algorithms
    - cycle detection in undirected graph (can use both BFS and DFS)
        - in directed graph, only DFS
    - Ford-Fulkerson Algorithm
        - BFS or DSF to find max flow
        - BFS preffered as it reduces worst case time complexity O(VE^2)
    - to test if graph is bipartite
        - BFS or DSF
    - path finding
        - BFS or DSF to find if there is a path between two nodes
    - finding all nodes within one connected component
        - BFS or DSF
"""

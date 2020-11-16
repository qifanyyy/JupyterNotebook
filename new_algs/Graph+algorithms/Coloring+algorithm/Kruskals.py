import networkx
"""
Finds minimum spanning tree of graph using Kruskal's Algorithm.

Arguments: G - reference to networkx graph
Return: minimumSpanningTreeEdges - list of edges of MST
Note: G 
        - can't have self loops (because of union-find algorithm)
        - be undirected (because of union-find algorithm)
"""
def kruskalsAlgorithm(G):
    # sort all edges in non-decreasing order of their weight
    unvisitedEdges = []
    index = 0
    for e in G.edges():
        a,b = e
        for i in range(len(unvisitedEdges)):
            c,d = unvisitedEdges[i]
            if G.edges[a,b]['weight'] < G.edges[c,d]['weight']:
                index = i
                break
            index = i + 1
        unvisitedEdges.insert(index, e)

    # set up dictionary for cycle detection (node:it's parent)
    cycleDetection = {node:None for node in G.nodes}
    # set up find function for cycle detection
    def findParent(node):
        if cycleDetection[node] == None:
            return node
        else:
            return findParent(cycleDetection[node])
    #set up union function for cycle detection
    def setUnion(u, v):
        uSet = findParent(u)
        vSet = findParent(v)
        cycleDetection[uSet] = vSet

    # repeat until spanning tree has v-1 edges
    minimumSpanningTreeEdges = []
    while len(minimumSpanningTreeEdges) != len(G.nodes()) - 1 and len(unvisitedEdges) != 0:
        # pick edge with lowest weight
        edge = unvisitedEdges[0]
        u,v = edge
        # check if it forms a cycle with the spanning tree formed so far
        # if cycle is not formed, include this edge to MST
        if findParent(u) != findParent(v):
            setUnion(u, v)
            minimumSpanningTreeEdges.append(edge)
        # delete edge from unvisited
        unvisitedEdges.pop(0)

    # check if MST has (v - 1) edges -> if not clear MST
    if len(minimumSpanningTreeEdges) != len(G.nodes()) - 1:
        print("This graph doesn't have minimum spanning tree.")
        minimumSpanningTreeEdges.clear()

    print(minimumSpanningTreeEdges)
    return minimumSpanningTreeEdges
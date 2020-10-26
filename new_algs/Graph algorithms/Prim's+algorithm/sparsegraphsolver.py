# Put your solution here.

import networkx as nx
from math import ceil
import random
from heapq import heappop, heappush
from itertools import count

def solve(client):
    client.end()
    client.start()

    graph = client.G

    # Start by finding location of all bots using scout and remote.
    # Remotes likely places using edge with lowest weight
    # Does scout to all nodes first
    nodes = list(graph.nodes())
    numNodes = len(nodes)
    nodeValues = [0 for _ in nodes]
    checked = [False for _ in nodes]
    checked[nodes.index(client.h)] = True

    botsin = [0 for _ in nodes]

    all_students = list(range(1, client.students + 1))

    nodeReports = [0 for _ in nodes]
    for i in range(len(nodes)):
        if nodes[i] != client.h:
            nodeReports[i] = list(client.scout(nodes[i],all_students).values())

    totalnodes = len(nodes)
    minNumTruth = ceil(totalnodes/2)
    numStudents = client.students

    numTruth = [0 for _ in range(numStudents)]
    numLies = [0 for _ in range(numStudents)]
    worstcaseprob = [(minNumTruth - numTruth[i])/(totalnodes - numTruth[i] - numLies[i]) for i in range(numStudents)]

    botsleft = client.bots - sum(client.bot_count)

    counter = 0

    while botsleft > 0 and len(nodes) > 0:
        targetIndex = -1
        for i in range(numNodes):
            if checked[i] == False:
                score = studentjudgment(worstcaseprob, nodeReports[i])
                if type(score) == int:
                    targetIndex = i
                    print("Found for sure")
                    print(i)
                    break
                nodeValues[i] = score[0] * score[1]
                if targetIndex == -1:
                    targetIndex = i
                    maxNodeValue = nodeValues[i]
                if maxNodeValue < nodeValues[i]:
                    targetIndex = i
                    maxNodeValue = nodeValues[i]
        target = nodes[targetIndex]
        checked[targetIndex] = True
        nextEdges = list(graph.edges(target,'weight',default=0))
        #print(nextEdges)
        minEdgeIndex = 0
        minEdge = -1
        for i in range(len(nextEdges)):
            if i == 0:
                minEdge = nextEdges[i][2]
                minEdgeIndex = i
            if nextEdges[i][2] < minEdge:
                minEdge = nextEdges[i][2]
                minEdgeIndex = i
        success = client.remote(target, nextEdges[minEdgeIndex][1])
        #print(nextEdges[minEdgeIndex])
        #print(nodes.index(nextEdges[minEdgeIndex][1]))
        botsin[nodes.index(nextEdges[minEdgeIndex][1])] += success
        #targetedges = graph.edges.data('weight', default=0)
        # for i in range(targetedges):
        #     u,v,w = targetedges[i]
        #     if i == 0:
        #         imin = i
        #         wmin = w
        #         vmin = v
        #         umin = u
        #     if w < wmin:
        #         imin = i
        #         wmin = w
        #         vmin = v
        #         umin = u
        # if umin == target:
        #     client.remote(target, vmin)
        # else:
        #     client.remote(target, umin)
        if success - botsin[targetIndex] > 0:
            right = True
        else:
            right = False
        for i in range(numStudents):
            answer = nodeReports[targetIndex][i]
            if answer == right:
                numTruth[i] += 1
            else:
                numLies[i] += 1
        worstcaseprob = [(minNumTruth - numTruth[i]) / (totalnodes - numTruth[i] - numLies[i]) for i in
                         range(numStudents)]

        botsleft = client.bots - sum(client.bot_count)
        counter += 1

    print("Bots recovered in remote(s): ")
    print(counter)

    # When all the locations discovered, we do algorithm in q2. (Prim's combined with Uniform Cost Search)
    # Uses client.bot_count

    botnodes = client.bot_locations
    for node in botnodes:
        path = nx.shortest_path(graph, source=node, target=client.h)
        for i in range(len(path)-1):
            client.remote(path[i],path[i+1])

    print("Number of bots needed to be resqued:")
    print(client.l)
    print("Number of final rescued bots:")
    print(client.bot_count[client.home])

    client.end()

def studentjudgment(probs, reports):
    judge = [0, 0]
    for i in range(len(probs)):
        if probs[i] == 1:
            if reports[i] == True:
                return 1
            else:
                return (-1, 1000)
        if reports[i] == 0:
            judge[0] += (probs[i]**2)
        if reports[i] == 1:
            judge[1] += (probs[i]**2)
    if judge[0] >= judge[1]:
        return (-1, judge[0])
    else:
        return (1, judge[1])


def prim_mst_edges(G, weight='weight', data=True):
    """Generate edges in a minimum spanning forest of an undirected
    weighted graph.

    A minimum spanning tree is a subgraph of the graph (a tree)
    with the minimum sum of edge weights.  A spanning forest is a
    union of the spanning trees for each connected component of the graph.

    Parameters
    ----------
    G : NetworkX Graph

    weight : string
       Edge data key to use for weight (default 'weight').

    data : bool, optional
       If True yield the edge data along with the edge.

    Returns
    -------
    edges : iterator
       A generator that produces edges in the minimum spanning tree.
       The edges are three-tuples (u,v,w) where w is the weight.

    Examples
    --------
    >> G=nx.cycle_graph(4)
    >> G.add_edge(0,3,weight=2) # assign weight 2 to edge 0-3
    >> mst=nx.prim_mst_edges(G,data=False) # a generator of MST edges
    >> edgelist=list(mst) # make a list of the edges
    >> print(sorted(edgelist))
    [(0, 1), (1, 2), (2, 3)]

    Notes
    -----
    Uses Prim's algorithm.

    If the graph edges do not have a weight attribute a default weight of 1
    will be used.
    """

    if G.is_directed():
        raise nx.NetworkXError(
            "Mimimum spanning tree not defined for directed graphs.")

    push = heappush
    pop = heappop

    nodes = list(G.nodes())
    c = count()

    while nodes:
        u = nodes.pop(0)
        frontier = []
        visited = [u]
        for u, v in G.edges(u):
            push(frontier, (G[u][v].get(weight, 1), next(c), u, v))

        while frontier:
            W, _, u, v = pop(frontier)
            if v in visited:
                continue
            visited.append(v)
            nodes.remove(v)
            for v, w in G.edges(v):
                if not w in visited:
                    push(frontier, (G[v][w].get(weight, 1), next(c), v, w))
            if data:
                yield (u, v, G[u][v])
            else:
                yield (u, v)


def prim_mst(G, weight='weight'):
    """Return a minimum spanning tree or forest of an undirected
    weighted graph.

    A minimum spanning tree is a subgraph of the graph (a tree) with
    the minimum sum of edge weights.

    If the graph is not connected a spanning forest is constructed.  A
    spanning forest is a union of the spanning trees for each
    connected component of the graph.

    Parameters
    ----------
    G : NetworkX Graph

    weight : string
       Edge data key to use for weight (default 'weight').

    Returns
    -------
    G : NetworkX Graph
       A minimum spanning tree or forest.

    Examples
    --------
    >> G=nx.cycle_graph(4)
    >> G.add_edge(0,3,weight=2) # assign weight 2 to edge 0-3
    >> T=nx.prim_mst(G)
    >> print(sorted(T.edges(data=True)))
    [(0, 1, {}), (1, 2, {}), (2, 3, {})]

    Notes
    -----
    Uses Prim's algorithm.

    If the graph edges do not have a weight attribute a default weight of 1
    will be used.
    """
    T = nx.Graph(prim_mst_edges(G, weight=weight, data=True))
    # Add isolated nodes
    if len(T) != len(G):
        T.add_nodes_from([n for n, d in G.degree().items() if d == 0])
    # Add node and graph attributes as shallow copy
    for n in T:
        T.node[n].update(G.node[n].copy())
    T.graph = G.graph.copy()
    return T

def prim_mst_edges_sparse(G, weight='weight', data=True):
    """Generate edges in a minimum spanning forest of an undirected
    weighted graph.

    A minimum spanning tree is a subgraph of the graph (a tree)
    with the minimum sum of edge weights.  A spanning forest is a
    union of the spanning trees for each connected component of the graph.

    Parameters
    ----------
    G : NetworkX Graph

    weight : string
       Edge data key to use for weight (default 'weight').

    data : bool, optional
       If True yield the edge data along with the edge.

    Returns
    -------
    edges : iterator
       A generator that produces edges in the minimum spanning tree.
       The edges are three-tuples (u,v,w) where w is the weight.

    Examples
    --------
    >> G=nx.cycle_graph(4)
    >> G.add_edge(0,3,weight=2) # assign weight 2 to edge 0-3
    >> mst=nx.prim_mst_edges(G,data=False) # a generator of MST edges
    >> edgelist=list(mst) # make a list of the edges
    >> print(sorted(edgelist))
    [(0, 1), (1, 2), (2, 3)]

    Notes
    -----
    Uses Prim's algorithm.

    If the graph edges do not have a weight attribute a default weight of 1
    will be used.
    """

    if G.is_directed():
        raise nx.NetworkXError(
            "Mimimum spanning tree not defined for directed graphs.")

    push = heappush
    pop = heappop

    nodes = list(G.nodes())
    c = count()

    while nodes:
        u = nodes.pop(0)
        frontier = []
        visited = [u]
        for u, v in G.edges(u):
            push(frontier, (G[u][v].get(weight, 1), next(c), u, v))

        while frontier:
            W, _, u, v = pop(frontier)
            if v in visited:
                continue
            visited.append(v)
            nodes.remove(v)
            for v, w in G.edges(v):
                if not w in visited:
                    push(frontier, (G[v][w].get(weight, 1), next(c), v, w))
            if data:
                yield (u, v, G[u][v])
            else:
                yield (u, v)


def prim_mst_sparse(G, weight='weight'):
    """Return a minimum spanning tree or forest of an undirected
    weighted graph.

    A minimum spanning tree is a subgraph of the graph (a tree) with
    the minimum sum of edge weights.

    If the graph is not connected a spanning forest is constructed.  A
    spanning forest is a union of the spanning trees for each
    connected component of the graph.

    Parameters
    ----------
    G : NetworkX Graph

    weight : string
       Edge data key to use for weight (default 'weight').

    Returns
    -------
    G : NetworkX Graph
       A minimum spanning tree or forest.

    Examples
    --------
    >> G=nx.cycle_graph(4)
    >> G.add_edge(0,3,weight=2) # assign weight 2 to edge 0-3
    >> T=nx.prim_mst(G)
    >> print(sorted(T.edges(data=True)))
    [(0, 1, {}), (1, 2, {}), (2, 3, {})]

    Notes
    -----
    Uses Prim's algorithm.

    If the graph edges do not have a weight attribute a default weight of 1
    will be used.
    """
    T = nx.Graph(prim_mst_edges(G, weight=weight, data=True))
    # Add isolated nodes
    if len(T) != len(G):
        T.add_nodes_from([n for n, d in G.degree().items() if d == 0])
    # Add node and graph attributes as shallow copy
    for n in T:
        T.node[n].update(G.node[n].copy())
    T.graph = G.graph.copy()
    return T


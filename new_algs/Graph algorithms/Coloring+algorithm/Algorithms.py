"""Algorithms for graph coloring"""


import collections
from itertools import product
from random import choice


def bruteForce(graph, useHeuristics=False):
    """
    Brute force header function. Sequentially calls bruteForceKcolor() until coloring is found
    :param graph: Input graph
    :param useHeuristics: Use heuristic acceleration or not
    :return: tuple of dictionary and integer:
    found coloring: key is a vertex, value is a color
    numbers of colors used
    """
    # removeBadVertices(graph)
    n = graph.getVertexCount()
    coloring = ()
    colorCount = 0
    start = 1
    if useHeuristics:
        start = getLargestCliqueSize(graph)
    for k in range(start-1, n):
        coloring = bruteForceKcolor(graph, k)
        if coloring:
            colorCount = k
            break

    coloring = resolveSingleColoredVertices(graph, coloring, colorCount)
    return coloring, colorCount


def bruteForceWithHeuristics(graph):
    """
    Ancillary function. Calls bruteForce() with enabled useHeuristics
    :param graph: Input graph
    :return: Result of called function bruteForce()
    """
    return bruteForce(graph, useHeuristics=True)


def bruteForceKcolor(g, k):
    """
    Core of brute force algorithm. Checks every possible k-coloring of the graph g
    :param g: Input graph
    :param k: Number of colors to deal with
    :return: Dictionary, found coloring: key is a vertex, value is a color. Empty dictionary if not found
    """

    solution = {}
    indexedVertices = {v: k for k, v in dict(enumerate(g.getAdjDict())).items()}
    for coloring in product(range(k), repeat=g.getVertexCount()):
        found = True
        for v in g.getAdjDict():
            for u in g.getAdjDict()[v]:
                if coloring[indexedVertices[v]] == coloring[indexedVertices[u]]:
                    found = False
                    break
            if not found:
                break
        if found:
            # match iteratively graph vertices to colors in coloring, store in dictionary
            solution = {key: val for key, val in zip(g.getAdjDict(), coloring)}
            break
    return solution


def getLargestCliqueSize(g):
    """
    Header of the calcMaxCliqueSize() function.
    Returns size of the largest clique in the graph g
    :param g: Input graph
    :return: Size of the largest clique
    """

    # Use list to be able to modify it by function
    maxSize = [0]
    calcMaxCliqueSize([], list(g.getAdjDict()), [], g, maxSize)
    return maxSize[0]


def calcMaxCliqueSize(R, P, X, g, maxCliqueSize):
    """
    Modified Bron-Kerbosch recursive algorithm with pivoting
    for finding size of the largest clique.
    R, P and X are ancillary arrays.

    :param g: Input graph
    :param maxCliqueSize: Wrapped in list variable which will contain the result of the algorithm

    """

    if not any((P, X)):
        if len(R) > maxCliqueSize[0]:
            maxCliqueSize[0] = len(R)
    if not P:
        return

    # Choose random vertex from union of P and X as a pivot
    pivot = choice(P + X)

    for v in P[:]:
        if v not in g.getAdjDict()[pivot]:
            R_v = R + [v]
            P_v = [v1 for v1 in P if v1 in g.getAdjDict()[v]]
            X_v = [v1 for v1 in X if v1 in g.getAdjDict()[v]]
            calcMaxCliqueSize(R_v, P_v, X_v, g, maxCliqueSize)
            P.remove(v)
            X.append(v)


def WelshPowell(graph):
    """
    Implementation of the Welsh Powell algorithm
    :param graph: Input graph
    :return: tuple of dictionary and integer:
    found coloring: key is a vertex, value is a color
    numbers of colors used
    """

    removeBadVertices(graph)
    orderedVertices = list(collections.OrderedDict(sorted(graph.getAdjDict().items(),
                                                          key=lambda kv: len(kv[1]), reverse=True)).keys())

    coloring = {orderedVertices[0]: 0}
    colorsUsed = 0
    for v in orderedVertices[1:]:
        available = [True] * len(graph.getAdjDict())
        for u in graph.getAdjDict()[v]:
            if u in coloring:
                col = coloring[u]
                available[col] = False
        clr = 0
        for clr in range(len(available)):
            if available[clr]:
                if clr > colorsUsed:
                    colorsUsed = clr
                break
        coloring[v] = clr

    coloring = resolveSingleColoredVertices(graph, coloring, colorsUsed)
    return coloring, colorsUsed + 1


def removeBadVertices(graph):
    """
    Remove all vertices with degree n-1
    :param graph: Input graph
    """

    for v in list(graph.getAdjDict()):
        if len(graph.getAdjDict()[v]) == graph.getVertexCount() - 1:
            graph.removeVertex(v)


def resolveSingleColoredVertices(graph, coloring, colorsUsed):
    """
    Finds single colored vertices and tries to color them with another used color
    :param graph: Input graph
    :param coloring: Found coloring
    :param colorsUsed: Number of colors used
    :return: None if failed. Otherwise fixed coloring
    """
    inv_coloring = {}
    for i in range(colorsUsed+1):
        inv_coloring[i] = []

    for k, v in coloring.items():
        inv_coloring[v].append(k)

    singleColoredVertices = []
    for color, vertices in inv_coloring.items():
        if len(vertices) == 1:
            singleColoredVertices.append(vertices[0])

    if len(singleColoredVertices) == 0:
        return coloring

    # sort single colored vertices by valence
    singleColoredVertices.sort(key=lambda x: len(graph.getAdjDict()[x]), reverse=True)

    # find first vertex to pair with single colored
    for sv in singleColoredVertices:
        foundPair = False
        for u in graph.getAdjDict():
            if u not in graph.getAdjDict()[sv] and sv != u:
                if len(inv_coloring[coloring[u]]) > 2:
                    coloring[u] = coloring[sv]
                    foundPair = True
                    break
        if not foundPair:
            return None
    return coloring




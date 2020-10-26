# DetourMatrix.py
# Calculates the Detour Matrix for a given graph
# Returns detour matrix, and all computed paths
import networkx as nx
import itertools
import numpy as np


def assign_to_matrix(matrix, pathLen, vertices):
    for (x, y) in vertices:
        matrix[x, y] = pathLen[(x, y)]
        matrix[y, x] = pathLen[(x, y)]
        matrix[x, x] = np.nan
        matrix[y, y] = np.nan
    return matrix


def detour_matrix(g):
    def all_paths(vertex_a, vertex_b):
        return list(nx.all_simple_paths(g, source=vertex_a, target=vertex_b))

    nodes = g.nodes()
    numOfNodes = len(list(nodes))

    detourMatrix = np.zeros(numOfNodes ** 2).reshape(numOfNodes, numOfNodes)
    # flatten = lambda l: [item for sublist in l for item in sublist]
    vertexPairs = list(itertools.combinations(nodes, 2))

    lengthOfPath = lambda a: len(a) - 1
    AllPaths = {x: all_paths(x[0], x[1]) for x in vertexPairs}
    DictOfPaths = {x: map(lengthOfPath, y) for x, y in AllPaths.items()}
    maxPathLength = lambda a: max(DictOfPaths[a])
    DictOfLen = {x: maxPathLength(x) for x in vertexPairs}
    detourMatrix = assign_to_matrix(detourMatrix, DictOfLen, vertexPairs)

    return int(np.nanmin(detourMatrix)), AllPaths

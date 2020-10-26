"""
Provides Single Source Shortest Path implementation for a weighted graph
"""

from heapq import heappush, heappop
from model.graph import Graph

__author__ = "Eduardo Hernandez"
__email__ = "https://www.linkedin.com/in/eduardohernandezj/"


def single_source_shortest_paths_dijkstra(graph: Graph, source: int, cutoff=None):
    """
    Provides Single Source Shortest Path implementation for a weighted graph

    :param graph: Weighted graph implemented with adjacency list.
    Edges in the graph are in the form of (u,v,w) where u,v are long and w is float
    :param source: source node
    :param cutoff: threshold value of largest possible distance in shortest paths.
    :return: all possible shortest paths from source to every other node in the graph
    """

    adj_list = graph.adj_list

    distances = {}  # final distances

    # paths to return
    # key = destination, value: list of paths. path = list of nodes
    paths = dict.fromkeys(graph.nodes, [])
    paths[source] = [[source]]

    predecessors = dict()

    visited = dict()
    visited[source] = 0

    heap = []  # head queue with 3-tuples (distance, path_to_node, node_id)
    heappush(heap, (0, source, source))

    while heap:
        (distance, pred, v) = heappop(heap)

        if v in distances:
            continue  # node already processed

        distances[v] = distance

        for u, weight in adj_list[v].items():
            vu_distance = distances[v] + weight
            if cutoff is not None:
                if vu_distance > cutoff:
                    continue
            if u in distances:
                # from networkx:
                if vu_distance < distances[u]:
                    raise ValueError('Contradictory paths found:',
                                     'negative weights?')

            elif u not in visited or vu_distance < visited[u]:  # shorter path found
                visited[u] = vu_distance
                heappush(heap, (vu_distance, v, u))
                _update_paths(paths, u, v)
                predecessors[u] = [v]

            elif vu_distance == visited[u]:  # equal paths
                predecessors[u].append(v)
                _update_paths(paths, u, v)

    return paths, distances


def _update_paths(paths, u, v):
    paths[u] = []  # Purge shortest paths list on new path distance
    for path in paths[v]:
        paths[u] = paths[u] + [path + [u]]

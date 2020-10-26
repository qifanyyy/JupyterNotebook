"""Functions for edge betweenness centrality computation"""

from algorithms.shortest_path import single_source_shortest_paths_dijkstra
from model.graph import Graph

__author__ = "Eduardo Hernandez"
__email__ = "https://www.linkedin.com/in/eduardohernandezj/"


def get_edges_with_highest_betweenness(graph: Graph):
    betweenness_dict = edge_betweenness(graph)

    sorted_by_betweenness_desc = sorted(betweenness_dict.items(),
                                        key=lambda edge_betweenness_pair: (
                                            edge_betweenness_pair[1], edge_betweenness_pair[0]),
                                        reverse=True)

    top_betweennness = sorted_by_betweenness_desc[0][1]
    top_edges = list()

    for edge_betweenness_pair in sorted_by_betweenness_desc:
        if edge_betweenness_pair[1] != top_betweennness:
            break
        top_edges.append(edge_betweenness_pair[0])

    return top_edges


def edge_betweenness(graph: Graph):
    """
    :param graph:
    :return: dictionary of edges betweennes. key = edge, value = edge betweennes. edge = (source_node, target_node)
    { (u,v): b }
    """
    betweenness = dict.fromkeys(graph.edges, 0.0)

    for node in graph.nodes:
        _update_edge_betweenness_single_source(graph, betweenness, node)

    return betweenness


def _update_edge_betweenness_single_source(graph: Graph, betweenness, source):
    paths, _ = single_source_shortest_paths_dijkstra(graph, source=source)

    # map to number of paths
    paths_count_map = {target: len(paths_list) for (target, paths_list) in paths.items()}

    # map to edges count in each path
    edges_count_map = {target: _get_edge_count(paths_list) for (target, paths_list) in paths.items()}

    for target in edges_count_map.keys():
        edges_count = edges_count_map[target]
        paths_count = paths_count_map[target]

        for (edge, edge_count) in edges_count.items():
            edge = tuple(sorted(edge))
            betweenness[edge] += edge_count / paths_count  # sigma_st(e) / sigma_st

    return betweenness


def _get_edge_count(paths_list):
    """

    :param paths_list:
    :return: key = edge, value = count of shortest paths through that edge to this target
    """
    edge_count = dict()

    for path in paths_list:
        for i in range(len(path) - 1):
            edge = (path[i], path[i + 1])
            edge_count[edge] = edge_count.get(edge, 0) + 1.0

    return edge_count
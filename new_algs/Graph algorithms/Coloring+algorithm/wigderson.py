import logging

import algorithm
from algorithm_helper import *


# def max_ind_set_wigderson_strategy(graph, colors, L, init_params):
#     """Colors some of the nodes using Wigderson technique.
#
#         Args:
#             graph (graph): Graph to be processed.
#             colors (dict): Global vertex-color dictionary.
#             threshold_degree (int): Lower boundary for degree of processed nodes of graph.
#         """
#
#     print '\n starting Wigderson algorithm:'
#     print '     threshold deg:', threshold_degree
#     max_degree = max(dict(graph.degree()).values())
#     iterations = 0
#     while max_degree > threshold_degree:
#         iterations += 1
#         print '\n iteration', iterations
#         print ' max deg:', max_degree
#
#         # Find any vertex with degree equal to max_degree.
#         max_vertex = 0
#         for v in dict(graph.degree()):
#             if graph.degree()[v] == max_degree:
#                 max_vertex = v
#                 break
#
#         neighbors_subgraph = graph.subgraph(graph.neighbors(max_vertex))
#
#         # Find large independent set in neighbors subgraph using approximate maximum independent set algorithm.
#         # Can we find this large independent set using our algorithm recursively?
#         min_available_color = max(colors.values()) + 1
#         max_ind_set = nx.algorithms.approximation.maximum_independent_set(neighbors_subgraph)
#         # max_ind_set = nx.maximal_independent_set(neighbors_subgraph)
#         for v in max_ind_set:
#             colors[v] = min_available_color
#
#         # Remove nodes that have just been colored
#         graph.remove_nodes_from(max_ind_set)
#         max_degree = max(dict(graph.degree()).values())
#
#     return True


def recursive_wigderson_strategy(graph, colors, L, init_params, literal_init_params):
    """Colors some of the nodes using Wigderson technique.

    Args:
        graph (graph): Graph to be processed.
        colors (dict): Global vertex-color dictionary.

    Returns:
        bool: Returns true if it is not an empty function.
    """

    # TODO; Maybe try iterative version

    logging.info('Starting Wigderson technique...')

    k = find_number_of_vector_colors_from_vector_coloring(graph, L)
    n = graph.number_of_nodes()
    max_degree = max(dict(graph.degree()).values())
    threshold_degree = pow(n, (k - 1) / k)
    it = 0
    while max_degree > threshold_degree and graph.number_of_nodes() > 25:
        it += 1

        # Find any vertex with degree equal to max_degree.
        max_vertex = 0
        for v in dict(graph.degree()):
            if graph.degree()[v] == max_degree:
                max_vertex = v
                break

        neighbors_subgraph = nx.Graph()
        neighbors_subgraph.add_nodes_from(graph.neighbors(max_vertex))
        neighbors_subgraph.add_edges_from(graph.subgraph(graph.neighbors(max_vertex)).edges())
        alg = algorithm.VectorColoringAlgorithm(
            partial_color_strategy=literal_init_params['partial_color_strategy'],
            partition_strategy=literal_init_params['partition_strategy'],
            find_independent_sets_strategy=literal_init_params['find_independent_sets_strategy'],
            normal_vectors_generation_strategy=literal_init_params['normal_vectors_generation_strategy'],
            independent_set_extraction_strategy=literal_init_params['independent_set_extraction_strategy'],
            wigderson_strategy=literal_init_params['wigderson_strategy'],
            sdp_type=literal_init_params['sdp_type'],
            alg_name=literal_init_params['alg_name']
        )
        neighbors_colors = alg.color_graph(neighbors_subgraph)
        for v in neighbors_subgraph.nodes():
            colors[v] = neighbors_colors[v]

        # Remove nodes that have just been colored
        graph.remove_nodes_from(neighbors_subgraph.nodes())
        max_degree = max(dict(graph.degree()).values())

    return it > 0


def no_wigderson_strategy(graph, colors, L, init_params, literal_init_params):
    return False

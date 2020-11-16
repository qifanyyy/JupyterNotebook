# -*- coding: utf-8 -*-
"""
partial_color_strategy:
        'color_all_vertices_at_once',
        'color_by_independent_sets'

independent_set_extraction_strategy:
        'max_degree_first',
        'min_vertex_cover',
        'arora_kms',
        'arora_kms_prim'

sdp_type:
        'nonstrict',
        'strict',
        'strong'

wigderson_strategy:
        'no_wigderson',
        'recursive_wigderson'

find_independent_sets_strategy:
        'random_vector_projection',
        'clustering'

partition_strategy: (only for partial_color_strategy='color_all_vertices_at_once')
        'hyperplane_partition',
        'clustering'

normal_vectors_generation_strategy: (only for partition_strategy='hyperplane_partition')
        'random_normal',
        'orthonormal'


"""

from algorithm import *
from results_processing import *

algorithms = {}

# the number next to algorithm configuration is it's position in gui

algorithms[u'Koloruj i popraw: klasteryzacja'] = [VectorColoringAlgorithm(
    partial_color_strategy='color_all_vertices_at_once',
    partition_strategy='clustering',
    independent_set_extraction_strategy='max_degree_first',
    wigderson_strategy='no_wigderson',
    sdp_type='nonstrict',
    alg_name='clustering all vertices',
    deterministic=True
), 6]

algorithms[u'Koloruj i popraw: ortonormalne hiperpłaszczyzny'] = [VectorColoringAlgorithm(
    partial_color_strategy='color_all_vertices_at_once',
    partition_strategy='hyperplane_partition',
    normal_vectors_generation_strategy='orthonormal',
    independent_set_extraction_strategy='max_degree_first',
    wigderson_strategy='no_wigderson',
    sdp_type='nonstrict',
    alg_name='orthonormal hyperplane partition',
    deterministic=False
), 4]

algorithms[u'Koloruj i popraw: losowe hiperpłaszczyzny'] = [VectorColoringAlgorithm(
    partial_color_strategy='color_all_vertices_at_once',
    partition_strategy='hyperplane_partition',
    normal_vectors_generation_strategy='random_normal',
    independent_set_extraction_strategy='max_degree_first',
    wigderson_strategy='no_wigderson',
    sdp_type='nonstrict',
    alg_name='random hyperplane partition',
    deterministic=False
), 5]

algorithms[u'Strategia zbiorów niezależnych: rzutowanie wektorów'] = [VectorColoringAlgorithm(
    partial_color_strategy='color_by_independent_sets',
    find_independent_sets_strategy='random_vector_projection',
    independent_set_extraction_strategy='max_degree_first',
    wigderson_strategy='no_wigderson',
    sdp_type='nonstrict',
    alg_name='random vector projection',
    deterministic=False
), 7]

algorithms[u'Strategia zbiorów niezależnych: klasteryzacja'] = [VectorColoringAlgorithm(
    partial_color_strategy='color_by_independent_sets',
    find_independent_sets_strategy='clustering',
    independent_set_extraction_strategy='max_degree_first',
    wigderson_strategy='no_wigderson',
    sdp_type='nonstrict',
    alg_name='clustering independent sets',
    deterministic=True
), 8]

algorithms[u'Greedy Independent Set'] = [ColoringAlgorithm(
    lambda graph: nx.algorithms.coloring.greedy_color(graph, strategy='independent_set'), 'greedy_independent_set'), 0]

algorithms[u'DSATUR'] = [ColoringAlgorithm(
    lambda graph: nx.algorithms.coloring.greedy_color(graph, strategy='DSATUR'), 'dsatur'), 1]

algorithms[u'Kolorowanie optymalne (programowanie liniowe)'] = [ColoringAlgorithm(
    lambda graph: compute_optimal_coloring_lp(graph, verbose=True), 'optimal_lp'), 2]

algorithms[u'Kolorowanie optymalne (programowanie dynamiczne)'] = [ColoringAlgorithm(
    lambda graph: compute_optimal_coloring_dp(graph, verbose=True), 'optimal_dp'), 3]

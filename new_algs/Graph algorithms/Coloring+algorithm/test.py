"""Script for running the algorithms on specified graphs.

Usage: python test.py
"""

from datetime import datetime
from timeit import default_timer as timer

from algorithm import *
from graph_create import *
from graph_io import *
from results_processing import *

# gg = create_k_cycle(n=250, k=24)  # done (second time error RVP)
# save_graph_to_col_file(gg)

# Logging configuration
logging.basicConfig(format='%(message)s', level=logging.DEBUG, datefmt='%I:%M:%S')

# Test graph creation
graphs = []

# graphs.append(nx.powerlaw_cluster_graph(180, 37, 0.3)) # duza przewaga dsatur
# graphs.append(create_erdos_renyi_graph(n=120, p=0.5))  # nie widac roznicy
# graphs.append(create_barabasi_albert_graph(n=20, m=20))
# graphs.append(create_watts_strogatz_graph(30, 6, 0.6))
# graphs.append(nx.ring_of_cliques(10, 7))
# graphs.append(nx.connected_caveman_graph(10,10))
# graphs.append(nx.random_regular_graph(19, 160))
# graphs.append(nx.circular_ladder_graph(140))
# graphs.append(nx.dorogovtsev_goltsev_mendes_graph(2))
# graphs.append(nx.full_rary_tree(40, 350))
# graphs.append(nx.ladder_graph(150))
# graphs.append(nx.lollipop_graph(20, 50))
# graphs.append(nx.star_graph(150))
# graphs.append(nx.turan_graph(150, 9))
# graphs.append(nx.wheel_graph(170))
# graphs.append(nx.margulis_gabber_galil_graph(12)) # contains selfloops
# graphs.append(nx.chordal_cycle_graph(131))
# graphs.append(create_crown_graph(130))
# graphs.append(nx.triangular_lattice_graph(30,21))
# graphs.append(nx.tutte_graph())
# graphs.append(nx.random_lobster(130, 0.8, 0.7))
# graphs.append(nx.duplication_divergence_graph(170, 0.999))
# graphs.append(nx.geographical_threshold_graph(150, 0.2))
# graphs.append(nx.windmill_graph(16, 14))
# graphs.append(nx.mycielski_graph(8))
# graphs.append(nx.random_partition_graph([x for x in range(15, 23)], 0.9, 0.2))

# graphs.append(read_graph_from_file('other', 'grotzsch', starting_index=0))
graphs.append(read_graph_from_file("dimacs", "DSJC125.5", starting_index=1))
# graphs.append(read_graph_from_file("dimacs", "DSJC1000.1", starting_index=1))

# graphs.append(create_k_cycle(4, 20))

algorithms = []


algorithms.append(VectorColoringAlgorithm(
    partial_color_strategy='color_all_vertices_at_once',
    partition_strategy='clustering',
    independent_set_extraction_strategy='max_degree_first',
    wigderson_strategy='no_wigderson',
    sdp_type='nonstrict',
    alg_name='clustering all vertices',
    deterministic=True
))

# algorithms.append(VectorColoringAlgorithm(
#     partial_color_strategy='color_all_vertices_at_once',
#     partition_strategy='hyperplane_partition',
#     normal_vectors_generation_strategy='orthonormal',
#     independent_set_extraction_strategy='max_degree_first',
#     wigderson_strategy='no_wigderson',
#     sdp_type='nonstrict',
#     alg_name='orthonormal hyperplane partition',
#     deterministic=False
# ))

# algorithms.append(VectorColoringAlgorithm(
#     partial_color_strategy='color_all_vertices_at_once',
#     partition_strategy='hyperplane_partition',
#     normal_vectors_generation_strategy='random_normal',
#     independent_set_extraction_strategy='max_degree_first',
#     wigderson_strategy='no_wigderson',
#     sdp_type='nonstrict',
#     alg_name='random hyperplane partition',
#     deterministic=False
# ))
#
# algorithms.append(VectorColoringAlgorithm(
#     partial_color_strategy='color_by_independent_sets',
#     find_independent_sets_strategy='random_vector_projection',
#     independent_set_extraction_strategy='max_degree_first',
#     wigderson_strategy='no_wigderson',
#     sdp_type='nonstrict',
#     alg_name='random vector projection',
#     deterministic=False
# ))
#
# algorithms.append(VectorColoringAlgorithm(
#     partial_color_strategy='color_by_independent_sets',
#     find_independent_sets_strategy='clustering',
#     independent_set_extraction_strategy='max_degree_first',
#     wigderson_strategy='no_wigderson',
#     sdp_type='nonstrict',
#     alg_name='clustering independent sets',
#     deterministic=True
# ))

algorithms.append(ColoringAlgorithm(
    lambda g: nx.algorithms.coloring.greedy_color(g, strategy='independent_set'), 'greedy_independent_set'))

algorithms.append(ColoringAlgorithm(
    lambda g: nx.algorithms.coloring.greedy_color(g, strategy='DSATUR'), 'dsatur'))

# algorithms.append(ColoringAlgorithm(lambda g: compute_optimal_coloring_lp(g), 'optimal_coloring_lp'))
#
# algorithms.append(ColoringAlgorithm(lambda g: compute_optimal_coloring_dp(g), 'optimal_coloring_dp'))

# Run algorithms to obtain colorings
repetitions_per_graph = 1
algorithms_results = {}  # Dictionary - graph: list of RunResults (one result per algorithm)
config.run_seed = datetime.now().strftime("%m-%d_%H-%M-%S")
for graph_counter, graph in enumerate(graphs):
    algorithms_results[graph] = []
    for alg_counter, alg in enumerate(algorithms):
        logging.info("\nComputing graph: {0} ({2}/{3}), algorithm: {1} ({4}/{5}) ...\n".format(
            graph.name, alg.get_algorithm_name(), graph_counter + 1, len(graphs), alg_counter + 1, len(algorithms)))
        nrs_of_colors = []
        times = []
        graph_colorings = []
        for iteration in range(repetitions_per_graph):
            start = timer()
            coloring = alg.color_graph(graph, verbose=True)
            end = timer()
            times.append(end - start)
            graph_colorings.append(coloring)

        results = RunResults()
        results.graph = graph
        results.algorithm = alg
        results.average_time = np.mean(times)
        results.best_coloring = min(graph_colorings, key=lambda coloring: len(set(coloring.values())))
        results.average_nr_of_colors = np.mean([len(set(coloring.values())) for coloring in graph_colorings])
        results.repetitions = repetitions_per_graph

        algorithms_results[graph].append(results)
        logging.info("Done graph: {0}, algorithm: {1}, colors: {2}, time: {3:6.2f} s ...\n".format(
            graph.name, alg.get_algorithm_name(), len(set(results.best_coloring.values())), results.average_time))
    save_graph_run_data_to_file(algorithms_results[graph], graph)

logging.shutdown()

# Check if colorings are legal
for graph in algorithms_results:
    for results in algorithms_results[graph]:
        if not check_if_coloring_legal(graph, results.best_coloring):
            raise Exception('Coloring obtained by {0} on {1} is not legal'.format(results.algorithm.name, graph.name))

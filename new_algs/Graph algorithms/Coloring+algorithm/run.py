# -*- coding: utf-8 -*-
from datetime import datetime
from timeit import default_timer as timer

import algorithm_config
from algorithm import *
from graph_io import *
from results_processing import *


def do_run(fullpath, algorithm_name):
    # Logging configuration
    logging.basicConfig(format='%(message)s', level=logging.DEBUG, datefmt='%I:%M:%S')

    (_, filename) = os.path.split(fullpath)
    (graph_name, _) = os.path.splitext(filename)
    graph = read_graph_from_file(folder_name="", graph_name=graph_name, graph_type=None, starting_index=0,
                                 fullpath=fullpath)

    algorithm = algorithm_config.algorithms[algorithm_name][0]

    graphs = [graph]
    algorithms = [algorithm]

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
                raise Exception(
                    'Coloring obtained by {0} on {1} is not legal'.format(results.algorithm.name, graph.name))

    return algorithms_results


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print "Usage: python run.py <path_to_graphfile>.col <algorithm>"
        sys.exit()

    if not os.path.exists(sys.argv[1]):
        print "Plik {0} nie istnieje".format(sys.argv[1])
        sys.exit()

    if not algorithm_config.algorithms.has_key(sys.argv[2]):
        print "Algorytm {0} nie istnieje".format(sys.argv[2])
        sys.exit()

    do_run(sys.argv[1], sys.argv[2])

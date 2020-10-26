if __name__ == '__main__':

    from datetime import datetime
    from timeit import default_timer as timer
    from graph_create import *
    from algorithm import *
    from graph_io import *
    from results_processing import *

    # Logging configuration
    logging.basicConfig(format='%(message)s', level=logging.DEBUG, datefmt='%I:%M:%S')

    # Test graph creation
    graphs = []

    graphs.append(read_graph_from_file("dimacs", "DSJC125.1", 'random', starting_index=1))
    # graphs.append(create_erdos_renyi_graph(n=250, p=0.9, name_suffix='1'))  # done

    # Random graphs
    # graphs.append(read_graph_from_file("dimacs", "DSJC250.5", 'random', starting_index=1))  # usun to zaraz
    # graphs.append(read_graph_from_file("dimacs", "DSJC125.1", 'random', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "DSJC125.5", 'random', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "DSJC125.9", 'random', starting_index=1))  # PROBLEM
    # graphs.append(read_graph_from_file("dimacs", "DSJC250.1", 'random', starting_index=1))  # done
    #
    #
    #
    # ##Geometric random graphs
    #
    # graphs.append(read_graph_from_file("dimacs", "DSJR500.1", 'random_geometric', starting_index=1))  # done
    #
    # graphs.append(read_graph_from_file("dimacs", "r125.1", 'random_geometric', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "r125.1c", 'random_geometric', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "r125.5", 'random_geometric', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "r250.1", 'random_geometric', starting_index=1))  # done
    #
    #
    # ##Quadi-random graphs with flatness = 0
    #
    #
    # # Register allocation based on real code
    #
    #
    # graphs.append(read_graph_from_file("dimacs", "fpsol2.i.2",'register_allocation', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "fpsol2.i.3",'register_allocation', starting_index=1))  # done
    #
    # graphs.append(read_graph_from_file("dimacs", "mulsol.i.1",'register_allocation', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "mulsol.i.2",'register_allocation', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "mulsol.i.3",'register_allocation', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "mulsol.i.4",'register_allocation', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "mulsol.i.5",'register_allocation', starting_index=1))  # done
    #
    # graphs.append(read_graph_from_file("dimacs", "zeroin.i.1",'register_allocation', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "zeroin.i.2",'register_allocation', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "zeroin.i.3",'register_allocation', starting_index=1))  # done
    #
    # ##Leighton graphs
    #
    #
    #
    # ##Graphs based on Mycielski transformation
    #
    # graphs.append(read_graph_from_file("dimacs", "myciel2", 'mycielski_graph', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "myciel3", 'mycielski_graph', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "myciel4", 'mycielski_graph', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "myciel5", 'mycielski_graph', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "myciel6", 'mycielski_graph', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "myciel7", 'mycielski_graph', starting_index=1))  # done
    #
    # ##Class scheduling graphs
    #
    #
    # ## Stanford graph database
    # #
    # graphs.append(read_graph_from_file("dimacs", "games120", 'stanford_gb', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "huck", 'stanford_gb',starting_index=1)) # done
    # graphs.append(read_graph_from_file("dimacs", "jean", 'stanford_gb',starting_index=1)) # done
    # graphs.append(read_graph_from_file("dimacs", "anna", 'stanford_gb',starting_index=1)) # done
    # graphs.append(read_graph_from_file("dimacs", "david",'stanford_gb', starting_index=1)) # done
    #
    # graphs.append(read_graph_from_file("dimacs", "miles250", 'stanford_gb',starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "miles500", 'stanford_gb',starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "miles750", 'stanford_gb',starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "miles1000",'stanford_gb', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "miles1500",'stanford_gb', starting_index=1))  # done
    #
    # graphs.append(read_graph_from_file("dimacs", "queen5_5", 'stanford_gb',starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "queen6_6", 'stanford_gb',starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "queen7_7", 'stanford_gb',starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "queen8_8", 'stanford_gb',starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "queen8_12",'stanford_gb', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "queen9_9", 'stanford_gb',starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "queen10_10", 'stanford_gb',starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "queen11_11", 'stanford_gb',starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "queen12_12", 'stanford_gb',starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "queen13_13", 'stanford_gb',starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "queen14_14", 'stanford_gb',starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "queen15_15", 'stanford_gb',starting_index=1))  # done

    # long lasting

    # graphs.append(create_k_cycle(n=50, k=5))
    # graphs.append(create_k_cycle(n=50, k=12))
    # graphs.append(create_k_cycle(n=50, k=20))
    # graphs.append(create_k_cycle(n=125, k=12))
    # graphs.append(create_k_cycle(n=125, k=30))

    # graphs.append(create_k_cycle(n=125, k=50))
    # graphs.append(create_k_cycle(n=250, k=24))
    # graphs.append(create_k_cycle(n=250, k=60))
    # graphs.append(create_k_cycle(n=250, k=100))  do later or never

    # graphs.append(read_graph_from_file("dimacs", "queen16_16", 'stanford_gb', starting_index=1))  # done

    # graphs.append(create_erdos_renyi_graph(n=50, p=0.1, name_suffix='1'))  # done
    # graphs.append(create_erdos_renyi_graph(n=50, p=0.5, name_suffix='1'))  # done
    # graphs.append(create_erdos_renyi_graph(n=50, p=0.9, name_suffix='1'))  # done
    # graphs.append(create_erdos_renyi_graph(n=125, p=0.1, name_suffix='1'))  # done
    # graphs.append(create_erdos_renyi_graph(n=125, p=0.5, name_suffix='1'))  # done
    # graphs.append(create_erdos_renyi_graph(n=125, p=0.9, name_suffix='1'))  # done
    # graphs.append(create_erdos_renyi_graph(n=250, p=0.1, name_suffix='1'))  # done
    # graphs.append(create_erdos_renyi_graph(n=250, p=0.5, name_suffix='1'))  # done

    # graphs.append(create_erdos_renyi_graph(n=50, p=0.1, name_suffix='2'))  # done
    # graphs.append(create_erdos_renyi_graph(n=50, p=0.5, name_suffix='2'))  # done
    # graphs.append(create_erdos_renyi_graph(n=50, p=0.9, name_suffix='2'))  # done
    # graphs.append(create_erdos_renyi_graph(n=125, p=0.1, name_suffix='2'))  # done
    # graphs.append(create_erdos_renyi_graph(n=125, p=0.5, name_suffix='2'))  # done
    # graphs.append(create_erdos_renyi_graph(n=125, p=0.9, name_suffix='2'))  # done
    # graphs.append(create_erdos_renyi_graph(n=250, p=0.1, name_suffix='2'))  # done
    # graphs.append(create_erdos_renyi_graph(n=250, p=0.5, name_suffix='2'))  # done

    # graphs.append(create_erdos_renyi_graph(n=50, p=0.1, name_suffix='3'))  # done
    # graphs.append(create_erdos_renyi_graph(n=50, p=0.5, name_suffix='3'))  # done
    # graphs.append(create_erdos_renyi_graph(n=50, p=0.9, name_suffix='3'))  # done
    # graphs.append(create_erdos_renyi_graph(n=125, p=0.1, name_suffix='3'))  # done
    # graphs.append(create_erdos_renyi_graph(n=125, p=0.5, name_suffix='3'))  # done
    # graphs.append(create_erdos_renyi_graph(n=125, p=0.9, name_suffix='3'))  # done
    # graphs.append(create_erdos_renyi_graph(n=250, p=0.1, name_suffix='3'))  # done
    # # graphs.append(create_erdos_renyi_graph(n=250, p=0.5, name_suffix='3'))  # done
    #
    # graphs.append(create_watts_strogatz_graph(n=50, k=5, p=0.1, name_suffix='1'))  # done
    # graphs.append(create_watts_strogatz_graph(n=50, k=25, p=0.1, name_suffix='1'))  # done
    # graphs.append(create_watts_strogatz_graph(n=50, k=40, p=0.1, name_suffix='1'))  # done
    # graphs.append(create_watts_strogatz_graph(n=125, k=15, p=0.1, name_suffix='1'))  # done
    # graphs.append(create_watts_strogatz_graph(n=125, k=60, p=0.1, name_suffix='1'))  # done
    # graphs.append(create_watts_strogatz_graph(n=125, k=100, p=0.1, name_suffix='1'))  # done
    # graphs.append(create_watts_strogatz_graph(n=250, k=30, p=0.1, name_suffix='1'))  # done
    # graphs.append(create_watts_strogatz_graph(n=250, k=120, p=0.1, name_suffix='1'))  # done (second time error RVP)

    # graphs.append(create_watts_strogatz_graph(n=50, k=5, p=0.1, name_suffix='2'))  # done
    # graphs.append(create_watts_strogatz_graph(n=50, k=25, p=0.1, name_suffix='2'))  # done
    # graphs.append(create_watts_strogatz_graph(n=50, k=40, p=0.1, name_suffix='2'))  # done
    # graphs.append(create_watts_strogatz_graph(n=125, k=15, p=0.1, name_suffix='2'))  # done
    # graphs.append(create_watts_strogatz_graph(n=125, k=60, p=0.1, name_suffix='2'))  # done
    # graphs.append(create_watts_strogatz_graph(n=125, k=100, p=0.1, name_suffix='2'))  # done
    # graphs.append(create_watts_strogatz_graph(n=250, k=30, p=0.1, name_suffix='2'))  # done
    # # graphs.append(create_watts_strogatz_graph(n=250, k=120, p=0.1, name_suffix='2'))  # done (second time error RVP)
    #
    # graphs.append(create_watts_strogatz_graph(n=50, k=5, p=0.1, name_suffix='3'))  # done
    # graphs.append(create_watts_strogatz_graph(n=50, k=25, p=0.1, name_suffix='3'))  # done
    # graphs.append(create_watts_strogatz_graph(n=50, k=40, p=0.1, name_suffix='3'))  # done
    # graphs.append(create_watts_strogatz_graph(n=125, k=15, p=0.1, name_suffix='3'))  # done
    # graphs.append(create_watts_strogatz_graph(n=125, k=60, p=0.1, name_suffix='3'))  # done
    # graphs.append(create_watts_strogatz_graph(n=125, k=100, p=0.1, name_suffix='3'))  # done
    # graphs.append(create_watts_strogatz_graph(n=250, k=30, p=0.1, name_suffix='3'))  # done
    # graphs.append(create_watts_strogatz_graph(n=250, k=120, p=0.1, name_suffix='3'))  # done (second time error RVP)

    # graphs.append(create_barabasi_albert_graph(n=50, m=int(0.1 * ((50 * 49) / 2)), name_suffix='1'))  #
    # graphs.append(create_barabasi_albert_graph(n=50, m=int(0.5 * ((50 * 49) / 2)), name_suffix='1'))  #
    # graphs.append(create_barabasi_albert_graph(n=50, m=int(0.9 * ((50 * 49) / 2)), name_suffix='1'))  #
    # graphs.append(create_barabasi_albert_graph(n=125, m=int(0.1 * ((125 * 124) / 2)), name_suffix='1'))
    # graphs.append(create_barabasi_albert_graph(n=125, m=int(0.5 * ((125 * 124) / 2)), name_suffix='1'))
    # graphs.append(create_barabasi_albert_graph(n=125, m=int(0.9 * ((125 * 124) / 2)), name_suffix='1'))
    # graphs.append(create_barabasi_albert_graph(n=250, m=int(0.1 * ((250 * 249) / 2)), name_suffix='1'))
    # # graphs.append(create_barabasi_albert_graph(n=250, m=int(0.5*((250*249)/2)), name_suffix='1'))
    # # graphs.append(create_barabasi_albert_graph(n=250, m=int(0.9*((250*249)/2)), name_suffix='1'))
    #
    # graphs.append(create_barabasi_albert_graph(n=50, m=int(0.1 * ((50 * 49) / 2)), name_suffix='2'))
    # graphs.append(create_barabasi_albert_graph(n=50, m=int(0.5 * ((50 * 49) / 2)), name_suffix='2'))
    # graphs.append(create_barabasi_albert_graph(n=50, m=int(0.9 * ((50 * 49) / 2)), name_suffix='2'))
    # graphs.append(create_barabasi_albert_graph(n=125, m=int(0.1 * ((125 * 124) / 2)), name_suffix='2'))
    # graphs.append(create_barabasi_albert_graph(n=125, m=int(0.5 * ((125 * 124) / 2)), name_suffix='2'))
    # graphs.append(create_barabasi_albert_graph(n=125, m=int(0.9 * ((125 * 124) / 2)), name_suffix='2'))
    # graphs.append(create_barabasi_albert_graph(n=250, m=int(0.1 * ((250 * 249) / 2)), name_suffix='2'))
    # graphs.append(create_barabasi_albert_graph(n=250, m=int(0.5 * ((250 * 249) / 2)), name_suffix='2'))
    # graphs.append(create_barabasi_albert_graph(n=250, m=int(0.9 * ((250 * 249) / 2)), name_suffix='2'))

    graphs.append(create_barabasi_albert_graph(n=50, m=int(0.1 * ((50 * 49) / 2)), name_suffix='3'))
    graphs.append(create_barabasi_albert_graph(n=50, m=int(0.5 * ((50 * 49) / 2)), name_suffix='3'))
    graphs.append(create_barabasi_albert_graph(n=50, m=int(0.9 * ((50 * 49) / 2)), name_suffix='3'))
    graphs.append(create_barabasi_albert_graph(n=125, m=int(0.1 * ((125 * 124) / 2)), name_suffix='3'))
    graphs.append(create_barabasi_albert_graph(n=125, m=int(0.5 * ((125 * 124) / 2)), name_suffix='3'))
    graphs.append(create_barabasi_albert_graph(n=125, m=int(0.9 * ((125 * 124) / 2)), name_suffix='3'))
    graphs.append(create_barabasi_albert_graph(n=250, m=int(0.1 * ((250 * 249) / 2)), name_suffix='3'))
    graphs.append(create_barabasi_albert_graph(n=250, m=int(0.5 * ((250 * 249) / 2)), name_suffix='3'))
    graphs.append(create_barabasi_albert_graph(n=250, m=int(0.9 * ((250 * 249) / 2)), name_suffix='3'))

    # graphs.append(read_graph_from_file("dimacs", "le450_5a", 'leighton_graph', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "le450_5b", 'leighton_graph', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "le450_5c", 'leighton_graph', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "le450_5d", 'leighton_graph', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "le450_15a", 'leighton_graph', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "le450_15b", 'leighton_graph', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "le450_25a", 'leighton_graph', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "le450_25b", 'leighton_graph', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "le450_15c", 'leighton_graph', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "le450_15d", 'leighton_graph', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "le450_25c", 'leighton_graph', starting_index=1))
    # graphs.append(read_graph_from_file("dimacs", "le450_25d", 'leighton_graph', starting_index=1))
    #
    # graphs.append(read_graph_from_file("dimacs", "fpsol2.i.1", 'register_allocation', starting_index=1))  # done
    #
    # graphs.append(read_graph_from_file("dimacs", "school1", 'class_scheduling', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "school1_nsh", 'class_scheduling', starting_index=1))  # done
    #
    # graphs.append(read_graph_from_file("dimacs", "flat300_20_0", 'random_flat', starting_index=1))  # clust
    # graphs.append(read_graph_from_file("dimacs", "flat300_26_0", 'random_flat', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "flat300_28_0", 'random_flat', starting_index=1))  # done
    #
    # graphs.append(read_graph_from_file("dimacs", "DSJC250.5", 'random', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "DSJC250.9", 'random', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "DSJC500.1", 'random', starting_index=1))  # done
    #
    # graphs.append(read_graph_from_file("dimacs", "r250.1c", 'random_geometric', starting_index=1))  # done
    # graphs.append(read_graph_from_file("dimacs", "r250.5", 'random_geometric', starting_index=1))  # done

    algorithms = []

    algorithms.append(VectorColoringAlgorithm(
        partial_color_strategy='color_by_independent_sets',
        find_independent_sets_strategy='random_vector_projection',
        independent_set_extraction_strategy='max_degree_first',
        wigderson_strategy='no_wigderson',
        sdp_type='nonstrict',
        alg_name='random vector projection',
        deterministic=False
    ))

    algorithms.append(VectorColoringAlgorithm(
        partial_color_strategy='color_by_independent_sets',
        find_independent_sets_strategy='clustering',
        independent_set_extraction_strategy='max_degree_first',
        wigderson_strategy='no_wigderson',
        sdp_type='nonstrict',
        alg_name='clustering independent sets',
        deterministic=True
    ))

    algorithms.append(VectorColoringAlgorithm(
        partial_color_strategy='color_all_vertices_at_once',
        partition_strategy='hyperplane_partition',
        normal_vectors_generation_strategy='random_normal',
        independent_set_extraction_strategy='max_degree_first',
        wigderson_strategy='no_wigderson',
        sdp_type='nonstrict',
        alg_name='random hyperplane partition',
        deterministic=False
    ))

    algorithms.append(VectorColoringAlgorithm(
        partial_color_strategy='color_all_vertices_at_once',
        partition_strategy='hyperplane_partition',
        normal_vectors_generation_strategy='orthonormal',
        independent_set_extraction_strategy='max_degree_first',
        wigderson_strategy='no_wigderson',
        sdp_type='nonstrict',
        alg_name='orthonormal hyperplane partition',
        deterministic=False
    ))

    algorithms.append(VectorColoringAlgorithm(
        partial_color_strategy='color_all_vertices_at_once',
        partition_strategy='clustering',
        independent_set_extraction_strategy='max_degree_first',
        wigderson_strategy='no_wigderson',
        sdp_type='nonstrict',
        alg_name='clustering all vertices',
        deterministic=True
    ))

    algorithms.append(ColoringAlgorithm(
        lambda g: nx.algorithms.coloring.greedy_color(g, strategy='independent_set'), 'greedy_independent_set'))

    algorithms.append(ColoringAlgorithm(
        lambda g: nx.algorithms.coloring.greedy_color(g, strategy='DSATUR'), 'dsatur'))

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
                coloring = alg.color_graph(graph, verbose=config.solver_verbose)
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
            logging.info("# done graph: {0}, algorithm: {1}, colors: {2}, time: {3:6.2f} s ...\n".format(
                graph.name, alg.get_algorithm_name(), len(set(results.best_coloring.values())), results.average_time))
        save_graph_run_data_to_file(algorithms_results[graph], graph)

    logging.shutdown()

    # Check if colorings are legal
    for graph in algorithms_results:
        for results in algorithms_results[graph]:
            if not check_if_coloring_legal(graph, results.best_coloring):
                raise Exception(
                    'Coloring obtained by {0} on {1} is not legal'.format(results.algorithm.name, graph.name))

from results_processing import *

# Test graph creation
# tested_graphs = []
#
# tested_graphs.append(read_graph_from_file("dimacs", "DSJC125.1", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "DSJC125.5", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "DSJC125.9", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "DSJC250.1", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "DSJC250.5", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "DSJC250.9", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "DSJC500.1", starting_index=1))
#
# tested_graphs.append(read_graph_from_file("dimacs", "DSJR500.1", starting_index=1))
#
# tested_graphs.append(read_graph_from_file("dimacs", "flat300_20_0", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "flat300_26_0", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "flat300_28_0", starting_index=1))
#
# tested_graphs.append(read_graph_from_file("dimacs", "fpsol2.i.1", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "fpsol2.i.2", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "fpsol2.i.3", starting_index=1))
#
# tested_graphs.append(read_graph_from_file("dimacs", "mulsol.i.1", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "mulsol.i.2", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "mulsol.i.3", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "mulsol.i.4", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "mulsol.i.5", starting_index=1))
#
# tested_graphs.append(read_graph_from_file("dimacs", "zeroin.i.1", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "zeroin.i.2", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "zeroin.i.3", starting_index=1))
#
# tested_graphs.append(read_graph_from_file("dimacs", "games120", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "huck", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "jean", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "anna", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "david", starting_index=1))
#
# tested_graphs.append(read_graph_from_file("dimacs", "le450_5a", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "le450_5b", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "le450_5c", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "le450_5d", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "le450_15a", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "le450_15b", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "le450_15c", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "le450_15d", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "le450_25a", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "le450_25b", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "le450_25c", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "le450_25d", starting_index=1))
#
# tested_graphs.append(read_graph_from_file("dimacs", "miles250", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "miles500", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "miles750", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "miles1000", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "miles1500", starting_index=1))
#
# tested_graphs.append(read_graph_from_file("dimacs", "myciel2", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "myciel3", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "myciel4", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "myciel5", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "myciel6", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "myciel7", starting_index=1))
#
# tested_graphs.append(read_graph_from_file("dimacs", "queen5_5", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "queen6_6", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "queen7_7", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "queen8_8", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "queen8_12", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "queen9_9", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "queen10_10", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "queen11_11", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "queen12_12", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "queen13_13", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "queen14_14", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "queen15_15", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "queen16_16", starting_index=1))
#
# tested_graphs.append(read_graph_from_file("dimacs", "r125.1", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "r125.1c", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "r125.5", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "r250.1", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "r250.1c", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "r250.5", starting_index=1))
#
# tested_graphs.append(read_graph_from_file("dimacs", "school1", starting_index=1))
# tested_graphs.append(read_graph_from_file("dimacs", "school1_nsh", starting_index=1))

chromatic_number = {}
exact = True
chi_ind = -1
chi_lb_ind = -1
chi_ub_ind = -1
with open("/home/hubert/chromatic_numbers.txt", 'r') as infile:
    for line in infile:
        values = line.split()
        if values[0] == 'x':
            if len(values) == 2:
                exact = True
                chi_ind = int(values[1])
            else:
                exact = False
                chi_lb_ind = int(values[1])
                chi_ub_ind = int(values[2])
        else:
            if exact:
                chromatic_number[values[0]] = str(values[chi_ind])
            else:
                chromatic_number[values[0]] = '[' + values[chi_lb_ind] + ';' + values[chi_ub_ind] + ']'

results = load_algorithm_run_data_from_file('AggregatedResults')
for graph_name in sorted(results.keys(), key=lambda k: (
        results[k][0]['graph_family'], int(results[k][0]['graph_nr_of_vertices']),
        float(results[k][0]['graph_density']))):
    if graph_name.startswith("erdos"):
        a = 2
    orthonormal_hyperplane_partition = \
        filter(lambda x: x['algorithm_name'] == 'orthonormal hyperplane partition', results[graph_name])[0]
    clustering_all_vertices = \
        filter(lambda x: x['algorithm_name'] == 'clustering all vertices', results[graph_name])[0]
    random_hyperplane_partition = \
        filter(lambda x: x['algorithm_name'] == 'random hyperplane partition', results[graph_name])[0]
    random_vector_projection = \
        filter(lambda x: x['algorithm_name'] == 'random vector projection', results[graph_name])[0]
    clustering_independent_sets = \
        filter(lambda x: x['algorithm_name'] == 'clustering independent sets', results[graph_name])[0]
    greedy_independent_set = filter(lambda x: x['algorithm_name'] == 'greedy_independent_set', results[graph_name])[
        0]
    dsatur = filter(lambda x: x['algorithm_name'] == 'dsatur', results[graph_name])[0]

with open("/home/hubert/graph_table_clr", 'w') as outfile:
    results = load_algorithm_run_data_from_file('AggregatedResults')
    for graph_name in sorted(results.keys(), key=lambda k: (
            results[k][0]['graph_family'], int(results[k][0]['graph_nr_of_vertices']),
            float(results[k][0]['graph_density']))):
        orthonormal_hyperplane_partition = \
            filter(lambda x: x['algorithm_name'] == 'orthonormal hyperplane partition', results[graph_name])[0]
        clustering_all_vertices = \
            filter(lambda x: x['algorithm_name'] == 'clustering all vertices', results[graph_name])[0]
        random_hyperplane_partition = \
            filter(lambda x: x['algorithm_name'] == 'random hyperplane partition', results[graph_name])[0]
        random_vector_projection = \
            filter(lambda x: x['algorithm_name'] == 'random vector projection', results[graph_name])[0]
        clustering_independent_sets = \
            filter(lambda x: x['algorithm_name'] == 'clustering independent sets', results[graph_name])[0]
        greedy_independent_set = filter(lambda x: x['algorithm_name'] == 'greedy_independent_set', results[graph_name])[
            0]
        dsatur = filter(lambda x: x['algorithm_name'] == 'dsatur', results[graph_name])[0]

        last_param = chromatic_number[results[graph_name][0]['graph_family']] if \
            results[graph_name][0]['graph_family'] in chromatic_number else ' '

        latex_line = "{0} & {1} & {2:.2f} & {3} & {4} & {5} & {6} & {7} & {8} & {9} & {10} \\\\\n".format(
            results[graph_name][0]['graph_family'],
            results[graph_name][0]['graph_nr_of_vertices'],
            results[graph_name][0]['graph_density'],
            random_hyperplane_partition['min_nr_of_colors'],
            orthonormal_hyperplane_partition['min_nr_of_colors'],
            clustering_all_vertices['min_nr_of_colors'],
            random_vector_projection['min_nr_of_colors'],
            clustering_independent_sets['min_nr_of_colors'],
            greedy_independent_set['min_nr_of_colors'],
            dsatur['min_nr_of_colors'],
            last_param
        ).replace("_", "\_")

        latex_line_colors = latex_line.split(' & ')[3:10]
        latex_line_colors = map(lambda s: float(s), latex_line_colors)
        min_color = min(latex_line_colors)
        m_latex_line = latex_line.split(' & ')
        for i in range(3, 10):
            str = m_latex_line[i]
            try:
                if float(str) == min_color:
                    str = '\\textbf{' + str + '}'
            except ValueError:
                str = str
            m_latex_line[i] = str

        m_latex_line = ' & '.join(m_latex_line)

        outfile.write(m_latex_line)

with open("/home/hubert/graph_table_t", 'w') as outfile:
    results = load_algorithm_run_data_from_file('AggregatedResults')
    for graph_name in sorted(results.keys(), key=lambda k: (
            results[k][0]['graph_family'], int(results[k][0]['graph_nr_of_vertices']),
            float(results[k][0]['graph_density']))):
        orthonormal_hyperplane_partition = \
            filter(lambda x: x['algorithm_name'] == 'orthonormal hyperplane partition', results[graph_name])[0]
        clustering_all_vertices = \
            filter(lambda x: x['algorithm_name'] == 'clustering all vertices', results[graph_name])[0]
        random_hyperplane_partition = \
            filter(lambda x: x['algorithm_name'] == 'random hyperplane partition', results[graph_name])[0]
        random_vector_projection = \
            filter(lambda x: x['algorithm_name'] == 'random vector projection', results[graph_name])[0]
        clustering_independent_sets = \
            filter(lambda x: x['algorithm_name'] == 'clustering independent sets', results[graph_name])[0]
        greedy_independent_set = filter(lambda x: x['algorithm_name'] == 'greedy_independent_set', results[graph_name])[
            0]
        dsatur = filter(lambda x: x['algorithm_name'] == 'dsatur', results[graph_name])[0]

        outfile.write(
            "{0} & {1} & {2:.2f} & {3:.2f} & {4:.2f} & {5:.2f} & {6:.2f} & {7:.2f} & {8:.2f} & {9:.2f} \\\\\n".format(
                results[graph_name][0]['graph_family'],
                results[graph_name][0]['graph_nr_of_vertices'],
                results[graph_name][0]['graph_density'],
                random_hyperplane_partition['avg_time'],
                orthonormal_hyperplane_partition['avg_time'],
                clustering_all_vertices['avg_time'],
                random_vector_projection['avg_time'],
                clustering_independent_sets['avg_time'],
                greedy_independent_set['avg_time'],
                dsatur['avg_time'],
            ).replace("_", "\_"))

# trash for spawning another process
# # # freeze_support()
# q = JoinableQueue()
# # p = Process(target=compute_vector_coloring,
# #             kwargs={"graph": working_graph,
# #                     "sdp_type": self._sdp_type,
# #                     "verbose":verbose,
# #                     "iteration":it,
# #                     "queue": q})
# p = Process(target=compute_vector_coloring_2,
#             args=(working_graph, self._sdp_type, verbose, q, it))
# p.start()
# L = q.get()
# p.join()
#
#

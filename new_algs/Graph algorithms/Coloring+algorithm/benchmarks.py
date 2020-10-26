"""Script for running vector coloring algorithm on a user-defined graph.

Usage: python benchmarks.py
"""

import time

from graph_io import *
from algorithm import *


def save_running_time_plot(times):
    """Plots vector coloring algorithm running times and saves to a file."""

    output_dir = '/home/hubert/Desktop/vc-graphs/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    values = []
    for n in sorted(times.keys()):
        print('random_n{0} time: {1}'.format(n, times[n]))
        values.append(times[n])

    fig, ax = plt.subplots()
    ax.plot(sorted(times.keys()), values)

    ax.set(xlabel='vertices', ylabel='avg. time (s)', title='Coloring graph')
    ax.grid()

    plt.savefig(output_dir + 'mygraph')
    plt.close()
    # plt.show()


benchmarking_graphs = []
benchmarking_graphs.append(read_graph_from_file('dimacs', 'DSJC250.1'))


def benchmark_solver(benchmarking_graphs):
    """Measures time of finding matrix coloring of given graphs.

    Args:
        benchmarking_graphs (list): List of benchmarking graphs.
    """

    start = time.time()
    for G in benchmarking_graphs:
        find_matrix_coloring_cvxpy(G)
    end = time.time()
    print '\nbenchmarking time:', end - start


def benchmark_algorithm(benchmarking_graphs):
    """Measures time of coloring given graphs using vector coloring.

    Args:
        benchmarking_graphs (list): List of benchmarking graphs.
    """

    start = time.time()
    for G in benchmarking_graphs:
        color_graph(G)
    end = time.time()
    print '\nbenchmarking time:', end - start

import logging
import math
from multiprocessing import Lock, Process, Manager

import networkx as nx
import networkx.algorithms.approximation
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.stats import ortho_group

from algorithm_helper import *

np.set_printoptions(precision=5, suppress=True)


def better_partition_parallel(graph, part1, part2, independent_set_extraction_strategy):
    """ part2 i current best & part1 is shmeme list"""

    best = part2
    for i in range(len(part1)):
        if better_partition(graph, part1[i], best, independent_set_extraction_strategy):
            best = part1[i]

    return best

def better_partition(graph, part1, part2, independent_set_extraction_strategy):
    """Checks whether the first partition is better than the second one."""

    # TODO: When there are more hyperplanes it often chooses the resulting partition
    # TODO: as best even though it results in more colors (e.g. for DSJC 125.5)

    if part2 is None or len(part2) == 0:
        return True

    if part1 is None or len(part1) == 0:
        return False

    # Remove colors from one endpoint of each illegal edge in each partition.
    nodes_to_delete1 = nodes_to_delete(graph, part1, strategy=independent_set_extraction_strategy)
    nodes_to_color1 = {n for n in graph.nodes() if n not in nodes_to_delete1}
    nr_of_colors1 = len(set(part1.values()))

    nodes_to_delete2 = nodes_to_delete(graph, part2, strategy=independent_set_extraction_strategy)
    nodes_to_color2 = {n for n in graph.nodes() if n not in nodes_to_delete2}
    nr_of_colors2 = len(set(part2.values()))

    avg1 = float(len(nodes_to_color1)) / nr_of_colors1
    avg2 = float(len(nodes_to_color2)) / nr_of_colors2

    return avg1 > avg2


def color_all_vertices_at_once_parallel(graph, L, colors, init_params):
    """General strategy for coloring whole graph at once and then improving the coloring.

    This strategy colors graph by finding the best partition i.e. possibly illegal coloring of all vertices,
    and then truncating the input graph by finding some proper partial coloring and deleting its vertices.

    Args:
        graph (nx.Graph): Graph to be processed. Function modifies this parameter.
        L (2-dim matrix): Rows constitute vector coloring of graph.
        colors (dict): Dictionary of current (probably partial) colors of working graph. Function modifies this parameter.
        partition_strategy (lambda graph, L, colors, options): Function that computes coloring, possibly illegal,
            of graph using some hyperplane partition strategy
    """

    def update_colors_and_graph(graph, colors, partition):
        """Given best partition updates global colors (so that coloring is never illegal) and truncates graph graph

        Args:
            graph (nx.Graph): Graph that is being colored. The function removes some nodes from it so that only the part
                that is not yet colored remains.
            colors (dict): Global dictionary of colors of vertices of graph.
            partition (dict): Coloring of vertices of graph given by hyperplane partition. Might be illegal.
        """

        nodes_to_del = nodes_to_delete(graph, partition, strategy=init_params['independent_set_extraction_strategy'])
        nodes_to_color = {n for n in graph.nodes() if n not in nodes_to_del}

        min_color = max(colors.values()) + 1
        for v in nodes_to_color:
            colors[v] = min_color + partition[v]

        if not check_if_coloring_legal(graph, colors, partial=True):
            raise Exception('Some partition resulted in illegal coloring.')

        graph.remove_nodes_from(nodes_to_color)

    logging.info('Looking for partial coloring using all_vertices_at_once strategy...')

    best_partition = None

    manager = Manager()
    shmem_partitions = manager.list()
    lock = Lock()
    processes = []

    iterations = 1 if init_params['deterministic'] else \
        config.color_all_vertices_at_once_params['nr_of_partitions_to_try'] / config.nr_of_parallel_jobs
    nr_jobs = 1 if init_params['deterministic'] else config.nr_of_parallel_jobs

    for j in range(iterations):
        for job in range(nr_jobs):
            processes.append(Process(target=init_params['partition_strategy'], args=(
                graph, L, init_params, shmem_partitions, lock)))

        for p in processes:
            p.start()

        for p in processes:
            p.join()

        processes = []

    best_partition = better_partition_parallel(graph, shmem_partitions, best_partition,
                                               init_params['independent_set_extraction_strategy'])

    update_colors_and_graph(graph, colors, best_partition)

    logging.info('Partial coloring found. There are {0} vertices left to color'.format(graph.number_of_nodes()))



def color_all_vertices_at_once(graph, L, colors, init_params):
    """General strategy for coloring whole graph at once and then improving the coloring.

    This strategy colors graph by finding the best partition i.e. possibly illegal coloring of all vertices,
    and then truncating the input graph by finding some proper partial coloring and deleting its vertices.

    Args:
        graph (nx.Graph): Graph to be processed. Function modifies this parameter.
        L (2-dim matrix): Rows constitute vector coloring of graph.
        colors (dict): Dictionary of current (probably partial) colors of working graph. Function modifies this parameter.
        partition_strategy (lambda graph, L, colors, options): Function that computes coloring, possibly illegal,
            of graph using some hyperplane partition strategy
    """

    def update_colors_and_graph(graph, colors, partition):
        """Given best partition updates global colors (so that coloring is never illegal) and truncates graph graph

        Args:
            graph (nx.Graph): Graph that is being colored. The function removes some nodes from it so that only the part
                that is not yet colored remains.
            colors (dict): Global dictionary of colors of vertices of graph.
            partition (dict): Coloring of vertices of graph given by hyperplane partition. Might be illegal.
        """

        nodes_to_del = nodes_to_delete(graph, partition, strategy=init_params['independent_set_extraction_strategy'])
        nodes_to_color = {n for n in graph.nodes() if n not in nodes_to_del}

        min_color = max(colors.values()) + 1
        for v in nodes_to_color:
            colors[v] = min_color + partition[v]

        if not check_if_coloring_legal(graph, colors, partial=True):
            raise Exception('Some partition resulted in illegal coloring.')

        graph.remove_nodes_from(nodes_to_color)

    logging.info('Looking for partial coloring using all_vertices_at_once strategy...')

    best_partition = None
    nr_of_trials = 1 if init_params['deterministic'] else config.color_all_vertices_at_once_params[
        'nr_of_partitions_to_try']
    for it in range(nr_of_trials):
        # sys.stdout.write("\r{0}/{1}".format(it + 1, nr_of_trials))
        # sys.stdout.flush()
        partition = init_params['partition_strategy'](graph, L, init_params)

        if better_partition(graph, partition, best_partition, init_params['independent_set_extraction_strategy']):
            best_partition = partition

    # sys.stdout.write("\r")
    # sys.stdout.flush()
    update_colors_and_graph(graph, colors, best_partition)

    logging.info('Partial coloring found. There are {0} vertices left to color'.format(graph.number_of_nodes()))


def hyperplanes_partition_strategy(graph, L, init_params, shmem_partitions=None, lock=None):
    """Returns the result of single partition using random hyperplane strategy.

    Args:
        graph (networkx.Graph): Graph to be colored
        L (2-dim array): Rows of L constitute vector coloring of graph.

    Returns:
        dict: Assignment of colors to every vertex of graph given by partition of vector space. Coloring might be illegal.
    """

    def optimal_nr_of_hyperplanes(graph, L):
        """Returns the optimal number of hyperplanes.

        Returns:
            opt_nr_of_hyperplanes (int)
        """

        max_degree = max(dict(graph.degree()).values())
        k = find_number_of_vector_colors_from_vector_coloring(graph, L)
        opt_nr_of_hyperplanes = 2
        try:
            opt_nr_of_hyperplanes = 2 + int(math.ceil(math.log(max_degree, k)))
        except ValueError:
            logging.info("math domain error")

        return max(1, opt_nr_of_hyperplanes - 2)

    def get_random_vectors(nr_of_vectors, strategy):
        """Returns matrix which rows are random vectors generated according to strategy."""

        if strategy == 'orthonormal':
            array = ortho_group.rvs(nr_of_vectors)
        elif strategy == 'random_normal':
            array = np.zeros((nr_of_vectors, nr_of_vectors))
            for i in range(nr_of_vectors):
                array[i] = np.random.normal(0, 1, nr_of_vectors)
        else:
            raise Exception('Wrong random vector generation strategy')

        return array

    nr_of_hyperplanes = optimal_nr_of_hyperplanes(graph, L)

    n = graph.number_of_nodes()
    hyperplanes_sides = {v: 0 for v in range(0, n)}
    r_array = get_random_vectors(n, strategy=init_params['normal_vectors_generation_strategy'])
    for i in range(nr_of_hyperplanes):
        r = r_array[i]
        x = np.sign(np.dot(L, r))
        for v in range(0, n):
            if x[v] >= 0:
                hyperplanes_sides[v] = hyperplanes_sides[v] * 2 + 1
            else:
                hyperplanes_sides[v] = hyperplanes_sides[v] * 2

    temp_colors = {v: -1 for v in graph.nodes()}
    for i, v in enumerate(sorted(graph.nodes())):  # Assume that nodes are given in the same order as in rows of L
        temp_colors[v] = hyperplanes_sides[i]

    if shmem_partitions is not None and lock is not None:
        lock.acquire()
        shmem_partitions.append(temp_colors)
        lock.release()

    return temp_colors


def clustering_partition_strategy(graph, L, init_params, shmem_partitions=None, lock=None):
    z = linkage(L, method='complete', metric='cosine')

    k = find_number_of_vector_colors_from_vector_coloring(graph, L)
    opt_t = 1 + 1 / (k - 1) - 0.001 if k > 1.5 else 2.0  # Should guarantee each cluster can be colored with one color

    best_partition = None
    for t in np.linspace(
            opt_t * config.color_all_vertices_at_once_params['cluster_size_lower_factor'],
            opt_t * config.color_all_vertices_at_once_params['cluster_size_upper_factor'],
            config.color_all_vertices_at_once_params['nr_of_cluster_sizes_to_check']):
        clusters = fcluster(z, t, criterion='distance')
        partition = {n: clusters[v] for v, n in enumerate(sorted(list(graph.nodes())))}
        if better_partition(graph, partition, best_partition, init_params['independent_set_extraction_strategy']):
            best_partition = partition

    if shmem_partitions is not None and lock is not None:
        lock.acquire()
        shmem_partitions.append(best_partition)
        lock.release()

    return best_partition


def kmeans_clustering_partition_strategy(graph, L, init_params):
    from spherecluster import SphericalKMeans

    n = graph.number_of_nodes()
    best_partition = None
    for k in range(int(0.2 * n) + 1, int(0.5 * n), 5):
        # clusters = KMeans(n_clusters=k).fit_predict(L)
        # partition = {n: clusters[v] for v, n in enumerate(sorted(list(graph.nodes())))}
        skm = SphericalKMeans(n_clusters=k).fit(L)
        partition = {n: skm.labels_[v] for v, n in enumerate(sorted(list(graph.nodes())))}
        if better_partition(graph, partition, best_partition):
            best_partition = partition

    return best_partition

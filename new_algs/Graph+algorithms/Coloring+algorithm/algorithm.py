"""Module containing main algorithm logic."""

import itertools
import logging
import sys

from mosek.fusion import *
from networkx import Graph

import color_all_vertices_at_once
import color_by_independent_sets
# import wigderson
from algorithm_helper import *
from solver import compute_vector_coloring


class ColoringAlgorithm:

    def __init__(self, color_func, alg_name=None):
        """Creates algorithm coloring graphs using color_func procedure.

        Args:
            color_func (nx.Graph->dict): Function that takes nx.Graph and returns vertex: color dictionary
            alg_name (str): Optional algorithm name.
        """

        self._color_graph = color_func
        if alg_name is not None:
            self.name = alg_name
        else:
            self.name = str(self.color_graph)

    def color_graph(self, graph, colors=None, verbose=False):
        """Color graph using self._color_graph and ignoring 'colors' and 'verbose' parameters"""

        return self._color_graph(graph)

    def get_algorithm_name(self):
        return self.name


class VectorColoringAlgorithm:
    partial_color_strategy_map = {
        'color_all_vertices_at_once': color_all_vertices_at_once.color_all_vertices_at_once,
        'color_by_independent_sets': color_by_independent_sets.color_by_independent_sets,
    }
    find_independent_sets_strategy_map = {
        'random_vector_projection': color_by_independent_sets.find_ind_sets_by_random_vector_projection,
        'clustering': color_by_independent_sets.find_ind_sets_by_clustering,
        None: None,
    }
    partition_strategy_map = {
        'hyperplane_partition': color_all_vertices_at_once.hyperplanes_partition_strategy,
        'clustering': color_all_vertices_at_once.clustering_partition_strategy,
        'kmeans_clustering': color_all_vertices_at_once.kmeans_clustering_partition_strategy,
        None: None,
    }

    # wigderson_strategy_map = {
    #     'no_wigderson': wigderson.no_wigderson_strategy,
    #     'recursive_wigderson': wigderson.recursive_wigderson_strategy,
    # }

    def __init__(self,
                 partial_color_strategy,
                 wigderson_strategy='no_wigderson',
                 partition_strategy=None,
                 normal_vectors_generation_strategy='random_normal',
                 find_independent_sets_strategy=None,
                 independent_set_extraction_strategy='max_degree_first',
                 sdp_type='nonstrict',
                 alg_name=None,
                 deterministic=False):
        """Describe here the interfaces for all those strategies"""

        # TODO: Check for wrong strategy parameters

        init_params = {
            'partial_color_strategy': self.partial_color_strategy_map[partial_color_strategy],
            # 'wigderson_strategy': self.wigderson_strategy_map[wigderson_strategy],
            'sdp_type': sdp_type,
            'independent_set_extraction_strategy': independent_set_extraction_strategy,
            'alg_name': alg_name,
            'partition_strategy': self.partition_strategy_map[partition_strategy],
            'normal_vectors_generation_strategy': normal_vectors_generation_strategy,
            'find_independent_sets_strategy': self.find_independent_sets_strategy_map[find_independent_sets_strategy],
            'deterministic': deterministic,
        }

        # All values are strings; needed for recursive VectorColoringAlgorithm creation
        self._literal_init_params = init_params.copy()
        self._literal_init_params['partial_color_strategy'] = partial_color_strategy
        # self._literal_init_params['wigderson_strategy'] = wigderson_strategy
        self._literal_init_params['partition_strategy'] = partition_strategy
        self._literal_init_params['find_independent_sets_strategy'] = find_independent_sets_strategy
        self._literal_init_params['deterministic'] = deterministic

        self._partially_color_strategy = lambda graph, L, colors: \
            init_params['partial_color_strategy'](graph, L, colors, init_params)

        self._wigderson_strategy = lambda graph, L, colors: \
            init_params['wigderson_strategy'](graph, L, colors, init_params, self._literal_init_params)

        self._sdp_type = sdp_type

        if alg_name is not None:
            self._name = alg_name
        else:
            self._name = "pcs: " + partial_color_strategy + " ws: " + wigderson_strategy

    def color_graph(self, graph, verbose=False):
        """Colors graph using vector coloring algorithm.

        Args:
            graph (Graph): Graph to be colored.
            verbose (bool): Set verbosity level e.g. for solver.

        Returns:
            dict: Global vertex-color dictionary indexed from 0 to graph.number_of_nodes()-1.
        """

        if graph.number_of_selfloops() > 0:
            raise Exception('Graph contains self loops')

        colors = {v: -1 for v in graph.nodes()}

        logging.info('Starting color_graph procedure on a graph with {0} vertices and {1} edges...'.format(
            graph.number_of_nodes(), graph.number_of_edges()))

        max_iterations = graph.number_of_nodes() * 2  # is it a good boundary?
        working_graph = graph.copy()

        it = 0
        while (working_graph.number_of_nodes() >= 0 and -1 in set(colors.values())) and it < max_iterations:
            it += 1
            logging.info('\nStarting iteration nr {0} of main loop...'.format(it))
            if working_graph.number_of_nodes() > 1 and working_graph.number_of_edges() > 0:
                L = compute_vector_coloring(
                    working_graph, sdp_type=self._sdp_type, verbose=verbose, iteration=it)
                # if it == 1:
                #     if self._wigderson_strategy(working_graph, colors, L):
                #         continue  # Wigderson colored some vertices so we need to recompute vector coloring
                current_nodes = working_graph.number_of_nodes()
                while working_graph.number_of_nodes() == current_nodes:
                    self._partially_color_strategy(working_graph, L, colors)
            elif working_graph.number_of_nodes() == 1:
                colors[list(working_graph.nodes())[0]] = get_lowest_legal_color(graph, list(working_graph.nodes())[0],
                                                                                colors)
                break
            elif working_graph.number_of_edges() == 0:
                new_color = max(colors.values()) + 1
                for v in working_graph.nodes():
                    colors[v] = new_color
                break
            else:
                break

        return colors

    def get_algorithm_name(self):
        return self._name


def compute_optimal_coloring_lp(graph, verbose=False):
    """Computes optimal coloring using linear programming."""

    with Model() as M:

        n = graph.number_of_nodes()

        # Variables
        x = M.variable([n, n], Domain.binary())
        w = M.variable("w", n, Domain.binary())

        # Constraints
        M.constraint('X', Expr.sum(x, 1), Domain.equalsTo(1))

        for i in range(n):
            for j in range(n):
                M.constraint('C{0}-{1}'.format(i, j), Expr.sub(x.index(i, j), w.index(j)),
                             Domain.lessThan(0.0))

        for i in range(n):
            for j in range(n):
                if i > j and has_edge_between_ith_and_jth(graph, i, j):
                    for k in range(n):
                        M.constraint('D{0}-{1}-{2}'.format(i, j, k), Expr.add(x.index(i, k), x.index(j, k)),
                                     Domain.lessThan(1.0))

        # Objective
        M.objective(ObjectiveSense.Minimize, Expr.sum(w))

        # Set solver parameters
        M.setSolverParam("numThreads", 0)

        if verbose:
            M.setLogHandler(sys.stdout)

        M.solve()

        coloring = {}

        for i, v in enumerate(sorted(list(graph.nodes()))):
            for c in range(n):
                if x.index(i, c).level() == 1.0:
                    coloring[v] = c
                    break

    return coloring


def compute_optimal_coloring_dp(graph, verbose=False):
    """Computes optimal coloring using dynamic programming."""

    t_sets = {w: [] for r in range(graph.number_of_nodes() + 1) for w in itertools.combinations(graph.nodes(), r)}
    t = {w: -1 for r in range(graph.number_of_nodes() + 1) for w in itertools.combinations(graph.nodes(), r)}  # set(w)
    t[()] = 0

    for w in t.keys():
        if len(w) == 1:
            t[w] = 1
            t_sets[w] = [w]

    for w in sorted(t.keys(), key=len):
        if len(w) <= 1:
            continue

        min_chi = graph.number_of_nodes()
        min_s = []
        subsets = [s for r in range(1, len(w) + 1) for s in itertools.combinations(w, r)]  # non-empty subsets

        for s in subsets:
            if len(s) == len(w):
                g_s = graph.subgraph(s)
                if g_s.number_of_edges() > 0:
                    continue
            else:
                if t[s] > 1:  # S is not independent
                    continue

            temp = list(set(w) - set(s))
            temp.sort()
            temp = tuple(temp)

            if t[temp] < min_chi:
                min_chi = t[temp]
                min_s = s

        t[w] = min_chi + 1
        t_sets[w] = min_s

    # Now compute the coloring
    ind_sets = []
    vertices = tuple(graph.nodes())
    while vertices:
        i_set = t_sets[vertices]
        vertices = tuple(v for v in vertices if v not in i_set)
        ind_sets.append(i_set)

    coloring = {}
    clr = -1
    for v_set in ind_sets:
        clr += 1
        for v in v_set:
            coloring[v] = clr

    return coloring

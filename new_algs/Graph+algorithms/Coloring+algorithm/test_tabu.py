import graph_tool.all as gt
import numpy as np
import sys
# import packing_coloring.graph_generator as gg
sys.path.append('..')
from packing_coloring.utils import get_distance_matrix
import packing_coloring.graph_generator.generator as gntr
from packing_coloring.algorithms.problem import GraphProblem
from packing_coloring.algorithms.perturbative.tabupackcol import partial_pack_col, react_partial_pack_col, tabu_pack_col
from packing_coloring.utils.benchmark_utils import search_step_trace
import packing_coloring.algorithms.search_space.partial_valide_col as pvc


pvc.random_ok = False
np.random.seed(10)


def benchmark_function(graphe, nbr_it, func, *func_args, **func_kwargs):

    best_sol = None
    best_score = float("inf")

    search_step_trace.env_name = func.__name__

    dist_mat = get_distance_matrix(graphe)
    prob = GraphProblem(dist_mat)

    if hasattr(graphe, "name"):
        prob.name = graphe.name

    for i in range(nbr_it):
        print(func.__name__, "#", i)

        sol = func(prob, *func_args, **func_kwargs)
        if sol.get_max_col() < best_score:
            best_sol = sol
            best_score = best_sol.get_max_col()
        search_step_trace.clear_all()

    solfname = "{0}_{1}.pcol".format(prob.name, best_sol.get_max_col())
    with open(solfname, 'a') as f:
        print(best_sol, file=f)
        print("", file=f)

    return best_sol


def graph_partcol_pcoloring(g, nbr_it):
    kwargs = {"k_count": 5, "tt_a": 20, "tt_d": 0.6,
              "max_iter": 10000, "count_max": 5}
    return benchmark_function(g, nbr_it, partial_pack_col, **kwargs)


def graph_tabu_pcoloring(g, nbr_it):
    kwargs = {"k_count": 5, "tt_a": 20, "tt_d": 0.6,
              "max_iter": 3000, "count_max": 5}
    return benchmark_function(g, nbr_it, tabu_pack_col, **kwargs)

if __name__ == "__main__":
    graphs = []
    # g = distance_graph((1, 7), 640)
    # setattr(g, "name", "D({0},{1})".format(1, 7))
    # graphs.append(g)

    # g = distance_graph((2, 5), 336)
    # setattr(g, "name", "D({0},{1})".format(2, 5))
    # graphs.append(g)

    # g = distance_graph((3, 4), 672)
    # setattr(g, "name", "D({0},{1})".format(3, 4))
    # graphs.append(g)

    # g = gt.lattice([11, 11])
    # setattr(g, "name", "G_{0}x{1}".format(11, 11))

    # g = gntr.geometric_random_graph(150, 0.5)
    # graphs.append(g)

    g = gntr.geometric_random_graph(250, 0.4)
    graphs.append(g)

    for g in graphs:

        graph_tabu_pcoloring(g, 10)
        graph_partcol_pcoloring(g, 10)

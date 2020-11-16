import graph_tool.all as gt
import numpy as np
import sys
# import packing_coloring.graph_generator as gg
sys.path.append('..')
from packing_coloring.utils import get_distance_matrix
from packing_coloring.graph_generator.generator import distance_graph
from packing_coloring.algorithms.problem import GraphProblem
from packing_coloring.algorithms.perturbative.tabupackcol import partial_pack_col, react_partial_pack_col, tabu_pack_col
from packing_coloring.algorithms.perturbative.hybrid_algo import hybrid_algorithm
from packing_coloring.algorithms.perturbative.memetic_algo import memetic_algorithm
from packing_coloring.utils.benchmark_utils import search_step_trace
from packing_coloring.algorithms.constructive.swo_algo import swo_algorithm


def benchmark_function(graphe, nbr_it, func, *func_args, **func_kwargs):
    best_sol = None
    best_score = float("inf")

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

        # tracefname = "{0}.qst".format(func.__name__)
        # with open(tracefname, 'a') as f:
        #     for name, data in sol.record.items():
        #         print(prob.name, ", ", sol.get_max_col(), ", ",
        #               search_step_trace.csv_format().format(name, data),
        #               file=f, sep="")
        #     print("", file=f)

    solfname = "{0}_{1}.pcol".format(prob.name, best_sol.get_max_col())
    with open(solfname, 'a') as f:
        print(best_sol, file=f)
        print("", file=f)

    return best_sol


def graph_hybrid_pcoloring(g, nbr_it):
    eval_func = lambda prob, a: a.get_area_score(prob)
    ls_args = {"k_count": 3, "tt_a": 20, "tt_d": 0.6,
               "max_iter": 1000, "count_max": 50}
    init_args = {"iter_count": 50, "blame_value": 25, "blame_rate": 0.85}

    kwargs = {"pop_size": 10, "nbr_gen": 10, "pool_size": 1,
              "replace_rate": 0.4, "mut_prob": 0.2,
              "local_search": partial_pack_col, "ls_args": ls_args,
              "init_heur": swo_algorithm, "init_args": init_args,
              "eval_func": eval_func}

    return benchmark_function(g, nbr_it, hybrid_algorithm, **kwargs)


def graph_memetic_pcoloring(g, nbr_it):
    eval_func = lambda prob, a: a.get_area_score(prob)
    ls_args = {"k_count": 3, "tt_a": 20, "tt_d": 0.6,
               "max_iter": 1000, "count_max": 50}
    init_args = {"iter_count": 50, "blame_value": 25, "blame_rate": 0.85}

    kwargs = {"pop_size": 10, "nbr_gen": 10, "pool_size": 1, "p_nbr": 3,
              "local_search": partial_pack_col, "ls_args": ls_args,
              "init_heur": swo_algorithm, "init_args": init_args,
              "eval_func": eval_func}

    return benchmark_function(g, nbr_it, memetic_algorithm, **kwargs)


if __name__ == "__main__":
    graphs = []
    # g = distance_graph((1, 7), 640)
    # setattr(g, "name", "D({0},{1})".format(1, 7))
    # graphs.append(g)

    g = distance_graph((2, 5), 336)
    setattr(g, "name", "D({0},{1})".format(2, 5))
    graphs.append(g)

    # g = distance_graph((3, 4), 672)
    # setattr(g, "name", "D({0},{1})".format(3, 4))
    # graphs.append(g)

    # g = gt.lattice([24, 24])
    # setattr(g, "name", "G_{0}x{1}".format(24, 24))
    # graphs.append(g)

    for g in graphs:
        graph_hybrid_pcoloring(g, 10)
        graph_memetic_pcoloring(g, 10)

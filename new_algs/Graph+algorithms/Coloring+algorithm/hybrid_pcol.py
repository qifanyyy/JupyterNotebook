#!/usr/bin/env python

from __future__ import print_function
import graph_tool.all as gt
import numpy as np

import packing_coloring.utils.benchmark_utils as bu
from packing_coloring.utils import get_distance_matrix
import packing_coloring.algorithms.search_space.partial_valide_col as pvc
import packing_coloring.graph_generator as gntr
from packing_coloring.algorithms import GraphProblem
from packing_coloring.algorithms.constructive import rlf_algorithm
from packing_coloring.algorithms.constructive import swo_algorithm
from packing_coloring.algorithms.perturbative import partial_pack_col, react_partial_pack_col, tabu_pack_col
from packing_coloring.algorithms.perturbative import hybrid_algorithm

import argparse


def benchmark_function(graphe, func, *func_args, **func_kwargs):
    dist_mat = get_distance_matrix(graphe)
    prob = GraphProblem(dist_mat)

    if hasattr(graphe, "name"):
        prob.name = graphe.name
    if bu.search_step_trace.enabled:
        bu.search_step_trace.env_name = func.__name__

    sol = func(prob, *func_args, **func_kwargs)

    return prob, sol


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='specify a candidate through parameters')

    parser.add_argument('instance', type=str)
    parser.add_argument('--seed', dest='seed',
                        type=int, default=None)
    parser.add_argument('--enable_trace', dest='enable_trace',
                        action="store_true")
    parser.add_argument('--print_sol', dest='print_sol',
                        action="store_true")
    parser.add_argument('--trace_path', dest='trace_path',
                        type=str, default='')
    parser.add_argument('--rand_init', dest='rand_init',
                        action="store_true")

    parser.add_argument('--pop_size', dest='pop_size',
                        type=int, required=True)
    parser.add_argument('--nbr_gen', dest='nbr_gen',
                        type=int, required=True)
    parser.add_argument('--pool_size', dest='pool_size',
                        type=int, required=True)
    parser.add_argument('--replace_rate', dest='replace_rate',
                        type=float, required=True)
    parser.add_argument('--mut_prob', dest='mut_prob',
                        type=float, required=True)

    parser.add_argument('--init_pop', dest='init_pop',
                        type=int, required=True)
    parser.add_argument('--crossover', dest='crossover',
                        type=int, required=True)
    parser.add_argument('--local_search', dest='local_search',
                        type=int, required=True)
    # parser.add_argument('--constructive', dest='constructive',
    #                     type=int, required=True)
    parser.add_argument('--duration', dest='duration',
                        type=int, default=20)

    eval_func = lambda prob, a: a.get_area_score(prob)

    ls_methodes = [partial_pack_col,
                   react_partial_pack_col,
                   tabu_pack_col]
    ls_args = [{"k_count": 3, "tt_a": 90, "tt_d": 0.1, "max_iter": 1000, "count_max": 5},
               {"k_count": 3, "tt_a": 20, "tt_d": 0.6, "max_iter": 100, "iter_period": 130, "tenure_inc": 75},
               {"k_count": 3, "tt_a": 80, "tt_d": 1., "max_iter": 250, "count_max": 160}]

    init_methodes = [rlf_algorithm]
    init_args = [{}]

    args = parser.parse_args()

    if args.seed is not None:
        np.random.seed(args.seed)
    pvc.random_ok = args.rand_init
    bu.search_step_trace.enabled = args.enable_trace
    bu.search_step_trace.dir_path = args.trace_path

    g = gt.load_graph(args.instance)
    kwargs = {"pop_size": args.pop_size,
              "nbr_gen": args.nbr_gen,
              "pool_size": args.pool_size,
              "replace_rate": args.replace_rate,
              "mut_prob": args.mut_prob,
              "local_search": ls_methodes[0],
              "ls_args": ls_args[0],
              "init_heur": init_methodes[0],
              "init_args": init_args[0],
              "eval_func": eval_func,
              "init_methode": args.init_pop,
              "crossover_methode": args.crossover,
              "duration": args.duration}

    prob, sol = benchmark_function(g, hybrid_algorithm, **kwargs)
    print(sol.get_max_col())

    if args.print_sol:
        solfname = "{0}_{1}.pcol".format(prob.name, sol.get_max_col())
        with open(solfname, 'a') as f:
            print(sol, file=f)
            print("", file=f)

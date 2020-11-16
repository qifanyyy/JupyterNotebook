#!/usr/bin/env python

from __future__ import print_function
import graph_tool.all as gt
import numpy as np

import packing_coloring.utils.benchmark_utils as bu
from packing_coloring.utils import get_distance_matrix
import packing_coloring.algorithms.search_space.partial_valide_col as pvc
import packing_coloring.graph_generator as gntr
from packing_coloring.algorithms import GraphProblem
from packing_coloring.algorithms.perturbative import partial_pack_col
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
    parser.add_argument('--k_count', dest='k_count',
                        type=int, required=True)
    parser.add_argument('--tt_a', dest='tt_a',
                        type=int, required=True)
    parser.add_argument('--tt_d', dest='tt_d',
                        type=float, required=True)
    parser.add_argument('--max_iter', dest='max_iter',
                        type=int, required=True)
    parser.add_argument('--count_max', dest='count_max',
                        type=int, required=True)
    parser.add_argument('--duration', dest='duration',
                        type=int, default=20)

    args = parser.parse_args()

    if args.seed is not None:
        np.random.seed(args.seed)
    pvc.random_ok = args.rand_init
    bu.search_step_trace.enabled = args.enable_trace
    bu.search_step_trace.dir_path = args.trace_path

    g = gt.load_graph(args.instance)
    kwargs = {"k_count": args.k_count,
              "tt_a": args.tt_a,
              "tt_d": args.tt_d,
              "max_iter": args.max_iter,
              "count_max": args.count_max,
              "duration": args.duration}

    prob, sol = benchmark_function(g, partial_pack_col, **kwargs)
    print(sol.get_max_col())

    if args.print_sol:
        solfname = "{0}_{1}.pcol".format(prob.name, sol.get_max_col())
        with open(solfname, 'a') as f:
            print(sol, file=f)
            print("", file=f)

# -*- coding: utf-8 -*-
from __future__ import print_function

import numpy as np
import numpy.random as rd

from packing_coloring.algorithms.solution import PackColSolution
from packing_coloring.algorithms.constructive.neighborhood.random import random_order
from packing_coloring.algorithms.constructive.neighborhood.closeness import closeness_order
from packing_coloring.algorithms.constructive.neighborhood.betweenness import betweenness_order
from packing_coloring.algorithms.constructive.greedy_algo import greedy_algorithm
from packing_coloring.algorithms.constructive.rlf_algo import rlf_algorithm
from packing_coloring.utils.benchmark_utils import set_env, search_step_trace


# Squeaky Wheel Optimizer
def swo_algorithm(prob, iter_count=500, blame_value=25, blame_rate=0.85, random_init=True):
    if random_init:
        priority_seq = random_order(prob)
    else:
        priority_seq = (rlf_algorithm(prob)).get_greedy_order()

    best_score = float("inf")
    best_sol = None
    for i in np.arange(iter_count):
        cur_sol = greedy_algorithm(prob, priority_seq)
        cur_score = cur_sol.get_max_col()
        # print(cur_score)

        if cur_score < best_score:
            best_sol = cur_sol.copy()
            best_score = best_sol.get_max_col()
            priority_seq = best_sol.get_greedy_order()
            blame_treshold = np.ceil(blame_rate * min(best_score, prob.get_diam()))

        b_v = blame_value + abs(cur_score - blame_treshold)
        blame = np.zeros(prob.v_size, dtype=int)
        for v in np.arange(prob.v_size):
            if cur_sol[v] > blame_treshold:
                # blame[v] += max(b_v, cur_sol.pack_size(cur_sol[v]-1))
                # blame[v] += np.ceil(blame_value * (1 + (cur_sol[v] / cur_score)))
                blame[v] += b_v

        prior_blame = blame[priority_seq]
        order = (-prior_blame, np.arange(prob.v_size) - prior_blame)
        priority_seq = priority_seq[np.lexsort(order)]

    return best_sol


def aics_algorithm(prob, iter_count=200, random_init=True):
    if random_init:
        best_sol = greedy_algorithm(prob, random_order(prob))
    else:
        best_sol = rlf_algorithm(prob)

    best_score = best_sol.get_max_col()
    mean_score = best_score
    # print(best_sol, "->", best_score)
    blame = best_sol[:]
    # print(blame, "\n")

    permut = np.arange(1, best_sol.get_max_col()+1, dtype=int)
    permut = rd.permutation(permut)
    priority_seq = best_sol.get_by_permut(permut)
    for i in np.arange(1, iter_count+1):
        # The Constructor
        cur_sol = greedy_algorithm(prob, priority_seq)
        cur_score = cur_sol.get_max_col()
        # print(np.round(mean_score, decimals=2), cur_score)

        # The Analyzer
        if cur_score >= np.floor(mean_score):
            w = [mean_score, cur_score]
            blame = np.average([cur_sol[:], blame], axis=0, weights=w)
            permut = np.arange(1, cur_sol.get_max_col()+1, dtype=int)
            permut = rd.permutation(permut)
            priority_seq = cur_sol.get_by_permut(permut)
        else:
            if cur_score < best_score:
                best_sol = cur_sol
                best_score = best_sol.get_max_col()
            blame = np.average([cur_sol[:], blame], axis=0)
            priority_seq = np.arange(prob.v_size)[np.argsort(blame)]

        mean_score = (mean_score*(3./4)) + (cur_score*(1./4))

        # print(np.round(blame, decimals=2), "\n")

        # The Prioritizer

    return best_sol

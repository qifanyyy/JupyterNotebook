# -*- coding: utf-8 -*-
from __future__ import print_function

import numpy as np
import numpy.random as rd
import time
import logging

from packing_coloring.algorithms.search_space.complete_illegal_col import *
from packing_coloring.algorithms.search_space.partial_valide_col import *
from packing_coloring.algorithms.solution import *
from packing_coloring.algorithms.constructive.rlf_algo import rlf_algorithm
from packing_coloring.utils.benchmark_utils import trace, print_trace


def update_fitness(prob, sol, fitness, colors, vertex, col):
    vertices = np.arange(prob.v_size)
    prev_col = sol[vertex]

    old_range = vertices[prob[vertex] <= prev_col]
    for v in old_range:
        if sol[v] != prev_col:
            fitness[v, prev_col-1] -= 1
        elif v != vertex:
            for i, c in enumerate(colors):
                if c != prev_col:
                    fitness[v, i] += 1
                fitness[vertex, i] += 1

    new_range = vertices[prob[vertex] <= col]
    for v in new_range:
        if sol[v] != col and v != vertex:
            fitness[v, col-1] += 1
        elif sol[v] == col:
            for i, c in enumerate(colors):
                if c != col:
                    fitness[v, i] -= 1
                fitness[vertex, i] -= 1

    fitness[vertex, col-1] = 0
    return fitness


def init_fitness(prob, sol, colors):
    vertices = np.arange(prob.v_size)
    fitness = np.zeros((prob.v_size, len(colors)), dtype=int)

    for v in vertices:
        v_col = sol[v]
        add_conf = np.logical_and(sol != v_col, prob[v] <= v_col)
        for u in vertices[add_conf]:
            fitness[u, v_col-1] += 1
        del_conf = (np.sum(np.logical_and(sol == v_col, prob[v] <= v_col)) - 1)
        for i, c in enumerate(colors):
            if c != v_col:
                fitness[v, i] -= del_conf
    return fitness


@trace
def tabu_kpack_col(prob, k_col, sol=None, tt_a=10,
                   tt_d=0.5, max_iter=1000, count_max=10):
    colors = np.arange(1, k_col+1)
    tabu_list = np.zeros((prob.v_size, k_col), dtype=int)

    if sol is None:
        sol = rlf_algorithm(prob)
    if k_col < prob.get_diam():
        sol[sol > k_col] = rd.randint(1, k_col+1, len(sol[sol > k_col]))
    else:
        sol[sol > prob.get_diam()] = rd.randint(
            1, k_col+1, len(sol[sol > prob.get_diam()]))
    best_sol = sol.copy()

    fitness = init_fitness(prob, sol, colors)
    best_score = score = count_conflicting_edge(prob, sol)
    count_iter = count_slope = 0
    while score > 0 and count_iter < max_iter:
        vertex, col = best_one_exchange(prob, sol, fitness, score,
                                        best_score, colors, tabu_list)
        prev_col = sol[vertex]

        if col == 0:
            logging.warning("tabue list too large")
            break

        prev_score = score
        score += fitness[vertex, col-1]
        fitness = update_fitness(prob, sol, fitness, colors, vertex, col)
        sol[vertex] = col

        if score == prev_score:
            count_slope += 1
        else:
            count_slope = 0

        tabu_list = tabu_list - 1
        tabu_list[tabu_list < 0] = 0
        tabu_list[vertex, prev_col-1] = (rd.randint(tt_a) +
                                         (2 * tt_d * score * col) +
                                         np.ceil(float(count_slope)/count_max))

        if score < best_score:
            best_score = score
            best_sol = sol.copy()

        count_iter += 1

    return best_sol


def tabu_pack_col(prob, k_count=3, sol=None, tt_a=10, tt_d=0.5,
                  max_iter=1000, count_max=10, duration=30):
    end_time = time.time()+(duration*60)

    if sol is None:
        sol = rlf_algorithm(prob)
    best_sol = sol.copy()

    k_lim = sol.get_max_col()
    k_col = k_lim - 1
    count = 0
    while count < k_count:
        logging.warning("{0}: {1}, {2}".format(count, k_col, k_lim))
        sol = tabu_kpack_col(prob, k_col, sol,
                             tt_a, tt_d, max_iter, count_max)
        new_score = count_conflicting_edge(prob, sol)
        max_col = sol.get_max_col()
        if max_col >= k_lim:
            count += 1
        if new_score == 0:
            if max_col < best_sol.get_max_col():
                count = 0
                k_lim = k_col
                best_sol = sol.copy()
                print_trace(prob, best_sol)

            k_col = max_col - 1
        else:
            k_col = max_col + 1

        if time.time() >= end_time:
            logging.warning("time stop!")
            break

    return best_sol


def prepare_sol(prob, k_col, max_iter, sol=None):
    has_pillars = False
    tabu_list = np.zeros((prob.v_size, k_col), dtype=int)

    if sol is None:
        sol = rlf_algorithm(prob)
    elif np.any(sol == 0):
        has_pillars = True

    sol[sol >= k_col] = 0
    diam = prob.get_diam()
    if k_col >= diam:
        sol[sol >= diam] = 0

    if has_pillars:
        logging.warning("has pillars")
        # tabu_list[sol != 0] = max_iter + 1
        for v in np.arange(prob.v_size)[sol != 0]:
            v_col = sol[v]
            influences = (prob.dist_matrix[v] <= v_col).A1
            tabu_list[influences, v_col-1] = max_iter + 1
    else:
        nbr_to_reach = np.ceil(float(prob.v_size) / k_col)
        nbr_yet = np.sum(sol == 0)
        if nbr_to_reach > nbr_yet:
            mask = np.arange(prob.v_size)[sol != 0]
            nbr = nbr_to_reach - nbr_yet
            proba = sol[mask].astype(float) / k_col
            proba = proba / np.sum(proba)
            sample = rd.choice(mask, nbr, replace=False, p=proba)
            sol[sample] = 0

    return sol, tabu_list


@trace
def partial_kpack_col(prob, k_col, sol=None, tt_a=10, tt_d=0.6,
                      max_iter=1000, count_max=10):
    if k_col >= sol.get_max_col() and sol.count_uncolored() == 0:
        k_col = sol.get_max_col() - 1
    sol, tabu_list = prepare_sol(prob, k_col, max_iter, sol)
    colors = np.arange(1, k_col+1)

    best_sol = sol.copy()
    best_score = score = sol.count_uncolored()

    if score == 0:
        logging.warning("no challenge men! {0}".format(k_col - sol.get_max_col()))

    count_iter = count_slope = 0
    while score > 0 and count_iter <= max_iter:
        vertex, col, conflicts = best_i_swap(prob, sol, best_score,
                                             colors, tabu_list)
        if vertex == -1:
            logging.warning("tabue list too large")
            break
        sol[conflicts] = 0
        sol[vertex] = col
        prev_score = score
        score = sol.count_uncolored()
        if score == prev_score:
            count_slope += 1
        else:
            count_slope = 0

        if score < best_score:
            best_score = score
            best_sol = sol.copy()

        tabu_list = tabu_list - 1
        tabu_list[tabu_list < 0] = 0
        for v in np.arange(prob.v_size)[conflicts]:
            tabue_tenure = (rd.randint(tt_a) + (2 * tt_d * score * col) +
                            np.ceil(float(count_slope)/count_max))
            tabu_list[v, col-1] = tabue_tenure

        count_iter += 1

    if np.any(best_sol == 0):
        best_sol = rlf_algorithm(prob, best_sol)

    return best_sol


def partial_pack_col(prob, k_count=3, sol=None, start_col=None, count_max=10,
                     tt_a=10, tt_d=0.6, max_iter=1000, duration=30):
    end_time = time.time()+(duration*60)

    if sol is None:
        sol = rlf_algorithm(prob)
    elif start_col is not None:
        logging.warning("get start col: {0}".format(start_col))
        sol = partial_kpack_col(prob, start_col, sol=sol, tt_a=tt_a, tt_d=tt_d,
                                max_iter=max_iter, count_max=count_max)
    best_sol = sol.copy()

    k_lim = sol.get_max_col()
    k_col = k_lim - 1
    count = 0
    while count < k_count:
        logging.warning("{0}: {1}, {2}".format(count, k_col, k_lim))
        sol = partial_kpack_col(prob, k_col, sol=sol, tt_a=tt_a, tt_d=tt_d,
                                max_iter=max_iter, count_max=count_max)

        max_col = sol.get_max_col()
        if max_col <= k_col:
            if max_col < best_sol.get_max_col():
                count = 0
                k_lim = max_col
                best_sol = sol.copy()
                print_trace(prob, best_sol)
            k_col = max_col - 1
        else:
            k_col = max_col + 1
        if k_col >= k_lim:
            count += 1

        if time.time() >= end_time:
            break

    return best_sol


@trace
def react_partial_kpack_col(prob, k_col, sol=None, tt_a=10, tt_d=0.6,
                            max_iter=1000, iter_period=100, tenure_inc=5):

    if k_col >= sol.get_max_col() and sol.count_uncolored() == 0:
        k_col = sol.get_max_col() - 1
    sol, tabu_list = prepare_sol(prob, k_col, max_iter, sol)
    colors = np.arange(1, k_col+1)

    best_sol = sol.copy()
    best_score = score = sol.count_uncolored()

    if score == 0:
        logging.warning("no challenge men! {0}".format(k_col - sol.get_max_col()))

    min_score = float('inf')
    max_score = 0
    tt = tt_a
    iter_count = 1
    while score > 0 and iter_count <= max_iter:
        vertex, col, conflicts = best_i_swap(prob, sol, best_score,
                                             colors, tabu_list)
        if vertex == -1:
            logging.warning("tabue list too large")
            break
        sol[conflicts] = 0
        sol[vertex] = col
        score = sol.count_uncolored()
        if score < min_score:
            min_score = score
        if score > max_score:
            max_score = score
        if iter_count % iter_period == 0:
            delta = max_score - min_score
            if delta < 1:
                tt = tt + tenure_inc
            else:
                tt = tt - 1
                if tt < tt_a:
                    tt = tt_a
            min_score = float('inf')
            max_score = 0

        if score < best_score:
            best_score = score
            best_sol = sol.copy()

        tabu_list = tabu_list - 1
        tabu_list[tabu_list < 0] = 0
        for v in np.arange(prob.v_size)[conflicts]:
            tabue_tenure = rd.randint(tt) + (2 * tt_d * score * col)
            tabu_list[v, col-1] = tabue_tenure

        iter_count += 1

    if np.any(best_sol == 0):
        best_sol = rlf_algorithm(prob, best_sol)

    return best_sol


def react_partial_pack_col(prob, k_count=3, sol=None, start_col=None, tt_a=10,
                           tt_d=0.6, iter_period=100, tenure_inc=5,
                           max_iter=1000, duration=30):
    end_time = time.time()+(duration*60)

    if sol is None:
        sol = rlf_algorithm(prob)
    elif start_col is not None:
        logging.warning("get start col: {0}".format(start_col))
        sol = react_partial_kpack_col(
            prob, start_col, sol=sol, tt_a=tt_a, tt_d=tt_d,
            max_iter=max_iter, iter_period=iter_period, tenure_inc=tenure_inc)
    best_sol = sol.copy()

    k_lim = sol.get_max_col()
    k_col = k_lim - 1
    count = 0
    while count < k_count:
        logging.warning("{0}: {1}, {2}".format(count, k_col, k_lim))
        sol = react_partial_kpack_col(
            prob, k_col, sol=sol, tt_a=tt_a, tt_d=tt_d,
            max_iter=max_iter, iter_period=iter_period, tenure_inc=tenure_inc)
        max_col = sol.get_max_col()
        if max_col >= k_lim:
            count += 1
        if max_col <= k_col:
            if max_col < best_sol.get_max_col():
                count = 0
                k_lim = k_col
                best_sol = sol.copy()
                print_trace(prob, best_sol)
            k_col = max_col - 1

        if time.time() >= end_time:
            break

    return best_sol

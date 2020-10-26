# -*- coding: utf-8 -*-
from __future__ import print_function

import numpy as np
import sympy as sp
import numpy.random as rd
import math

from packing_coloring.algorithms.solution import *
from packing_coloring.algorithms.search_space.partial_valide_col import *


def non_coloured(sol):
    return np.sum(sol.uncolored())


def free_for_colour(prob, sol, k_col):
    return np.sum(k_colorable_set(prob, sol, k_col))


def give_k_colorable_set(prob, sol, k_col):
    return np.arange(prob.v_size)[k_colorable_set(prob, sol, k_col)]


def plant_colour(prob, sol, k_col, temp_t, k):
    pattern_l = sol.copy()

    while free_for_colour(prob, pattern_l,  k_col) > 0:
        v = None
        f_v = float("inf")

        choosable = give_k_colorable_set(prob, pattern_l, k_col)
        for i in range(k):
            w = rd.choice(choosable)
            w_colored = pattern_l.copy()
            w_colored[w] = k_col
            f_w = (free_for_colour(prob, pattern_l, k_col) -
                   free_for_colour(prob, w_colored, k_col))

            if rd.random() < sp.N(sp.exp((f_v - f_w)/temp_t)):
                f_v = f_w
                v = w

        if v is not None:
            pattern_l[v] = k_col

    return pattern_l


def sa_algorithm(prob, t_max, t_min, q, k):
    best_patterns = []
    pattern_k = PackColSolution(prob)
    best_patterns.append(pattern_k)

    color_c = 1
    while non_coloured(best_patterns[0]) > 0:
        new_patterns = []
        p = non_coloured(pattern_k)
        m = 0
        for pattern in best_patterns:
            temp = t_max
            while temp > t_min:
                pattern_t = plant_colour(prob, pattern, color_c, temp, k)
                a = p - non_coloured(pattern_t)

                if a >= m:
                    if a > m:
                        new_patterns = []
                        m = a
                    if pattern_t not in new_patterns:
                        new_patterns.append(pattern_t)

                temp = temp * q

        best_patterns = new_patterns

        # print("Patterns after building the color", color_c, "packing")
        # for pattern in best_patterns:
        #     print(pattern)
        # print('\n')

        color_c += 1

    return best_patterns[0]

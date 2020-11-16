# -*- coding: utf-8 -*-
from __future__ import print_function

import numpy as np
from packing_coloring.algorithms.search_space.partial_valide_col import *
from packing_coloring.algorithms.solution import *
from packing_coloring.utils.benchmark_utils import trace, print_trace


def rlf_algorithm(prob, sol=None):
    if sol is not None:
        coloring = sol.copy()
    else:
        coloring = PackColSolution(prob)

    # The coloring is done by constructing the k-packing
    k_col = 1
    while not coloring.is_complete():
        while np.any(k_colorable_set(prob, coloring, k_col)):
            v = partition_next_vertex(prob, coloring, k_col)
            coloring[v] = k_col

        k_col += 1

    return coloring

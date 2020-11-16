from __future__ import print_function

import numpy as np
import numpy.random as rd
import time

from packing_coloring.algorithms.search_space.complete_illegal_col import *
from packing_coloring.algorithms.solution import *
from packing_coloring.algorithms.problem import *
from packing_coloring.algorithms.constructive.rlf_algo import rlf_algorithm
from packing_coloring.algorithms.constructive.greedy_algo import greedy_algorithm


def pertub(prob, sol, heuristic, local_search):
    bounds = np.zeros(prob.v_size, dtype=int)
    for i in range(sol.v_size):
        i_col = sol[i]
        bound = np.sum(prob.dist_matrix[i] == i_col)
        bounds[i] = bound

    v = np.argmax(bounds)
    adj_mat = (prob.dist_matrix == 1)
    changes = (prob.dist_matrix[v] == sol[v])
    adj_mat[v] = changes
    adj_mat[..., v] = np.transpose(changes)
    new_prob = GraphProblem(adj_mat)
    new_sol = heuristic(new_prob)
    new_sol = local_search(new_prob, sol=new_sol, duration=5)
    return greedy_algorithm(prob, new_sol.get_greedy_order())


def ils_algorithm(prob, heuristic, local_search, sol=None, max_iter=100):
    if sol is None:
        sol = heuristic(prob)

    sol = local_search(prob, sol=sol, duration=5)
    score = sol.get_max_col()
    best_sol = sol
    best_score = score
    print(score)

    while max_iter > 0:
        new_sol = pertub(prob, sol, heuristic, local_search)
        new_sol = local_search(prob, sol=new_sol, k_count=1, max_iter=100, duration=5)
        new_score = new_sol.get_max_col()
        print(new_score)

        if new_score < best_score:
            best_sol = new_sol
            best_score = new_score

        sol = new_sol

    return best_sol

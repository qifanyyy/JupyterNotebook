from __future__ import print_function

import numpy as np
import numpy.random as rd
import time
import logging

from packing_coloring.algorithms.search_space.complete_illegal_col import *
from packing_coloring.algorithms.solution import *
from packing_coloring.algorithms.problem import *
from packing_coloring.algorithms.perturbative.tabupackcol import *
from packing_coloring.algorithms.constructive.rlf_algo import rlf_algorithm
from packing_coloring.algorithms.constructive.greedy_algo import greedy_algorithm


def generate_population(prob, size, heuristic, init_args):
    logging.info("Init population by permut")
    pop = []
    indiv = heuristic(prob, **init_args)
    permut = np.arange(1, indiv.get_max_col()+1, dtype=int)
    pop.append(indiv)
    logging.info("init candidate 0: " + str(indiv.get_max_col()))
    for i in range(1, size):
        new_permut = rd.permutation(permut)
        priority = indiv.get_by_permut(new_permut)
        pop.append(greedy_algorithm(prob, priority))
        logging.info("init candidate " + str(i) + ": " + str(pop[i].get_max_col()))
    return pop


def generate_population2(prob, size, heuristic, init_args):
    logging.info("Init population by random order")
    pop = []
    for i in range(size):
        indiv = heuristic(prob, **init_args)
        pop.append(indiv)
        logging.info("init candidate " + str(i) + ": " + str(pop[i].get_max_col()))
    return pop


def selection(pop, pool_size=2):
    # Tournament Selection
    indices = np.arange(len(pop), dtype=int)
    best = rd.choice(indices, 1)[0]

    for i in range(pool_size):
        adv = rd.choice(np.delete(indices, best), 1)[0]
        if pop[adv] < pop[best]:
            best = adv
    logging.info("Tournament select -> " + str(best))
    return pop[best]


def choose_parents(pop, nbr, pool_size):
    logging.info("Parents selection")
    pop_indices = np.arange(len(pop), dtype=int)
    parents_i = []
    for i in range(min(nbr, len(pop))):
        pi = selection(np.delete(pop_indices, parents_i), pool_size)
        parents_i.append(pi)
    parents = [pop[i] for i in parents_i]

    return parents


def crossover(prob, sols, k_col, local_search, ls_args):
    logging.info("Crossover pillars")
    if len(sols) < 2:
        logging.error("Not enough parents!")
        return None

    common_base = sols[0].copy()
    for p in sols[1:]:
        common_base[common_base[:] != p[:]] = 0
    common_base[common_base[:] >= k_col] = 0
    logging.info("percent of pillars: " +
                 str(np.sum(common_base[:] != 0)/prob.v_size))
    child = local_search(prob, sol=common_base, start_col=k_col, **ls_args)
    return child


@trace
def update_population(prob, pop, eval_func, nbr_gen=None):
    logging.info("Update")
    area_val = []
    pcol_val = []
    for s in pop:
        area_val.append(eval_func(prob, s))
        pcol_val.append(s.get_max_col())
    order = np.lexsort((np.array(area_val), np.array(pcol_val)))
    pop = [pop[i] for i in order]

    logging.info("Population scores: \n" +
                 str(np.array([[i, j] for i, j in zip(pcol_val, area_val)])[order]) +
                 "\n")
    return pop


def memetic_algorithm(prob, pop_size, nbr_gen, pool_size,
                      breeding_rate, local_search, ls_args, init_heur,
                      init_args, eval_func, init_methode, duration):
    end_time = time.time()+(duration*60)

    init_pops = [generate_population,
                 generate_population2]
    init_pop = init_pops[init_methode]

    pop = init_pop(prob, pop_size, init_heur, init_args)
    pop = update_population(prob, pop, eval_func)

    p_nbr = max(min(int(np.ceil(pop_size*breeding_rate)), pop_size-1), 2)

    best_sol = pop[0]
    best_score = best_sol.get_max_col()
    for i in range(nbr_gen):
        logging.info("############### generation " + str(i) + " ################")
        parents = choose_parents(pop, p_nbr, pool_size)
        child = crossover(prob, parents, best_sol.get_max_col()-1,
                          local_search, ls_args)
        pop.append(child)
        pop = update_population(prob, pop, eval_func)
        pop = pop[:pop_size]

        if pop[0].get_max_col() < best_score:
            best_sol = pop[0]
            best_score = best_sol.get_max_col()

        if time.time() >= end_time:
            logging.warning("time stop!")
            break

    return best_sol

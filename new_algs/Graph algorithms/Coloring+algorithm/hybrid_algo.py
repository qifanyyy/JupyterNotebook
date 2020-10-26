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
from packing_coloring.utils.benchmark_utils import trace, print_trace


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
        new_indiv = greedy_algorithm(prob, priority)
        pop.append(new_indiv)
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

@trace
def selection(pop, tournament_size=2):
    # Tournament Selection
    indices = np.arange(len(pop), dtype=int)
    best = rd.choice(indices, 1)[0]

    for i in range(tournament_size):
        adv = rd.choice(np.delete(indices, best), 1)[0]
        if pop[adv] < pop[best]:
            best = adv
    logging.info("Tournament select -> " + str(best))
    return pop[best]


@trace
def choose_parents(pop, nbr, tournament_size):
    logging.info("Parents selection")
    pop_indices = np.arange(len(pop), dtype=int)
    parents_i = []
    for i in range(min(nbr, len(pop))):
        pi = selection(np.delete(pop_indices, parents_i), tournament_size)
        parents_i.append(pi)
    parents = [pop[i] for i in parents_i]
    return parents


@trace
def crossover_permut(prob, sols):
    logging.info("Crossover stupid and easy")
    p1 = sols[0].get_greedy_order()
    p2 = sols[1].get_greedy_order()
    child_permut = p1
    chrom_size = np.floor(len(child_permut)/2)
    to_change = rd.choice(np.arange(prob.v_size), chrom_size, replace=False)
    deleted = child_permut[to_change]
    replacing = np.intersect1d(p2, deleted)
    child_permut[to_change] = replacing
    return greedy_algorithm(prob, child_permut)


@trace
def crossover_cx(prob, sols):
    logging.info("Crossover cycle")
    p1 = sols[0].get_greedy_order()
    p2 = sols[1].get_greedy_order()
    child1 = np.zeros(prob.v_size, dtype=int)
    child2 = np.zeros(prob.v_size, dtype=int)

    positions = np.arange(prob.v_size, dtype=int)
    order1 = np.argsort(p1)
    inplace = p1 == p2
    child1[inplace] = p1[inplace]
    child2[inplace] = p2[inplace]
    positions[inplace] = -1

    cycle_nbr = 0
    while np.any(positions != -1):
        cycle = [np.argmax(positions > -1)]

        while p1[cycle[0]] != p2[cycle[-1]]:
            step = p2[cycle[-1]]
            pos = order1[step]
            cycle.append(pos)
        positions[cycle] = -1

        if cycle_nbr % 2 == 0:
            child1[cycle] = p1[cycle]
            child2[cycle] = p2[cycle]
        else:
            child1[cycle] = p2[cycle]
            child2[cycle] = p1[cycle]
        cycle_nbr += 1

    sol1 = greedy_algorithm(prob, child1)
    sol2 = greedy_algorithm(prob, child2)
    if sol1.get_max_col() <= sol2.get_max_col():
        return sol1
    else:
        return sol2


@trace
def crossover_cover(prob, sols):
    logging.info("Crossover cover")
    diff_rate = np.sum(np.equal(sols[0][:], sols[1][:]))/prob.v_size
    child = PackColSolution(prob)
    diam = prob.get_diam()
    max_pack = min(diam-1, sols[0].get_max_col(), sols[1].get_max_col()) - 1
    max_pack = int(np.ceil(max_pack * (1. - diff_rate)))
    sol1_packing = sols[0].get_partitions()[:max_pack]
    sol2_packing = sols[1].get_partitions()[:max_pack]

    for i in range(max_pack-1):
        new_packing = None
        if (i % 2) == 1:
            sol_packing = sol1_packing
        else:
            sol_packing = sol2_packing

        scores = np.zeros(max_pack, dtype=float)
        for col in np.arange(1, max_pack):
            kcol_nodes = sol_packing[col]
            dist_mat = prob.dist_matrix[kcol_nodes]
            cover_score = np.sum(dist_mat <= col)
            cover_score -= np.sum(kcol_nodes)
            scores[col] = cover_score

        new_col = np.argmax(scores)
        # scores[scores == 0] = float("inf")
        # new_col = np.argmin(scores)
        new_packing = np.copy(sol_packing[new_col])
        child[new_packing] = new_col

        sol1_packing[..., new_packing] = False
        sol2_packing[..., new_packing] = False
        sol1_packing[new_col] = False
        sol2_packing[new_col] = False

    if np.any(child == 0):
        child = rlf_algorithm(prob, child)

    if count_conflicting_edge(prob, child) > 0:
        logging.error("Crossover cover -> Fail !")

    return child


@trace
def crossover_area(prob, sols):
    logging.info("Crossover area")
    child = PackColSolution(prob)
    diam = prob.get_diam()
    diff_rate = np.sum(np.equal(sols[0][:], sols[1][:]))/prob.v_size
    max_pack = min(diam-1, sols[0].get_max_col(), sols[1].get_max_col()) - 1
    max_pack = int(np.ceil(max_pack * diff_rate))
    sol1_packing = sols[0].get_partitions()[:max_pack]
    sol2_packing = sols[1].get_partitions()[:max_pack]

    logging.info("difference rate " + str(diff_rate))
    for i in range(max(2, max_pack-1)):
        new_packing = None
        sol_packing = None
        if (i % 2) == 0:
            sol_packing = sol1_packing
        else:
            sol_packing = sol2_packing

        if np.sum(sol_packing) <= 0:
            break

        scores = np.zeros(max_pack, dtype=float)
        for col in np.arange(1, max_pack-1):
            kcol_nodes = sol_packing[col]
            if np.sum(kcol_nodes) > 0:
                dist_mat = prob.dist_matrix.A
                kcol_dist = dist_mat[kcol_nodes]

                first_half = np.floor(float(col)/2)
                half_nodes = kcol_dist <= first_half
                # half_nodes[dist_mat == 0] = False
                area_score = np.sum(half_nodes)
                if col % 2 == 1:
                    border = np.ceil(float(col)/2)
                    for x in np.arange(prob.v_size)[kcol_nodes]:
                        x_dist = dist_mat[x]
                        x_half_nodes = (x_dist <= first_half)
                        border_nodes = (x_dist == border)
                        for y in np.arange(prob.v_size)[border_nodes]:
                            y_neighbors = (dist_mat[y] == 1)
                            common = np.logical_and(y_neighbors, x_half_nodes)
                            area_score += (float(np.sum(common)) /
                                           np.sum(y_neighbors))
                # area_score = area_score/np.sum(kcol_nodes)
                scores[col] = area_score

        new_col = np.argmax(scores)
        # scores[scores == 0] = float("inf")
        # new_col = np.argmin(scores)
        new_packing = np.copy(sol_packing[new_col])
        child[new_packing] = new_col

        sol1_packing[..., new_packing] = False
        sol2_packing[..., new_packing] = False
        sol1_packing[new_col] = False
        sol2_packing[new_col] = False

    # colors = np.copy(np.unique(child[:]))
    # for i, j in enumerate(colors):
    #     if i < j:
    #         child[child == j] = i

    if np.any(child == 0):
        child = rlf_algorithm(prob, child)

    if count_conflicting_edge(prob, child) > 0:
        logging.error("Crossover area -> Fail !")

    return child


@trace
def mutation(prob, sol, local_search, ls_args):
    logging.info("Mutation")
    diam = prob.get_diam()
    bounds = np.zeros(prob.v_size, dtype=int)
    for i in range(sol.v_size):
        i_col = min(sol[i], diam - 1) + 1
        bound = np.sum(prob.dist_matrix[i] == i_col)
        bounds[i] = bound

    v = np.argmax(bounds)
    v_col = min(sol[v], diam - 1) + 1
    adj_mat = (prob.dist_matrix == 1)
    # changes = (prob.dist_matrix[v] == v_col)
    changes = np.logical_or((prob.dist_matrix[v] == v_col), adj_mat[v])
    adj_mat[v] = changes
    adj_mat[..., v] = np.transpose(changes)
    new_prob = GraphProblem(adj_mat)
    new_sol = PackColSolution(new_prob)
    new_sol = rlf_algorithm(new_prob)
    new_sol = local_search(new_prob, sol=new_sol, **ls_args)

    # mutated = PackColSolution(prob)
    # mutated[v] = new_sol[v]
    # mutated = rlf_algorithm(prob, sol=mutated)

    ordering = new_sol.get_greedy_order()
    mutated = greedy_algorithm(prob, ordering)
    logging.info("mutation diff: " + str(np.sum(np.equal(mutated[:], sol[:]))/prob.v_size))
    return mutated


@trace
def update_population(prob, pop, eval_func):
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


def hybrid_algorithm(prob, pop_size, nbr_gen, pool_size, replace_rate,
                     mut_prob, local_search, ls_args, init_heur, init_args,
                     eval_func, init_methode, crossover_methode, duration):
    end_time = time.time()+(duration*60)
    crossovers = [crossover_permut,
                  crossover_cx,
                  crossover_cover,
                  crossover_area]

    init_pops = [generate_population,
                 generate_population2]

    crossover = crossovers[crossover_methode]
    init_pop = init_pops[init_methode]

    pop = init_pop(prob, pop_size, init_heur, init_args)
    pop = update_population(prob, pop, eval_func)

    best_sol = pop[0]
    best_score = best_sol.get_max_col()
    print_trace(prob, best_sol)

    new_gen_size = np.ceil(pop_size * replace_rate)
    for gen in range(nbr_gen):
        logging.info("############### generation " + str(gen) + " ################")
        new_gen = []
        while len(new_gen) < new_gen_size:
            parents = choose_parents(pop, 2, pool_size)
            logging.info("Parents: (" + str(parents[0].get_max_col()) +
                         ", " + str(parents[1].get_max_col()) + ")")
            child = crossover(prob, parents)

            if rd.rand() <= mut_prob:
                logging.info("Before mutation" + str(child.get_max_col()))
                child = mutation(prob, child, local_search, ls_args)
                logging.info("After mutation" + str(child.get_max_col()))
                child = local_search(prob, sol=child, **ls_args)
                logging.info("Result" + str(child.get_max_col()))

            child = local_search(prob, sol=child, **ls_args)
            logging.info("Resulting child" + str(child.get_max_col()) +
                         " ->" + str(child.get_max_col()))
            new_gen.append(child)

        new_gen = update_population(prob, new_gen, eval_func)
        pop = new_gen + pop
        pop = update_population(prob, pop, eval_func)
        pop = pop[:pop_size]

        if pop[0].get_max_col() < best_score:
            best_sol = pop[0].copy()
            best_score = best_sol.get_max_col()
            print_trace(prob, best_sol)

        if time.time() >= end_time:
            logging.warning("time stop!")
            break

    return best_sol

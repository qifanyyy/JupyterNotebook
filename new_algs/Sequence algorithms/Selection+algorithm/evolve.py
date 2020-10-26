import tracta_ml.pool_maintenance as pm
import numpy as np
import collections


def converge(parents, best_parent):
    mean_fitness = np.mean([i.fitness['fit_mod'] for i in parents])
    best_fitness = best_parent.fitness['fit_mod']
    return abs(best_fitness - mean_fitness)/mean_fitness


def model_tuner(X, Y, mod, param_dict, cv, scoring, verbose,\
                look_back=1000, n_gen=2000, known_best=None):

    '''Initializing parent pool'''
    pool_size = 5

    if type(known_best) != type(None):
        inter_param_dict = collections.OrderedDict()
        for i in range(len(known_best.hpGene)):
            key = [j for j in known_best.param_list.keys()][i]
            value = param_dict[key]
            inter_param_dict[key] = value
        param_dict = inter_param_dict
    else:
        param_dict = collections.OrderedDict(param_dict)

    parents = pm.gen_random_parents(X, Y, mod, param_dict, cv, scoring, 10*pool_size)
    parents.sort(reverse=True)
    parents = parents[0:pool_size]

    if type(known_best) == type(parents[0]):
        parents[0] = known_best

    best_parent = parents[0]
    previous_best = best_parent

    best_mod_fit = []
    best_feat_fit = []
    best_stdev_fit = []

    lb_cntr = 0
    restart_count = 0

    for gen_cnt in range(n_gen):

        '''Crossover Pool'''
        crossover_pool = pm.crossover_pool(parents, X, Y, mod, cv, scoring, pool_size-1)
        parents = crossover_pool + [best_parent]

        '''Elitism for next generation'''
        parents.sort(reverse=True)
        best_parent = parents[0]

        '''Checking for Nominal convergence'''

        if converge(parents,parents[0]) < 10**-6:
            restart_count += 1
            parents = pm.gen_random_parents(X, Y, mod, param_dict, cv, scoring, pool_size-1)
            parents = parents + [best_parent]
            parents.sort(reverse=True)
            best_parent = parents[0]

        current_best = best_parent

        '''Checking for Solution convergence'''
        if previous_best == current_best:
            lb_cntr += 1
        else:
            lb_cntr = 0
        if lb_cntr >= look_back:
            break
        previous_best = current_best

        best_mod_fit.append(best_parent.fitness['fit_mod'])
        best_feat_fit.append(best_parent.fitness['fit_feat'])
        best_stdev_fit.append(best_parent.fitness['fit_stdev'])

        if verbose == True:
            print("Iteration -",gen_cnt+1,"complete","......",\
                  "best_score : {:.4f}, score_stdev: {:.4f}, feat_fitness: {:.4f}".\
                  format(best_mod_fit[-1], best_stdev_fit[-1], best_feat_fit[-1]))

    monitor = {'Model_Fitness': best_mod_fit,
               'Feature_Fitness': best_feat_fit,
               'Stdev': best_stdev_fit}

    return best_parent, monitor
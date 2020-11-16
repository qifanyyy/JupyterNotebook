#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 20:52:19 2017

@author: rahul
"""

import random
import math
import numpy
import config
import data_handler
import algorithm


def init():
    qubit = []
    for i in range(0, config.NUM_FEATURES):
        qubit.append(random.uniform(0, 1)*math.pi*2)
    return qubit


def pop_init():
    pop_qubits = []
    for i in range(0, config.POPULATION_SIZE):
        pop_qubits.append(init())
    return pop_qubits


def qubit_observe(qubits):
    clabits = []
    for el in qubits:
        if math.pow(math.cos(el), 2) > random.uniform(0, 1):
            clabits.append(0)
        else:
            clabits.append(1)
    return clabits


def pop_observe(pop_qubits):
    pop_obs_qubits = []
    for qubits in pop_qubits:
        pop_obs_qubits.append(qubit_observe(qubits))
    return pop_obs_qubits


#def pop_accuracy(pop_obs_qubits):
#    accuracy = []
#    for clabits in pop_obs_qubits:
#        dataX, dataY = data_handler.dataset_with_feature_subset(clabits)
#        trainX, trainY, testX, testY = data_handler.train_test_set(dataX, dataY)
#        LR_model = algorithm.train_LR(trainX, trainY)
#        test_acc = algorithm.test_LR(LR_model, testX, testY)
#        accuracy.append(test_acc)
#    return accuracy


def pop_accuracy(pop_obs_qubits):
    mean_accuracy = []
    cross_validation_score = []
    for clabits in pop_obs_qubits:
        dataX, dataY = data_handler.dataset_with_feature_subset(clabits)
        LR_model = algorithm.train_LR(dataX, dataY)
        cv_score = algorithm.cross_validation_score(LR_model, dataX, dataY, 10)
        cross_validation_score.append(cv_score)
        mean_accuracy.append(numpy.mean(cv_score))
    return mean_accuracy, cross_validation_score


#def pop_accuracy(pop_obs_qubits):
#    accuracy = []
#    for clabits in pop_obs_qubits:
#        trainX, trainY = data_handler.read_train_data()
#        testX, testY = data_handler.read_test_data()
#        LR_model = algorithm.train_LR(trainX, trainY)
#        test_acc = algorithm.test_LR(LR_model, testX, testY)
#        accuracy.append(test_acc)
#    return accuracy


def mutation(qubits, pop_qubits, ind_num):
    index = list(range(0, config.POPULATION_SIZE))
    index.remove(ind_num)
    rand_indexes = random.sample(index, 3)
    Rand1 = pop_qubits[rand_indexes[0]]
    Rand2 = pop_qubits[rand_indexes[1]]
    Rand3 = pop_qubits[rand_indexes[2]]
    mut_qubits = []
    for i in range(0, config.NUM_FEATURES):
        mut_qubit = Rand1[i] + config.F * (Rand2[i] - Rand3[i])
        mut_qubits.append(mut_qubit)
    return mut_qubits


def pop_mutation(pop_qubits):
    pop_mut_qubits = []
    for ind_num, qubits in enumerate(pop_qubits):
        pop_mut_qubits.append(mutation(qubits, pop_qubits, ind_num))
    return pop_mut_qubits


def crossover(qubits, mut_qubits, Irand):
    cross_qubits = []
    for i in range(0, config.NUM_FEATURES):
        if random.uniform(0, 1) <= config.CR and i == Irand:
            cross_qubits.append(mut_qubits[i])
        else:
            cross_qubits.append(qubits[i])
    return cross_qubits


def get_Irand():
    Irand = int(1 + random.uniform(0, 1) * config.NUM_FEATURES)
    return Irand


def pop_crossover(pop_qubits, pop_mut_qubits, accuracy):
    pop_cross_qubits = []
    for qubits, mut_qubits in zip(pop_qubits, pop_mut_qubits):
        Irand = get_Irand()
        pop_cross_qubits.append(crossover(qubits, mut_qubits, Irand))
    return pop_cross_qubits


def selection(solution, cross_solution, solution_accuracy, cross_solution_accuracy):
    if cross_solution_accuracy > solution_accuracy:
        return cross_solution
    else:
        return solution


def pop_selection(pop_qubits, pop_obs_qubits, qubits_accuracy, pop_cross_qubits, pop_obs_cross_qubits, cross_qubits_accuracy):
    final_pop_qubits = []
    final_pop_obs_qubits = []
    for qubit, obs_qubit, qubit_accuracy, cross_qubit, obs_cross_qubit, cross_qubit_accuracy in zip(pop_qubits, pop_obs_qubits, qubits_accuracy, pop_cross_qubits, pop_obs_cross_qubits, cross_qubits_accuracy):
        if qubit_accuracy < config.ELITISM:
            final_pop_qubits.append(selection(qubit, cross_qubit, qubit_accuracy, cross_qubit_accuracy))
            final_pop_obs_qubits.append(selection(obs_qubit, obs_cross_qubit, qubit_accuracy, cross_qubit_accuracy))
        else:
            final_pop_qubits.append(qubit)
            final_pop_obs_qubits.append(obs_qubit)
    return final_pop_qubits, final_pop_obs_qubits

def print_output(final_pop_qubits, final_pop_obs_qubits, final_qubits_cross_val_score):
    f = open(config.OUTPUT_FILEPATH, 'w')
    f.write('VERSION : ' + config.VERSION + '\n')
    f.write('NUM_FEATURES : ' + str(config.NUM_FEATURES) + '\n')
    f.write('POPULATION_SIZE : ' + str(config.POPULATION_SIZE) + '\n')
    f.write('EQDE_MAXITER : ' + str(config.EQDE_MAXITER) + '\n')
    f.write('ELITISM : ' + str(config.ELITISM) + '\n')
    f.write('F : ' + str(config.F) + '\n')
    f.write('CR : ' + str(config.CR) + '\n')
    f.write('TEST_SIZE : ' + str(config.TEST_SIZE) + '\n' + '\n')

    for fold in range(0, 10):
        f.write("FOLD_" + str(fold) + "  --------------------\n\n")
        for solution in range(0, config.POPULATION_SIZE):
            f.write("Solution_" + str(solution) + ":" + '\n')
            f.write("ACCURACY: " + str(final_qubits_cross_val_score[solution][fold]) + '\n')
            f.write('QUBITS: ' + ' '.join(str(el) for el in final_pop_qubits[solution]) + '\n')
            f.write('OBSERVED_QUBITS: ' + ' '.join(str(el) for el in final_pop_obs_qubits[solution]) + '\n\n')

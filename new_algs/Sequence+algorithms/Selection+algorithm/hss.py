''' ===================== HYBRID SELECTION STRATEGY (HSS) ======================
        Universidade Federal de Sao Carlos - UFSCar, Sorocaba - SP - Brazil

        Master of Science Project       Artificial Intelligence

        Prof. Tiemi Christine Sakata    (tiemi@ufscar.br)
        Author: Vanessa Antunes         (tunes.vanessa@gmail.com)
   
    ============================================================================ '''

import sys
import numpy as np
import os
import math
from sklearn.metrics.cluster import adjusted_rand_score

from time import time

import pdb
import warnings

import readFiles as rf
import pareto
import plotting
import regionDivision as rd
import selection as sel

''' Calculates the adjusted rand index between the files and the true partitions
'''
def adjusted_rand(namePartitions, partitions, tp):
    
    mydt = np.dtype([('id', np.str_, 64), ('ari', np.float32, (len(tp),))])

    ari = []
    for __ in range(0, len(tp)):
        ari.append(str(adjusted_rand_score(partitions[0]['cluster'], tp[__]['cluster'])))
    
    list = np.array([(namePartitions[0], ari)], dtype = mydt)
    
    for _ in range(1, len(partitions)):
        ari = []
        for __ in range(0, len(tp)):
            ari.append(str(adjusted_rand_score(partitions[_]['cluster'], tp[__]['cluster'])))
        
        list = np.insert(list, len(list), (namePartitions[_], ari), axis=0)


    return list


def main(argv):
    partitionsPath, datasetName, tpPath, output, figureName, algorithm, percentage, outputreg = rf.inOut(argv)
    #pdb.set_trace()
    namePartitions, partitions = rf.readPartitions(partitionsPath)
    nameTP, partitionsTP = rf.readPartitions(tpPath)
    dataset = rf.readDataset(datasetName)

    import matplotlib.pyplot as plt 

    ari = adjusted_rand(namePartitions, partitions, partitionsTP)

    maxx = len(partitions)

    # Pareto Front
    f1, f2 = pareto.objectives(partitions + partitionsTP, dataset)
    p_frontX, p_frontY, p_frontName = pareto.pareto_frontier(f1[0:maxx], f2[0:maxx], namePartitions, maxX = False, maxY = False) 
    plt = plotting.plottingPartitions(plt, 1, ari, nameTP, f1, f2, len(partitions), namePartitions, 'Pareto Front', p_frontX, p_frontY, figureName)

    # Region Division
    #pdb.set_trace()
    y_pred = rd.region_division_k(p_frontX, p_frontY, p_frontName, algorithm, percentage)
    reg = rd.solutionsPerRegion(p_frontX, p_frontY, p_frontName, y_pred)

    for _ in range(0, len(reg)):
        fileout = open(outputreg + '_r' + str(_) + '.out', 'w')
        for __ in range(0,len(reg[_])):
            fileout.write(reg[_][__]['id'] + '\n')
        fileout.close()


    #plt = plotting.plotRegionDivision(plt, 2, ari, nameTP, p_frontX, p_frontY, p_frontName, y_pred, 'Pareto Front Region Division')
    
    # Selection
    selected = sel.selection(reg, partitions, namePartitions, p_frontX, p_frontY, p_frontName, ari, output, y_pred)

    #plt.show()

if __name__ == "__main__": 
    main(sys.argv[1:])
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
import random
from sklearn.metrics.cluster import adjusted_rand_score

from time import time

import pdb
import warnings
import sys, getopt

import readFiles as rf
import pareto
import plotting
import regionDivision as rd
import selection as sel

def sentence():
    print 'Usage: beRandom.py -p <partitions_path> -d <dataset_path> -t <true_partition_path> -o <output_path> -n <number_partitions>'

def inOut(argv):

    try:
        opts, args = getopt.getopt(argv,"hp:d:t:o:n:",["partitions=", "dataset=", "tp=", "output=", "number="])

    #   Exception getopt.GetoptError: This is raised when an unrecognized option is found in the argument list or when an option requiring an argument is given none. 
    except getopt.GetoptError:
        sentence()
        sys.exit(2)

    if len(opts) < 5:
        sentence()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            sentence()
            sys.exit()
        elif opt in ("-p", "--partitions"):
            partitionsPath = arg
        elif opt in ("-d", "--dataset"):
            dataset = arg
        elif opt in ("-t", "--tp"):
            tpPath = arg
        elif opt in ("-o", "--output"):
            output = arg
        elif opt in ("-n", "--number"):
            number = int(arg)

    #output += dataset.split('/')[-1].split('.')[0] + '.csv'
    # for mock and mocle:
    #output += partitionsPath.split('/')[5] + "/" + partitionsPath.split('/')[5] + '_' + partitionsPath.split('/')[6] + '.csv'

    print 'Partitions path: ', partitionsPath
    print 'Dataset: ', dataset
    print 'TP path is: ', tpPath
    print 'Output Path: ', output
    print 'Number of partitions: ', number

    return partitionsPath, dataset, tpPath, output, number

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
    #pdb.set_trace()
    partitionsPath, dataset, tpPath, output, number = inOut(argv)
    namePartitions, partitions = rf.readPartitions(partitionsPath)
    nameTP, partitionsTP = rf.readPartitions(tpPath)
    ari = adjusted_rand(namePartitions, partitions, partitionsTP)

    aux = random.sample(xrange(0, len(namePartitions)), number)

    fileout = open(output, 'w')    
    for x in aux:
        #print namePartitions[x]
        straux = ''
        for __ in range(0, len(ari[x][1])):
            straux += str('{0:.12f}'.format(ari[x][1][__])) + ' '

        fileout.write(ari[x][0] + ' ' + straux + '\n')

if __name__ == "__main__": 
    main(sys.argv[1:])
import sys, getopt
import numpy as np
import os
import math
import csv
import pdb
from math import log

#https://gist.github.com/jwcarr/626cbc80e0006b526688#file-vi-py

def inOut(argv):

    try:
        opts, args = getopt.getopt(argv,"hp:l:d:",["partitions=","list=","dataset="])

    #   Exception getopt.GetoptError: This is raised when an unrecognized option is found in the argument list or when an option requiring an argument is given none. 
    except getopt.GetoptError:
        sys.exit(2)

    if len(opts) < 1:
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            sys.exit()
        elif opt in ("-l", "--list"):
            list = arg
        elif opt in ("-p", "--partitions"):
            partitions = arg
        elif opt in ("-d", "--dataset"):
            dataset = arg

    list += dataset + '.csv'
    print ('partitions: ', partitions)
    print ('list: ', list)
    print ('dataset: ', dataset)

    return partitions, list, dataset

def variation_of_information(X, Y):
    n = float(sum([len(x) for x in X]))
    sigma = 0.0
    for x in X:
        p = len(x) / n
        for y in Y:
            q = len(y) / n
            r = len(set(x) & set(y)) / n
            if r > 0.0:
                sigma += r * (log(r / p, 2) + log(r / q, 2))

    return abs(sigma)

def read_csv(csvname):
    with open(csvname) as csvfile:
        readCSV = csv.reader(csvfile, delimiter='\t')
        data=[]
        max = 1
        for row in readCSV:
            if int(row[1]) > max:
                max = int(row[1])
            data.append(row)
    
    part = []

    for i in range(max):
        part.append([])

    for i in range(len(data)):
        part[int(data[i][1]) -1].append(data[i][0])

    return part

def dissimiarity(selected_p, partitions, datasetName):
    p=[]

    for my_p in selected_p:
        p.append(read_csv(partitions + my_p))
    
    fx = []
    lim = len(selected_p)
    for _ in range(lim):
        vii = 0
        for __ in range(lim):
            vii += variation_of_information(p[_], p[__])
        
        fx.append(round((vii / lim),2))
    
    fileout = open('/home/vantunes/UFSCar/SelectionStrategyFinal/dissimilariry_hsspf.out', 'a')
    fileout.write(datasetName + '\t' + str(np.mean(fx)) + '\n')
    fileout.close()


def main(argv):
    partitions, csvname, dataset = inOut(argv)
    #pdb.set_trace()

    with open(csvname) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=' ')
        selected_p=[]
        for row in readCSV:
            selected_p.append(row[0])

    #selected_p = os.listdir(path)
    dissimiarity(selected_p, partitions, dataset)

if __name__ == "__main__": 
    main(sys.argv[1:])
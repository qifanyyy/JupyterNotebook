__author__ = 'suhas subramanya'

import MapReduce
import sys
import json

mr=MapReduce.MapReduce()

def mapper(record):
    mr.emit_intermediate(record[1],('A',record[0],record[2]))
    mr.emit_intermediate(record[0],('B',record[1],record[2]))

def reducer(key,list_of_values):
    firstMatrix=[]
    secondMatrix=[]
    for each in list_of_values:
        if each[0]=='A':
            firstMatrix.append((each[1],each[2]))
        else:
            secondMatrix.append((each[1],each[2]))

    for eachFirst in firstMatrix:
        for eachSecond in secondMatrix:
            mr.emit((eachFirst[0],eachSecond[0],eachFirst[1]*eachSecond[1]))



inputdata= open(sys.argv[1])
mr.execute(inputdata,mapper,reducer)


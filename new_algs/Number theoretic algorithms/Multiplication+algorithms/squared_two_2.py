__author__ = 'suhas subramanya'

import MapReduce
import sys

mr=MapReduce.MapReduce()

def mapper(record):
    mr.emit_intermediate((record[0],record[1]),record[2])

def reducer(key,list_of_values):
    sum=0
    for each in list_of_values:
        sum+=each
    mr.emit((key[0],key[1],sum))


inputdata= open(sys.argv[1])
mr.execute(inputdata,mapper,reducer)


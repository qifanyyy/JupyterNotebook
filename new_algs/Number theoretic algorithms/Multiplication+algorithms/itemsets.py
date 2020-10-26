__author__ = 'suhas subramanya'

import MapReduce
import sys

mr=MapReduce.MapReduce()

def mapper(record):
    for i in range(0,len(record)-1):
        for j in range(i+1,len(record)):
            mr.emit_intermediate((record[i],record[j]),1)


def reducer(key,list_of_values):
    total=0
    for each in list_of_values:
        total+=1
    if total>=100:
        mr.emit(key)


inputdata= open(sys.argv[1])
mr.execute(inputdata,mapper,reducer)

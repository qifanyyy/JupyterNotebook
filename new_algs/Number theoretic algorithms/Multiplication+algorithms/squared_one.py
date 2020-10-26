__author__ = 'suhas subramanya'

import MapReduce
import sys

mr=MapReduce.MapReduce()

def mapper(record):
    for k in range(0,5):
        mr.emit_intermediate((record[0],k),('A',record[1],record[2]))
    for k in range(0,5):
        mr.emit_intermediate((k,record[1]),('B',record[0],record[2]))


def reducer(key,list_of_values):
    sum=0
    flag=0
    for j in range(0,5):
        product=1
        flag=0
        count=0
        for each in list_of_values:

            if each[1]==j:
                count+=1
                if(each[2]==1):
                    flag=1
                product*=each[2]
        if count==2:
            if product==1 and flag==1:
                sum+=product
            elif product>1:
                sum+=product
    mr.emit((key[0],key[1],sum))


inputdata= open(sys.argv[1])
mr.execute(inputdata,mapper,reducer)




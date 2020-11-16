#!/usr/bin/python

import sys

####ASSUMPTION: rdered matrix!

##get the size of the matrices from a size file:
#info = open("matrix_size.txt").readlines()
#for info_line in info:
#    info_line = info_line.strip()
#    matrix,i,j = info_line.split(",")
#    if matrix == "A":
#        #error prone type conversion
#        try:
#            A_i = int(i)
#        except ValueError:
#            continue
#    else:
#        try:
#            B_j = int(j)
#        except ValueError:
#            continue

#actual mapping algorithm that needs A_i, B_i and text file as input

n = int(3)
m = int(3)

for line in sys.stdin:
    line = line.strip()
    matrix,i,j,v = line.split(",")

    #case matrix A
    if matrix == "A":
        for ind in range(1,n+1):
            if j == str(ind):
                key = str(ind)+ "\t" + "A"
                print ("%s\t%s\t%s"%(key,i,v))
    #case matrix B
    else:
        for ind in range(1,m+1):
            if j == str(ind):
                key = str(ind)+ "\t" + "B"
                print ("%s\t%s\t%s"%(key,j,v))



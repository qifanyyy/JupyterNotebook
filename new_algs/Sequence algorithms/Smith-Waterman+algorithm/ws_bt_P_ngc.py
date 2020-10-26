# -*- coding: utf8 -*

__author__ = "Draesslerová Dominika"

"""
    backtrace implementation using 3 scoring arrays and 1 direction array, with visualization, missing endgap penalty
"""

import numpy as np
import sys, psutil, os
import time
import gc

#   penalizations
GAP = -10
EXTENDEDGAP = -1

DNA_matrix = {
    "G": {"G": 5, "C": -4, "A": -4, "T": -4},
    "C": {"G": -4, "C": 5, "A": -4, "T": -4},
    "A": {"G": -4, "C": -4, "A": 5, "T": -4},
    "T": {"G": -4, "C": -4, "A": -4, "T": 5},
}

#   get max from all posibilities or zero value
def maxscore(a, b, c):
    if a > 0 or b > 0 or c > 0:
        if a > b and a > c:
            return a, 0
        if b > c:
            return b, 1
        return c, 2
    else:
        return 0,0

#   get maxi in columns
def getMaxInColumn(scoreArr, i, j):
    retv = -100000
    for a in range(i, 0, -1):
        if retv < (scoreArr[i - a, j, 0] + GAP + (EXTENDEDGAP * a)):
            retv = scoreArr[i - a, j, 0] + GAP + (EXTENDEDGAP * a)
    return retv

#   get max in rows
def getMaxInRow(scoreArr, i, j):
    retv = -100000
    for a in range(j, 0, -1):
        if retv < (scoreArr[i, j - a, 0] + GAP + (EXTENDEDGAP * a)):
            retv = scoreArr[i, j - a, 0] + GAP + (EXTENDEDGAP * a)
    return retv

#   major calculation process
def align_sequences(s1, s2, lens1, lens2, scoreArr):
    #   start timecalculation
    start = time.process_time()
    
    #   for each cell in scoreArr calculate 3 options
    for i in range(1, lens1):
        for j in range(1, lens2):

            opt0= scoreArr[i - 1, j - 1, 0] + DNA_matrix[s1[i]][s2[j]]
            opt1 = getMaxInColumn(scoreArr, i, j)
            opt2 = getMaxInRow(scoreArr, i, j)

            #   get maximum  from 3 options
            scoreArr[i, j] = maxscore(opt0, opt1, opt2)

    #   get maximum scores in scoreArr
    maximums = np.where(scoreArr == np.amax(scoreArr))
    maximums = list(zip(maximums[0], maximums[1]))

    #  for each maximum score in scoreArr create result alignment
    for i, j in maximums:
        score = scoreArr[i,j,0]
        out1 = ""
        out2 = ""
        bind = ""
        
        #   backtrace
        while (i > 0) and (j > 0) and scoreArr[i, j, 0] > 0:
            if scoreArr[i, j, 1] == 0:
                out1 = s1[i] + out1
                bind = ("|" if s1[i] == s2[j] else ".") + bind
                out2 = s2[j] + out2
                i -= 1
                j -= 1
            elif scoreArr[i, j, 1] == 1:
                out1 = s1[i] + out1
                bind = " " + bind
                out2 = "-" + out2
                i -= 1
            else:
                out1 = "-" + out1
                bind = " " + bind
                out2 = s2[j] + out2
                j -= 1

        # stop time calculation
        end = time.process_time()

        #   print result
        print(out1)
        print(bind)
        print(out2)
    print("score: " + str(score))
    print("time: " + str((end-start)*1000000) + ' us')

#   main
args = sys.argv
gc.disable()
#   read sequences from input file
f = open(args[1])
s1, s2 = " " + f.readline()[:-1], " " + f.readline()
process = psutil.Process(os.getpid())
print("s1: "+s1[1:])
print("s2: "+s2[1:])
lens1 = len(s1)
lens2 = len(s2)
print("lenght of string s1: "+str(lens1-1))
print("lenght of string s2: "+str(lens2-1))

#   declare scoreArr
scoreArr = np.zeros((lens1, lens2, 2), dtype=int)
scoreArr[:, 0] = [[0, 1] for i in range(0, lens1)]
scoreArr[0, :] = [[0, 2] for i in range(0, lens2)]
scoreArr[0, 0, 1] = -1

#   start calculation
align_sequences(s1, s2, lens1, lens2, scoreArr)
print("total memory allocated: "+ str(process.memory_info().rss) + " [B]")

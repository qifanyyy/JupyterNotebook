# -*- coding: utf8 -*

__author__ = "Draesslerova Dominika"

"""
    classic iterative global implementation with reverse calculation, no endgap penalty, garbage collector disabled
"""
import numpy as np
import sys, psutil, os, time, gc

#   penalizations
GAP = -10

#   score matrix
DNA_matrix = {
    "G": {"G": +5, "C": -4, "A": -4, "T": -4},
    "C": {"G": -4, "C": +5, "A": -4, "T": -4},
    "A": {"G": -4, "C": -4, "A": +5, "T": -4},
    "T": {"G": -4, "C": -4, "A": -4, "T": +5}
}

#   find best score from all posibilities calculated from scoreArray
def maxscore(a, b, c):
    if a > b and a > c:
        return a
    if b > c:
        return b
    return c

#   major calculation proccess
def align_sequences(s1, s2, lens1, lens2, scoreArr):
    #   start time calculation
    start = time.process_time()

    #   for each cell in scoreArr calculate 3 options
    for i in range(1, lens1):
        for j in range(1, lens2):
    
            opt0 = scoreArr[i - 1, j - 1] + DNA_matrix[s1[i]][s2[j]]
            opt1 = scoreArr[i - 1, j] + GAP
            opt2 = scoreArr[i, j - 1] + GAP

            #   get maximum from 3 options
            maximum = maxscore(opt0, opt1, opt2)
            scoreArr[i, j] = maximum
    
    #   backtrace
    i = lens1 - 1
    j = lens2 - 1

    score = scoreArr[i, j]
    out1 = ""
    bind = ""
    out2 = ""

    #   create best alignment
    while (i > 0) and (j > 0):
        if scoreArr[i, j] == scoreArr[i - 1, j - 1] + DNA_matrix[s1[i]][s2[j]]:
            #   diagonal   
            out1 = s1[i] + out1
            bind = ("|" if s1[i] == s2[j] else ".") + bind
            out2 = s2[j] + out2
            i -= 1
            j -= 1
        elif scoreArr[i, j] == scoreArr[i - 1, j] + GAP:
            #   up
            out1 = s1[i] + out1
            bind = " " + bind
            out2 = "-" + out2
            i -= 1
        elif scoreArr[i, j] == scoreArr[i, j - 1] + GAP:
            #   left
            out1 = "-" + out1
            bind = " " + bind
            out2 = s2[j] + out2
            j -= 1

    while i > 0:
        out1 = s1[i] + out1
        bind = " " + bind
        out2 = "-" + out2
        i -= 1

    while j > 0:
        out1 = "-" + out1
        bind = " " + bind
        out2 = s2[j] + out2
        j -= 1

    #   stop time calculation
    end = time.process_time()

    #   print result
    print(out1)
    print(bind)
    print(out2)
    print("score: " + str(score))
    print("time: " + str((end-start)*1000000) + " us")

#   main
args = sys.argv

#   disable garbage collector
gc.disable()

#   read sequences from file
f = open(args[1])
s1, s2 = " " + f.readline()[:-1], " " + f.readline()
process = psutil.Process(os.getpid())
print("s1: " + s1[1:]) 
print("s2: " + s2[1:])
lens1 = len(s1)
lens2 = len(s2)
print("lenght of s1: " + str(lens1 - 1))
print("lenght of s2: " + str(lens2 - 1))

#   declare scoreArr
scoreArr = np.zeros((lens1, lens2), dtype=int)
scoreArr[:, 0] = [-i for i in range(0, lens1)]
scoreArr[0, :] = [-i for i in range(0, lens2)]

#   start calculation
align_sequences(s1, s2, lens1, lens2, scoreArr)
print("total memory allocated: " + str(process.memory_info().rss) + " [B]")

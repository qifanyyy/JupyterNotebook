# -*- coding: utf8 -*

__author__ = "Draesslerova Dominika"

"""
    recursive implementation, memoization 2D array memCon, extended gap, endgap penalization  
"""

import numpy as np
import sys, psutil, os
import time

#   penalizations
GAP = -10
EXTENDEDGAP = -1
ENDGAP = 0

DNA_matrix = {
    "G": {"G": 5, "C": -4, "A": -4, "T": -4},
    "C": {"G": -4, "C": 5, "A": -4, "T": -4},
    "A": {"G": -4, "C": -4, "A": 5, "T": -4},
    "T": {"G": -4, "C": -4, "A": -4, "T": 5},
}

#   major calculation process
def align_sequences(s1, s2, eg1, eg2, memCon, i, j):

    #   stop condition
    if s1 == "":
        return len(s2) * ENDGAP, [["-" * len(s2), "", s2]]
    elif s2 == "":
        return len(s1) * ENDGAP, [[s1, "", "-" * len(s1)]]
    #   already calculated?
    elif memCon[i][j][0] != float("-inf"):
        return memCon[i][j]
    else:
        #   get options
        opt0_score, opt0_alignment = align_sequences(
            s1[1:], s2[1:], False, False, memCon, i + 1, j + 1
        )
        opt1_score, opt1_alignment = align_sequences(
            s1[1:], s2, False, True if eg2 else False, memCon, i + 1, j
        )
        opt2_score, opt2_alignment = align_sequences(
            s1, s2[1:], True if eg1 else False, False, memCon, i, j + 1
        )

        #   edit score
        opt0_score += DNA_matrix[s1[0]][s2[0]]
        opt1_score += (
            ENDGAP
            if eg2
            else (EXTENDEDGAP if opt1_alignment[0][2].startswith("-") else GAP)
        )
        opt2_score += (
            ENDGAP
            if eg1
            else (EXTENDEDGAP if opt2_alignment[0][0].startswith("-") else GAP)
        )

        #   edit sequences
        opt0_alignment = [
            [s1[0] + seq1, ("|" if s1[0] == s2[0] else ".") + bind, s2[0] + seq2]
            for seq1, bind, seq2 in opt0_alignment
        ]
        opt1_alignment = [
            [s1[0] + seq1, " " + bind, "-" + seq2]
            for seq1, bind, seq2 in opt1_alignment
        ]
        opt2_alignment = [
            ["-" + seq1, " " + bind, s2[0] + seq2]
            for seq1, bind, seq2 in opt2_alignment
        ]

        #   new options
        opt0 = opt0_score, opt0_alignment
        opt1 = opt1_score, opt1_alignment
        opt2 = opt2_score, opt2_alignment

        # výběr lepší větve výpočtu
        xs = [opt0, opt1, opt2]
        maximum, alignment = max(xs)

        memCon[i][j] = [maximum, alignment]
        return [maximum, alignment]


def get_array(s1, s2):
    orlens1 = len(s1)
    orlens2 = len(s2)
    alignment = float("-inf"), [["", "", ""]]
    memCon = [[alignment for i in range(orlens2)] for i in range(orlens1)]
    return memCon

#   main
args = sys.argv

#   read sequences from input file
f = open(args[1])
s1, s2 = f.readline()[:-1], f.readline()
process = psutil.Process(os.getpid())
print("s1: "+s1[1:])
print("s2: "+s2[1:])
lens1 = len(s1)
lens2 = len(s2)
print("lenght of string s1: "+str(lens1-1))
print("lenght of string s2: "+str(lens2-1))

#   declare memoization array
memCon = get_array(s1, s2)
#   start timecalculation
start = time.process_time()
result = align_sequences(s1, s2, True, True, memCon, 0, 0)

# stop time calculation
end = time.process_time()

#   print result
print(result[1][0][0])
print(result[1][0][1])
print(result[1][0][2])
print("score: ", result[0])
print("time: " + str((end-start)*1000000) + ' us')
print("total memory allocated: "+ str(process.memory_info().rss) + " [B]")

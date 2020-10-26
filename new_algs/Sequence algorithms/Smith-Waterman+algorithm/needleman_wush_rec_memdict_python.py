# -*- coding: utf8 -*

__author__ = "Draesslerová Dominika"

"""
    recursive implementation with memoization (dictionary), with endgap penalty implementation, visualization available  
"""

import numpy as np
import sys

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


def memoize(f):
    memCon = {}

    def helper(s1, s2, eg1, eg2):
        if (s1, s2) not in memCon:
            memCon[(s1, s2)] = f(s1, s2, eg1, eg2)
        return memCon[(s1, s2)]

    return helper


# @memoize
def align_sequences(s1, s2, eg1, eg2):
    if s1 == "" or s2 == "":
        return [0, s1, "", s2]

    # if (s1, s2) in memo:
    #     print("return",memo[(s1, s2)])
    #     return memo[(s1, s2)]

    opt0 = align_sequences(s1[1:], s2[1:], False, False)

    opt1 = align_sequences(s1[1:], s2, False, True if eg2 else False)

    opt2 = align_sequences(s1, s2[1:], True if eg1 else False, False)

    opt0[0] += DNA_matrix[s1[0]][s2[0]]
    opt1[0] += ENDGAP if eg2 else (EXTENDEDGAP if opt1[3].startswith("-") else GAP)
    opt2[0] += ENDGAP if eg1 else (EXTENDEDGAP if opt1[1].startswith("-") else GAP)

    if opt0[0] > opt1[0] and opt0[0] > opt2[0]:
        index_of_max = 0
    elif opt1[0] > opt2[0]:
        index_of_max = 1
    else:
        index_of_max = 2

    if index_of_max == 0:
        solution = [
            opt0[0],
            s1[0] + opt0[1],
            ("|" if s1[0] == s2[0] else ".") + opt0[2],
            s2[0] + opt0[3],
        ]
    elif index_of_max == 1:
        solution = [
            opt1[0],
            s1[0] + opt1[1],
            " " + opt1[2],
            "-" + opt1[3],
        ]
    else:
        solution = [
            opt2[0],
            "-" + opt2[1],
            " " + opt2[2],
            s2[0] + opt2[3],
        ]

    # memo[(s1, s2)] = solution
    return solution


args = sys.argv
s1,s2 = args[1], args[2]
print(s1, s2)
orlens1 = len(s1)
orlens2 = len(s2)

result = align_sequences(s1, s2, True, True)
print("score: ", result[0])
print(result[1])
print(result[2])
print(result[3])

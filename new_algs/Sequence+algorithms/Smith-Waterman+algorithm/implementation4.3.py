# -*- coding: utf8 -*

__author__ = "Draesslerová Dominika"

"""
    recursive implementation with memoization dictionary, without endgap penalization, visualization available  
"""

import numpy as np

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


def align_sequences(s1, s2, eg1, eg2, memCon, i, j):
    if s1 == "" or s2 == "":
        return [0, s1, "", s2]

    # if memCon[i][j][0] != float("-inf"):
    #     return memCon[i][j]

    opt0 = align_sequences(s1[1:], s2[1:], False, False, memCon, i + 1, j + 1)

    opt1 = align_sequences(s1[1:], s2, False, True if eg2 else False, memCon, i + 1, j)

    opt2 = align_sequences(s1, s2[1:], True if eg1 else False, False, memCon, i, j + 1)

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

    # memCon[i][j] = solution
    return solution


with open("data.txt", "r") as f:
    for s1, s2, x in zip(f, f, f):
        s1, s2 = s1.strip(), s2.strip()
        orlens1 = len(s1)
        orlens2 = len(s2)
        alignment = [float("-inf"), "", "", ""]
        memCon = [[alignment for i in range(orlens2)] for i in range(orlens1)]
        result = align_sequences(s1, s2, True, True, memCon, 0, 0)
        # print(memCon)
        print("score: ", result[0])
        print(result[1])
        print(result[2])
        print(result[3])

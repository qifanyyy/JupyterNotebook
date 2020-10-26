# -*- coding: utf8 -*

__author__ = "Draesslerová Dominika"


"""
    backtrace implementation with 3 scoring tables and 1 direction table, without endgap penalty implementation, visualization implemented
"""

import numpy as np
import sys

#   penalizations
GAP = -10
EXTENDEDGAP = -1


DNA_matrix = {
    "G": {"G": 5, "C": -4, "A": -4, "T": -4},
    "C": {"G": -4, "C": 5, "A": -4, "T": -4},
    "A": {"G": -4, "C": -4, "A": 5, "T": -4},
    "T": {"G": -4, "C": -4, "A": -4, "T": 5},
}


def resetArrays(lens1, lens2):
    D = np.zeros((lens1, lens2), dtype=int)
    M = np.zeros((lens1, lens2), dtype=int)
    L = np.zeros((lens1, lens2), dtype=int)
    U = np.zeros((lens1, lens2), dtype=int)

    for i in range(lens1):
        for j in range(lens2):
            if i == 0 and j == 0:
                M[0][0] = 0
                D[0][0] = -1
            elif i == 0:
                M[0][j] = GAP + j * EXTENDEDGAP
                U[0][j] = GAP + j * EXTENDEDGAP
                L[0][j] = GAP + j * EXTENDEDGAP
                D[0][j] = 2
            elif j == 0:
                M[i][0] = GAP + i * EXTENDEDGAP
                L[i][0] = GAP + i * EXTENDEDGAP
                U[i][0] = GAP + i * EXTENDEDGAP
                D[i][0] = 1

    return M, U, L, D


def maxScore(a, b, c):
    if a > b and a > c:
        return 0, a
    if b > c:
        return 1, b
    return 2, c


def align_sequences(s1, s2, lens1, lens2, M, U, L, D):
    #   calculate
    for i in range(1, lens1):
        for j in range(1, lens2):
            M[i, j] = M[i - 1, j - 1] + DNA_matrix[s1[i]][s2[j]]
            L[i, j] = np.amax([L[i - 1, j] + EXTENDEDGAP, M[i - 1, j] + GAP])
            U[i, j] = np.amax([U[i, j - 1] + EXTENDEDGAP, M[i, j - 1] + GAP])

            D[i, j], M[i, j] = maxScore(M[i, j], L[i, j], U[i, j])

    #   backtrace
    i = lens1 - 1
    j = lens2 - 1

    out1 = ""
    bind = ""
    out2 = ""

    score = M[i, j]
    while D[i, j] != -1:
        if M[i, j] > score:
            score = M[i, j]
        if D[i, j] == 0:
            out1 = s1[i] + out1
            bind = ("|" if s1[i] == s2[j] else ".") + bind
            out2 = s2[j] + out2
            i -= 1
            j -= 1
        elif D[i, j] == 1:
            out1 = s1[i] + out1
            bind = " " + bind
            out2 = "-" + out2
            i -= 1
        else:
            out1 = "-" + out1
            bind = " " + bind
            out2 = s2[j] + out2
            j -= 1

    print("score: " + str(score))
    print(out1)
    print(bind)
    print(out2)


args = sys.argv
s1,s2 = " "+args[1], " "+args[2]
print(s1, s2)
lens1 = len(s1)
lens2 = len(s2)
M, U, L, D = resetArrays(lens1, lens2)
align_sequences(s1, s2, lens1, lens2, M, U, L, D)

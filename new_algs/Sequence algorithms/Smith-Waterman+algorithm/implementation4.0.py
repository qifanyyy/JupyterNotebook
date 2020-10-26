# -*- coding: utf8 -*

__author__ = "Draesslerová Dominika"

"""
    recursive implementation with memoization 2d array, without endgap penalization,    
"""

import numpy as np

#   penalizations
GAP = -10
EXTENDEDGAP = -1
ENDGAP = 0

DNA_matrix = {
    "G": {"G": +1, "C": -3, "A": -3, "T": -3, "N": 0},
    "C": {"G": -3, "C": +1, "A": -3, "T": -3, "N": 0},
    "A": {"G": -3, "C": -3, "A": +1, "T": -3, "N": 0},
    "T": {"G": -3, "C": -3, "A": -3, "T": +1, "N": 0},
    "N": {"G": 0, "C": 0, "A": 0, "T": 0, "N": 0},
}


def align_sequences(i, j):

    if (i == lens1) or (j == lens2):
        return 0

    if memCon[i, j] != -1:
        return memCon[i, j]

    opt0 = DNA_matrix[s1[i]][s2[j]] + align_sequences(i + 1, j + 1)
    opt1 = (ENDGAP if j == 0 else GAP) + align_sequences(i + 1, j)
    opt2 = (ENDGAP if i == 0 else GAP) + align_sequences(i, j + 1)

    opts = [opt0, opt1, opt2]
    max_index = np.argmax(opts)

    memCon[i,j] = opts[max_index] 
    return opts[max_index]


with open("data.txt", "r") as f:
    for s1, s2, x in zip(f, f, f):
        s1, s2 = s1.strip(),s2.strip()
        lens1 = len(s1)
        lens2 = len(s2)
        memCon = np.ndarray((lens1,lens2),dtype=int)
        memCon.fill(-1)
        print(s1,s2)
        score = align_sequences(0, 0)
        print(score)

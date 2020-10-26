# -*- coding: utf8 -*

__author__ = "Draesslerová Dominika"

'''
    backtrace implementation using 3 scoring arrays and 1 direction array, with visualization, missing endgap penalty
'''

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


def get_index(arr, ax):
    return np.argmax(arr, axis=ax)[0]


def align_sequences(s1, s2, lens1, lens2, score_arr):
    for i in range(1, lens1):
        for j in range(1, lens2):

            opt1 = score_arr[i - 1, j - 1] + DNA_matrix[s1[i]][s2[j]]
            index = get_index(score_arr[:i, j - 1 : j], 1)
            opt2 = score_arr[i, index] + GAP + (index * EXTENDEDGAP)
            index = get_index(score_arr[i - 1 : i, :j], 0)
            opt3 = score_arr[index, j] + GAP + (index * EXTENDEDGAP)

            score_arr[i, j] = np.amax([opt1, opt2, opt3, 0])

    maximums = np.where(score_arr == np.amax(score_arr))
    maximums = list(zip(maximums[0], maximums[1]))

    for i, j in maximums:
        out1 = ""
        bind = ""
        out2 = ""
        score = 0
        while (i > 0) and (j > 0) and score_arr[i, j] > 0:
            score += score_arr[i, j]
            if score_arr[i, j] == score_arr[i - 1, j - 1] + DNA_matrix[s1[i]][s2[j]]:
                out1 = s1[i] + out1
                bind = ("|" if s1[i] == s2[j] else ".") + bind
                out2 = s2[j] + out2
                i -= 1
                j -= 1
            elif score_arr[i, j] == score_arr[
                i, get_index(score_arr[:i, j - 1 : j], 0)
            ] + GAP + (get_index(score_arr[:i, j - 1 : j], 0) * EXTENDEDGAP):
                out1 = s1[i] + out1
                bind = " " + bind
                out2 = "-" + out2
                i -= 1
            else:
                out1 = "-" + out1
                bind = " " + bind
                out2 = s2[j] + out2
                j -= 1

        print(out1)
        print(bind)
        print(out2)
        print(score)

args = sys.argv
s1,s2 = " "+args[1], " "+args[2]
print(s1, s2)
lens1 = len(s1)
lens2 = len(s2)
score_arr = np.zeros((lens1, lens2), dtype=int)
align_sequences(s1, s2, lens1, lens2, score_arr)


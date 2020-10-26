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

result = dict()

def save_result(opt, score, i, j, depth):

    result = dict()
    result["score"] = score

    if opt == 0:
        result["alignment"] = {
            "out1": s1[i],
            "bind": "|" if s1[i] == s2[j] else ".",
            "out2": s2[j],
        }
    elif opt == 1:
        result["alignment"] = {"out1": s1[i], "bind": " ", "out2": "-"}
    else:
        result["alignment"] = {"out1": "-", "bind": " ", "out2": s2[j]}
    results[depth][(i, j)] = result


def align_sequences(i, j):
    if (i == lens1) or (j == lens2):
        return {"score": 0, "alignment": ["", "", ""]}
    print(s1[i],s2[j],DNA_matrix[s1[i]][s2[j]])

    if result[i][j] != dict():
        return result[i][j]

    opt0 = align_sequences(i + 1, j + 1)
    opt0["score"] += DNA_matrix[s1[i]][s2[j]]
    opt0["alignment"] = [[s1[i], "|" if s1[i] == s2[j] else ".", s2[j]][i] + opt0[
        "alignment"
    ][i] for i in range(3)]

    opt1 = align_sequences(i + 1, j)
    opt1["score"] += ENDGAP if j == 0 else (GAP)
    opt1["alignment"] = [[s1[i], " ", '-'][i] + opt0[
        "alignment"
    ][i] for i in range(3)]

    opt2 = align_sequences(i, j + 1)
    opt2["score"] += ENDGAP if j == 0 else GAP
    opt2["alignment"] = [['-', " ", s2[j]][i] + opt0[
        "alignment"
    ][i] for i in range(3)]

    opts = [opt0,opt1,opt2]
    print([opt["score"] for opt in opts])
    max_index = np.argmax([opt0["score"],opt1["score"],opt2["score"]])
    result[i][j] = opts[max_index]

    print(opts[max_index]["score"])
    print(opts[max_index]["alignment"][0])
    print(opts[max_index]["alignment"][1])
    print(opts[max_index]["alignment"][2])

    return opts[max_index]


with open("data.txt", "r") as f:
    for s1, s2, x in zip(f, f, f):
        s1, s2 = s1.strip(), s2.strip()
        lens1 = len(s1)
        lens2 = len(s2)

        #   declare size of memDict
        for i in range(lens1):
            result[i] = dict()
            for j in range(lens2):
                result[i][j] = dict()

        print(s1, s2)
        result = align_sequences(0, 0)
        print("score: "+str(result["score"]))
        print(result["alignment"][0])
        print(result["alignment"][1])
        print(result["alignment"][2])

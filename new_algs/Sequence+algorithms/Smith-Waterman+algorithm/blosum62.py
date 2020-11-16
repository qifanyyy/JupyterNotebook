# -*- coding: utf-8 -*-
"""
Sequence Aligment
    - Smith-Waterman algorithm
    - BLOSUM62 matrix

Xavier Pinho & Jorge Melo- Introduction to Bioinformatics, University of Coimbra, 2018/2019
"""
import numpy as np
import os

print("--------Importation Complete----------")

home = os.getcwd()
os.chdir(home)

file_blosum =open(home+"/BLOSUM62.txt")
blosum = file_blosum.read()
blosum_list = blosum.split("\n")

print("---------Data Loaded-----------------")

for i in range(len(blosum_list)):
    blosum_list[i] = blosum_list[i].split(" ")
for i in range(len(blosum_list)):
    while True:
        try:
            blosum_list[i].remove("")
        except ValueError:
            break
blosum_matrix = []
for line in range(len(blosum_list)):
    if line == 0:
        linha = blosum_list[line][0:]
    else:
        linha = blosum_list[line][1:]
    blosum_matrix.append(linha)
aa_list = blosum_matrix[0]
blosum_matrix = blosum_matrix[1:24]
blosum_matrix = np.array(blosum_matrix)


def smith_waterman(a: str, b: str, gap_cost: float = 2) -> float:
    """
    Compute the Smith-Waterman alignment score for two strings.
    See https://en.wikipedia.org/wiki/Smith%E2%80%93Waterman_algorithm#Algorithm
    This implementation has a fixed gap cost (i.e. extending a gap is considered
    free). In the terminology of the Wikipedia description, W_k = {c, c, c, ...}.
    This implementation also has a fixed alignment score, awarded if the relevant
    characters are equal.
    Kinda slow, especially for large (50+ char) inputs.
    """
    # H holds the alignment score at each point, computed incrementally
    H = np.zeros((len(a) + 1, len(b) + 1))
    P = np.zeros((len(a) + 1, len(b) + 1))
    DELETION, INSERTION, MISMATCH, MATCH = range(4)

    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            k = aa_list.index(a[i - 1])
            l = aa_list.index(b[j - 1])
            alignment_score = int(blosum_matrix[k][l])
            # The score for substituting the letter a[i-1] for b[j-1]. Generally low
            # for mismatch, high for match.
            match = (H[i - 1, j - 1] + (alignment_score if a[i - 1] == b[j - 1] else 0), MATCH)
            mismatch = (H[i - 1, j - 1] - (alignment_score if a[i - 1] != b[j - 1] else 0), MISMATCH)
            # The scores for for introducing extra letters in one of the strings (or
            # by symmetry, deleting them from the other).
            delete = (H[1:i, j].max() - gap_cost if i > 1 else 0, DELETION)
            insert = (H[i, 1:j].max() - gap_cost if j > 1 else 0, INSERTION)
            H[i, j], P[i, j] = max(match, delete, insert, mismatch, (0, 0))



    outfile1 = home+"/parte2_database"
    np.save(outfile1,H)
    outfile2 = home+"/parte2_database_p"
    np.save(outfile2,P)

    def backtrack():
        ind = np.unravel_index(np.argmax(H, axis=None), H.shape)
        i, j = ind
        while i > 0 or j > 0:
            assert i >= 0 and j >= 0
            if P[i][j] == MATCH or P[i][j] == MISMATCH:
                i -= 1
                j -= 1
                yield a[i], b[j]
            elif P[i][j] == INSERTION:
                j -= 1
                yield '-', b[j]
            elif P[i][j] == DELETION:
                i -= 1
                yield a[i], '-'
            else:
                assert (False)

    return [''.join(reversed(s)) for s in zip(*backtrack())]


seq1_file = open(home+"/seq1.txt")
seq1 = seq1_file.read()
seq1 = seq1.replace("\n","")

seq2_file = open(home+"/seq2.txt")
seq2 = seq2_file.read()
seq2 = seq2.replace("\n","")

results = smith_waterman(a=seq1, b=seq2)

seq1_results = results[0]
seq2_results = results[1]

file_out = open(home+"/seq1_results.txt","w")
file_out.write(seq1_results)
file_out.close()

file_out = open(home+"/seq2_results.txt","w")
file_out.write(seq2_results)
file_out.close()


print('------------Done-------------')
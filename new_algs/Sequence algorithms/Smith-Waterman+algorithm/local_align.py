import argparse
import numpy as np
import pandas as pd
from smith_waterman import scoringMatrixParse, matrix, traceback, evaluate, mutate
import os
import glob
import csv
import itertools
from Bio import SeqIO


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
def main():
    parser = argparse.ArgumentParser(description = "pairwise local alignment")
    parser.add_argument("gap_cost", help="affine gap penalty cost", type = int)
    parser.add_argument("gap_extension", help = "gap extension cost", type = int)
    parser.add_argument("matrix", help="scoring matrix")
    parser.add_argument("--score_only", help="set True if you only want the alignment score, False otherwise", type=str2bool, nargs="?", const=True, default=True)
    args = parser.parse_args()
    matrix_path = os.path.join("/Users/matt/OneDrive/UCSF/algorithms/HW3/scoring_matrices/", args.matrix)
    with open("/Users/matt/OneDrive/UCSF/algorithms/HW3/metadata/Negpairs.txt") as tsvfile:
        reader = csv.reader(tsvfile, delimiter=" ")
        nega_list = []
        negb_list = []
        for x, pair in enumerate(reader):
            A_input = os.path.join("/Users/matt/OneDrive/UCSF/algorithms/HW3/", pair[0])
            B_input = os.path.join("/Users/matt/OneDrive/UCSF/algorithms/HW3/", pair[1])
            fasta_seq = SeqIO.parse(open(A_input),"fasta")
            for fasta in fasta_seq:
                seq_A = str(fasta.seq).upper()
                nega_list.append(seq_A)
            fasta_seqb= SeqIO.parse(open(B_input), "fasta")
            for fasta in fasta_seqb:
                seq_B = str(fasta.seq).upper()
                negb_list.append(seq_B)
    with open("/Users/matt/OneDrive/UCSF/algorithms/HW3/metadata/Pospairs.txt") as tsvfile:
        reader = csv.reader(tsvfile, delimiter=" ")
        posa_list = []
        posb_list = []
        for x, pair in enumerate(reader):
            A_input = os.path.join("/Users/matt/OneDrive/UCSF/algorithms/HW3/", pair[0])
            B_input = os.path.join("/Users/matt/OneDrive/UCSF/algorithms/HW3/", pair[1])
            fasta_seq = SeqIO.parse(open(A_input),"fasta")
            for fasta in fasta_seq:
                seq_A = str(fasta.seq).upper()
                posa_list.append(seq_A)
            fasta_seqb= SeqIO.parse(open(B_input), "fasta")
            for fasta in fasta_seqb:
                seq_B = str(fasta.seq).upper()
                posb_list.append(seq_B)
    ############# -- create optimized matrix -- ###############
    negative = np.array(list(zip(nega_list, negb_list))[:4])
    positive = np.array(list(zip(posa_list, posb_list))[:4])
    optimized_matrix = mutate(negative, positive)
    pd.DataFrame(optimized_matrix)
    optimized_matrix.shape
    np.reshape(optimized_matrix, (22,22)).shape

s_list = np.zeros((50))
p_list = np.zeros((50))
fpr_list = []
roc_list = []
M = scoringMatrixParse(os.path.join("/Users/matt/OneDrive/UCSF/algorithms/HW3/scoring_matrices/", "PAM250"))
M.shape
M = optimized_matrix
for x, a in enumerate(list(zip(nega_list,negb_list))[:1]):
    H = matrix(a[0], a[1], M, -9, -3)
    pd.DataFrame(H)
    s = traceback(H, True, b=seq_B, b_="", old_i=0)
    s_list[x] = s
for x, a in enumerate(zip(posa_list,posb_list)):
    H = matrix(a[0], a[1], M, -9, -3)
    s = traceback(H, True, b=seq_B, b_="", old_i=0)
    p_list[x] = s

all_values = set(np.append(p_list, s_list).flatten())
tpr_list = []
fpr_list = []
for value in all_values:
    tpr = sum(p_list > value)/len(p_list)
    tpr_list.append(tpr)
    fpr = sum(s_list > value)/len(s_list)
    fpr_list.append(fpr)




################# -- ROC curve code -- ###################
s_list = np.zeros((50))
p_list = np.zeros((50))
fpr_list = []
roc_list = []
for mx in ["BLOSUM50", "BLOSUM62",  "MATIO",  "PAM100",  "PAM250"]:
matrix_path = os.path.join("/Users/matt/OneDrive/UCSF/algorithms/HW3/scoring_matrices/", "PAM250")
#false positives have an s > 311 with -9 and -3 gap penalties
for x, a in enumerate(zip(nega_list,negb_list)):
    M = scoringMatrixParse(matrix_path)
    H = matrix(a[0], a[1], M, -9, -3)
    s = traceback(H, True, b=seq_B, b_="", old_i=0)
    s_list[x] = s
matrix_pathp = os.path.join("/Users/matt/OneDrive/UCSF/algorithms/HW3/scoring_matrices/", "PAM250")
#false positives have an s > 311 with -9 and -3 gap penalties
for x, a in enumerate(zip(posa_list,posb_list)):
    M = scoringMatrixParse(matrix_pathp)
    H = matrix(a[0], a[1], M, -9, -3)
    s = traceback(H, True, b=seq_B, b_="", old_i=0)
    p_list[x] = s
all_values = set(np.append(p_list, s_list).flatten())
tpr_list = []
fpr_list = []
np.percentile(p_list, 30)
for value in all_values:
    tpr = sum(p_list > value)/len(p_list)
    tpr_list.append(tpr)
    fpr = sum(s_list > 38.7)/len(s_list)
    fpr_list.append(fpr)
#blosum50 is 0.28
#blosum62 is 0.32
#matio is 0.38
#PAM100 is 0.12
#pam250 is 0.34
 for tp in [[0.2,561],[0.4,415],[0.6,347],[0.8,263],[1,108]]:
     name = tp[0]
     thresh = tp[1]
     fpr = sum(s_list>thresh)/50
     print([mx, name ,fpr])
     roc_list.append([mx, name ,fpr])

import matplotlib.pyplot as plt
%matplotlib inline
plt.scatter(fpr_list, tpr_list)

plt.legend()
plt.show()









    ############ -- 20 x 5 parameter testing determined 9 and 3 to be an optimal solution for opening and extension penalties respectively ##################
    #fp_matrix=np.zeros((20,5))
    #for i in range(0,20):
    #   for j in range(0,5):
    #        with open("/Users/matt/OneDrive/UCSF/algorithms/HW3/metadata/Negpairs.txt") as tsvfile:
    #            reader = csv.reader(tsvfile, delimiter=" ")
    #            scores_array = np.zeros((50))
    #            for x, pair in enumerate(reader):
    #                #Loop through pairs
    #                A_input = os.path.join("/Users/matt/OneDrive/UCSF/algorithms/HW3/", pair[0])
    #                B_input = os.path.join("/Users/matt/OneDrive/UCSF/algorithms/HW3/", pair[1])
    #                fasta_seq = SeqIO.parse(open(A_input),"fasta")
    #                for fasta in fasta_seq:
    #                    seq_A = str(fasta.seq).upper()
    #                fasta_seqb= SeqIO.parse(open(B_input), "fasta")
    #                for fasta in fasta_seqb:
    #                    seq_B = str(fasta.seq).upper()
    #                M = scoringMatrixParse(matrix_path)
    #                H = matrix(seq_A, seq_B, M, -(i+1), -(j+1))
    #                s = traceback(H, args.score_only, b=seq_B, b_="", old_i=0)
    #                scores_array[x] = s
    #            fpr = sum(scores_array>311.8)/50
    #            fp_matrix[i,j] = fpr
    #print(fp_matrix)
if __name__ == "__main__":
    main()

#Part 1
#--done-- Implement/comment/test Smith-Waterman algorithm
#__done__ Find best gap opening/extension penalty combination for BLOSUM50
# Compare ROC curves for matrices
# Compare ROC curves for normalized and unnormalized scores
#Part 2
# Implement/test and describe optimization algorithm
# Optimize starting from best matrix
# Optimize starting from MATIO
# Explain how to convincingly argue for utility of an optimized matrix

########### -- percentile calculations done in excel -- ##############
#positive pairs 30th percentile = 311.8 (-3, -2)
#Negative paris 30th percentile = 182.4 (-3, -2)

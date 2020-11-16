import argparse
import numpy as np
from smith_waterman import scoringMatrixParse, matrix, traceback
import os
import glob
import csv
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
        reader = csv.reader(tsvfile, delimiter = " ")
        for x, pair in enumerate(reader):
            A_input = os.path.join("/Users/matt/OneDrive/UCSF/algorithms/HW3/", pair[0])
            B_input = os.path.join("/Users/matt/OneDrive/UCSF/algorithms/HW3/", pair[1])
            fasta_seq = SeqIO.parse(open(A_input),"fasta")
            seqarrayA = np.empty((50),dtype=np.str)
            seqarrayB = np.empty((50),dtype=np.str)
            print(seqarrayA)
            for fasta in fasta_seq:
                seq_A = str(fasta.seq).upper()
                seqarrayA[x] = seq_A
            fasta_seqb = SeqIO.parse(open(B_input),"fasta")
            for fasta in fasta_seqb:
                seq_B = str(fasta.seq).upper()
                seqarrayB[x] = seq_B
            print(seq_A)
    
    fp_matrix=np.zeros((20,5))
    for i in range(0,20,5):
        for j in range(0,5,2):
            with open("/Users/matt/OneDrive/UCSF/algorithms/HW3/metadata/Negpairs.txt") as tsvfile:
                reader = csv.reader(tsvfile, delimiter=" ")
                scores_array = np.zeros((50))
                for x, pair in enumerate(reader):
                    #Loop through pairs
                    A_input = os.path.join("/Users/matt/OneDrive/UCSF/algorithms/HW3/", pair[0])
                    B_input = os.path.join("/Users/matt/OneDrive/UCSF/algorithms/HW3/", pair[1])
                    fasta_seq = SeqIO.parse(open(A_input),"fasta")
                    for fasta in fasta_seq:
                        seq_A = str(fasta.seq).upper()
                    fasta_seqb= SeqIO.parse(open(B_input), "fasta")
                    for fasta in fasta_seqb:
                        seq_B = str(fasta.seq).upper()
                    M = scoringMatrixParse(matrix_path)
                    H = matrix(seq_A, seq_B, M, -(i+1), -(j+1))    
                    s = traceback(H, args.score_only, b=seq_B, b_="", old_i=0)
                    scores_array[x] = s
                fpr = sum(scores_array>311.8)/50
                fp_matrix[i,j] = fpr
        print(fp_matrix)

if __name__ == "__main__":
    main()

#Part 1
#--done-- Implement/comment/test Smith-Waterman algorithm
# Find best gap opening/extension penalty combination for BLOSUM50
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


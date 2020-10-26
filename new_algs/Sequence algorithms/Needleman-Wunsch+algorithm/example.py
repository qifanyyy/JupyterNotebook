from NeedlemanWunschPy.algorithms import NeedlemanWunschLinear
from NeedlemanWunschPy.substitutionmatrix import Blosum50
from NeedlemanWunschPy.score import SumOfPairs
from NeedlemanWunschPy.utils import read_fasta_as_a_list_of_pairs, totally_conserved_columns

# Initialization
seqA = read_fasta_as_a_list_of_pairs("data/test1.fasta")[0][1]
seqB = read_fasta_as_a_list_of_pairs("data/test2.fasta")[0][1]

gap_penalty = -3
matrix = Blosum50(gap_penalty)
score = SumOfPairs(matrix)

# Set to False if we don't want it
save_score_matrix_to_file = True

# Create the alignment
seqAaln, seqBaln = NeedlemanWunschLinear(seqA, seqB, gap_penalty, matrix) \
    .get_alignment(save_score_matrix_to_file)

# Save results to file
with open('output/traceback.txt', 'w') as output:
    output.write('[SEQUENCE1] ' + seqAaln + '\n' +
                 '[CONSERVED] ' + totally_conserved_columns(seqAaln, seqBaln) + '\n' +
                 '[SEQUENCE2] ' + seqBaln + '\n' +
                 '[SCORE    ] ' + str(score.compute(seqAaln, seqBaln)))
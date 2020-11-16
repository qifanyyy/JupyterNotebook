# SEQUENCE ALIGNMENT VALUES TO DETERMINE SCORE
MATCH = 5
MISMATCH = -3
GAP = -4


# Initialize score and traceback matrices
def matrix_initialization(seq1, seq2):
    nbr_lines = len(seq1) + 1
    nbr_columns = len(seq2) + 1
    score_matrix = [[0] * nbr_columns for i in range(nbr_lines)]
    traceback_matrix = [[(0, 0)] * nbr_columns for i in range(nbr_lines)]

    for i in range(1, nbr_columns):
        score_matrix[0][i] += GAP + score_matrix[0][i - 1]
        traceback_matrix[0][i] = (0, i - 1)

    for i in range(1, nbr_lines):
        score_matrix[i][0] += GAP + score_matrix[i - 1][0]
        traceback_matrix[i][0] = (i - 1, 0)

    return score_matrix, traceback_matrix


def scoring(seq1, seq2, score_matrix, traceback_matrix):
    partial = 0  # diagonal comparing result
    # Algorithm
    for i in range(1, len(seq1) + 1):
        for j in range(1, len(seq2) + 1):

            if seq1[i - 1] == seq2[j - 1]:
                partial = MATCH
            else:
                partial = MISMATCH

            up = score_matrix[i - 1][j] + GAP
            left = score_matrix[i][j - 1] + GAP
            diag = score_matrix[i - 1][j - 1] + partial
            score_matrix[i][j] = max(up, left, diag)

            if score_matrix[i][j] == up:
                traceback_matrix[i][j] = (i - 1, j)
            else:
                if score_matrix[i][j] == diag:
                    traceback_matrix[i][j] = (i - 1, j - 1)
                else:
                    traceback_matrix[i][j] = (i, j - 1)

    # The final score is in the bottom right corner cell of the score matrix
    score = score_matrix[len(seq1)][len(seq2)]

    return score, score_matrix, traceback_matrix


def needleman_wunsch(seq1, seq2):
    score_matrix, traceback_matrix = matrix_initialization(seq1, seq2)
    score, score_matrix, traceback_matrix = scoring(seq1, seq2, score_matrix, traceback_matrix)
    aligned_seq1, aligned_seq2 = alignment(seq1, seq2, traceback_matrix)

    return score_matrix, score, aligned_seq1, aligned_seq2


# Also known as traceback step
def alignment(seq1, seq2, traceback_matrix):
    # Traceback
    aligned_seq1 = ""
    aligned_seq2 = ""
    i = len(seq1)
    j = len(seq2)

    while i != 0 or j != 0:
        if traceback_matrix[i][j][0] == i - 1 and traceback_matrix[i][j][1] == j - 1:
            aligned_seq1 += seq1[i - 1]
            aligned_seq2 += seq2[j - 1]
            i -= 1
            j -= 1
        else:
            if traceback_matrix[i][j][0] == i - 1:  # lines
                aligned_seq1 += seq1[i - 1]
                aligned_seq2 += "-"
                i -= 1
            else:  # columns
                aligned_seq1 += "-"
                aligned_seq2 += seq2[j - 1]
                j -= 1

    aligned_seq1 = aligned_seq1[::-1]
    aligned_seq2 = aligned_seq2[::-1]

    return aligned_seq1, aligned_seq2

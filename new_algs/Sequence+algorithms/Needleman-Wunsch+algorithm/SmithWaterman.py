# define score matrix S1 and S2
import pandas
import numpy as np

nuc = ['A', 'G', 'C', 'T'] # Purines, Pyramidines
# match=1, mismatch=-1
match_mismatch = np.reshape((1, -1, -1, -1, -1, 1, -1, -1, -1, -1, 1, -1, -1, -1, -1, 1), (4, 4))
# score matrix:
S1 = pandas.DataFrame(match_mismatch, index=nuc, columns=nuc)
print("S1 = \n", S1)
# 2 if a = b, 1 if a b is purine or a b is pyrimidine,
# -2 if a is a purine and b is a pyrimidine or vice versa.
pur_pyr = np.reshape((2, 1, -2, -2, 1, 2, -2, -2, -2, -2, 2, 1, -2, -2, 1, 2), (4, 4))
S2 = pandas.DataFrame(pur_pyr, index=nuc, columns=nuc)
print("\nS2 = \n", S2)

# F matrix, A in the row headers (i.e. down the left side), B in column headers (i.e. across the top),
# S score matix, d linear gap penalty
def local_alignment(A, B, S, d=-2.0):
    # The dimension of the matrix
    rown = len(A) + 1
    coln = len(B) + 1

    # init 2D F matrix, shape=(len(A)+1, len(B)+1)
    F = np.zeros(shape=(rown, coln))

    # value and coordinate of the highest score in F matrix
    max_score = 0
    max_pos = None

    """
    Returns a local alignment between sequences A and B,
    S is the score matrix, and d is the penalty.
    F is the F matrix, where A is in row, B is in column.
    max_pos is the coordinate of the highest score max_score in F matrix.
    String AlignmentA and AlignmentB are the alignment. 
    """

    # go through each row in the outer loop, then each column in each row in the inner loop
    for i in range(rown):
        for j in range(coln):

            # The free leading gaps in A and B. This is what makes it a local alignment -
            # The algorithm can start matching at any point in a sequence and not be penalised
            if i == 0 or j == 0:
                # This column and row are already initialised to 0s
                continue

            # Then fill each remaining cell with the highest score out of the four options:
            # - Match or mismatch with score from S. S is indexed by the base's letter, taken from A and B
            # - Inserting a gap in A
            # - Inserting a gap in B
            # - 0 (to flag a stop in backtracing - there was no positive score leading into here)

            previousCellScore = F[i-1][j-1]
            diagonalScore = previousCellScore + S.loc[A[i-1], B[j-1]]

            gapInA = F[i][j-1] + d
            gapInB = F[i-1][j] + d

            F[i][j] = max(diagonalScore, gapInA, gapInB, 0)

            # Keep track of the max score to start back tracing from. The order of loops will ensure
            # this is the lowest then rightmost appearance of the score
            if F[i][j] >= max_score :
                max_score = F[i][j]
                max_pos = (i, j)

    # Get the alignments from tracing back
    AlignmentA, AlignmentB = trace_back_local(F, A, B, S, max_pos, d)

    # AlignmentA and AlignmentB are strings
    return AlignmentA, AlignmentB, max_score, max_pos, F

# F is matrix of scores, A and B are the sequences, S is scoring matrix indexed by base, gap is gap penalty
def trace_back_local(F, A, B, S, startingCoords, gap):
    i, j = startingCoords[0], startingCoords[1]

    if i == 0 or j == 0 or i >= np.shape(F)[0] or j >= np.shape(F)[1]:
        raise ValueError('Invalid position [%s, %s] !' % (i, j))

    AlignmentA = ""
    AlignmentB = ""

    currentCellScore = F[i][j]
    while (currentCellScore != 0) :

        # Find which direction to trace back through. The order of these conditions
        # enforces taking the high road when there are equally scored directions

        if (currentCellScore == F[i-1][j] + gap) :
            # if this score came from a previous gap in B (vertical cell):
            AlignmentA = A[i-1] + AlignmentA
            AlignmentB = "-" + AlignmentB
            i = i-1
        elif (currentCellScore == F[i-1][j-1] + S.loc[A[i-1], B[j-1]]) :
            # if this score came from the diagonal cell:
            AlignmentA = A[i-1] + AlignmentA
            AlignmentB = B[j-1] + AlignmentB
            i = i-1
            j = j-1
        else :
            # if this score came from a previous gap in A (horizontal cell):
            AlignmentA = "-" + AlignmentA
            AlignmentB = B[j-1]  + AlignmentB
            j = j-1

        currentCellScore = F[i][j]

    # string type
    return AlignmentA, AlignmentB

# https://en.wikipedia.org/wiki/Smith–Waterman_algorithm
x = "GGTTGACTA"
y = "TGTTACGG"
AlignmentA, AlignmentB, max_score, max_pos, F = local_alignment(x, y, S1*3)
print("y: ", AlignmentB, "\nx: ", AlignmentA, "\n", F,
      "\nmax score =", max_score, "\nmax score coordinate =", max_pos)

assert AlignmentB == "GTT-AC"
assert AlignmentA == "GTTGAC"
assert max_score == 13.0
"""
Hamilton Evans and Bruce Atwood
05/13/2019
Bioinformatics Algorithms
Middlebury College CSCI 0321

Linear Space Global Alignment Algorithm Helper Functions

Hirschberg's Algorithm with:
    linSpaceScore: Returns last score row of 2 sequences
    returnTurningPoint: Returns next turning point for rec call
    getMaxGlobalAlignment: NonLinear Space Global Alignment
"""

from Bio.SubsMat.MatrixInfo import pam250
import numpy as np
from itertools import product

def linSpaceScore (word1, word2, matrix=pam250, indel=5):
    """
    Helper function for linear space global alignment.
    Returns the score of 2 sequences
    (sequences are not the full sequences, cut down before fed into this alg)
    """
    score = np.zeros((len(word1)+1, len(word2)+1))
    # Inititalizing arr
    for i in range(1,len(word1)+1):
        score[i,0] = score[i-1,0] - indel
    for j in range(1,len(word2)+1):
        score[0,j] = score[0,j-1] - indel

    for i in range(1, len(word1)+1):
        for j in range(1, len(word2)+1):
            cost = matrix.get((word1[i-1], word2[j-1])) #cost from matrix
            if (cost == None):
                cost = matrix.get((word2[j-1], word1[i-1]))

            diag = score[(i-1, j-1)] + cost
            vert = score[(i-1, j)] - indel
            horiz = score[(i, j-1)] - indel

            score[i,j] = max(diag, vert, horiz) # can have negatives for global alignment

    return score[-1]

def returnTurningPoint (word1, word2):
    """
    Returning the next split point of the second sequence
    (first sequence split in half, second split by this point)
    """
    split = int(len(word1)/2)
    x1 = word1[:split]
    x2 = word1[split:]

    prefixSeq = linSpaceScore(x1, word2, pam250, 5)
    sufixSeq = linSpaceScore(x2[::-1], word2[::-1], pam250, 5)

    sum = prefixSeq+sufixSeq[::-1]
    turningPoint = sum.argmax()

    return turningPoint

def hirschbergsAlgorithm (word1, word2):
    """
    Implemented from pseudocode from the Hirschberg Algorithm Wikipedia page.
    Linear Space Global Alignment Algorithm of two sequences,
    run with careful recursion.
    """
    if (len(word1) == 0): # Base Case 1: Word1 == blank
        return ("-"*len(word2), word2)

    elif (len(word2) == 0): # Base Case 2: Word2 == blank
        return (word1, "-"*len(word1))

    elif (len(word1) == 1 or len(word2) == 1):
        # Base Case 3: 1 char left for a word.  Run nonlinear global alignment alg.
        # Only 1 letter and 1 word, makes it linear.
        word1Rec, word2Rec, score = getMaxGlobalAlignment (word1, word2)
        return (word1Rec, word2Rec)

    else: # Recurse until 1 char or no char for a sequence
        xlen = int(len(word1)/2)

        xPre = word1[:xlen]
        xSuf = word1[xlen:]

        indexMax = returnTurningPoint(word1, word2) # next mid point
        word2Rec1 = word2[:indexMax]
        word2Rec2 = word2[indexMax:]

        prefix1, prefix2 = hirschbergsAlgorithm(xPre, word2Rec1)
        suffix1, suffix2 = hirschbergsAlgorithm(xSuf, word2Rec2)

    return (prefix1+suffix1, prefix2+suffix2)

def getMaxGlobalAlignment(word1, word2):
    """
    NONLINEAR SPACE global alignment.  Used to assist Hirschberg Alg.
    Finding the max alignment of the two words with affine penalty
    Backtracking through words, returninng probable combinations
    """
    word1l, word2l = len(word1), len(word2)
    table = {(0, 0): (0, None)}

    table.update({((i, 0), (i*-5, (i-1, 0))) for i in range(1, word1l+1)}) #init table
    table.update({((0, i), (i*-5, (0, i-1))) for i in range(1, word2l+1)})

    for i, j in product(range(1, word1l+1), range(1, word2l+1)):
        cost = pam250.get((word1[i-1], word2[j-1])) #cost from pam250
        if (cost == None):
            cost = pam250.get((word2[j-1], word1[i-1]))

        # Accounting for different directions, vert, horiz, diag in approaching new square
        temp1 = table[(i-1, j-1)][0] + cost
        temp2 = table[(i-1, j)][0] - 5
        temp3 = table[(i, j-1)][0] - 5
        temp4 = max(temp1, temp2, temp3)

        if (temp1 == temp4):
            table[(i, j)] = (temp4, (i-1, j-1))
        elif (temp2 == temp4):
            table[(i, j)] = (temp4, (i-1, j))
        elif (temp3 == temp4):
            table[(i, j)] = (temp4, (i, j-1))

    score = table[(i,j)][0]
    # print(table)

    # Backtracking through, adding gaps where needed
    output1 = ""
    output2 = ""
    while (i!=0 or j!=0):
         nodePast = table[(i,j)][1] # Accessing location of tuple stored
         diag = (i-1, j-1)
         vert = (i-1, j)
         horiz = (i, j-1)

         if (diag == nodePast): # Its a match!
             output1 = word1[i-1] + output1
             output2 = word2[j-1] + output2
             j-=1
             i-=1
         elif (vert == nodePast): # Word2 needs gap!
             output1 = word1[i-1] + output1
             output2 = '-' + output2
             i-=1
         elif (horiz == nodePast): # Word1 needs gap!
             output1 = '-' + output1
             output2 = word2[j-1] + output2
             j-=1

    return output1, output2, score

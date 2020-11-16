"""
Hamilton Evans and Bruce Atwood
05/13/2019
Bioinformatics Algorithms
Middlebury College CSCI 0321

Linear Space Local Alignment Algorithm
Input: 2 Protein Sequences
Output: Optimal local alignment of sequences

Uses linear space, weighted using pam250 scoring matrix
"""
from linearSpaceGlobalAlignment import hirschbergsAlgorithm
from Bio.SubsMat.MatrixInfo import pam250
from itertools import product
import numpy as np
import time

def readFile (fileName1, fileName2):
    """
    Opening file, returning two sequences.
    """
    file1 = open(fileName1, 'r')
    file1 = file1.readlines()
    word1 = ''
    for i in range(1, len(file1)):
        word1 += file1[i].strip()

    file2 = open(fileName2, 'r')
    file2 = file2.readlines()
    word2 = ''
    for j in range(1, len(file2)):
        word2 += file2[j].strip()

    return word1, word2

def alignLetterWord (letter, word, tableIn, indexMax, matrix=pam250, indel=5):
    """
    Modified code from the Local Alignment Algorithm.
    Made to run on a 1-d array as our previous level,
    and a single letter from word1 and all of word2.
    """
    maxCount = -1
    maxJ = 0
    wordl = len(word)

    tableOut = [[],[]]
    for i in range(len(word)+1): # Init table
        tableOut[0].append(0)
        tableOut[1].append([0,0]) # for i AND j start coordinate

    for j in range(1, wordl+1):
        cost = matrix.get((letter, word[j-1])) #cost from matrix
        if (cost == None):
            cost = matrix.get((word[j-1], letter))

        diag = tableIn[0][j-1] + cost # matches and mismatches
        vert = tableIn[0][j] - indel # gaps
        horiz = tableOut[0][j-1] - indel
        best = max(diag, vert, horiz, 0) # Can be zero now for local alignment

        tableOut[0][j] = best #each table loc has highest count of the 4 options

        # Made to find the start index of our local alignment
        if (diag == best):
            prev = tableIn[1][j-1]
            if (prev == [0,0]): # If no alignment yet.  Can only start alignment on diag
                tableOut[1][j][0] = indexMax
                tableOut[1][j][1] = j - 1
            else:
                tableOut[1][j] = tableIn[1][j-1] # If there is alignment, take from prev
        elif (vert == best):
            tableOut[1][j] = tableIn[1][j]
        elif (horiz == best):
            tableOut[1][j] = tableOut[1][j-1]

        if (best > maxCount): # Storing highest overall count
            maxCount = best
            endJ = j

    score = tableOut[0][endJ] # score = maxCount of whole array
    return  endJ, score, tableOut


def linearSpaceLocalMaxScoreIndex (word1, word2, matrix = pam250, indel = 5):
    """
    Using linear space to return max score and
    beginning and end indices of both sequences.
    """

    table = [[],[]]
    for i in range(len(word2)+1):
        table[0].append(0) # to store usual dynam prog info, 1 array at a time
        table[1].append([0,0]) # to store i, j start indices for that location

    maxScore = -1
    for i in range(len(word1)):
        word1Linear = word1[i] # going letter by letter for linear space
        j, score, table = alignLetterWord (word1Linear, word2, table, i, matrix, indel)

        if (score > maxScore): # New max score!
            maxScore = score
            startI = table[1][j][0] # New start loc
            startJ = table[1][j][1]
            endI = i+1 # New end loc!
            endJ = j

    return startI, startJ, endI, endJ, maxScore

def linearSpaceLocalAlignment (word1, word2, startI, startJ, endI, endJ, maxScore):
    """
    Linear Space Local Alignment Algorithm:
    Taking 2 sequences, 2 start indices, 2 end indices, and maxScore
    Returning 2 local aligned sequences made with linear Space
    """
    word1Rec = word1[startI:endI] # portion of word used in local alignment
    word2Rec = word2[startJ:endJ]
    switch = False # condition for linear space global alignment- len(word1) > len(word2)

    if (len(word2Rec) > len(word1Rec)):
        tempStore = word1Rec
        word1Rec = word2Rec
        word2Rec = tempStore
        switch = True
    word1Aligned, word2Aligned = hirschbergsAlgorithm (word1Rec, word2Rec)

    if (switch == True): # If switched, switching back
        tempStore = word1Aligned
        word1Aligned = word2Aligned
        word2Aligned = tempStore

    return word1Aligned, word2Aligned

def main (fileName1, fileName2):
    """
    Putting all together.
    Reading file, returning indices and max score, printing max score and aligned words.
    """
    start = time.time()
    word1, word2 = readFile (fileName1, fileName2)
    print(len(word1))
    print(len(word2))
    word1 = word1[:101]
    word2 = word2[:101]
    startI, startJ, endI, endJ, maxScore = linearSpaceLocalMaxScoreIndex (word1, word2, pam250, 5)
    print(time.time() - start)
    word1Aligned, word2Aligned = linearSpaceLocalAlignment (word1, word2, startI, startJ, endI, endJ, maxScore)
    print(maxScore)
    print(word1Aligned)
    print(word2Aligned)
    print()
    print(time.time() - start)



main ('humanProteinTTN.txt', 'monkeyProteinTTN.txt')

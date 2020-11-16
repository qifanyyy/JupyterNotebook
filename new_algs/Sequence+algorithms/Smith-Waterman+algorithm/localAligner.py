#!/usr/local/bin/python3
import numpy as np
__author__ = 'Stef'

'''
This class is an implementation of the Smith-Waterman local alignment algorithm with a linear gap model.
Two sequences, either default or provided by the user in fasta format
are inputs for sequence alignment. Either default scoring parameters
or user provided (at the command line) parameters are used.
'''
class LocalAligner(object):
    #Constructor
    def __init__(self, match=None, mismatch=None, gap=None, fileP=None, fileQ=None):
        #Default arguments
        #StringQ = GCTGGAAGGCAT
        #StringP = GCAGAGCACG
        #Match Score = +5, Mismatch Score = -4, Gap Penalty = -4
        if match is None and mismatch is None and gap is None and fileP is None and fileQ is None:
            #string1
            self.q = "GCTGGAAGGCAT"
            self.stringQName = "Sequence Q"

            #string2
            self.p = "GCAGAGCACG"
            self.stringPName = "Sequence P"

            #Scoring parameter
            self.gapPen = -4
            self.mismatchPen = -4
            self.matchScore = 5

        #User has given sequences and scoring arguments to the object
        elif match is not None and mismatch is not None and gap is not None and fileP is not None and fileQ is not None:
            #Default string name if one is not present in the file
            self.stringQName = "String Q"
            self.q = self.parseFile(fileQ, 1)

            #Default string name if one is not present in the file
            self.stringQName = "String P"
            self.p = self.parseFile(fileP, 2)

            #Scoring parameters given at the command line
            self.gapPen = int(gap)
            self.mismatchPen = int(mismatch)
            self.matchScore = int(match)


        #Final sequence alignments
        self.finalQ = ""
        self.finalP = ""

        #Create a table and initialize to zero
        #We will use numpy arrays as they are generally more efficient than lists for large amounts of data (ie sequences)
        self.MatrixA = np.empty(shape=[len(self.p)+1,len(self.q)+1])

        #Create b table
        self.MatrixB = np.empty(shape=[len(self.p)+1,len(self.q)+1])

        #Store max score and location
        self.maxScore = 0
        self.maxI = None
        self.maxJ =None

    #Populates the A and B tables
    #A table holds the scores and the B table holds the direction of the optimal solution for each sub problem
    def calcTables(self):
        #insert initial blank string 1
        try:
            self.q = '-' + self.q
        except IOError:
            print("Error with sequence 1")

        #insert initial blank string 2
        try:
            self.p = '-' + self.p
        except IOError:
            print("Error with sequence 2")

        #Initialize row and column 0 for A and B tables
        self.MatrixA[:,0] = 0
        self.MatrixA[0,:] = 0
        self.MatrixB[:,0] = 0
        self.MatrixB[0,:] = 0

        for i in range(1,len(self.p)):
            for j in range(1, len(self.q)):

                #Look for match
                if self.p[i] == self.q[j]:
                    #Match found
                    self.MatrixA[i][j] = self.MatrixA[i-1][j-1] + self.matchScore
                    #3 == "diagonal" for traversing solution
                    self.MatrixB[i][j] = 3

                    #Check for max score
                    if self.MatrixA[i][j] > self.maxScore:
                        self.maxScore = self.MatrixA[i][j]
                        self.maxI = i
                        self.maxJ = j

                #Match not found
                else:
                    self.MatrixA[i][j] = self.findMaxScore(i,j)


    #Finds the maximum score either in the north or west neighbor in the A table
    #Due to the ordering, gaps are checked first
    def findMaxScore(self, i, j):

        #North score
        qDelet = self.MatrixA[i-1][j] + self.gapPen
        #West score
        pDelet = self.MatrixA[i][j-1] + self.gapPen
        #Diagonal Score
        mismatch = self.MatrixA[i-1][j-1] + self.mismatchPen

        #Determine the max score
        maxScore = max(qDelet, pDelet, mismatch)

        #Set B table
        if qDelet == maxScore:
            self.MatrixB[i][j] = 2 #2 == "up" for traversing solution

        elif pDelet == maxScore:
            self.MatrixB[i][j] = 1 #1 == "left" for traversing solution

        elif mismatch == maxScore:
            self.MatrixB[i][j] = 3 #3 == "diagonal" for traversing solution

        return maxScore

    #Calculate the alignment with the highest score by tracing back the highest scoring local solution
    #Integers:
    #3 -> "DIAGONAL" -> match
    #2 -> "UP" -> gap in string q
    #1 -> "LEFT" -> gap in string p
    #were used in the B table
    def calcAlignemnt(self, i=None, j=None):

        #Default arguments to the maximum score in the A table
        if i is None and j is None:
            i = self.maxI
            j = self.maxJ

        #Base case, end of the local alignment
        if i == 0 or j == 0:
            return

        #Optimal solution "DIAGONAL"
        if self.MatrixB[i][j] == 3:
            self.calcAlignemnt(i-1 , j-1)
            self.finalQ += self.q[j]
            self.finalP += self.p[i]

        else:
            #Optimal solution "UP"
            if self.MatrixB[i][j] == 2:
                self.calcAlignemnt(i-1, j)
                self.finalQ += '-'
                self.finalP += self.p[i]

            else:
                #Optimal solution "LEFT"
                self.calcAlignemnt(i, j-1)
                self.finalP += '-'
                self.finalQ += self.p[j]

    #Parse the input sequence file for string
    #Assumes fasta a format
    def parseFile(self, filePath, stringNumber):
        #Empty sequence
        seq = ""
        #Parse the file
        with open(filePath) as f:
            for line in f:
                #Remove new line characters
                line = line.replace('\r',"")   #Windows
                line = line.replace('\n', "")

                #Header encountered
                if line.startswith(">"):
                    if stringNumber == 2:
                        self.stringQName = line.replace('>',"")
                        continue
                    elif stringNumber == 1:
                        self.stringPName = line.replace('>',"")
                        continue
                    else:
                        continue

                #Append line
                seq += line
            f.close()
        return seq








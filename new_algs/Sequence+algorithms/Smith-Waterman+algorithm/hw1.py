#!/usr/bin/python
__author__ = "Seth Lyon" 
__email__ = "seth.lyon@yale.edu" 
__copyright__ = "Copyright 2019" 
__license__ = "GPL"
__version__ = "1.0.0"
### Usage:    python hw1.py -i <input file> -s <score file>
### Example:    python hw1.py -i input.txt -s blosum62.txt
### Note:    Smit-Waterman Algorithm
### Scripting must be done from scratch, without the use of any pre-existing packages. ### Python standard library (I/O) and numpy are allowed.
import argparse
import numpy as np


#Returns a dictionary that contains the score value for each amino acid combination
#Score values and characters contained in scoreDictionary are dictated by the scoreFile
def populateScoreDictionary(scoreLines):
    scoringDictionary = {}
    
    seqList = scoreLines[0]
    seqList = seqList.split()
    
    i = 1
    j = 1
    for i in range(1, len(scoreLines) - 1, 1):
        row = scoreLines[i]
        row = row.split()
        
        for matchValue in row[1:len(scoreLines) - 1]:
            scoringDictionary[seqList[i-1], seqList[j-1]] = int(matchValue)
            j += 1
        
        j = 1
    
    return scoringDictionary


#Populate scoreMatrix with values according to Smith Waterman algorithm
#This is done by iterating from (1,1) in scoreMatrix to (numRow - 1, numCol - 1)
#The value at scoreMatrix[i][j] is determined by the following parameters:
#    scoreMatrix[i][j] = max(scoreMatrix[i-1][j-1] + matschore[i][j],
#                            max(scoreMatrix[i][j - k] - gapCost),
#                            max(scoreMatrix[i - k][j] - gapCost),
#                            0)
#                        where 1 <= k < numCol, 1 <= l < numRow, and
#                              gapCost = openGap - n * extGap where n = k (or l) - 1
    
def populateScoreMatrix(scoreMatrix, numRow, numCol, scoreDictionary, refSeq, querySeq, openGap, extGap):
    #Smith-Waterman algorithm requires first row and first column only contain zero values, so they are not iterated through
    for i in range(1, numRow, 1):
        for j in range(1, numCol, 1):
        
            #initialize matrix that keeps track of the four possible values that can be assigned to matrix[i][j]
                #maxValue[0] corresponds to value obtained from the top-left diagonal (match/mismatch)
                #maxValue[1] corresponds to value obtained from the top (insertions)
                #maxValue[2] corresponds to value obtained from the left (deletions)
                #maxValue[3] is zero
            maxValues = np.zeros(4, np.int)
                 
            #Retrieve the match/mismatch score from the scoringDictionary
            matchscore = scoreDictionary[refSeq[i - 1], querySeq[j - 1]]
            maxValues[0] = matchscore + scoreMatrix[i -1][j - 1]
        
        
            #iterate up the rows from i - 1 to zero in the j column and find the max value - gapCost
            #numGap keeps track of how many gaps have been introduced so extGapCost penalty can be applied
            numGap = 0
            maxAbovePosition_ij = 0  
                  
            for k in range(i - 1, 0, -1):
                temp = scoreMatrix[k][j] + openGap + (numGap * extGap)
                  
                if temp > maxAbovePosition_ij:
                    maxAbovePosition_ij = temp
                      
                numGap += 1
            
        
            maxValues[1] = maxAbovePosition_ij

              
            numGap = 0
            maxLeftPosition_ij = 0
        
            for m in range(j - 1, 0, -1):
                temp = scoreMatrix[i][m] + openGap + (numGap * extGap)
                  
                if temp > maxLeftPosition_ij:
                    maxLeftPosition_ij = temp
                      
                numGap += 1
              
            maxValues[2] = maxLeftPosition_ij
            

            #store the maximum calculated value
            scoreMatrix[i][j] = np.max(maxValues)



#Finds the next optimal path indices in scoreMatrix alignment from a starting coordinate in scorMatrix
#    The next optimal position in the local alignment is determined by the following:
#        nextPostion = scoreMatrix indices at max(scoreMatrix[i - 1][j - 1], scoreMatrix[i][j - 1], scoreMatrix[i - 1][j])
#
#Note: if scoreMatrix[i - 1][j - 1] == scoreMatrix[i][j - 1] == scoreMatrix[i - 1][j],
#            then scoreMatrix[i - 1][j - 1] will be chosen as the next optimal path (matches/mismatches are preferred over insertions/deletions)
#
#Note: if scoreMatrix[i - 1][j - 1] < scoreMatrix[i][j - 1] == scoreMatrix[i - 1][j],
#            then scoreMatrix[i][j - 1] will be chosen as the next optimal path (deletions are preferred over insertions)
def traceback(optimalPath, scoreMatrix, i, j):
    if scoreMatrix[i][j] > 0:

        #Store values of the next possible path 
        #nextPositionValues[0] corresponds to top-left diagonal of current position (match/mismatch)
        #nextPositionValues[1] corresponds to left of current position (deletion)
        #nextPositionValues[2] corresponds to top of current position (insertion)
        
        nextPositionValues = np.array([scoreMatrix[i - 1][j - 1], scoreMatrix[i][j-1], scoreMatrix[i -1][j]])
    
        #check if a position with zero value is encountered, otherwise find the next maximum value
        #note: argmax finds the first position of max, so mismatches will be favored over gaps
        if np.min(nextPositionValues) == 0:
            index = np.argmin(nextPositionValues)
        else:
            index = np.argmax(nextPositionValues)
    
                #determine the coordinates in matrix that index corresponded to
        if index == 0:
            i2 = i - 1
            j2 = j - 1
    
        elif index == 1:
            i2 = i
            j2 = j - 1
        else:
            i2 = i -1
            j2 = j
    
        #Add the coordinates of the next position in the optimal path matrix
        optimalPath = np.vstack((optimalPath, [i2, j2]))
        
        #recursively call function and store the results
        optimalPath = traceback(optimalPath, scoreMatrix, i2, j2)
            
    return(optimalPath)



#Pretty prints the score matrix to the output file with row and column labels, where each label represents the a character in a sequence
#By default, elements are tab delimited
def printScoreMatrix(scoreMatrix, refSeq, querySeq, output):    
    
    rowInScoreMatrix = ['', '']
    
    for j in range(0, len(querySeq) - 1, 1):
        rowInScoreMatrix.append(querySeq[j])
    
    rowString = '\t'.join(rowInScoreMatrix)
    
    output.write(rowString + '\n')
    
    #Print the second row, which has no label and contains only zero values
    rowInScoreMatrix = [' ']
    for j in range(0, len(querySeq), 1):
        
        matrixValue = str(scoreMatrix[0][j])
        rowInScoreMatrix.append(matrixValue)
    
    rowString = '\t'.join(rowInScoreMatrix)
    
    output.write(rowString + '\n')
    
    
    #Print the third through len(refSeq) rows
    for i in range(0, len(refSeq), 1):
        
        #print the row label (column 0). The next value down the row (row 3, column 1) after this will always be zero, so the space can defined        
        rowInScoreMatrix = [refSeq[i], '0']
        
        #print the rest of the values in the row
        for j in range(1, len(querySeq), 1):
            
            matrixValue = str(scoreMatrix[i + 1][j])
            rowInScoreMatrix.append(matrixValue)
            
        rowString = '\t'.join(rowInScoreMatrix)
    
        output.write(rowString + '\n')

    output.write('\n')


#Aligns the characters in querySeq to refSeq according to the coordinates in optimalPath
#The results of the alignment are then printed to the output file
def printAlignment(optimalPath, refSeq, querySeq, output):
    
    #Flip the optimalPath so that the alignment can be performed from left to right
    optimalPath = np.flip(optimalPath, 0)
    
    #Convert sequences into a list so a queue can be used to easier access sequence characters
    rSeq = list(refSeq)
    qSeq = list(querySeq)


    #Lists for alignment    
    alignQ = []
    alignRef = []
    alignMatch = []
    
    #if alignment contains indels/mismatches
    
    if optimalPath[0][0] > 1 or optimalPath[0][1] > 1:
        num = abs(optimalPath[0][0] - optimalPath[0][1])
        
        #if alignment begins with an indel
        if num > 0:
            insertion = optimalPath[0][0] < optimalPath[0][1]
            
            if insertion:
                for i in range(0, num, 1):
                    alignQ.append(qSeq.pop(0))
                    alignRef.append(' ')
                    alignMatch.append(' ')
            
            #deletion otherwise
            else:
                for i in range(0, num, 1):
                    alignQ.append(' ')
                    alignRef.append(rSeq.pop(0))
                    alignMatch.append(' ')               
    
        
        #mismatches before alignment
        for i in range(num, max(optimalPath[0,:])):
                    alignQ.append(qSeq.pop(0))
                    alignRef.append(rSeq.pop(0))
                    alignMatch.append(' ')
    
    #start filling in alignment
    alignQ.append('(')
    alignRef.append('(')
    alignMatch.append(' ')
    
    
    for i in range(0, np.size(optimalPath, 0) - 1, 1):
        
        #Check for insertion
        if optimalPath[i][0] == optimalPath[i + 1][0]:
            alignQ.append(qSeq.pop(0))
            alignRef.append('-')
            alignMatch.append(' ')
        
        #Check for deletion
        elif optimalPath[i][1] == optimalPath[i + 1][1]:
            alignQ.append('-')
            alignRef.append(rSeq.pop(0))
            alignMatch.append(' ')
        
        #Otherwise a match/mismatch
        else:
            alignQ.append(qSeq.pop(0))
            alignRef.append(rSeq.pop(0))
            
            #If match
            if alignQ[-1] == alignRef[-1]:
                alignMatch.append('|')
            else:
                alignMatch.append(' ')

    #Local alignment is finished
    alignQ.append(')')
    alignRef.append(')')
    alignMatch.append(' ')
    
    
    #Print any deletions/insertions/mismatches that occur after the local alignment
    while len(qSeq) > 0:
        alignQ.append(qSeq.pop(0))
    
    while len(rSeq) > 0:
        alignRef.append(rSeq.pop(0))
    
    
    #Convert the lists into a string so they can be printed
    queryAlignment = ''.join(alignQ)
    matchAlignment = ''.join(alignMatch)
    refAlignment = ''.join(alignRef)
    
    #Write alignment to output file
    output.write(queryAlignment + '\n')
    output.write(matchAlignment + '\n')
    output.write(refAlignment + '\n')





def runSW(inputFile, scoreFile, openGap, extGap):
    
    ### Print input and score file names. You can comment these out.
    #print ("input file : %s" % inputFile)
    #print ("score file : %s" % scoreFile)
    #print ("open gap penalty : %s" % openGap)
    #print ("extension gap penalty : %s" % extGap)
    
    #Open the input file, extract and store the sequences
    inputSeqFile = open(inputFile, 'r')
    inputSeqLines = np.array(inputSeqFile.read().splitlines())
    inputSeqFile.close()
    
    #Line 1 in the input file is assumed to be the query sequence
    querySeq = inputSeqLines[0]
    
    #Line 2 in the input file is assumed to be the reference sequence
    refSeq = inputSeqLines[1]


    
    
    #Open the scoring file and extract data
    inputScoreFile = open(scoreFile, 'r')
    scoreLines = inputScoreFile.readlines()
    inputScoreFile.close()
    
    #Create a dictionary so that match/mismatch scores can be looked up later
    scoreDictionary = populateScoreDictionary(scoreLines)
    
    #Initialize the score matrix (n + 1, m + 1)
    #Rows correspond to the reference sequence
    #Columns correspond to the query sequence
    numRow = len(refSeq) + 1
    numCol = len(querySeq) + 1
    scoreMatrix = np.zeros((numRow, numCol), np.int)
    
    #Calculate and fill-in the scoreMatrix values
    populateScoreMatrix(scoreMatrix, numRow, numCol, scoreDictionary, refSeq, querySeq, openGap, extGap)
    


    #Find the coordinates of the max value and store in an array
    maxValueInScoreMatrix = scoreMatrix.argmax()
    maxValueCoordinates = np.asarray(np.unravel_index(maxValueInScoreMatrix, (numRow, numCol)))

    #Traceback to find the optimal path in the alignment
    optimalPath = traceback(maxValueCoordinates, scoreMatrix, maxValueCoordinates[0], maxValueCoordinates[1])
    
    

    #Write outputs to output file
    output = open("output.txt", "w")
      
    output.write("----------------------------------------------------\n")
    output.write("|    Sequences                                     |\n")
    output.write("----------------------------------------------------\n")
  
    output.write("sequence1\n")
    output.write(querySeq + '\n')
    output.write("sequence2\n")
    output.write(refSeq + '\n')
      
    output.write("----------------------------------------------------\n")
    output.write("|    Score Matrix                                  |\n")
    output.write("----------------------------------------------------\n")
    output.write('\n')
    printScoreMatrix(scoreMatrix, refSeq, querySeq, output)
    
    output.write("----------------------------------------------------\n")
    output.write("|    Best Local Alignment                          |\n")
    output.write("----------------------------------------------------\n") 
    output.write('\n')
    output.write("Alignment Score:    " + str(np.max(scoreMatrix)) + "\n")
    
    printAlignment(optimalPath, refSeq, querySeq, output)
    
    output.close()





### We need to read input file and score file.
parser = argparse.ArgumentParser(description='Smith-Waterman Algorithm')
parser.add_argument('-i', '--input', help='input file', required=True)
parser.add_argument('-s', '--score', help='score file', required=True)
parser.add_argument('-o', '--opengap', help='open gap', required=False, default=-2)
parser.add_argument('-e', '--extgap', help='extension gap', required=False, default=-1)
args = parser.parse_args()


### Run your Smith-Waterman Algorithm
runSW(args.input, args.score, args.opengap, args.extgap)
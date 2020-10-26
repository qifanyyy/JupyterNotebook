#Soroush Hajizadeh
#MSc. BioInformatics UAB 2017-2018
#Algorithms Assignment 
#learned about the algorithm over here:
#https://www.cs.sjsu.edu/~aid/cs152/NeedlemanWunsch.pdf
#blos62 taken and altered from http://biopython.org/DIST/docs/api/Bio.SubsMat.MatrixInfo-pysrc.html
#NOte: score depends on order of given strings, due to differing values for insertion and deletion
#####################################################################
#import numpy as np #just to visualize matrix / help do it
#The wanted pretty format is a bit strange, with lines when there isn't a match, but I included it as required

import sys

#Here we read from a multi.fasta and take in the first two sequences to compare. Ignoring the rest if there are more
string1 = ""
string2 = ""
firstChar = 0
with open(sys.argv[1], 'r') as f:  #open and read file, check for name which begins with >. Read from next line till next >
    for line in f:
        if (line[0] == ">"):
            firstChar += 1 #count which line we're on now
            continue #ignore line with >
        elif firstChar == 1:
            string1 += line
        elif firstChar == 2:
            string2 += line

#since we're adding lines to save cycles, instead of going through each character, we'll use built-
#in (split) function to remove \n from the final sequence.
string1 = [item for item in string1.split('\n')]
string1 = ''.join(string1)
string2 = [item for item in string2.split('\n')]
string2 = ''.join(string2)
pattern = string1  #give them the name pattern and text to match examples done in class
text = string2

#if you just want to put in your own string 1 and string 2 in the code below
#pattern = "DFAWKTQKFNGRSSKLYLGGYSALSFQSPDPPPASDFVAVAADPT"#"DFAWKTQKFNGSRNMRSSKLYLIRSSTNGGYSALSFQSPDSRNMPPPASDFVAVAADPT"
#text ="DFAWKKFNGRVSKLYLGGYSALSFQSSPDPPPDFVDVAADPT"# "DFAWKKFSFNGRVSKLYLGGYSASMFNSLSFQSSPDPPPDLKSMFVDVAADPT"

deletion = -2 #score for deletion, insertion
insertion = -4
#match = 1          In this example we're always using blos62, but match can be coded in if needed

#using dictionary to be slightly faster
blos62= {('W', 'F'): 1, ('L', 'R'): -2, ('S', 'P'): -1, ('V', 'T'): 0,
          ('Q', 'Q'): 5, ('N', 'A'): -2, ('Z', 'Y'): -2, ('W', 'R'): -3,
          ('Q', 'A'): -1, ('S', 'D'): 0, ('H', 'H'): 8, ('S', 'H'): -1,
          ('H', 'D'): -1, ('L', 'N'): -3, ('W', 'A'): -3, ('Y', 'M'): -1,
          ('G', 'R'): -2, ('Y', 'I'): -1, ('Y', 'E'): -2, ('B', 'Y'): -3,
          ('Y', 'A'): -2, ('V', 'D'): -3, ('B', 'S'): 0, ('Y', 'Y'): 7,
          ('G', 'N'): 0, ('E', 'C'): -4, ('Y', 'Q'): -1, ('Z', 'Z'): 4,
          ('V', 'A'): 0, ('C', 'C'): 9, ('M', 'R'): -1, ('V', 'E'): -2,
          ('T', 'N'): 0, ('P', 'P'): 7, ('V', 'I'): 3, ('V', 'S'): -2,
          ('Z', 'P'): -1, ('V', 'M'): 1, ('T', 'F'): -2, ('V', 'Q'): -2,
          ('K', 'K'): 5, ('P', 'D'): -1, ('I', 'H'): -3, ('I', 'D'): -3,
          ('T', 'R'): -1, ('P', 'L'): -3, ('K', 'G'): -2, ('M', 'N'): -2,
          ('P', 'H'): -2, ('F', 'Q'): -3, ('Z', 'G'): -2, ('X', 'L'): -1,
          ('T', 'M'): -1, ('Z', 'C'): -3, ('X', 'H'): -1, ('D', 'R'): -2,
          ('B', 'W'): -4, ('X', 'D'): -1, ('Z', 'K'): 1, ('F', 'A'): -2,
          ('Z', 'W'): -3, ('F', 'E'): -3, ('D', 'N'): 1, ('B', 'K'): 0,
          ('X', 'X'): -1, ('F', 'I'): 0, ('B', 'G'): -1, ('X', 'T'): 0,
          ('F', 'M'): 0, ('B', 'C'): -3, ('Z', 'I'): -3, ('Z', 'V'): -2,
          ('S', 'S'): 4, ('L', 'Q'): -2, ('W', 'E'): -3, ('Q', 'R'): 1,
          ('N', 'N'): 6, ('W', 'M'): -1, ('Q', 'C'): -3, ('W', 'I'): -3,
          ('S', 'C'): -1, ('L', 'A'): -1, ('S', 'G'): 0, ('L', 'E'): -3,
          ('W', 'Q'): -2, ('H', 'G'): -2, ('S', 'K'): 0, ('Q', 'N'): 0,
          ('N', 'R'): 0, ('H', 'C'): -3, ('Y', 'N'): -2, ('G', 'Q'): -2,
          ('Y', 'F'): 3, ('C', 'A'): 0, ('V', 'L'): 1, ('G', 'E'): -2,
          ('G', 'A'): 0, ('K', 'R'): 2, ('E', 'D'): 2, ('Y', 'R'): -2,
          ('M', 'Q'): 0, ('T', 'I'): -1, ('C', 'D'): -3, ('V', 'F'): -1,
          ('T', 'A'): 0, ('T', 'P'): -1, ('B', 'P'): -2, ('T', 'E'): -1,
          ('V', 'N'): -3, ('P', 'G'): -2, ('M', 'A'): -1, ('K', 'H'): -1,
          ('V', 'R'): -3, ('P', 'C'): -3, ('M', 'E'): -2, ('K', 'L'): -2,
          ('V', 'V'): 4, ('M', 'I'): 1, ('T', 'Q'): -1, ('I', 'G'): -4,
          ('P', 'K'): -1, ('M', 'M'): 5, ('K', 'D'): -1, ('I', 'C'): -1,
          ('Z', 'D'): 1, ('F', 'R'): -3, ('X', 'K'): -1, ('Q', 'D'): 0,
          ('X', 'G'): -1, ('Z', 'L'): -3, ('X', 'C'): -2, ('Z', 'H'): 0,
          ('B', 'L'): -4, ('B', 'H'): 0, ('F', 'F'): 6, ('X', 'W'): -2,
          ('B', 'D'): 4, ('D', 'A'): -2, ('S', 'L'): -2, ('X', 'S'): 0,
          ('F', 'N'): -3, ('S', 'R'): -1, ('W', 'D'): -4, ('V', 'Y'): -1,
          ('W', 'L'): -2, ('H', 'R'): 0, ('W', 'H'): -2, ('H', 'N'): 1,
          ('W', 'T'): -2, ('T', 'T'): 5, ('S', 'F'): -2, ('W', 'P'): -4,
          ('L', 'D'): -4, ('B', 'I'): -3, ('L', 'H'): -3, ('S', 'N'): 1,
          ('B', 'T'): -1, ('L', 'L'): 4, ('Y', 'K'): -2, ('E', 'Q'): 2,
          ('Y', 'G'): -3, ('Z', 'S'): 0, ('Y', 'C'): -2, ('G', 'D'): -1,
          ('B', 'V'): -3, ('E', 'A'): -1, ('Y', 'W'): 2, ('E', 'E'): 5,
          ('Y', 'S'): -2, ('C', 'N'): -3, ('V', 'C'): -1, ('T', 'H'): -2,
          ('P', 'R'): -2, ('V', 'G'): -3, ('T', 'L'): -1, ('V', 'K'): -2,
          ('K', 'Q'): 1, ('R', 'A'): -1, ('I', 'R'): -3, ('T', 'D'): -1,
          ('P', 'F'): -4, ('I', 'N'): -3, ('K', 'I'): -3, ('M', 'D'): -3,
          ('V', 'W'): -3, ('W', 'W'): 11, ('M', 'H'): -2, ('P', 'N'): -2,
          ('K', 'A'): -1, ('M', 'L'): 2, ('K', 'E'): 1, ('Z', 'E'): 4,
          ('X', 'N'): -1, ('Z', 'A'): -1, ('Z', 'M'): -1, ('X', 'F'): -1,
          ('K', 'C'): -3, ('B', 'Q'): 0, ('X', 'B'): -1, ('B', 'M'): -3,
          ('F', 'C'): -2, ('Z', 'Q'): 3, ('X', 'Z'): -1, ('F', 'G'): -3,
          ('B', 'E'): 1, ('X', 'V'): -1, ('F', 'K'): -3, ('B', 'A'): -2,
          ('X', 'R'): -1, ('D', 'D'): 6, ('W', 'G'): -2, ('Z', 'F'): -3,
          ('S', 'Q'): 0, ('W', 'C'): -2, ('W', 'K'): -3, ('H', 'Q'): 0,
          ('L', 'C'): -1, ('W', 'N'): -4, ('S', 'A'): 1, ('L', 'G'): -4,
          ('W', 'S'): -3, ('S', 'E'): 0, ('H', 'E'): 0, ('S', 'I'): -2,
          ('H', 'A'): -2, ('S', 'M'): -1, ('Y', 'L'): -1, ('Y', 'H'): 2,
          ('Y', 'D'): -3, ('E', 'R'): 0, ('X', 'P'): -2, ('G', 'G'): 6,
          ('G', 'C'): -3, ('E', 'N'): 0, ('Y', 'T'): -2, ('Y', 'P'): -3,
          ('T', 'K'): -1, ('A', 'A'): 4, ('P', 'Q'): -1, ('T', 'C'): -1,
          ('V', 'H'): -3, ('T', 'G'): -2, ('I', 'Q'): -3, ('Z', 'T'): -1,
          ('C', 'R'): -3, ('V', 'P'): -2, ('P', 'E'): -1, ('M', 'C'): -1,
          ('K', 'N'): 0, ('I', 'I'): 4, ('P', 'A'): -1, ('M', 'G'): -3,
          ('T', 'S'): 1, ('I', 'E'): -3, ('P', 'M'): -2, ('M', 'K'): -1,
          ('I', 'A'): -1, ('P', 'I'): -3, ('R', 'R'): 5, ('X', 'M'): -1,
          ('L', 'I'): 2, ('X', 'I'): -1, ('Z', 'B'): 1, ('X', 'E'): -1,
          ('Z', 'N'): 0, ('X', 'A'): 0, ('B', 'R'): -1, ('B', 'N'): 3,
          ('F', 'D'): -3, ('X', 'Y'): -1, ('Z', 'R'): 0, ('F', 'H'): -1,
          ('B', 'F'): -3, ('F', 'L'): 0, ('X', 'Q'): -1, ('B', 'B'): 4
       }

#pretty function, displays text the way that is requested
def pretty (topString, bottomString):
    middleString = ""
    for x in range (0, len(topString)):
        if (topString[x] == bottomString[x]):  #check for - or not to place | or not
            middleString= middleString+ "|"
        elif(topString[x] == "-"):
            middleString= middleString+ "|"
        elif(bottomString[x] == "-"):
            middleString= middleString+"|"
        else:
            middleString = middleString+" "
    print topString  #print strings on top of eachother
    print middleString
    print bottomString

#traceback function. Goes through matrix from bottom right to top left to find out which way the
#function should go.
def traceback (protein1,protein2, matrix):
    y = len(protein1)
    x = len(protein2)
    alignmentTop= ''  #top string given.
    alignmentBottom=''  #bottom string given
    while( x>0 and y>0):
        if (matrix[x][y] == "Diag" ):  #if it's to go diagonal, moves to that position.
            alignmentBottom += protein2[x-1]
            alignmentTop += protein1[y-1]
            x = x-1
            y = y-1
        elif (matrix[x][y] == "Up"):  #if up, then places "-"
            alignmentBottom += protein2[x-1]
            alignmentTop += "-"
            x = x-1
        elif (matrix[x][y] == "Left"): #if left, then places "-"
            alignmentTop += protein1[y-1]
            alignmentBottom += "-"
            y= y-1
    alignmentTop = reverse(alignmentTop)  #reverse strings as they've been read from inverse
    alignmentBottom = reverse(alignmentBottom) #reverse strings
    pretty(alignmentTop,alignmentBottom)  #call pretty to display them along with lines

def reverse(s):  #reverses string.
    str = ""
    for i in s:
        str = i + str
    return str

def blossom(position1, position2):  #used to call blossom properly. As it's only half a matrix that is read in both directions.
        if (position1, position2) in blos62:
                return blos62[position1, position2]
        else:  #If a, b doesn't work, test b,a
                return blos62[position2, position1]

        #return (-1) #If just basic 1 cost

def NW(protein1, protein2):  #NeedlemanWunsch algo!
#I decided to create a second matrix so the user can visualize using "up, diagonal and left" how
#the algorithm is working. Instead of the usual subtraction trace back. Thought it'd be cool to see
#I then use that in the traceback too!

    ##get length of sequences
    length1 = len(protein1)
    length2 = len(protein2)

    #create matrix has to be one longer in both directions for comparison and traceback
    NWMatrix =[[0 for x in range(length1+1)] for y in range(length2+1)]
    tracebackMatrix =[[" " for x in range(length1+1)] for y in range(length2+1)]  #create second matrix with blanks instead of ints

    count = 0           #fill top of matrix
    for x in range(length1):
        NWMatrix[0][x+1] = deletion+ count
        count = count + deletion
        tracebackMatrix[0][x+1] = "Left"  #this is for the second visual matrix, top row

    count=0
    for y in range(length2):   #fill bottom of matrix
        NWMatrix[y+1][0] = insertion + count
        count = count + insertion
        tracebackMatrix[y+1][0] = "Up"  #for second visual matrix, left column

    for x in range(1,length2+1):  #fills the inside
        for y in range (1,length1+1):
            qDiag = NWMatrix[x-1][y-1] + blossom(protein1[y-1], protein2[x-1]) #Adds blossom for comparison
            qUp = NWMatrix[x-1][y] + insertion  #uses insertion in case
            qleft = NWMatrix[x][y-1] + deletion  #uses deletion case
            NWMatrix[x][y] = max(qDiag, qUp, qleft)
            if (NWMatrix[x][y] == qDiag):  #placing into second matrix
                tracebackMatrix[x][y] = "Diag"
            elif (NWMatrix[x][y] == qUp):
                tracebackMatrix[x][y] = "Up"
            elif (NWMatrix[x][y] == qleft): #had just else before, but kept this just in case
                tracebackMatrix[x][y] = "Left"

    print ("Alignment Score is: "), #printing alignment score which is the last x,y position
    print(NWMatrix[x][y]) #bottom right of Matrix
    print("")
    traceback(protein1,protein2, tracebackMatrix)  #calls traceback to perform traceback

    #If you want to visualize matrix, uncomment both below, as well as the numpy import function at the topNee
#    print(np.matrix(NWMatrix))
#    print(np.matrix(tracebackMatrix))

#only function we're actuall calling below, the NeedlemanWunsch
NW(pattern,text)

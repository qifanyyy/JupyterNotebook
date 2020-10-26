#!/usr/bin/python
# Needleman-Wunsch Algorithm
# as outlined in Exploring Bioinformatics, p. 54
# Goal: Determine the optimal global alignment of two squences
# Input: Two sequences
# Output: Best, global alignment(s) of two input sequences

# Initialization
# Input the two sequences: s1 and s2

infile1 = open("short1.txt", "r");
infile1.readline()
s1 = infile1.read()
s1 = s1.replace('\n', '')
#s1 = 'CTAG'
lens1 = len(s1)

infile2 = open("short2.txt", "r");
infile2.readline()
s2 = infile2.read()
s2 = s2.replace('\n', '')
#s2 = 'CAG'
lens2 = len(s2)

N = lens1
M = lens2

# STEP 1: Build Alignment Matrix

matrix = [[0 for i in range(M+1)] for j in range(N+1)]

gap = -1
mismatch = 0
match = 1

#-----------------------------------

def printM(matrix):
	for i in range(len(matrix)):
		print (matrix[i])
	print ('---------------------')
#-----------------------------------
printM(matrix)

for i in range(1, N + 1):
    matrix[i][0] = matrix[i-1][0] + gap
printM(matrix)

for j in range(1, M + 1):
    matrix[0][j] = matrix[0][j-1] + gap
printM(matrix)

for i in range(1, N + 1):
    for j in range(1, M + 1):
        if (s1[i-1] == s2[j-1]):
            score1 = matrix[i-1][j-1] + match
        else:
            score1 = matrix[i-1][j-1] + mismatch
        score2 = matrix[i][j-1] + gap
        score3 = matrix[i-1][j] + gap
        matrix[i][j] = max(score1, score2, score3)
printM(matrix)

# STEP 2: Create Directional Strings
# ------------------------------------------------------
# Function to create directional string
def buildDirectionalString(matrix, N, M):
    dstring = ""
    currentrow = N
    currentcol = M
    while (currentrow != 0 or currentcol != 0):
        value = matrix[currentrow][currentcol]
        left = matrix[currentrow][currentcol - 1]
        top = matrix[currentrow - 1][currentcol]
        if (currentrow == 0):
            dstring = 'H' + dstring
            currentcol -= 1
        elif (currentcol == 0):
            dstring = 'V' + dstring
            currentrow -= 1
        elif left + gap == value:
            dstring = 'H' + dstring
            currentcol -= 1
        elif top + gap == value:
            dstring = 'V' + dstring
            currentrow -= 1
        else:
            dstring = 'D' + dstring
            currentrow -= 1
            currentcol -= 1
    return dstring
# ------------------------------------------------------
dstring = buildDirectionalString(matrix, N, M)
print (dstring)
# ------------------------------------------------------
# STEP 3: Build Alignments Using Directional Strings

alignment1 = ''
alignment2 = ''
matchline = ''
identity = 0 
gaps = 0

seq1pos= N-1 
seq2pos= M-1 
dirpos = len(dstring) - 1

while (dirpos >= 0):
    if (dstring[dirpos] == "D"):
        alignment1 = alignment1 + s1[seq1pos]
        alignment2 = alignment2 + s2[seq2pos]
        if s1[seq1pos] == s2[seq2pos]:
            matchline = matchline + '|'
            identity += 1
        else:
            matchline = matchline + '.'
            gap += 1
        seq1pos -= 1
        seq2pos -= 1
    elif dstring[dirpos] == "V":
        alignment1 = alignment1 + s1[seq1pos]
        alignment2 = alignment2 + '-'
        seq1pos -= 1
    else:
        alignment1 = alignment1 + '-'
        alignment2 = alignment2 + s2[seq2pos]
        seq2pos -= 1
    dirpos -= 1
# ------------------------------------------------------
print (alignment1)
print (matchline)
print (alignment2)
# ------------------------------------------------------
counts = 0
gaps = 0  
for i in range(0, len(alignment1)):
    if alignment1[i] == alignment2[i]:
        if alignment1[i] != "-":
            counts += 1
        else:
            gaps=gaps+1 
print ("Percent Identity: ")
print (100*(counts/float((len(alignment1)-gaps))))


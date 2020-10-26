#implemented by Shashank Shukla and Anil Gupta
#M.Tech 1st sem mini project
#Smith-Waterman algorithm for local alignment in python
import sys

seqA = "AAGAGAG"
seqB = "GAAGGAG"

#seqA = "ACACACTA"
#seqB = "AGCACACA"

match = 1
mismatch = 0
gap = -1

row = len(seqA)
col = len(seqB)

def new_value(curI,curJ):
    if curI == row-1 or curJ == col-1:
        return A[curI][curJ]
    else:
        maxCell = A[curI+1][curJ+1]
        
        for i in range(curI+1,row):
            maxCell = max(maxCell,A[i][curJ]+gap)
        for j in range(curJ+1,col):
            maxCell = max(maxCell,A[curI][j]+gap)
        return A[curI][curJ] + maxCell

def create_matrix(row,col,mismatch):
    A = [mismatch] * row
    for i in range(row):
        A[i] = [mismatch] * col
    return A

def initialize_matrix(row,col,seqA,seqB,match):
    for i in range(row):
        for j in range(col):
            if seqA[i] == seqB[j]:
                A[i][j] = match
    return A

def complete_matrix(row,col,gap):
    for i in range(row-1,-1,-1):
        for j in range(col-1,-1,-1):
            A[i][j] = new_value(i,j)
    return A

def print_matrix():
    for i in range(row):
        print("{}".format(A[i]))

def trace_back(i,j,action):
    if i == row-1 or j == col-1:
        return [seqA[i],seqB[i]]
    else:
        max_trace = max(A[i+1][j+1],A[i][j+1],A[i+1][j])
        if A[i+1][j+1] == max_trace:
            list = trace_back(i+1,j+1,"normal")
        elif A[i][j+1] == max_trace:
            list = trace_back(i,j+1,"skiprow")
        else:
            list = trace_back(i+1,j,"skipcol")
        
        partA = seqA[i]
        partB = seqB[j]
        if action == "skiprow":
            partA = "-"
        elif action == "skipcol":
            partB = "-"
        return [partA+list[0],partB+list[1]]

def get_middle(traced):
    middle = ""
    for k in range(0,len(traced[0])):
        mid = " "
        if traced[0][k] == traced[1][k]:
            mid = "|"
        middle = middle + mid
    return middle

#Create initial grid
A = create_matrix(row,col,mismatch)

#Create initial matches
A = initialize_matrix(row,col,seqA,seqB,match)

A = complete_matrix(row,col,gap)

#In order to show it.
#print_matrix()

traced = trace_back(0,0,"normal")
middle = get_middle(traced)

print("{}\n{}\n{}".format(traced[0],middle,traced[1]))

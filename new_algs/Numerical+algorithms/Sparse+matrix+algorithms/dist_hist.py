'''
This code implements the distance histogram representation for sparse matrices where the spatial distribution of nonzero elements of the matrix is stored in terms of histograms. 
It consists of two matrices, one for storing histograms for the rows of original matrix and other for the columns. The histogram is based on the distance between an element and the principal
diagonal of the original matrix.
'''

import numpy as np
from numpy import ndarray as Tensor 

def row_histogram(A: Tensor, r: int, BINS: int) -> Tensor:
    '''
    This function creates a row histogram for given original matrix A. 'r' is a hyperparameter to decide the number of rows in the histogram matrix (0 < r <= max(A.rows,A.columns)), so is the 'BINS' parameter, 
    to decide the number of bins in the histogram. 

    Inputs:
    A -> 2D matrix (need not be square)
    r -> number of rows in resulting histogram matrix
    BINS -> number of bins

    Output:
    R -> row histogram matrix

    Algorithm:
    1) Create zero matrix R of size 'r x BINS', which is the row histogram matrix.
    2) Calculate the scale ratio for given matrix as scaleRatio = A.height/r
    3) find the max dimension, maxDimension = max(A.height, A.width)
    4) for each non-zero entry e in A do:
        int row = e.row/scaleRatio
        bin = BINS*|e.row-e.column| / maxDimension
        R[row][bin]++
       return R
    '''
    R = np.zeros((r,BINS))
    A_rows = A.shape[0]
    A_cols = A.shape[1]
    scaleRatio = A_rows//r
    maxDimension = max(A_rows, A_cols)
    for rows in range(0,A_rows):
        for col in range(0,A_cols):
            if(A[rows][col] != 0):
                row = rows//scaleRatio
                bin = (BINS*abs(rows-col))//maxDimension
                R[row][bin] += 1
    
    return R

def column_histogram(A: Tensor, c: int, BINS: int) -> Tensor:
    '''
    This function creates a column histogram for given original matrix A. 'c' is a hyperparameter to decide the number of rows in the histogram matrix (0 < c <= max(A.rows,A.columns)), so is the 'BINS' parameter, 
    to decide the number of bins in the histogram. 

    Inputs:
    A -> 2D matrix (need not be square)
    c -> number of columns in resulting histogram matrix
    BINS -> number of bins

    Output:
    C -> column histogram matrix

    Algorithm:
    1) Create zero matrix C of size 'c x BINS', which is the column histogram matrix.
    2) Calculate the scale ratio for given matrix as scaleRatio = A.height/c
    3) find the max dimension, maxDimension = max(A.height, A.width)
    4) for each non-zero entry e in A do:
        int col = e.column/scaleRatio
        bin = BINS*|e.row-e.column| / maxDimension
        C[col][bin]++
       return C
    '''
    C = np.zeros((c,BINS))
    A_rows = A.shape[0]
    A_cols = A.shape[1]
    scaleRatio = A_cols//c
    maxDimension = max(A_rows, A_cols)
    for rows in range(0,A_rows):
        for columns in range(0,A_cols):
            if(A[rows][columns] != 0):
                col = columns//scaleRatio
                bin = (BINS*abs(rows-columns))//maxDimension
                #print(row,bin)
                C[col][bin] += 1
    
    return C

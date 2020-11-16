"""
Programmer: Chris Tralie
Purpose: To implement a implicit versions of Smith-Waterman that work on
a binary cross-similarity matrix
"""

import numpy as np
import numba

@numba.jit(nopython=True)
def Delta(a, b, gapopen = -0.5, gapext = -0.7):
    """
    Helper function for swalignimpconstrained for affine
    gap penalties
    """
    if b > 0:
        return 0
    if b == 0 and a > 0:
        return gapopen
    return gapext


@numba.jit(nopython=True)
def swconstrained(CSM, match = 1, mismatch = -1, gapopen = -0.5, gapext = -0.7):
    """
    Implicit smith waterman align with diagonal constraints
    Parameters
    ----------
    CSM: ndarray(N, M)
        A binary N x M cross-similarity matrix
    match: float
        Score for a match
    mismatch: float

    #Outputs: 1) Distance (scalar)
    #2) (N+1) x (M+1) dynamic programming matrix
    """
    N = CSM.shape[0]+1
    M = CSM.shape[1]+1
    D = np.zeros((N, M))
    maxD = 0
    for i in range(3, N):
        for j in range(3, M):
            if CSM[i-1, j-1] == 0:
                MS = mismatch
            else:
                MS = match
            #H_(i-1, j-1) + S_(i-1, j-1) + delta(S_(i-2,j-2), S_(i-1, j-1))
            d1 = D[i-1, j-1] + MS + Delta(CSM[i-2, j-2], CSM[i-1, j-1], gapopen, gapext)
            #H_(i-2, j-1) + S_(i-1, j-1) + delta(S_(i-3, j-2), S_(i-1, j-1))
            d2 = D[i-2, j-1] + MS + Delta(CSM[i-3, j-2], CSM[i-1, j-1], gapopen, gapext)
            #H_(i-1, j-2) + S_(i-1, j-1) + delta(S_(i-2, j-3), S_(i-1, j-1))
            d3 = D[i-1, j-2] + MS + Delta(CSM[i-2, j-3], CSM[i-1, j-1], gapopen, gapext)
            D[i, j] = np.max(np.array([d1, d2, d3, 0.0]))
            if (D[i, j] > maxD):
                maxD = D[i, j]
    return maxD

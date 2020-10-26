"""
@author: David Lei
@since: 26/08/2016
@modified: 

from Data Structures and Algoirthms in Python

Given a collection of n 2 dimensional matrices, we want to calculate the product

A = A0 * A1 * .. * An-1, where A is the resulting matrix and A0 .. An-1 are our collection of 2D matrices

To multiply a matrices
 [n * m] * [m * n] = [n * n] matrix, m and n represent the size of the matrix (row x col)

  2 * 3      3 * 2      2 * 2
 |1 2 3| *  |7  8 | =   |e1,1 e1,2|                 = |58   64|
 |4 5 6|    |9  10|     |e2,1 e2,2|, e = element      |139 154|
            |11 12|

e1,1 is the dot product of row 1 of matrix 1 and column 1 of matrix 2
= 1*7 + 2*9 + 3*11 = 58
e1,2 is the dot product of row 1 of matrix 1 and column 2 of matrix 2
= 1*8 + 2*10 * 3*12 = 64
and so on..

matrix multiplication is also associative meaning A*(B*C) = B*(A*C), order doesn't matter, will get same result
we can exploit this as:
let:
 - B = 2 x 10 matrix
 - C = 10 x 50 matrix
 - D = 50 x 20 matrix

B*(C*D) requires
    C*D = [10 * 50] * [50 * 20] = 10 * 50 * 20 multiplications resulting in a [10 * 20] matrix
    B*^ = [2 * 10] * [10 * 20] = 2 * 10 * 20 multiplications resulting in a [2 * 20] matrix
    overall multiplications = 10*50*20 + 2*10*20 = 10400

(B*C)*D requires
    B*C = [2 * 10] * [10 * 50] = 2 * 10 * 50 multiplications resulting in a [2 * 50] matrix
    ^*D = [2 * 50] * [50 * 20] = 2 * 50 * 20 multiplications resulting in a [2 * 20] matrix
    overall multiplications = 2*10*50 + 2*50*20 = 3000

Matrix chain product probme is to determine expression of product to minimize multiplications

Approach:

Defining Subproblems
    1. Naive: (brute force) enumerate over all possible permutations of doing so = O(2^n) exponential
    2. Better:
        - problem can be spit into sub problems
            to find Ni,j (min number of mults) for subproblem Ai * Ai+1 * .. * Aj

Characterizing optimal solutions
    - can characterize an optimal solution to a subproblem in terms of optimal solutions of its subproblems (subproblem optimality)

Can compute Ni,j by considering each place k where we can put the final multiplication and taking the minimum

"""

def matrix_chain_mult(matrix_sizes):
    """
    :param matrix_sizes: list of n+1 numbers such that the size of the kth matrix is matrix_sizes[k] x matrix_sizes[k+1]
    :return: n x n table such that tale[i][j] is the minimum number of multiplications needed to compute Ai to Aj inclusive
    """
    n = len(matrix_sizes) - 1
    table = [[0] * n for _ in range(n)]
    for b in range(1, n):
        for i in range(n-b):
            j = i + b
            #for k in range(i, j, 1):
            table[i][j] = min(table[i][k] + table[k + 1][j] + matrix_sizes[i] * matrix_sizes[k + 1] * matrix_sizes[j + 1] for k in range(i, j))
    return table

if __name__ == "__main__":
    matrix_sizes = [2, 10, 10, 50, 10, 20]
    print(matrix_chain_mult(matrix_sizes))

    # I still have no idea what is going on here but this is cool!
    # O(n^3)
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 13:15:55 2019

@author: DSU
"""

import sys
sys.path.append("..")

from mpmath import *
from bigint.bigint import MyBigIntegers

# dynamic implementation
def FibLoop(x: int) -> str:
    assert x >= 0           # input validation
    # base case
    if x <= 1: return '1'
    a, b, = MyBigIntegers('1'), MyBigIntegers('1')
    # keep adding until you reach your index
    for _ in range(x-1):
        a, b = b, a+b
    return b.ToString()

# helper method for power that multiplies matricies
def MatrixMultiply(F: list, M: list) -> None:
    # calculate each
    x = (F[0][0] * M[0][0] + 
         F[0][1] * M[1][0]) 
    y = (F[0][0] * M[0][1] + 
         F[0][1] * M[1][1]) 
    z = (F[1][0] * M[0][0] + 
         F[1][1] * M[1][0]) 
    w = (F[1][0] * M[0][1] + 
         F[1][1] * M[1][1]) 

    # replace in-place
    F[0][0] = x 
    F[0][1] = y 
    F[1][0] = z 
    F[1][1] = w

# helper method for FibMatrix that computes powers of matrices
def MatrixPower(F: list, x: int) -> None: 
    if x <= 1: return

    # multiply matrices
    MatrixPower(F, x // 2) 
    MatrixMultiply(F, F)
    
    # multiply if odd
    if x % 2: 
        # matrix to multiply by if odd
        M = [[MyBigIntegers('1'), MyBigIntegers('1')],\
             [MyBigIntegers('1'), MyBigIntegers('0')]]
        MatrixMultiply(F, M)

# matrix multiplication method
def FibMatrix(x: int) -> int:
    assert x >= 0
    # F is the matrix that is computed
    F = [[MyBigIntegers('1'), MyBigIntegers('1')],\
         [MyBigIntegers('1'), MyBigIntegers('0')]]
    # power
    MatrixPower(F, x) 
    
    return F[0][0].ToString()

# using golden ratio (only works to x==69 before precision becomes an issue)
def FibFormula(x: int) -> int:
    assert x >= 0
    sq5 = 5**0.5
    phi = (1 + sq5) / 2
    return str(round(phi ** (x+1) / sq5))

# same as FibFormula, except with more precision - only works to x==77
def FibFormulaBig(x: int) -> int:
    assert x >= 0
    sq5 = mpf(5)**0.5
    phi = (1 + sq5) / 2
    return str(round(phi ** (x+1) / sq5))
    

# list of algorithms
algorithms = [FibLoop, FibMatrix, FibFormula, FibFormulaBig]

"""
Driver code verification
Runs up to 50th fib number
"""
if __name__ == '__main__':
    for i in range(50):
        vals = [algo(i) for algo in algorithms]
        assert all(vals[0] == x for x in vals)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
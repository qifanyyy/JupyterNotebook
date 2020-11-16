# Order finding quantum subroutine of Shor's algorithm.
# Finds the s of the function f(i) = x^i mod N, i.e.
# find the smallest s such that x^s (mod N) = 1.
# Here N is the number we want to factor, and x is 
# a randomly chosen number s.t. gcd(x, N) = 1.

# Here we will use two quantum registers:
# an m qubit register, where m = 3 log N; 
# and an n qubit register, where n = log N.

import numpy as np
import math
import pretty_print_complex as ppc
from qft import * 
from qgates import * 
from measure import measure
from sample_qubits import zero_state

def find_order(a, N):
    m = int(3 * math.ceil(math.log(N, 2)))
    M = 2**m
    reg1 = zero_state(m)
    
    n = int(math.ceil(math.log(N)))
    reg2 = zero_state(n) 

    # put m register into an equal superposition
    reg1 = fqft(reg1)
    ppc.print_state(reg1)
    return 3


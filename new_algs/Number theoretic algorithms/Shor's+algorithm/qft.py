# Matrix implementation of the quantum fourier transform.
# Takes in a normalized ket implemented as an np array.

import numpy as np
import math
import cmath
from qutils import *
import qgates
import sample_qubits
import pretty_print_complex as ppc

def mqft(reg):
    """Simple matrix multiplication implementation of the QFT"""
    # dimension of the QFT
    M = len(reg)
    # the Mth root of unity
    p = complex(0, 2*math.pi / M)
    omega = cmath.exp(p)
    # the ijth entry of the QFT matrix is omega^((i-1)(j-1))
    transform = np.ones((M,M), dtype=complex)    
    for x in xrange(M):
        for y in xrange(M):
            transform[x][y] = (1 / math.sqrt(M)) * pow(omega,x*y)
    return np.dot(transform,reg)
    
def fqft(reg):
    """Circuit implementation of the QFT"""
    # dimension of the QFT
    M = len(reg)
    # number of qubits
    m = int(math.log(M, 2)) 
    # print "Number of qubits = %d" % m
    for j in xrange(m):
        # Hadamard on jth qubit
        # print "Taking H on qubit %d ..." % j
        Hj = nkron(i_kron(j), qgates.H, i_kron(m-j-1), eyes=[0,2])
        reg = np.dot(Hj, reg)
        # ppc.print_state(reg)
        # print "\n"
        # Controlled phase changes Rk on all the other qubits
        for k in xrange(2, m-j+1):
            CRk = qgates.CREMOTE(gate=qgates.Rk(k), control=j+k-1, target=j, n=m)
            reg = np.dot(CRk, reg)
    # reverse output qubits using SWAP gates
    for j in xrange(m):
        for k in xrange(m-j-1):
            # swap kth and k+1th qubit
            SWAPk = nkron(i_kron(k), qgates.SWAP, i_kron(m-k-2), eyes=[0,2])
            reg = np.dot(SWAPk, reg)

    return reg 

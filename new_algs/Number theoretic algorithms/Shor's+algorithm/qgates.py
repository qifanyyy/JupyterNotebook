# Quantum gates.
# Assumes input qubits are 1D matrices 

import numpy as np
from math import sqrt
from cmath import exp
from qutils import *
import pretty_print_complex as ppc
from sample_qubits import *

# Identity
I = np.eye(2, dtype = complex)

# Hadamard
H = sqrt(0.5) * np.array([[1, 1],[1, -1]], dtype = complex)

# NOT gate
NOT = np.array([[0, 1], [1, 0]], dtype = complex) 

# Phase flip (Z)
# acts as NOT gate in the plus/minus basis
ZNOT = np.array([[1, 0], [0, -1]], dtype = complex)

# CNOT
# takes in two-qubit system vector
# performs NOT gate on target vector if first qubit is in state 1
CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype = complex)

# SWAP gate
SWAP = np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]], dtype = complex)

# Phase gate
# performs phase shift by phi
def RPHI(phi):
    return np.array([[1,0],[0,exp(1j*phi)]], dtype = complex)

# Phase gate for QFT
def Rk(k):
    return RPHI((2*np.pi)/(2**k))

# Rotate
# takes in theta as angle of rotation in radians
def ROT(theta):
    return np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]], dtype = complex)

# Controlled phase gate
def CPG(phi):
    return np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,exp(1j*phi)]], dtype = complex)

# Projection operators 
P0 = np.array([[1,0],[0,0]], dtype = complex)
P1 = np.array([[0,0],[0,1]], dtype = complex) 

# Controlled gate between the control and target qubits in a n qubit system
# N.B. n is the number of qubits not the length of the state vector 
def CREMOTE(gate, control, target, n):
    preserve, transform = np.eye(1), np.eye(1)
    for x in xrange(n):
        if x == control:
            preserve = nkron(preserve, P0)
            transform = nkron(transform, P1)
        elif x == target:
            preserve = nkron(preserve, I, eyes=[1])
            transform = nkron(transform, gate)
        else:
            preserve = nkron(preserve, I, eyes=[1])
            transform = nkron(transform, I, eyes=[1])
    return (preserve + transform)

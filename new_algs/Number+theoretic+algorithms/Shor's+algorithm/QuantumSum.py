#Juan Daniel Torres 2020

from qiskit import QuantumCircuit, IBMQ ,Aer, execute
from qiskit.visualization import plot_histogram
from math import gcd, pi
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import randint
from qiskit.quantum_info import Statevector
%matplotlib inline

#Functions for the QFT
#Taken from qiskit textbook
#https://qiskit.org/textbook/ch-algorithms/quantum-fourier-transform.html

def qft_rotations(circuit, n):
    """Performs qft on the first n qubits in circuit (without swaps)"""
    if n == 0:
        return circuit
    n -= 1
    circuit.h(n)
    for qubit in range(n):
        circuit.cu1(pi/2**(n-qubit), qubit, n)
    # At the end of our function, we call the same function again on
    # the next qubits (we reduced n by one earlier in the function)
    qft_rotations(circuit, n)

def swap_registers(circuit, n):
    """swap"""
    for qubit in range(n//2):
        circuit.swap(qubit, n-qubit-1)
    return circuit

def qft(circuit, n):
    """QFT on the first n qubits in circuit"""
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit

def qftdag(circuit, n):
    """QFT dagger on the first n qubits in circuit"""
    swap_registers(circuit, n)
    for j in range(n):
        for m in range(j):
            circuit.cu1(-pi/float(2**(j-m)), m, j)
        circuit.h(j)
    return circuit

#Initally, we want to implement the sum operation of two numbers a and b. We do following the method described in ArXiv: https://arxiv.org/abs/quant-ph/0205095

def getPhases(binary):
    """Transform a to a set of phase shitf operations in Fourier space"""
    phases = []
    for j in range(len(binary)):
        phases.append([])
        for i in range(j,len(binary)):
            if binary[i] == '1':
                phases[j].append(2**(i-j))           
    return phases

def applyPhases(N,phases,inv,ctrl,ctrlq):
    """Several options can be included in the application of the sum phases. The inv(0 or 1) and ctrl(bool) variables control if we do sum or substraction, and if we do a controled or normal operation, respectively."""
    qr = QuantumCircuit(N)
    for i in range(N):
        for j in range(len(phases[i])):
            if ctrl:
                qr.u1((-1)**inv * pi/float(phases[i][j]),i)
            else:
                qr.cu1((-1)**inv * pi/float(phases[i][j]),ctrlq,i)
    #print(qr)
    return qr

def Q_sum(N,abin,inv,ctrl,ctrlq):
    return applyPhases(N,getPhases(abin),inv,ctrl,ctrlq)


def abstrings(a,b):
    
    if len(a) != len(b):
        m = max(len(a),len(b))
        a = '0'*(m-len(a)) + a
        b = '0'*(m-len(b)) + b
        
    a = '0'+a
    b = '0'+b
        
    return a,b

def initializeQ(qr,binary):
    """This function initializes the quantum register with b"""
    for i in range(len(binary)):
        if binary[i] == '1':
            qr.x(i)
    return qr

#Sum algorithm
def sumQFT(a,inv,ctrl,ctrlq):
    
    """
        Sum operation of two binary numbers a and b.
        
        Algorithm:
        1) Apply a QFT to the quantum register previously initialized to b
        2) Apply the single q gates from a (classical number)
        3) Apply QFT dagger to the quantum register
    """

    N = len(a)

    qr = QuantumCircuit(N)
    qr.append(qft(N),range(N))
    qr.append(Q_sum(N,a,inv,ctrl,ctrlq),range(N))
    qr.append(qftdag(N),range(N))
    return qr



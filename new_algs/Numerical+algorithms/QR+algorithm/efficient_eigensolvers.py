#@copyright to other people

import scipy.linalg as la
import numpy as np
import matplotlib.pyplot as plt
import os
from matricesGenerator import matrix_generator
#from PIM import PowerMethod
import copy
import math
#######################QR Algorithms###############################
#https://rosettacode.org/wiki/QR_decomposition#Python



def qr(A):
    m, n = A.shape
    Q = np.eye(m)
    for i in range(n - (m == n)):
        H = np.eye(m)
        H[i:, i:] = make_householder(A[i:, i])
        Q = np.dot(Q, H)
        A = np.dot(H, A)
    return Q, A


def make_householder(a):
    v = a / (a[0] + np.copysign(np.linalg.norm(a), a[0]))
    v[0] = 1
    H = np.eye(a.shape[0])
    H -= (2 / np.dot(v, v)) * np.dot(v[:, None], v[None, :])
    return H

def QR_unshifted(A, convergence_condition=0.0001):
    idx = 0
    N = A.shape[0]
    pQ = np.identity(N)

    while True:
        idx = idx + 1
        Q, R = np.linalg.qr(A)
        lam = A[0,0]
        A = np.matmul(R, Q)
        pQ = np.matmul(pQ,Q)
        # calculate the convergence condition
        if np.abs(A[0,0] - lam) < convergence_condition:
            break

    eigenv = pQ[:, 0]
    eigenv = eigenv / np.linalg.norm(eigenv)
    return eigenv, A[0,0], idx

######shifted#######

def WilkinsonShift( a, b, c):
    # Calculate Wilkinson's shift for symmetric matrices:
    delta = (a-c)/2
    return c - np.sign(delta) * b**2 /(np.abs(delta) + math.sqrt( delta**2 + b**2))

def QR_wilkinson_shift(A, convergence_condition=0.00001):
    idx = 0
    N = A.shape[0]
    pQ = np.identity(N)
    while True:
        idx = idx + 1
        lam = A[0, 0]
        # pick a shift
        mu = WilkinsonShift(A[N-2,N-2], A[N-2,N-1], A[N-1, N-1])
        Q, R = np.linalg.qr(A - mu * np.identity(N))
        A = np.matmul(R, Q) + mu * np.identity(N)
        pQ = np.matmul(pQ, Q)
        # calculate the convergence condition
        if np.abs(A[0, 0] - lam) < convergence_condition:
            break

    eigenv = pQ[:, 0]
    eigenv = eigenv / np.linalg.norm(eigenv)
    return eigenv, A[0, 0], idx


def QR_shifted(A, convergence_condition=0.00001):
    idx = 0
    N = A.shape[0]
    pQ = np.identity(N)
    while True:
        idx = idx + 1
        lam = A[0, 0]
        #pick a shift
        mu = A[N-1,N-1]
        Q, R = np.linalg.qr(A - mu * np.identity(N))
        A = np.matmul(R, Q) + mu * np.identity(N)
        pQ = np.matmul(pQ, Q)
        # calculate the convergence condition
        if np.abs(A[0, 0] - lam) < convergence_condition:
            break

    eigenv = pQ[:, 0]
    eigenv = eigenv / np.linalg.norm(eigenv)
    return eigenv, A[0, 0], idx

def QR_deflation(A, convergence_condition=0.00001):
    return
##########################Rayleigh Quotient Iteration######################

def RayleighQuotientIteration(A, convergence_condition=0.00001):
    idx = 0
    r, c = A.shape
   # initialize eigenvectors
    v = np.zeros(r)
    v[0] = 1
    # initialize eigenvalues
    lam = 1
    while True:
        idx = idx + 1
        IA = A - lam * np.identity(r)
        v_new = np.linalg.solve(IA, v)
        v_new = v_new / np.linalg.norm(v_new)
        lam_new = v_new.dot(A.dot(v_new))
        if np.abs(lam_new - lam) < convergence_condition:
            break
        lam = lam_new
        v = v_new
    return v_new, lam_new, idx

#########################Power Iteration Method#############################

def PowerMethod(A, convergence_condition=0.00001):
    idx = 0
    r, c = A.shape

    if r != c:
        raise Exception("not a square matrix")
    # initialize eigenvectors
    v = np.zeros(r)
    v[-1] = 1
    # initialize eigenvalues
    lam = v.dot(A.dot(v))
    while True:
        idx = idx + 1
        # new vector
        v_new = A.dot(v)
        v_new = v_new / np.linalg.norm(v_new)

        lam_new = v_new.dot(A.dot(v_new))
        if np.abs(lam_new - lam) < convergence_condition:
            break
        lam = lam_new
        v = v_new
    return v_new, lam_new, idx



if __name__ == '__main__':
    A, eigenvals = matrix_generator(2)
    print(eigenvals)
    print(A)
    w, v = la.eig(A)
    print(w)
    print(v)
    print("#########################")
    A = np.array([[0.44073316, 0.03219927],[0.03219927 ,0.93954406]])
    eigenvec, val = QR_shifted(A)
    print(eigenvec)
    print(val)
    print("#########################")

    eigenvec, val = QR_unshifted(A)
    print(eigenvec)
    print(val)

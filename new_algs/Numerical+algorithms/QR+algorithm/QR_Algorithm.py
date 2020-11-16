"""
author: "Kelly Rivera"
title: "QR Algorithm"
"""

##Import Python Libraries
import numpy as npy
import scipy.linalg as spl  # SciPy Linear Algebra Library


## Householder transformation method
def qr_Algorithm_HH(x, converge_range):
    m, n = x.shape
    Q_last = npy.identity(n)
    diff = 1
    
    lamb, u = spl.eig(x)
    lamb = max(npy.abs(lamb))
    
    # QR Algo using 
    while diff > converge_range:
        Q, R = npy.linalg.qr(x)
        # This update matrix A, by dot product of reverse QR 
        x = npy.dot(R, Q) 
        
        eigenvalue = npy.diag(x)  #outputs only the values on the main diaginal
        eigenvalue = max(npy.abs(eigenvalue))
        
        diff = npy.abs(lamb - eigenvalue)
        
        eigenvectors = npy.dot(Q_last, Q)
        Q_last = eigenvectors
        
        
    eigenvalues = npy.diag(x)  #outputs only the values on the main diaginal
    
    return eigenvectors, eigenvalues


## Gram-Schmidt Process
def qr_GS(x):
    m, n = x.shape
    Q = npy.zeros((m, n)) # Q is all zero
    R = npy.zeros((n, n))

    for j in range(n): #range (3) = {0,1,2}
        v = x[:, j] # x[:,0] returns the first* column* of x, x[:,1] reutrns the second column etc

        for i in range(j):
            
            Q1 = Q[:, i] #when we are here for the the first time, q = 
            R[i, j] = npy.dot(Q1, v)
            v = v - R[i, j] * Q1

        vNorm = npy.linalg.norm(v)
        R[j, j] = vNorm
        Q[:, j] = v / vNorm
    
    return Q, R

def qr_Algorithm_GS(x, converge_range):
    m, n = x.shape
    Q_last = npy.identity(n)
    diff = 1
    
    lamb, u = spl.eig(x)
    lamb = max(npy.abs(lamb))

    while diff > converge_range:
        Q, R = qr_GS(x)
        # This update matrix A, by dot product of reverse QR 
        x = npy.dot(R, Q) 
        
        eigenvalue = npy.diag(x)  #outputs only the values on the main diaginal
        eigenvalue = max(npy.abs(eigenvalue))
        
        diff = npy.abs(lamb - eigenvalue)
        
        eigenvectors = npy.dot(Q_last, Q)
        Q_last = eigenvectors
        
    eigenvalues = npy.diag(x)  #outputs only the values on the main diaginal   

    return eigenvectors, eigenvalues


## QR with Shift using the Gram-Schmidt precess 
def shiftedQR_Algorithm(x, converge_range):
    m, n = x.shape
    I = npy.identity(n)
    Q_last = npy.identity(n)
    diff = 1
   
    lamb, u = spl.eig(x)
    lamb = max(npy.abs(lamb))
    
    while diff > converge_range:
        μ = x[[n-1],[n-1]]         # shift: μ = a_nn
        Q, R = qr_GS((x - (μ*I)))
        # This update matrix A, by dot product of reverse QR 
        x = npy.dot(R, Q) + (μ*I)   # Updates matrix, by dot product of reverse QR and adding back the shift
        
        eigenvalue = npy.diag(x)  #outputs only the values on the main diaginal
        eigenvalue = max(npy.abs(eigenvalue))
        
        diff = npy.abs(lamb - eigenvalue)
        
        eigenvectors = npy.dot(Q_last, Q)
        Q_last = eigenvectors
        
    eigenvalues = npy.diag(x)  #outputs only the values on the main diaginal    
    
    return eigenvectors, eigenvalues     

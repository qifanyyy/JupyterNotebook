'''
The functions used to run Grover's algorithm
- Dense or sparse matrix calculation can be chosen by commenting out the other choice
  in the imports
- There is also an option to run Grovers through application of a series of gates the
  the register or using predetermined Oracle and Diffusion gates built from the series
  of gates. This is done by commenting out the current sections and uncommenting the
  #NOTE sections in 'grover'.
  -> Using the series method is faster
'''

import numpy as np
import math as m
import time as t
import InOut as IO
from dense import *
#from sparse import *
#from lazy import *

def numits(n):
    '''
    Determines the number of iterations of Grover's iteration required
    '''
    its = int((m.pi/4.0)*(2**n)**(1/2))

    return its

def findBinary(n, target):
    '''
    Finds the binary array for the target fock value as the same length of array as the number of
    qubits, this is used to find the application of PauliX gates in the Orcale for searching
    for the required target value
    '''
    print('\nConverting Fock value to binary array...')
    ti = t.time()
    B = [int(x) for x in bin(target)[2:]]
    while len(B) != n: #required to make matrices equal sizes
        B = np.insert(B, 0, 0)
    Binaryform = B
    print('Binary array was formed in ' + str(t.time()-ti) + ' s')

    return Binaryform

def oracleX(n, Binaryform, x, I):
    '''
    This determines the application of PauliX gates to which qubits in the register and forms
    the large matrix to by applied to the register. This is part of the Oracle and requires the
    target value in binary as an array of the same length as the number of qubits
    '''
    print('\nAssigning PauliX gates to qubits for Oracle search...')
    ti = t.time()
    #Initialise
    i = Binaryform[n-1]
    if i == 0:
        Search = x
    elif i == 1:
        Search = I

    #Loop for rest of binary value
    for i in range(n-2, -1, -1):
        if Binaryform[i] == 0:
            Search = x&Search
        elif Binaryform[i] == 1:
            Search = I&Search
    print('Assigning the PauliX gates took ' +str(t.time() - ti) + ' s')

    return Search

def formOracle(Search, cZ):
    t1 = t.time()
    print('\nForming the Oracle...')
    Oracle = Search*cZ*Search
    print('This took ' + str(t.time()-t1) + ' s')

    return Oracle

def formDiffusion(H, X, cZ):
    t1 = t.time()
    print('\nForming the Diffusion matrix...')
    Diffusion = H*X*cZ*X*H
    print('This took ' + str(t.time()-t1) + ' s\n')

    return Diffusion

def grover(q, Search, cZ, H, X, its):
    '''
    Creates a superposition state of the register and runs Grovers itertion the required
    number of times, returning the qubit reg on completion
    - As in the note at the top of the file, there is an option to run this using preformed
      Oracle and Diffusion matrices, although it is slower.
      -> done by commenting out the current iteration method and commenting in the #NOTE sections
    '''
    #Create Superposition of states
    print('\nCreating superposition state...')
    t1 = t.time()
    q = H*q
    print('Creating superposition state took ' + str(t.time()-t1) + ' s')

    # # NOTE: Test Option - can comment in and use preformed O and D method
    # Oracle = formOracle(Search, cZ)
    #
    # Diffusion = formDiffusion(H, X, cZ)

    #Grover's Iteration
    print('\nBeginning Grovers Iteration...')
    ti = t.time()
    for i in range(its):
        #Oracle
        q = Search*q
        q = cZ*q
        q = Search*q
        #Diffusion
        q = H*q
        q = X*q
        q = cZ*q
        q = X*q
        q = H*q
        #IO.hist(q)
        # # NOTE: Test Option - commented in to use pre determined O and D
        # q = Oracle*q
        # q = Diffusion*q

        if i == 0:
            print('One Grover iteration took ' + str(t.time()-ti) + ' s')
    print('All of Grovers iteration took ' + str(t.time()-ti) + ' s')

    return q

def run(args, noise):
    '''
    Runs the Grover simulation with the input of reg size and target fock in args and
    a value for noise(0 if none). This has print statements to say the current operation and timings.
    There is an option to display the Oracle and Diffusion matrices used for the current run by
    commenting in the lines below the NOTE.
    '''
    # --- Reg size and target value ---
    n = args[0]
    target = args[1]

    # --- Timer Initialise ---
    t1 = t.time()

    # --- Initialised gates ---
    print('\nInitialising gates...')
    I = Identity()
    H = Hadamard(n)   #hadamard all
    X = PauliX(n)   #paulix all
    x = PauliX()
    z = PauliZ()
    cZ = Controlled(z, n)   #controlled z all
    #for noisy use; Initialises all gates with the same noise
    if noise != 0:
        I = Noisy(I, noise[0])
        H = Noisy(H, noise[1])
        x = Noisy(x, noise[2])
        X = Noisy(X, noise[3])
        cZ = Noisy(cZ, noise[4])
    print('Gate initialisation took ' + str(t.time()-t1) + ' s')

    # --- Qreg formation ---
    print('\nForming quantum register...')
    t2 = t.time()
    q = Qubit(n)
    print('Quantum register formation took ' + str(t.time()-t2) + ' s')

    # --- Number of Iterations calculation ---
    its = numits(n)

    # --- Fock to Binary Array Conversion ---
    Binaryform = findBinary(n, target)

    # --- Oracle PauliX application dependent on Fock Target ---
    Search = oracleX(n, Binaryform, x, I)

    # --- Create Superposition and Grover's Iteration ---
    q = grover(q, Search, cZ, H, X, its)

    # --- Measure and Display ---
    q.measure()
    IO.printOut(q, target)
    tf = t.time()-t1
    print('\nThis took '+str(tf)+' s to run')
    #NOTE: Comment in to display Oracle and Diffusion matrices, can increase runtime
    #      significantly for higher number of qubits
    #IO.display(formOracle(Search, cZ))
    #IO.display(formDiffusion(H, X, cZ))
    return tf

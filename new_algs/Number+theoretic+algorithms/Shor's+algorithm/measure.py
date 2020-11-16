# Takes in a normalized vector representing system of qubits.
# "Measures" the system and returns the resulting state.

import random
import cmath 

# Say the system is in state j with probability p:
    # - The probability p that a qubit is in state j is given by
    #   the the jth amplitude multiplied by its complex conjugate.
    # - We can write p as the (sum of the first j+1 elements
    #   of the probability list) - (the sum of the first j elements).
    # - The probability that a uniformly random float n in [0,1] is in 
    #   the interval [a,b] where b-a = p is p.
    # - Therefore we find the first element  <n in the cumulative sum array.

def measure(qubits):
    random.seed()
    n = random.random()
    accum = 0
    for i in xrange(0,len(qubits)):    
        accum += qubits[i] * qubits[i].conjugate()
        if accum > n:
            return i
        i += 1 
    # signifies error
    return -1 

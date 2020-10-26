# Simulates Shor's quantum algorithm for factoring.
# Translated from MATLAB.

from fractions import gcd
import cmath
import numpy as np
from measure import measure
import random
from find_order import find_order

# Returns random number coprime to argument.
def rand_coprime(N):
    r = random.randint(2,N-1)
    while gcd(r,N) != 1:
        r = random.randint(2,N-1)
    return r

# The Shor algorithm. Calls the quantum order finding subroutine "find_order".
    # args: N, number to be factored.
    # return value: tuple (f1,f2) containing nontrivial factors of N.
def shor(N):
    # Factoring N has been reduced to the following problem:
        # Find the order r of the function f(x) = a^x (mod N) for random a.
        # If r is odd OR if a^r/2 = -1 (mod N), choose another a.
        # Otherwise, gcd(a^r/2-1,N) and gcd(a^r/2+1,N) are factors of N.
   
    # ensure we don't find a nontrivial factor with first random number
    a = rand_coprime(N) 

    r = find_order(a, N)
    return    
    while ((r % 2 == 1) or (pow(a,r/2,N) == -1)): 
        a = rand_coprime(N)
        print "Random coprime seed is %d" % a
        r = find_order(a)
        print "The order of %d^x (mod N) is %d" % (a, r) 
  
    f1 = gcd((pow(a,r/2) - 1), N)
    f2 = gcd((pow(a,r/2) + 1), N)
    
    assert(f1*f2 == N)
    print "Factored %d into %d x %d" % (N, f1, f2)
    return (f1, f2)
    

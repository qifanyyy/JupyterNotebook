#!/usr/local/bin/python3
"""
solovay_strassen.py
AUTHOR:     Peter Walker
DATE:       08 November 2015
ABSTRACT:
    This file is an implementation of the Solovay/Strassen Algorithm for
    determining if a number is prime.
    I will also attempt to make some improvements to the efficiency of the
    algorithm using ___.
"""

import sys
import math
import random
#import warnings



def jacobi(a, p):
    """
    Copied from libnum, temporarily
    http://www-math.ucdenver.edu/~wcherowi/courses/m5410/ctcprime.html
    Return Jacobi symbol (or Legendre symbol if p is prime)
    """
    s = 1
    while True:
        if p < 1:
            raise ValueError("Too small module for Jacobi symbol: {0}".format(p))
        if p & 1 == 0:
            raise ValueError("Jacobi is defined only for odd modules")
        if p == 1:
            return s

        a = a % p  #(1)
        if a == 0:
            return 0
        if a == 1:
            return s

        if a & 1 == 0:
            if p % 8 in (3, 5):  #(3)
                s = -s
            #If 'a' is even (binary of 'a' ANDed with 1 == 0), then the value is even.
            # So we shift right by 1, which removes 2**x from 'a'
            a >>= 1  #(2)
            continue

        if a % 4 == 3 and p % 4 == 3: #(4)
            s = -s

        a, p = p, a  #(4)
    return
#END DEF




def _run(P, accuracy=90):
    """
    Determines if the given value, P, is a prime number
    INPUTS:
        P : Integer, the value we are testing
        accuracy : Number, the percent certainty that the number should be prime
    RETURNS:
        True : P is prime with accuracy 'accuracy'
        False : P is not prime
    """
    #For every random number we select that returns 1, the probability that P is
    # prime is 1 - 1/2^(iterations). So, given the accuracy passed, we can deduce
    # how many iterations we need.
    NUMITERS = math.ceil( math.log(1-(accuracy/100.0), 0.5) )
    print("Testing {0} times for primeness".format(NUMITERS))
    USED = []
    CT = 0
    #For each iteration, we pick a random number that has not already been
    # used, and pass it to the _test() function. If the value returned is not 1,
    # then the number is not prime
    while (CT < NUMITERS):
        NEWRAND = random.randint(2, P)
        while (NEWRAND in USED):
            NEWRAND = random.randint(2, P)
        USED.append(NEWRAND)
        RES = pow(USED[-1], int((P-1)/2), P)

        if RES==1:
            if jacobi(USED[-1], P) != 1:
                return False
        elif RES==(P-1):
            if jacobi(USED[-1], P) != -1:
                return False
        else:
            return False

        CT+=1
    #END WHILE
    return True
#END DEF


def _run_i(P, accuracy=90):
    """
    Determines if the given value, P, is a prime number. This
      is an 'improved' version of the original algorithm, _run()
    INPUTS:
        P : Integer, the value we are testing
        accuracy : Number, the percent certainty that the number should be prime
    RETURNS:
        True : P is prime with accuracy 'accuracy'
        False : P is not prime
    """
    return False
#END DEF


def _run_t(P):
    """
    Determines if the given value, P, is a prime number. A slower version that
      goes through each number between 2 and P.
    INPUTS:
        P : Integer, the value we are testing
    RETURNS:
        True : P is prime
        False : P is not prime
    """
    _isPrime = True
    for A in range(2, (P-1)):
        RES = pow(A, int((P-1)/2), P)
        JAC = jacobi(A, P)
        if (RES not in (1, P-1)):
            _isPrime = False
        else:
            if RES==1 and JAC!=RES:
                _isPrime = False
            elif RES==(P-1) and JAC!=-1:
                _isPrime = False
        print("{0}".format(A).ljust(5),
              "Euler: {0}".format(RES).ljust(11),
              "Jacobi: {0}".format(JAC).ljust(12),
              "prime? ", _isPrime)
    #END FOR
    return _isPrime
#END DEF




def __printh():
    """Printing the help text"""
    print("SOLOVAY-STRASSEN ALGORITHM:")
    print("USAGE: FILE.py [-oeh] NUMBER [ACCURACY]")
    print("  NUMBER : Value you want to test for primeness")
    print("  -o : Test using original Solovay/Strassen algorithm. Default option")
    print("  -i : Test using 'improved' algorithm")
    print("  -t : Test, running through values incrementally.")
    print("  ACCURACY : Percent accuracy of primeness. Default 90")
    print("  -h : help screen")
    print("EXAMPLE: python3 solovay_strassen.py -o 173 95")
#END DEF


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("ERROR: Please provide some command arguements.")
        __printh()
        return

    sys.argv = sys.argv[1:]
    if sys.argv[0] == '-h':
        __printh()
        return
    #Testing that the user has given one of the three flags
    if sys.argv[0] not in ["-o", "-i", "-t", "-h"]:
        sys.argv = ["-o"] + sys.argv

    #Testing that the second value is a number (our testee)
    if (len(sys.argv)<2) or not sys.argv[1].isdigit():
        print("ERROR: You must pass in a number to this program.")
        __printh()
        return
    #Since we know we have a number, casting the string to an int
    sys.argv[1] = int(sys.argv[1])
    #One quick test to see if the number is even, by binary ANDing the value with 1
    if (sys.argv[1] & 1 == 0):
        print("{0} is NOT prime.".format(sys.argv[1]))
        return

    #Making sure we have a percent on the end of our arguments
    if len(sys.argv) < 3:
        sys.argv.append(99)
    #Split once on '.', test each half if is numeric digits
    elif not all( [part.isnumeric() for part in sys.argv[2].split(".",1)] ):
        print("ERROR: Please pass in a percent certainty for primeness.")
        __printh()
        return
    #Cast to float, and check it's value
    sys.argv[2] = float(sys.argv[2])
    if sys.argv[2] < 1 or sys.argv[2] >= 100:
        print("ERROR: Please provide a percentage between 1 and 100.")
        __printh()
        return


    #Now that we've done our tests, calling the appropiate _run() function based
    # on the given flag
    if sys.argv[0] == "-o":
        isPrime = _run(sys.argv[1], sys.argv[2])
    elif sys.argv[0] == "-i":
        isPrime = _run_i(sys.argv[1], sys.argv[2])
    elif sys.argv[0] == "-t":
        isPrime = _run_t(sys.argv[1])
        return
    else:
        print("ERROR: Something went wrong. How did you get here?")
        __printh()
        return

    if (isPrime):
        print("{0} is prime with at least {1}% certainty.".format(sys.argv[1], sys.argv[2]))
    else:
        print("{0} is NOT prime.".format(sys.argv[1]))
#END DEF


main()

#END OF LINE

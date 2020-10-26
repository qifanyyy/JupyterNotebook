import random
from ellipticCurve import *
from euclid import *
from numbertype import *
import sys
from random import randint
from Soloway_Strassen_Primality_test import *
from math import log

class _Modular(FieldElement):
    pass

def IntegersModP(p):
    class IntegerModP(_Modular):
        def __init__(self, n):
            try:
                self.n = int(n) % IntegerModP.p
            except:
                raise TypeError("Can't cast type %s to %s in __init__" % (type(n).__name__, type(self).__name__))
            self.field = IntegerModP
        #Basic arithmetic
        @typecheck
        def __add__(self, other):
            return IntegerModP(self.n + other.n)
        @typecheck
        def __sub__(self, other):
            return IntegerModP(self.n - other.n)
        @typecheck
        def __mul__(self, other):
            return IntegerModP(self.n * other.n)
        def __neg__(self):
            return IntegerModP(-self.n)
        @typecheck
        def __eq__(self, other):
            return isinstance(other, IntegerModP) and self.n == other.n
        @typecheck
        def __ne__(self, other):
            return not isinstance(other, IntegerModP) or self.n != other.n
        @typecheck
        def __divmod__(self, divisor):
            q, r = divmod(self.n, divisor.n)
            return (IntegerModP(q), IntegerModP(r))
        def inverse(self):
            x, y, d = extendedEuclideanAlgorithm(self.n, self.p)
            if d != 1:
                if d!= self.p:
                    global factor
                    factor = d
                else:
                    #fix later
                    raise Exception("It looks like you were really unlucky, and this possible edge-case has not been bothered to be fixed yet. Sorry!")
            return IntegerModP(x)
        def __abs__(self):
            return abs(self.n)
        def __str__(self):
            return str(self.n)
        def __repr__(self):
            return '%d (mod %d)' % (self.n, self.p)
        def __int__(self):
            return self.n

    IntegerModP.p = p
    IntegerModP.__name__ = 'Z/%d' % (p)
    IntegerModP.englishName = 'IntegersMod%d' % (p)
    return IntegerModP

def lenstra(n):
    ff = IntegersModP(n)
    x,y = ff(2),ff(3)
    for i in range(1,n//2-1):
        curve = Curve(ff(i), ff(1-2*i))
        print("    Trying curve: %s" % (curve))
        P = Point(x, y, curve)
        dmax = max(int(log(n, 2)**(1.61)), 20)
        for i in range (1,dmax+1):
            try:
                P = i*P
            except:
                print("    Divisible by "+str(factor))
                return factor

def primeSizeN(n):
    r = random_with_N_digits(n)
    if r % 2 == 1:
        return findPrime(r)
    else:
        return findPrime(r+1)

def findPrime(r):
    if SSTest(r):
        return r
    else:
        return findPrime(r+2)

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)
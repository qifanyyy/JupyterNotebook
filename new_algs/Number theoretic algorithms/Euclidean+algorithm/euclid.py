""" Copyright (C) 2012 Arpit Chauhan """
""" See main.py for the license """

def gcd(a,b):
    """ Returns greatest common denominator by using recursive Euclidean algorithm  """
    if b==0:
        return a
    return gcd(b, a % b)

# The following two functions are to get a modulo b, i.e. a^(-1) mod b

def extended_gcd(a, b):
    """ Recursive extended Euclidean algorithm """
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    """ Returns the inverse of a modulo m """
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return pow(x, 1, m)
        
def getrelprime(num):
    """ Returns the smallest relative prime number to num """
    for i in xrange(2, num):
        if gcd(i, num) == 1:
            return i

    
    
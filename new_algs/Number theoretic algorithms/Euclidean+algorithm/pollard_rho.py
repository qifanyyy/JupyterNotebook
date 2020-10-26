""" pollard_rho.py: Takes an integer and returns either a non-trivial factor
                    or 0. Implementation of Pollard's rho algorithm. """

from gcd import gcd

def pollard_rho(n):
    x, y, d = 2, 2, 1
    g = lambda i: (i**2 + 1)%n

    while d == 1:
        x = g(x)
        y = g(g(y))
        d = gcd(abs(x-y), n)
    
    if d == n: return 0
    else: return d

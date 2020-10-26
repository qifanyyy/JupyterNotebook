from lenstrasAlgorithm import *
from Soloway_Strassen_Primality_test import *
import sys,getopt
from math import floor,ceil

factors = []
primefactors = []

def perfectpower(n):
    n = float(n)
    latest = n
    lowest = None
    i = 2
    while latest > 2:
        if (abs((n**(1/i))-round(n**(1/i))) < 0.0000001):
            if round(n**(1/i))**i == n:
                lowest = [i, round(n**(1/i))]
        latest = n**(1/i)
        i += 1
    return lowest


def factor(n):
    print("Factoring: " + str(n))
    #check if prime
    if SSTest(n):
        print("    It is prime!")
        return [1, n]
    #check if perfect power
    if not perfectpower(n) == None:
        ret = [0]
        l = perfectpower(n)
        for i in range(l[0]):
            ret.append(l[1])
        return ret
    if n % 2 == 0:
        print("    Divisible by 2")
        primefactors.append(2)
        return [0, n//2]
    if n % 3 == 0:
        print("    Divisible by 3")
        primefactors.append(3)
        return [0, n//3]
    p = lenstra(n)
    return [0, p, n//p]

def main(argv):
    short_options = "hd:D:n:"
    long_options = ["help", "demo", "number", "demoHARD"]
    global factors
    global primefactors
    try:
        opts, args = getopt.getopt(argv, short_options, long_options)
    except getopt.GetoptError:
        print("Invalid arguments. Run eccf.py -h for usage tips")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("py eecf.py -d (--demo) d: Factor a random number with d digits\n"
                  "py eecf.py -D (--demoHARD) d: Factor a number with d digits, consisting of two primes of [n/2] digits\n"
                  "py eecf.py -n (--number) n: Factor the provided number n\n"
                  "py eecf.py -h (--help): Help")
            sys.exit()
        elif opt in ("-d", "--demo"):
            n = random_with_N_digits(int(arg))
        elif opt in ("-D", "--demoHARD"):
            n = primeSizeN(floor(int(arg)/2))*primeSizeN(ceil(int(arg)/2))
        elif opt in ("-n", "--number"):
            n = int(arg)
    print("\nTrying to factor %s\n"
          "----------------------------" % n)
    factors.append(n)
    while len(factors) > 0:
        fl = factor(factors[0])
        if fl[0] == 0:
            factors = factors + fl[1:]
            factors.pop(0)
        else:
            primefactors = primefactors + fl[1:]
            factors.pop(0)
    primefactors.sort()
    m = 1
    for p in primefactors:
        m = m * p
    print("\n -------- !DONE! -------- \n")
    print(str(n) + " = {}".format(" * ".join([str(i) for i in primefactors])))
    if not m == n:
        print("Uhh, started with %s, but this is %s" % (n, m))

if __name__ == "__main__":
    main(sys.argv[1:])
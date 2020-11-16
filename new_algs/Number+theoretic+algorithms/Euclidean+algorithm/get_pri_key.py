#!/usr/bin/python
import json, sys, hashlib, math

def usage():
    print ("""Usage:
        python get_pri_key.py student_id (i.e., qchenxiong3)""")
    sys.exit(1)

# Determine factors of n
def get_factors(n):
    p = 0
    q = 0
    
    sqrRoot = math.floor(math.sqrt(n))

    i = int(sqrRoot)

    while(i>1):

        if((n % i) == 0):
            p = i
            q = n / p
            break

        i = i-1
    
    return (p, q)

# Get d from p, q and e using Extended Euclidean Algorithm function
def get_key(p, q, e):
    d = 0
    
    phi_N = (p-1)*(q-1)

    g, x, y = egcd(e, phi_N)

    d = x % phi_N
    
    return d

# Recursive implementation of the extended Euclidean algorithm for finding GCD
# Source: https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
def egcd(a, b):

    if a == 0:
        return (b, 0, 1)

    g, y, x = egcd(b%a, a)

    return (g, x - (b//a) * y, y)

def main():
    if len(sys.argv) != 2:
        usage()

    n = 0
    e = 0

    all_keys = None
    with open("keys4student.json", 'r') as f:
        all_keys = json.load(f)

    name = hashlib.sha224(sys.argv[1].strip()).hexdigest()
    if name not in all_keys:
        print (sys.argv[1], "not in keylist")
        usage()

    pub_key = all_keys[name]
    n = int(pub_key['N'], 16)
    e = int(pub_key['e'], 16)

    print ("your public key: (", hex(n).rstrip("L"), ",", hex(e).rstrip("L"), ")")

    (p, q) = get_factors(n)
    d = get_key(p, q, e)
    print ("your private key:", hex(d).rstrip("L"))

if __name__ == "__main__":
    main()

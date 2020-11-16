#!/usr/bin/python
import json, sys, hashlib, math

def usage():
    print ("""Usage:
    python find_waldo.py student_id (i.e., qchenxiong3)""")
    sys.exit(1)

# Determine whether n1 and n2 share p or q
def is_waldo(n1, n2):
    result = False
    
    GCD = find_gcd(n1, n2)

    my_q = n1 / GCD
    waldo_q = n2 / GCD

    if (GCD != 1):
        result = True    

    return result

# Simple method for finding GCD
# Source: https://stackoverflow.com/questions/11175131/code-for-greatest-common-divisor-in-python
def find_gcd(a, b):

    while b:
        a, b = b, a%b
    return a

# Recursive implementation of the extended Euclidean algorithm for finding GCD
# Source: https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
def egcd(a, b):

    if a == 0:
        return (b, 0, 1)

    g, y, x = egcd(b%a, a)

    return (g, x - (b//a) * y, y)

#Get private key of n1 by using Extended Euclidean Algorithm to determine Greatest Common Divisor (GCD)
def get_private_key(n1, n2, e):
    d = 0
   
    p = find_gcd(n1, n2)
    q = n1 / p

    phi_N = (p-1)*(q-1)

    g, x, y = egcd(e, phi_N)

    d = x % phi_N    

    return d

def main():
    if len(sys.argv) != 2:
        usage()

    all_keys = None
    with open("keys4student.json", 'r') as f:
        all_keys = json.load(f)

    name = hashlib.sha224(sys.argv[1].strip()).hexdigest()
    if name not in all_keys:
        print (sys.argv[1], "not in keylist")
        usage()

    pub_key = all_keys[name]
    n1 = int(pub_key['N'], 16)
    e = int(pub_key['e'], 16)
    d = 0
    waldo = "dolores"

    print ("your public key: (", hex(n1).rstrip("L"), ",", hex(e).rstrip("L"), ")")

    for classmate in all_keys:
        if classmate == name:
            continue
        n2 = int(all_keys[classmate]['N'], 16)

        if is_waldo(n1, n2):
            waldo = classmate
            d = get_private_key(n1, n2, e)
            break

    print ("your private key: ", hex(d).rstrip("L"))
    print ("your waldo: ", waldo)


if __name__ == "__main__":
    main()

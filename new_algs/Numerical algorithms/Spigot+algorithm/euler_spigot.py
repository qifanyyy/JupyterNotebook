#!/usr/bin/env python
"""euler_spigot.py

Find n digits of euler's number, using the spigot algorithm
presented in "A Spigot Algorithm for the Digits of [pi]",
published in The American Mathematical Monthly, vol 2, no 3,
March of 1995, written by Stanley Rabinowitz and Stan Wagon."""

import sys

# hard limit
limit = 1000

def main():
    try:
        n = (int)(sys.argv[1])
        if n < 1:
            raise ValueError
    except(ValueError, IndexError):
        print("Usage: euler_spigot.py [n]")
        print("[n] is a positive integer")
        sys.exit(1)

    digits = [2]
    a = []
    a_len = n+2
    for i in range(a_len):
        a.append(1)

    for loop in range(n-1):
        a = [element * 10 for element in a]
        for i in range(a_len-1, -1, -1):
            denominator = i+2
            q = a[i] / denominator
            r = a[i] % denominator
            a[i] = r
            if(i>0):
                a[i-1] += q
            else:
                digits.append(q)
    print(digits)
            
        

if __name__ == "__main__":
    main()

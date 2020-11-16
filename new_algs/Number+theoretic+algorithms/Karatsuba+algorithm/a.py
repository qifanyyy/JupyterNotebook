"""

Authors:        Gabriel Duarte and Elliot Newman
Class:          CS415 Algorithm Analysis
Assignment:     Project 2
Date:           10/22/2018
Description:    Code Karatsuba's Algorithm and Exponentiation Algorithm
                to show efficiency in run time.

"""

import time


def sub(a,b):

    # Create lists
    c = []; d = []; e = []

    # Enter the strings into lists
    for i in range(len(a)):
        c.append(a[i])
    for i in range(len(b)):
        d.append(b[i])

    # Reverse the lists for ease of subtraction
    c.reverse()
    d.reverse()

    # Make sure that the lengths are the same by padding
    # with zeros where needed
    if len(c) < len(d):
        while len(c) != len(d):
            c.append('0')
    if len(d) < len(c):
        while len(c) != len(d):
            d.append('0')

    # Subtracts and checks to see if it needs to borrow
    for i in range(len(c)):
        # We only check < and not > because we always know that
        # (a0 + a1) * (b1 + b0) will be bigger than (c2 + c0)
        if c[i] < d[i]:
            c[i+1] = str(int(c[i+1]) - 1)  # Borrow
            c[i] = int(c[i]) + 10  # Add borrow to number
            e.append(str(int(c[i]) - int(d[i])))
        else:
            e.append(str(int(c[i]) - int(d[i])))
    e.reverse()  # Reverse for the correct value

    # Return as string rather than list
    return "".join(e)

def add(a, b):

    # Create list to keep track of answer and carry
    c = []
    carry = 0

    # Reverse the lists for ease of addition
    if len(a) > 1 or len(b) > 1:
        a.reverse()
        b.reverse()

    # Make sure that the lengths are the same by padding
    # with zeros where needed
    if len(b) < len(a):
        while len(b) != len(a):
            b.append('0')
    if len(a) < len(b):
        while len(a) != len(b):
            a.append('0')

    # Add the numbers and check to see if we need to carry
    for i in range(len(b)):
        result = int(a[i]) + int(b[i]) + carry
        carry = 0
        if result >= 10:
            carry = 1
            new = result % 10
            c.append(str(new))
        else:
            c.append(str(result))

    # Add the carry if > 100
    # For ex: 99 + 9 would give us 08, so we add the 1
    if carry == 1:
        c.append('1')

    c.reverse()  # Reverse for the correct value

    # Return as string rather than list
    return str("".join(c))

def karatsuba(first_num, second_num):
    # Create the arrays for storing digits by 1 digit per index
    # Also creating lists on 2 lines rather than 8 different lines
    fn = [];  sn = [];  r = [];  r1 = []
    c21 = [];  c01 = [];  p = [];  p2 = []

    # Create n for the power of 10^n and 10^(n/2)
    n = ''
    n2 = ''

    # Base case for one digit multiplications
    if len(first_num) == 1 and len(second_num) == 1:
        return int(first_num) * int(second_num)

    # Adds zeros to left for un-matching number lengths
    # For ex: 12 x 4561 would pad 12 as 0012 x 4561
    if len(first_num) < len(second_num):
        while len(first_num) != len(second_num):
            first_num = '0' + first_num
    if len(first_num) > len(second_num):
        while len(first_num) != len(second_num):
            second_num = '0' + second_num

    num_of_digits = len(first_num)

    # Split the list in half
    split = (num_of_digits // 2)
    if num_of_digits % 2 == 1:
        split += 1

    for i in range(num_of_digits):
        fn.append(first_num[i])
        sn.append(second_num[i])

    # This get the n for 10^n and 10^(n/2)
    # This is also replaces padc1 = num_of_digits - split
    # and padc2 = padc1 * 2 since we are not able to use standard operators
    padc1 = sub(str(num_of_digits), str(split))
    padc2 = karatsuba(str(padc1),'2')
    padc1 = int(padc1)

    # Create the necessary amount of zeros for
    # 10^n and 10^(n/2)
    for i in range(padc2): n += '0'
    for i in range(padc1): n2 += '0'

    # Python syntax to get the indexes from
    # [0:split] and [split:end]
    a1 = fn[:split]
    b1 = sn[:split]
    a0 = fn[split:]
    b0 = sn[split:]

    # Calculate c2, c1, c0, c
    # "".join(a1) joins elements in the list For ex: ['1','2'] would yield '12'
    c2 = str(karatsuba("".join(a1), "".join(b1)))
    c0 = str(karatsuba("".join(a0), "".join(b0)))

    # Append numbers to list so we don't exceed data type
    for i in range(len(c2)): r.append(c2[i])
    for j in range(len(c0)): r1.append(c0[j])

    # For c1 = (a1 + a0) * (b1 + b0) - (c2 + c0) the sub is on the outside, sub(x, y)
    c1 = sub(str(karatsuba(add(a1, a0), add(b1, b0))), str(add(r, r1)))

    # add the zeros (pad), this is done with string rather than integers
    c2 = str(c2) + n
    c1 = str(c1) + n2

    # Append numbers to list so we don't exceed data type
    for i in range(len(c2)): c21.append(c2[i])
    for j in range(len(c1)): c01.append(c1[j])

    # Add c2 + c1 from my function and not built in operator
    ret = str(add(c21, c01))

    # Append numbers to list so we don't exceed data type
    for i in range(len(ret)): p.append(ret[i])
    for j in range(len(c0)): p2.append(c0[j])

    # Add ret + c0, ret is the sum of c2 + c1
    c  = int(add(p, p2))
    return c


def exponentiation(a, n):

    # Create base case
    if n == 0:
        return 1

    if n % 2 == 0:
        val = exponentiation(a, n // 2)
        result = karatsuba(str(val), str(val))
    else:
        val = exponentiation(a, (n-1)//2)
        result = karatsuba(str(val), str(val))
        result = karatsuba(str(result), str(a))
    return result


def main():

    x = '0'

    # Loop until the user wants to exit
    while x != '3':

        # Ask which Task the user would like to run
        print("\n1: Karatsuba's Algorithm")
        print("2: Exponentiation")
        print("3: Quit\n")
        print("Which option would you like? ")
        x = input()

        # Run Karatsuba's Algorithm
        if x == '1':
            # Grab some input from the user
            first_num = str(input("\nPlease enter a number less than or equal to 1000: "))
            second_num = str(input("Please enter another number less than or equal to 1000: "))
            print("\nThe product of", first_num, "and", second_num, "is:", int(int(first_num) * int(second_num)))
            c = karatsuba(first_num, second_num)
            print("Product after karatsuba is: ", c)

        # Run Exponentiation Algorithm
        elif x == '2':
            # Grab some input from the user
            a = int(input("\nPlease enter a number less than or equal to 1000 for the constant: "))
            n = int(input("Please enter another number less than or equal to 1000 for the power: "))
            print("Built in power function:", pow(a, n))
            start = time.time()
            result = exponentiation(a, n)
            end = time.time()
            print("Final Value:", result)
            print("Time taken:", end - start)
            if result == pow(a, n):
                print("These match!")
                print("Number of digits:", len(str(result)))

main()

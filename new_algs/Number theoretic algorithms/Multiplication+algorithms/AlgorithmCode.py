f = open("output.txt", "w")


def twosComplement(num, BIT_LENGTH):
    '''
    Returns the Twos Complement of int type "num" as a string of length BIT_LENGTH.
    '''
    b = rjust(bin(num)[2:], BIT_LENGTH, "0")
    s = ""
    for i in b:
        if (i == "1"):
            s += "0"
        else:
            s += "1"
    return rjust(bin(int(s, 2) + 1)[2:], BIT_LENGTH, "0")


def addTwoBinNums(a, b, BIT_LENGTH):
    '''
    adds 2 numbers in binary and ignores any overflow bits the result is of BIT_LENGTH bits
    '''
    x = int(a, 2)
    y = int(b, 2)
    return rjust(bin(x + y)[2:], BIT_LENGTH, '0')


def rightShift(P):
    '''
    simple arithmetic right shift in string format
    '''
    return P[0] + P[:-1]


def leftShift(P, s):
    '''
    simple arithmetic left shift in string format
    '''
    return P[1:] + s


def binToSignedInt(a):
    '''
    binary number to it's signed integer representation
    '''
    if(a[0] == "1"):
        return -int(twosComplement(int(a[1:], 2), len(a[1:])), 2)
    else:
        return int(a, 2)


def rjust(s, l, char=" "):
    '''
    adds padding in a string on its left side.
    '''
    if len(s) > l:
        return s[-l:]
    else:
        return s.rjust(l, char)


def ljust(s, l, char=" "):
    '''
    adds padding in a string on its right side.
    '''
    if(len(s) > l):
        return s[:l]
    else:
        return s.ljust(l, char)


def multiply(Multiplicand, Multiplier):
    '''
    Multiplies two signed integers in their binary form using Booth's algorithm.
    '''
    x = len(bin(abs(Multiplicand))[2:]) + 1
    y = len(bin(abs(Multiplier))[2:]) + 1

    BIT_LENGTH = x + y + 1

    m = rjust(bin(abs(Multiplicand))[2:], x, "0")
    negm = twosComplement(abs(Multiplicand), x)
    if(Multiplicand < 0):
        m, negm = negm, m

    if(Multiplier < 0):
        r = twosComplement(Multiplier, y)
    else:
        r = rjust(bin(abs(Multiplier))[2:], y, "0")

    A = ljust(m, BIT_LENGTH, "0")
    S = ljust(negm, BIT_LENGTH, "0")
    P = rjust((r + "0"), BIT_LENGTH, "0")

    for i in range(y):
        if P[-1] == P[-2]:
            P = rightShift(P)
            continue
        if P[-1] == "0":
            P = addTwoBinNums(P, S, BIT_LENGTH)
        else:
            P = addTwoBinNums(P, A, BIT_LENGTH)
        P = rightShift(P)

    f.write(
        ("RESULT = " + str(binToSignedInt(P[:-1])) + " ( " + P[:-1] + " ) ") + "\n")
    return binToSignedInt(P[:-1])


def verifyMult():
    '''
    testing multiplication
'''
    for i in range(-TEST_SIZE, TEST_SIZE):
        for j in range(-TEST_SIZE, TEST_SIZE):
            print("Testing " + str(i) + " " + str(j), end=' ')
            if i * j != multiply(i, j):
                print ("FAILED", i, j)
                exit()
            else:
                print (".....OK")


def testDiv():
    '''
    testing division
    '''
    for i in range(-TEST_SIZE, TEST_SIZE):
        for j in range(-TEST_SIZE, TEST_SIZE):
            if i == 0 or j == 0:
                continue
            print ("TESTING ", i, j, end=" ")
            q, r = divide(i, j)
            if((i // j != q or r != i % j) and (q - 1 != i // j or r + j != i % j)):
                print()
                print (q - 1, r + j)
                print (q, r)
                print(i // j, i % j)
                print ("FAILED", i, j)
                exit()
            else:
                print("....OK")


def divide(Dividend, Divisor):
    '''
    Divides two signed integers in their binary form using Restoring Division Algorithm.
    '''
    if(Divisor == 0):
        print("ERROR: Division by 0 not defined.")
        return

    if(Dividend == 0):
        Q = "0"
        R = "0"

    elif(abs(Dividend) < abs(Divisor)):
        Q = "0"
        R = "0" + bin(abs(Dividend))[2:]
        if(Dividend < 0):
            R = twosComplement(int(R, 2), len(R))

    else:
        n = len(bin(abs(Dividend))[2:])
        BIT_LENGTH = n + 2

        Q = bin(abs(Dividend))[2:]
        M = twosComplement(abs(Divisor), BIT_LENGTH)
        R = "0" * BIT_LENGTH

        for i in range(n):
            R = leftShift(R, Q[0])
            origR = R
            R = addTwoBinNums(R, M, BIT_LENGTH)
            if R[0] == "0":
                Q = leftShift(Q, "1")
            else:
                Q = leftShift(Q, "0")
                R = origR

        R = "0" + R.lstrip("0")
        Q = "0" + Q.lstrip("0")

        if(Dividend < 0):
            R = twosComplement(int(R, 2), len(R))
        if((Dividend < 0 and Divisor > 0) or (Dividend > 0 and Divisor < 0)):
            Q = twosComplement(int(Q, 2), len(Q))

    f.write(("Quotient = " + str(binToSignedInt(Q)) + " ( " + Q + " ) ") + "\n")
    f.write("Remainder = " + str(binToSignedInt(R)) + " ( " + R + " ) \n")
    return (binToSignedInt(Q), binToSignedInt(R))


A = int(input("Enter first number: "))
B = int(input("Enter second number: "))
f.write("\nMULTIPLICATION\n")
multiply(A, B)
f.write(("\nDIVISION ( Taking Dividend = " +
         str(A) + " and Divisor = " + str(B) + " )\n"))
divide(A, B)
# TEST_SIZE = 1000
# testDiv()
# verifyMult()

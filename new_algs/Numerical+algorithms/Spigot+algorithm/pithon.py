import math


def getnumdigits():  # getting input from user, pretty simple
    print("How many digits do you want?")
    global NUM_DIGIT
    try:
        NUM_DIGIT = int(input())
        if NUM_DIGIT < 1:
            print("That's not a valid number")
            getnumdigits()
    except:
        print("That's even not a number")
        getnumdigits()


NUM_DIGIT = 0
getnumdigits()
A = []  # A is an array used by the spigot algorithm to calculate pi
digits = []  # The array that will store the digits of pi
REPEATLOOP = math.floor(10*NUM_DIGIT / 3) + 1  # times to repeat
# The [10n/3] + 1 is the minimum number of times necessary as proven by Arndt and Haenel
for i in range(1, REPEATLOOP):
    A.append(2)
for i in range(0, NUM_DIGIT):
    for i in range(0, len(A)):
        A[i] *= 10
    for i in range(len(A) - 1, -1, -1):
        numerator = (i)
        denominator = (2 * (i + 1) - 1)
        if i > 0:
            r = A[i] % denominator
            q = (A[i] - r) / denominator * numerator
            A[i] = r
            A[i-1] += q
        if i == 0:
            digits.append(int(A[i] / 10))
            A[i] = A[i] % 10
FIRSTDIG = digits.pop(0)  # should be three
print(FIRSTDIG, end='.')
for num in digits:
    print(num, end='')
print()

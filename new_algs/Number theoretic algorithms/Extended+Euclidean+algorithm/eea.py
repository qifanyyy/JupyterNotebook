from random import randint
import math


def eea(a, b):
    r = [a, b]
    s = [1, 0]
    t = [0, 1]
    q = [0]
    i = 1

    while r[i] != 0:
        i += 1
        r.append(r[i - 2] % r[i - 1])
        q.append(0)
        q[i - 1] = (r[i-2] - r[i]) / r[i - 1]
        s.append(s[i - 2] - q[i - 1] * s[i - 1])
        t.append(t[i - 2] - q[i - 1] * t[i - 1])

    array = [r[i - 1], s[i - 1], t[i - 1]]
    # print("gcd(", a, b, ") = ", r[i - 1])
    # print("Coefficient S = ", s[i - 1])
    # print("Coefficient T = ", t[i - 1])
    return array


a = eea(11069529223, 188351587)
print("1) ", a[0])

a = eea(435985, 288651)
print("2) ", a[0])


def inverse(a, b):
    array = eea(a, b)

    if array[0] == 1:
        #x = 0  # This is a place holder - need to figure out what the proper use of EEA would be in this context
        x = array[1]*a+array[2]*b
        x = x%a
    else:
        print("a is not invertible")

    if x == 1:
        return array[1]
    else:
        print("There was an error")

    '''
    t = 0
    r = b
    newt = 1
    newr = a

    while newr != 0:
        quotient = r % newr
        (t, newt) = (newt, t - quotient * newt)
        (r, newr) = (newr, r - quotient * newr)

    print(r)

    if r > 1:
        print("A is not invertible")

    if r < 0:
        t += b
        print(t)
    '''


print("3) ", inverse(300, 104759))

print("4) ", inverse(300, 104003))

'''
# This part does not work yet see page 189
def fermat(n, k):
    i = 0
    check = False

    if n < 3:
        print("Invalid n value. Please select n > 3.")

    while i < k and not check:
        i += 1
        a = randint(2, n - 2)
        compare = 1 % n

        if a^(n-1) != compare:
            print "Composite"
            check = True

    if not check:
        print "Probably prime"
    print i


# This part does not work yet see page 191
def miller(n, k):
    i = 0
    j = 1
    found = False

    while i < k:
        a = randint(0, n - 2)

        # unsure how to get this info in correct order
        r = (n - 1)/(2 ^ u)
        u = math.log2((n-1)/r)
        z = a ^ r % n

        if z != 1 & z != n-1:
            while j < u - 1:
                z = z ^ 2 % n
                if z == 1:
                    print(n, " is composite")
                    found = True
            if z != n-1:
                print(n, " is composite")
                found = True
    if not found:
        print(n, " is likely prime")

'''


def fermat(n):
    if n > 1:
        for time in range(3):
            random = randint(2, n) - 1
            if(pow(random, n - 1, n) != 1):
                return False
        return True
    else:
        return False


def miller(n):
    if n == 2:
        return True
    elif n == 1 or n % 2 == 0:
        return False

    odd = n - 1
    timesTwo = 0

    while odd % 2 == 0:
        odd = odd/2
        timesTwo = timesTwo + 1

    for time in range(3):
        while True:
            random = randint(2, n) - 1
            if random != 0 and random != 1:
                break
        randomPower = pow(random, odd, n)
        if randomPower != 1 and randomPower != n - 1:
            i = 1
            while i <= timesTwo - 1 and randomPower != n - 1:
                    randomPower = pow(randomPower, 2, n)
                    i += 1
            if randomPower != n-1:
                return False
    return True


print("Fermat for 9746347772161")
if fermat(9746347772161) == True:
    print "probably prime"
else:
    print "composite"

print("Miller-Rabin for 9746347772161")
if miller(9746347772161) == True:
    print "probably prime"
else:
    print "composite"


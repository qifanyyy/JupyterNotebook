from Division import euclidian_division as divide
from math import fabs

'''
    This method finds the gcd of two integers using the Euclid's Algorithm
'''
def gcd_euclid(a, b):
    # The gcd is independent of the sign, so keep everything positive for simplicity
    if a < 0:
        return gcd_euclid(-a, b)
    if b < 0:
        return gcd_euclid(a, -b)

    # The gcd is independent of the order, so keep a >= b, for simplicity
    if a < b:
        return gcd_euclid(b, a)

    r = divide(a, b)[1]
    # Euclid's Algorithm implementation
    while r != 0:
        a = b
        b = r
        r = divide(a, b)[1]
    return b

'''
    This method finds the Bezout coefficients of two numbers, i.e the couple (m, n) such that
        am + bn = gcd(a, b). Bezout proved that this couple always exist
    Ex: bezout_coefficients(5, 2) = (1, -2), since 5 * 1 + 2 * -2 = 1 = gcd(5, 2)
        bezout_coefficients(4, 2) = (0, 1), since 4 * 0 + 2 * 1 = 2 = gcd(4, 2)
        bezout_coefficients(20, 97) = (34, -7), since 20 * 34 + 97 * -7 = 1 = gcd(20, 97) 
'''
def bezout_coefficients(a, b):
    return __bezout_coefficients_flip(a, b, False)

'''
    This method finds the Bezout coefficients of two numbers and returns them in their initial order.
    It uses an extended version of Euclid's Algorithm, by keeping track of the quotients of the divisions
        to determine the coefficients
'''
def __bezout_coefficients_flip(a, b, flipped):
    if fabs(a) < fabs(b):
        return __bezout_coefficients_flip(b, a, True)
    # If b divides a, then gcd(a, b) = b, so we have a * 0 + b * 1 = b = gcd(a, b). The Bezout
    #   coefficients in this case are (0, 1)
    if a % b == 0:
        # Reverse the order in case a and b were flipped before
        if flipped:
            return 1, 0
        else:
            return 0, 1
    # From now on, x_n and y_n are the coefficients such that a_n * x_n + b_n * y_n = r_n, where
    #   a_n, b_n, q_n and r_n are the respective values of a, b, q and r after the n_th iteration.
    # I have proven mathematically the following recurrence relationships:
    #   x_0 = 1, x_1 = -q_1, x_n = x_n-2 - q_n * x_n-1
    #   y_0 = -q_0, y_1 = 1 - y_0 * q_1, y_n = y_n-2 - q_n * y_n-1
    q, r = divide(a, b)
    x_0 = 1
    y_0 = -q

    a = b
    b = r
    q, r = divide(a, b)
    if r != 0:
        x_1 = -q
        y_1 = 1 - y_0 * q
        while r != 0:
            a = b
            b = r
            q, r = divide(a, b)
            # Update x_n using the recurrence relationships
            x_2 = x_0 - q * x_1
            y_2 = y_0 - q * y_1
            # Instead of keeping track of all the iteration, keep track of the
            #   n_th, n-1_th and n-2_th, using the variables x_2, x_1, x_0, respectively
            x_0 = x_1
            y_0 = y_1
            x_1 = x_2
            y_1 = y_2
    if flipped:
        # Reverse the order in case a and b were flipped
        return y_0, x_0
    else:
        return x_0, y_0

'''
    This method returns true if two given numbers are prime, false otherwise.
    Two numbers a and b are prime if gcd(a, b) = 1
'''
def arePrime(a, b):
    return gcd_euclid(a, b) == 1

'''
    This method returns the lowest common multiple of two given numbers a and b from
        scratch, i.e looping through the multiples of a and finding the smallest one that
        is also a multiple of b. More efficient when one of the numbers is significantly
        greater than the other
'''
def lcm_from_scratch(a, b):
    if a < 0 or b < 0:
        a = int(fabs(a))
        b = int(fabs(b))
    if a < b:
        return lcm_from_scratch(b, a)
    i = 1
    # Loop through the multiples of the a and find the first multiple of b in there
    while True:
        current = a * i
        if current % b == 0:
            return current
        i = i + 1

'''
    This method finds the lowest common multiples of two given numbers a and b by
        finding their gcd first, then using the formula gcd(a, b) * lcm(a, b) = |a * b|
'''
def lcm_from_gcd(a, b):
    return int(fabs(a * b) / gcd_euclid(a, b))


'''
    This method solves the diophantine equation ax + by = c
    Ex: diophantine_equation(6,4,16) = ((2, 8), (-3, -8)), meaning x = 2k + 8, y = -3k - 8, k being an integer
'''
def diophantine_equation(a, b, c):
    # Limit cases
    if a == 0:  # The equation becomes by = c
        if b == 0:  # The equation becomes 0 = c
            if c == 0:
                raise ValueError("Any couple of integers (x, y) is a solution")
            else:
                raise ValueError("No solution")
        else:
            if c % b == 0:
                return (1, 0), (0, c // b)
            else:
                raise ValueError("No solution")
    else:
        if b == 0:  # The equation becomes ax = c
            if c % a == 0:
                return (0, c // a), (1, 0)
            else:
                raise ValueError("No solution")

    # If a and b are both nonzero
    gcd = gcd_euclid(a, b)
    if c % gcd != 0:
        raise ValueError("No solution")
    # Simplify the equation by dividing by the gcd
    a = a // gcd
    b = b // gcd
    c = c // gcd
    m, n = bezout_coefficients(a, b)
    return (b, c * m), (-a, c * n)

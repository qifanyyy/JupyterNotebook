# This script requires Python version 3.5 or higher and the NumPy library.
import math
import numpy as np

# Looking for the inverse of b in mod a, example values: a = 1155, b = 862 
a = 1156
b = 862


solve_inverse = True


def inverse_euclidean(a, b):
    U = np.array([a, 1, 0], dtype='int64')
    V = np.array([b, 0, 1], dtype='int64')
    print("Input: U =", U, ", V =", V)

    while V[0] > 0:
        W = U - math.floor(U[0] / V[0]) * V
        U = V
        V = W

    return U

try:
    gcd = math.gcd(a, b)
except:
    pass

if a < 1 or b < 1 or type(a) is not int or type(b) is not int:
    print("a and b must be positive integers")

elif a < b:
    print("a must be greater or equal to b")

elif gcd > 1 and solve_inverse:
    print("gcd({},{}) > 1 => extended euclidean algorithm cannot be used.".format(a, b))

else:
    U = inverse_euclidean(a, b)
    x = U[1]
    y = U[2]
    inv = y % a  # the inverse of b

    print("Result: U =", U, "\n")
    # Test if the algorithm worked correctly and print the results
    print("Testing if the algorithm worked as intended:")
    test1 = U[0] == gcd
    test2 = a * x + b * y == gcd
    test3 = inv*b % a == 1

    print("U(1) = gcd({},{}) = {} || {}".format(a, b, gcd, test1))
    print("x*a + y*b = ({}*{}) + ({}*{}) = {} || {}".format(x, a, y, b, a*x+b*y, test2))
    if solve_inverse:
        print("{}*{} ≡ {} (mod {}) || {}".format(b, inv, (b*inv) % a, a, test3))

    if test1 and test2 and test3 and solve_inverse:
        s = str(a).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))
        print("\nAlgorithm worked as expected, therefore:")
        print("Result: {}⁻¹ = {} in Z{}".format(b, inv, s))

    elif solve_inverse:
        print("Something went wrong! :(")

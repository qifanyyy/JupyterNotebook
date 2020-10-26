#!../venv/Scripts/python.exe
# -*- encoding : utf-8 -*-

"""
@Description:  classical.py provides classical algorithm required to reduce factoring problem to period finding problem
@Author: Quentin Delamea
@Copyright: Copyright 2020, PyShor
@Credits: [Quentin Delamea]
@License: MIT
@Version: 0.0.1
@Maintainer: Quentin Delamea
@Email: qdelamea@gmail.com
@Status: Dev
"""

# Standard lib imports
import random as rd

# External libs imports
import numpy as np


def _miller_test(n: int, d: int) -> bool:
    # Pick a random number a in range [2, n - 2]
    a = rd.randrange(2, n - 1)
    x = np.power(a, d) % n

    if x == 1 or x == n - 1:
        return True

    while d != n - 1:
        x = np.power(x, 2) % n
        print(x)
        if x == 1:
            return False
        elif x == n - 1:
            return True


def is_prime_number(n: int, k: int = 40) -> bool:
    """
    Performs the primarily test using Miller-Rabin's algorithm.
    See: https://gist.github.com/Ayrx/5884790

    :param n: (int) number on which the test is performed
    :param k: (int) number of round, by default equal to 40 the optimal number

    :return: (bool) True if n is a prime number, False otherwise
    """

    # Miller-Robina's test handle odd integer greater than three.
    if not isinstance(n, int):
        raise TypeError('the argument passed to the function must be an integer')
    elif n < 0:
        raise ValueError('number must be a positive integer')
    elif n <= 1:
        return False
    elif n == 2:
        return True
    if n % 2 == 0:
        return False

    # Now we can perform the Miller-Robina's test
    # We find r and d such as n = 2^r * d + 1 with d an odd integer
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Witness loop
    for _ in range(k):

        if not _miller_test(n, d):
            return False

    return True

    #     # Now we perform the Miller's test
    #
    #     # Pick a number in [2, n - 2]
    #     a = rd.randrange(2, n - 1)
    #     x = np.power(a, d) % n
    #
    #     if x == 1 or x == n - 1:
    #         return True
    #
    #     # Repeat r - 1 times
    #     for _ in range(r - 1):
    #         x = np.power(x, 2) % n
    #         if x == n - 1:
    #             return True
    # return False


class NotPrimerPowerException(Exception):
    """
    Exception raised when a non prime power is given to the following function.
    """
    pass


def primer_power(n: int) -> int:
    """
    Returns the prime number to write it in prime power.

    :param n: (int) the integer such as n = root^power with p a prime number

    :return: (int) the root

    :except NotPrimerPowerException: raised if the argument passed to the function is not a primer power
    """

    # n = root^power implies power <= log(n), so we iterate over all possible powers and check if the root is an integer
    for power in range(1, int(np.trunc(np.log(n))) + 1):
        root = int(np.trunc(np.power(n, 1./power)))
        if np.power(root, power) == n:
            if is_prime_number(root):
                return root
    raise NotPrimerPowerException


def gcd(x: int, y: int) -> int:
    """
    Computes the GCD (Greatest Common Divisor) of two numbers using Euclid's algorithm.

    :param x: (int) first number
    :param y: (int) second number

    :return: (int) the greatest common divider
    """
    if x < y:
        return gcd(y, x)
    while y != 0:
        (x, y) = (y, x % y)
    return x


def continued_fraction_expansion(n: int, b: int, q: int) -> int:
    """
    Extracts the period knowing the final state measured on the quantum computer at the end of Shor's algorithm
    execution. This extraction is performed using continued fraction expansion.

    :param n: (int) the integer we want to factorize
    :param b: (int) the measured state expressed in decimal base
    :param q: (int) the length of the first register use in Shor's algorithm

    :return: (int) the period researched in Shor's algorithm
    """

    # Initialize the float whose fractional expansion is looking for
    x = b/q
    print('n : ', n)
    print('b : ', b)
    print('q : ', q)
    print('x : ', x)

    # Compute the two first value of the expansion
    a_seq = [int(np.trunc(x))]
    if x == a_seq[-1]:
        raise ValueError('fail to find the period')
    x = 1 / (x - a_seq[-1])

    a_seq.append(int(np.trunc(x)))
    if x == a_seq[-1]:
        raise ValueError('fail to find the period')
    x = 1 / (x - a_seq[-1])

    # Init p and q sequences
    p_seq = [a_seq[0], a_seq[0] * a_seq[1] + 1]
    q_seq = [1, a_seq[1]]

    # Continue the expansion until the period i
    while q_seq[-1] < n:
        print('a_seq : ', a_seq)
        print('x : ', x)
        print('p_seq : ', p_seq)
        print('q_seq : ', q_seq)
        a_seq.append(int(np.trunc(x)))
        p_seq.append(a_seq[-1] * p_seq[-1] + p_seq[-2])
        q_seq.append(a_seq[-1] * q_seq[-1] + q_seq[-2])

        # If |b/q - p_n/q_n| < 1/q with q_n < n then r = q_n so the function returns the period
        if np.abs(b/q - p_seq[-1] / q_seq[-1]) < 1 / (2 * q):
            return q_seq[-1]

        if x == a_seq[-1]:
            raise ValueError('fail to find the period')
        x = 1/(x - a_seq[-1])

    # There is a non-zero probability that the algorithm fails to find the period because the measured state does no
    # match, in this case an exception is raised to indicate that the research must be continued
    raise ValueError('fail to find the period')

#!../venv/Scripts/python.exe
# -*- encoding : utf-8 -*-

"""
@Description:  This project provides a Python implementation of Shor's algorithm.
               For more details see : https://arxiv.org/abs/1907.09415
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
from typing import List, Tuple

# Local imports
from algs import is_prime_number, primer_power, NotPrimerPowerException, gcd, period_finder


def find_divisor(n: int) -> int:
    """
    Finds a non trivial factor of a composite integer performing Shor's algorithm.

    :param n: (int) a none prime number integer strictly greater than one

    :return: (int) a divisor of n

    :except TypeError: raised if the argument passed to the function is not an integer
    :except ValueError: raised if the argument passed to the function is not an integer strictly greatest than one
    """

    # The following lines check that the argument passed to the function is valid
    if not isinstance(n, int):
        raise TypeError('can only handle integers')
    elif n <= 1:
        raise ValueError('number must be strictly greater than one')
    elif n % 2 == 0:
        return 2
    elif is_prime_number(n):
        raise ValueError('number is prime number')

    # First we reduce the factorization problem to order-finding problem
    try:
        return primer_power(n)
    except NotPrimerPowerException:
        x_set = list(range(2, n))

        # Main loop
        while True:
            x = rd.choice(x_set)
            x_set.remove(x)
            print('Random number : ', x)

            # If gcd(x, n) != 1 then we find a non trivial divisor of n
            if gcd(x, n) > 1:
                return gcd(x, n)

            # Since now the factorization problem consits in finding the period of the function : a -> x^a mod n
            r = period_finder(n, x)

            # If the period found r is not valid we go back to the beginning of the loop
            if r % 2 == 1 or x ** (r / 2) % n == -1:
                continue

            # Since the period is valid we compute the two factors we can deduce from it
            fac_1, fac_2 = gcd(x ** (r // 2) - 1, n), gcd(x ** (r // 2) + 1, n)

            # If the factors we obtain are trivial, we go back to the beginning of the loop
            if (fac_1 == 1 or fac_1 == n) and (fac_2 == 1 or fac_2 == n):
                continue

            # Shor's algorithm ensures us that the two factors are non trivial factors of n
            return fac_1, fac_2


def _clean(factorization: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    cleans up the list of factors by ensuring that each prime number appears only once with its corresponding power and
    by ensuring that the list is sorted, i.e. the prime powers are arranged in ascending order.

    :param factorization: (List<Tuple<int, int>>) a non clean list of factors

    :return: (List<Tuple<int, int>>) the clean up list of factors
    """

    clean_factorization = []
    for prime_number, power in factorization:
        if prime_number not in [factor[0] for factor in clean_factorization]:
            clean_factorization.append((prime_number, 1))
        else:
            for i in range(len(clean_factorization)):
                if clean_factorization[i][0] == prime_number:
                    clean_factorization[i] = (prime_number, clean_factorization[i][1] + power)

    return sorted(clean_factorization, key=lambda item: item[0])


def prime_factorize(n: int) -> List[Tuple[int, int]]:
    """
    Performs the prime factorization of an integer.

    :param n: (int) a positive integer

    :return: (List<Tuple<int, int>>) the unique prime factorization of n.
    If n = p1^a1 * p2^a2 * ... * pn^an then the function returns [(p1, a1), (p2, a2), ..., (pn, an)]

    :except TypeError: raised if the argument passed to the function is not an integer
    :except ValueError: raised if the argument passed to the function is not an integer strictly greatest than one
    """

    if not isinstance(n, int):
        raise TypeError('can only handle integers')
    elif n <= 1:
        raise ValueError('integer must be strictly greater than one')
    elif is_prime_number(n):
        return [(n, 1)]
    elif n % 2 == 0:
        return _clean([(2, 1)] + prime_factorize(n // 2))
    else:
        divisor = find_divisor(n)
        return _clean([(divisor, 1)] + prime_factorize(n // divisor))


# while True:
#     n = int(input('Number : '))
#     print('Factorization : ', find_divisor(n))

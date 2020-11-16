#!../venv/Scripts/python.exe
# -*- encoding : utf-8 -*-

"""
@Description:  test_pyshor.py provides functions and classes to ensure the proper functioning of PyShor
@Author: Quentin Delamea
@Copyright: Copyright 2020, PyShor
@Credits: [Quentin Delamea]
@License: MIT
@Version: 0.0.1
@Maintainer: Quentin Delamea
@Email: qdelamea@gmail.com
@Status: Dev
"""

import random as rd

import pytest

from pyshor import find_divisor, prime_factorize, gcd, is_prime_number, primer_power, NotPrimerPowerException


class TestPyShorExceptions:
    """
    Contains functions to test PyShor's exceptions.
    """

    def test_find_divisor(self) -> None:
        """
        Tests find_divisor exceptions.
        """

        with pytest.raises(TypeError):
            find_divisor('a')
            find_divisor('12')

        with pytest.raises(ValueError):
            find_divisor(rd.randint(-100, 1))
            find_divisor(rd.choice(3, 5, 7, 11, 13, 17, 19, 23, 29, 31))

    def test_prime_factorize(self) -> None:
        """
        Tests prime_factorize exceptions.
        """

        with pytest.raises(TypeError):
            prime_factorize('a')
            prime_factorize('12')

        with pytest.raises(ValueError):
            prime_factorize(rd.randint(-100, 1))


class TestPyShorSubmodules:
    """
    Contains functions to test PyShor's submodules.
    """

    def test_gcd(self) -> None:
        """
        Tests the function gcd.
        """

        assert gcd(24, 36) == 12
        assert gcd(12, 15) == 3
        assert gcd(9, 10) == 1
        assert gcd(12, 21) == 3
        assert gcd(72, 8) == 8
        assert gcd(52, 76) == 4
        assert gcd(1701, 3768) == 3

    def test_is_prime_number(self) -> None:
        """
        Tests the function is_prime_number.
        """

        assert is_prime_number(2)
        assert is_prime_number(rd.choice([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
                                          73, 79, 83, 89, 97]))
        assert is_prime_number(9929)
        assert not is_prime_number(rd.choice(25, 18, 27, 28))
        assert not is_prime_number(9931)

    def test_primer_power(self) -> None:
        """
        Tests the function primer_power.
        """

        assert primer_power(128) == 2
        assert prime_factorize(125) == 5
        assert primer_power(98585041) == 9929

        with pytest.raises(NotPrimerPowerException):
            primer_power(15)
            primer_power(225)
            primer_power(23)


class TestPyShorFindDivisor:
    """
    Contains functions to test the PyShor find_divisor function.
    """

    def test_find_divisor(self) -> None:
        """
        Tests the function find_divisor.
        """

        assert find_divisor(2) == 2
        assert find_divisor(4) == 2
        assert find_divisor(6) == 2
        assert find_divisor(9) == 3
        assert find_divisor(12) in [3, 4]
        assert find_divisor(15) in [3, 5]
        assert find_divisor(21) in [3, 7]
        # assert find_divisor(33) in [3, 11]
        # assert find_divisor(247) in [13, 19]


class TestPyShorPrimeFactorize:
    """
    Contains functions to test the PyShor prime_factorize function.
    """

    def test_prime_factorize(self) -> None:
        """
        Tests the function prime_factorize.
        """

        assert prime_factorize(20) == [(2, 2), (5, 1)]
        assert prime_factorize(72) == [(2, 3), (3, 2)]
        assert prime_factorize(60) == [(2, 2), (3, 1), (5, 1)]
        # assert prime_factorize(135) == [(2, 2), (3, 4), (5, 1)]

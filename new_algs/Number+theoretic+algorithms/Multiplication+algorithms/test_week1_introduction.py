from unittest import TestCase

import numpy

from tools import array_to_int
from week1_introduction import simple_mult, simple_mult_as_arrays, karatsuba_mult


class TestMult(TestCase):
    def test_simple_mult(self):
        a, b = 123, 357

        result = simple_mult(a, b, size=4)
        assert result == a * b, result

    def test_simple_mult2(self):
        a, b = 77771232346123, 832409801237

        result = simple_mult(a, b)
        assert result == a * b, result

    def test_karatsuba_mult(self):
        a, b = 1234, 3575

        result = karatsuba_mult(a, b)
        assert result == a * b, (result, a * b)

    def test_karatsuba_mult2(self):
        a, b = 77771232346123, 832409801237

        result = simple_mult(a, b)
        assert result == a * b, result

    def test_result_offset(self):

        a = numpy.array([2])
        b = numpy.array([2])

        result = numpy.array([0, 0])

        out = array_to_int(simple_mult_as_arrays(a, b, result, result_offset=1))

        assert out == 40, out

    def test_result_input_offset(self):
        a = numpy.array([0, 0, 1])
        b = numpy.array([1, 2, 3])

        result = numpy.zeros(6, dtype=int)

        out = array_to_int(simple_mult_as_arrays(a, b, result, a_slice=(1, 3), b_slice=(1, 2)))

        assert out == 20, out

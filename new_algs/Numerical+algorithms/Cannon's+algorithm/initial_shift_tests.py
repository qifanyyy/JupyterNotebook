# -*- mode:python; coding:utf-8; tab-width:4 -*-

from unittest import TestCase

from hamcrest import assert_that, is_

from matrix_utils import matrix_horizontal_shift, matrix_vertical_shift
import Cannon
from common import M2, M3, M4, M6


class MatrixInitialShiftTests(TestCase):
    def test_horizontal_shift_2x2_by_blocks_1x1(self):
        # given
        M = Cannon.Matrix(2, [1, 2,
                              3, 4])

        # when
        actual = matrix_horizontal_shift(M, block_order=1)

        # then
        expected = Cannon.Matrix(2, [1, 2,
                                     4, 3])

        assert_that(actual, is_(expected))

    def test_horizontal_shift_3x3_by_blocks_1x1(self):
        # given
        original = M3(1, 2, 3,
                      4, 5, 6,
                      7, 8, 9)

        # when
        actual = matrix_horizontal_shift(original, block_order=1)

        # then
        expected = M3(1, 2, 3,
                      5, 6, 4,
                      9, 7, 8)

        assert_that(actual, is_(expected))

    def test_horizontal_shift_4x4_by_blocks_1x1(self):
        # given
        original = M4(1,  2,  3,  4,
                      5,  6,  7,  8,
                      9, 10, 11, 12,
                     13, 14, 15, 16)

        # when
        actual = matrix_horizontal_shift(original, block_order=1)

        # then
        expected = M4(1,  2,  3,  4,
                      6,  7,  8,  5,
                     11, 12,  9, 10,
                     16, 13, 14, 15)

        assert_that(actual, is_(expected))

    def test_horizontal_shift_6x6_by_blocks_1x1(self):
        # given
        original = M6(1,  2,  3,  4,  5,  6,
                      7,  8,  9, 10, 11, 12,
                     13, 14, 15, 16, 17, 18,
                     19, 20, 21, 22, 23, 24,
                     25, 26, 27, 28, 29, 30,
                     31, 32, 33, 34, 35, 36)

        # when
        actual = matrix_horizontal_shift(original, block_order=1)

        # then
        expected = M6(1,  2,  3,  4,  5,  6,
                      8,  9, 10, 11, 12,  7,
                     15, 16, 17, 18, 13, 14,
                     22, 23, 24, 19, 20, 21,
                     29, 30, 25, 26, 27, 28,
                     36, 31, 32, 33, 34, 35)

        assert_that(actual, is_(expected))

    def test_horizontal_shift_4x4_by_blocks_2x2(self):
        # given
        original = M4(1,  2,  3,  4,
                      5,  6,  7,  8,
                      9, 10, 11, 12,
                     13, 14, 15, 16)

        # when
        actual = matrix_horizontal_shift(original, block_order=2)

        # then
        expected = M4(1,  2,  3,  4,
                      5,  6,  7,  8,
                     11, 12,  9, 10,
                     15, 16, 13, 14)

        assert_that(actual, is_(expected))

    def test_horizontal_shift_6x6_by_blocks_2x2(self):
        # given
        original = M6(1,  2,  3,  4,  5,  6,
                      7,  8,  9, 10, 11, 12,
                     13, 14, 15, 16, 17, 18,
                     19, 20, 21, 22, 23, 24,
                     25, 26, 27, 28, 29, 30,
                     31, 32, 33, 34, 35, 36)

        # when
        actual = matrix_horizontal_shift(original, block_order=2)

        # then
        expected = M6(1,  2,  3,  4,  5,  6,
                      7,  8,  9, 10, 11, 12,
                     15, 16, 17, 18, 13, 14,
                     21, 22, 23, 24, 19, 20,
                     29, 30, 25, 26, 27, 28,
                     35, 36, 31, 32, 33, 34)

        assert_that(actual, is_(expected))

    def test_horizontal_shift_6x6_blocks_3x3(self):
        # given
        original = M6(1,  2,  3,  4,  5,  6,
                      7,  8,  9, 10, 11, 12,
                     13, 14, 15, 16, 17, 18,
                     19, 20, 21, 22, 23, 24,
                     25, 26, 27, 28, 29, 30,
                     31, 32, 33, 34, 35, 36)

        # when
        actual = matrix_horizontal_shift(original, block_order=3)

        # then
        expected = M6(1,  2,  3,  4,  5,  6,
                      7,  8,  9, 10, 11, 12,
                     13, 14, 15, 16, 17, 18,
                     22, 23, 24, 19, 20, 21,
                     28, 29, 30, 25, 26, 27,
                     34, 35, 36, 31, 32, 33)

        assert_that(actual, is_(expected))

    def test_vertical_shift_2x2_by_blocks_1x1(self):
        # given
        original = M2(1, 2,
                      3, 4)

        # when
        actual = matrix_vertical_shift(original, block_order=1)

        # then
        expected = M2(1, 4,
                      3, 2)

        assert_that(actual, is_(expected))

    def test_vertical_shift_4x4_by_blocks_2x2(self):
        # given
        original = M4(1,  2,  3,  4,
                      5,  6,  7,  8,
                      9, 10, 11, 12,
                     13, 14, 15, 16)

        # when
        actual = matrix_vertical_shift(original, block_order=2)

        # then
        expected = M4(1,  2, 11, 12,
                      5,  6, 15, 16,
                      9, 10,  3,  4,
                     13, 14,  7,  8)

        assert_that(actual, is_(expected))

    def test_vertical_shift_6x6_blocks_2x2(self):
        # given
        original = M6(1,  2,  3,  4,  5,  6,
                      7,  8,  9, 10, 11, 12,
                     13, 14, 15, 16, 17, 18,
                     19, 20, 21, 22, 23, 24,
                     25, 26, 27, 28, 29, 30,
                     31, 32, 33, 34, 35, 36)

        # when
        actual = matrix_vertical_shift(original, block_order=2)

        # then
        expected = M6(1,  2, 15, 16, 29, 30,
                      7,  8, 21, 22, 35, 36,
                     13, 14, 27, 28,  5,  6,
                     19, 20, 33, 34, 11, 12,
                     25, 26,  3,  4, 17, 18,
                     31, 32,  9, 10, 23, 24)

        assert_that(actual, is_(expected))

    def test_vertical_shift_6x6_blocks_3x3(self):
        # given
        original = M6(1,  2,  3,  4,  5,  6,
                      7,  8,  9, 10, 11, 12,
                     13, 14, 15, 16, 17, 18,
                     19, 20, 21, 22, 23, 24,
                     25, 26, 27, 28, 29, 30,
                     31, 32, 33, 34, 35, 36)

        # when
        actual = matrix_vertical_shift(original, block_order=3)

        # then
        expected = M6(1,  2,  3, 22, 23, 24,
                      7,  8,  9, 28, 29, 30,
                     13, 14, 15, 34, 35, 36,
                     19, 20, 21,  4,  5,  6,
                     25, 26, 27, 10, 11, 12,
                     31, 32, 33, 16, 17, 18)

        assert_that(actual, is_(Cannon.Matrix(6, expected)))

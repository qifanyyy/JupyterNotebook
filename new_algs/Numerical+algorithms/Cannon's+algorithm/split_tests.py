# -*- mode:python; coding:utf-8; tab-width:4 -*-

from unittest import TestCase

from hamcrest import assert_that, is_

from matrix_utils import (list_split, matrix_split)

from common import M2, M3, M4, M6, M8


class MatrixSplitTests(TestCase):
    def test_list_split(self):
        assert_that(list_split([1, 2, 3, 4], 2), is_([[1, 2], [3, 4]]))

    def test_split_4x4_in_4_blocks(self):
        # given
        original = M4(1,  2,  3,  4,
                      5,  6,  7,  8,
                      9, 10, 11, 12,
                     13, 14, 15, 16)

        # when
        actual = matrix_split(original, block_order=2)

        # then
        E00 = M2(1, 2,
                 5, 6)

        E01 = M2(3, 4,
                 7, 8)

        E10 = M2(9, 10,
                13, 14)

        E11 = M2(11, 12,
                 15, 16)

        assert_that(actual, is_([E00, E01,
                                 E10, E11]))

    def test_split_6x6_in_9_blocks(self):
        # given
        original = M6(1,  2,  3,  4,  5,  6,
                      7,  8,  9, 10, 11, 12,
                     13, 14, 15, 16, 17, 18,
                     19, 20, 21, 22, 23, 24,
                     25, 26, 27, 28, 29, 30,
                     31, 32, 33, 34, 35, 36)

        # when
        blocks = matrix_split(original, block_order=2)

        # then
        E00 = M2(1, 2,
                 7, 8)

        E01 = M2(3,  4,
                 9, 10)

        E02 = M2(5,  6,
                11, 12)

        E10 = M2(13, 14,
                 19, 20)

        E11 = M2(15, 16,
                 21, 22)

        E12 = M2(17, 18,
                 23, 24)

        E20 = M2(25, 26,
                 31, 32)

        E21 = M2(27, 28,
                 33, 34)

        E22 = M2(29, 30,
                 35, 36)

        assert_that(blocks, is_([E00, E01, E02,
                                 E10, E11, E12,
                                 E20, E21, E22]))

    def test_split_6x6_in_4_blocks(self):
        # given
        original = M6(1,  2,  3,  4,  5,  6,
                      7,  8,  9, 10, 11, 12,
                     13, 14, 15, 16, 17, 18,
                     19, 20, 21, 22, 23, 24,
                     25, 26, 27, 28, 29, 30,
                     31, 32, 33, 34, 35, 36)

        # when
        blocks = matrix_split(original, block_order=3)

        # then
        E00 = M3(1,  2,  3,
                 7,  8,  9,
                13, 14, 15)

        E01 = M3(4,  5,  6,
                10, 11, 12,
                16, 17, 18)

        E10 = M3(19, 20, 21,
                 25, 26, 27,
                 31, 32, 33)

        E11 = M3(22, 23, 24,
                 28, 29, 30,
                 34, 35, 36)

        assert_that(blocks, is_([E00, E01,
                                 E10, E11]))

    def test_split_8x8_in_4_blocks(self):
        # given
        original = M8(1,  2,  3,  4,  5,  6,  7,  8,
                      9, 10, 11, 12, 13, 14, 15, 16,
                     17, 18, 19, 20, 21, 22, 23, 24,
                     25, 26, 27, 28, 29, 30, 31, 32,
                     33, 34, 35, 36, 37, 38, 39, 40,
                     41, 42, 43, 44, 45, 46, 47, 48,
                     49, 50, 51, 52, 53, 54, 55, 56,
                     57, 58, 59, 60, 61, 62, 63, 64)

        # when
        blocks = matrix_split(original, block_order=4)

        # then
        E00 = M4(1,  2,  3,  4,
                 9, 10, 11, 12,
                17, 18, 19, 20,
                25, 26, 27, 28)

        E01 = M4(5,  6,  7,  8,
                13, 14, 15, 16,
                21, 22, 23, 24,
                29, 30, 31, 32)

        E10 = M4(33, 34, 35, 36,
                 41, 42, 43, 44,
                 49, 50, 51, 52,
                 57, 58, 59, 60)

        E11 = M4(37, 38, 39, 40,
                 45, 46, 47, 48,
                 53, 54, 55, 56,
                 61, 62, 63, 64)

        assert_that(blocks, is_([E00, E01,
                                 E10, E11]))

    def test_split_8x8_in_16_blocks(self):
        # given
        original = M8(1,  2,  3,  4,  5,  6,  7,  8,
                      9, 10, 11, 12, 13, 14, 15, 16,
                     17, 18, 19, 20, 21, 22, 23, 24,
                     25, 26, 27, 28, 29, 30, 31, 32,
                     33, 34, 35, 36, 37, 38, 39, 40,
                     41, 42, 43, 44, 45, 46, 47, 48,
                     49, 50, 51, 52, 53, 54, 55, 56,
                     57, 58, 59, 60, 61, 62, 63, 64)

        # when
        blocks = matrix_split(original, block_order=2)

        # then
        E00 = M2(1,  2,
                 9, 10)

        E01 = M2(3,  4,
                 11, 12)

        E02 = M2(5,  6,
                 13, 14)

        E03 = M2(7,  8,
                 15, 16)

        E10 = M2(17, 18,
                 25, 26)

        E11 = M2(19, 20,
                 27, 28)

        E12 = M2(21, 22,
                 29, 30)

        E13 = M2(23, 24,
                 31, 32)

        E20 = M2(33, 34,
                 41, 42)

        E21 = M2(35, 36,
                 43, 44)

        E22 = M2(37, 38,
                 45, 46)

        E23 = M2(39, 40,
                 47, 48)

        E30 = M2(49, 50,
                 57, 58)

        E31 = M2(51, 52,
                 59, 60)

        E32 = M2(53, 54,
                 61, 62)

        E33 = M2(55, 56,
                 63, 64)

        assert_that(blocks, is_([E00, E01, E02, E03,
                                 E10, E11, E12, E13,
                                 E20, E21, E22, E23,
                                 E30, E31, E32, E33]))

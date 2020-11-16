# -*- mode:python; coding:utf-8; tab-width:4 -*-

from unittest import TestCase

from hamcrest import assert_that, is_

from matrix_utils import matrix_join

from common import M2, M3, M4, M6, M8


class MatrixJoinTests(TestCase):
    def test_join_4_2x2_blocks_in_4x4_matrix(self):
        # given
        A0 = M2(1, 2,
                5, 6)

        A1 = M2(3, 4,
                7, 8)

        A2 = M2(9, 10,
               13, 14)

        A3 = M2(11, 12,
                15, 16)
        
        blocks = (A0, A1, A2, A3)

        # when
        actual = matrix_join(blocks)

        # then
        expected = M4(1,  2,  3,  4,
                      5,  6,  7,  8,
                      9, 10, 11, 12,
                     13, 14, 15, 16)

        assert_that(actual, is_(expected))

    def test_join_9_2x2_blocks_in_6x6_matrix(self):
         # given
         A0 = M2(1, 2,
                 7, 8)

         A1 = M2(3,  4,
                 9, 10)

         A2 = M2(5,  6,
                11, 12)

         A3 = M2(13, 14,
                 19, 20)

         A4 = M2(15, 16,
                 21, 22)

         A5 = M2(17, 18,
                 23, 24)

         A6 = M2(25, 26,
                 31, 32)

         A7 = M2(27, 28,
                 33, 34)

         A8 = M2(29, 30,
                 35, 36)
                 
         blocks = (A0, A1, A2,A3, A4, A5, A6, A7, A8)

         # when
         actual = matrix_join(blocks)
         # then
         expected = M6(1,  2,  3,  4,  5,  6,
                       7,  8,  9, 10, 11, 12,
                      13, 14, 15, 16, 17, 18,
                      19, 20, 21, 22, 23, 24,
                      25, 26, 27, 28, 29, 30,
                      31, 32, 33, 34, 35, 36)


         assert_that(actual, is_(expected))

    def test_join_4_3x3_blocks_in_6x6_matrix(self):
         # given
         A0 = M3(1,  2,  3,
                 7,  8,  9,
                13, 14, 15)

         A1 = M3(4,  5,  6,
                10, 11, 12,
                16, 17, 18)

         A2 = M3(19, 20, 21,
                 25, 26, 27,
                 31, 32, 33)

         A3 = M3(22, 23, 24,
                 28, 29, 30,
                 34, 35, 36)
                 
         blocks = (A0, A1, A2, A3)

         # when
         actual = matrix_join(blocks)

         # then
         expected = M6(1,  2,  3,  4,  5,  6,
                       7,  8,  9, 10, 11, 12,
                      13, 14, 15, 16, 17, 18,
                      19, 20, 21, 22, 23, 24,
                      25, 26, 27, 28, 29, 30,
                      31, 32, 33, 34, 35, 36)

         assert_that(actual, is_(expected))

    def test_join_4_4x4_blocks_in_8x8_matrix(self):
         # given
         A0 = M4(1,  2,  3,  4,
                 9, 10, 11, 12,
                17, 18, 19, 20,
                25, 26, 27, 28)

         A1 = M4(5,  6,  7,  8,
                13, 14, 15, 16,
                21, 22, 23, 24,
                29, 30, 31, 32)

         A2 = M4(33, 34, 35, 36,
                 41, 42, 43, 44,
                 49, 50, 51, 52,
                 57, 58, 59, 60)

         A3 = M4(37, 38, 39, 40,
                 45, 46, 47, 48,
                 53, 54, 55, 56,
                 61, 62, 63, 64)
                 
                 
         blocks = (A0, A1, A2, A3)

         # when
         actual = matrix_join(blocks)

         # then
         expected = M8(1,  2,  3,  4,  5,  6,  7,  8,
                       9, 10, 11, 12, 13, 14, 15, 16,
                      17, 18, 19, 20, 21, 22, 23, 24,
                      25, 26, 27, 28, 29, 30, 31, 32,
                      33, 34, 35, 36, 37, 38, 39, 40,
                      41, 42, 43, 44, 45, 46, 47, 48,
                      49, 50, 51, 52, 53, 54, 55, 56,
                      57, 58, 59, 60, 61, 62, 63, 64)

         assert_that(actual, is_(expected))

    def test_join_16_2x2_blocks_in_8x8_matrix(self):
         # given
         A0 = M2(1,  2,
                 9, 10)

         A1 = M2(3,  4,
                11, 12)

         A2 = M2(5,  6,
                13, 14)

         A3 = M2(7,  8,
                15, 16)

         A4 = M2(17, 18,
                 25, 26)

         A5 = M2(19, 20,
                 27, 28)

         A6 = M2(21, 22,
                 29, 30)

         A7 = M2(23, 24,
                 31, 32)

         A8 = M2(33, 34,
                 41, 42)

         A9 = M2(35, 36,
                 43, 44)

         A10 = M2(37, 38,
                  45, 46)

         A11 = M2(39, 40,
                  47, 48)

         A12 = M2(49, 50,
                  57, 58)

         A13 = M2(51, 52,
                  59, 60)

         A14 = M2(53, 54,
                  61, 62)

         A15 = M2(55, 56,
                  63, 64)
                  
         blocks = (A0,  A1,  A2,  A3, A4,  A5,  A6,  A7, A8,  A9,  A10, A11, A12, A13, A14, A15)

         # when
         actual = matrix_join(blocks)

         # then
         expected = M8(1,  2,  3,  4,  5,  6,  7,  8,
                       9, 10, 11, 12, 13, 14, 15, 16,
                      17, 18, 19, 20, 21, 22, 23, 24,
                      25, 26, 27, 28, 29, 30, 31, 32,
                      33, 34, 35, 36, 37, 38, 39, 40,
                      41, 42, 43, 44, 45, 46, 47, 48,
                      49, 50, 51, 52, 53, 54, 55, 56,
                      57, 58, 59, 60, 61, 62, 63, 64)

         assert_that(actual, is_(expected))

import unittest
import logging

from NeedlemanWunschPy.algorithms import NeedlemanWunschLinear
from NeedlemanWunschPy.substitutionmatrix import Blosum50


class NeedlemanWunschLinearTestCases(unittest.TestCase):

    def setUp(self):
        # Disable logger content
        logging.disable(logging.CRITICAL)

        seqA = "ACCCGT"
        seqB = "AACCGCCGT"

        gap_penalty = -8

        self.algorithm = NeedlemanWunschLinear(seqA, seqB, gap_penalty, Blosum50())

    def test_get_score_from_A_and_A_return_5(self):
        result = self.algorithm._get_score(1, 1)
        expected = 5
        self.assertEqual(result, expected)

    def test_first_element_of_score_matrix_return_0(self):
        self.algorithm._compute_score_matrix()
        result = self.algorithm.M[0][0]
        expected = 0
        self.assertEqual(result, expected)

    def test_third_element_in_the_first_row_of_score_matrix_return_minus_16(self):
        self.algorithm._compute_score_matrix()
        result = self.algorithm.M[0][2]
        expected = -16
        self.assertEqual(result, expected)

    def test_third_element_in_the_first_column_of_score_matrix_return_minus_16(self):
        self.algorithm._compute_score_matrix()
        result = self.algorithm.M[2][0]
        expected = -16
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()

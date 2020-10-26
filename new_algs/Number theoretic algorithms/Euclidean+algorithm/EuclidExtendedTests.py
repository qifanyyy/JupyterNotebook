import unittest

from EuclidExtended import euclid_extended


class EuclidExtendedTests(unittest.TestCase):

    def test_1_and_1(self):
        self.assertEqual(euclid_extended([1, 1]), (1, [1, 0]))

    def test_7_8_9(self):
        self.assertEqual(euclid_extended([7, 8, 9]), (1, [-1, 1, 0]))


if __name__ == '__main__':
    unittest.main()

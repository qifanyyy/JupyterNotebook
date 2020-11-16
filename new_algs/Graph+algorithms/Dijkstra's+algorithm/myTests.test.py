#!usr/bin/env python3
import unittest
import warnings

from utils import readFileToAdjacencyList, pathString
from myDijkstra import djikstras


def ignore_warnings(test_func):
    def start_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            test_func(self, *args, **kwargs)
    return start_test


class TestDijkstra(unittest.TestCase):

    @ignore_warnings
    def test_0(self):
        adjacency_matrix, start, end = readFileToAdjacencyList(
        "test_cases/test_case_0.txt")
        path, dist = djikstras(adjacency_matrix, start, end)
        self.assertEqual(pathString(path, start, end), "0-3-2")
        self.assertAlmostEqual(dist, 8.2)
        self.assertNotEqual(dist, 8)
        self.assertNotEqual(dist, 8.4)
    
    @ignore_warnings
    def test_1(self):
        adjacency_matrix, start, end = readFileToAdjacencyList(
        "test_cases/test_case_1.txt")
        path, dist = djikstras(adjacency_matrix, start, end)
        self.assertEqual(pathString(path, start, end), "2-3-0-9")
        self.assertAlmostEqual(dist, 10.0)
        self.assertNotEqual(dist, 10.2)
        self.assertNotEqual(dist, 9.8)

    @ignore_warnings
    def test_2(self):
        adjacency_matrix, start, end = readFileToAdjacencyList(
        "test_cases/test_case_2.txt")
        path, dist = djikstras(adjacency_matrix, start, end)
        self.assertEqual(pathString(path, start, end), "25-14-2-9-4-3")
        self.assertAlmostEqual(dist, 11.2)
        self.assertNotEqual(dist, 11.0)
        self.assertNotEqual(dist, 11.4)

    @ignore_warnings
    def test_3(self):
        adjacency_matrix, start, end = readFileToAdjacencyList(
        "test_cases/test_case_3.txt")
        path, dist = djikstras(adjacency_matrix, start, end)
        self.assertEqual(pathString(path, start, end), "7-16-19")
        self.assertAlmostEqual(dist, 1.5)
        self.assertNotEqual(dist, 1.7)
        self.assertNotEqual(dist, 1.2)

    @ignore_warnings
    def test_4(self):
        adjacency_matrix, start, end = readFileToAdjacencyList(
        "test_cases/test_case_4.txt")
        path, dist = djikstras(adjacency_matrix, start, end)
        self.assertEqual(pathString(path, start, end), "33-18-27-13-1")
        self.assertAlmostEqual(dist, 1.9)
        self.assertNotEqual(dist, 2)


if __name__ == '__main__':
    unittest.main()
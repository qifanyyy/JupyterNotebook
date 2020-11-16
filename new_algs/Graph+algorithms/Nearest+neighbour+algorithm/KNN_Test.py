import unittest
import math as math
import KNN_Implementation
from KNN_Implementation import *

trainingSet = [(1, 2, 3, 4, 'A'),
               (6, 1, 2, 3, 'A'),
               (2, 8, 4, 1, 'B'),
               (11, 2, 4, 1, 'B'),
               (1, 2, 1, 2, 'A')]
trainingSetNeightbours = [(1, 2, 3, 4),
                          (6, 1, 2, 3),
                          (2, 8, 4, 1),
                          (11, 2, 4, 1),
                          (1, 2, 1, 2)]
testSet = [(2, 2, 4, 5, 'A'),
           (7, 5, 1, 5, 'A')]

testSetNeightbours = [(2, 2, 4, 5),
                      (7, 5, 1, 5)]

class TestKNNAlgorithm(unittest.TestCase):
    def setUp(self):
        pass
    def testGetDataWithoutLabels(self):
        self.assertEqual(getNeighbors(testSet), testSetNeightbours)
        self.assertEqual(getNeighbors(trainingSet), trainingSetNeightbours)
    def testDistance(self):
        self.assertEqual(distance(trainingSet[0], testSet[0]), math.sqrt(3))
        self.assertEqual(distance(trainingSet[0], testSet[1]), math.sqrt(50))
        self.assertEqual(distance(trainingSet[1], testSet[1]), math.sqrt(22))
        self.assertEqual(distance(trainingSet[2], testSet[1]), math.sqrt(59))
        self.assertEqual(distance(trainingSet[3], testSet[1]), math.sqrt(50))
        self.assertEqual(distance(trainingSet[4], testSet[0]), math.sqrt(19))

    def testPredict(self):
        k = KNN_Implementation.KNN.__init__(3, trainingSet)
        predicted = ['A', 'A']
        self.assertEqual(KNN.predict(testSetNeightbours), predicted)

    def testScore(self):
        self.assertEqual(KNN.score(testSet, KNN.predict(testSetNeightbours)), 2)

    if __name__ == '__main__':
        unittest.main()

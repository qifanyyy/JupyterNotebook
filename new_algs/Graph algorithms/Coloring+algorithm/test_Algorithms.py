import unittest


import Graph
from GraphGen import genGraph
import Algorithms


class TestAlgorithms(unittest.TestCase):
    def test_WelshPowell(self):
        n = 20
        d = 0.8
        g = genGraph(n, d)
        coloring, _ = Algorithms.WelshPowell(g)
        self.checkColoring(g, coloring)

    def test_WelshPowellNewGenMethod(self):
        n = 1000
        d = 0.95
        k = 6
        g = genGraph(n, d, k, seed=1)
        _, colorsUsed = Algorithms.WelshPowell(g)
        print(colorsUsed)
        self.assertTrue(k <= colorsUsed)

    def test_bruteForce(self):
        g = genGraph(10, 0.75, 4)
        coloring, _ = Algorithms.bruteForce(g)
        self.checkColoring(g, coloring)

    def test_getMaximumCliqueSize(self):
        g = Graph.Graph()
        for i in range(6):
            g.addVertex(i)
        g.addEdges([(0, 1), (1, 2), (1, 3), (1, 5), (2, 3), (2, 5), (3, 4), (3, 5), (4, 5)])
        self.assertEqual(4, Algorithms.getLargestCliqueSize(g))

    def test_fastBruteForce(self):
        g = genGraph(11, 0.8, 6, seed=100)
        coloring, colorCount = Algorithms.bruteForce(g, True)
        self.checkColoring(g, coloring)
        self.assertTrue(6 >= colorCount)

    def checkColoring(self, graph, coloring):
        # Check if BruteForce coloring is correct
        for v in graph.getAdjDict():
            for u in graph.getAdjDict()[v]:
                if coloring[v] == coloring[u]:
                    self.fail("Algorithm failed!")

    def test_removeBadVertices(self):
        g = Graph.Graph()
        for i in range(5):
            g.addVertex(i)
        g.addEdges([(0, 1), (1, 2), (1, 3), (3, 4), (1, 4), (0, 2)])
        Algorithms.removeBadVertices(g)
        self.assertDictEqual(g.getAdjDict(), {
            0: [2],
            2: [0],
            3: [4],
            4: [3]
        })

        g = Graph.Graph()
        for i in range(5):
            g.addVertex(i)
        g.addEdges([(0, 1), (1, 2), (1, 3), (2, 3), (3, 4), (1, 4), (0, 2), (0, 3)])
        Algorithms.removeBadVertices(g)
        self.assertDictEqual(g.getAdjDict(), {
            0: [2],
            2: [0],
            4: []
        })

    def test_singleColoredVertices(self):
        n = 1000
        d = 0.8
        k = 100
        g = genGraph(n, d, k, seed=1)
        coloring, colorsUsed = Algorithms.WelshPowell(g)
        print(coloring)
        print(colorsUsed)
        # coloringBF, colorsUsedBF = Algorithms.bruteForce(g, True)

        if coloring is None:
            self.fail()

    def test_singleColoredFail(self):
        g = Graph.Graph()
        g.addVertices(range(4))
        g.addEdge(0, 1)
        g.addEdge(1, 2)
        g.addEdge(1, 3)
        g.addEdge(2, 3)
        coloring, colorsUsed = Algorithms.bruteForce(g)
        self.assertTrue(coloring is None)


if __name__ == '__main__':
    unittest.main()

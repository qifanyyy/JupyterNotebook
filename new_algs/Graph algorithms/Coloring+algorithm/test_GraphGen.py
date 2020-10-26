from unittest import TestCase
from time import time
from GraphGen import genEdges, genGraph
from Algorithms import WelshPowell


class TestGraphGen(TestCase):
    def test_genEdges(self):
        n = 100
        density = 0.8
        edgesCount = int(n*(n-1)/2*density)
        edges = genEdges(n, density)
        self.assertEqual(edgesCount, len(edges))

    def test_genGraph(self):
        n = 100
        density = 0.8
        edgesCount = int(n * (n - 1) / 2 * density)
        g = genGraph(n, density)
        self.assertEqual(n, g.getVertexCount())
        self.assertEqual(edgesCount, g.getEdgeCount())

    def test_genGraphWithGroups(self):
        n = 100
        density = 1.0
        i = 20
        for groupsCount in range(1, i+1):
            g = genGraph(n, density, groupsCount)
            chromatic = WelshPowell(g)[1]
            # print(groupsCount, chromatic)
            self.assertTrue(groupsCount == chromatic)

    def test_seedTwoGens(self):
        n = 100
        density = 0.8
        seed = time()
        g = genGraph(n, density, seed=seed)
        f = genGraph(n, density, seed=seed)
        self.assertTrue(g == f)

    def test_differentGraphs(self):
        n = 100
        density = 0.8
        k = 5
        g = genGraph(n, density, k)
        f = genGraph(n, density, k)
        self.assertFalse(g == f)

    def test_seed(self):
        n = 5
        d = 0.4
        seed = 3
        g = genGraph(n, d, seed=seed)
        self.assertDictEqual({'0': ['4', '3'], '1': [], '2': ['4', '3'], '3': ['0', '2'], '4': ['0', '2']},
                             g.getAdjDict())

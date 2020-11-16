import pygraph.core as graphs
from pygraph.algorithms.transitivity import acyclic_closure
import unittest

class TestTransitiveClosure(unittest.TestCase):
    def setUp(self):
        self.a = graphs.NamedNode("A")
        self.b = graphs.NamedNode("B")
        self.c = graphs.NamedNode("C")
        self.d = graphs.NamedNode("D")
        self.e = graphs.NamedNode("E")
        self.digraph = graphs.Digraph()
        self.digraph.add_edge(self.a, self.b)
        self.digraph.add_edge(self.a, self.c)
        self.digraph.add_edge(self.b, self.d)
        self.digraph.add_edge(self.c, self.d)
        self.digraph.add_edge(self.d, self.e)


    def test_generates_reachability_matrix(self):
        matrix = acyclic_closure(self.digraph)

        # Reachability from A
        self.assertEquals(1, matrix.get(self.a, self.a))
        self.assertEquals(1, matrix.get(self.a, self.b))
        self.assertEquals(1, matrix.get(self.a, self.c))
        self.assertEquals(1, matrix.get(self.a, self.d))
        self.assertEquals(1, matrix.get(self.a, self.e))

        # Reachability from B
        self.assertEquals(1, matrix.get(self.b, self.b))
        self.assertEquals(0, matrix.get(self.b, self.a))
        self.assertEquals(0, matrix.get(self.b, self.c))
        self.assertEquals(1, matrix.get(self.b, self.d))
        self.assertEquals(1, matrix.get(self.b, self.e))

        # Reachability from C
        self.assertEquals(1, matrix.get(self.c, self.c))
        self.assertEquals(0, matrix.get(self.c, self.a))
        self.assertEquals(0, matrix.get(self.c, self.b))
        self.assertEquals(1, matrix.get(self.c, self.d))
        self.assertEquals(1, matrix.get(self.c, self.e))

        # Reachability from D
        self.assertEquals(1, matrix.get(self.d, self.d))
        self.assertEquals(0, matrix.get(self.d, self.a))
        self.assertEquals(0, matrix.get(self.d, self.b))
        self.assertEquals(0, matrix.get(self.d, self.c))
        self.assertEquals(1, matrix.get(self.d, self.e))

        # Reachability from E
        self.assertEquals(1, matrix.get(self.e, self.e))
        self.assertEquals(0, matrix.get(self.e, self.a))
        self.assertEquals(0, matrix.get(self.e, self.b))
        self.assertEquals(0, matrix.get(self.e, self.c))
        self.assertEquals(0, matrix.get(self.e, self.d))
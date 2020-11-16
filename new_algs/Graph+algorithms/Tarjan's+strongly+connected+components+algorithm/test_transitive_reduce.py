import pygraph.core as graphs
from pygraph.algorithms.transitivity import acyclic_reduce
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
        self.digraph.add_edge(self.a, self.d)
        self.digraph.add_edge(self.a, self.e)
        self.digraph.add_edge(self.b, self.d)
        self.digraph.add_edge(self.b, self.e)
        self.digraph.add_edge(self.c, self.d)
        self.digraph.add_edge(self.c, self.e)
        self.digraph.add_edge(self.d, self.e)

    def test_removes_redundant_edges(self):
        acyclic_reduce(self.digraph)
        self.assertEquals(5, len(self.digraph.edges()))
        self.assertTrue(self.digraph.has_edge(self.a, self.b))
        self.assertTrue(self.digraph.has_edge(self.a, self.c))
        self.assertTrue(self.digraph.has_edge(self.b, self.d))
        self.assertTrue(self.digraph.has_edge(self.c, self.d))
        self.assertTrue(self.digraph.has_edge(self.d, self.e))
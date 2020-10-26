import unittest
import pygraph.core as graphs
import pygraph.algorithms.strong_components as scc

class TestStrongComponents(unittest.TestCase):
    def setUp(self):
        self.a       = graphs.NamedNode("A")
        self.b       = graphs.NamedNode("B")
        self.c       = graphs.NamedNode("C")
        self.d       = graphs.NamedNode("D")
        self.e       = graphs.NamedNode("E")
        self.digraph = graphs.Digraph()

    def test_simple_cycle_identification(self):
        self.digraph.add_edge(self.a, self.b)
        self.digraph.add_edge(self.b, self.a)

        quotient = scc.quotient(self.digraph)
        nodemap  = quotient.nodemap

        self.assertEquals(2, len(nodemap))
        self.assertTrue(nodemap[self.a] == nodemap[self.b])
        self.assertEquals(1, len(quotient.nodes_set()))
        self.assertEquals(0, len(quotient.edges()))

    def test_simple_component_with_outgoing_edge(self):
        """
        digraph {
            A -> B;
            B -> A;
            B -> C;
        }

        """
        
        self.digraph.add_edge(self.a, self.b)
        self.digraph.add_edge(self.b, self.a)
        self.digraph.add_edge(self.b, self.c)

        quotient = scc.quotient(self.digraph)
        nodemap  = quotient.nodemap
        
        self.assertEquals(nodemap[self.a], nodemap[self.b])
        self.assertNotEquals(nodemap[self.c], nodemap[self.a])

        c1, c2 = nodemap[self.a], nodemap[self.c]
        self.assertEquals(2, len(quotient.nodes_set()))
        self.assertEquals(1, len(quotient.edges()))
        self.assertTrue(quotient.has_edge(c1, c2))

    def test_cycle_of_three(self):
        """
        digraph {
            A -> B;
            B -> A;
            B -> C;
            C -> B;
        }

        """

        self.digraph.add_edge(self.a, self.b)
        self.digraph.add_edge(self.b, self.a)
        self.digraph.add_edge(self.b, self.c)
        self.digraph.add_edge(self.c, self.b)

        quotient = scc.quotient(self.digraph)
        nodemap  = quotient.nodemap

        self.assertEquals(3, len(nodemap))
        self.assertTrue(nodemap[self.a] == nodemap[self.b] == nodemap[self.c])

        self.assertEquals(1, len(quotient.nodes_set()))
        self.assertEquals(0, len(quotient.edges()))

    def test_edges_between_components(self):
        """
        digraph {
            A -> B;
            B -> A;
            B -> C;
            B -> E;
            C -> D;
            D -> C;
            D -> E;
        }
        
        """

        self.digraph.add_edge(self.a, self.b)
        self.digraph.add_edge(self.b, self.a)
        self.digraph.add_edge(self.b, self.c)
        self.digraph.add_edge(self.b, self.e)
        self.digraph.add_edge(self.c, self.d)
        self.digraph.add_edge(self.d, self.c)
        self.digraph.add_edge(self.d, self.e)

        quotient = scc.quotient(self.digraph)
        nodemap  = quotient.nodemap

        self.assertTrue(nodemap[self.a] == nodemap[self.b])
        self.assertTrue(nodemap[self.c] == nodemap[self.d])
        self.assertTrue(nodemap[self.a] != nodemap[self.c])
        self.assertTrue(nodemap[self.e] != nodemap[self.a])
        self.assertTrue(nodemap[self.e] != nodemap[self.c])
        self.assertEquals(5, len(nodemap))

        c1, c2, c3 = nodemap[self.a], nodemap[self.c], nodemap[self.e]

        self.assertTrue(quotient.has_edge(c1, c2))
        self.assertTrue(quotient.has_edge(c1, c3))
        self.assertTrue(quotient.has_edge(c2, c3))
        self.assertEquals(3, len(quotient.nodes_set()))
        self.assertEquals(3, len(quotient.edges()))
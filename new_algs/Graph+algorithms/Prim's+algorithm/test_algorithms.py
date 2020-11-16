import unittest
from mstfind import dijkstra_mst, kruskal_mst, prim_mst
from mstfind import Graph


class TestAlgorithms(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()
        self.graph.add_edge(('A', 'B'), 2)
        self.graph.add_edge(('C', 'A'), 10)
        self.graph.add_edge(('B', 'D'), 7)
        self.graph.add_edge(('C', 'D'), 8)
        self.graph.add_edge(('E', 'C'), 7)
        self.graph.add_edge(('E', 'D'), 3)

        self.mst_true = {(('A', 'B'), 2), (('D', 'E'), 3), (('B', 'D'), 7), (('C', 'E'), 7)}

    def test_dijkstra_mst(self):
        mst = dijkstra_mst(self.graph)
        self.assertEqual(self.sort_edges(mst.edges()), self.mst_true)

    def test_kruskal_mst(self):
        mst = kruskal_mst(self.graph)
        self.assertEqual(self.sort_edges(mst.edges()), self.mst_true)
        
    def test_prim_mst(self):
        mst = prim_mst(self.graph)
        self.assertEqual(self.sort_edges(mst.edges()), self.mst_true)

    @staticmethod
    def sort_edges(mst_edges):
        return set((tuple(sorted(uv)), w) for (uv, w) in mst_edges)



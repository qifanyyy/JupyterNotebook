import unittest

from inout.parser import parse
from algorithms.shortest_path import single_source_shortest_paths_dijkstra as sssp
import os
import config as cfg
import networkx as nx

from view.visualiser import draw_small_graph


class ShortestPathTests(unittest.TestCase):

    def test_shortest_path(self):
        """
        Test shortest path correctness.
        :return:
        """

        edges_path = os.path.join(cfg.TESTS_IN_DIR, "sssp_graph.csv")

        graph = parse(edges_path)

        graph_nx = nx.Graph()
        graph_nx.add_weighted_edges_from(graph.weighted_edges)

        # draw_small_graph(graph)

        shortest_paths, distances = sssp(graph, 1)

        # The path [1,2,4] has higher distance and should not appear
        # in shortest paths
        self.assertEqual(shortest_paths[4], [[1,3,4]])


if __name__ == '__main__':
    unittest.main()

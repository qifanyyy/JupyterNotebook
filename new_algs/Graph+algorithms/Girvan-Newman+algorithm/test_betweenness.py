import unittest

from inout.parser import parse
from algorithms.betweenness import get_edges_with_highest_betweenness
from networkx.algorithms.centrality.betweenness import edge_betweenness_centrality
import os
import config as cfg
import networkx as nx


class BetweennessTests(unittest.TestCase):

    def test_highest_betweenness(self):
        """
        Test edge with highest betweenness in graph is same as networkx
        :return:
        """

        edges_path = os.path.join(cfg.TESTS_IN_DIR, "simple_graph.csv")

        graph = parse(edges_path)

        graph_nx = nx.Graph()
        graph_nx.add_weighted_edges_from(graph.weighted_edges)

        top_edges_cs = get_edges_with_highest_betweenness(graph)

        betweenness_nx = edge_betweenness_centrality(graph_nx, normalized=False)
        top_edges_nx = self.get_edges_with_highest_betweenness(betweenness_nx)

        self.assertEqual(top_edges_cs, top_edges_nx)

    def get_edges_with_highest_betweenness(self, betweenness_dict):

        sorted_by_betweenness_desc = sorted(betweenness_dict.items(),
                                            key=lambda edge_betweenness_pair: (
                                                edge_betweenness_pair[1], edge_betweenness_pair[0]),
                                            reverse=True)

        top_betweennness = sorted_by_betweenness_desc[0][1]
        top_edges = list()

        for edge_betweenness_pair in sorted_by_betweenness_desc:
            if edge_betweenness_pair[1] != top_betweennness:
                break
            top_edges.append(edge_betweenness_pair[0])

        return top_edges


if __name__ == '__main__':
    unittest.main()

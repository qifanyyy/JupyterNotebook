import unittest
from inout.parser import parse
from algorithms.connected import connected_components
import os
import config as cfg


class TestConnected(unittest.TestCase):
    def test_connected(self):
        edges_path = os.path.join(cfg.TESTS_IN_DIR, 'two_component_graph.csv')

        graph = parse(edges_path)

        comp = connected_components(graph)

        expected = ({1, 2, 3}, {4, 5, 6})
        actual =  tuple(comp)
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()

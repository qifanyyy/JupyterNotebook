import unittest
import Graph_OOP


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph_OOP.Graph()
        edge_list = (("A", "B", 3),
                     ("B", "C", 4),
                     ("B", "D", 2),
                     ("A", "D", 20),
                     ("A", "E", 1),
                     ("C", "E", 6),
                     ("D", "E", 5))
        for input_edge in edge_list:
            self.graph.add_edge(*input_edge)

    def tearDown(self):
        self.graph = None

    def test_adj_mat_string(self):
        expected = '  | A B C D E\n' \
                   '_ _ _ _ _ _ _ \n' \
                   'A | 0 3 0 20 1\n' \
                   'B | 0 0 4 2 0\n' \
                   'C | 0 0 0 0 6\n' \
                   'D | 0 0 0 0 5\n' \
                   'E | 0 0 0 0 0\n'
        actual = self.graph.adj_mat_string
        self.assertEqual(expected, actual)

    def test_edge_list_string(self):
        expected = "A, B, 3\n" \
                   "A, D, 20\n" \
                   "A, E, 1\n" \
                   "B, C, 4\n" \
                   "B, D, 2\n" \
                   "C, E, 6\n" \
                   "D, E, 5\n"
        actual = self.graph.edge_list_string
        self.assertEqual(expected, actual)

    def test_is_simple_with_multiple_edge(self):
        self.graph.add_edge("B", "D", 5)
        self.assertFalse(self.graph.is_simple())

    def test_is_simple_with_loop(self):
        self.graph.add_edge("C", "C", 1)
        self.assertFalse(self.graph.is_simple())

    def test_is_simple_with_simple_graph(self):
        self.assertTrue(self.graph.is_simple())
        self.graph.add_edge("D", "B", 2)  # Test edge between same vertices, but opposite direction
        self.assertTrue(self.graph.is_simple())

    def test_remove_edge_weighted(self):
        self.graph.add_edge("B", "D", 5)
        self.graph.remove_edges("B", "D", 2)
        expected = "A, B, 3\n" \
                   "A, D, 20\n" \
                   "A, E, 1\n" \
                   "B, C, 4\n" \
                   "B, D, 5\n" \
                   "C, E, 6\n" \
                   "D, E, 5\n"
        actual = self.graph.edge_list_string
        self.assertEqual(expected, actual)

    def test_remove_edge_unweighted(self):
        self.graph.add_edge("B", "D", 5)
        self.graph.remove_edges("B", "D")
        expected = "A, B, 3\n" \
                   "A, D, 20\n" \
                   "A, E, 1\n" \
                   "B, C, 4\n" \
                   "C, E, 6\n" \
                   "D, E, 5\n"
        actual = self.graph.edge_list_string
        self.assertEqual(expected, actual)

    def test_remove_vertex(self):
        initial_num_vertices = len(self.graph.vertex_names)
        self.graph.remove_vertex("A")
        final_num_vertices = len(self.graph.vertex_names)

        # Check vertices stored
        self.assertEqual(initial_num_vertices, final_num_vertices + 1)

        # Check graph representation
        expected = "B, C, 4\n" \
                   "B, D, 2\n" \
                   "C, E, 6\n" \
                   "D, E, 5\n"
        actual = self.graph.edge_list_string
        self.assertEqual(expected, actual)

    def test_dijkstra_shortest_path_no_revisiting_past_vertices(self):
        path_vertices, path_edges, final_cost = self.graph.dijkstra_shortest_path("A", "C")

        # Verify vertices
        vertex_names = [vertex.name for vertex in path_vertices]
        expected_vertex_names = ["A", "B", "C"]
        self.assertEqual(expected_vertex_names, vertex_names)

        # Verify edges
        edge_names = [edge.edge for edge in path_edges]
        expected_edge_names = [('A', 'B', 3), ('B', 'C', 4)]
        self.assertEqual(expected_edge_names, edge_names)

        # Verify cost
        self.assertEqual(7, final_cost)

    def test_dijkstra_shortest_path_revisit_vertex_with_larger_cost(self):
        # Vertex E is encountered twice: The first time after expanding vertex A, and then again after expanding C.
        # On the second encounter, the path to E through B and C has a larger cost.
        # The cost of E should not be updated, and E should not be added to the priority queue again.
        self.graph.remove_edges("B", "D")
        path_vertices, path_edges, _ = self.graph.dijkstra_shortest_path("A", "D")

        # Verify vertices
        vertex_names = [vertex.name for vertex in path_vertices]
        expected_vertex_names = ["A", "D"]
        self.assertEqual(expected_vertex_names, vertex_names)

        # Verify edges
        edge_names = [edge.edge for edge in path_edges]
        expected_edge_names = [('A', 'D', 20)]
        self.assertEqual(expected_edge_names, edge_names)

        # Verify cost
        self.assertEqual(1, self.graph.get_vertex("E").cost)

    def verify_path_AD(self, weight_AB, weight_BD):
        path_vertices, path_edges, final_cost = self.graph.dijkstra_shortest_path("A", "D")

        # Verify vertices
        vertex_names = [vertex.name for vertex in path_vertices]
        expected_vertex_names = ["A", "B", "D"]
        self.assertEqual(expected_vertex_names, vertex_names)

        # Verify edges
        edge_names = [edge.edge for edge in path_edges]
        expected_edge_names = [('A', 'B', weight_AB), ('B', 'D', weight_BD)]
        self.assertEqual(expected_edge_names, edge_names)

        # Verify cost
        self.assertEqual(weight_AB + weight_BD, final_cost)

    def test_dijkstra_shortest_path_revisit_vertex_with_smaller_cost(self):
        # Vertex D is encountered twice: The first time after expanding vertex A, and then again after expanding B.
        # On the second encounter, the path to D through B has a smaller cost.
        # The cost of D should be updated appropriately.
        # The position of D in the priority queue should be updated to be ahead of C.

        self.verify_path_AD(3, 2)

    def test_dijkstra_shortest_path_with_loop(self):
        # Add loop at vertex C.
        # When C is expanded, the loop is seen as encountering C a second time, but with a larger cost.
        # The loop is therefore not added to the priority queue.
        self.graph.add_edge("C", "C", 1)
        self.graph.add_edge("B", "C", 1)
        self.graph.remove_edges("B", "C", 4)

        self.verify_path_AD(3, 2)

    def test_dijkstra_shortest_path_with_multiple_edge(self):
        # Add edge with a greater weight
        self.graph.add_edge("A", "B", 5)

        self.verify_path_AD(3, 2)

        # Add edge with a lower weight
        self.graph.add_edge("A", "B", 1)

        self.verify_path_AD(1, 2)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGraph)
    unittest.TextTestRunner(verbosity=2).run(suite)

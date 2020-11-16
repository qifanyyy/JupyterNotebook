from unittest import TestCase

from mock import MagicMock

from hungarian import Hungarian


class TestInitialize(TestCase):
    def test_not_nxn(self):
        matrix = [[], []]
        with self.assertRaises(ValueError):
            Hungarian(matrix)

    def test_init_labels(self):
        matrix = [[7, 4, 3], [3, 1, 2], [3, 0, 0]]
        h = Hungarian(matrix)
        h._init_labels()
        self.assertEqual(h.x_labels, [7, 3, 3])
        self.assertEqual(h.y_labels, [0, 0, 0])


class TestFindAugmentingPath(TestCase):
    def test_neighbourhood_s_equals_t(self):
        matrix = [[7, 4, 3], [3, 1, 2], [3, 0, 0]]
        h = Hungarian(matrix)
        h._init_labels()
        h.matching = {0: 0}
        h.inverse_matching = {0: 0}
        h._update_labels = MagicMock()
        copy_find_augmenting_path = h._find_augmenting_path
        h._find_augmenting_path = MagicMock()
        copy_find_augmenting_path({1: None, 0: 1}, {1, 0}, {0})
        h._update_labels.assert_called_once_with({1, 0}, {0})

    def test_found_matched_y(self):
        matrix = [[7, 4, 3], [3, 1, 2], [3, 0, 0]]
        h = Hungarian(matrix)
        h._init_labels()
        h.matching = {0: 0}
        h.inverse_matching = {0: 0}

        copy_find_augmenting_path = h._find_augmenting_path
        h._find_augmenting_path = MagicMock()
        copy_find_augmenting_path({1: None}, {1}, set())

        h._find_augmenting_path.assert_called_once_with({1: None, 0: 1}, {1, 0}, {0})

    def test_found_free_y(self):
        matrix = [[7, 4, 3], [3, 1, 2], [3, 0, 0]]
        h = Hungarian(matrix)
        h._init_labels()
        h.matching = {}
        h.inverse_matching = {}
        t = h._find_augmenting_path({0: None}, {0}, set())
        self.assertEqual(t, (0, 0, {0: None}))


class TestAugmentMatching(TestCase):
    def test_augment_matching(self):
        matrix = [[1, 6, 0], [0, 8, 6], [4, 0, 1]]
        h = Hungarian(matrix)
        h._init_labels()
        h.matching = {1: 1, 2: 0}
        h.inverse_matching = {0: 2, 1: 1}
        path = {1: 0, 0: None}
        h._augment_matching(1, 2, path)
        self.assertEqual(h.matching, {0: 1, 1: 2, 2: 0})
        self.assertEqual(h.inverse_matching, {1: 0, 2: 1, 0: 2})


class TestInEqualityGraph(TestCase):
    def test_not_in_graph(self):
        matrix = [[7, 4, 3], [3, 1, 2], [3, 0, 0]]
        h = Hungarian(matrix)
        h._init_labels()
        self.assertTrue(h._in_equality_graph(0, 0))
        self.assertTrue(h._in_equality_graph(1, 0))
        self.assertTrue(h._in_equality_graph(2, 0))

    def test_in_graph(self):
        matrix = [[7, 4, 3], [3, 1, 2], [3, 0, 0]]
        h = Hungarian(matrix)
        h._init_labels()
        self.assertFalse(h._in_equality_graph(0, 1))
        self.assertFalse(h._in_equality_graph(1, 1))
        self.assertFalse(h._in_equality_graph(2, 1))
        self.assertFalse(h._in_equality_graph(0, 2))
        self.assertFalse(h._in_equality_graph(1, 2))
        self.assertFalse(h._in_equality_graph(2, 2))


class TestUpdateLabels(TestCase):
    def test_update_labels(self):
        matrix = [[7, 4, 3], [3, 1, 2], [3, 0, 0]]
        h = Hungarian(matrix)
        h._init_labels()
        h._update_labels({0, 1}, {0})
        self.assertEqual(h.x_labels, [6, 2, 3])
        self.assertEqual(h.y_labels, [1, 0, 0])


class TestCompute(TestCase):
    def test_minimize(self):
        pass

    def test_maximize(self):
        matrix = [[7, 4, 3], [3, 1, 2], [3, 0, 0]]
        h = Hungarian(matrix)
        h.compute()
        self.assertEqual(9, h.total_profit)


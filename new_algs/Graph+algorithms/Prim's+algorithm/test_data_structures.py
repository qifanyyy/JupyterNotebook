import unittest
from mstfind.data_structures import PriorityQueue, UnionFind


class TestPriorityQueue(unittest.TestCase):

    def setUp(self):
        self.queue = PriorityQueue()
        self.queue.put((10, 'a'))
        self.queue.put((3, 'b'))
        self.queue.put((5, 'c'))

    def test_get_order(self):
        self.assertEqual(self.queue.get(), (3, 'b'))
        self.assertEqual(self.queue.get(), (5, 'c'))
        self.assertEqual(self.queue.get(), (10, 'a'))

class TestUnionFind(unittest.TestCase):

    def setUp(self):
        self.uf = UnionFind()
    
    def test_find(self):
        self.uf.add('A')
        self.assertEqual(self.uf.find('A'), 'A')

    def test_union(self):
        self.uf.add('A')
        self.uf.add('B')
        self.uf.union('A', 'B')
        self.assertEqual(self.uf.find('B'), 'A')
        self.assertEqual(self.uf._node('A').rank, 1)

        self.uf.add('E')
        self.uf.union('E', 'B')
        self.assertEqual(self.uf.find('B'), 'A')
        self.assertEqual(self.uf.find('E'), 'A')
        self.assertEqual(self.uf._node('A').rank, 1)

        self.uf.add('C')
        self.uf.add('D')
        self.uf.union('C', 'D')
        self.assertEqual(self.uf.find('D'), 'C')
        self.assertEqual(self.uf._node('C').rank, 1)
        
        self.uf.union('D', 'E')
        self.assertEqual(self.uf.find('D'), 'C')
        self.assertEqual(self.uf.find('A'), 'C')
        self.assertEqual(self.uf.find('B'), 'C')
        self.assertEqual(self.uf.find('E'), 'C')


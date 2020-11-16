from kruskal import kruskal
import unittest

class TestKruskal(unittest.TestCase):    
    def testFind(self):     
        k = kruskal([])

        #Disjoint set #1        
        k.sets.append(['g', 'd', 2])
        k.sets.append(['a', 'f', 2])
        k.sets.append(['c', 'h', 1])
        k.sets.append(['d', 'h', 1])
        k.sets.append(['f', 'h', 1])
        k.sets.append(['h', None, 0])

        #Disjoint set #2
        k.sets.append(['b', 'e', 1])
        k.sets.append(['e', None, 0])


        #Disjoint set #1 tests
        self.assertEqual(k.find('a'), ['h', None, 0])
        self.assertEqual(k.find('g'), ['h', None, 0])
        self.assertEqual(k.find('c'), ['h', None, 0])
        self.assertEqual(k.find('d'), ['h', None, 0])
        self.assertEqual(k.find('f'), ['h', None, 0])

        #Disjoint set #2 tests
        self.assertEqual(k.find('b'), ['e', None, 0])
        self.assertEqual(k.find('e'), ['e', None, 0])

        #Not in any set tests
        self.assertEqual(k.find('z'), [])
        self.assertEqual(k.find(28), [])
        self.assertEqual(k.find(''), [])
        
    
    def testUnion(self):
        k = kruskal([])
    
        k.makeSet('a')
        k.makeSet('b')
        k.makeSet('c')
        k.makeSet('d')
        k.makeSet('e')
        k.makeSet('f')
        k.makeSet('g')
        
        self.assertEqual(k.sets, \
                         [['a', None, 0], \
                          ['b', None, 0], \
                          ['c', None, 0], \
                          ['d', None, 0], \
                          ['e', None, 0], \
                          ['f', None, 0], \
                          ['g', None, 0] \
                         ])

        k.union('a', 'd')
        k.union('b', 'e')
        k.union('c', 'f')
        self.assertEqual(k.sets, \
                         [['a', 'd', 0], \
                          ['b', 'e', 0], \
                          ['c', 'f', 0], \
                          ['d', None, 1], \
                          ['e', None, 1], \
                          ['f', None, 1], \
                          ['g', None, 0] \
                         ])
        
        k.union('c', 'g')
        k.union('e', 'a')
        self.assertEqual(k.sets, \
                         [['a', 'd', 0], \
                          ['b', 'e', 0], \
                          ['c', 'f', 0], \
                          ['d', None, 2], \
                          ['e', 'd', 1], \
                          ['f', None, 1], \
                          ['g', 'f', 0] \
                         ])
        k.union('b', 'g')
        self.assertEqual(k.sets, \
                         [['a', 'd', 0], \
                          ['b', 'e', 0], \
                          ['c', 'f', 0], \
                          ['d', None, 2], \
                          ['e', 'd', 1], \
                          ['f', 'd', 1], \
                          ['g', 'f', 0] \
                         ])

    def testKruskal(self):
        edges = []
        file = open("graph1.txt", 'r')
        #Format of each line in file: vertex1 vertex2 distance
        for line in file:
            v1, v2, dist = line.split()    
            edges.append([v1, v2, int(dist)])
        file.close()

        k = kruskal(edges)
        self.assertEqual(k.run(), \
                         [['a', 'e', 1], \
                          ['c', 'd', 2], \
                          ['a', 'b', 3], \
                          ['b', 'c', 5]  \
                         ])
        
if __name__ == "__main__":
    unittest.main(exit=False)






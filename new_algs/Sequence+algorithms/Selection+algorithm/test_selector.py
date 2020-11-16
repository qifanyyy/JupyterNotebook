import numpy as np
import unittest
import random
from genetic_selection.genetic_selector import GeneticSelector

class TestGeneticSelector(unittest.TestCase):

    def test_tournament_selection(self):    
        random.seed(123)    
        gs = GeneticSelector(None, 0, 5, 10, 0, 0, 0, 0, 0, 0, 0)
        genes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        scores = np.array([1, 5, 7, 2, 10, 3, 8, 4, 2, 10])
        self.assertEqual(gs.tournament_selection(scores, genes), 'e')

    def test_mutation(self):
        random.seed(123)
        gs = GeneticSelector(None, 0, 0, 0, 0.5, 20, 5, 0, 0, 0, 0)
        gene = [1, 2, 3, 4, 5]
        mutated = gs.mutate_gene(gene)
        self.assertListEqual([6, 4, 18, 2, 0], mutated)

if __name__ == "__main__":
    unittest.main()
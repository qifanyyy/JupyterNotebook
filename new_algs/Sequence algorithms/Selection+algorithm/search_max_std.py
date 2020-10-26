import sys, os
sys.path.insert(0, os.path.abspath('..'))
from genetic_selection.genetic_selector import GeneticSelector
from genetic_selection import score_provider
import numpy as np

class SumScoreProvider(score_provider.ScoreProvider):
    
    def compute_score(self, genes):
        return np.array([np.std(gene) for gene in genes])

sum_score_provider = SumScoreProvider()
gs = GeneticSelector(sum_score_provider, 2, 4, 100, 0.1, 100, 10, 0.5, 0.5, 200, 1000, verbose=True)

res = gs.search()
print(res)
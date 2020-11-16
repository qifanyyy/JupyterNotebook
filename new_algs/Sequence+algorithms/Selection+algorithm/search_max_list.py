import sys, os
sys.path.insert(0, os.path.abspath('..'))
from genetic_selection.genetic_selector import GeneticSelector
from genetic_selection import score_provider
import numpy as np

class ListScoreProvider(score_provider.ScoreProvider):
    
    values = np.random.random(100)

    def compute_score(self, genes):
        return np.array([np.sum(self.values[gene]) for gene in genes])

list_score_provider = ListScoreProvider()
print(np.sum(sorted(list_score_provider.values, reverse=True)[:10]))

gs = GeneticSelector(list_score_provider, 2, 4, 100, 0.2, 100, 10, 0.5, 0.5, 200, 1000, verbose=True)

res = gs.search()

print(res)
print(np.sum(sorted(list_score_provider.values, reverse=True)[:10]))
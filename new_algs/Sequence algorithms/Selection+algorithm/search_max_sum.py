import sys, os
sys.path.insert(0, os.path.abspath('..'))
from genetic_selection.genetic_selector import GeneticSelector
from genetic_selection import score_provider
import numpy as np

class SumScoreProvider(score_provider.ScoreProvider):
    
    def compute_score(self, genes):
        return np.array([sum(gene) for gene in genes])

sum_score_provider = SumScoreProvider()
gs = GeneticSelector(sum_score_provider, 2, 4, 100, 0.2, 100, 10, 0.5, 0.5, 200, 1000, verbose=True, log=True, log_file='data.csv')
# you can run 'run_visualization.py'
res = gs.search()

print(res)
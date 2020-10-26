import graph_tool.all as gt
from packing_coloring.graph_generator import *
from packing_coloring.utils import *
from packing_coloring.algorithms.problem import *

from packing_coloring.algorithms.perturbative.tabupackcol import *

import numpy as np
import pandas as pd
import igraph
np.set_printoptions(threshold=np.nan)
import cProfile

def square_grid_ts_pcoloring(size):
    g = gt.lattice([size, size])
    dist_mat = get_distance_matrix(g)
    prob = GraphProblem(dist_mat)

    p_col1 = tabu_pack_col(prob, k_count=5, tt_a=10, tt_d=0.6, max_iter=1000)

    max_col = p_col1.get_max_col()

    print(np.max(p_col1))
    print(p_col1)
    
def random_ts_pcoloring():
    g = gt.load_graph("instances/dot_format/random.dot")
    dist_mat = get_distance_matrix(g)
    prob = GraphProblem(dist_mat)

    p_col1 = tabu_pack_col(prob, k_count=10, tt_a=5, tt_d=0.6, max_iter=1000)

    max_col = p_col1.get_max_col()

    print(np.max(p_col1))
    print(p_col1)

cProfile.run('square_grid_ts_pcoloring(3)', 'test2.prof')
#square_grid_pts_pcoloring(24)
#random_pts_pcoloring()




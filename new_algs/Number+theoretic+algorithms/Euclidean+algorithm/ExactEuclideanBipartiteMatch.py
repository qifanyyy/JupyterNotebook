from lapsolver import solve_dense
from agarwal_paper.functions.get_dist_matrix import *


class ExactEuclideanBipartiteMatch:
    def __init__(self, node_set):
        self.pos_1, self.pos_2 = node_set

    def match(self, islonlat=False, distance_category='euclidean'):
        # pos_1 and pos_2 are both two-column numpy array
        # denoting the longitude and latitude coordinates
        # distance_category = ['manhattan', 'euclidean']

        dist_mat = get_dist_mat(self.pos_1, self.pos_2, islonlat=islonlat, how=distance_category)

        # lapsolver (much faster than `scipy.optimize.linear_sum_assignment`)
        # https://github.com/cheind/py-lapsolver
        # Works well for float32 type of cost matrix
        # Scale distances up to make integer different

        dist_mat_float = dist_mat.astype('float32')
        ind_1, ind_2 = solve_dense(dist_mat_float)

        bipartite_distance_array = dist_mat[ind_1, ind_2]

        avg_distance = np.mean(bipartite_distance_array)

        return bipartite_distance_array, avg_distance, ind_1, ind_2

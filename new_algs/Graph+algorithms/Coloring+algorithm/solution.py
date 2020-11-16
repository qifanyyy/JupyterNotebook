# -*- coding: utf-8 -*-
import numpy as np

class PackColSolution:
    def __init__(self, g_prob=None):
        self.pack_col = None
        if g_prob is None:
            self.pack_col = np.zeros([], dtype=int)
        else:
            self.pack_col = np.zeros(g_prob.v_size, dtype=int)
            self.v_size = g_prob.v_size

    def copy(self):
        pcol = PackColSolution()
        pcol.pack_col = self.pack_col.copy()
        pcol.v_size = self.v_size
        return pcol

    def uncolored(self):
        return self.pack_col == 0

    def colored(self):
        return self.pack_col != 0

    def count_uncolored(self):
        return np.sum(self.pack_col == 0)

    def get_greedy_order(self):
        return np.argsort(self.pack_col)

    def pack_size(self, k_col):
        return np.sum(self.pack_col == k_col)

    def is_complete(self):
        return (not np.any(self.pack_col == 0))

    def is_partial(self):
        return np.any(self.pack_col == 0)

    def get_sum(self):
        return np.sum(self.pack_col)

    def get_kcol_cover(self, prob, k_col):
        kcol_nodes = self.pack_col == k_col
        dist_mat = prob.dist_matrix[kcol_nodes]
        cover_score = np.sum(dist_mat <= k_col)
        cover_score -= np.sum(kcol_nodes)
        return cover_score

    def get_partitions(self):
        max_pack = self.get_max_col()
        packing = np.zeros((max_pack+1, self.v_size), dtype=bool)
        for k in range(max_pack+1):
            mask = (self.pack_col == k)
            packing[k, mask] = True
        return packing

    def get_kpartition(self, k_col):
        return np.arange(self.v_size)[self.pack_col == k_col]

    def get_by_permut(self, col):
        permut = np.array([], dtype=int)
        for k in col:
            permut = np.append(permut, self.get_kpartition(k))
        return permut

    def get_max_col(self):
        return max(self.pack_col)

    def get_k_area(self, prob, k_col):
        kcol_nodes = (self.pack_col == k_col)
        dist_mat = prob.dist_matrix.A
        kcol_dist = dist_mat[kcol_nodes]

        first_half = np.floor(float(k_col)/2)
        half_nodes = kcol_dist <= first_half
        # half_nodes[kcol_dist == 0] = False
        area_score = np.sum(half_nodes)

        if k_col % 2 == 1:
            border = np.ceil(float(k_col)/2)
            for x in np.arange(prob.v_size)[kcol_nodes]:
                x_dist = dist_mat[x]
                x_half_nodes = (x_dist <= first_half)

                border_nodes = (x_dist == border)
                for y in np.arange(prob.v_size)[border_nodes]:
                    y_neighbors = (dist_mat[y] == 1)
                    common = np.logical_and(y_neighbors, x_half_nodes)
                    area_score += float(np.sum(common))/np.sum(y_neighbors)

        area_score = float(area_score)/np.sum(kcol_nodes)
        return area_score

    def get_area_score(self, prob):
        scores = np.zeros(self.get_max_col(), dtype=float)
        for col in np.arange(1, self.get_max_col()+1):
            scores[col-1] = self.get_k_area(prob, col)
        scores = np.nan_to_num(scores)
        scores = 1./scores[scores != 0]
        scores[scores == np.inf] = 0
        return np.abs(1. - np.sum(scores))

    def __eq__(self, val):
        if np.issubdtype(type(val), np.integer):
            return self.pack_col == val
        elif type(val) is PackColSolution:
            return np.all(np.equal(self.pack_col, val.pack_col))

    def __ne__(self, val):
        if np.issubdtype(type(val), np.integer):
            return self.pack_col != val
        elif type(val) is PackColSolution:
            return np.any(np.not_equal(self.pack_col, val.pack_col))

    def __lt__(self, val):
        if np.issubdtype(type(val), np.integer):
            return self.pack_col < val
        elif type(val) is PackColSolution:
            if val.is_partial():
                return np.sum(self.colored()) < np.sum(val.colored())
            else:
                return self.get_max_col() < val.get_max_col()

    def __le__(self, val):
        if np.issubdtype(type(val), np.integer):
            return self.pack_col <= val
        elif type(val) is PackColSolution:
            if val.is_partial():
                return np.sum(self.colored()) <= np.sum(val.colored())
            else:
                return self.get_max_col() <= val.get_max_col()

    def __gt__(self, val):
        if np.issubdtype(type(val), np.integer):
            return self.pack_col > val
        elif type(val) is PackColSolution:
            if val.is_partial():
                return np.sum(self.colored()) > np.sum(val.colored())
            else:
                return self.get_max_col() > val.get_max_col()

    def __ge__(self, val):
        if np.issubdtype(type(val), np.integer):
            return self.pack_col >= val
        elif type(val) is PackColSolution:
            if val.is_partial():
                return np.sum(self.colored()) >= np.sum(val.colored())
            else:
                return self.get_max_col() >= val.get_max_col()

    def __contains__(self, val):
        if np.issubdtype(type(val), np.integer):
            return val in self.pack_col
        elif type(val) is PackColSolution:
            if val.is_partial():
                not_zeros = (val.pack_col != 0)
                return (self.pack_col[not_zeros] == val.pack_col[not_zeros])
            else:
                return np.all(self.pack_col == val.pack_col)

    def __len__(self):
        return len(self.pack_col)

    def __getitem__(self, key):
        try:
            return self.pack_col[key]
        except IndexError:
            raise IndexError("index out of bound: {0}".format(key))

    def __setitem__(self, key, value):
        try:
            self.pack_col[key] = value
        except IndexError:
            raise IndexError("index out of bound: {0}".format(key))
        except ValueError:
            raise ValueError("wrong value type: {0}, {1}".format(
                self.pack_col.dtype, type(value)))

    def __str__(self):
        return str(self.pack_col)

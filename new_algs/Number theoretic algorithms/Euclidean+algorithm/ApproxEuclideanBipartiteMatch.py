import networkx as nx
from agarwal_paper.functions.ExactEuclideanBipartiteMatch import *
from agarwal_paper.functions.get_dist_matrix import *
from agarwal_paper.functions.minimum_spanning_tree import *


class ApproxEuclideanBipartiteMatch:
    def __init__(self, node_set, epsilon, C):
        self.node_set = node_set
        self.node_set_ind = [np.arange(len(self.node_set[i])) for i in [0, 1]]

        self.epsilon = epsilon
        self.pos_1, self.pos_2 = self.node_set
        self.C = C  # the size of nodes under which exact algorithm is run

        # Square bound
        pos_concat = np.concatenate((self.pos_1, self.pos_2), axis=0)
        self.min_x, self.max_x = np.min(pos_concat[:, 0]), np.max(pos_concat[:, 0])
        self.min_y, self.max_y = np.min(pos_concat[:, 1]), np.max(pos_concat[:, 1])

        self.bound_sqr_side_len = max(self.max_x - self.min_x, self.max_y - self.min_y)

    def match(self):
        # num of nodes
        m = (len(self.pos_1) + len(self.pos_2)) / 2

        if m <= self.C:  # If # of nodes lower than a constant, use conventional algorithm
            bipartite_distance_array, avg_distance, ind_1, ind_2 = \
                ExactEuclideanBipartiteMatch(self.node_set).match()  # returns global index
            output_ind_1 = ind_1
            output_ind_2 = ind_2
        else:
            # Find alpha
            alpha = self.compute_alpha()
            grid_delta = 2 * m ** 5 * alpha  # TODO: ISSUE: grid_delta can be so huge, if m is huge

            if grid_delta > (self.bound_sqr_side_len / 8):  # Do submatch
                bipartite_distance_array, avg_distance, ind_1, ind_2 = \
                    self.submatch(self.node_set_ind, self.bound_sqr_side_len, alpha, m)  # Returns global index
                output_ind_1 = ind_1
                output_ind_2 = ind_2
                result_bipartite_distance_array = bipartite_distance_array
            else:  # Do conventional match for extra nodes: DIDN'T RUN
                cell_bounds = self.create_grid(grid_delta)
                extra_pos_1_ind_array = np.array([])
                extra_pos_2_ind_array = np.array([])
                result_bipartite_distance_array = np.array([])
                result_ind_1_array = np.array([])
                result_ind_2_array = np.array([])

                for cell in cell_bounds:
                    pos_1_ind_in_cell = self.find_node_in_cell(self.pos_1, cell)
                    pos_2_ind_in_cell = self.find_node_in_cell(self.pos_2, cell)
                    num_pos_1_in_cell, num_pos_2_in_cell = len(pos_1_ind_in_cell), len(pos_2_ind_in_cell)

                    if num_pos_1_in_cell + num_pos_2_in_cell == 0:
                        continue

                    num_extra_nodes = abs(num_pos_1_in_cell - num_pos_2_in_cell)
                    if num_pos_1_in_cell > num_pos_2_in_cell:
                        extra_pos_1_ind_in_cell = \
                            pos_1_ind_in_cell[np.random.choice(num_pos_1_in_cell, num_extra_nodes, replace=False)]
                        extra_pos_1_ind_array = np.append(extra_pos_1_ind_array, extra_pos_1_ind_in_cell)
                        pos_1_ind_in_cell = np.setdiff1d(pos_1_ind_in_cell, extra_pos_1_ind_in_cell)
                    else:
                        extra_pos_2_ind_in_cell = \
                            pos_2_ind_in_cell[np.random.choice(num_pos_2_in_cell, num_extra_nodes, replace=False)]
                        extra_pos_2_ind_array = np.append(extra_pos_2_ind_array, extra_pos_2_ind_in_cell)
                        pos_2_ind_in_cell = np.setdiff1d(pos_2_ind_in_cell, extra_pos_2_ind_in_cell)

                    # For remnant nodes in the cell, submatch them
                    if len(pos_1_ind_in_cell) + len(pos_2_ind_in_cell) == 0:
                        continue

                    node_set_ind = [pos_1_ind_in_cell, pos_2_ind_in_cell]
                    bipartite_distance_array, avg_distance, ind_1, ind_2 = \
                        self.submatch(node_set_ind, grid_delta, alpha, m)  # Returns global index
                    result_bipartite_distance_array = np.append(result_bipartite_distance_array,
                                                                bipartite_distance_array)
                    result_ind_1_array = np.append(result_ind_1_array, ind_1)
                    result_ind_2_array = np.append(result_ind_2_array, ind_2)

                # Match all extra nodes
                if len(extra_pos_1_ind_array) > 0:
                    extra_node_set_ind = [extra_pos_1_ind_array,
                                          extra_pos_2_ind_array]

                    extra_node_set = [self.pos_1[extra_node_set_ind[0]],
                                      self.pos_2[extra_node_set_ind[1]]]

                    # Move to cell center and do matching
                    extra_node_set_moved = self.move_to_cell_center(extra_node_set, cell_bounds)

                    _, avg_distance, ind_1, ind_2 = \
                        ExactEuclideanBipartiteMatch(extra_node_set_moved).match()  # returns local index
                    bipartite_distance_array = get_dist_mat(extra_node_set[0], extra_node_set[1], islonlat=False)[
                        ind_1, ind_2]

                    # Combined results
                    result_bipartite_distance_array = np.append(result_bipartite_distance_array,
                                                                bipartite_distance_array)
                    result_ind_1_array = np.append(result_ind_1_array, extra_node_set_ind[0][ind_1])
                    result_ind_2_array = np.append(result_ind_2_array, extra_node_set_ind[1][ind_2])

                output_ind_1 = result_ind_1_array
                output_ind_2 = result_ind_2_array
                avg_distance = np.mean(result_bipartite_distance_array)

        output_ind_1, output_ind_2 = np.int_(output_ind_1), np.int_(output_ind_2)

        return result_bipartite_distance_array, avg_distance, output_ind_1, output_ind_2

    def submatch(self, node_set_ind, side_length, alpha, m):
        sub_ind_1, sub_ind_2 = node_set_ind
        sub_pos_1, sub_pos_2 = self.pos_1[sub_ind_1], self.pos_2[sub_ind_2]
        sub_node_set = [sub_pos_1, sub_pos_2]

        m_sub = (len(sub_pos_1) + len(sub_pos_2)) / 2

        if m_sub == 0:
            a = np.array([])

            return a, None, a, a

        if side_length <= alpha / (m ** 2):  # do random match: DIDN'T RUN
            # Random match
            sub_ind_2_shuffled = sub_ind_2.copy()
            np.random.shuffle(sub_ind_2_shuffled)

            dist_mat = get_dist_mat(sub_pos_1, sub_pos_2, islonlat=False)
            bipartite_distance_array = dist_mat[sub_ind_1, sub_ind_2_shuffled]
            avg_distance = np.mean(bipartite_distance_array)

            result_bipartite_distance_array = bipartite_distance_array
            output_ind_1 = sub_ind_1
            output_ind_2 = sub_ind_2
        else:
            delta = self.epsilon / 12

            if m_sub <= m ** (6 * delta):  # Do conventional match: DID
                bipartite_distance_array, avg_distance, ind_1, ind_2 = \
                    ExactEuclideanBipartiteMatch(sub_node_set).match()  # returns local index

                result_bipartite_distance_array = bipartite_distance_array
                output_ind_1 = sub_ind_1[ind_1]
                output_ind_2 = sub_ind_2[ind_2]
            else:  # DID
                grid_delta = side_length / max(8, m ** delta)

                cell_bounds = self.create_grid(grid_delta)
                extra_pos_1_ind_array = np.array([])
                extra_pos_2_ind_array = np.array([])
                result_bipartite_distance_array = np.array([])
                result_ind_1_array = np.array([])
                result_ind_2_array = np.array([])

                for i, cell in enumerate(cell_bounds):
                    pos_1_ind_in_cell = self.find_node_in_cell(sub_pos_1, cell)
                    pos_2_ind_in_cell = self.find_node_in_cell(sub_pos_2, cell)

                    num_pos_1_in_cell, num_pos_2_in_cell = len(pos_1_ind_in_cell), len(pos_2_ind_in_cell)

                    if num_pos_1_in_cell + num_pos_2_in_cell == 0:
                        continue

                    num_extra_nodes = abs(num_pos_1_in_cell - num_pos_2_in_cell)

                    if num_pos_1_in_cell > num_pos_2_in_cell:
                        extra_pos_1_ind_in_cell = \
                            pos_1_ind_in_cell[np.random.choice(num_pos_1_in_cell, num_extra_nodes, replace=False)]
                        extra_pos_1_ind_array = np.append(extra_pos_1_ind_array, extra_pos_1_ind_in_cell)
                        pos_1_ind_in_cell = np.setdiff1d(pos_1_ind_in_cell, extra_pos_1_ind_in_cell)
                    else:
                        extra_pos_2_ind_in_cell = \
                            pos_2_ind_in_cell[np.random.choice(num_pos_2_in_cell, num_extra_nodes, replace=False)]
                        extra_pos_2_ind_array = np.append(extra_pos_2_ind_array, extra_pos_2_ind_in_cell)
                        pos_2_ind_in_cell = np.setdiff1d(pos_2_ind_in_cell, extra_pos_2_ind_in_cell)

                    # For remnant nodes
                    if len(pos_1_ind_in_cell) + len(pos_2_ind_in_cell) == 0:
                        continue

                    node_set_ind = [sub_ind_1[pos_1_ind_in_cell], sub_ind_2[pos_2_ind_in_cell]]
                    bipartite_distance_array, avg_distance, ind_1, ind_2 = \
                        self.submatch(node_set_ind, grid_delta, alpha, m)  # Returns global index
                    result_bipartite_distance_array = np.append(result_bipartite_distance_array,
                                                                bipartite_distance_array)
                    result_ind_1_array = np.append(result_ind_1_array, ind_1)
                    result_ind_2_array = np.append(result_ind_2_array, ind_2)

                # Match all extra nodes
                if len(extra_pos_1_ind_array) > 0:
                    extra_pos_1_ind_array, extra_pos_2_ind_array = \
                        np.int_(extra_pos_1_ind_array), np.int_(extra_pos_2_ind_array)

                    extra_node_set_ind = [sub_ind_1[extra_pos_1_ind_array],
                                          sub_ind_2[extra_pos_2_ind_array]]
                    extra_node_set = [self.pos_1[extra_node_set_ind[0]],
                                      self.pos_2[extra_node_set_ind[1]]]

                    # Move to cell center and do matching
                    extra_node_set_moved = self.move_to_cell_center(extra_node_set, cell_bounds)

                    _, avg_distance, ind_1, ind_2 = \
                        ExactEuclideanBipartiteMatch(extra_node_set_moved).match()  # returns local index
                    bipartite_distance_array = get_dist_mat(extra_node_set[0], extra_node_set[1], islonlat=False)[
                        ind_1, ind_2]

                    # Combined results
                    result_bipartite_distance_array = np.append(result_bipartite_distance_array,
                                                                bipartite_distance_array)

                    result_ind_1_array = np.append(result_ind_1_array, extra_node_set_ind[0][ind_1])
                    result_ind_2_array = np.append(result_ind_2_array, extra_node_set_ind[1][ind_2])

                output_ind_1 = result_ind_1_array
                output_ind_2 = result_ind_2_array
                avg_distance = np.mean(result_bipartite_distance_array)

        output_ind_1, output_ind_2 = np.int_(output_ind_1), np.int_(output_ind_2)

        return result_bipartite_distance_array, avg_distance, output_ind_1, output_ind_2

    def compute_alpha(self):
        return 0.01

        i_star = 0
        # Total number of nodes
        N = len(self.pos_1) + len(self.pos_2)

        # Compute Minimum Spanning Tree (MST)
        all_nodes = np.concatenate((self.pos_1, self.pos_2), axis=0)

        A = get_dist_mat(all_nodes, all_nodes, islonlat=False)

        R = minimum_spanning_tree(A)
        tree_list = [[(r[0], r[1]), A[r[0], r[1]]] for r in R]

        tree_list = sorted(tree_list, key=lambda x: x[-1])

        for i in range(1, len(tree_list) + 1):
            # Create edge-induced subgraph
            subgraph_edges = [r[0] for r in tree_list[:i]]
            S = nx.Graph(subgraph_edges)
            component = list(nx.connected_component_subgraphs(S))

            # print(i, len(component))
            equal_num_of_both_parties = True

            for j, c in enumerate(component):
                edges = np.array(list(c.edges))
                nodes_array = np.unique(edges.flatten())

                if len(nodes_array) % 2 == 1 or np.sum(nodes_array < (N / 2)) != np.sum(nodes_array >= (N / 2)):
                    equal_num_of_both_parties = False
                    # print('[%d/%d] Component %s doesn\'t include same number of both parties (nodes %s)'
                    #       % (j, len(component), list(c.edges), nodes_array))
                    break

            if equal_num_of_both_parties:  # i_star found
                i_star = i - 1
                break

        alpha = tree_list[i_star][-1]

        print('alpha=%0.5f, i*=%d, num_of_components=%d' % (alpha, i_star, len(component)))

        return alpha

    def create_grid(self, grid_delta):
        a_x = np.random.uniform(0, grid_delta, 1)
        a_y = np.random.uniform(0, grid_delta, 1)

        min_i = np.int_(np.floor((self.min_x - a_x) / grid_delta))
        max_i = np.int_(np.ceil((self.max_x + a_x) / grid_delta))

        min_j = np.int_(np.floor((self.min_y - a_y) / grid_delta))
        max_j = np.int_(np.ceil((self.max_y + a_y) / grid_delta))

        cell_bounds = []
        for i in np.arange(min_i, max_i):
            x_min = i * grid_delta + a_x
            x_max = (i + 1) * grid_delta + a_x
            for j in np.arange(min_j, max_j):
                y_min = j * grid_delta + a_y
                y_max = (j + 1) * grid_delta + a_y

                cell_bound = [[x_min[0], x_max[0]], [y_min[0], y_max[0]]]

                cell_bounds.append(cell_bound)
        return cell_bounds

    def find_node_in_cell(self, nodes, cell_bound):
        [[min_x, max_x], [min_y, max_y]] = cell_bound
        ind = (min_x < nodes[:, 0]) & (nodes[:, 0] <= max_x) & (min_y < nodes[:, 1]) & (nodes[:, 1] <= max_y)
        ind = np.where(ind)[0]

        return ind

    def move_to_cell_center(self, nodes, cell_bounds):
        cell_bounds = np.array(cell_bounds)
        x_gap, y_gap = np.diff(cell_bounds[0], 1).flatten().tolist()
        x_min = cell_bounds[:, 0].min()
        y_min = cell_bounds[:, 1].min()

        val_min = np.array([x_min, y_min])
        pos_1, pos_2 = nodes
        pos_1_shifted = np.floor((pos_1 - val_min) / x_gap + 0.5) * x_gap + val_min
        pos_2_shifted = np.floor((pos_2 - val_min) / x_gap + 0.5) * x_gap + val_min

        nodes_shifted = [pos_1_shifted, pos_2_shifted]

        return nodes_shifted

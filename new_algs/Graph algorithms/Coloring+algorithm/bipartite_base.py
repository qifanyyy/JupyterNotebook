import copy
import logging
import os
import sys
from datetime import datetime


class BipartiteMixin:

    def deepcopy(self):
        return copy.deepcopy(self)

    def copy(self):
        return copy.copy(self)

    def find_cole_hopcroft_covering_matching(self):
        M_containing_set = self.max_degree_vertices()
        logging.debug("initial M-cont set is " + str(M_containing_set))
        itergraph = self.copy()
        logging.debug("incident before is " + str(itergraph.incident))

        while itergraph.max_degree('degree') > 1:
            G1, G2 = itergraph.cole_hopcroft_covering_partition()
            logging.debug(str(G1.max_degree('degree')) + " G1 max degree")
            logging.debug(str(G2.max_degree('degree')) + " G2 max degree")
            logging.debug("G1 incident " + str(G1.incident))
            logging.debug("G2 incident " + str(G2.incident))
            # criteria
            G1_max_degree = G1.max_degree('degree')
            G2_max_degree = G2.max_degree('degree')

            return_from_while_loop = False
            if G1_max_degree == 1 and G2_max_degree == 1:
                for elem in M_containing_set:
                    logging.debug("ELEM FROM M-CONT_SET")
                    if elem in G1.incident:
                        itergraph = G1
                        return_from_while_loop = True
                        logging.debug("G1 RESOLVED")
                        break
                    else:
                        itergraph = G2
                        return_from_while_loop = True
                        logging.debug("G2 RESOLVED")
                        break

            if return_from_while_loop:
                break

            if G1_max_degree is not None and G1_max_degree == 1:
                itergraph = G1
                break
            elif G2_max_degree is not None and G2_max_degree == 1:
                itergraph = G2
                break

            if G1_max_degree > G2_max_degree:
                itergraph = G2
            else:
                itergraph = G1

        matching = []
        for node in itergraph.incident:
            if node in M_containing_set:
                for node_incident in itergraph.incident[node]:
                    matching.append((node, node_incident))
                    if node_incident not in M_containing_set:
                        matching.append((node_incident, node))

        logging.debug("incident after is " + str(itergraph.incident))
        logging.debug('matching is ' + str(matching))
        return matching

    def euler_partiton(self, with_deepcopy=True):
        logging.debug("start partition")
        if with_deepcopy:
            graph_to_color_copy = self.deepcopy()
        else:
            graph_to_color_copy = self.copy()

        partitions = []
        queue = []
        odd_degrees = []
        even_degrees = []

        for node in graph_to_color_copy.incident:
            degree = graph_to_color_copy.degree(node)
            if degree % 2 == 0:
                even_degrees.append(node)
            else:
                odd_degrees.append(node)

        queue.extend(odd_degrees)
        queue.extend(even_degrees)

        while len(queue) != 0:
            first_node = queue[0]
            queue.remove(first_node)

            if graph_to_color_copy.degree(first_node) != 0:
                new_path = []
                current_node = first_node

                while graph_to_color_copy.degree(current_node) != 0:
                    processing_vertex_neighbors = graph_to_color_copy.neighbors(current_node)
                    next_node = processing_vertex_neighbors[0]
                    graph_to_color_copy.remove_edge(current_node, next_node)
                    new_path.append((current_node, next_node))
                    current_node = next_node

                partitions.append(new_path)
                if graph_to_color_copy.degree(first_node) != 0:
                    queue.append(first_node)

        logging.debug(partitions)

        return partitions

    # @timing
    def euler_split(self, with_graph_copy):
        logging.debug("start split")
        H1_edges = []
        H2_edges = []

        partitions = self.euler_partiton(with_deepcopy=with_graph_copy)

        for partition in partitions:
            count = 0
            for edge in partition:
                if count % 2 == 0:
                    H1_edges.append(edge)
                else:
                    H2_edges.append(edge)
                count += 1

        H1_new = self.__class__()
        H2_new = self.__class__()

        for edge in H1_edges:
            H1_new.add_edge(edge[0], edge[1])

        for edge in H2_edges:
            H2_new.add_edge(edge[0], edge[1])

        # self.draw_euler_split(H1_new, H2_new)

        return H1_new, H2_new

    def draw_euler_split(self, G1, G2):
        colors = ['Purple', 'Orange', 'Yellow', 'Green', 'Brown', 'Pink']
        time = str(datetime.now())
        # pathlib.Path('/results/' + str(self.__class__.i)).mkdir(parents=True, exist_ok=True)
        # logging.debug(sys.path[0])
        os.makedirs(sys.path[0] + '/results/' + str(self.__class__.i), exist_ok=True)
        pos = self.draw_graph_simple('black',
                                     str(self.__class__.i) + '/' + 'euler_split_initial_graph' + " " + time + ".png")

        parts = [G1, G2]
        colors = ['Orange', 'Green']
        for i in range(0, 2):
            parts[i].draw_graph_simple(colors[i], str(self.__class__.i) + '/' +
                                       'euler_split_part' + str(i) + " " + time + ".png", pos)
            self.__class__.i += 1

    def cole_hopcroft_covering_partition(self):
        logging.debug("covering partition")
        if self.max_degree('degree') % 2 == 0:
            return self.euler_split(with_graph_copy=False)

        H1, H2 = self.euler_split(with_graph_copy=True)
        M_containing_set = self.max_degree_vertices()
        logging.debug("M containing set is " + str(M_containing_set))
        D = self.max_degree('degree')
        logging.debug("D is " + str(D))
        odd_count1 = 0
        odd_count2 = 0

        e = -666
        r = -666

        if D % 4 == 3:
            e = -1
            r = (D + 1) // 4
        else:
            e = 1
            r = D // 4

        k = r
        d = e

        for node in M_containing_set:
            H1_degree = H1.degree(node)

            if H1_degree % 2 == 0:
                odd_count2 += 1
            else:
                odd_count1 += 1

        if odd_count2 > odd_count1:
            H2, H1 = H1, H2

        M1 = set()
        for node in M_containing_set:
            if H1.degree(node) == 2 * r + e:
                M1.add(node)

        M2 = M_containing_set - M1
        logging.debug(str(M1) + " is M1")
        logging.debug(str(M2) + " is M2")
        while len(M2) != 0:
            logging.debug(str(M2) + " is M2 looping")
            H21, H22 = H2.euler_split(with_graph_copy=True)
            if H21.max_degree('degree') == 0 or H22.max_degree('degree') == 0:
                return H21, H22
            if H21.max_degree('degree') == 1 or H22.max_degree('degree') == 1:
                return H21, H22
            logging.debug("H21 incident " + str(H21.incident))
            logging.debug("H22 incident " + str(H22.incident))
            H21_count = 0
            H22_count = 0

            for node in M2:
                if node in H21.incident and H21.degree(node) == k + d:
                    H21_count += 1
                else:
                    H22_count += 1

            if H22_count > H21_count:
                H22, H21 = H21, H22

            M21 = set()
            for node in M2:
                if node in H21.incident and H21.degree(node) == k + d:
                    M21.add(node)
            M22 = M2 - M21

            logging.debug("M21 is " + str(M21))
            logging.debug("M22 is " + str(M22))

            if k % 2 == 0:
                H1 = (H1.union(H21))
                H2 = H22
            else:
                H1 = H22
                H2 = (H1.union(H21))

            M1 = (M1.union(M21))
            M2 = M22

        return H1, H2
import logging
import random

from timing_util import timing


class VizingColoring:

    def __init__(self, graph, coloring=None, color_counter=None):
        self.graph = graph
        self.coloring = coloring
        self.color_counter = color_counter

    def __call__(self, *args, **kwargs):
        return self.vizing_color(self.graph)

    def vizing_color(self, graph):

        number_of_colors = graph.max_degree('degree')
        coloring = {color: [] for color in range(number_of_colors)}

        edge_coloring_map = {}

        for edge in graph.edges:

            coloring1 = {color: [] for color in range(number_of_colors)}

            if edge in edge_coloring_map:
                continue

            v1 = edge[0]
            v2 = edge[1]

            v1_incident_edges_except_current = list(graph.incident_edges(v1))
            v1_incident_edges_except_current.remove((v1, v2))
            v2_incident_edges_except_current = list(graph.incident_edges(v2))
            v2_incident_edges_except_current.remove((v2, v1))

            allowed_colors_v1 = set(color for color in range(0, number_of_colors))
            allowed_colors_v2 = set(color for color in range(0, number_of_colors))

            for v1_incident_edge in v1_incident_edges_except_current:
                if v1_incident_edge in edge_coloring_map:
                    v1_color_to_prohibit = edge_coloring_map[v1_incident_edge]
                    allowed_colors_v1.remove(v1_color_to_prohibit)

            for v2_incident_edge in v2_incident_edges_except_current:
                if v2_incident_edge in edge_coloring_map:
                    v2_color_to_prohibit = edge_coloring_map[v2_incident_edge]
                    allowed_colors_v2.remove(v2_color_to_prohibit)

            allowed_color_both = allowed_colors_v1.intersection(allowed_colors_v2)

            if len(allowed_color_both) != 0:
                color_to_set = random.choice(list(allowed_color_both))
                edge_coloring_map[(v1, v2)] = color_to_set
                edge_coloring_map[(v2, v1)] = color_to_set
                continue

            color_to_keep_at_v1v2 = random.choice(list(allowed_colors_v1))
            color_to_satisfy_v2 = random.choice(list(allowed_colors_v2))

            edge_coloring_map[(v1, v2)] = color_to_keep_at_v1v2
            edge_coloring_map[(v2, v1)] = color_to_keep_at_v1v2

            cur_v = v2
            next_v = -1
            color_to_set = color_to_satisfy_v2
            color_to_push = color_to_keep_at_v1v2

            for edge_from_v2_incident in v2_incident_edges_except_current:
                if edge_from_v2_incident in edge_coloring_map \
                        and edge_coloring_map[edge_from_v2_incident] == color_to_keep_at_v1v2:
                    next_v = edge_from_v2_incident[1]

            if next_v == -1:
                raise Exception

            found_edge_with_color_to_push = True

            while found_edge_with_color_to_push:
                edge_coloring_map[(cur_v, next_v)] = color_to_set
                edge_coloring_map[(next_v, cur_v)] = color_to_set
                next_v_incident_edges_except_current = list(graph.incident_edges(next_v))
                if (next_v, cur_v) in next_v_incident_edges_except_current:
                    next_v_incident_edges_except_current.remove((next_v, cur_v))
                if (cur_v, next_v) in next_v_incident_edges_except_current:
                    next_v_incident_edges_except_current.remove((cur_v, next_v))

                found_edge_with_color_to_push = False
                for next_v_incident_edge in next_v_incident_edges_except_current:
                    if next_v_incident_edge in edge_coloring_map and edge_coloring_map[next_v_incident_edge] == color_to_set:
                        cur_v = next_v
                        next_v = next_v_incident_edge[1] if next_v_incident_edge[1] != next_v else next_v_incident_edge[0]
                        color_to_set = color_to_keep_at_v1v2 if color_to_set == color_to_satisfy_v2 \
                            else color_to_satisfy_v2
                        color_to_push = color_to_satisfy_v2 if color_to_set == color_to_satisfy_v2 \
                            else color_to_keep_at_v1v2
                        found_edge_with_color_to_push = True

        for edge, color in edge_coloring_map.items():
            coloring[color].append(edge)

        return coloring
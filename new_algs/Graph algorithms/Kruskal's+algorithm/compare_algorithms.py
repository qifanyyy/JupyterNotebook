#!/usr/bin/env python
# -*- coding: utf-8

import sys
sys.path.append('../src')

from utils import generate_graph, calculate_duration, vals_to_str
from prim import prims, prims_fh
from kruskal import kruskal_ts, kruskal_ms
from create_plot import show_plot


NODE_LIST = [2000]
EDGE_LIST = [2000, 4000, 8000, 16000]
MAX_WEIGHT = 10


def generate_times(node_list, edge_list):
    times_prim = list()
    times_kruskal = list()

    for num_node in node_list:
        for num_edge in edge_list:
            print(num_node)
            generated_graph = generate_graph(num_node, num_edge, MAX_WEIGHT)
            graph = generated_graph.graph
            edges = list(generated_graph.get_edges())

            duration1 = calculate_duration(graph, prims, 0)
            duration2 = calculate_duration(graph, kruskal_ms, edges)

            times_prim.append(duration1)
            times_kruskal.append(duration2)

            print("Adding {} n, {} m".format(num_node, num_edge))
            print("\tPrim: ", duration1)
            print("\tKruskal: ", duration2)

    return times_prim, times_kruskal


if __name__ == "__main__":
    edge_str = vals_to_str(EDGE_LIST)
    times_prim, times_kruskal = generate_times(NODE_LIST, EDGE_LIST)
    show_plot(times_prim, times_kruskal, edge_str)

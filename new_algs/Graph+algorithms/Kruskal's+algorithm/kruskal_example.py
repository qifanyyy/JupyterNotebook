#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../src')

from utils import generate_graph, calculate_duration
from kruskal import kruskal_ts, kruskal_ms


# Generating random graph with specific number of nodes and edges

NUM_NODES = 1000
NUM_EDGES = 2000
MAX_WEIGHT = 10


def main():
    generated_graph = generate_graph(NUM_NODES, NUM_EDGES, MAX_WEIGHT)
    graph2 = generated_graph.get_graph()
    edges = list(generated_graph.get_edges())

    duration1 = calculate_duration(graph2, kruskal_ts, edges)
    duration2 = calculate_duration(graph2, kruskal_ms, edges)

    print("Kruskal (Tim Sort):", duration1)
    print("Kruskal (Merge Sort):", duration2)


if __name__ == "__main__":
    main()

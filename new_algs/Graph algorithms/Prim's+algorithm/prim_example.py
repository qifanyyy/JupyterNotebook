#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../src')

from utils import generate_graph, calculate_duration
from prim import prims, prims_fh


# Generating random graph with specific number of nodes and edges

NUM_NODES = 1000
NUM_EDGES = 2000
MAX_WEIGHT = 10
START = 0


def main():
    generated_graph = generate_graph(NUM_NODES, NUM_EDGES, MAX_WEIGHT)
    graph2 = generated_graph.get_graph()

    duration1 = calculate_duration(graph2, prims, START)
    duration2 = calculate_duration(graph2, prims_fh, START)

    print("Prims (Binary Heap): ", duration1)
    print("Prims (Fibonacci Heap): ", duration2)


if __name__ == "__main__":
    main()

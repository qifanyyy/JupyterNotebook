"""Entry point for sequential community scanner"""

import os
import sys
import config as cfg
from inout.parser import parse, get_headers
from algorithms.girvan_newman import girvan_newman_generator
from algorithms.girvan_newman import girvan_newman
from view.visualiser import draw
from time import time

__author__ = "Eduardo Hernandez"
__email__ = "https://www.linkedin.com/in/eduardohernandezj/"


DEFAULT_EDGES_FILE = os.path.join(cfg.BASE_DIR, "sample_files", "girvan_graph.csv")

if __name__ == '__main__':

    edges_path = DEFAULT_EDGES_FILE if len(sys.argv) < 2 else sys.argv[1]

    source_header, target_header, weight_header = get_headers(edges_path)

    # Parse with edges limit:
    graph = parse(edges_path, edge_limit=cfg.EDGES_LIMIT,
                  source_header=source_header, target_header=target_header, weight_header=weight_header)

    number_of_edges = len(list(graph.edges))

    before_time = time()

    components = girvan_newman(graph, cfg.COMPONENTS_LEVEL)

    elapsed_time = time() - before_time

    print('Edges: {0};\t\tTarget Level: {1};\t\t\tSequential Computing Time (seconds): {2}\n\n'.format(
        number_of_edges, cfg.COMPONENTS_LEVEL, elapsed_time
    ))

    print(components)

    if cfg.DRAW:
        draw(graph, components)

    if cfg.DISPLAY_ALL_COMPONENTS:
        for components in girvan_newman_generator(graph):
            print(len(components), components)

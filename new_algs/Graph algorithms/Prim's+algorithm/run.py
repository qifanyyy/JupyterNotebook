#!/usr/bin/env python3

import argparse
import sys

from matplotlib import pyplot as plt

from src.alg.kruskal import kruskal
from src.alg.prim import prim
from src.ds.graph import Graph
from src.viz import show_mst


def main():
    # parse arguments
    args = parse_arguments()

    # load the graph
    try:
        G = Graph.from_file(args.graph)
    except Exception:
        abort("Error reading graph file")

    # run the algorithm
    if args.kruskal:
        mst = kruskal(G)
    elif args.prim:
        mst = prim(G)
    else:
        abort("No algorithm specified")

    # display the result MST edges
    print("The resulting min-spanning-tree contains following edges:")
    for (u, v) in mst:
        print(u, v)

    # plot if asked
    if args.show_graph:
        show_mst(G, mst)
        plt.show()


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=("Find the minimum spanning tree of a connected weighted"
                     "undirected graph"),
        epilog="Author: Manish Munikar <manish.munikar@mavs.uta.edu>")
    parser.add_argument("graph", help="input graph file")
    parser.add_argument(
        "-k", "--kruskal", action="store_true",
        help="use Kruskal's algorithm")
    parser.add_argument(
        "-p", "--prim", action="store_true",
        help="use Prim's algorithm (default)")
    parser.add_argument(
        "-g", "--show-graph", action="store_true",
        help="display the result as a visual graph")

    args = parser.parse_args()

    if args.kruskal and args.prim:
        abort("Please specify only one algorithm")
    if not (args.kruskal or args.prim):
        args.prim = True

    return args


def abort(msg, code=1):
    print(msg, file=sys.stderr)
    sys.exit(code)


if __name__ == "__main__":
    main()

# ChordedCycles.py
# Use python ChordedCycles <number of vertices> <number of chords>
import itertools
import os
import sys

import networkx as nx
from tqdm import *

import DetourMatrix as dm


def main():
    # First argument in the command line gives the number of vertices of the graph
    n = int(sys.argv[1:][0])
    # Second argument gives the number of chords
    ch = int(sys.argv[1:][1])

    # Change Directories to suit your needs
    graphDir = '/graphml_files/'
    wDir = str(os.getcwd()) + graphDir
    wFile = "-color-connected-graph-C_" + str(n) + "_" + str(ch) + "/"
    FileExt = ".graphml"

    # Now we generate the edges that we'll consider
    # The set difference of the edgelists for K_n and C_n
    edgesWeNeed = list(
        set(nx.complete_graph(n).edges()) - set(nx.cycle_graph(n).edges())
    )

    # we want collections of the considered edges, such that no edge
    # is repeated in the sublist
    chords = list(
        itertools.combinations(edgesWeNeed, ch)
    )

    # We'll make a cycle graph just for reference
    g = nx.cycle_graph(n)
    # and we'll find the cycle graphs shortest,longest path
    # see maximum topological distances matrix for details
    cycleLength, p = dm.detour_matrix(g)

    # So that we can use map over the nested lists in chords
    def add_edge_from_tuple(tuple_pair):
        g.add_edge(tuple_pair[0], tuple_pair[1])

    # Variable for indexing output
    q = 0

    # tqdm to keep track of progress
    for i in tqdm(chords):
        # graph instance to be modified
        g = nx.cycle_graph(n)
        # adding the chords to the graph
        for pair in i:
            add_edge_from_tuple(pair)
        # the minimum detour number, or k
        ChordedCycleLength, paths = dm.detour_matrix(g)
        # if ChordedCycleLength is larger than the value k for C_n
        # we write the graph to a graphml format
        if ChordedCycleLength > cycleLength:
            # we'll make the directory for the value k if it doesn't exist
            if not os.path.exists(wDir + str(ChordedCycleLength) + wFile):
                os.makedirs(wDir + str(ChordedCycleLength) + wFile)
            q = q + 1
            file_ext = wDir + str(ChordedCycleLength) + wFile + str(q) + FileExt
            print(file_ext)
            nx.write_graphml(g, file_ext)
        else:
            continue


if __name__ == "__main__":
    main()

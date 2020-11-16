__author__ = 'dstuckey'

# This program solves weighted network shortest path problems using Dijkstra's Algorithm

import networkx as nx
from time import time

approx_infinite_distance = 1000000

def find_shortest_path(graph, source, destination):
    # initialize v as a dictionary
    v = {}
    for node in graph.nodes():
        v[node] = 0 if node==source else approx_infinite_distance

    # initialize permanence dictionary
    perm = {}
    for node in graph.nodes():
        perm[node] = (node==source)

    last_perm = source

    # initialize d as an empty dictionary
    d = {}

    #debugging:
    # print "v: ", v
    # print "perm: ", perm
    # print "d: ", d

    while (not perm[destination]):
        candidate_edges = graph[last_perm]

        # update v and d
        for edge_dest in candidate_edges.keys():
            new_dist = v[last_perm] + candidate_edges[edge_dest]['weight']
            # print edge_dest, " new candidate dist: ", new_dist
            if new_dist < v[edge_dest]:
                # print "new shortest path to ", edge_dest
                v[edge_dest] = new_dist
                d[edge_dest] = last_perm

        # choose next permanent node
        next_perm = None
        next_perm_candidates = [n for n in perm.keys() if not perm[n]]
        # print "next perm candidates: ", next_perm_candidates
        min_dist = approx_infinite_distance
        # print "next perm cands: ", next_perm_candidates
        for cand in next_perm_candidates:
            if v[cand] < min_dist:
                next_perm = cand
                min_dist = v[cand]

        # if no new nodes can be marked permanent, there is no path to destination
        if (next_perm==None):
            raise Exception("No path to destination exists")

        # update last_perm var and permanence dictionary
        perm[next_perm] = True
        last_perm = next_perm
        # print "set as permanent node ", next_perm

    #debugging:
    # print "v: ", v
    # print "perm: ", perm
    # print "d: ", d

    path_length = v[destination]

    # construct the path (in reverse)
    path = [destination]
    last_visited = destination
    while (not (source in path)):
        path.append(d[last_visited])
        last_visited = d[last_visited]
    path.reverse()

    return path_length, path


__author__ = 'dstuckey'

import networkx as nx
from time import time
import dijkstra_impl as di

G = nx.read_weighted_edgelist("DC.txt")

print "num nodes: ", G.number_of_nodes()
print "num edges: ", G.number_of_edges()

print "edges: ", G.edges()

print "degree: ", G.degree()

paths=[]
lengths=[]
times=[]

for pair in [('0','8000'),('12','9000'),('100','8500'),('153','2345'),('224','1000'),('314','567'),('1000','7546'),
             ('0','256'),('10','1257'),('5','6432'),('24','976'),('168','8577')]:
    start = time()
    # shortest = di.find_shortest_path(G, '0','8000')
    shortest = di.find_shortest_path(G, pair[0], pair[1])
    finish = time()

    lengths.append(shortest[0])
    paths.append(shortest[1])
    times.append(finish-start)

    print "source: ", pair[0], "; destination: ", pair[1]
    print "\n\nshortest path length: ", shortest[0]
    print "shortest path: ", shortest[1]
    print "elapsed time: %0.2f s" % (finish - start)

print "lengths: ", lengths
print "paths: ", paths
print "times: ", times
# CSE 101 Winter 2016, PA 2
#
# Graph generator
#
# Be CAREFUL when modifying! Only constants should be tweaked.
#
# The root vertex is always set to be 0

import random
from networkx import *

# Edit these constants to tweak:
#   n:   Number of vertices in the graph (minimum 2).
#   p:   Probability that an edge exists between vertex u and v.
#        p must be in (0.0, 1.0].
#   w:   Max edge weight possible.
#        Edge weights will be randomly selected from [1.0, w].

n = 100
p = 0.5
w = 10

# DO NOT EDIT BELOW, REPEAT: DO NOT EDIT BELOW.

print '\nGenerating graph with n={0}, p={1}, and w={2}\n'.format(n, p, w)

g = fast_gnp_random_graph(n, p)

vertices = range(n)
random.shuffle(vertices)
for i in range(n):
    g.add_edge(vertices[i - 1], vertices[i])

print 'Graph generation complete\n'

filename = 'gen_graphs/{0}_{1}_{2}'.format(p, n, w)

output_file = open(filename, 'w')

print 'Writing out to file: {0}\n'.format(filename)

output_file.write('0\n')

for e in g.edges():
    output_file.write('{0} {1} {2:.4f}\n'.format(e[0], e[1], 1 + (w-1)*random.random()))

output_file.close()

print 'File writing complete\n'

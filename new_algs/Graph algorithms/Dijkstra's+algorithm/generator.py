# Kyle Barron-Kraus <kbarronk>

# The graphs that this generator creates are guaranteed to:
# 1) Be connected
# 2) Have a unique minimum spanning tree.
# 3) Not have duplicate edges.
#
# To generate an infile use the following command:
# python generator.py 5 10 > infile
# 
# The first argument (5 in this case) is the number of vertices that the graph 
# will have, and the second argument (10 in this case) is the maximum number
# of edges that the graph will have. Since most of the edges are generated
# randomly, not all random graphs will have exactly the maximum number of
# edges. max_edges must be >= num_vertices - 1, as this is required to allow
# the graph to be connected.
# 
# Output is in the format specified by PA3 for netplan input files.

import random
import sys

if len(sys.argv) != 3:
    print "Usage:", sys.argv[0], "num_vertices max_edges"
    sys.exit(1)

num_vertices = int(sys.argv[1])
max_edges = int(sys.argv[2])

if num_vertices < 2:
    print "num_vertices must be >= 2"
    sys.exit(1)

if max_edges < num_vertices - 1:
    print "max_edges must be >= num_vertices - 1"
    sys.exit(1)

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

vertices = set()

for x in range(num_vertices):
    while True:
        vertex = ''.join([str(random.choice(letters)) for x in range(5)])
        if vertex not in vertices:
            break
    vertices.add(vertex)

vertices = list(vertices)
edges = set()
weights = [x for x in range(max_edges)]
random.shuffle(weights)

def has_connection(first, second):
    if first + "-" + second in edges:
        return True
    if second + "-" + first in edges:
        return True
    return False

num_edges = 0
def add_connection(first, second):
    global num_edges
    edges.add(first + "-" + second)
    # Using random unique weights guarantees unique MST
    print first, second, weights[num_edges], random.randint(1, 15)
    num_edges += 1

# Make sure the graph is connected
for i in range(len(vertices)-1):
    add_connection(vertices[i], vertices[i+1])

# Add random edges
misses = 0
while num_edges < max_edges and misses < num_vertices:
    vertex1 = random.choice(vertices)
    vertex2 = random.choice(vertices)
     
    if vertex1 == vertex2:
        misses += 1
        continue
    if has_connection(vertex1, vertex2):
        misses += 1
        continue
    
    misses = 0
    add_connection(vertex1, vertex2)

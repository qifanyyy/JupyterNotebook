from math import log
"""
The Bellman-Ford algorithm

Graph API:

    iter(graph) gives all nodes
    iter(graph[u]) gives neighbours of u
    graph[u][v] gives weight of edge (u, v)
"""

# In initialization stage prepare the data structures that will hold 
#   the path lengths from source node to destination 
#   and tracking predecessor nodes
def initialize(graph, source):
    d = {} # will hold your destination lengths for the source node to various nodes
    p = {} # will hold predecessor nodes
    for node in graph:
        d[node] = float('Inf') # Start with an overestimate, we will update this later
        p[node] = None
    d[source] = 0 # Source node to source node = 0
    return d, p

# relaxation is a subprocedure needed for the bellman ford algorithm
def relax(node, neighbor, graph, d, p):
    # If you observe a distance between the node and the neighbor 
    #   is lower than the current recorded one then record this lower distance
    return

# the bellman_ford algorithm can be used to find the shortest path in a graph
# and also can include procedure for detecting negative weight cycles in a graph
def bellman_ford(graph, source):
    d, p = initialize(graph, source)
    
    # TODO: perform relaxation on your graph
    # your code here

    # TODO: check for negative-weight cycles
    # your code here

    return d, p

# normalize makes a normalized copy of a graph
def normalize(arbitrage_g_raw):
    arbitrage_g = {}
    
    # TODO: here you may need to normalize the weighted edge values of a graph
    # your code here

    return arbitrage_g

def test():
    graph = {
        'a': {'b': -1, 'c':  4},
        'b': {'c':  3, 'd':  -2, 'e':  2},
        'c': {},
        'd': {'b':  1, 'c':  5},
        'e': {'d': -3}
        }

    currency_raw1 = {
        'a': {'b': 0.8185, 'c': 1.2344, 'd': 1.3564, 'e': 1.5318 },
        'b': {'a': 1.2217, 'c': 1.5083, 'd': 1.6573, 'e': 1.8716 },
        'c': {'a': 0.8101, 'b': 0.6630, 'd': 1.0988, 'e': 1.2409 },
        'd': {'a': 0.7372, 'b': 0.6034, 'c': 0.9101, 'e': 1.1293 },
        'e': {'a': 0.6528, 'b': 0.5343, 'c': 0.8059, 'd': 0.8855 }
    }
    currency1 = normalize(currency_raw1)

    currency_raw2 = {
        'a': {'b': 0.8185, 'c': 1.2344, 'd': 1.3564, 'e': 0.09318 },
        'b': {'a': 1.2217, 'c': 1.5083, 'd': 1.6573, 'e': 1.8716 },
        'c': {'a': 0.8101, 'b': 0.6630, 'd': 1.0988, 'e': 1.2409 },
        'd': {'a': 0.7372, 'b': 0.6034, 'c': 0.9101, 'e': 1.1293 },
        'e': {'a': 0.6528, 'b': 0.5343, 'c': 0.8059, 'd': 0.8855 }
    }
    currency2 = normalize(currency_raw2)

    src_node = 'a' # here you can set a source_node

    d, p = bellman_ford(graph, src_node)
    print "src node: " + src_node
    print p

if __name__ == '__main__': test()

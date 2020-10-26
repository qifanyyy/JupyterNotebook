from math import log
"""
The Bellman-Ford algorithm

Graph API:

    iter(graph) gives all nodes
    iter(graph[u]) gives neighbours of u
    graph[u][v] gives weight of edge (u, v)
"""

# Step 1: For each node prepare the destination and predecessor
def initialize(graph, source):
    d = {} # should hold your destination lengths for various nodes
    p = {} # Stands for predecessor
    for node in graph:
        d[node] = float('Inf') # We start admiting that the rest of nodes are very very far
        p[node] = None
    d[source] = 0 # For the source we know how to reach
    return d, p

def relax(node, neighbor, graph, d, p):
    # If the distance between the node and the neighbor is lower than the one I have now
    if d[neighbor] > d[node] + graph[node][neighbor]:
        # Record this lower distance
        d[neighbor]  = d[node] + graph[node][neighbor]
        p[neighbor] = node

def bellman_ford(graph, source):
    d, p = initialize(graph, source)
    for i in range(len(graph)-1): #Run this until is converges
        for u in graph:
            for v in graph[u]: #For each neighbor of u
                relax(u, v, graph, d, p) #Lets relax it

    # Step 3: check for negative-weight cycles
    for u in graph:
        for v in graph[u]:
            if d[v] <= d[u] + graph[u][v]:
                #find that negative cycle and return it
                #print "found neg cycle u,v: " + u + " " + v
                return d, p

    print "No Arbitrage Opp found"
    return d, p

# we need to convert currency ratios by taking their negative log
def normalize(arbitrage_g_raw):
    arbitrage_g = {}
    for k, neighbors in arbitrage_g_raw.iteritems():
        arbitrage_g[k] = {}
        for m, weights in neighbors.iteritems():
            arbitrage_g[k][m] = (-1) * log(weights)
    return arbitrage_g

def test():
    graph = {
        'a': {'b': -1, 'c':  4},
        'b': {'c':  3, 'd':  -2, 'e':  2},
        'c': {},
        'd': {'b':  1, 'c':  5},
        'e': {'d': -3}
        }

    currency_g_raw = {
        'a': {'b': 0.8185, 'c': 1.2344, 'd': 1.3564, 'e': 1.5318 },
        'b': {'a': 1.2217, 'c': 1.5083, 'd': 1.6573, 'e': 1.8716 },
        'c': {'a': 0.8101, 'b': 0.6630, 'd': 1.0988, 'e': 1.2409 },
        'd': {'a': 0.7372, 'b': 0.6034, 'c': 0.9101, 'e': 1.1293 },
        'e': {'a': 0.6528, 'b': 0.5343, 'c': 0.8059, 'd': 0.8855 }
    }
    currency_g = normalize(currency_g_raw)

    arbitrage_g_raw = {
        'a': {'b': 0.8185, 'c': 1.2344, 'd': 1.3564, 'e': 0.09318 },
        'b': {'a': 1.2217, 'c': 1.5083, 'd': 1.6573, 'e': 1.8716 },
        'c': {'a': 0.8101, 'b': 0.6630, 'd': 1.0988, 'e': 1.2409 },
        'd': {'a': 0.7372, 'b': 0.6034, 'c': 0.9101, 'e': 1.1293 },
        'e': {'a': 0.6528, 'b': 0.5343, 'c': 0.8059, 'd': 0.8855 }
    }
    arbitrage_g = normalize(arbitrage_g_raw)



    #d, p = bellman_ford(graph, 'a')
    alphabet = ['a', 'b', 'c', 'd', 'e']
    for src_node in alphabet:
        is_arbitrage = False
        d, p = bellman_ford(arbitrage_g, src_node)
        print "src node: " + src_node
        print p
        #for n, pred in enumerate(p):
        #    if pred == src_node:
        #        is_arbitrage = True
        #        print "FOUND for " + src_node
        #        print p
        #if not is_arbitrage:
        #    print "NO ARB for " + src_node

    #assert d == {
    #    'a':  0,
    #    'b': -1,
    #    'c':  2,
    #    'd': -2,
    #    'e':  1
    #    }

    #assert p == {
    #    'a': None,
    #    'b': 'a',
    #    'c': 'b',
    #    'd': 'e',
    #    'e': 'b'
    #    }

if __name__ == '__main__': test()

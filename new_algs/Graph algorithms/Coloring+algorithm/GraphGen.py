

import random
from time import time
import argparse


from Graph import Graph
import IOHandling


def genEdges(n, d):
    """
    Generate edges for graph

    :param n: Vertex count in the graph
    :param d: Density - ratio of number of edges in the graph to the number of edges in a N complete graph

    :return: List of edges represented as tuples
    """

    edgeCountComplete = int(n*(n-1)/2)
    edgeCountToGenerate = int(edgeCountComplete * d)

    return random.sample([(str(i), str(j),) for i in range(n-1) for j in range(i+1, n)], edgeCountToGenerate)


def genGraph(n=0, d=0.0, k=0, p=None, seed=None):
    """
    Generate graph random graph based on parameters
    Function guaranties that the chromatic number
    of the returned graph won't be greater than k

    :param n: Vertex count in the graph
    :param d: Graph's density
    :param k: Create k-divisible graph if k>0
    :param p: Partitioning of k-divisible graph
    :param seed: For test purposes
    :return: Generated graph
    """

    if not k:
        k = n
    if seed is None:
        seed = time()

    g = Graph()
    rand = random.Random(seed)

    # If vertex count is 0 just return empty graph
    if n == 0:
        return g

    for v in range(n):
        g.addVertex(str(v))
    # g.addVertices(range(n))

    # If there are no edges to generate return graph
    if d == 0.0:
        return g

    # Impossible to divide graph more than in n partitions
    if k > n:
        return None

    if k == 0 or k == n:
        edgeCountComplete = int(n * (n - 1) / 2)
        edgeCountToGenerate = int(edgeCountComplete * d)

        rand.seed(seed)
        g.addEdges(rand.sample([(str(i), str(j),) for i in range(n - 1)
                                  for j in range(i + 1, n)], edgeCountToGenerate))
        return g

    # Generate partitioning and calculate total amount of edges
    edgeCountComplete = 0
    if p is None and k > 0:
        p = []
        c = n
        keys = list(g.getAdjDict())
        rand.shuffle(keys)
        for i in range(k, 0, -1):
            var = c//i
            group = keys[:var]
            p.append(group)
            keys = keys[var:]
            c -= var
            edgeCountComplete += len(group) * c

    edgeCountToGenerate = int(edgeCountComplete * d)

    rand.seed(seed)
    g.addEdges(rand.sample([(str(l), str(n),) for i in range(len(p)-1)
                              for j in range(i+1, len(p)) for l in p[i] for n in p[j]], edgeCountToGenerate))
    return g


if __name__ == '__main__':
    """
    Dump json-formatted generated graph to stdout
    """

    parser = argparse.ArgumentParser(prog='GraphGen.py', description='Random graph generator')
    parser.add_argument('-n', type=int, metavar='', help='Number of vertices')
    parser.add_argument('-d', default=0.0, type=float, metavar='', help='Density of the graph')
    parser.add_argument('-k', default=0, type=int, metavar='', help='Divisibility of the graph')
    parser.add_argument('-p', default=None, type=list,
                        metavar='', help='Partitioning of the graph in case k>0')
    parser.add_argument('-s', '--seed', default=time(), type=float,
                        metavar='', help='Seed used by random functions while generating a graph')

    # Parsing arguments
    args = vars(parser.parse_args())
    if not args['n']:
        parser.print_help()
        exit(1)

    n = args['n']
    d = args['d']
    k = args['k']
    p = args['p']
    s = args['seed']
    g = genGraph(n, d, k, p, s)

    IOHandling.dumpGraph(g)

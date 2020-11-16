"""Module for creating graphs of different families."""

import itertools
import random

import networkx as nx


def create_kneser_graph(m):
    r = m / 2
    t = m / 8

    vertices = [combination for combination in itertools.combinations(range(m), r)]
    edges = []
    for i in range(len(vertices)):
        for j in range(len(vertices)):
            if i < j and len(set(vertices[i]) & set(vertices[j])) < t:
                edges.append((vertices[i], vertices[j]))

    graph = nx.Graph()
    graph.add_nodes_from(vertices)
    graph.add_edges_from(edges)

    graph.name = 'Kneser graph {0}'.format(m)

    return graph


def create_k_colorable_graph(k, n, p, cluster_by_modulo=False):
    """Creates k-colorable graph with color classes of the same cardinality.

    If p < 1 then chromatic number may be less than k.

    Args:
        k (int): Number of vertex clusters.
        n (int): Number of vertices in each cluster.
        p (float): Probability of edge creation between vertices in different clusters.
        cluster_by_modulo (bool): Each cluster contains vertices with the same remainder modulo k
    """

    vertices = list(range(k * n))
    vertex_cluster = {}

    for v in vertices:
        vertex_cluster[v] = random.choice([c for c in range(k)])

    if cluster_by_modulo:
        for v in vertices:
            vertex_cluster[v] = v % k

    edges = []
    for i in vertices:
        for j in vertices:
            if i > j and vertex_cluster[i] != vertex_cluster[j]:
                if random.random() < p:
                    edges.append((i, j))

    graph = nx.Graph()
    graph.add_nodes_from(vertices)
    graph.add_edges_from(edges)

    graph.name = 'graph with {0}v in {1} clusters and {2} edge prob'.format(n, k, p)
    graph.family = 'k-colorable'
    graph.starting_index = 0

    return graph


def create_k_cycle(k, n):
    """Creates graph that is hard to color for dsatur.

    Args:
        k (int): Distance to the farthest neighbor of each vertex.
        n (int): Number of vertices.
    """

    vertices = [i for i in range(n)]
    edges = []
    for i in vertices:
        for j in vertices:
            if 0 < ((i - j) % n) <= k:
                edges.append((i, j))

    graph = nx.Graph()
    graph.add_nodes_from(vertices)
    graph.add_edges_from(edges)

    graph.name = '{0}-cycle {1}v'.format(k, n)
    graph.family = 'k-cycle'
    graph.starting_index = 0

    return graph


def create_crown_graph(n):
    vertices = [i for i in range(2 * n)]
    edges = []
    for i in range(n):
        for j in range(n, 2 * n):
            if abs(i - j) != n:
                edges.append((i, j))

    graph = nx.Graph()
    graph.add_nodes_from(vertices)
    graph.add_edges_from(edges)

    graph.name = 'crown graph {0}n'.format(n)
    return graph


def create_erdos_renyi_graph(n, p, name_suffix=""):
    """Creates random graph of type networkx.erdos_renyi_graph."""

    graph = nx.erdos_renyi_graph(n, p)
    graph.name = 'erdos_renyi_{0}n_{1}p'.format(n, p) + '_' + name_suffix
    graph.family = 'erdos_renyi'
    graph.starting_index = 0

    return graph


def create_watts_strogatz_graph(n, k, p, name_suffix=""):
    """Creates random graph of type nx.connected_watts_strogatz_graph.

    Args:
        n (int): the number of nodes
        k (int): each node is joined with k nearest neighbors in a ring topology
        p (float): the probability of rewiring each edge
    """

    graph = nx.connected_watts_strogatz_graph(n, k, p)
    graph.name = 'watts_strogatz_{0}n_{1}k_{2}p'.format(n, k, p) + '_' + name_suffix
    graph.family = 'watts_strogatz'
    graph.starting_index = 0

    return graph


def create_barabasi_albert_graph(n, m, name_suffix=""):
    """Creates random graph of type networkx.dense_gnm_random_graph.
    Args:
        n (int): number of nodes
        m (int): number of edges to attach from a new node to existing nodes
    """

    graph = nx.dense_gnm_random_graph(n, m)
    graph.name = 'barabasi_albert_{0}n_{1}m'.format(n, m) + '_' + name_suffix
    graph.family = 'barabasi_albert'
    graph.starting_index = 0

    return graph


def create_set_of_random_graphs(
        min_vertices=20,
        max_vertices=40,
        iterations_per_vertex_number=2):
    """Creates set of random graphs.

    Returns:
        list: List of Graph instances."""

    graphs = []
    for n in range(min_vertices, max_vertices):
        max_m = (n * (n - 1)) / 2
        density = [0.5 * max_m]
        for m in density:
            for iters in range(iterations_per_vertex_number):
                graphs.append(create_erdos_renyi_graph(n, m))

    return graphs

import copy

import networkx as nx

from src.graph import Graph


def create_graph_from_txt_file(txt_file: str):
    nodes = []
    with open(txt_file) as file:
        line = file.readline()
        while line:
            if "#" not in line:
                n_info = line.replace("\n", "").split(",")
                nodes.append((n_info[0], n_info[1], n_info[2]))

            line = file.readline()

    if len(nodes) > 0:
        g = Graph()
        g.add_node_list(nodes)
        return g

    raise Exception("Wrong input file provided")


def get_mst(graph: Graph):
    # Kruskal's algorithm
    edges = graph.get_edges()
    weighted_edges = {}
    for (u, v) in edges:
        weighted_edges[(u, v)] = int(graph.get_edge_weight(u, v))

    # sort edges by weight, by value
    weighted_edges = sorted(weighted_edges.items(), key=lambda x: x[1])

    mst_graph = Graph()
    nodes = []
    for itm in weighted_edges:
        u, v = itm[0]
        mst_graph.add_edge(u, v, graph.get_edge_weight(u, v))
        try:
             nx.algorithms.find_cycle(mst_graph.get_graph())
             mst_graph.get_graph().remove_edge(u, v)
        except nx.NetworkXNoCycle:
            nodes.append(u)
            nodes.append(v)

    return mst_graph


def get_degrees(graph: Graph):
    degrees = {}

    for d in graph.get_degree():
        degrees[d[0]] = d[1]

    return degrees


def get_nodes_odd_degrees(degrees: dict):
    odd_degrees = {}

    for k in degrees.keys():
        if (degrees[k]%2) !=0:
            odd_degrees[k] = degrees[k]

    return odd_degrees


def print_edges_with_weight(graph: Graph):
    if isinstance(graph.get_graph(), nx.MultiGraph):
        for e in graph.get_edges():
            print(f"Edge : ({e[0]},{e[1]})")
    else:
        for e in graph.get_edges():
            print(f"Edge : ({e[0]},{e[1]}) = {graph.get_edge_weight(e[0], e[1])}")


def convert_edges_tuples_to_dict(nodes, edges_tuples):
    edges = {}

    # add all nodes as keys
    for n in nodes:
        edges[n] = []

    for e in edges_tuples:
        edges[e[0]].append((e[1]))
        edges[e[1]].append((e[0]))

    return edges


def create_subgraph(graph: Graph, nodes_to_include):
    subgraph = nx.Graph(graph.get_graph().subgraph(nodes_to_include))
    return Graph(subgraph)


def create_minimum_weight_perfect_matching(graph: Graph):
    # create new graph with negative weight
    new_graph = Graph()
    for e in graph.get_edges():
        new_graph.add_edge(e[0], e[1], -int((graph.get_edge_weight(e[0], e[1]))))

    set_matching = nx.max_weight_matching(new_graph.get_graph(), maxcardinality=True)

    matching_graph = Graph()
    for m in set_matching:
        matching_graph.add_edge(m[0], m[1], graph.get_edge_weight(m[0], m[1]))

    return matching_graph


def union_graphs(graph1: Graph, graph2: Graph):

    multi_graph = Graph(multi_graph=True)
    for e in graph1.get_edges():
        multi_graph.add_edge(e[0], e[1])

    for e in graph2.get_edges():
        multi_graph.add_edge(e[0], e[1])

    return multi_graph


def get_total_cost(graph, path):
    weight = 0
    for i in range(1, len(path)):
        weight += int(graph.get_edge_weight(path[i-1], path[i]))
    return weight

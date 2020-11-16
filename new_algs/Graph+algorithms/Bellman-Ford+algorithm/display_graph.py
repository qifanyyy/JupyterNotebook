"""Ad hoc tool to draw some algorithms results on an original input graph."""

import networkx as nx
import matplotlib.pyplot as plt


def display_graph(graph, edges_to_color=()):
    """Colors specific edges of a given graph,
    according to edges listed in edges_to_color parameter.

    :param graph: Adjacency list representation of a graph.
        graph_example = {
                        'a': {'b': 4},
                        'b': {'a': 4, 'c': 8},
                        'c': {'b': 8}
                        }
    :param edges_to_color: Example: [('a', 'b'), ('a', 'c')}
    """

    # Create a set of edges as a reference for changing a color of a tree.
    colored = set()
    for i in edges_to_color:
        colored.add(i)
        colored.add(i[::-1])

    # Create graph with distance and color attributes.
    g = nx.Graph()
    for tail in graph:
        for head, dist in graph[tail].items():
            color = 'red' if (tail, head) in colored or \
                             (head, tail) in colored else '#f8f8f8'
            g.add_edge(tail, head, distance=dist, color=color)

    labels = nx.get_edge_attributes(g, 'distance')
    colors = nx.get_edge_attributes(g, 'color')  # get dict {edge: color}
    pos = nx.spring_layout(g)  # set points positions

    # Draw g graph.
    nx.draw(g, pos=pos, with_labels=True, width=1.7,
            edgelist=colors.keys(), edge_color=colors.values())
    nx.draw_networkx_edge_labels(g, pos=pos, edge_labels=labels)  # draw distances as labels
    plt.show()

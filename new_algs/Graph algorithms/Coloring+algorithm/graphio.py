import networkx as nx
import matplotlib.pyplot as plt


def read_edges(path='input.txt'):
    with open(path) as inputs:
        edges = [tuple(i.strip().split()) for i in inputs.readlines()]
    return edges


def write_edges(path='output.txt'):
    pass


def show(edges, node_color, message='Colored graph', with_labels=True):
    g = nx.Graph()
    g.add_edges_from(edges)
    pos = nx.spring_layout(g)
    for node, color in node_color.items():
        nx.draw(g, pos, nodelist=[node], node_color=color, with_labels=with_labels)
    plt.gcf().canvas.set_window_title(message)
    plt.show()

"""
Functions to visualize graphs and minimum spanning tree.
"""

import networkx as nx
from matplotlib import pyplot as plt


def show_graph(G, size=15):
    """
    Draws the graph in a matplotlib figure and returns the figure.

    Args:
        G:      The graph object
        size:   Size of plot
    """
    # initialize a figure canvas
    fig = plt.figure(figsize=[size, size])

    # convert to networkx graph (to use networkx visualization features)
    G = G.to_nx()

    # find the vertex positions
    pos = nx.spring_layout(G)

    # draw the nodes and labels
    nx.draw_networkx_nodes(
        G, pos, node_color="b", node_size=400, linewidths=1, edgecolors="black")
    nx.draw_networkx_labels(G, pos, font_color="white", font_weight="bold")

    # draw the edges in a faint color
    nx.draw_networkx_edges(G, pos, edge_color="#ccc", style="solid")

    # also draw edge labels if available
    try:
        edge_labels = {(a, b): int(d["weight"])
                       for a, b, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    except KeyError:
        pass

    return fig


def show_mst(G, mst, size=15):
    """
    Draws the graph in a matplotlib figure and returns the figure.

    Args:
        G:      The graph object
        mst:    List of minimum spanning tree edges
        size:   Size of plot
    """
    # initialize a figure canvas
    fig = plt.figure(figsize=[size, size])

    # convert to networkx graph (to use networkx visualization features)
    G = G.to_nx()

    # find the vertex positions
    pos = nx.spring_layout(G)

    # draw the nodes and labels
    nx.draw_networkx_nodes(
        G, pos, node_color="b", node_size=400, linewidths=1, edgecolors="black")
    nx.draw_networkx_labels(G, pos, font_color="white", font_weight="bold")

    # draw the edges in a faint color
    nx.draw_networkx_edges(G, pos, edge_color="#ccc", style="solid")

    # draw the min-spanning-tree edges in red bold color
    nx.draw_networkx_edges(
        G, pos, edge_color="red", style="solid", edgelist=mst, width=3
    )

    # also draw edge labels if available
    try:
        edge_labels = {(a, b): int(d["weight"])
                       for a, b, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    except KeyError:
        pass

    return fig

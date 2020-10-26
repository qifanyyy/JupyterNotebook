"""Module for loading, saving and displaying graphs."""

import logging
import os

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pylab

import config


def read_graph_from_file(folder_name, graph_name, graph_type=None, starting_index=0, fullpath=None):
    """Creates graph from DIMACS-format file.

    Args:
        graph_name (str): Name of the file to read, without directory and extension.
        starting_index (int): Index of first vertex.

    Returns:
        Graph: networkx.Graph object created from given file with nodes indexed from 0.
    """

    graph = nx.Graph()

    if fullpath is not None:
        filename = fullpath
    else:
        filename = 'graph_instances/' + folder_name + '/' + graph_name + '.col'

    with open(filename) as f:
        for line in f:
            l = line.split()
            if l[0] == 'p':
                nr_of_nodes = int(l[2])
                graph.add_nodes_from(range(starting_index, starting_index + nr_of_nodes))
            elif l[0] == 'e':
                try:
                    e1 = int(l[1])
                    e2 = int(l[2])
                    graph.add_edge(e1, e2)
                except ValueError:
                    graph.add_edge(l[1], l[2])

    # G = nx.relabel_nodes(G, lambda x: x - 1, copy=False)
    graph.name = graph_name
    graph.family = graph.name
    graph.starting_index = starting_index
    graph.type = graph_type

    return graph


def draw_graph(graph, colors, toConsole=True, toImage=False, filename='graph'):
    """Draws graph and saves image to file.

    Args:
        graph (Graph): Graph to be drawn.
        colors (dict): Global vertex-color dictionary.
        filename (str): File to save.
    """

    output_dir = config.drawings_directory()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # for v in colors.keys():
    # colors[v] = list(set(colors.values())).index(colors[v])

    if colors:
        colors_list = [v for k, v in sorted(colors.items())]
        # print 'colors list:', colors_list
        # print 'colors set:', set(colors_list)
        print 'number of colors used:', len(set(colors_list))
        # print 'bin colors: ', [bin(colors[v]) for v in range(0, G.number_of_nodes() + 0)]
    else:
        colors_list = [1] * graph.number_of_nodes()

    if toConsole:
        print 'name:', graph.name
        print 'number of nodes:', graph.number_of_nodes()
        print 'number of edges:', graph.number_of_edges()
        # print 'edges:', G.edges()

    if toImage:
        node_labels = {v: str(v + 0) for v in range(graph.number_of_nodes())}
        logging.getLogger("matplotlib.backends._backend_tk").setLevel(logging.CRITICAL)
        fig = pylab.figure(figsize=(10, 7))
        # thismanager = matplotlib.pyplot.get_current_fig_manager()
        # img = BitmapImage(file='favicon.bmp')
        # thismanager.window.tk.call('wm', 'iconphoto', thismanager.window._w, img)

        nx.draw(graph, pos=nx.circular_layout(graph), with_labels=True, node_color=colors_list, cmap=plt.cm.Spectral,
                labels=node_labels)

        # hide axis
        fig.gca().axes.get_xaxis().set_ticks([])
        fig.gca().axes.get_yaxis().set_ticks([])

        pylab.savefig('{0}/{1}.png'.format(output_dir, filename), format="PNG")
        pylab.show()


def display_graph_stats(graph):
    """Displays some graphs stats.

    Args:
        graph (Graph): Graph to display.
    """

    degrees = dict(graph.degree()).values()
    n = graph.number_of_nodes()
    max_degree = max(degrees)
    min_degree = min(degrees)
    avg_degree = np.average(degrees)

    print ' current graph stats:'
    print '     number of vertices:', n
    print '     max degree:', max_degree
    print '     avg degree:', avg_degree
    print '     min degree:', min_degree
    print '     number of edges:', graph.number_of_edges()
    print '     edge density:', float(graph.number_of_edges()) / float((n * (n - 1) / 2))


def save_graph_to_col_file(graph):
    filename = 'graph_instances/generated/' + graph.name + '.col'

    with open(filename, 'w') as outfile:
        for e1, e2 in graph.edges():
            outfile.write("e {0} {1}\n".format(e1, e2))

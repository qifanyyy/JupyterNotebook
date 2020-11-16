import matplotlib.pyplot as plt
import networkx as nx
import pdb
from colors import *

PAUSE_TIME = 0.5

def convertToNX(graph):
    G = nx.Graph()
    G.add_nodes_from(graph.getVertices())
    for node in graph.getVertices():
        for neighbor in node.neighbors:
            G.add_edge(node, neighbor)

    return G

def plotGraph(graph, iter_num):
    G = convertToNX(graph)
    cols = [x.color for x in graph.getVertices()]
    cols = [plotColorsDict[color] for color in cols]
    nx.draw_networkx(G, node_color = cols)

    plt.draw()
    plt.pause(PAUSE_TIME)
    plt.clf()

    return

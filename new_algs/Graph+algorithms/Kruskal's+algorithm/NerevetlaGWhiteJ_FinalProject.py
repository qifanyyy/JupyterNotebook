'''
This program will take the number of nodes and the algorithm to use as arguments, and generates a picture
demonstrating the algorithm working its magic creating a Minimum Spanning Tree!
'''

import random
import sys
import time
import networkx as nx
import matplotlib.pyplot as plt
from networkx.utils import UnionFind

#returns the smallest edge that is not in the subgraph but connects to the node out side the subgraph
def minDistance(G, subG):
    min_key = sys.maxsize
    for edge in G.edges(subG.nodes()):
        if edge[1] not in subG.nodes() and G[edge[0]][edge[1]]['weight'] < min_key:
                min_key = G[edge[0]][edge[1]]['weight']
                min_edge = [edge[0], edge[1], min_key]
    return min_edge

#Accepts the graph and the position and returns the MST generated using prim's algorithm.
def prim(G, pos):
    subG = G.subgraph(0).copy()
    for i in range(1, G.number_of_nodes()):
        edge = minDistance(G, subG)
        subG.add_edge(edge[0], edge[1], weight=edge[2], color='g')
        drawGraph(G, pos, subG)
        plt.show()
        #time.sleep(.5)
    drawGraph(subG, pos, subG)
    plt.show()
    return subG

#takes in graph and position, then generates the MST using Kruskal's algorithm.
def kruskal(G, pos):
    subG = nx.empty_graph()
    subsets = UnionFind()
    edgelist = []
    for edge in G.edges:
        edgelist.append([edge[0], edge[1], G[edge[0]][edge[1]]['weight']])
    edgelist.sort(key=lambda x: x[2])
    i = 0
    for edge in edgelist:
        edge = edgelist[i]
        if subsets[edge[0]] != subsets[edge[1]]:
            subsets.union(edge[0], edge[1])
            subG.add_edge(edge[0], edge[1], weight=edge[2], color='g')
            drawGraph(G, pos, subG)
            plt.show()
            #time.sleep(.5)
        i += 1
    drawGraph(subG, pos, subG)
    plt.show()
    return subG

#Generates graph images
def drawGraph(G, pos, subG=nx.empty_graph()):
    edges = G.edges()
    color_map = []
    for i in G.nodes():
        if i not in subG:
            color_map.append('r')
        else:
            color_map.append('g')
    edge_colors = []
    for edge in edges:
        if edge not in subG.edges():
            edge_colors.append(G[edge[0]][edge[1]]['color'])
        else:
            edge_colors.append(subG[edge[0]][edge[1]]['color'])
    nx.draw(G, pos, edges=edges, with_labels=True, node_size=80, node_color=color_map, edge_color=edge_colors, font_size=8)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=5)
    return pos


n = int(sys.argv[1])
algo = sys.argv[2]
#Generates randoms graph.
if n > 4:
    G = nx.random_regular_graph(4, n, seed=None)
elif n > 1:
    G = nx.random_regular_graph(1, n, seed=None)
elif n == 1:
    G = nx.empty_graph()
    G.add_node(0)
else:
    print("Number of nodes is less than 1")

#colors pre MST edges
for (u, v) in G.edges():
    G[u][v]['weight'] = random.randint(1, n)
    G[u][v]['color'] = 'r'
pos = nx.spring_layout(G, k=0.80, iterations=100)
drawGraph(G, pos)
plt.show()

if algo == "prim":
    v = prim(G, pos)
elif algo == "kruskal":
    v = kruskal(G, pos)
elif algo == "both":
    v = prim(G, pos)
    v = kruskal(G, pos)
else:
    print("Invalid input")

#!/usr/bin/python
# -*- coding: utf-8 -*-
#
"""
Graph coloring

@author: Henrique Moura
@change: April 04, 2017


@requires: networkx
"""
from __future__ import print_function
import networkx as nx
import sys

__ALL__ = ['read_graph', 'color_graph']

sys.setrecursionlimit(5000)  # this value depends on the size of the graph, beacuse coloring is recursive


def assign_colors(index_k, graph, colors):
    amnt_vertex = len(graph)
    vertices = graph.nodes()
    while True:
        index_a = colors[index_k] + 1
        colors[index_k] = index_a % (amnt_vertex + 1)
        if colors[index_k] == 0:
            ''' acabaram as cores '''
            return
        node1 = vertices[index_k - 1]
        j = 0
        for j in range(amnt_vertex):
            node2 = vertices[j]
            if graph.has_edge(node1, node2) and colors[index_k] == colors[j + 1]:
                break
        if j == amnt_vertex - 1:
            return


def coloring(index_k, graph, colors):
    ''' algoritmo de coloracao exata
        ref.: puntambekar
    '''
    assign_colors(index_k, graph, colors)
    if colors[index_k] == 0:
        return
    if index_k == len(graph):
        '''cada vertice recebeu uma cor diferente'''
        return
    else:
        coloring(index_k + 1, graph, colors)


def color_graph(graph):
    colors = [0 for i in range(len(G) + 1)]
    coloring(index_k=1, graph=G, colors=colors)
    colors.remove(0)  # colors[0] is not used
    vertices = graph.nodes()
    d = {}
    for i in range(len(vertices)):
        d[vertices[i]] = colors[i] - 1
    return d


def read_graph(clq_file):
    G = nx.Graph()
    with open(clq_file, 'r') as f:
        for line in f:
            line = line.split()
            if len(line) == 2:
                G.add_edge(int(line[0]), int(line[1]))
            else:
                if line[0] == 'e':
                    G.add_edge(int(line[1]), int(line[2]))
    return G


if __name__ == "__main__":
    '''
     testando com este grafo
      1----2
      |\   |
      |  \ |
      |   \|
      3----4
    '''

    G = nx.Graph()
    G.add_edge(1, 2)
    G.add_edge(1, 3)
    G.add_edge(1, 4)
    G.add_edge(2, 4)
    G.add_edge(3, 4)

    '''
     ref. https://networkx.github.io/documentation/development/reference/generated/networkx.algorithms.coloring.greedy_color.html#networkx.algorithms.coloring.greedy_color

     strategy_saturation_largest_first==> DSATUR
    '''
    d = nx.coloring.greedy_color(G, strategy=nx.coloring.strategy_saturation_largest_first)
    print("Usando nx.coloring")
    print(d)

    d = color_graph(graph=G)
    print("Usando algoritmo exato")
    print(d)
    print("cores necessarias = ", list(set(d.values())))

    print("\nacrescentando aresta entre 2 e 3")
    G.add_edge(2, 3)

    d = nx.coloring.greedy_color(G, strategy=nx.coloring.strategy_saturation_largest_first)
    print("Usando nx.coloring")
    print(d)

    print("Usando algoritmo exato")
    d = color_graph(graph=G)
    print(d)
    print("cores necessarias = ", list(set(d.values())))

    from os import listdir
    from os.path import isfile, join

    mypath = './benchmark/clq/'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.split('.')[-1] == 'clq']
    for f in sorted(onlyfiles):
        print('lendo', f)
        G = read_graph(join(mypath, f))
        print('processando', f, 'nodes =', len(G))
        d = color_graph(graph=G)
        print(d)
        cores = list(set(d.values()))
        print("cores necessarias = ", cores)
        print("num cores necessarias = ", max(cores))

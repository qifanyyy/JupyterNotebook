import networkx as nx
import subprocess
import sys
import matplotlib.pyplot as plt

# AUTHOR: Luis Enrique Neri Pérez
# Copyright 2019

# This is an implementation of the Breath First Algorithm


Q = []
A = []
nodes = {}


def install():
    if 'networkx' not in sys.modules:
        subprocess.call([sys.executable, "-m", "pip", "install", 'networkx'])
    if 'matplotlib' not in sys.modules:
        subprocess.call([sys.executable, "-m", "pip", "install", 'matplotlib'])


def createGraph():
    g = nx.DiGraph();
    for k in nodes:
        g.add_node(k)
    listaEdges = [];
    for k in nodes:
        for elemento in nodes[k]:
            listaEdges.append((k, elemento));
    g.add_edges_from(listaEdges);
    color_map = [];
    for nodo in g:
        if nodo in Q:
            color_map.append('yellow')
        elif nodo in A:
            color_map.append('blue');
        else:
            color_map.append('green');

    nx.draw(g, node_color=color_map, with_labels=True);
    plt.show();


def processInput():
    print("\nWrite the list of every node and its edge with the format (V,E):")
    print(
        "Ex. (1,2), (1,3), (1,4), (2,5), (2,6), (2,3), (3,7), (3,8), (4,8), (5,2), (6,2), (7,3), (7,9), (8,3), (8,4), (9,7)")
    edges = input("\nNodes: ")
    saving = False
    for i in range(0, len(edges) - 1):
        if edges[i] == '(':
            saving = True;
            continue

        elif edges[i] == ')':
            saving = False
            continue

        elif saving:
            pair = edges[i:i + 3]
            if (int(pair[0]) not in nodes.keys()):
                lista = []
                lista.append(int(pair[2]))
                nodes[int(pair[0])] = lista
            else:
                key = int(pair[0])
                listaAct = nodes.get(key)
                listaAct.append(int(pair[2]))
                nodes.update({int(pair[0]): listaAct})

            saving = False
        else:
            continue
    print(nodes)


def bfs():
    # Initial condition
    print("\nInitial Condition")
    Q.insert(0, 1)
    A.append(1)
    print("Q: ", Q, " - YELLOW")
    print("A: ", A, " - BLUE\n")
    createGraph()
    for i in range(1, len(nodes) + 1):
        print("Iteration ", i)
        key = Q.pop()

        if key in nodes:
            for k in nodes[key]:
                if k not in A:
                    Q.insert(0, k)
                    A.append(k)

        print("Q: ", Q, " - YELLOW")
        print("A: ", A, " - BLUE\n")
        createGraph()


def program():
    global Q, A, nodes
    Q = []
    A = []
    nodes = {}
    processInput()
    bfs()


def main():
    print("Traversing ALGORITHM\n")
    install()
    program()


main()

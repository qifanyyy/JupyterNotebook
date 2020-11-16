"""
Support of illustrating graphs
"""

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from warnings import catch_warnings, simplefilter


class DrawUnit:
    def __init__(self):
        self.callNumber = 0
        self.pos = []

    def drawGraph(self, graph, solution=None):
        """
        Draw 2 graphs: before and after coloring. Function also saves images

        :param graph: Input graph
        :param solution: The coloring of the graph

        """
        colors = mcolors.BASE_COLORS
        with catch_warnings():
            simplefilter("ignore")

            G = nx.Graph()
            for k in graph.getAdjDict().keys():
                G.add_node(k)
            for v in graph.getAdjDict():
                for u in graph.getAdjDict()[v]:
                    G.add_edge(u, v)

            if self.callNumber == 0:
                self.pos = nx.spring_layout(G)

            plt.figure(self.callNumber)
            nx.draw(G, self.pos, with_labels=True)
            nx.draw_networkx_nodes(G, self.pos, node_size=700)

            if self.callNumber == 0:
                plt.savefig("Graph_before_coloring")

            if solution:
                coloring = solution[0]
                colorsUsed = solution[1]

                inv_coloring = {}
                for i in range(colorsUsed + 1):
                    inv_coloring[i] = []
                for k, v in coloring.items():
                    inv_coloring[v].append(k)

                for subset, color in zip(inv_coloring.items(), colors):
                    nx.draw_networkx_nodes(G, self.pos, subset[1], node_color=color, width=4, node_size=700)

                plt.savefig("Graph_after_coloring")
                plt.show()

            self.callNumber += 1


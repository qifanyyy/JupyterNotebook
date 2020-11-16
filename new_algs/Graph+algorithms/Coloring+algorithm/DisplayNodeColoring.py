import networkx as nx
import pylab

"""
Colors nodes from lists of list, every list of nodes will be assigned different color.
Arguments: G - reference to networkx graph, colorList - list of lists of nodes
Returns: -

Note: there can't be more than 10 colors used for coloring (color list has just 10 available colors)
"""
def colorNodes(G, colorList):
    # draw the whole graph
    pos = nx.spring_layout(G)
    edge_labels = dict([((u, v,), d['weight']) for u, v, d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    nx.draw(G, pos, with_labels=True, node_color="gray")

    # color nodes
    colors = ['b', 'c', 'm', 'y', 'k', 'r', 'w', 'o', 'b', 'g']
    for i in range(len(colorList)):
        nx.draw_networkx_nodes(G, pos, nodelist = colorList[i], node_color = colors[i])

    pylab.savefig("coloredGraph.png")
    pylab.show()

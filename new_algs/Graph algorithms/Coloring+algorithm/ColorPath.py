import networkx as nx
import pylab

"""
Colors path (nodes and edges) from startNode to endNode in red.
Arguments: G - reference to networkx graph, startNode - first node on path
            endNode - last node on path, pathDic - dictionary of paths (nodes visited
            on the path) from startNode to all other nodes
Returns: -
"""
def colorPath(G, startNode, endNode, pathDic):
    # get path from dictionary
    nodeList = pathDic[endNode]
    pathEdges = [(nodeList[n], nodeList[n + 1]) for n in range(0, len(nodeList) - 1)]

    # draw the whole graph
    pos = nx.spring_layout(G)
    edge_labels = dict([((u, v,), d['weight']) for u, v, d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    nx.draw(G, pos, with_labels = True, node_color = "gray")

    # draw the path (edges and nodes) in red
    nx.draw_networkx_nodes(G, pos, nodelist = nodeList, node_color = "blue")
    nx.draw_networkx_edges(G, pos, edgelist = pathEdges, edge_color = "blue")

    # color startNode
    nx.draw_networkx_nodes(G, pos, nodelist=startNode, node_color="red")

    pylab.savefig("coloredPath.png")
    pylab.show()


"""
Colors paths from pathDic dictionary in various colors and thickness.
Arguments: G - reference to networkx graph, pathDic - dictionary of paths
Returns: -
"""
def colorMultiplePaths(G, startNode, pathDic):
    # get path nodes
    pathsNodes = []
    for k in pathDic:
        pathsNodes.append(pathDic[k])
    # get path edges
    pathsEdges = []
    for p in pathsNodes:
        edges = [(p[n], p[n + 1]) for n in range(0, len(p) - 1)]
        pathsEdges.append(edges)

    # draw the whole graph
    pos = nx.spring_layout(G)
    edge_labels = dict([((u, v,), d['weight']) for u, v, d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    nx.draw(G, pos, with_labels = True, node_color = "gray")

    # draw paths
    colors = ['b', 'c', 'm', 'y', 'k']
    linewidths = []
    for n in range(len(pathsEdges)):
        linewidths.append(3 * (len(pathsEdges) - n))
    for i, edgePath in enumerate(pathsEdges):
        nx.draw_networkx_edges(G, pos, edgelist = edgePath, edge_color = colors[i], width = linewidths[i])

    # color startNode
    nx.draw_networkx_nodes(G, pos, nodelist=startNode, node_color="red")

    pylab.savefig("coloredMultiplePaths.png")
    pylab.show()
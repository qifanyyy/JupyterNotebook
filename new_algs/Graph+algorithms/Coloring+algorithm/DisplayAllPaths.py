import networkx as nx
import pylab

"""
Colors all shortest paths from startNode in blue.
Arguments: G - reference to networkx graph, startNode - node to color red, pathDic - dictionary of paths
Returns: -
"""
def displayAllPaths(G, startNode, pathDic):
    # get tree nodes
    treeNodes = []
    for k in pathDic:
        treeNodes.append(pathDic[k])
    listNode = []
    for l in treeNodes:
        for n in l:
            if n not in listNode:
                listNode.append(n)
                
    # get tree edges
    treeEdges = []
    for p in treeNodes:
        for n in range(0, len(p) - 1):
            treeEdges.append((p[n], p[n + 1]))

    # draw the whole graph
    pos = nx.spring_layout(G)
    edge_labels = dict([((u, v,), d['weight']) for u, v, d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    nx.draw(G, pos, with_labels = True, node_color = "gray")

    # draw the tree (edges and nodes) in blue
    nx.draw_networkx_nodes(G, pos, nodelist = listNode, node_color = "blue")
    nx.draw_networkx_edges(G, pos, edgelist = treeEdges, edge_color = "blue")

    # color startNode
    nx.draw_networkx_nodes(G, pos, nodelist=startNode, node_color="red")

    pylab.savefig("coloredAllPaths.png")
    pylab.show()


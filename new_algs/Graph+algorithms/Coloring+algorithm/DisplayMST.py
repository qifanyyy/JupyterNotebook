import networkx as nx
import pylab


"""
Colors minimum spanning tree in blue.
Arguments: G - reference to networkx graph, startNode - node to color red, pathDic - dictionary of paths
Returns: -
"""
def displayMST(G, listEdges):
    # draw the whole graph
    pos = nx.spring_layout(G)
    edge_labels = dict([((u, v,), d['weight']) for u, v, d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    nx.draw(G, pos, with_labels = True, node_color = "gray")

    # draw the minimum spanning tree (edges and nodes) in blue
    nx.draw_networkx_nodes(G, pos, nodelist=G.nodes(), node_color="blue")
    nx.draw_networkx_edges(G, pos, edgelist=listEdges, edge_color="blue")

    pylab.savefig("minimumSpanningTree.png")
    pylab.show()

"""
Minimum spanning tree problem - given connected graph G, find min weight set of edges that connects all nodes.
MST has n-1 edges
APPLICATIONS of minimum spanning tree
- network design (telephone, electricity, Internet)
    - problem - business with several offices, set up lines with minimum total cost
- approximation algorithms for NP-hard problems
    - for example for travelling salesman problem
        - given the list of cities and distances between them, what is the shortest rout that visits each city and
        returns to the origin
    - in general MST weight is less then TSP weight because it is a minimization over a strictly larger set
    - if you draw a path tracing around the MST, you trace every edge twice
    - so TSP weight is less than twice MST weight
- cluster analysis
    - k clustering problem can be viewed as finding MST and deleting the k-1 most expensive edges
"""
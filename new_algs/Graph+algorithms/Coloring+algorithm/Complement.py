import networkx as nx
"""
Computes complements of graph.
Arguments: G - reference to networkx graph
Return: complement - reference to networkx graph (undirected and unweighted)

NOTES: G
        - can't have self loops
        - must be undirected
"""
def complementOfG(G):
    # create complement and list of missing edges in G
    complement = nx.Graph()
    nodeVisited = list()

    # go though all nodes N
    for node in G.nodes():
        # go though all nodes
        for potentialNeighbor in G.nodes():
            # if node and potential neighbor are the same, ignore
            if node == potentialNeighbor:
                continue
            # if potential neighbor of N was visited, edge N-neighbor was already added
            if potentialNeighbor in nodeVisited:
                continue
            # if edge N-potentialNeighbor doesn't exist
            if G.has_edge(node, potentialNeighbor) == False:
                # include into complement
                complement.add_edge(node, potentialNeighbor)
        # add node N to nodeVisited
        nodeVisited.append(node)

    return complement

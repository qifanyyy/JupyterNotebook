import numpy as np
from HeapLib import Heap


def prim(edges):
    # This function implements Prim's algorithm using a heap to store the edges

    # Rename nodes to start at 0
    node_namebase = edges[:, :-1].max()
    edges[:, :2] -= 1

    # Extract number of nodes and edges from the edgelist
    n_nodes = edges[:, :-1].max() + 1
    # n_edges = edges.shape[0]

    # Build adjacency list
    nodes = n_nodes * [[]]
    for i_node in range(n_nodes):
        nodes[i_node] = ([list(x[[1, 2]]) for x in edges if x[0] == i_node]
                         + [list(x[[0, 2]]) for x in edges if x[1] == i_node])

    # Start the algorithm from node# 0. Initialize list of explored nodes to only node 0.
    explored = np.array([True] + (n_nodes - 1) * [False])

    # Initialize heap to hold edges between any explored node and any unexplored node
    # Going forward, the heap will also have edge between explored nodes, but these will be deleted when necessary
    edge_heap = Heap("min")
    for edge in nodes[0]:
        edge_heap.insert(edge[1], [0, edge[0]])

    # Initialize cost of Minimum Spanning Tree (MST) to 0
    mst_cost = 0

    for n_nodes_added in range(1, n_nodes):

        found_good_candidate = False
        while not found_good_candidate:

            candidate = edge_heap.extractmin()

            # Determine whether this candidate edge has 0, 1 or two explored nodes
            candidate_explrd_nodes = sum(explored[candidate[1]])

            if candidate_explrd_nodes == 1:
                # Candidate is a valid edge as it bridges an explored node with an unexplored one

                # Determine which node is newly explored
                if explored[candidate[1][0]]:
                    new_node = candidate[1][1]
                else:
                    new_node = candidate[1][0]

                # Set NEW node that this edge connects to explored
                explored[new_node] = True

                # Add edges between the newly explored node and unexplored nodes to the heap
                for edge in nodes[new_node]:
                    if not explored[edge[0]]:
                        edge_heap.insert(edge[1], [new_node, edge[0]])

                # Add edge cost to MST cost
                mst_cost += candidate[0]

                # Set condition for while loop to false
                found_good_candidate = True

            elif candidate_explrd_nodes == 0:
                # Candidate is between 2 unexplored nodes. This should not occur by construction of the edge heap,
                # so raise an error
                raise Exception("Edge between two unexplored nodes found in heap.")

                # If neither condition is met, the candidate edge connects two explored nodes. In this, we can safely
                # discard it (it was removed from the heap by the extractmin() call) and look for the next minimum.

    return mst_cost

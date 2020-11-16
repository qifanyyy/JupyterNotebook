"""
@author: David Lei
@since: 20/04/2017
@modified: 

- N nodes labelled 1..N
- given start node

- remember to convert math.inf to -1

https://www.hackerrank.com/challenges/dijkstrashortreach

TLE on test case 7 with PyP3 and sys.stdin.readline(), it is just a lot of input. This soln is good for the general case.
"""
import heapq
import sys  # sys.stdin.readline().strip("\n") is faster than input()
import math

test_cases = int(sys.stdin.readline().strip("\n"))
for t in range(test_cases):
    num_nodes, num_edges = [int(x) for x in sys.stdin.readline().strip("\n").split(' ')]
    # A way to look up edges and weights.

    # Use map to handle duplicate edges.
    graph = [{} for _ in range(num_nodes + 1)]  # Index 0 is a placeholder so can index the say way nodes are numbered.
    distances = [math.inf for _ in range(num_nodes + 1)]  # Distance a vertex is.
    e = 0
    for _ in range(num_edges):  # Edges are undirected.
        node_a, node_b, weight = [int(x) for x in sys.stdin.readline().strip("\n").split(' ')]

        e += 1

        # Add edges and weights to dict, handles duplicates by picking min edge.
        if node_b not in graph[node_a]:
            graph[node_a][node_b] = weight
        else:
            graph[node_a][node_b] = min(graph[node_a][node_b], weight)

        if node_a not in graph[node_b]:
            graph[node_b][node_a] = weight
        else:
            graph[node_b][node_a] = min(graph[node_b][node_a], weight)
        # No duplicate edges should exist.
    start_node = int(sys.stdin.readline().strip("\n"))

    # Min heap takes a tuple (node_distance/cost, node_id), priority queue sorted based of distance/cost firs then
    # node_id is used as a tiebreaker.
    # Set each node distance to infinity.
    # min_heap is a priority queue of vertices that have not been chosen yet, a way to pick shortest path form a bunch of nodes.
    # heapq will compare based on item1 then item2.
    min_heap = [(math.inf, node_id) for node_id in range(1, num_nodes + 1) if node_id != start_node]
    min_heap.append((0, start_node))  # Add start node with distance/cost = 0.
    distances[start_node] = 0
    heapq.heapify(min_heap)  # Turn into heap.

    seen = [0] * (num_nodes + 1)  # List to keep track of seen nodes, index 0 is placeholder.

    while min_heap:  # Loop until all nodes are chosen (know shortest path to).
        # Get node with smallest distance to, tiebreaker: in order of node_id.
        current_node = heapq.heappop(min_heap)  # Heap is pairs of cost, node_id.
        current_node_id = current_node[1]
        current_node_cost = current_node[0]
        seen[current_node_id] = 1  # Mark node as seen.

        for adjacent_node, edge_weight in graph[current_node_id].items():  # Get nodes from adjacency list.
            # edge_weight is cost from current node to adjacent_node.
            if seen[adjacent_node] == 1:  # Already know shortest path to this node, don't process.
                continue
            # Relax edges.
            if current_node_cost + edge_weight < distances[adjacent_node]:
                distances[adjacent_node] = current_node_cost + edge_weight
                # Put back in min heap with new cost.
                heapq.heappush(min_heap, (distances[adjacent_node], adjacent_node))
    # All nodes processed, distances should have distance from source.

    # Don't count first index (placeholder) and starting node.
    relevant = [distances[k] for k in range(len(distances)) if k != start_node and k != 0]
    for d in relevant[:-1]:  # For each distance up to last.
        if d == math.inf:
            d = -1
        print("%s " % d, end="")
    print(relevant[-1] if relevant[-1] != math.inf else -1)
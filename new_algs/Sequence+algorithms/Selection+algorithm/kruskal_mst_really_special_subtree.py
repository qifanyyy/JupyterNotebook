"""
@author: David Lei
@since: 18/04/2017
@modified:

Use Kruskal's algorithm to find minimum spanning tree.
The graph is undirected.

MST = min weight, has all nodes.

1. Pick smallest weight first that connects any 2 nodes.
2. Make sure no cycle.

https://www.hackerrank.com/challenges/kruskalmstrsub

This is a really hacked together version that does lots of extra computation.
Works except for last case TLE due to extra computation. Conceptually sound.
"""


def try_traverse_dfs(list_of_edges, total_nodes_in_graph, check_cycle=False):
    edges = [(a, b) for a, b, w in list_of_edges[:]]
    start = edges[0][0]

    nodes = [start]
    nodes_looking_at = set(nodes)
    seen = set()  # Nodes seen while traversing.
    while nodes:
        cur_node = nodes.pop()
        nodes_looking_at.remove(cur_node)
        seen.add(cur_node)
        adj = [edge for edge in edges if cur_node == edge[0]]  # Forces it to be directional for cycle checking.
        for adj_edge in adj:
            if adj_edge[0] == cur_node:
                connecting_node = adj_edge[1]
            else:
                connecting_node = adj_edge[0]
            if check_cycle:
                if connecting_node in seen:
                    return True  # Is a cycle.

            if connecting_node not in seen and connecting_node not in nodes_looking_at:
                nodes_looking_at.add(connecting_node)
                nodes.append(connecting_node)
    # If nodes seen == total nodes in graph, graph is connected, can traverse to all nodes.
    # Else disconnected.
    if check_cycle:
        return False
    return len(seen) == total_nodes_in_graph

num_nodes, num_edges = [int(x) for x in input().split(' ')]

edges = []

for _ in range(num_edges):
    node_a, node_b, weight = [int(x) for x in input().split(' ')]
    edges.append((node_a, node_b, weight))

# Definition of a cycle, A->B, B->C, C->A, if you go to a node hat is already seen.

nodes = {}

# Representation of nodes for if they are in MST.
for i in range(1, num_nodes + 1):
    nodes[i] = False

edges.sort(key=lambda t:(t[2], t[0], t[1]))  # Minimum weight ordering.

nodes_in_mst = 0
edges_in_mst = []

for edge in edges:
    node_a, node_b, weight = edge
    if [e for e in edges_in_mst if e[0] == node_a and e[1] == node_b]:  # Don't allow same edge w/ diff weight.
        continue
    # This might cause a cycle.
    if nodes[node_b] and nodes[node_a]:  # Both already in MST, this will cause cycle.
        edges_in_mst.append(edge)
        cycle = try_traverse_dfs(edges_in_mst, num_nodes, check_cycle=True)

        if cycle:  # Cycle detected, don't take this edge.
            edges_in_mst.pop()
            continue
        else:
            edges_in_mst.pop()  # Code below adds in back in.

    # Can add to MST.
    edges_in_mst.append(edge)
    if not nodes[node_a]:
        nodes[node_a] = True
        nodes_in_mst += 1
    if not nodes[node_b]:
        nodes[node_b] = True
        nodes_in_mst += 1
    # Did not check all nodes are connected to for the MST.
    if num_nodes <= nodes_in_mst:  # Should not be less than, but just check to be defensive.
        res = try_traverse_dfs(edges_in_mst, num_nodes)
        if res:
            break

# MST found.
total_weight = sum([edge[2] for edge in edges_in_mst])
# print(edges_in_mst)
print(total_weight)

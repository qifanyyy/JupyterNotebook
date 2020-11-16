# Reza Asad
# Algorithm Class
# Feb 27th, 2016
######################### Algorithms ########################
from heapq import heappush, heappop, heapify
from collections import defaultdict
# This finds the minimum spanning tree of a graph using Prim's
# greedy algorithm.
def prims_mst(G):
    num_vertices = len(G)
    seen = set()
    # take a starting point.
    # The alorithm does not depend on this.
    source = G.iterkeys().next()
    seen.add(source)
    source_connection = list(G[source])
    edge_costs =  source_connection
    heapify(edge_costs)

    selected_nodes = [source]
    total_cost = 0
    while len(selected_nodes) != num_vertices:
        # Add the next vertex
        next_edge = heappop(edge_costs)
        if next_edge[1] in seen:
            continue
        total_cost += next_edge[0]
        added_vertex = next_edge[1]
        selected_nodes.append(added_vertex)
        seen.add(added_vertex)

        # Maintain the edges_cost vertex addition
        for edge in G[added_vertex]:
            if edge[1] not in seen:
                heappush(edge_costs, edge)
    return selected_nodes, total_cost
######################## Main ###############################
# Extract the edges
data_file = open('edges.txt')
# Pre process the data
graph = defaultdict(set)
next(data_file)
for line in data_file:
    vals = line.split()
    graph[vals[0]].add((int(vals[2]), vals[1]))
    graph[vals[1]].add((int(vals[2]), vals[0]))
print (prims_mst(graph))




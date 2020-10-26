"""
@author: David Lei
@since: 29/04/2017
@modified: 

"""

import heapq
import math

def relax(source, destination, edge, distances):
    if distances[source.index] + edge.cost < distances[destination.index]:
        distances[destination.index] = distances[source.index] + edge.cost
        return True
    return False

def dijkstra(graph, source):
    pq = []
    nodes = graph.get_all_vertices()
    distances = [math.inf] * len(nodes)
    path = [-1] * len(nodes)
    distances[source.index] = 0
    for node in nodes:
        # Store as (priority, task) tuples, heapq will sort on first element.
        heapq.heappush(pq, (distances[node.index], node))
    while pq:
        # Assumes non negative weights, so when popping a node it is the best way to get there.
        dist, node = heapq.heappop(pq)
        for edge in graph.get_adjacent_edges(node):
            # Note: can't terminate early and do this.
            # Eg: (s) -3-> (c) -12-> (d)
            #      \-20->(d) will be wrong
            # if distances[edge.destination.index] != math.inf:  # We already have the shortest path to this node.
            #     continue
            if relax(node, edge.destination, edge, distances):
                # Found a better way to get to a next node, add that to the pq and set the parent.
                heapq.heappush(pq, (distances[edge.destination.index], edge.destination))
                path[edge.destination.index] = node.index
    return distances, path  # Shortest path from source to any other node in distances.

if __name__ == "__main__":
    # Hackerrank submission: https://www.hackerrank.com/challenges/5595/problem
    # RTE on last one but that is allg because I think the input is massively ridiculous.
    class Node:
        def __init__(self, index):
            self.index = index
            self.bleh = 0

        # This is needed for heapq even though we can tell it should just use the first item in the tuple for ordering.
        # it requires everything to be able to be ordered, can just set them all to 0 and compare because it will never be used.
        def __lt__(self, other):
            return self.bleh < other.bleh
        def __gt__(self, other):
            return self.bleh > other.bleh
        def __eq__(self, other):
            return self.bleh == other.bleh

    class Edge:
        def __init__(self, source, destination, cost):
            self.source = source
            self.destination = destination
            self.cost = cost

    class Graph:
        def __init__(self, num_nodes):
            self.nodes = [Node(i) for i in range(num_nodes)]
            self.edges = [[] for _ in range(num_nodes)]

        def get_all_vertices(self):
            return self.nodes

        def get_adjacent_edges(self, node):
            return self.edges[node.index]

        def add_edge(self, source, destination, cost):
            edge = Edge(source, destination, cost)
            self.edges[source.index].append(edge)

    T = int(input())
    for _ in range(T):
        num_nodes, num_edges = [int(x) for x in input().split(' ')]
        graph = Graph(num_nodes + 1)
        for _ in range(num_edges):
            source, destination, cost = [int(x) for x in input().split(' ')]
            source = graph.nodes[source]
            destination = graph.nodes[destination]
            graph.add_edge(source, destination, cost)
            graph.add_edge(destination, source, cost)
        start = graph.nodes[int(input())]

        dist, paths = dijkstra(graph, start)
        for i in range(1, len(dist)):
            if i == start.index:
                continue
            print(-1 if dist[i] == math.inf else dist[i], end=" ")
        print()







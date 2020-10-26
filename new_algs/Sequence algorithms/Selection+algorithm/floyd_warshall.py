"""
@author: David Lei
@since: 7/10/2017

Implementation of floyd_wrashall shortest path between all nodes.
"""
import math

from algorithms_datastructures.graphs.implementations.adjacency_list import AdjacencyList

def floyd_warshall(graph):  # O(V^3)
    nodes = graph.get_all_vertices()
    num_nodes = len(nodes)

    # Stores shortest path, distances[i][j] is the shortest path from node i to node j.
    # If no path will be inf.
    distances = [[math.inf for _ in range(num_nodes)] for _ in range(num_nodes) ]

    path = [[-1 for _ in range(num_nodes)] for _ in range(num_nodes) ]

    for node in nodes:
        distances[node.index][node.index] = 0  # A node to itself is 0.

    for edge in graph.get_all_edges():  # graph is directed.
        # You can get from origin to destination of an edge with cost the weight of the edge.
        distances[edge.origin.index][edge.destination.index] = edge.weight
        path[edge.origin.index][edge.destination.index] = edge.origin.index

    for k in range(num_nodes):
        # Is going through node k going to give a shorter distance.
        for i in range(num_nodes):
            # Look at node i.
            for j in range(num_nodes):
                # Try get to node j.
                if distances[i][j] > distances[i][k] + distances[k][j]:
                    # Cost to get to node j from i is greater than the cost to get from i to k and then from k to j.
                    # Meaning we found a shorter path going through node k.
                    distances[i][j] = distances[i][k] + distances[k][j]
                    path[i][j] = path[k][j]  # Update path to show shortest path from i to j goes through k to get to j.

    # Check if there is a negative weight cycle, if a diagonal is negative there is a negative weight cycle.
    for i in range(num_nodes):
        if distances[i][i] < 0:
            print("Has negative weight cycle")
            return False, path

    return distances, path


def print_path_from_matrix(distances, graph, paths, source, target):
    source_index = source.index
    target_index = target.index

    path = [target.index]
    current = paths[source_index][target_index]

    while current != -1:
        path.append(current)
        current = paths[source_index][current]
    path = path[::-1]  # Node indices.

    print("Shortest path from %s to %s is %s" % (source.rep, target.rep, distances[source.index][target.index]))
    for node_index in path:
        node = graph.list[node_index]
        print(node.rep, end="->")
    print('end')


def run_floyd_warshall(test_num, make_graph_fn):
    print("\t\t~~~ Test: %s ~~~" % test_num)
    graph, s, t = make_graph_fn()
    distances, paths = floyd_warshall(graph)
    if distances:
        print("Distances")
        for row in distances:
            print(row)
        print("Path")
        for row in paths:
            print(row)
        print_path_from_matrix(distances, graph, paths, s, t)

def make_graph_1():
    # https://www.youtube.com/watch?v=4OQeCuLYj-4&ab_channel=MichaelSambol
    graph = AdjacencyList(4)
    one = graph.add_vertex(index=0, rep='(1)')
    two = graph.add_vertex(index=1, rep='(2)')
    three = graph.add_vertex(index=2, rep='(3)')
    four = graph.add_vertex(index=3, rep='(4)')
    graph.add_edge(origin_vertex=one, destination_vertex=three, weight=-2)
    graph.add_edge(origin_vertex=three, destination_vertex=four, weight=2)
    graph.add_edge(origin_vertex=four, destination_vertex=two, weight=-1)
    graph.add_edge(origin_vertex=two, destination_vertex=three, weight=3)
    graph.add_edge(origin_vertex=two, destination_vertex=one, weight=4)
    return graph, four, three

if __name__ == "__main__":
    run_floyd_warshall(1, make_graph_1)
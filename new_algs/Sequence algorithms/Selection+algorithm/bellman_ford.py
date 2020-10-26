"""
@author: David Lei
@since: 29/04/2017
@modified:

Implementation of bellman-ford to find shortest path from a single source to all other nodes in a dag with negative edge weights.

"""
import math
from algorithms_datastructures.graphs.implementations.adjacency_list import AdjacencyList

def relax(edge, parents, distance):
    origin = edge.origin
    destination = edge.destination
    cost = edge.weight

    if distance[origin.index] + cost < distance[destination.index]:
        distance[destination.index] = distance[origin.index] + cost
        parents[destination.index] = origin.index

def bellman_ford(graph, source, parents, distance):  # O(V * E)
    distance[source.index] = 0
    # Does work here.
    for node in graph.get_vertices():  # O(V) Can improve this by stopping if nothing changes.
        for edge in graph.get_all_edges():  # O(E)
            relax(edge, parents, distance)
    # One more check to see if there are negative cycles.
    for edge in graph.get_all_edges():
        if distance[edge.destination.index] > distance[edge.origin.index] + edge.weight:
            return False
    return True

def run_bellman_ford(test_num, num_nodes, make_graph_fn):
    print("\t\t~~~ Test: %s ~~~" % test_num)
    distance = [math.inf for _ in range(num_nodes)]
    parents = [-1 for _ in range(num_nodes)]
    graph, source, target, expected = make_graph_fn()
    no_neg_cycle = bellman_ford(graph, source, parents, distance)
    nodes = graph.get_vertices()
    distances_labeled = []
    for i in range(len(nodes)):
        distances_labeled.append((nodes[i].rep, distance[i]))
    print("Distances labeled: %s" % distances_labeled)
    print("Parents: %s" % parents)
    if no_neg_cycle:
        path = []
        current = target.index
        while current != -1:
            path.append(nodes[current].rep)
            current = parents[current]
        path = path[::-1]
        print("Shortest path from: %s to %s is \n%s" % (source.rep, target.rep, path))
    else:
      print("Has negative cycle, no solution.")
    print("Passed: %s\n" % (expected == distance if no_neg_cycle else no_neg_cycle == expected))

# -------------------------------------- driver functions ----------------------------------------

def make_graph_1():
    # http://www.programming-algorithms.net/article/47389/Bellman-Ford-algorithm
    graph = AdjacencyList(6)
    S = graph.add_vertex(index=0, rep='S')
    A = graph.add_vertex(index=1, rep='A')
    B = graph.add_vertex(index=2, rep='B')
    C = graph.add_vertex(index=3, rep='C')
    D = graph.add_vertex(index=4, rep='D')
    E = graph.add_vertex(index=5, rep='E')
    graph.add_edge(origin_vertex=S, destination_vertex=A, weight=10)
    graph.add_edge(origin_vertex=S, destination_vertex=E, weight=8)
    graph.add_edge(origin_vertex=E, destination_vertex=D, weight=1)
    graph.add_edge(origin_vertex=D, destination_vertex=A, weight=-4)
    graph.add_edge(origin_vertex=D, destination_vertex=C, weight=-1)
    graph.add_edge(origin_vertex=A, destination_vertex=C, weight=2)
    graph.add_edge(origin_vertex=C, destination_vertex=B, weight=-2)
    graph.add_edge(origin_vertex=B, destination_vertex=A, weight=1)
    # S A B C D E
    # 0 5 5 7 9 8
    expected = [0, 5, 5, 7, 9, 8]
    return graph, S, C, expected

def make_graph_2():
    # https://www.youtube.com/watch?v=-mOEd_3gTK0&ab_channel=TusharRoy-CodingMadeSimple
    graph = AdjacencyList(5)
    zero = graph.add_vertex(index=0, rep='(0)')
    one = graph.add_vertex(index=1, rep='(1)')
    two = graph.add_vertex(index=2, rep='(2)')
    three = graph.add_vertex(index=3, rep='(3)')
    four = graph.add_vertex(index=4, rep='(4)')
    graph.add_edge(origin_vertex=zero, destination_vertex=one, weight=4)
    graph.add_edge(origin_vertex=zero, destination_vertex=two, weight=5)
    graph.add_edge(origin_vertex=one, destination_vertex=two, weight=-3)
    graph.add_edge(origin_vertex=zero, destination_vertex=three, weight=8)
    graph.add_edge(origin_vertex=three, destination_vertex=four, weight=2)
    graph.add_edge(origin_vertex=four, destination_vertex=three, weight=1)
    graph.add_edge(origin_vertex=two, destination_vertex=four, weight=4)
    expected = [0, 4, 1, 6, 5]
    return graph, zero, three, expected

def make_graph_with_neg_cycle():
    # https://www.youtube.com/watch?v=-mOEd_3gTK0&t=969s&ab_channel=TusharRoy-CodingMadeSimple
    graph = AdjacencyList(4)
    zero = graph.add_vertex(index=0, rep='(0)')
    one = graph.add_vertex(index=1, rep='(1)')
    two = graph.add_vertex(index=2, rep='(2)')
    three = graph.add_vertex(index=3, rep='(3)')
    graph.add_edge(origin_vertex=zero, destination_vertex=one, weight=1)
    graph.add_edge(origin_vertex=one, destination_vertex=two, weight=3)
    graph.add_edge(origin_vertex=two, destination_vertex=three, weight=2)
    graph.add_edge(origin_vertex=three, destination_vertex=one, weight=-6)
    expected = False
    return graph, zero, one, expected

if __name__ == "__main__":
    run_bellman_ford(1, 6, make_graph_1)
    run_bellman_ford(2, 5, make_graph_2)
    run_bellman_ford(3, 4, make_graph_with_neg_cycle) # Note: Each iteration of bellman-ford will decrease distance when there is a negative cycle.

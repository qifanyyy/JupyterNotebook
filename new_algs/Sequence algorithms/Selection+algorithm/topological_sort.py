"""
@author: David Lei
@since: 18/10/2017

"""
from collections import deque

def topological_sort_rec(dag, node, visited, stack):  # Called O(n) times at max.
    print('called')  # Can use this to show it has only been called O(n) times.
    if visited[node.index] != 1:
        visited[node.index] = 1
        for edge in dag.get_adjacent_edges(node):  # Explore all children, O(e).
            # Exploring children first and putting them on the stack first means when we pop elements off
            # it is guaranteed parents happen before children meaning we can only do child after parent.
            if visited[edge.destination.index] == 0:
                topological_sort_rec(dag, edge.destination, visited, stack)
        stack.append(node)  # Add node to the stack only once all children explored.

def topological_sort_aux(dag):
    nodes = dag.get_all_vertices()
    visited = [0] * len(nodes)
    stack = deque()

    for node in nodes: # O(n)
        if visited[node.index] == 0:
            topological_sort_rec(dag, node, visited, stack)
    topological_ordering = []
    while stack: # O(n)
        topological_ordering.append(stack.pop().rep)
    return topological_ordering

if __name__ == "__main__":
    from algorithms_datastructures.graphs.implementations.adjacency_list import AdjacencyList

    # Graph from https://www.youtube.com/watch?v=ddTC4Zovtbc
    dag = AdjacencyList(8)
    A = dag.add_vertex(0, 'A')
    B = dag.add_vertex(1, 'B')
    C = dag.add_vertex(2, 'C')
    D = dag.add_vertex(3, 'D')
    E = dag.add_vertex(4, 'E')
    F = dag.add_vertex(5, 'F')
    G = dag.add_vertex(6, 'G')
    H = dag.add_vertex(7, 'H')
    dag.add_edge(origin_vertex=A, destination_vertex=C)
    dag.add_edge(origin_vertex=B, destination_vertex=C)
    dag.add_edge(origin_vertex=B, destination_vertex=D)
    dag.add_edge(origin_vertex=C, destination_vertex=E)
    dag.add_edge(origin_vertex=D, destination_vertex=F)
    dag.add_edge(origin_vertex=E, destination_vertex=H)
    dag.add_edge(origin_vertex=E, destination_vertex=F)
    dag.add_edge(origin_vertex=F, destination_vertex=G)

    top_ordering = topological_sort_aux(dag)
    print(top_ordering)  # ['B', 'D', 'A', 'C', 'E', 'F', 'G', 'H'] is a valid topological ordering.


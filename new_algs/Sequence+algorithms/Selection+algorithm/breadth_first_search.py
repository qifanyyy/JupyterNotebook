"""
@author: David Lei
@since: 21/08/2016
@modified: 

How it works
    Breadth = Long or length wise = Queue (FIFO)
        - explore neighbour nodes first
        - then move on to a deeper level

        1. Start with an empty Queue
        2. Initialize each node to have infinity distance
        3. Visit a node, current node = node visited, add it to the output
        4. Loop while not all nodes visited
            5. Visit all nodes you can from current node and Enqueue them and add them to output
            6. When you can't visit anymore, current node = Deque Q
            repeat until finished
        note: if stalemate in picking node pick in alphabetical order

Time complexity: O(v + e)
    - need to look at each node
    - for a given current node, we look at all adjacent edges (eventually look at all edges)
    O(v + e) as we look at all edges and nodes
    O(e) wil at most be O(v^2) and at least O(1)
    so worst case bounded by e = O(e)


Space complexity: O(v)
    - output array
    - queue
    both are of the size of the number of nodes = O(2v) = O(v)

Can use to traverse trees or graphs

Note: order you put things in dict isn't always reflected in output, so if i keep running this bfs result on
graph_map might change
http://stackoverflow.com/questions/4458169/in-what-order-does-python-display-dictionary-keys
"The order has to do with how they work internally and what order they end up in the hashtable.
That in turn depends on the keys hash-value, the order they were inserted, and which Python implementation you are using.
The order is arbitrary (but not random) and it will never be useful to know which order it will be."
"""
from collections import deque
from algorithms_datastructures.datastructures.linked_queue import LinkedQueue

def bfs_2(graph, root):
    q = deque([root])
    visited = [0] * len(graph.get_all_vertices())
    output = []
    while q:
        node = q.popleft()
        if visited[node.index] == 0:
            visited[node.index] = 1
            output.append(node)
        for edge in graph.get_adjacent_edges(node):
            next_node = edge.destination
            if visited[next_node.index] == 0:
                q.append(next_node)
    return output


def breadth_first_search(graph, root, use_rep=False):

    nodes = graph.get_vertices()

    for node in nodes:
        node.distance = "Infinity"

    root.distance = 0
    queue = LinkedQueue()                                 # array acting as a Queue, root enqueued
    queue.enqueue(root)
    output = [root.rep if use_rep else root.index]
    while not queue.is_empty():                           # while stuff in Q
        current_node = queue.deque()
        edges = graph.get_adjacent_edges(current_node)
        for edge in edges:                                # for nodes adjacent, at most once per edge as we check if the end of the edge is visit or not
            node = edge.destination
            if node.distance == "Infinity":
                node.distance = current_node.distance + 1
                queue.enqueue(node)
                output.append(node.rep if use_rep else node.name)  # .name just because of the weird way I implemented it :P
    return output

if __name__ == "__main__":
    from algorithms_datastructures.graphs.implementations.adjacency_map import AdjacencyMap
    from algorithms_datastructures.graphs.implementations.adjacency_list import AdjacencyList

    # Example from FIT2004 sem 2 2014 lec 15, slide 16 = A, B, C, E, F, D
    # any permutation of B, C, E (lvl 1) and F, D (lvl 2) are fine as they are all on the same level
    print("Testing bfs on adjacency map")
    graph_map = AdjacencyMap()
    # Set up adj map graph.
    A = graph_map.add_vertex('A')
    B = graph_map.add_vertex('B')
    C = graph_map.add_vertex('C')
    D = graph_map.add_vertex('D')
    E = graph_map.add_vertex('E')
    F = graph_map.add_vertex('F')
    graph_map.add_edge(A, B)
    graph_map.add_edge(A, C)
    graph_map.add_edge(A, E)
    graph_map.add_edge(B, C)
    graph_map.add_edge(B, F)
    graph_map.add_edge(C, D)
    graph_map.add_edge(E, D)
    graph_map.add_edge(F, D)
    source = A
    bfs_adj_map = breadth_first_search(graph_map, source)
    print("BFS on adj_map graph: " + str(bfs_adj_map))
    # Sometimes the order of the adjacency_map changes (it is still correct, just not alphabetical)
    # this is because there is some randomness with dictionaries.

    print("\nTesting bfs on adjacency list.")
    graph_list = AdjacencyList(6)
    # This Graph List data structure assumes a directed graph
    # set up adj map graph, slightly different set up due to diff underlying structure
    a = graph_list.add_vertex(0,'A')
    b = graph_list.add_vertex(1,'B')
    c = graph_list.add_vertex(2,'C')
    d = graph_list.add_vertex(3,'D')
    e = graph_list.add_vertex(4,'E')
    f = graph_list.add_vertex(5,'F')
    # Undirected.
    graph_list.add_edge(a, b)
    graph_list.add_edge(a, c)
    graph_list.add_edge(a, e)
    graph_list.add_edge(b, c)
    graph_list.add_edge(b, f)
    graph_list.add_edge(c, d)
    graph_list.add_edge(e, d)
    graph_list.add_edge(f, d)
    graph_list.add_edge(b, a)
    graph_list.add_edge(c, a)
    graph_list.add_edge(e, a)
    graph_list.add_edge(c, b)
    graph_list.add_edge(f, b)
    graph_list.add_edge(d, c)
    graph_list.add_edge(d, e)
    graph_list.add_edge(d, f)

    source2 = a

    bfs_adj_list = breadth_first_search(graph_list, source2, use_rep=True)
    bfs_adj_list_2 = bfs_2(graph_list, source2)
    bfs_adj_list_2 = [node.rep for node in bfs_adj_list_2]
    print("BFS on adj_list graph: " + str(bfs_adj_list))
    if bfs_adj_list_2 == bfs_adj_list:
        print("Yay bfs worked")
    else:
        print("bfs_2() might have not worked: " + str(bfs_adj_list_2))





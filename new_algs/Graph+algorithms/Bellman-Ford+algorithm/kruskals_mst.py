"""Python Kruskal's minimum spanning tree implementation."""

from disjoint_set import DisjointSet


testcase = {
    'a': {'b': 4, 'h': 8},
    'b': {'a': 4, 'c': 8, 'h': 11},
    'c': {'b': 8, 'd': 7, 'f': 4, 'i': 2},
    'd': {'c': 7, 'e': 9, 'f': 14},
    'e': {'d': 9, 'f': 10},
    'f': {'c': 4, 'd': 14, 'e': 10, 'g': 2},
    'g': {'i': 6, 'f': 2, 'h': 1},
    'h': {'a': 8, 'b': 11, 'i': 7, 'g': 1},
    'i': {'c': 2, 'g': 6, 'h': 7}
}


def kruskals(graph):
    """Returns MST edges. If a graph is disconnected it will still process all the edges,
    but exception will be raised, instead of returning MST forest edges.
    """
    disjoint_set = DisjointSet()

    # Extract edges from an adjacency list representation of a graph.
    edges = []  # (u, v, dist)
    for u in graph:
        for v, dist in graph[u].items():
            edges.append((u, v, dist))
            disjoint_set.make_set(v)
        disjoint_set.make_set(u)

    # Sort edges by a distance in ascending order.
    edges.sort(key=lambda x: x[2])

    mst = []
    for edge in edges:
        if disjoint_set.is_connected(edge[0], edge[1]):
            continue

        disjoint_set.union(edge[0], edge[1])
        mst.append(edge)

        # MST should have |V|-1 edges.
        if len(mst) == len(disjoint_set) - 1:
            return mst

    # Mst becomes minimum spanning forest here
    raise Exception("The graph is disconnected.")


if __name__ == "__main__":
    from display_graph import display_graph

    mst_edges = [(i[0], i[1]) for i in kruskals(testcase)]
    display_graph(testcase, mst_edges)

"""Python implementation of Prim-Dijkstra-Jarnik MST algorithm.
Prim (1957), Dijkstra (1959), Jarnik (1930)"""

import heapq


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


def prims(graph, start):
    visited = {start}
    distances = {start: 0}
    paths = []
    edges = []  # priority queue
    tail = start
    for _ in range(len(graph)):
        if tail in graph:
            for head, dist in graph[tail].items():
                if head in visited:
                    continue

                edge = (dist, head, tail)
                heapq.heappush(edges, edge)

        while edges:
            d, h, t = heapq.heappop(edges)  # dist, head, tail
            if h not in visited:
                visited.add(h)
                distances[h] = d
                paths.append((t, h))
                tail = h
                break

    return distances, paths


if __name__ == "__main__":
    from display_graph import display_graph

    _, mst = prims(testcase, 'i')
    display_graph(testcase, mst)

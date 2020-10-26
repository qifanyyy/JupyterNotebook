import argparse
from collections import defaultdict
from contextlib import closing


parser = argparse.ArgumentParser(description="Determine the shortest distance between to OSM nodes.")
parser.add_argument("--data", dest="data", type=str, help="Location of .dat")
parser.add_argument("--start", dest="start", type=str, help="Start node id")
parser.add_argument("--end", dest="end", type=str, help="End node id")


class Graph():
    def __init__(self):
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        # All edges are bidirectional.
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = int(weight)
        self.weights[(to_node, from_node)] = int(weight)


def parse_data(data_path):
    """
    File format:
    <number of nodes>
    <OSM id of node>
    ...
    <OSM id of node>
    <number of edges>
    <from node OSM id> <to node OSM id> <length in meters>
    ...
    <from node OSM id> <to node OSM id> <length in meters>
    """

    edges = []
    with closing(open(data_path)) as f:
        node_count = f.readline()
        for _ in range(int(node_count)):
            # throw nodes on the floor
            f.readline()

        edge_count = f.readline()
        for _ in range(int(edge_count)):
            from_node, to_node, distance = f.readline().split()

            edges.append((from_node, to_node, distance))

    return edges


def dijkstra_path(graph, start, end):
    # shortest paths is a dict of nodes whose value is a tuple of (previous node, weight)
    shortest_paths = {start: (None, 0)}
    current_node = start
    visited = set()

    while current_node != end:
        visited.add(current_node)
        neighbours = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in neighbours:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                if shortest_paths[next_node][1] > weight:
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            raise Exception("Route not possible")

        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node

    return path


def dijkstra_length(graph, start, end):
    path = dijkstra_path(graph, start, end)
    length = sum([graph.weights[(path[i], path[i+1])] for i in range(len(path) - 1)])

    return length


def main():
    args = parser.parse_args()

    edges = parse_data(args.data)

    graph = Graph()

    for edge in edges:
        graph.add_edge(*edge)

    length = dijkstra_length(graph, args.start, args.end)

    print(length)


if __name__ == "__main__":
    main()

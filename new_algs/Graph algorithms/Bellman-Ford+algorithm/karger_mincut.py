
"""Python implementation of Karger's mincut algorithm.

Karger Mincut is a type of Monte Carlo algorithm and has to be run
multiple times with a hope to find minimum cuts, but with no guarantee.

Implementation notes:
Three containers are in play, while node contraction progresses.
1. Copy of a graph in a form of weighted adjacency list, where weight
represents a number of connections between points.
2. Copy of edges list.
3. Index dictionary, which maps tail points with indexes of edges location in
edges list where such a node is present.

Randomness is realized by random.shuffle function.
"""

from collections import defaultdict
from random import shuffle
from copy import deepcopy


TESTCASE = {
    'a': {'b': 1, 'c': 1},
    'b': {'a': 1, 'c': 1, 'd': 1},
    'c': {'a': 1, 'b': 1, 'd': 1},
    'd': {'b': 1, 'c': 1}
}


class MinCut:
    """Public run_mincut(runs) method does the job. Results are hold by
    instance variables mincuts_num and mincuts_edges.
    """
    def __init__(self, graph):
        """Graph and edges variables are initialized instantly. Graph is the original
        input graph and won't be changed at any point. Instead, it will be copied for
        each mincut run. The edges variable will only be shuffled before each run and
        then copied for further modifications.

        Mincuts_num and mincuts_edges will keep the minimum cut results and will be
        updated after each run if better values are discovered.
        """
        self.graph = graph
        self.edges = []
        self._generate_edges()

        self.mincuts_num = float('inf')
        self.mincuts_edges = []

    def _generate_edges(self):
        """Generates a list of edges. The list helps to get uniformly random distribution
        of edges. Randomness will be realized by shuffling the list before each mincut run.
        """
        for tail in self.graph:
            for head in self.graph[tail]:
                self.edges.append([tail, head])

    @staticmethod
    def edges_index_mapper(edges):
        """Returns a dictionary, which holds tail vertex as a key and
        set of indexes as a value. Indexes point at location of an edge
        in the 'edges' list.
        """
        mapper = defaultdict(set)
        for idx, edge in enumerate(edges):
            mapper[edge[0]].add(idx)
        return mapper

    def contract(self):
        """Three containers are in play, while node contraction progresses.
        1. Copy of a graph in form of adjacency list. Contracted points are deleted.

        2. Copy of edges list, which is traversed backwards from the last index.
        Original edges list is shuffled before each run and then the copy is made.
        Self-loops are set to None. Edges, which are to be updated are localized by
        taking use of an index dictionary.

        3. Index dictionary maps tail points with indexes of edges list where such
        a node exists. Indexes are updated and removed during contraction process.

        Returns remaining edges after contraction is finished.
        """
        shuffle(self.edges)

        edges = deepcopy(self.edges)
        graph_copy = deepcopy(self.graph)
        indexes = self.edges_index_mapper(edges)

        last_edge_idx = len(edges) - 1
        while len(graph_copy) > 2:
            edge = edges[last_edge_idx]
            last_edge_idx -= 1
            if edge is None:
                continue

            # Merging vertex, merged vertex
            node_kept, node_merged = edge

            # Replace merged node with kept node in all edges it's been a part of as head.
            for vertex in graph_copy[node_merged]:
                if node_kept not in graph_copy[vertex]:
                    graph_copy[vertex][node_kept] = graph_copy[vertex][node_merged]
                else:
                    graph_copy[vertex][node_kept] += graph_copy[vertex][node_merged]

                del graph_copy[vertex][node_merged]

                # Expand kept node with edge from merged node.
                if vertex not in graph_copy[node_kept]:
                    graph_copy[node_kept][vertex] = graph_copy[node_merged][vertex]
                else:
                    graph_copy[node_kept][vertex] += graph_copy[node_merged][vertex]

                # Change edges in edges list, using index locations from indexes dictionary.
                for idx in tuple(indexes[vertex]):
                    if edges[idx][0] == node_kept and edges[idx][1] == node_merged:  # self-loop
                        edges[idx] = None
                        indexes[node_kept].discard(idx)
                    elif edges[idx][1] == node_merged:
                        edges[idx][1] = node_kept

            # Replace merged node with kept node in all edges it's been a part of as tail.
            for edge_idx in tuple(indexes[node_merged]):
                if edges[edge_idx][1] == node_kept:  # self-loop
                    edges[edge_idx] = None
                    indexes[node_merged].discard(edge_idx)
                else:
                    edges[edge_idx][0] = node_kept

            # Remove self-loops form node_kept
            graph_copy[node_kept].pop(node_kept, None)

            # Add edge indexes from merged node to kept node.
            indexes[node_kept].update(indexes[node_merged])

            # Remove contracted node from graph and from edge index mapper.
            del graph_copy[node_merged]
            del indexes[node_merged]

        # Return original edges that survived contraction.
        return [self.edges[e] for e in indexes[list(graph_copy.keys())[0]]]

    def run_mincut(self, runs):
        """Runs contraction algorithm multiple times, specified by
        the 'runs' parameter. Keeps minimum cuts number and edges in
        instance variables: mincuts_num and mincuts_edges.
        """
        for _ in range(runs):
            edges = self.contract()
            current_cuts_num = len(edges)
            if current_cuts_num < self.mincuts_num:
                self.mincuts_num = current_cuts_num
                self.mincuts_edges = edges


if __name__ == "__main__":
    import networkx as nx
    import matplotlib.pyplot as plt

    m = MinCut(TESTCASE)
    m.run_mincut(50)
    all_edges = m.edges

    # all_edges have duplicated edges in reversed points order. Example: [1, 2] and [2, 1].
    # Duplicate edges are not necessary for applying color to the graph.
    # So, either we remove duplicates from all_edges or add reversed edges to m.mincuts_edges list,
    # where edges are present without their reversed reflections. We choose the latter approach.
    mincut_edges = []
    for anedge in m.mincuts_edges:
        mincut_edges.append(anedge)
        mincut_edges.append(anedge[::-1])

    # Define color for every edge. Red for the mincut edges and black for the rest.
    colors = ['r' if e in mincut_edges else 'black' for e in all_edges]

    print(m.mincuts_edges)  # Mincut edges
    print('Number of mincut edges: ', m.mincuts_num)

    G = nx.MultiGraph(all_edges)
    # edgelist parameter has to be given to assure the right order of edges sequence,
    # which otherwise, would be messed up under the hood of networkx module.
    nx.draw(G, edgelist=all_edges, edge_color=colors, with_labels=True, width=1.7)
    plt.show()

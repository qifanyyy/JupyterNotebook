
"""Python implementation of Kosaraju's algorithm
for finding strongly connected components.

Usage example:

>>> scc = KosarajuSCC(TESTCASE)
>>> scc.find_scc()
>>> print(sorted(map(len, scc.scc.values())))
[1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 6]
"""

import resource
import sys
from collections import defaultdict


# Deep recursive calls require a change of default limits.
resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
sys.setrecursionlimit(10**6)


TESTCASE = {1: {7, 11},
            2: {5, 12},
            3: {9, 12, 4},
            4: {1, 13},
            5: {8, 14},
            6: {3, 8, 15},
            7: {4, 9, 16},
            8: {2, 17},
            9: {6, 18},
            19: {}}


class KosarajuSCC:
    """The algorithm takes advantage of the fact, stating that:
    The same graph with the direction of every edge reversed has exactly
    the same strongly connected components as the original graph.
    """
    def __init__(self, graph):
        self.graph = graph
        self.graph_rev = defaultdict(set)
        self._explored = set()
        self._stack = []  # points ordered by finishing time.
        self.scc = {}
        self.leader = None
        self._reverse_graph()

    def _reverse_graph(self):
        """Creates a reversed graph."""
        for tail in self.graph:
            if tail not in self.graph_rev:
                self.graph_rev[tail] = set()
            for head in self.graph[tail]:
                self.graph_rev[head].add(tail)

    def _dfs(self, graph, tail):
        """First dfs run and setting finishing time stack."""
        self._explored.add(tail)
        if tail in graph:
            for head in graph[tail]:
                if head not in self._explored:
                    self._dfs(graph, head)
        self._stack.append(tail)

    def _dfs2(self, graph, tail):
        """Second dfs run. Creation of strongly connected components dictionary
        with leader as a key and list of components as a value.
        """
        self._explored.add(tail)
        self.scc[self.leader].append(tail)

        for head in graph[tail]:
            if head not in self._explored:
                self._dfs2(graph, head)

    def find_scc(self):
        """Strongly connected components main method. First, dfs traverses the
        original graph and builds a stack of points according to finishing times.
        Next, dfs2 traverses the reversed graph in the order of points in the stack.
        """
        # First run.
        for node in self.graph:
            if node not in self._explored:
                self._dfs(self.graph, node)

        self._explored.clear()

        # Second run. Reversed direction. Ordered by finishing times.
        while self._stack:
            leader = self._stack.pop()
            if leader not in self._explored:
                self.leader = leader
                self.scc[leader] = []
                self._dfs2(self.graph_rev, leader)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

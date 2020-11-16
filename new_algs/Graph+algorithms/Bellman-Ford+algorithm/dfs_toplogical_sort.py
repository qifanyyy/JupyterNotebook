
"""Python implementation of topological sorting using depth-first search.

Input graph has to be directed and acyclic.
There can be many valid sorting results, since the key of
the job is to keep depended tasks/points in the right order.

                A ---> B ---> D
                 |          |
                  ---> C ---

So, for the above graph, there are 2 possible sorting orders:
ABCD or ACBD.
Both are correct and indicate that B and C have to precede D.
Also they have to follow A. However, there's no precedence
relation between themselves, so they can be sequenced freely.

Usage example:
G = {
    'B': {'E', 'F'},
    'A': {'C', 'E'},
    'C': {'D'},
    'D': {'F'},
    'E': {},
    'F': {}
}

TopologicalSort(G).sort()
"""


class TopologicalSort:
    def __init__(self, graph):
        """Input graph in form of g = {1: {2,3}, 3: {}}
        ordered - topological order. From final points to first ones.
        It's returned in a reversed order.
        """
        self.graph = graph
        self.explored = set()
        self.ordered = []

    def _dfs_loop(self):
        """Loops through every vertex and runs dfs from it.
        It's needed since we might not travers a whole directed,
        acyclic graph otherwise.
        """
        for node in self.graph:
            if node not in self.explored:
                self._dfs(node)
                self.explored.add(node)

    def _dfs(self, tail):
        """Depth-first recursive traversal."""
        for head in self.graph[tail]:
            if head not in self.explored:
                self.explored.add(head)
                self._dfs(head)

        self.ordered.append(tail)

    def sort(self):
        """Returns reversed result, since DFS recursion discovers
        the most distant points first and then backtracks,
        so such points are at the beginning of the list."""
        self._dfs_loop()
        return self.ordered[::-1]

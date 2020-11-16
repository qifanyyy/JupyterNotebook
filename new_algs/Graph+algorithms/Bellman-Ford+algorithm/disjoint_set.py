"""Python implementation of union find structure."""


from collections import defaultdict


class DisjointSet:
    """Public instance methods: make_set, find, union, is_connected, get_clusters."""

    def __init__(self):
        self.ds = {}  # {node: [parent, rank]}

    def __len__(self):
        return len(self.ds)

    def make_set(self, x):
        """Add a node x with a parent set to itself and rank equal to 0."""
        self.ds[x] = [x, 0]

    def find(self, x):
        """Path compression"""
        if x != self.ds[x][0]:
            self.ds[x][0] = self.find(self.ds[x][0])
        return self.ds[x][0]

    def union(self, x, y):
        """Union by rank."""
        xp, yp = self.find(x), self.find(y)
        if self.ds[xp][1] > self.ds[yp][1]:
            self.ds[yp][0] = xp
        else:
            self.ds[xp][0] = yp
            if self.ds[xp][1] == self.ds[yp][1]:
                # if ranks are equal, increase yp rank by 1
                self.ds[yp][1] += 1

    def is_connected(self, x, y):
        """Checks if two points are in the same tree. Have the same parent/leader."""
        return self.find(x) == self.find(y)

    def get_clusters(self):
        """Runs find method for all points to ensure they've got the correct leader.
        Returns dict with clusters as keys and lists containing associated points as values.
        """
        clusters = defaultdict(list)
        for node in self.ds:
            leader = self.find(node)
            clusters[leader].append(node)
        return clusters

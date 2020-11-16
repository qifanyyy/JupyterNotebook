"""
Implementation of the "disjoint set" data structure.
"""

from collections import defaultdict


class DisjointSet:
    """
    Disjoint set of items.
    """

    def __init__(self, items=None):
        self.items = [] if items is None else items
        self.parents = {item: None for item in items}
        self.ranks = {item: 1 for item in items}

    def find(self, item):
        """
        Find the set representative. (Uses path-compression)
        """
        if self.parents[item] is None:
            return item
        self.parents[item] = self.find(self.parents[item])
        return self.parents[item]

    def union(self, a, b):
        """
        Merge two sets if not already merged. (union-by-rank)
        """
        a_root = self.find(a)
        b_root = self.find(b)

        if a_root == b_root:
            return

        if self.ranks[a_root] < self.ranks[b_root]:
            self.parents[a_root] = b_root
        else:
            self.parents[b_root] = a_root
            if self.ranks[a_root] == self.ranks[b_root]:
                self.ranks[a_root] += 1

    def __repr__(self):
        sets = defaultdict(set)
        for item in self.items:
            root = self.find(item)
            sets[root].add(item)
        return repr(list(sets.values()))

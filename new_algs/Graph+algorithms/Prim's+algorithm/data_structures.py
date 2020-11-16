from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from typing import Any, Optional, Tuple


class PriorityQueue:
    
    def __init__(self):
        self._queue = []
    
    def put(self, item: Tuple[int, Any]):
        heapq.heappush(self._queue, item)
    
    def get(self):
        return heapq.heappop(self._queue)

    def __len__(self):
        return len(self._queue)


@dataclass
class Node:
    id : int
    parent: Optional[Node] = None
    rank: int = field(default=0, init=False)


class UnionFind:

    def __init__(self):
        self._items = []
        self._roots = []
        self._id = 0
    
    def add(self, item: Any):
        if item in self._items:
            return
        
        self._items.append(item)
        node = Node(self._id)
        node.parent = node
        self._roots.append(node)
        self._id += 1
    
    def find(self, item: Any):
        id = self._items.index(item)
        root = self.find_root(id)
        return self._items[root.id]

    def find_root(self, id: int):
        node = self._roots[id]
        while node.id != node.parent.id:
            node = node.parent

        root = node

        # path compression
        node = self._roots[id]
        while node.id != root.id:
            parent = node.parent
            node.parent = root
            node = parent
        
        return root

    def union(self, itemx: Any, itemy: Any):
        idx = self._items.index(itemx)
        idy = self._items.index(itemy)
        rootx = self.find_root(idx)
        rooty = self.find_root(idy)

        if rootx.id == rooty.id:
            return
        
        if rootx.rank < rooty.rank:
            rootx.parent = rooty
        elif rootx.rank > rooty.rank:
            rooty.parent = rootx
        else:
            rooty.parent = rootx
            rootx.rank += 1
        
    def _node(self, item: Any):
        id = self._items.index(item)
        return self._roots[id]
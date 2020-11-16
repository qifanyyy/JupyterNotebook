"""Python heap implementation. Both, min-heap and max-heap covered."""

import operator


class Heap:
    """Creates max-heap or min-heap.
    Instance public methods: heapify, insert_node, extract_root, sort, draw
    """
    def __init__(self, maxheap=False):
        """Min-heap is built by default. If maxheap param is set to True, then max-heap is created."""
        self.heap = []
        self.__heap_size = 0
        self.__compare = operator.lt if maxheap else operator.gt

    def __len__(self):
        return self.__heap_size

    def __getitem__(self, item):
        return self.heap[item]

    def __swap(self, idx1, idx2):
        self.heap[idx1], self.heap[idx2] = self.heap[idx2], self.heap[idx1]

    def heapify(self, alist):
        """Creates heap from an iterable."""
        for i in alist:
            self.insert_node(i)

    @staticmethod
    def get_children_idx(parent_idx):
        lvl = parent_idx * 2
        left_child_idx = lvl + 1
        right_child_idx = lvl + 2
        return left_child_idx, right_child_idx

    @staticmethod
    def get_parent_idx(child_idx):
        return (child_idx - 1) // 2

    def insert_node(self, node):
        """Inserts node. Bubble up. Follows min-heap or max-heap comparison rule,
        Depends on choice of instance self.__compare operator.
        """
        self.heap.append(node)
        self.__heap_size += 1
        child_idx = self.__heap_size - 1
        while True:
            parent_idx = self.get_parent_idx(child_idx)
            if not self.__compare(self.heap[parent_idx], node) or parent_idx < 0:
                break

            self.__swap(child_idx, parent_idx)
            child_idx = parent_idx

    def extract_root(self):
        """Extracts min or max node. Bubble down. Checks if a child index is not
        out of the heap range when walking down. Nodes swap is based on result of
        comparing parent and child points. Comparison operator is defined at instance
        creation when choosing heap type (min-heap or max-heap).
        """
        if self.__heap_size > 1:
            self.__swap(0, self.__heap_size - 1)
            self.__heap_size -= 1
            root = self.heap.pop()
            parent_idx = 0
            while True:
                left_child_idx, right_child_idx = self.get_children_idx(parent_idx)
                if right_child_idx < self.__heap_size:  # Both children present
                    # Takes smaller child idx in a min-heap or larger child idx in a max-heap.
                    child_idx = right_child_idx if self.__compare(
                        self.heap[left_child_idx], self.heap[right_child_idx]) else left_child_idx

                    if self.__compare(self.heap[parent_idx], self.heap[child_idx]):
                        self.__swap(parent_idx, child_idx)
                        parent_idx = child_idx
                    else:
                        return root

                elif left_child_idx < self.__heap_size:  # Only left child present.
                    if self.__compare(self.heap[parent_idx], self.heap[left_child_idx]):
                        self.__swap(parent_idx, left_child_idx)
                    return root
                else:  # No children
                    return root

        if self.__heap_size == 1:
            self.__heap_size -= 1
            return self.heap.pop(0)

        raise IndexError("pop from empty heap")

    def sort(self):
        """Heap sort."""
        return [self.extract_root() for _ in range(self.__heap_size)]

    def draw(self, print_width=50, min_char_width=3):
        """Produces illustration of a graph. Space for points in stdout
        is strongly limited by print_width and min_char_width parameters.
        Graph list will be sliced in order to meet a space constraint.
        """
        from math import log

        limiter = 2 ** int(log(print_width // min_char_width, 2)) * 2 - 1
        sliced = self.heap[:limiter]
        levels = int(log(len(sliced), 2))
        for lvl in range(levels + 1):
            nodes_per_lvl = 2 ** lvl
            sidx = 2 ** lvl - 1
            eidx = sidx + nodes_per_lvl
            nodes = sliced[sidx:eidx]
            nodes += [''] * (nodes_per_lvl - len(nodes))

            width = print_width // nodes_per_lvl
            fmt = '{{:^{}}}'.format(str(width))
            fmt *= nodes_per_lvl

            print('{{:>{}}} '.format(print_width + 7).format('Level: ' + str(lvl)))
            print(fmt.format(*nodes))

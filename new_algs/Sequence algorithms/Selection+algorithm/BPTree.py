import pysnooper
from BPLeafNode import *


class BPTree(object):
    """
    A b+ tree class.

    Attributes:
        root: The root node of the Tree
        m: The order of the tree.
    """

    def __init__(self, m):
        self.root = None
        self.m = m

    def insert(self, index, datum):
        """
        Insert one record into the tree;
        Check the constraints and split when the leaf has more than m - 1 indices.
        """
        leaf = self.search(self.root, index)
        if isinstance(leaf, BPLeafNode):                # Duplicate keys, insert to data directly
            if index in leaf.indices:
                key = index
                position = leaf.indices.index(key)
                leaf.data[position].insert(key, datum[0])
            else:
                result = leaf.insert(index, datum)
                if isinstance(result, BPInterNode):
                    self.root = result

    def search(self, root, index):
        """ Search a leaf node for insertion by the index. """
        if not self.root:  # Create a leaf node when root doesn't exist
            self.root = BPLeafNode(m=self.m)
            return self.root

        if isinstance(root, BPLeafNode):  # Terminate at the leaf node
            return root

        min_index, max_index = root.indices[0], root.indices[-1]
        if index < min_index:
            return self.search(root.children[0], index)
        elif index > max_index:
            return self.search(root.children[-1], index)
        for i in range(len(root.indices)):  # -1
            # if root.indices[i] <= index < root.indices[i + 1]:
            #     child_index = i + 1
            #     return self.search(root.children[child_index], index)
            if index <= root.indices[i]:
                child_index = i + 1
                return self.search(root.children[child_index], index)

    @staticmethod
    def traversal(root):
        print("Traversal!")
        queue = [root]
        while len(queue) != 0:
            head = queue[0]
            print(head.indices)
            if isinstance(head, BPLeafNode):
                print(head.data)
            if not isinstance(head, BPLeafNode):
                queue += head.children
            queue.pop(0)
        print()


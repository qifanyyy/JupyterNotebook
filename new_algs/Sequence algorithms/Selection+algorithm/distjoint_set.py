"""
@author: David Lei
@since: 20/10/2017

"""

class DistjointSetNode:
    def __init__(self, id, data):
        self.data = data
        self.parent = -1
        self.id = id   # Treat this as index.


class DistjointSet:

    def __init__(self, start_nodes=1):
        self.array = None

    def make_set(self, array, return_mapping=False):
        """Accepts an iterable of data elemetns and adds them into the distjoint set."""
        self.array = [DistjointSetNode(i, data) for i, data in enumerate(array)]
        if return_mapping:
            # The disjoint set is built on indexes so to merge things I need an index.
            # Return the mapping of data object to index which the DisjointSetNode.data points to for callers to use.
            mappings = {distjoint_set_node.data: i for i, distjoint_set_node in enumerate(self.array)}
            return mappings

    def _union_merge(self, smaller_root_index, larger_root_index):
        smaller_root_node = self.array[smaller_root_index]
        larger_root_node = self.array[larger_root_index]
        larger_root_node.parent += smaller_root_node.parent # Increment size of larger tree.
        smaller_root_node.parent = larger_root_node.id  # Point the smaller tree to the root of the larger.

    def union_by_size(self, node_a_index, node_b_index):
        """A really nifity trick we can do with distjoint sets is to store the number of elements in each
        set at the root node as a negative number. This won't effect the way we find parents and allows
        us to do unions by size faster.

        We add the smaller tree to the root of the larger as we want to minimize the max length in the tree
        to get from a child to the root.
        """
        a_root_index = self.find(node_a_index)
        b_root_index = self.find(node_b_index)

        if a_root_index == b_root_index:  # node_a and node_b already in the same set.
            return

        # Do union here.
        if abs(self.array[a_root_index].parent) >= abs(self.array[b_root_index].parent):  # tree_a > tree_b.
            self._union_merge(b_root_index, a_root_index)
        else:
            self._union_merge(a_root_index, b_root_index)

    def find(self, node_index):
        """Follows the chain of parent pointers all the way up until we reach a root (parent pointer -1).
        This parent will haven an id representing the set that it belongs to which is the id for the set.

        Returns:
            node_index: index for the root of the set, used to identify the set.
        """
        if self.array[node_index].parent < 0:
            return node_index  # Root of the set.
        # node_index is the index for the node, array[node_index] is my parent index.
        # so to find parent run .find() on array[node_index]
        return self.find(self.array[node_index].parent)

    def find_compressed(self, node_index):
        """Same as find() but flattens the structure whenever .find_with_path_compression() is used by
        making each node point directly to the root so you don't need to do the entire traversal.

        Returns:
            node_index: index for the root of the set, used to identify the set.
        """
        if self.array[node_index].parent < 0:  # Is root.
            return node_index
        root_index = self.find_compressed(self.array[node_index].parent)
        self.array[node_index].parent = root_index  # Make this node point to the root
        return root_index

if __name__ == "__main__":
    distjoint_set = DistjointSet()

    data_elements = ["A", "B", "C", "D", "E", "F"]  # These elements will be indexed in the distjoint set from 0 .. n - 1.
    distjoint_set.make_set(data_elements)
    distjoint_set.union_by_size(0, 1)  # Join A and B.
    distjoint_set.union_by_size(0, 2)  # Join A and C.
    distjoint_set.union_by_size(3, 5)  # Join D and F.

    sets = set()
    for i in range(6):
        set_id = distjoint_set.find_compressed(i)
        print("node_id: %s has data: %s belongs to set_id: %s with root: %s" %
              (i, distjoint_set.array[i].data, set_id, distjoint_set.array[set_id].data))
        sets.add(set_id)

    print("the sets we have are: " + str(sets))
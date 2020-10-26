"""
@author: David Lei
@since: 13/08/2017

https://www.hackerrank.com/challenges/binary-search-tree-lowest-common-ancestor/problem

The lowest common ancestor node in a BST for value1 and value2 is the node closest to value1 and value2 or the
first common node encountered when traversing from value1 up to the root and value2 up to the root.

This enforces a constraint that the lowest common ancestor is in the range
    [min(value1, value2), max(value1, value2)]
The question assumes that value1 can be the LCA of value1 and value2 if value1 is encountered on the path to value2.
This mean a node may be considered it's own ancestor, eg:

        4
    3
2

lca(2, 3) = 3
lca(2, 4) = 4
"""
import sys

# BST setup.

sys.path.append("../../../algorithms_datastructures/trees")  # Needed to import from another dir.

from algorithms_datastructures.trees.binary_search_tree import BinarySearchTree

node_values = [4, 2, 3, 1, 7, 6]

bst = BinarySearchTree()

for val in node_values:
    bst.insert(val)


print(bst.pre_order())

# LCA question.


def traverse_and_store_ancestors(value, start, ancestors):
    # Assumed start is in ancestors.
    # Value is guaranteed to be there so don't need to check nulls, nulls will only occur at a leaf.
    # If you are at a leaf you should have found value.
    current = start
    while True:
        # if current is None:
        #     return
        if current.key == value:
            ancestors.append(current)
            return
        if value < current.key:
            # Go left.
            ancestors.append(current)
            current = current.left
        else:
            # > Go right.
            ancestors.append(current)
            current = current.right


def lca(root, v1 , v2):
    v1_ancestors = []
    v2_ancestors = []
    traverse_and_store_ancestors(v1, root, v1_ancestors)  # O(h tree) = O(n) worst case
    traverse_and_store_ancestors(v2, root, v2_ancestors)  # O(h tree) = O(n) worst cas

    # Need for while loop as we are now appending the current node if it is one of the target values.
    # Where as in n^2 for loop it just compares everything.
    v1_ancestors.sort(key=lambda n: n.key, reverse=True)
    v2_ancestors.sort(key=lambda n: n.key, reverse=True)

    print("ancestors for value {0} are {1}".format(v1, [a.key for a in v1_ancestors]))
    print("ancestors for value {0} are {1}".format(v2, [a.key for a in v2_ancestors]))

    # Compare ancestor lists.

    # O(n + m) loop using pointers to check, better.
    # Loop backwards, ancestor lists sorted from highest to lowest.
    v1_index = len(v1_ancestors) - 1
    v2_index = len(v2_ancestors) - 1
    while True:
        if v1_ancestors[v1_index].key == v2_ancestors[v2_index].key:
            return v1_ancestors[v1_index]
        if v1_ancestors[v1_index].key > v2_ancestors[v2_index].key:
            # Make v2 catch up to v1 as v1 is bigger.
            # Reduce index to get ancestor to the left (bigger than right).
            v2_index -= 1
        else:
            v1_index -= 1

    # O(n^2) loop to check, not as good.
    # for v1_i in range(len(v1_ancestors) -1, -1, -1): # Loop backwards.
    #     for v2_i in range(len(v2_ancestors) - 1, -1, -1):
    #         if v1_ancestors[v1_i].key == v2_ancestors[v2_i].key:
    #             return v1_ancestors[v1_i]


v1 = 1
v2 = 7
print(lca(bst.root, v1, v2).key)
"""
@author: David Lei
@since: 13/08/2017

A BST holds the properties L < current < R.
The BST also must not contain duplicate values.

https://www.hackerrank.com/challenges/ctci-is-binary-search-tree/problem

An approach to each node  upholds the BST property with it's direct children is not enough as a tree witht he follow
configuration will be classed as valid.

1 2 4 3 5 6 7

          3
    2           6
1       4    5      7

Invalid because of 4.

Simply doing a check on nodes will not detect this.
Need to propagate up the max and min values.

A really easy approach is an in order traversal, copy and sort the results and compare.
"""

""" Dumber solution. TODO: Fix 7/14 test cases passed, I have a bug here somewhere."""

class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None



def check_node(node, fn):
    """Given a node, check it upholds the BST property with it's direct children.
    Then recurse down it's children to find the max and min values to ensure the BST property is upheld
    in subtrees.
    """
    if node.left is None and node.right is None:
        # Base case at leaf.
        return node.data

    left_max = None
    right_min = None

    if node.left is None or node.right is None:
        if node.left is None:
            if node.data < node.right.data:  # Check BST ordering.
                right_min = check_node(node.right, min)  # Propagate value up.
            else:
                right_min = False  # BST ordering violated.

        if node.right is None:
            if node.left.data < node.data:  # Check BST ordering.
                left_max = check_node(node.left, max)  # Propagate value up.
            else:
                left_max = False  # BST ordering violated.
    else:
        if node.left.data < node.data < node.right.data:  # Check BST ordering.
            left_max = check_node(node.left, max)  # Propagate value up.
            right_min = check_node(node.right, min)  # Propagate value up.
        else:
            left_max = False
            right_min = False

    if left_max is False or right_min is False:
        # BST property violated somewhere.
        return False

    values = [val for val in [left_max, right_min] if val is not None]
    return fn(values)  # Propagate value up.


def check(root):
    """Check a node and all it's children uphold the BST property.

    Does preliminary check that the root & it's children upholds the BST property, then calls () to recurse down each
    subtree from left to right, do the same check and propagate the boundary value up.
    Where the boundary value is defined
    """
    if not root.left and not root.right:
        return True  # Valid BST with 1 node.

    if not root.left or not root.right:
        # Only one child exists.
        if root.left:
            if not root.left.data < root.data:
                return False  # BST property violated on root's direct left child.
            left_max = check_node(root.left, max)
            return left_max < root.data
        if root.right:
            if not root.data < root.right.data :
                return False  # BST property violated on root's direct right child.
            right_min = check_node(root.right, min)
            return root.data < right_min
    else:
        # Both children exist.
        if not root.left.data < root.data < root.right.data:
            return False
        left_max = check_node(root.left, max)
        right_min = check_node(root.right, min)
        return left_max < root.data < right_min
    # Note: Might be an issue with the value 0.


root = Node(3)
left_child = Node(2)
left_left_leaf = Node(1)
left_right_leaf = Node(4)
right_child = Node(6)
right_left_leaf = Node(5)
right_right_leaf = Node(7)

root.left = left_child
left_child.left = left_left_leaf
left_child.right = left_right_leaf
root.right = right_child
right_child.left = right_left_leaf
right_child.right = right_right_leaf

""" Smarter Solution: Takes advantage of a BST needing to be in increasing order after an in order traversal.
Time complexity: O(n) for traversing tree with n nodes.
Space complexity: O(3n) store the n nodes in another array, then copy that and also use a set.
"""


def inOrderTraversal(node, data):
    if node.left:
        inOrderTraversal(node.left, data)
    data.append(node.data)
    if node.right:
        inOrderTraversal(node.right, data)


def checkBSTbetterButNotBest(root):
    tree_data_in_order = []
    inOrderTraversal(root, tree_data_in_order)
    sorted_data = tree_data_in_order[:]
    sorted_data.sort()
    if len(set(tree_data_in_order)) != len(tree_data_in_order):
        return False
    return sorted_data == tree_data_in_order

print(checkBSTbetterButNotBest(root))

""" Actual faster solution.
At the root the BST is valid, to the left of the root the values must be between negative infinity and the root.
To the right of the root the values must be between the root value until positive infinity. These ranges are exclusive
as this question has no duplicates.

Faster as can terminate at first occurance of an invalid range.

Time compexity: O(n) for number of nodes.
Space complexity: O(log n) as recursive.
"""

import math


def checkBstWithRange(node, min_val, max_val):
    if node is None:
        return True

    left_is_fine = True
    right_is_fine = True

    if node.left:
        # Anything to left of node must be between min_val and node.data
        left_is_fine = checkBstWithRange(node.left, min_val, node.data)

    if node.right:
        # Anything to the right of the node must be between node.data and max_val.
        right_is_fine = checkBstWithRange(node.right, node.data, max_val)
    # print("for node val: {0}, left is fine: {1}, right is fine: {2}".format(node.data, left_is_fine, right_is_fine))
    # print("Bounds: min = {0}, max = {1}".format(min_val, max_val))
    if not (left_is_fine and right_is_fine):
        return False
    return min_val < node.data < max_val


def checkBST(root):
    return checkBstWithRange(root, math.inf * -1, math.inf)

print(checkBST(root))
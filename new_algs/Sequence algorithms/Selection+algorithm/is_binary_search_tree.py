"""
@author: David Lei
@since: 6/11/2017

https://www.hackerrank.com/challenges/is-binary-search-tree/problem

Check if a binary tree is a binary search tree.

Idea: It is not enough to just check for every subtree L < root < R because you can have the case of.

         5
       /   \
      3     8
     / \   / \
    1  6  2  10

Where each triple has L < root < R but the overall structure doesn't.
So I should return the maximum value on the left subtree and the smallest value on the right subtree so I can check
the overall structure of the tree.

Note: Dealing with strictly < and >, won't have duplicate values.

Note: A really smart soln is do an in order traversal and sort and then check if traversal == sorted.
"""
def in_order(node, arr):
    if node.left:
        in_order(node.left, arr)
    arr.append(node.data)
    if node.right:
        in_order(node.right, arr)

def cheecky_soln(root):
    values = []
    in_order(root, values)
    sorted_values = list(set(values[::]))
    sorted_values.sort()
    return values == sorted_values

def check_structure(node, want_max=False):  # This only passes 11/13 test cases, not too sure why it fails but im running out of time :(
    if not node.left and not node.right:  # At a leaf, leaf maintains BST ordering.
        return node.data

    # want_max = True to return max value as looking at left subtree.
    # else want_max = False to return smallest looking at right subtree.

    # Check the immediate tree with L and R data values.
    max_left, min_right = None, None
    if node.left:
        if not node.left.data < node.data:
            return False
        max_left = check_structure(node.left, want_max=True)
        if not max_left:
            return False
        if not max_left < node.data:
            return False
    if node.right:
        if not node.right.data > node.data:
            return False
        min_right = check_structure(node.right, want_max=False)
        if not min_right:
            return False
        if not min_right > node.data:
            return False
    if want_max:
        return max(max_left if max_left else 0, min_right if min_right else 0, node.data)
    else:
        # Can use 1000000000 as max data value is bounded by 10^4.
        return min(max_left if max_left else 1000000000, min_right if min_right else 1000000000, node.data)


def check_binary_search_tree_(root):
    valid = check_structure(root)
    if not valid:
        return False
    return True


if __name__ == "__main__":
    # Testing.
    class Node:
        def __init__(self, data, l, r):
            self.data = data
            self.left = l
            self.right = r

    one = Node(1, None, None)
    four = Node(4, None, None)
    five = Node(5, one, four)
    six = Node(6, None, None)
    two = Node(2, six, None)
    root = Node(3, five, two)

    print(check_binary_search_tree_(root))
"""
@author: David Lei
@since: 6/11/2017

https://www.hackerrank.com/challenges/tree-level-order-traversal/problem

A level order traversal visits nodes at each level from left to right.

Passes :)
"""

def preorder(node, arr): # Won't work.
    arr.append(node.data)
    if node.left:
        preorder(node.left, arr)
    if node.right:
        preorder(node.right, arr)

from collections import deque

def levelOrder(root):
    # idea: to do things per level we need to look at the left and right child, process their data elements in check their children.
    #   can't just a preorder traversal as that will append any left nodes and their children before right nodes meaning
    #   it might go deeper than the current level.
    #   Since we need to process by levels we can use a queue and append to it as we encounter left and right children
    #   while taking the value from the root.
    data = []
    q = deque([root])
    while q:
        node = q.popleft()
        data.append(str(node.data))
        # Process children at this level.
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)
    print(" ".join(data))

    # Will always process a single level first as it starts with the root node.
    # then the two children of the root are appended. Those values are added to data
    # before any of their children are processes due to the FIFO nature of the queue.

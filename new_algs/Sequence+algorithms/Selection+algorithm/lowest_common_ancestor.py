"""
@author: David Lei
@since: 6/11/2017

https://www.hackerrank.com/challenges/binary-search-tree-lowest-common-ancestor/problem

LCA is the first ancestor of 2 noes when traversing back up to the root, it might be one of those ndoes.

It is guaranteed v1 and v2 are in the tree.

Passes :)
"""

def dfs(node, parents, goal): # O(n) traversal, O(n) space for array.
    if node.data == goal:
        parents.append(node)  # Allows a node to be a lca.
        return True
    parents.append(node)
    if node.left:
        if dfs(node.left, parents, goal):
            return True
    if node.right:
        if dfs(node.right, parents, goal):
            return True
    parents.pop()

def lca(root, v1, v2):  # Passes.
    # O(5n) time.
    # O(n) space.
    # Idea: can find node v1 and v2 and their paths and return the first common parent.
    path1 = [] # O(n) space.
    dfs(root, path1, v1) # O(n).
    path2 = [] # O(n) space.
    dfs(root, path2, v2) # O(n).
    path1 = path1[::-1] # O(n).
    path2 = set(path2) # O(n).
    for ancestor in path1: # O(n).
        if ancestor in path2: # O(1) amortized, O(n) worst.
            return ancestor


# Better solution by: https://www.youtube.com/watch?v=bl-gwEwm8CM&ab_channel=SmithaMilli
def lca_better(root, v1, v2):  # Passes.
    # O(n) time, only 1 traversal.
    # O(1) space, just a few pointers.
    # idea: if a goal node is found in the left and right subtrees in this recursive call then we know that the root is the LCA be definition.
    #   otherwise the goal node must have been found in a recursive call later in which case the first goal node encountered is returned.
    #   Eg:
    #           10
    #         /   \
    #        5     8
    #       / \     \
    #      9   3     4
    # Note: rec(n) means recursive call at n where n was the root.
    # Goals(9, 3) then 5 is the root and that will be returned up to rec(10), goal_in_left will be false, so return 5 as answer.
    # Goals(5, 4) at rec(5) 5 is returned, rec(8) calls rec(4) which returns 4, goal_in_left/right will be non falsy so return 10.
    # Goals(5, 3) at rec(5) 5 is returned, rec(8) returns false. This means that the right subtree of rec(10) is false so the goals
    #   must be in the left subtree. The first goal encountered in the left subtree is 5 so that must be the LCA as it is the
    #   lowest possible node to have 3 as a child also including 5 (itself). So return it up.
    #
    # Insight 1: if a goal node is found on left AND right then this node is LCA.
    # Insight 2: if a goal node is found, return that up as it must he the LCA if the other goal is somewhere in it's subtree
    #   else it will return a positive value to a caller who will get another positive value from a right call resulting in insight 1.
    # Insight 3: it is ok to not look for the 2nd goal node if the first is found due to insight 2, only need to check on the right of callers
    #   and if not found means the first is the LCA.
    if root is None:
        return None
    if root.data == v1 or root.data == v2:
        return root
    goal_in_left = lca_better(root.left, v1, v2)
    goal_in_right = lca_better(root.right, v1, v2)
    if goal_in_left and goal_in_right:
        return root  # Worst case will return the root of the tree.
    if goal_in_left:
        return goal_in_left
    if goal_in_right:
        return goal_in_right
    return False


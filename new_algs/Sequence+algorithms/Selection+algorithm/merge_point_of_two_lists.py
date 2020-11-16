"""
@author: David Lei
@since: 6/11/2017

https://www.hackerrank.com/challenges/find-the-merge-point-of-two-joined-linked-lists/problem

Given two lists guaranteed to converge (have same value) find when this occurs.
Return the data at the node where this occurs.

Both pass :)
"""
def FindMergeNodeBetter(headA, headB):
    # Space = O(1)
    # Time = O(a + b)
    # Idea: Since it is guaranteed to converge for pair of lists A and B with merge points a in list A
    #   and b in list B. In the worst case they are the ends of both lists and both lists are different lengths.
    #   If you join A and B and B and A then iterate through them you can find the point where the first common value occur.
    #   For example:
    #       A = [a, b, c, d, e]
    #       B = [k, i, e]
    #           a = e, b = e
    #           A' = A + B = [a, b, c, d, e, k, i e]
    #           B' = B + A = [k, i, e, a, b, c, d, e]
    #      A = [a, b, c, e, f, g]
    #      B = [z, f, g]
    #           a = f, b = f
    #           A' = A + B = [a, b, c, e, f, g, z, f, g]
    #           B' = B + A = [z, f, g, a, b, c, e, f, g]
    #    The same number of steps is required weather you traverse A first or B to find the common node to merge from.
    #    Instead of making new list using extra space, you can just start the traversal from the head of the other list
    #    when the current list is out of nodes.
    a = headA
    b = headB
    while True:
        if a.data == b.data: # Guaranteed.
            return a.data
        # Handles starting traversal from other list.
        a = a.next if a.next else headB
        b = b.next if b.next else headA
    # Note: If convergence is not guaranteed then can stop if iterations exceed len(a) + len(b).

def FindMergeNodeNaive(headA, headB):
    # Naive solution
    # Space = O(a + b)
    # Time = O(a + b + a)
    a_values = set() # O(len(a)) space.
    b_values = set() # O(len(b)) space.
    while headA: # O(len(a)).
        a_values.add(headA.data) # O(1) amortized, O(n) worst.
        headA = headA.next
    while headB: # O(len(b)).
        b_values.add(headB.data) # O(1) amortized, O(n) worst.
        headB = headB.next
    for i in a_values:
        if i in b_values:  # O(1) amortized, O(n) worst.
            return i


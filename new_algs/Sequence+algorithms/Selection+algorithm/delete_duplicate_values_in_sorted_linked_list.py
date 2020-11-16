"""
@author: David Lei
@since: 6/11/2017

https://www.hackerrank.com/challenges/delete-duplicate-value-nodes-from-a-sorted-linked-list/problem

Given a head pointer to a sorted linked list remove duplicates.

Passed :)
"""

def RemoveDuplicates(head):
    if not head:
        return None
    cur = head
    while cur:
        if not cur.next:  # Comparing last node with NULL, good I picked out this edge case :).
            break
        if cur.data == cur.next.data:
            cur.next = cur.next.next # Skip over 1 node with same value.
        else:
            cur = cur.next
    return head
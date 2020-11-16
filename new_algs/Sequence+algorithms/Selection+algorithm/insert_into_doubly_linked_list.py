"""
@author: David Lei
@since: 6/11/2017

https://www.hackerrank.com/challenges/insert-a-node-into-a-sorted-doubly-linked-list/problem

Given the head to a sorted doubly linked list, insert data into it while maintaining order.
Return the head of the updated list

Passed :)
"""

class Node(object):

   def __init__(self, data=None, next_node=None, prev_node = None):
       self.data = data
       self.next = next_node
       self.prev = prev_node

# I need to think about edge cases more!!!.

def SortedInsert(head, data):
    # Edge case 1: insert at start of list, need to return new head.
    if data < head.data: # New head.
        new_node = Node(data, head, head.prev)
        head.prev = new_node
        return new_node

    # Expected case, insert into body of list.
    cur = head
    while cur.data < data:
        # If cur.next is None then we need to insert to the end of the list.
        if not cur.next:
            # Edge case 2: insert to end of list, need to catch this will lead to an error if you keep iterating.
            new_node = Node(data, cur.next, cur)
            cur.next = new_node
            return head
        cur = cur.next
    # At a node >= to data.
    # Set prev to point to new node, new node to point to cur and back to prev, cur to point to new node.
    new_node = Node(data, cur, cur.prev)
    cur.prev.next = new_node
    cur.prev = new_node
    return head



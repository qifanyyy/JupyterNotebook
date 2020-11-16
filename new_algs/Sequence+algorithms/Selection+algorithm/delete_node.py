"""
@author: David Lei
@since: 5/11/2017

https://www.hackerrank.com/challenges/delete-a-node-from-a-linked-list/problem

Passed :)
"""

def Delete(head, position):
    # position guaranteed to be in range of the list.
    if position == 0:  # Remember to handle the edge cases.
        return head.next
    node = head
    for i in range(position - 1):
        # Want to end the loop right before you need to remove the node.
        # So loop until the position - 1th node.
        node = node.next
    node.next = node.next.next
    return head
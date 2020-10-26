"""
@author: David Lei
@since: 5/11/2017

https://www.hackerrank.com/challenges/detect-whether-a-linked-list-contains-a-cycle/problem

A cycle exists if any node is visited once during traversal.

Both Passed :)
"""

def has_cycle_better(head): # a.k.a floyd cycle detection, hare & turtle.
    # Idea: if a cycle exists then you won't be able to finish the traversal,
    #   it also means that if you have 2 pointers going at different speeds/steps that
    #   they will keep on going until they are both the same node.
    #   else if it has no cycles then both will finish fine.
    # Space complexity: O(1) don't store extra space, store an extra node.
    # Time complexity: O(n)
    #   best case where list has no loops O(n/2) = O(n) as b will traverse 2 nodes every time so you reach
    #       the last node in n/2 time at which b = None and the while loop will exit.
    #   worst case where loop exists, both a and b will be stuck in the loop until a == b.
    #       a will traverse the list at most just once, at which it will collide with b. so O(n).
    #   Informal complexity proof:
    #       consider a portion of a linked list where the slower pointer is the tortoise (t) and faster is the hare (h).
    #       since h moves faster than t, when t enters the loops h is already in it, this means h is coming from behind
    #       and can only catch up to t.
    #       h can either be an odd or even distance behind t.
    #       - simplest even distance is 2 spaces behind t:
    #               ..h.t..
    #           at the next step t will move forward one and h will move forward two resulting in
    #               ....ht. where h is 1 behind t
    #       - simplest odd distance is 1 space behind t:
    #               ....ht.
    #           at the next step t will move forward one and h will move forward two resulting in
    #               ......t
    #                     h
    #           they will meet.
    #       any other configuration in the loop simplifies to one of the above eg: if h it 3 spaces behind t then at the next
    #       step it will be two spaces behind t and so forth. Each iteration leads to h becoming 1 step closer to t.
    #   Inside the loop:
    #       In the best case when t enters the loop h is 1 node behind it at which it will catch t at the next step.
    #       In the worst case when t enters the loop h is one step ahead of it. That also means at this point
    #       there are n-1 nodes from h to t going forwards. Since h can catch up by 1 node at each step h will catch up to
    #       in the next n-1 iterations, and thus h wil always catch t before t finishes traversing the loop.
    #       At most t can go through every item in the loop, so at worst where the entire list forms a circle and there are n
    #       elements in the loop and t starts at the head and h starts at head.next (1 node ahead of t) t will only go to
    #       n nodes (n-1 links),  thus this is O(n).
    tortoise = head
    hare = head.next
    # Test case I missed if head points to head, I had if a == b and a != head so it looped forever.
    #   instead of checking that a and b are not both head like that I should start b as head.next so if they both
    #   end up pointing to head again there must be a cycle.
    #   Also if head.next is None then the list only has head and the while loop won't execute so that is fine.
    while tortoise and hare and hare.next: # if not any of these conditions then at least one of them is a, probs b.next meaning the list has been traversed.
        # print("a data: %s" % (a))
        # print("b data: %s" % (b))
        if tortoise == hare:  # Cycle
            return True
        tortoise = tortoise.next
        hare = hare.next.next
    return False

def has_cycle_naive(head): # Passes.
    # Store a reference to each node so you can check against it O(n) space.
    nodes_seen = set() # O(n) space.
    while head is not None: # O(n) time.
        if head in nodes_seen: # ~ O(1) time, worst case is O(n).
            return True
        nodes_seen.add(head)
        head = head.next
    return False

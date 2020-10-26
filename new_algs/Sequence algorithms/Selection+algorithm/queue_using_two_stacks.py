"""
@author: David Lei
@since: 7/11/2017

https://www.hackerrank.com/challenges/queue-using-two-stacks/problem

Queue is FIFO, stack is LIFO

Process q queries of 3 types:
1. enqueue element to end of queue
2. deque element at front of queue
3. print element at front of queue

Stacks have the oldest item at the bottom and newest item at the top.
- quick pop() but only in LIFO ordering
- quick push()

If we want to dequeue (get the oldest item) in a FIFO manner we need to pop all items
off the stack and find the last item.

If you reverse a stack it will have a FIFO order.

Quick deque requires a stack with FIFO ordering.
Quick enqueue requires a stack with LIFO ordering.

So we can enqueue quickly by simply pushing.
For deque we need a FIFO implementation. You can get this by popping from the
LIFO stack and adding it into a FIFO stack meaning the last item in LIFO (oldest/first item)
is on top of the FIFO stack.

Passed :)
"""

class QueueWithStacks:
    # Same complexity with stack apart from when _process_fifo_stack() called which at worst is O(n).
    def __init__(self):
        self.lifo_stack = []
        self.fifo_stack = []

    def enqueue(self, item):
        self.lifo_stack.append(item)

    def peak(self):
        self._process_fifo_stack()
        return self.fifo_stack[-1]

    def dequeue(self):
        self._process_fifo_stack()
        return self.fifo_stack.pop()

    def _process_fifo_stack(self):
        # Only need to shift elements if fifo stack is empty.
        if self.fifo_stack:
            return  # Already have fifo things, 1 peak/pop operation is fine.
        while self.lifo_stack:
            item = self.lifo_stack.pop()
            self.fifo_stack.append(item)

q = int(input())

queue = QueueWithStacks()

for _ in range(q):
    query = [int(x) for x in input().split()]
    if query[0] == 1:
        queue.enqueue(query[1])
    elif query[0] == 2:
        queue.dequeue()
    else:
        print(queue.peak())
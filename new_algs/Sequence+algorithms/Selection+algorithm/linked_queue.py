"""
@author: David Lei
@since: 25/08/2016
@modified: 

Supporting data structure for BFS

    [item, next] --> [item, next] --> [item, next]
front (deque from here)           end (enqueue from here)
"""
class LinkedNode:
    def __init__(self, item=None, next=None):
        self.item = item
        self.next = next
        self.back = None

class LinkedQueue:
    def __init__(self):
        self.front = None
        self.end = None

    def is_empty(self):
        return self.front == None

    def enqueue(self, x):
        new_node = LinkedNode(x)
        if self.is_empty():
            self.front = new_node
        else:
            self.rear.next = new_node   # self.rear will point at the last node
        self.rear = new_node            # always points at last item

    def deque(self):
        if not self.is_empty():
            item = self.front.item
            self.front = self.front.next
            if self.is_empty():
                self.rear = None        # just insace this is the last element, rear will still point to it w/o this
            return item
        raise Exception

    def get_items(self):
        items = []
        current = self.front
        while current is not None:
            items.append(current.item)
            current = current.next
        return items


    def to_doubly_linked_list_reversed(self, node, parent):
        """The queue structure is node -nextlink-> node.
        This will mutate the queue.

        This is just an exercise and probably is a very un-useful method in a queue.

        Reverse this so the the back link points to the next link and the next link points to the parent instead of the child
        starting from the front node.
        """
        first = node
        if node:
            node.back = node.next
            node.next = parent
            _, last = self.to_doubly_linked_list_reversed(node.back, node)
            if last is None:
                last = node
            return first, last
        return None, None

if __name__ == "__main__":
    q = LinkedQueue()
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(5)
    q.enqueue(6)
    q.enqueue(7)
    q.enqueue(8)
    q.deque()
    print(q.get_items())

    values_first = []
    values_last = []

    first, last = q.to_doubly_linked_list_reversed(q.front, None)
    if first:
        # This is the first node, can use .back to traverse the queue.
        current = first
        while current:
            values_first.append(current.item)
            current = current.back
        print(values_first)

    if last:
        # This is the last node, can use .next to get to parents.
        current = last
        while current:
            values_last.append(current.item)
            current = current.next
        print(values_last)

    if values_first and values_last:
        print("Correct: %s" % (values_first == values_last[::-1]))

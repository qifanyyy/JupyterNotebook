"""
@author: David Lei
@since: 25/08/2016
@modified: 

Supporting data structure for DFS

Note: implementation slightly different to linked queue/list

    [item, next] <-        [item, next] <-       [item, next] <- top points to last node
           ^       |_______________|      |______________|
           |
None ------

we only need to store top, each node's next points to the node before it (allows for easy implementation of pop)
if top is None stack is empty
"""
# supporting structures

class LinkedNode:
    def __init__(self, item=None, next=None):
        self.item = item
        self.next = next

class LinkedStack:
    def __init__(self):
        self.top = None
        self.count = 0

    def is_empty(self):
        return self.top == None

    def push(self, x):
        self.count += 1
        current_top_node = self.top
        new_node = LinkedNode(x, current_top_node)  # new node has item x and points to old top (current_top)
        self.top = new_node                         # old top points to new node which is the top of the stack

    def pop(self):
        self.count -= 1
        if not self.is_empty():
            item = self.top.item                    # item to return
            self.top = self.top.next                # points to previous link
            return item
        raise Exception

    def to_doubly_linked_list_reversed(self, node, parent):
        """The stack structure is node -nextlink-> node where .next points to an item the current node is sitting on top.

        This will mutate the stack.

        This is just an exercise and probably is a very un-useful method in a stack.

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

class Node:
    def __init__(self, item=None, next=None):
        self.item = item
        self.next = next

if __name__ == '__main__':
    linkedStack = LinkedStack()

    linkedStack.push(8)
    linkedStack.push(9)
    print(linkedStack.pop())
    print(linkedStack.pop())
    # assertion error
    #print(linkedStack.pop()

    #linkedStack.reset()
    linkedStack.push(11)    # next
    linkedStack.push(12)    # next
    linkedStack.push(13)    # top
    #print(linkedStack.nextDOTnext())
    print(linkedStack.pop())

    def reverse(string):
        stack = LinkedStack()

        for i in string:
            stack.push(i)

        output = ""

        while not stack.is_empty():
            output += stack.pop()
        return output
    print(reverse('helloworld'))

    linkedStack.push(15)  # Stack has 4 items.
    linkedStack.push(100)
    values_first = []
    values_last = []

    first, last = linkedStack.to_doubly_linked_list_reversed(linkedStack.top, None)
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

### For creating paths in optimization algorithm ###


def make_path(current, source, predecessor):

    # Create path for flow
    path = DoublyLinkedList()
    path.append(current)

    # current node is a Node instance
    current_node = path.head

    if current_node.data == source:
        return path

    path.append(predecessor[current_node.data])

    if current_node.next:
        while current_node.next.data != source:
            ancestor = predecessor[current_node.next.data]
            path.append(ancestor)
            current_node = current_node.next

    return path


class Node(object):

    def __init__(self, data, prev, next):
        self.data = data
        self.prev = prev
        self.next = next

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<node:{}>".format(self.data)


class DoublyLinkedList(object):

    head = None
    tail = None

    def append(self, data):
        new_node = Node(data, None, None)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            new_node.next = None
            self.tail.next = new_node
            self.tail = new_node

    def print_list(self):
        print ("Doubly linked list:")
        current = self.head
        while current:
            if current == self.head:
                print (current.prev)
            print (current.data)
            if current == self.tail:
                print (current.next)

            current = current.next


###############################################
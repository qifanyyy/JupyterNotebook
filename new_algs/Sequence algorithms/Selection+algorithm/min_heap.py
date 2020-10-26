"""
@author: David Lei
@since: 17/10/2017

"""

class MinHeap:
    """A min heap/priority queue class.
    Uses the heap implementation based on an array. Index 0 is blank, the root is at index 1.
    The children of the root are at indexes 1 * 2 + 1 and 1 * 2. Their respective children follow the same formula.
    The parent of a child is at the child index // 2.
    Eg:
        index: 0, 1, 2, 3, 4, 5
        array: -, A, B, C, D, E

    The root is A, it's children are 1 * 2 (2 = B)  & 1 * 2 + 1 (3 = C).
    D is the child of B, it's parent is 4 // 2 = 2.
    E is the child of B, it's parent is 5 // 2 = 2.

    Heap properties:
        - Shape property: is a complete binary tree meaning all levels of the tree, except possibly the last one (deepest) are fully filled, and, if the last level of the tree is not complete, the nodes of that level are filled from left to right.
        - Heap property: the key stored in each node is either <= tothe keys in the node's children.
    """
    def __init__(self):
        self.count = 0
        self.array = [None]

    def heapify(self, array):
        """O(n) heapify.
        Only sink down the nodes that we need to.
        We don't need to deal with leaves so given the input array with length n we only care about the first 1 .. n // 2 nodes.
        The last n // 2 .. n nodes are most likely leaves.
        So we only need to sink down the the first 1 .. n // 2 elements.
        We need to do this smartly as if we start at index 1 (the root) it will assume sub heaps encountered uphold the heap property,
        thus we must start from n // 2 and go up to 1 to ensure all sub heaps are fixed before fixing sub heaps from a higher level.

        This works as leaves are valid heaps, because they are filled out from left to right we can kinda ignore the last n // 2 elements as they are
        all leaves. So we then get the parents of these sub heaps and make sure they upload the heap property and do this from n // 2 until the root.

        A complete binary tree with height h (root has h = 0) has at max (n + 1)//2 leaves, where n is the number of nodes and 2^(h + 1) -1 nodes.
        """
        self.array = array[::]
        self.array.insert(0, None)
        self.count = len(array)
        i = (len(array) + 1) // 2  # Only sink nodes at index (n + 1) // 2 up until 1 ensuring all sub heaps upload heap property.
        log_n_calls = 0
        while i > 0:
            self.filter_down(i)
            i -= 1
            log_n_calls += 1
        return log_n_calls

    def is_empty(self):
        return self.count == 0

    def add_item(self, item):
        if self.count + 1 < len(self.array):
            self.array[self.count + 1] = item
        else:
            self.array.append(item)
        self.count += 1
        self.filter_up(self.count)

    def get_parent(self, i):
        """Returns the parent index of the node at index i."""
        return i // 2

    def get_children(self, i):
        """Returns the indexes for the left and right children of the node at index i."""
        if i * 2 > self.count:  # No children possible.
            return None, None
        return i * 2, i * 2 + 1

    def get_smallest_child(self, i):
        """Return the index of the smaller child of index i.
        We need the heap to maintain the property parent <= children, so as long as the parent is <= to it's smallest child we are fine."""
        left, right = self.get_children(i)
        if self.count == left:  # The length of the array only allows for the left child.
            return left
        if self.array[left] <= self.array[right]:
            return left
        return right

    def filter_up(self, i):  # O(log n).
        """Rise an item at index i to it's correct position in the heap.
        The heap property enforces that the parents key is <= it's children."""
        while i > 1 and self.array[i] < self.array[self.get_parent(i)]:  # Violates parent <= children.
            self.array[i], self.array[self.get_parent(i)] = self.array[self.get_parent(i)], self.array[i]
            i = self.get_parent(i)  # Now looking at the parent (where we moved node i to).
        # Exists loop when the child is >= to the parent meaning the parent is <= to the child.

    def filter_down(self, i): # O(log n).
        """Sink node at index i down to it's correct position enforcing heap property child <= parent."""
        while 2 * i <= self.count:  # self.count will hold the number of elements in the array, will be either 2 * i or 2 * i + 1 from the lowest parent node.
            # Node i can have children.
            smaller_child_index = self.get_smallest_child(i)
            if self.array[i] <= self.array[smaller_child_index]:  # Heap property is maintained.
                break
            # Swap child and parent to maintain heap property.
            self.array[i], self.array[smaller_child_index] = self.array[smaller_child_index], self.array[i]
            # The child that was < the parent is moved up, so the parent is in the place of the child. Move the parent down.
            i = smaller_child_index

    def get_min(self):
        """Return the min item at the root, does so by swapping root element with last element and then sinking that."""
        root_element = self.array[1]
        self.remove(1)
        return root_element

    def peak(self):
        """Look at smallest item in heap without modifying heap."""
        return self.array[1]

    def remove(self, i):
        # Swap the item at index i with the last item.
        self.array[i], self.array[self.count] = self.array[self.count], self.array[i]
        self.array[self.count] = '?'  # Place holder for removing an element.
        self.count -= 1
        self.filter_down(i)  # Filter down the item moved to index i.

    def print_heap(self, i):
        """Print contents of heap from parent to left then right in form (parent, l: left, r: right)."""
        left, right = self.get_children(i)
        s = "p: %s, l: %s, r: %s" % (self.array[i],
                                  self.array[left] if left and left <= self.count else "-",
                                  self.array[right] if right and right <= self.count else "-")
        print(s if i == 1 else "- %s" % s)
        if left and left <= self.count:
            self.print_heap(left)
        if right and right <= self.count:
            self.print_heap(right)

if __name__ == "__main__":
    pq = MinHeap()
    items = [1, 0, 10, -3, 4, -2, 1, 3, 2, 1, 4, 6, 8, 10, -1, -4, -5, -6, 19, -62, 50, 1, 0, 0]
    for item in items:  # O(n log n) heapify.
        pq.add_item(item)

    items.sort()

    output = []
    for _ in range(len(items)):
        output.append(pq.get_min())

    print("Sorted from heap: {0}, items: {1}".format(items == output, output))

    for item in items:  # Add back into heap.
        pq.add_item(item)

    for _ in range(3):
        print("Extracted min: " + str(pq.get_min()))
        print("Array looks like: " + str(pq.array))

    things_to_add = [100, -100, -50, -40, -60]
    for item in things_to_add:
        pq.add_item(item)
        print("Added item: " + str(item))
        print("Array looks like: " + str(pq.array))

    pq.print_heap(1)

    items.extend(items[::-1])
    print("~~ Testing O(n) heapify")
    log_n_calls = pq.heapify(items)
    print("O(n) heapify number of log(n) calls: {0} for array of length {1}".format(log_n_calls, len(items)))
    print(pq.array)
    pq.print_heap(1)

    sorted_elements = pq.array[::][1:]
    sorted_elements.sort()

    output = []
    for _ in range(pq.count):
        output.append(pq.get_min())

    print(sorted_elements == output)
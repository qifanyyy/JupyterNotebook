"""
@author: David Lei
@since: 7/11/2017

Given an array of n items, use a heap to return the d closest (smallest) value to t.
So you can return the d closest in O(n) time.

Assume that all inputs are positive integers so can turn it into a max heap by multiplying by -1.

Good source: https://www.youtube.com/watch?v=eaYX0Ee0Kcg&ab_channel=CSDojo

Other approaches:
- sort and return first d = O(n log n) time.
- selection sort = O(nk)
- quick select = O(n^2) worst
- heap = O(d + (n - d) * log d)
"""

from algorithms_datastructures.heaps.min_heap import MinHeap

def d_smallest_items(array, d): # O(d * log d + (n - d) * 2 log d + d)
                                # O(d + (n - d) * log d) if linear heapify.
    max_heap = MinHeap()

    # Create a min heap with d elements.
    for i in range(0, d): # O(d * log d), can do better with linear heapify but then you need to pass down an array of size d.
        max_heap.add_item(array[i] * - 1)

    # For each other element in the array.
    for i in range(d, len(array)): # O(n - d) * 2 log d
        max_value = max_heap.peak() * -1 # O(1).
        if array[i] < max_value: # O(1).
            #  Keep the d smallest items in the heap.
            max_heap.get_min()  # O(log d) Actually get max as we implement by * -1.
            max_heap.add_item(array[i] * -1) # O(log d)

    # Print the items in the heap, don't need to do so in sorted order.
    print(max_heap.array)
    for item in max_heap.array: # O(d)
        if item is not None:
            print(item * -1)

array = [4, 1, 5, 2, 3, 0, 10]
d_smallest_items(array, 5)




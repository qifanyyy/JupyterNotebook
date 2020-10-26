"""
@author: David Lei
@since: 13/08/2017

https://www.hackerrank.com/challenges/ctci-find-the-running-median/problem
https://www.hackerrank.com/challenges/find-the-running-median/problem

The median is the middle number of an array (middle index) or if the array has an even number of items the average of
the two middle numbers.

Brute force: Keep sorted array is O(n^2)

Smart approach: Keep 2 heaps, one that keeps track of the first half of the elements in the array with another
doing the opposite.

Keep a max heap of the lower half of the numbers.
Keep a min heap of the upper half of the numbers.

This allows us to get the median number quickly in log n time.

Size of the heaps also shouldn't differ by more than 1.

There are only positive numbers.

Pythons's heapq should allow O(log n) operations and O(1) loop up of smallest item (heap_array[0]).
"""
import heapq
# Note: heapq is a min heap.

upper_half_min_heap = []
lower_half_max_heap = []
# To maintain a max heap need to times values by -1 so biggest becomes smallest which will sit at the top of the heap.


def add_number_to_heap(num):
    """Adds a number to a heap, assuming the heaps correctly represent the lower half of numbers and the upper half.
    So the only factor taken into account is the number of items in the heaps.
    If same number of items add to lower half, else add to half with the least number of items.
    """
    if len(lower_half_max_heap) == 0:
        heapq.heappush(lower_half_max_heap, num * -1)
    elif len(upper_half_min_heap) == 0:
        heapq.heappush(upper_half_min_heap, num)
    else:
        # Assume the heap is a valid split of the data.
        # Difference will be positive if upper_half_min_heap has more elements, else negative.
        difference = len(upper_half_min_heap) - len(lower_half_max_heap)
        if difference >= 1:
            # upper_half_min_heap has more elements, should put this next number in lower_half_max_heap.
            heapq.heappush(lower_half_max_heap, num * -1)
        elif difference <= -1:
            # lower_half_max_heap has more elements, should put this next number in upper_half_min_heap.
            heapq.heappush(upper_half_min_heap, num)
        else:
            # Can push to either, difference is 0.
            heapq.heappush(lower_half_max_heap, num * -1)


def rebalance_heaps():
    """Ensures that no element in the upper half is less than any element in the lower half."""
    if not (len(lower_half_max_heap) >= 1 and len(upper_half_min_heap) >= 1):
        return  # Don't need to rebalance if one of them is empty.

    max_from_lower_half = lower_half_max_heap[0] * -1
    min_from_upper_half = upper_half_min_heap[0]

    if min_from_upper_half < max_from_lower_half:
        # Upper half has smaller elements than that of lower half.
        while min_from_upper_half < max_from_lower_half:
            # Swap elements.
            max_from_lower_half = heapq.heappop(lower_half_max_heap) * -1
            min_from_upper_half = heapq.heappop(upper_half_min_heap)
            heapq.heappush(lower_half_max_heap, min_from_upper_half * -1)
            heapq.heappush(upper_half_min_heap, max_from_lower_half)
            # heapq will handle restructuring heap so smallest values will be at index 0.
            max_from_lower_half = lower_half_max_heap[0] * -1
            min_from_upper_half = upper_half_min_heap[0]


numbers = int(input().strip())
for i in range(1, numbers + 1):
    num = int(input().strip())
    add_number_to_heap(num)
    rebalance_heaps()

    if i % 2 == 0:  # Even number of items so far.
        # Take the smallest from the upper half and largest from lower half (smallest * -1)
        largest_from_lower_half = lower_half_max_heap[0] * -1
        smallest_from_upper_half = upper_half_min_heap[0]
        median = (largest_from_lower_half + smallest_from_upper_half)/2
    else:  # Odd number of items so far.
        # lower_half_max_heap will fill up first.
        # median is the largest number in the lower half (smallest * -1)
        median = lower_half_max_heap[0] * -1
    # Format with min of 0 chars on left of decimal point and 2 after.
    print("{:0.1f}".format(median))
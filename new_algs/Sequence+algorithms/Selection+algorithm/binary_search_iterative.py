"""
@author: David Lei
@since: 21/04/2017
@modified:

Precondition: arr is in sorted order

How it works: look at middle item in arr, if target < mid split that half and binary search it, else look at the other
                half. This reduces the search size be half each time leading to the log n complexity
Invariants: the half we look at will either contain the target or not

Time complexity
- best O(1), target = arr[mid] first time
- worst O(log n), target is not in arr so we break up problem log n times and binary search them all
- avg O(log n)

Space complexity
- O(1), doesn't need any more space?

Does it always pick up the first occurrence of an element. No as in [1,1,1] searching for 1 will pick up the middle 1

Note: Don't slice array, that takes effort.
"""


def binary_search_iterative(array, target):
    lo = 0
    high = len(array) - 1
    while True:
        if lo > high:  # Can't find.
            return -1

        mid_index = (lo + high)//2
        if target == array[mid_index]:
            return mid_index
        elif target > array[mid_index]:
            lo = mid_index + 1
        else:
            high = mid_index - 1
    return -1

# Another implementation for practice ------

def binary_search(array, target):
    lo = 0
    hi = len(array) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if array[mid] == target:
            return mid
        elif array[mid] > target:  # Discard top half.
            hi = mid - 1
        else:  # Discard bottom half.
            lo = mid + 1
    return -1  # Not found.

#    0  1  2  3  4  5  6  7  8  9  10
a = [1, 2, 3, 5, 5, 5, 6, 7, 8, 9, 11]
target = 2

print(binary_search_iterative(a, target))
print(binary_search(a, target))
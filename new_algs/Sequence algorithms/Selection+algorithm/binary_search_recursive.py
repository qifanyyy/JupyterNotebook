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


def binary_search_rec(array, target, start, end):  # Precondition: Sorted low to high.
    middle_element_index = (start + end)//2
    if target == array[middle_element_index]:
        return middle_element_index
    if len(array) == 1:  # Only middle element.
        return -1  # Not found.
    elif target >= array[middle_element_index]:  # Search right half.
        return binary_search_rec(array, target, middle_element_index + 1, end)
    else:
        return binary_search_rec(array, target, start, middle_element_index - 1)

#    0  1  2  3  4  5  6  7  8  9  10
a = [1, 2, 3, 5, 5, 5, 6, 7, 8, 9, 11]
print(
    binary_search_rec(
        array=a,
        target=2,
        start=0,
        end=len(a) - 1
    )
)
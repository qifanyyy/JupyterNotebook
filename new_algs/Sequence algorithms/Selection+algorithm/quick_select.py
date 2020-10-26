"""
@author: David Lei
@since: 28/08/2016
@modified: 

Worst: O(n^2)
Best: O(n)

to find 3rd smallest element in array, a = [5, 4, 1, 2, 9, 8, 6]
    split array into 2 around a pivot, eg: make pivot 6
        less than 6 = [5, 4, 1, 2]
        greater than 6 = [6, 8]

        len(less than) = 4
        2 < 4 so do again
            pivot = 2
            less than = [1]
            greater than = [4, 5]

            len(less than) = 1, len(greater than) = 2

# given unsorted array, find kth smallest element
# same as sorting and finding item at index k
# but can do without complete sorting the entire array
"""
import random


def randomized_partition(array, start, end):
    random_index = random.randint(start, end)
    array[random_index], array[end] = array[end], array[random_index]
    # picked pivot 'randomly', put it at the end index
    # now partition
    pivot = array[end]          # randomly chosen pivot
    wall = start - 1
    for i in range(start, end):
        if array[i] <= pivot:
            wall += 1           # wall is <= pivot
            array[i], array[wall] = array[wall], array[i]       # swap elements
    array[wall + 1], array[end] = array[end], array[wall + 1]   # put pivot in right place
    return wall + 1             # index of pivot


def randomized_quick_select(array, start, end, i):
    """
    returns ith smallest element in an array[start...end]
    :param array: array of distinct elements
    :param start: start index to look at
    :param end: end index to look at
    :param i: something th smallest index we want
    """
    if start == end:                    # base case
        return array[start]
    pivot_index = randomized_partition(array, start, end)
    k = pivot_index - start + 1
    if i == k:
        return array[pivot_index]
    elif i < k:
        return randomized_quick_select(array, start, pivot_index-1, i)      # recurse on lower half
    else:
        return randomized_quick_select(array, pivot_index+1, end, i-k)      # recurse on upper half

# Another implementation for practice ------

def quick_select_partition_2(array, start, end, pivot_index):  # Inplace.
    array[end], array[pivot_index] = array[pivot_index], array[end]
    pivot_element = array[end]
    wall = start # Things left to the wall are smaller, right are bigger.
    for i in range(start, end):  # Exclusive of end as the pivot is now there.
        if array[i] < pivot_element:
            array[i], array[wall] = array[wall], array[i]
            wall += 1
    array[end], array[wall] = array[wall], array[end]
    return wall  # Will no return 0 but will return the value starting at start.

def quick_select_2(array, start, end, k):
    if start == end: # Only 1 element, return it.
        return array[start]
    pivot_index = (start + end) // 2
    pivot_index = quick_select_partition_2(array, start, end, pivot_index)  # Returns true position of pivot.
    k_smallest_element_index = k -1
    if k_smallest_element_index == pivot_index:  # We look for the kth smallest so the kth smallest is at index k.
        return array[k_smallest_element_index]
    elif k_smallest_element_index < pivot_index: # kth smallest element is in the bottom half.
        return quick_select_2(array, start, pivot_index - 1, k)
    else:                 # kth smallest element is in the top half.
        return quick_select_2(array, pivot_index + 1, end, k)


if __name__ == "__main__":
    #    1  2  3  4  5  6  7  8  9   10  11  12  13  14 | th smallest element.
    a = [1, 1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 14, 15, 20]
    # ith smallest element is in range [1, len(a)].
    ith_smallest_element = 9 # len(a) - 1
    print(randomized_quick_select(a[::-1], 0, len(a) - 1, ith_smallest_element))
    print(quick_select_2(a[::-1], 0, len(a) - 1, ith_smallest_element))
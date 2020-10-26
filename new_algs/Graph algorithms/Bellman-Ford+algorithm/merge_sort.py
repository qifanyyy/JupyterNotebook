#!/usr/bin/env python3

"""Merge sort implementation with inversions counter.
Max inversions number can be defined as n(n-1)/2
where n is a n-element array.
"""


def merge_sort(alist, inplace=False, print_inv=True, inversions=[0], reset_inv=True):
    """Merge sort implementation with inversions counter.
    :param alist: list
    :param inplace: bool. If True, list is sorted in place, otherwise a new list is returned.
    :param print_inv: bool. If True prints out total inversions number.
    :param inversions: mutable default argument to avoid globals (educational goal only).
    :param reset_inv: bool. Inversions parameter is set to [0] when sorting is done.

    >>> merge_sort([4, 3, 2, 1])
    Inversions: [6]
    [1, 2, 3, 4]
    >>> merge_sort([5, 4, 3, 2, 1])
    Inversions: [10]
    [1, 2, 3, 4, 5]
    >>> merge_sort([5, 4, 3, 2, 1, 5])
    Inversions: [10]
    [1, 2, 3, 4, 5, 5]
    >>> merge_sort([9, 8, 7, 6, 5, 4, 3, 2, 1, 0], True)
    Inversions: [45]
    """
    if inplace:
        combined = alist
    else:
        combined = alist[:]

    list_len = len(combined)
    if list_len > 1:
        middle = list_len // 2

        left = combined[:middle]
        right = combined[middle:]
        merge_sort(left, True, False, inversions, False)
        merge_sort(right, True, False, inversions, False)

        left_idx = 0
        right_idx = 0
        for k in range(list_len):
            if left_idx == len(left):
                combined[k] = right[right_idx]
                right_idx += 1
            elif right_idx == len(right):
                combined[k] = left[left_idx]
                left_idx += 1
            elif left[left_idx] <= right[right_idx]:
                combined[k] = left[left_idx]
                left_idx += 1
            elif left[left_idx] > right[right_idx]:
                combined[k] = right[right_idx]
                right_idx += 1

                # When this term is met. Count inversions by adding
                # a number of remaining elements in a left sublist.
                # Sublists are sorted, so when left element is greater
                # than the right one, all next left elements are greater too.
                inversions[0] += len(left[left_idx:])

    if print_inv:
        print("Inversions:", inversions)

    if reset_inv:
        inversions[0] = 0

    if not inplace:
        return combined

    return None


if __name__ == "__main__":
    import doctest
    doctest.testmod()

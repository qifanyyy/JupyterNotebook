#!/usr/bin/env python3

"""Python quick sort implementation with a comparisons counter.
Sorts in place, returns comparisons number.

Pivot selection can be done in 4 ways:
Always take the first element.
Always take the last element.
Choose median of 3 elements (first, last and the middle one).
Random choice.

First 2 methods can give you O(n**2) when an array is already sorted.
"""

import random


def quick_sort(alist, sidx, eidx, pivot_method=None):
    """Quick sort inplace implementation with comparisons counter. 4 methods to choose pivot:
    :param alist: A list.
    :param sidx: Start index for inplace list manipulation.
    :param eidx: End index for inplace list manipulation.
    :param pivot_method: None for default pivot selection: randomized. Other methods:
    'f' (first), 'l' (last), 'm3' (median of 3 elements: first, last and the middle one).
    :return: Comparisons number.

    >>> a = [9, 3, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    >>> b = [0, 3, 8, 1, 6, 8, 4]
    >>> c = [9, 3, 8, 4, 0, 2, 1, 9, 2, 2, 10]
    >>> quick_sort(a, 0, len(a), 'f')
    37
    >>> a
    [0, 1, 2, 3, 3, 4, 5, 6, 7, 8, 9]
    >>> quick_sort(b, 0, len(b), 'l')
    10
    >>> b
    [0, 1, 3, 4, 6, 8, 8]
    >>> quick_sort(c, 0, len(c), 'm3')
    27
    >>> c
    [0, 1, 2, 2, 2, 3, 4, 8, 9, 9, 10]
    """
    comps = 0

    if eidx - sidx < 2:
        return 0

    if pivot_method == 'f':  # First element
        piv_idx = sidx
    elif pivot_method == 'l':  # Last element
        piv_idx = eidx - 1
    elif pivot_method == 'm3':  # Median of 3 values (first, last and the middle one).
        midx = (sidx + eidx - 1) // 2
        med_of_three = [(alist[sidx], sidx), (alist[midx], midx), (alist[eidx - 1], eidx - 1)]
        piv_idx = sorted(med_of_three)[1][1]
    else:
        piv_idx = random.randint(sidx, eidx-1)  # Random pivot

    alist[sidx], alist[piv_idx] = alist[piv_idx], alist[sidx]
    pivot = alist[sidx]

    i = sidx + 1
    for j in range(sidx+1, eidx):
        comps += 1  # adds each comparison.
        if alist[j] < pivot:
            alist[i], alist[j] = alist[j], alist[i]
            i += 1

    alist[i - 1], alist[sidx] = alist[sidx], alist[i - 1]

    comps += quick_sort(alist, sidx, i - 1, pivot_method)
    comps += quick_sort(alist, i, eidx, pivot_method)
    return comps


if __name__ == "__main__":
    import doctest
    doctest.testmod()

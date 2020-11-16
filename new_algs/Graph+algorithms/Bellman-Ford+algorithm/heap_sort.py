"""Python heap sort implementation."""

import heapq


def heap_sort(l, desc_order=False):
    """Heap sort based on builtin heapq. Preserves original input list. Returns sorted list.
    Ascending order is default, however it can be reversed by setting desc_order to True.

    >>> a = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 3, 3, 1, 2]
    >>> heap_sort(a)
    [0, 1, 1, 2, 2, 3, 3, 3, 4, 5, 6, 7, 8, 9]
    >>> a
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 3, 3, 1, 2]
    >>> heap_sort(a, desc_order=True)
    [9, 8, 7, 6, 5, 4, 3, 3, 3, 2, 2, 1, 1, 0]
    """
    if desc_order:
        # It's still a min heap function, but all values are negated to get a max heap result.
        alist = [-i for i in l]
        heapq.heapify(alist)
        return [-heapq.heappop(alist) for _ in range(len(alist))]

    alist = l[:]
    heapq.heapify(alist)
    return [heapq.heappop(alist) for _ in range(len(alist))]


if __name__ == "__main__":
    import doctest
    doctest.testmod()

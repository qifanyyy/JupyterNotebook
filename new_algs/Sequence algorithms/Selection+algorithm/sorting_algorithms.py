from typing import List
import random

from utils.inputs import InputList

"""
=====================
MERGE SORT
=====================
"""


def merge_sort(L: List) -> List:
    """
    This will perform the merge sort algorithm.
    This is a compact version of the previous algorithm.
    It will save some space memory
    Args:
        L(list): Input list
    Returns:
        Sorted list
    """
    if len(L) <= 1:
        return L
    else:
        mid = len(L) // 2
        L_left = merge_sort(L[:mid])
        L_right = merge_sort(L[mid:])
        i, j, k = 0, 0, 0
        while i < len(L_left) and j < len(L_right):
            if L_left[i] < L_right[j]:
                L[k] = L_left[i]
                i += 1
            else:
                L[k] = L_right[j]
                j += 1
            k += 1
        while i < len(L_left):
            L[k] = L_left[i]
            i += 1
            k += 1

        while j < len(L_right):
            L[k] = L_right[j]
            j += 1
            k += 1
        return L


"""
=====================
QUICK SORT
=====================
"""


def quick_sort(L: List) -> list:
    """
    Performs the quick sort algorithm

    Parameters
    ----------
    L (list): input list

    Returns
    -------
    Sorted list
    """

    if len(L) <= 1:
        return L
    else:
        pivot = random.choice(L)
        L.remove(pivot)
        return quick_sort([x for x in L if x <= pivot]) \
               + [pivot] \
               + quick_sort([x for x in L if x > pivot])


if __name__ == "__main__":
    test_list = InputList(l_length=100)
    print(quick_sort(test_list))

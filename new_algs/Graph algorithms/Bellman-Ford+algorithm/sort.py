from copy import copy


def insertionsort(elements):
    def insert(element, sorted_elements):
        if len(sorted_elements) == 0:
            return [element]
        elif element < sorted_elements[0]:
            return [element] + sorted_elements
        else:
            return [sorted_elements[0]] + insert(element, sorted_elements[1:])

    return elements if len(elements) == 0 else insert(elements[0], insertionsort(elements[1:]))


def mergesort(elements):
    def merge(lhs, rhs):
        merged = []
        i = 0
        j = 0
        for _ in range(len(lhs) + len(rhs)):
            if i == len(lhs) or j < len(rhs) and lhs[i] > rhs[j]:
                merged.append(rhs[j])
                j += 1
            else:
                merged.append(lhs[i])
                i += 1
        return merged

    if len(elements) <= 1:
        return elements

    half_size = int(len(elements) / 2)

    return merge(
        mergesort(elements[:half_size]),
        mergesort(elements[half_size:])
    )


def quicksort(elements):
    """Sorts elements in-place. Returns None."""

    def quicksort_subarray(left, right):
        """Sorts in-place a subarray of elements from the left index (inclusive) to the right index (exclusive)."""
        if left < right:
            second_partition_start = partition(left, right)
            quicksort_subarray(left, second_partition_start - 1)
            quicksort_subarray(second_partition_start, right)

    def swap(a, b):
        elements[a], elements[b] = elements[b], elements[a]

    def partition(left, right):
        """Partition in-place a subarray of elements from the left index (inclusive) to the right index (exclusive).
        Returns an index of the beginning of the second partition.
        The implementation assumes that the first element of an array is a pivot element (aka a partitioning element)."""
        pivot = elements[left]
        # initially assume that the first partition is empty so the second starts just after the pivot
        second_partition_start = left + 1
        # now go through all the elements
        for i in range(left + 1, right):
            # and if a given element is smaller than the pivot
            if elements[i] < pivot:
                # then increase the first partition size by moving the start of the second to the right
                second_partition_start += 1
                # and move the element to the end of the first partition
                swap(i, second_partition_start - 1)
        # finally, place the pivot between the first and the second partition
        swap(left, second_partition_start - 1)
        return second_partition_start

    quicksort_subarray(0, len(elements))


def assert_sort(unsortet, sorted):
    assert insertionsort(unsortet) == sorted
    assert mergesort(unsortet) == sorted

    to_sort = copy(unsortet)
    quicksort(to_sort)
    assert to_sort == sorted


if __name__ == '__main__':
    assert_sort([], [])
    assert_sort([1, -1], [-1, 1])
    assert_sort([3, 2, 1], [1, 2, 3])
    assert_sort([1, 2, 3], [1, 2, 3])
    assert_sort([1, 3, -2], [-2, 1, 3])
    assert_sort([0, 0, 0, 0], [0, 0, 0, 0])
    assert_sort([-2, 2, -1, 1, 0], [-2, -1, 0, 1, 2])
    assert_sort([3, 5, 4, 1, 8, 6, 1], [1, 1, 3, 4, 5, 6, 8])
    assert_sort(['A', 'C', 'B'], ['A', 'B', 'C'])

    print('All tests passed')

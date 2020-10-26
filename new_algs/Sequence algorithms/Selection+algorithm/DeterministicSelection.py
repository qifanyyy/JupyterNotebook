# An implementation of the deterministic selection algorithm
# with a running time of O(n).
# select(array, n) returns the nth smallest element in an array
# where n >= 1.
# Also referred to as the nth order statistic.

import random


def swap(arr, i, j):
    temp = arr[i]
    arr[i] = arr[j]
    arr[j] = temp


def divide_array(arr):
    # Divides a list into groups of five and
    # returns a list of medians corresponding to each group.

    temp = []
    i = 0
    while True:
        if i * 5 == len(arr):
            break
        if (i * 5 + 5) > len(arr):
            divided = sorted(arr[i * 5: len(arr)])
            temp.append(divided[(len(arr) % 5) // 2])
            break

        divided = sorted(arr[i * 5: i * 5 + 5])
        temp.append(divided[2])
        i += 1

    return temp


def pivot_and_return_pivot_index(arr, pivot_pos):
    # Pivots the list 'arr' around arr[pivot_pos]
    # and returns the index of where the pivot ends up.

    swap(arr, 0, pivot_pos)
    pivot = arr[0]
    i = 0
    for j in range(1, len(arr)):
        if arr[j] <= pivot:
            i = i + 1
            swap(arr, i, j)

    swap(arr, 0, i)

    return i


def selector(arr, statistic):

    if len(arr) == 1:
        return arr[0]

    temp = divide_array(arr)

    # Finding an approximation to the median using the median
    # of medians technique.
    approx_median = selector(temp, len(temp)//2)

    # Finding the index of the approximate median
    # and pivoting around it.
    pivot_pos = arr.index(approx_median)
    i = pivot_and_return_pivot_index(arr, pivot_pos)

    if i == statistic:
        return arr[i]

    if i > statistic:
        return selector(arr[0: i], statistic)

    if i < statistic:
        return selector(arr[i+1: len(arr)], statistic-(i + 1))


def select(arr, statistic):
    # Make a copy to avoid in place changes.
    # statistic - 1 is passed to the  recursive function
    # to make the statistic 0 indexed
    # the user is expected to enter the nth statistic: n >= 1.

    arr_new = arr[:]
    return selector(arr_new, statistic-1)


# Testing the algorithm.
test_array = [i for i in range(-100, 100)]
random.shuffle(test_array)

# result is generated by querying the nth smallest element
# in shuffled test_array.
# result must be equal to the ordered test array.

result = []
for i in range(len(test_array)):
    result.append(select(test_array, i+1))

print("result == ordered test array? =", result == sorted(test_array))
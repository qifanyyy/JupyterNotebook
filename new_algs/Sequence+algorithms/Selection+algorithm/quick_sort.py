"""
@author: David Lei
@since: 21/08/2016
@modified:

How it works: at each stage, divide the problem around a pivot into 2 partitions. One containing things less than the
                pivot and another containing things greater or eqal to the pivot. Note that the paritioned lists will not
                include the pivot. This will keep on going until the list is of len 1 and then we can just put the overall
                list back together.

Invariants: section < pivot | pivot | section >= pivot

Compared to merge: work is done in the splitting of the array

Time complexity
- best O(n log n), when a decent pviot is chose for around event splitting
- worst O(n^2), when the pviot only discards one element from the array each time, thus needs to do it N^2 times
- avg O(n log n)

Space complexity - can do O(log n) note? figure out how
- O(N), create new lists when we split, for partitionaing arrays
- O(log n), when in place, still need log n space to for recursive calls to stall stack frames

I understand that both quick sort and merge sort need O(n) auxiliary space for the temporary sub-arrays that
are constructed, and in-place quick sort requires O(log n) auxiliary space for the recursive stack frames.
http://stackoverflow.com/questions/22233532/why-does-heap-sort-have-a-space-complexity-of-o1

There is a more complex version which uses an in-place partition algorithm and can achieve the complete sort
using O(log n) space (not counting the input) on average (for the call stack).
http://stackoverflow.com/questions/12573330/why-does-quicksort-use-ologn-extra-space

Stability: Not stable
"""
print_count = False
count = 0

def quick_sort(arr):
    """
    This works and uses the idea of quick sort but it can be done in place of the one array instead of making a new
    array which takes space
    """
    global count
    count += 1
    if print_count:
        print(count)

    if len(arr) <= 1:
        return arr
    else:
        # assume last item chosen as pivot
        pivot = arr[-1]

        wall = 0                        # everything before wall is < pivot
        for i in range(len(arr)-1):     # last element is pivot
            if arr[i] < pivot:
                temp = arr[wall]        # less than pivot
                arr[wall] = arr[i]      # move to index wall (everything before it will be <)
                arr[i] = temp
                wall += 1               # increment wall (so arr[i] is < pivot, now it is behind the wall)
        arr[len(arr)-1] = arr[wall]     # swap pivot with first element !< pivot
        arr[wall] = pivot

        less_than = quick_sort(arr[:wall])
        greater_eq_than = quick_sort(arr[wall+1:])

        return less_than + arr[wall:wall+1] + greater_eq_than

# ------ More pythonic solution -------
# http://stackoverflow.com/questions/25690175/bucket-sort-faster-than-quicksort

pythonic_count = 0
def pythonic_quick_sort(arr):         # more pythonic
    global pythonic_count
    pythonic_count += 1
    if print_count:
        print(pythonic_count)
    if len(arr) <= 1:
        return arr
    low, pivot, high = partition(arr)
    return pythonic_quick_sort(low) + [pivot] + pythonic_quick_sort(high)     # note [1] or [pivot] is a list of len 1

def partition(arr):
    pivot = arr[-1]
    # Inefficient space, also needs 2 loops instead of 1.
    low = [arr[x] for x in range(len(arr)-1) if arr[x] < pivot]
    high = [arr[x ]for x in range(len(arr)-1) if arr[x] >= pivot]
    return low, pivot, high

# ------ Inplace (same array, no extra space) solution -------

def quick_sort_inplace(arr, low, hi):
    if (hi-low) <= 1:           # array of len 1 eg first index, low = 0, hi = 1
        return arr              # array[start:to_non_inclusive]
    else:
        l_start, l_end, pivot_idx, ge_start, ge_end = partition_inplace(arr, low, hi)
        quick_sort_inplace(arr, l_start, l_end)
        quick_sort_inplace(arr, ge_start, ge_end)
        return arr

def partition_inplace(arr, low, hi):
    """
    low = start index of this sub array to partition
    hi = end index + 1 of this sub array to partition

    inplace (using the same array)
    restrict the array with the bounds arr[low:hi]
        1. make pivot the last element of the section we are looking at
        2. make some pointers to keep track of the part that is lower than pivot and greater than pivot
        3. loop over array from low to hi inclusive
        4. if element is < swap it with the first element that is greater (element at index wall)

    invariant: everything before wall is < pivot, everything after wall that we have already looked at is >= pivot
    """
    pivot = arr[hi-1]                               # take pivot to be the last element
    wall = low                                      # everything before the is < pivot
    for i in range(low, hi, 1):                     # loop from low to hi inclusive
        if arr[i] < pivot:                          # if less than pivot swap element at wall with the less than element
            arr[wall], arr[i] = arr[i], arr[wall]
            wall += 1
    arr[hi-1] = arr[wall]                           # put pivot in the right place
    arr[wall] = pivot
    # array mutated, don't need to return it
    # low = start of section < pivot
    # wall-1 = end of section < pivot
    # wall = pivot
    # wall+1 = start of section >= pivot
    # hi = end of section >= pivot
    return low, wall, wall, wall+1, hi

# ---- Another implementation for practice -----

def quick_sort_2(array):
    if len(array) <= 1:
        return array
    pivot = len(array) // 2  # Assume mid point as pivot.
    wall = 0  # Everything before the wall will be lower than array[pivot].
    pivot_element = array[pivot]
    array[-1], array[pivot] = array[pivot], array[-1]
    for i in range(len(array) - 1):  # This partitions the array such that elements less than pivot < wall <= elements greater equal to pivot.
        if array[i] < array[-1]:
            array[i], array[wall] = array[wall], array[i]
            wall += 1
    array[-1], array[wall] = array[wall], array[-1]
    left = quick_sort_2(array[:wall])  # Up until pivot not inclusive.
    right = quick_sort_2(array[wall + 1:])  # From pivot + 1 inclusive to the end.
    return left + [pivot_element] + right

if __name__ == "__main__":
    arr = [1,2,3,4,2]
    b = [10, 9, 8, 7, 4, 1, 0, -1, -40]
    bar = [8, 100 ,1,-3,11,1,0]
    car = [0,-3,1,-2]
    foo = [123,91,-19, 1,1,2,1,-54,1909,-51293,192,3,-4]
    dada = [-100301203, 1231, 90, 0, 123199, 123818, 14124, 12, 4, -41, -51, 9]
    boo = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 0, 0.131, 19]
    correct = 0

    for _ in range(1000):
        arrays = [arr, bar, car, foo, dada, boo, b]
        for array in arrays:
            sorted = array[::]
            sorted.sort()
            # Note: I think something here mutates the array and other things stuff up because of reference or
            # something but copying the array fixes this ¯\_(ツ)_/¯.
            result_qs = quick_sort(array[::])
            result_pythonic = pythonic_quick_sort(array[::])
            result_inplace = quick_sort_inplace(array[::], 0, len(array))
            result_qs_2 = quick_sort_2(array[::])

            if result_qs == result_pythonic == result_qs == result_inplace == sorted:
                print("Results match: " + str(result_qs_2))
                correct += 1
            else:
                print("Oh No! Results don\'t match")
                print("array:        " + str(array))
                print("quick sort:   " + str(result_qs))
                print("pythonic:     " + str(result_pythonic))
                print("inplace:      " + str(result_inplace))
                print("quick sort 2: " + str(result_qs_2))
    print("correct {}/1000 times".format(int(correct/7)))

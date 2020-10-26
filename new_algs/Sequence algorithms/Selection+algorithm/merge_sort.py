"""
@author: David Lei
@since: 21/08/2016
@modified:

How it works: at each stage, break down the sorting space by half (reduce the problem by half) and do this until
                we have a problem of size 1 O(log n), this is considered sorted. Then put all the pieces back together
                O(n)
Invariants: when we get to merging, after the merge everything in that list will be sorted?

Compared to quick: work is done putting the array back together

Time complexity
- best O(n log n)
- worst O(n log n)
- avg O(n log n)

Space complexity
- O(N), when we merge we copy so need another N space so O(N), also create new lists when we split?

Stability: yes as in merge we use > or < and not =

Note: no matter what the input is, the count always stays the same for arrays of the same length
- arr and bar are the same len, but different numbers. Both get a count of 13
- this reflects merge sort's best=worst=avg complexity


Inplace merge sort
http://stackoverflow.com/questions/2571049/how-to-sort-in-place-using-the-merge-sort-algorithm
"""
print_count = False
count = 0

def merge_sort(arr):
    """
    This works and is a decent implementation, it makes the most sense to me. However you can implement merge sort inplace
    """
    global count
    count += 1
    if print_count:
        print(count)
    if len(arr) <= 1:
        return arr
    else:
        mid = len(arr)//2
        left = merge_sort(arr[:mid])    # split list into left half
        right = merge_sort(arr[mid:])   # split list into right half

        # after split is done, lets merge
        merged_arr = []                 # copy into this, need another N space
        len_left = len(left)
        len_right = len(right)
        i = 0
        j = 0
        while i < len_left or j < len_right:
            if i < len_left and j < len_right:  # can compare elements from both lists
                if left[i] < right[j]:          # element in list L < R so append smaller
                    merged_arr.append(left[i])
                    i += 1
                else:
                    merged_arr.append(right[j]) # element in list R < L so append smaller
                    j += 1
            else:                               # one list has already fished being merged
                if i < len_left:                # still more in list L
                    start = i
                    for k in range(start, len(left)):
                        merged_arr.append(left[k])
                        i += 1
                elif j < len_right:
                    start = j
                    for r in range(start, len(right)):
                        merged_arr.append(right[r])
                        j += 1
        # above does the merge
        return merged_arr

# ---- Another implementation for practice -----

def merge_arrays(left, right):
    result = [0 for _ in range(len(left) + len(right))]
    result_index = 0
    left_index = 0
    right_index = 0
    while True:
        if left_index >= len(left):
            # Copy over rest of right.
            for i in range(right_index, len(right)):
                result[result_index] = right[i]
                result_index += 1
            break
        if right_index >= len(right):
            # Copy over rest of left.
            for i in range(left_index, len(left)):
                result[result_index] = left[i]
                result_index += 1
            break
        if left[left_index] <= right[right_index]:
            result[result_index] = left[left_index]
            result_index += 1
            left_index += 1
        else:  # right is < left.
            result[result_index] = right[right_index]
            result_index += 1
            right_index += 1
    return result

def merge_sort_2(array):
    if len(array) <= 1:
        return array
    mid = len(array) // 2
    left = merge_sort_2(array[:mid])
    right = merge_sort_2(array[mid:])
    return merge_arrays(left, right)


if __name__ == "__main__":
    arr = [1,2,3,4,5,6,7]
    bar = [8, 100 ,1,-3,11,1,0]
    car = [0,-3,1,-2]
    foo = [123,91,-19, 1,1,2,1,-54,1909,-51293,192,3,-4]
    tests = [arr, bar, car, foo]
    for array in tests:
        result1 = merge_sort(array)
        result2 = merge_sort_2(array)
        if result2 == result1:
            print("Results match, " + str(result1))
        else:
            print("Oh No!!! Results don't match")
            print("result1: " + str(result1))
            print("result2: " + str(result2))


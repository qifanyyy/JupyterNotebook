"""
@author: David Lei
@since: 22/04/2017
@modified: 

Inversions: How close/far the array is from being sorted.

Inversions occur in the merge step.

https://www.hackerrank.com/challenges/ctci-merge-sort

Good exercise for D & Q, a bit tricky to count inversions.

TLE last 3 out of 13 test cases.
"""


def merge_sort_inversions(arr, inversions):
    if len(arr) <= 1:  # Base case.
        return arr, inversions
    else:  # Recurse.
        mid_point = len(arr)//2
        # Recursive calls to left and right of arr to break problem into subproblems to conquer.
        left, left_inversions = merge_sort_inversions(arr[:mid_point], inversions)
        right, right_inversions = merge_sort_inversions(arr[mid_point:], inversions)
        inversions = left_inversions + right_inversions
        # Merge them back.
        temp = []
        left_index = 0
        right_index = 0

        while True:
            # Left should be < right due to ordering, if not it is an inversion.
            if left_index > len(left) - 1:  # Left out of bounds.
                if right_index <= len(right) - 1:  # Right in bounds.
                    temp.extend(right[right_index:])  # Copy rest of right over.
                break

            if right_index > len(right) - 1:  # Right out of bounds.
                if left_index <= len(left) - 1:  # Left in bounds.
                    temp.extend(left[left_index:])  # Copy rest of left over.
                    # Update inversions.
                    # before = INVERSIONS
                    # inversions += len(left[left_index:])
                    # after = INVERSIONS

                break

            if left[left_index] <= right[right_index]:
                temp.append(left[left_index])
                left_index += 1
            elif left[left_index] > right[right_index]:
                temp.append(right[right_index])
                right_index += 1
                # Increment inversions here.

                # TODO: Understand this & move to ctci folder.
                # Everything on left is meant to be < Everything on right.
                # E.g: left = [1, 2, 3, 4, 10, 11, 12], right = [7, 8]
                # up until left_index = 3, everything is fine, then right is bigger.
                # Currently combined array looks like [1, 2, 3, 4, 10, 11, 12, 7, 8]
                # Need to swap 10 and 7, 11 and 8, 10 and 12, 12 and 11 = 4 inversions.
                # len(left) = 6, left_index = 3.
                # Add 3 to inversions.
                # Put right on, then
                inversions += (len(left) - left_index)  # TODO: Work out this part and understand it.

        return temp, inversions

num_test_cases = int(input())

for _ in range(num_test_cases):
    _ = input()
    array = [int(x) for x in input().split(' ') if x != '']
    inversions = 0
    sorted_array, inversions = merge_sort_inversions(array, inversions)
    # print(sorted_array)
    print(inversions)
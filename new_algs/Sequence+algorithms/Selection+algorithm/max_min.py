"""
@author: David Lei
@since: 22/04/2017
@modified: 

https://www.hackerrank.com/challenges/angry-children

Given a list of N integers, select K integers from the list
so unfairness is minimized.

unfairness is defined as max(iterable) - min(iterable)
"""

number_elements = int(input())
k_selected_numbers = int(input())
l = [int(input()) for _ in range(number_elements)]
l.sort()

unfairness = None
for i in range(0, number_elements - k_selected_numbers + 1, 1):
    # Slicing is around O(k) work where k is the length of the slice, worst case in this can be O(n).
    # although that means the loop won't run as much, still upperbounds ~ O(n^2),
    # use pointers to get test case 9 to pass.
    # slice = l[i:i + k_selected_numbers]

    # Already know max and min as array is sorted.
    local_unfairness = l[i + k_selected_numbers - 1] - l[i]  # max(slice) - min(slice)
    if not unfairness:
        unfairness = local_unfairness
    elif local_unfairness < unfairness:
        unfairness = local_unfairness
print(unfairness)





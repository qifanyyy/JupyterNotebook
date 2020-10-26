"""
@author: David Lei
@since: 13/08/2017

https://leetcode.com/problems/3sum/description/

Given an array of integers, are there 3 elements a, b, c such that a + b + c = 0?
Find all unique triplets in the array which gives the sum of zero.

Specialized for of sum of subsets problem (or subset sum).

O(n^2) solution.

For each subset of 3, try do subset sum to total to 0.

To get a subset of 3, need to do n choose 3.

Combinations don't care about position, permutations do, we want unique sets (values matter, not position).

TODO: Optimize: https://www.youtube.com/watch?v=jXZDUdHRbhY

Loop from either end, find what number you need to make the target 0 and check in a hashmap if it exists.
"""

# Complexity below is upper bounded by O(n choose r) where n is len of set_of_values and r is 3.
# This is bad, more than n^2 (the optimal solution).
import itertools

set_of_values = [-1, 0, 1, 2, -1, -4]

# A solution set is:
# [
#   [-1, 0, 1],
#   [-1, -1, 2]
# ]

combination_iterable = itertools.combinations(set_of_values, 3)  # O(len(set_of_values) choose 3)

sum_value = 0
seen_solutions = set()

for combination in combination_iterable: # O(len(set_of_values) choose 3)
    combination = list(combination)
    # Needed as otherwise [1, 0, -1] and [-1, 0, 1] will both be considered as solutions.
    combination.sort()  # O(3)
    if sum(combination) == 0: # O(3)
        if str(combination) not in seen_solutions:
            seen_solutions.add(str(combination))
print([eval(s) for s in seen_solutions])

# TODO: Try naive n^3 solution.

# TODO: Try optimal n^2 solution.


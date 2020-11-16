"""
@author: David Lei
@since: 7/11/2017

https://www.hackerrank.com/challenges/components-in-graph/problem

Seems like the problem is if there is an edge, merge components.
Then look at the array in the distjoint set and print the biggest and smallest.

Passed :) Damn distjoint sets are powerful.
"""

n = int(input())


class DistjointSet:

    def __init__(self, n):
        self.array = [-1] * n

    def find(self, i): # Includes path compression.
        # Find group that index i belongs to.
        if self.array[i] < 0:
            return i
        group = self.find(self.array[i])
        self.array[i] = group  # Path compression.
        return group

    def union(self, a, b):
        group_a_index = self.find(a)
        group_b_index = self.find(b)
        if group_a_index == group_b_index:
            return
        if abs(self.array[group_a_index]) >= abs(self.array[group_b_index]):
            # B is smaller so add it to the larger which is A so the max len of A doesn't increase.
            self.array[group_a_index] += self.array[group_b_index]
            self.array[group_b_index] = group_a_index
        else:
            # A is smaller, B is larger so add A to B so max len of A doesn't increase.
            self.array[group_b_index] += self.array[group_a_index]
            self.array[group_a_index] = group_b_index

distjoint_set = DistjointSet(2 * n + 1) # Allow for 1 based nature of questions.

for _ in range(n):
    a, b = [int(x) for x in input().split()]
    distjoint_set.union(a, b)

min_components = 150000
max_components = 1
for value in distjoint_set.array[1:]: # Need to slice from index 1 as my implementation is 0 based.
    if value > 0 or value == -1: # Single nodes not taken into account.
        continue # Is a parent pointer and not a component.
    if value * -1 > max_components:
        max_components = value * -1
    if value * -1 < min_components:
        min_components = value * -1
print("%s %s" % (min_components, max_components))



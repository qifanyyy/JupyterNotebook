"""
@author: David Lei
@since: 7/11/2017

https://www.hackerrank.com/challenges/merging-communities/problem

Seems like a basic distjoint set problem.

Passes :)
"""

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



n, queries = [int(x) for x in input().split()]

distjoint_set = DistjointSet(n + 1)

for _ in range(queries):
    cmd = input().split()
    if cmd[0] == "Q":
        group_index = distjoint_set.find(int(cmd[1]))
        print(distjoint_set.array[group_index] * -1)
    else:
        distjoint_set.union(int(cmd[1]), int(cmd[2]))

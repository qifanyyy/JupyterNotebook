"""
@author: David Lei
@since: 22/04/2017
@modified: 

https://www.hackerrank.com/challenges/ctci-comparator-sorting

Sample input:
5
amy 100
david 100
heraldo 50
aakansha 75
aleksa 150
"""
from functools import cmp_to_key


class Player:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __repr__(self):
        return self.name + " " + self.score

    def comparator(a, b):
        """
        Compares a and b where a is self and b is another object.

        returns:
            -1: if a < b
            0: if a == b
            1: a > b

        -1 means appears in list earlier than 1.

        Sort in decreasing order, largest first.
        """
        if a.score < b.score:
            # a < b based on score, want to return a > b so it placed towards the end of the
            # return list as bigger elements are at the end of the array.
            # Results in bigger score being seen as smaller so placed earlier in the array.
            return 1
        if b.score < a.score:
            # Likewise with above, if b < a, put a it at the end as it is smaller return a > b as
            # Normally larger gets put at end.
            return -1
        if a.name < b.name:
            return -1
        if b.name < a.name:
            return 1
        return 0


n = int(input())
data = []
for i in range(n):
    name, score = input().split()
    score = int(score)
    p = Player(name, score)
    data.append(p)

data = sorted(data, key=cmp_to_key(Player.comparator))
for i in data:
    print(i.name, i.score)

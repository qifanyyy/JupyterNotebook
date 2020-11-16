"""
@author: David Lei
@since: 1/09/2017

Fenwick Tree (a.k.a Binary Indexed Tree). Use to calculate running values.

https://www.youtube.com/watch?v=CWDQJGaN1gY&ab_channel=TusharRoy-CodingMadeSimple
https://www.hackerrank.com/topics/binary-indexed-tree
https://www.topcoder.com/community/data-science/data-science-tutorials/binary-indexed-trees/

A Binary Indexed Tree (BIT) is used to store cumulative sums.
You have an array a0, a1, ..., an. You want to be able to retrieve the sum of the first k elements in O(logn) time,
and you want to be able to add a quantity q to the i-th element in O(logn) time. Note that these two operations can be
implemented with a normal array, but the time complexity will be O(n) and O(1).

Given array A: [3, 2, 0, 6, 5, -1, 2]

A Fenwick tree allows you to give quick range queries of form what is the sum for index x to y.

Naive approach: Keep a prefix sum array where each index is the sum from index 0 to index n of A.
This is very bad with frequent updates.

Note: Can also use segment tree but that is more complex.

Fenwick Tree:
- Space Complexity: O(n)
- Time Complexity:
    - Search: O(log n)
    - Update every element: O(log n)
    - Create for first time: O(n log n)

Example:
    i:   0  1   2  3  4  5   6  7  8  9 10
    A: [ 3, 2, -1, 6, 5, 4, -3, 3, 7, 2, 3 ]

    Tree:
        0: dummy node, doesn't store any info.
        nodes 1 - 11 will store prefix sum
        nodes shown as [value]index.

        for each node on level 1, if you get the binary representation and flip the right most bit, the value will be 0
        which is their parent. They are all even numbers < 9 so bin rep is 1 and any number of trailing 0's which when
        flipped will be 0.

        for node 10, bin rep = 1010, right most bit flipped = 1000 = 8, so 10's parent is 8.

        for node 11, bin rep = 1011, right most bit flipped = 1010 = 10, so 11's parent is 10.

        get_parent(node_i): return bin rep with right most bit flippe.


        lvl 0:                                 []0
                               ------------/----|--------\-----------------
                              /           /                \                \
        lvl 1:             [3]1        [5]2                [10]4             [19]8
                                         |                   / \              | \
                                         /                  /   \             /  ----\
        lvl 2:                         [-1]3               [5]5  [9]6       [7]9     [9]10
                                                                 |                   |
        lvl 3:                                                   [-3]7               [3]11

        Every number can be represented as a sum of powers of two. eg:
            10 = 2^3 + 2^1
            11 = 2^3 + 2^1 + 2^0

        Fenwick trees use this to store the values.

          A[i]  | value |   sum 4 range |  T[i]                | meaning in A
        --------|-------|---------------|----------------------|------------------------------------------------------------------------------------
           0    |   3   |       3       | 1 = 0 + 2^0          | starting from index 0, sum of next element or range (0, 0) is 3 stored in 1
           1    |   2   |       5       | 2 = 0 + 2^1          | starting from index 0, sum of range(0 1) is 5 stored i 2
           2    |   -1  |       -1      | 3 = 2^1 + 2^0        | starting from index 2, sum of next element or range (2, 2) is -1 stored in 3
           3    |   6   |       10      | 4 = 0 + 2^2          | starting from 0, sum of next 4 elements stored in 4. sum = 10, store 10 in 4.
           4    |   5   |       5       | 5 = 2^2 + 2^0        | starting from 4, next 1 element stored at 5. Sum = range(5, 5) = 5
           5    |   4   |       9       | 6 = 2^2 + 2^1        | starting from 4, sum of next 2 elements or range(4, 5) is stored in 6. sum = 9
           6    |   -3  |       -3      | 7 = 2^2 + 2^1 + 2^0  | starting from sum(lhs) = 6, sum of the next element or range(6, 6) is stored in 7. sum = -3
           7    |   3   |       19      | 8 = 0 + 2^3          | starting from 0, sum of range (0, 8) is 19.
           8    |   7   |       7       | 9 = 2^3 + 2^0        | range (8, 8), sum = 7. store 7 in 9
           9    |   2   |       9       | 10 = 2^3 + 2^1       | range(8, 9), sum = 9. store 9 in 10.
           11   |       |               | 11 = 2^3 + 2^1 + 2^0 | sum(lhs) = 10, range = (10, 10). sum is 3, store 3 in 11.

    Searching in tree:
        Aim: Get prefix sum given a range.

        Eg: get prefix sum of range (0, 5)

            1. go to node 6, take that value and then go to parent
            2. get value at parent and sum, go to parent
            keep doing this until it is over.

            node 6 = 9, parent = node 4
            node 4 = 10, parent = node 0
            prefix sum = 9 + 10 = 19 is sum of index 0 to 5 in A.

        Eg: get prefix sum of range(0, 9)

            node 10 = 9, parent is 8.
            node 8 = 19, parent is 0.
            prefix sum = 19 + 9 = 28

        Eg: get prefix sum of range(0, 6)

            node 7 = -3, parent is 6
            node 6 = 9, parent = node 4
            node 4 = 10, parent = node 0
            prefix sum = 16

        Time = height of binary index tree = O(log n) in worse case.

    Create tree.
        Use get_next() to update everything that can be effected by an update.

"""

class FenwickTree:

    def __init__(self, len):
        self.arr = [0] * (len + 1)

    def compute_range_sum(self, upper_index):
        """The indexes will be within the array range.
        Compute sum from 0 to including upper_index.
        """
        total = 0
        total += self.arr[upper_index + 1]

        parent = self.get_parent(upper_index + 1)
        while parent != 0:
            total += self.arr[parent]
            parent = self.get_parent(parent)
        return total

    def get_next(self, i):
        """Get anything that can be effected by a update.
        1. get 2's compliment (flip all bits, add 1).
        2. AND with original number.
        3. ADD to original number.
        """
        bin_rep = bin(i)
        flipped_bits = '0b' + ''.join(['1' if x == '0' else '0' for x in bin_rep[2:]])
        twos_compliment = int(flipped_bits, 2) + 1
        anded = i & twos_compliment
        added = i + anded
        return added

    def add(self, index, value):
        self._update(index + 1, value)
        next = self.get_next(index + 1)
        while next < len(self.arr):
            self._update(next, value)
            next = self.get_next(next)
        print(self.arr)

    def _update(self, index, value):
        if self.arr[index] == 0:
            self.arr[index] = value
        else:
            self.arr[index] = self.arr[index] + value

    def print_tree(self):
        print('Fenwick Tree')
        for i in range(len(self.arr)):
            print("(node: {0}, value: {1})".format(i, self.arr[i]))


    def make_tree(self, arr):
        for index, value in enumerate(arr):
            self._update(index + 1, value)
            next = self.get_next(index + 1)
            while next < len(self.arr):
                self._update(next, value)
                next = self.get_next(next)
        print(self.arr)

    def get_parent(self, i):
        """Get parent of a node in a Fenwick tree.
        1. get 2's compliment (flip all bits, add 1)
        2. and with original number
        3. subtract from original number
        This is flipping the right most set bit.
        """
        bin_rep = bin(i)
        # TODO: ~i also works, but don't understand why.
        flipped_bits = '0b' + ''.join(['1' if x == '0' else '0' for x in bin_rep[2:]])
        twos_compliment = int(flipped_bits, 2) + 1
        anded = i & twos_compliment
        subtracted = i - anded
        return subtracted


if __name__ == "__main__":
    arr = [3, 2, -1, 6, 5, 4, -3, 3, 7, 2, 3]
    ft = FenwickTree(len(arr))
    ft.make_tree(arr)
    ft.print_tree()
    print(ft.compute_range_sum(6))  # 16.
    print(ft.compute_range_sum(9))  # 28.
    ft.add(6, -30)
    print(ft.compute_range_sum(6))  # -14.

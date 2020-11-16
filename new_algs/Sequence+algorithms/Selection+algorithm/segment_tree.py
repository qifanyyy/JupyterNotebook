"""
@author: David Lei
@since: 2/09/2017

Segment trees allow for range queries in arrays.

Allows queries such as what is the minimum in this range what is the maximum in this range.

http://codeforces.com/blog/entry/6847
https://www.youtube.com/watch?v=ZBHKZF5w4YU&t=523s&ab_channel=TusharRoy-CodingMadeSimple

Segment tree is a binary tree with elements of the array as leaves of the tree.

idx:   0  1  2  3  4  5
arr: [-1, 3, 4, 0, 2, 1]

Tree:

Create the tree by splitting the array in half until length 1.

Start by putting in leaves, parent is min(children)

lhs = [-1, 3, 4]    |       rhs = [0, 2, 1]

value[lo_idx, hi_idx] means value is min in the range

                    -1[0, 5]
              r4  /          \   r0
                /             \
              -1[0,2]         0[3,5]
             /    \            /    \
            /      \          /      \
         -1[0,1]   4[2,2]    0[3,4]   1[5,5]
         /    \              /    \
        /      \            /      \
      -1[0,0]  3[1,1]      0[3,3]   2[4,4]

Rules:
    1. partial overlap, look on both sides
    2. total overlap, stop return that value.
    3. no overlap, stop return big number.

Range queries:
    range(2, 4), what is the minimum in range 2, 4 in the array.

        1. start at root
            (2,4) & (0, 5), (2,4) does not totally overlap (0,5) so partial overlap so look both directions.
        2. explore down left branch
            (2,4) & (0, 2), partial overlap, explore both branches
        3. explore down left branch
            (2,4) & (0, 1), no overlap won't contribute to answer stop and return big number.
        4. explore down right branch of (0, 2)
            (2,4) & (2, 2) total overlap.
            (2,4) completely encapsulate (2,4), return value 4.
        5. propagate 4 up, at (0,2) min(big_num, 4) is 4 so lhs returns 4.
            r4
        6. explore down right branch of root
            (2,4) & (3,5) partial overlap, look at both branches
        7. explore down left branch of (3,5)
            (2,4) & (3,4) total overlap
            (3,4) must be in (2,4) as 2 is a lower lower bound than 3.
            return 0
        8. propagate 0 up. right branch of (3, 5) is (5,5) no overlap so return big max.
            return 0 up to root, so rhs returns 0.
        9. pick min(lhs, rhs) at root = 0.

        This means the minimum from 2, 4 is 0.

    range(0, 4), what is the minimum in range 0, 4

        1. look at root, partial overlap as (0, 5) not entirely in (0, 4)
        2. left branch of root, (0,2) is entirely in (0,4)
            return value -1, we know there is no need to traverse deeper as the min for anything else
            has alreay been propagated up.
        3. right branch of root, (3, 5) partial overlap.
        4. left branch of (3, 4), (3,4) totally overlapped so return min.
        5. return 0 from rhs.
        6. pick min at root = -1

    At max you will go to a depth of 4 so in worst case time complexity is O(4 log n)*[]:

Creating tree with array.

size of array = if array len is power of 2 then segment tree array len = number * 2 - 1
                    else find next power of 2 and do the same.


arr: [ -1, 0, 3, 6]

tree:

    value[index]

            -1[0]
          /      |
      -1[1]       3[2]
      /   \      /   \
    -1[3] 0[4]  3[5]  6[6]

this tree is stored in an array.

idx:         0   1  2   3  4  5  6
tree_arr: [ -1, -1, 3, -1, 0, 3, 6]

left child = 2i + 1
right child = 2i + 2
parent = (i - 1) // 2

Space: O(4n) = O(n)

Time:
    - create O(n)
    - query O(log n)

"""

class SegmentTree:

    def _get_next_power_of_two(self, n):
        """TODO: Figure out how this works xD."""
        if n == 0:
            return 1
        if n & (n - 1) == 0:
            return n
        while n & (n - 1) > 0:
            n &= (n - 1)
        return n << 1

    def __init__(self, arr):
        length = len(arr)
        next_power_of_two = self._get_next_power_of_two(length)
        self.arr = [0] * ((next_power_of_two * 2) - 1)




    def make_tree(self, arr):
        pass


    def make_query(self):
        pass
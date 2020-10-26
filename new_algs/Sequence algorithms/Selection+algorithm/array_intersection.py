"""
@author: David Lei
@since: 20/10/2017

Given two sorted lists and return a list of their intersection with no
duplicates with O(1) space and O(n) run time
 For example:  A[2,3,3,4,6,6,8] B[3,3,6,7,9]  should return [3, 6]  

Approach:

So since they are sorted we can have pointers i looking at array a and j looking at array b and iterate through that
which would be O(a) + O(b) = O(n) where is the number of items in both arrays.
I'm not sure how to make the output constant space so ill make the output O(intersection) but won't use any other space apart from that.

Another approach is to use sets, turn both arrays into a set and return the intersection, but that would use extra space.

"""

def intersection_extra_space(array_a, array_b):
    return list(set(array_a) & set(array_b))

def intersection(array_a, array_b):
    i = 0
    j = 0
    # Doing it without a set means we need ot keep track of the last number we added. output = set()
    last_num = None
    output = []
    while True:
        # Termination: When we have look through all of 1 array until the end of the array, there can't be anything shared past this.
        if i >= len(array_a):
            break
        if j >= len(array_b):
            break
        if array_a[i] == array_b[j]:
            if last_num != array_a[i]: # Don't already have a copy of this.
                output.append(array_a[i])
            if not last_num:
                last_num = array_a[i]
            # Can increment both as don't want dups.
            i += 1
            j += 1
        elif array_a[i] < array_b[j]:
            i += 1
        else:
            j += 1
    return output

if __name__ == "__main__":
    a = [2,3,3,4,6,6,8]
    b = [3,3,6,7,9]
    print(intersection_extra_space(a, b))
    print(intersection(a, b))
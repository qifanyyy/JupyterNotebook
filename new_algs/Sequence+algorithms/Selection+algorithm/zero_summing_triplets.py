"""
@author: David Lei
@since: 8/11/2017

http://www.geeksforgeeks.org/find-triplets-array-whose-sum-equal-zero/
"""

array = [0, -1, 2, -3 ,1]
def zero_summing_triples(array): # O(n^2) time, O(n) space. Naive is O(n^3) time, can do n^2 soln in O(1) space using sorting.
    # Match this i with every other j.
    # so 0 is matched with -1, 2, -3, 1
    # and -1 is matched with -1, 2, -3, 1.
    # and so forth.
    for i in range(len(array)):
        look_up = set()
        for j in range(i + 1, len(array)):
            sum_to_zero = -1 * (array[i] + array[j])
            if sum_to_zero in look_up:
                print("This triple sums to 0: %s, %s, %s" % (array[i], array[j], sum_to_zero))
            else:
                look_up.add(array[j])
    """ Works because, for the fist triple we encounter.
    (0, -1, 1)
    i = 0
    j goes from 1 to n - 1
    when j = 1, array[1] = -1, so we need to find 0 + -1 + x = 0 so x is 1
    1 is not in the look_up so we add in the value of j.

    Since if a triple appears we must encounter a part of the non set triple (set one is 0) twice
    in the j loop we know that when we get to j = 4, array[4] = 1 we need to find 0 + 1 + x = 0 and x = -1
    so we can check to look up to see has there been any value we have already seen that fits in this triple.

    Damn this is really smart.
    """
zero_summing_triples(array)
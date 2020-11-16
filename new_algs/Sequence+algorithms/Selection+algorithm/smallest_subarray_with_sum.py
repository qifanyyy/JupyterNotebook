"""
@author: David Lei
@since: 7/11/2017

http://www.geeksforgeeks.org/minimum-length-subarray-sum-greater-given-value/

Given an array of integers and a value x, what is the minimum subarray
that sums to > x.

Minimum is defined by the length of the sub array.

Print out the length of the minimum sub array.

Sub array means that items must be contiguous.
"""

def minimum_subarray(array, x):  # Naive O(n^2) soln.
    min_len = len(array) + 1 # + 1 so if min_len > len(array) is impossible.
    # For all items in array.
    for start_index in range(len(array)):  # Picks starting element.
        current_sum = array[start_index]
        if current_sum > x:  # Special case, smallest sub array only contains 1 element.
            return 1
        # From about item as the start, considering all others.
        for end_index in range(start_index + 1, len(array)):  # Considers all elements after starting element.
            current_sum += array[end_index]  # Add to the current sum.
            if current_sum > x:
                # If start = 2 and end = 3 then the len is 2 but 3 - 2 is 1 so need the + 1
                if end_index - start_index + 1 < min_len:  # Keep track of min length encountered.
                    min_len = end_index - start_index + 1
    return min_len

def minimum_subarray_efficient(array, x):
    min_len = len(array) + 1
    current_sum = 0
    start_index = 0
    end_index = 0
    while end_index < len(array):  # O(n), due to pointers in the worst case we only consider each element twice once with start and once with end.
        # Only wanna process stuff if have not reached end of array.

        while current_sum <= x and end_index < len(array):
        # Keep adding until we get a current sum > x.
            current_sum += array[end_index]
            end_index += 1

        while current_sum > x and start_index < len(array):
            # Only get here once current sum > x.
            # Since we have a current sum > x then the sub array is a candidate for the soln.
            if end_index - start_index < min_len:
                min_len = end_index - start_index
            # Remove starting elements to try shrink sub array.
            #   if this leads to current_sum <= x then loop won't execute again.
            #       if above occurs then the first inner while loop will take care of adding stuff again.
            current_sum -= array[start_index]
            start_index += 1
    return min_len

arr = [1, 11, 100, 1, 0, 200, 3, 2, 1, 250]
x = 280
print(minimum_subarray(arr, x))
print(minimum_subarray_efficient(arr, x))
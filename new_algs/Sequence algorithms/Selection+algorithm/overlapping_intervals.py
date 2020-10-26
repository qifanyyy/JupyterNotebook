"""
@author: David Lei
@since: 18/05/2017
@modified: 

http://www.geeksforgeeks.org/merging-intervals/


Given a bunch of intervals:  {{1,3}, {2,4}, {5,7}, {6,8}},
Output them merged with no overlap: {{1, 4,}, {5, 8}

If can merge, merge. If can't don't.

Assume won't always be sorted.

Complexity is upper bounded by sort time O(n log n) as .sort() is timsort.
"""

# Precondition: interval_b fits in or can extend interval b.
def merge_interval(interval_a, interval_b):
    lower_bound = min(interval_a[0], interval_b[0])
    upper_bound = max(interval_a[1], interval_b[1])
    return [lower_bound, upper_bound]


# Assume input is a list of tuples, not always sorted.
def merge_all_intervals(intervals):
    # Sort by start of interval.
    intervals.sort(key=lambda tup: tup[0])  # Sort by first item in each tuple.
    output = []
    first_interval = intervals[0]
    current_interval = [first_interval[0], first_interval[1]]
    for i in range(1, len(intervals)):
        lower_bound, upper_bound = intervals[i]

        if current_interval is None:
            current_interval = [lower_bound, upper_bound]
            continue

        processing_interval = [lower_bound, upper_bound]
        # Check if lower_bound being processing is less than upper bound of current_interval.
        # If so then can merge.
        # Cases where can merge:
        #   1. Extends current_interval, lower_bound is > current_interval lower_bound but upper_bound is
        #       greater, so can stretch current_interval out.
        #   2. Contained in current_interval, lower_bound is <= current_interval lower_bound and upper_bound
        #       <= current_interval upper bound, so can squeeze it in.
        # Note: It is always the case as we iterate over the list that there will never be a lower_bound >
        # than current_interval's lower bound.
        if lower_bound < current_interval[1]:
            current_interval = merge_interval(current_interval, processing_interval)
        else:
            # Append a tuple.
            output.append(current_interval)
            current_interval = processing_interval
    if current_interval is not None:
        output.append(current_interval)
    return output


# intervals = [[1,3], [2,6], [8,10], [15,18]]
intervals = [[1,6], [1, 9], [2, 4], [4, 7], [0, 4], [-1, 6], [10, 14]]
output = merge_all_intervals(intervals)
print(output)
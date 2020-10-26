"""
@author: David Lei
@since: 13/08/2017

Given a total and a set of non negative integers, is there a subset in the set that add up to the total.

https://www.youtube.com/watch?v=s6FhG--P7z0
http://www.geeksforgeeks.org/dynamic-programming-subset-sum-problem/
http://algorithms.tutorialhorizon.com/dynamic-programming-subset-sum-problem/

2D matrix:
    sum going from 0 to total for the columns
    ordered ascending set elements on the rows

        0   1   2   3   4   5   6   7   8   9   10  11
    2   T   F   T   F   F   F   F   F   F   F   F   F
    3   T   F   T   T   Fx  Tx  F   F   F   F   F   F
    7   T   F   T   T   F   T   F   T   F   Ti  T   F
    8   T   F   T   T   F   T   T   T   T   To  T   T
    10  T   F   T   T   F   T   T   T   T   T   T   T

    col 0: to make 0, use empty set, so you can do it, set all to True
    row 0 (val = 2): for each col, can you make the value with just one 2?
        Note: Can't form 4 with just one 2.
    if you can make it with current value, get the one from above.

    Fx go up to F and take 3 steps to the left at the F under 1, so it's False

    Tx go up one row to F, take 3 steps to the left at the T under 2 so it's True meaning you can make 5 with one 3,
        then - 3 to the col value and you can make 2 with one two so it is True.

    Ti can form 9 with 7 and 2, go up one row (using the 7), go seven steps back as we have used seven and just need to
        form 9, is that True? yes so we can form two with the remaining 2 and 3.

    To if the above is True we can just set it as True because the row above To being True means we can make 9 with
        {7, 3 2}, if we can make 9 with that then we can definitely make 9 with {8, 7, 3, 2}.

    To find the subset, trace back in the matrix.
        1. check if True comes from above, if from above move up.
        2. if True is not form above, value at current row is in answer, go current_row_value steps to the left.
        3. when you get to the 0th col, you are done.
"""

def print_subset(dp_table):
    # TODO: Implement getting the solution when we know one exists.
    pass



def subset_sum(set_of_values, total):
    # set_of_values is assumed to be an ordered list of values.
    dp_table = [[0 for _ in range(0, total + 1)] for _ in range(len(set_of_values))]

    # Set 0th col to True.
    for row in dp_table:
        row[0] = 1

    # Loop over for first row.
    for val in range(1, total + 1):
        # Set col in first row to 1 if we can make the value with the first item in our set.
        dp_table[0][val] = 1 if val == set_of_values[0] else 0

    for row_index in range(1, len(set_of_values)):
        for col_index in range(1, total + 1):

            # Can make col value with current value in set.
            if col_index == set_of_values[row_index]:
                dp_table[row_index][col_index] = 1
                continue

            # Can make col value with other values in set already looked at.
            true_from_above = dp_table[row_index - 1][col_index]
            if true_from_above:
                dp_table[row_index][col_index] = 1
                continue

            # Go up a row using the current value and go current value steps to the left, check that.
            if col_index - set_of_values[row_index] >= 0:
                dp_table[row_index][col_index] = dp_table[row_index - 1][col_index - set_of_values[row_index]]
            else:
                dp_table[row_index][col_index] = 0

    return dp_table[len(set_of_values) - 1][total]

total = 11
set_of_values = [2, 3, 3, 7, 8, 10]

# Below examples should be True as well:

# set_of_values = [3, 2, 7, 1]
# total = 6

# set_of_values = [3, 34, 4, 12, 5, 2]
# set_of_values.sort()
# total = 9

# Works for this but might not work for other non neg sets?
# set_of_values = [-7, -3, -2, 5]
# total = 0

print(True if subset_sum(set_of_values, total) == 1 else False)


"""
@author: David Lei
@since: 11/08/2017
@modified: 


Given a value and denomination of coins, what it the maximum number of unique ways to make up the value.

Validate results with: https://prismoskills.appspot.com/lessons/Dynamic_Programming/Chapter_03_-_Max_ways_in_which_coins_can_make_a_sum.jsp

Also can submit on: https://www.hackerrank.com/challenges/ctci-coin-change/problem
"""

value = 10
denominations = [1, 3, 5]


def get_max_unique_ways_to_make_value(value, coins):
    dp_table = [[0 for _ in range(value + 1)] for _ in range(len(coins) + 1)]

    for coin_index in range(1, len(coins) + 1):
        # Skip first row, loop through all coins.
        for i in range(1, value + 1):
            # Loop from value 1 to value.
            value_from_above = dp_table[coin_index - 1][i]
            is_col_same_as_coin = 1 if i == coins[coin_index - 1] else 0
            value_to_the_left = dp_table[coin_index][i - coins[coin_index - 1]] if i - coins[coin_index - 1] >= 0 else 0
            dp_table[coin_index][i] = value_from_above + is_col_same_as_coin + value_to_the_left
    print("Max unique ways to form {0} with coins {1} is {2}".format(value, coins, dp_table[len(coins)][value]))


get_max_unique_ways_to_make_value(value, denominations)

""" Working out

Ways to make 10: 11
- 1 (x 10)
- 2 (x 1) + 1 (x 8)
- 2 (x 2) + 1 (x 6)
- 2 (x 3) + 1 (x 4)
- 2 (x 4) + 1 (x 2)
- 2 (x 5)
- 5 (x 1) + 1 (x 5)
- 5 (x 1) + 2 (x 1) + 1 (x 3)
- 5 (x 1) + 2 (x 2) + 1 (x 1)
- 5 (x 2)
- 10 (x 1)

1. For DP problems identify a pattern that uses sub solutions to build up a solution.

Above translated to a table
        0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
    0   0   0   0   0   0   0   0   0   0   0   0
    1   0   1   1   1   1   1   1   1   1   1   1
    2   0   1   2   2   3   3   4   4   5   5   6
    5   0   1   2   2   3   4   5   6   7   8   10
    10  0   1   2   2   3   4   5   6   8   9   11

    max_unique_ways = (above + 1 if col==coin + index - coin if in range)

Working out for coins of denomination 1 & 2.

value 4:
- 1 (x 4)
- 2 (x 1) + 1 (x 2)
- 2 (x 2)

value 5:
- 1 (x 5)
- 2 (x 1) + 1 (x 3)
- 2 (x 2) + 1 (x 2)

value 6:
- 1 (x 7)
- 2 (x 1) + 1 (x 4)
- 2 (x 2) + 1 (x 2)
- 2 (x 3)

value 7:
- 1 (x 7)
- 2 (x 1) + 1 (x 5)
- 2 (x 2) + 1 (x 3)
- 2 (x 3) + 1 (x 1)

value 8:
- 1 (x 8)
- 2 (x 1) + 1 (x 6)
- 2 (x 2) + 1 (x 4)
- 2 (x 3) + 1 (x 2)
- 2 (x 4)

value 9:
- 1 (x 9)
- 2 (x 1) + 1 (x 7)
- 2 (x 2) + 1 (x 5)
- 2 (x 3) + 1 (x 3)
- 2 (x 4) + 1 (x 1)

value 10:
- 1 (x 10)
- 2 (x 1) + 1 (x 8)
- 2 (x 2) + 1 (x 6)
- 2 (x 3) + 1 (x 4)
- 2 (x 4) + 1 (x 2)
- 2 (x 5)

Working out for coins of denomination 1 & 2 & 5.

value 5:
- 1 (x 5)
- 2 (x 1) + 1 (x 3)
- 2 (x 2) + 1 (x 1)
- 5 (x 1)

value 6:
- 1 (x 6)
- 2 (x 1) + 1 (x 4)
- 2 (x 2) + 1 (x 2)
- 2 (x 3)
- 5 (x 1) + 1 (x 1)

value 7:
- 1 (x 7)
- 2 (x 1) + 1 (x 5)
- 2 (x 2) + 1 (x 3)
- 2 (x 3) + 1 (x 1)
- 5 (x 1) + 1 (x 2)
- 5 (x 1) + 2 (x 1)

value 8:
- 1 (x 8)
- 2 (x 1) + 1 (x 6)
- 2 (x 2) + 1 (x 4)
- 2 (x 3) + 1 (x 2)
- 2 (x 4)
- 5 (x 1) + 1 (x 3)
- 5 (x 1) + 2 (x 1) + 1 (x 1)

value 9:
- 1 (x 9)
- 2 (x 1) + 1 (x 7)
- 2 (x 2) + 1 (x 5)
- 2 (x 3) + 1 (x 3)
- 2 (x 4) + 1 (x 1)
- 5 (x 1) + 1 (x 4)
- 5 (x 1) + 2 (x 1) + 1 (x 2)
- 5 (x 1) + 2 (x 2)

value 10:
- 1 (x 10)
- 2 (x 1) + 1 (x 8)
- 2 (x 2) + 1 (x 6)
- 2 (x 3) + 1 (x 4)
- 2 (x 4) + 1 (x 2)
- 2 (x 5)
- 5 (x 1) + 1 (x 5)
- 5 (x 1) + 2 (x 1) + 1 (x 3)
- 5 (x 1) + 2 (x 2) + 1 (x 1)
- 5 (x 2)

"""
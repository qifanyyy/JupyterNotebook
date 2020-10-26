"""
@author: David Lei
@since: 21/04/2017
@modified: 

Cleaner implementation of Minimum_Number_of_Coins.py
"""
import math


def find_coins(table, coins):
    # Start from solution (bottom right).
    # Coins only added in taking 1 from the current coin value.
    #
    # The total number of coins for a cell can only come form
    # 1. The top (same value as current cell).
    # 2. The left, 1 + value of another cell where cell to the left < current.
    row = len(table) - 1
    col = len(table[0]) - 1
    used_coins = []
    while True:
        if col == 0:  # Traversed entire table, we are done.
            break
        current_number_of_coins = table[row][col]

        # Number came from the top.
        if table[row - 1][col] == current_number_of_coins:
            row -= 1  # Start looking in prev row.
            continue

        # Number came from the left, subtract coins[row] from col index to get to next cell to look at.
        used_coins.append(coins[row - 1])
        col -= coins[row - 1]
    return used_coins


def get_min_coins(coins, total_value):
    table = [[math.inf] * (total_value + 1) for _ in range(len(coins) + 1)]
    for row in table:
        row[0] = 0  # 0 coins needed to make value of 0.

    # DP part.
    # Rows represent coins.
    # Columns represent values in range 0, 1, .., total_value.
    # Cell means, for this coin value and coin values for all rows above, what is the min way I can make this col value.
    for coin_row_index in range(len(coins)):
        for value_col in range(total_value):
            # + 1 as cols padded with 0, and rows padded with math.inf.
            table[coin_row_index + 1][value_col + 1] = min(
                # Use calculation from row above, already know can make value_col using the value at the row above.
                table[coin_row_index][value_col + 1],
                # Use 1 of this current coin (coins[coin_row_index], look back value_col - current_coin_value column
                # indexes to build upon sub-solution.
                1 + table[coin_row_index + 1][value_col - coins[coin_row_index] + 1]
            )

    min_coins_required = table[-1][-1]
    for row in table:
        print(row)
    coins_used = find_coins(table, coins)
    print("Min coins required: %s" % min_coins_required)
    print("Coins used: %s" % coins_used)

coins = [1, 2, 4, 6]
total_value = 13
get_min_coins(coins, total_value)

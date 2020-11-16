"""
@author: David Lei
@since: 25/08/2016
@modified: 

Given n items with v value, what should you take?
    - can only take 1 of each item

https://www.youtube.com/watch?v=8LusJS5-AGo&list=PLrmLmBdmIlpsHaNTPP_jHHDx_os9ItYXr
https://github.com/mission-peace/interview/blob/master/src/com/interview/dynamic/Knapsack01.java

Dynamic programming approach is bottom up
    - find solution to small problem --> build it

Recursive approach is top down
"""

# Bottom up approach.
def knapsack_iterative(items, bag_capacity):
    """
    Uses dp to find optimal solution to the one-zero (either take or leave)
    knapsack problem
    :param items: assumed given as a tuple of (space_it_takes_up, value)
    :param bag_capacity: given as an integer of the capacity of the bag
    :return: maximised value, items taken
    """

    table = [[0 for _ in range(bag_capacity + 1)] for _ in range(len(items))]  # typically have a first col of 0s

    first_item = items[0]
    for c in range(1, bag_capacity + 1):          # work out first row so can extend solution to other rows
        if first_item[0] <= c:                    # consider only the first item for all weights of the bag
            table[0][c] = first_item[1]           # set the value to the value of the first item
    # can only take each item at most once, so don't need to extend solution in first for loop

    for i in range(1, len(items)):                # loop for all items apart from the first, represents the row
        for j in range(1, bag_capacity + 1):      # loop for cumulative capacity of the bag, represents the column
            item = items[i]
            if item[0] <= j:                      # space item takes vs bag capacity (j), if we can take item

                table[i][j] = max(                        # take max of (remember can only take each item once)
                        table[i - 1][j],                      # - previous best, and leave this item
                        item[1] + table[i - 1][j - item[0]]   # - take this item and anything we can with the left space
                    )                                     # space by going up one row and going the the index with space
            else:                                 # no chance we can take the item, go with previous best
                table[i][j] = table[i - 1][j]
    # took_items = find_chosen(table, items)
    return table, []

def find_chosen(table, items):
    """
    to find the things chosen
        1. find solution
        2. check if solution came from above (from another value), if so go up
        3. check if solution came from this row, add the value represented by the row to output
    be careful of boundary cases

    using negative indexes to work our way up (yay python =])
    the first row will be - len(table) with - indexing
    """
    # TODO: Bug here, probs an edge case/off by one leading to infinite loop.
    took = []
    solution = table[-1][-1]
    current_value = solution
    row = -1
    col = -1
    while current_value > 0:
        # going up takes precedent over checking to the left, want to go up as much as possible first (i think)
        can_go_up = True
        while can_go_up:
            if row - 1 > - len(table):                                  # check if row - 1 will be out of bound
                if table[row - 1][col] == current_value:                # the current value came from here
                    row -= 1                                            # decrement row
                else:
                    break
            else:
                break
        if col - 1 > - len(table[0]):                               # check if col -= will be out of bound
            item_space = items[row][0]
            current_row_item_value = items[row][1]
            if table[row][col - item_space] + current_row_item_value == current_value:  # item from this row was selected
                took.append(items[row])
                col -= item_space                              # update column
                current_value -= current_row_item_value
    return took

def test(items, bag_capacity):
    """
    items = [(1,1), (3,4), (4,5), (5,7)]
    bag_capacity = 7

    correct table for youtube example
    [0, 1, 1, 1, 1, 1, 1, 1]
    [0, 1, 1, 4, 5, 5, 5, 5]
    [0, 1, 1, 4, 5, 6, 6, 9]
    [0, 1, 1, 4, 5, 7, 8, 9]
    """
    table, took_items = knapsack_iterative(items, bag_capacity)

    for row in table:
        print(row)
    print("Max value you can take: " + str(table[-1][-1]) + ", with bag capacity: " + str(bag_capacity))
    print("Items taken:")
    for item in took_items:
        print(" -  item space: " + str(item[0]) + ", item: value: " + str(item[1]))

if __name__ == "__main__":
    print("Testing scenario 1, expected 9")
    items = [(1,1), (3,4), (4,5), (5,7)]
    bag_capacity = 7
    test(items, bag_capacity)
    print("Testing scenario 2, expected 13")
    item_weights = [2, 2, 4, 5]
    item_values = [2, 4, 6, 9]
    bag_capacity = 8
    items = list(zip(item_weights, item_values))
    test(items, bag_capacity)
    print("Testing scenario 3, expected 90") # bug in find chosen here.
    item_weights = [5, 4, 6, 3]
    item_values = [10, 40, 30, 50]
    bag_capacity = 10
    items = list(zip(item_weights, item_values))
    items.sort(key=lambda t:t[0])
    test(items, bag_capacity)

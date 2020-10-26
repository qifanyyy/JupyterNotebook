# -*- coding: utf-8 -*-
"""
author: Xiaolou Huang
"""


# ============================== Counting Pond ================================
# Find the number of ponds connected together.
# Similar to counting islands problem.
# Ref: https://www.youtube.com/watch?v=o8S2bO3pmO4
def count_ponds(G):
    m = len(G)
    n = len(G[0])
    num_ponds = 0  # number of ponds

    # iterate through every element in matrix G
    for row in range(m):
        for col in range(n):
            # if find a pond, find all the connected ponds to prevent overlap counting
            if G[row][col] == '#':
                num_ponds += dfs(G, row, col)

    return num_ponds


# Helper function for count_ponds()
# explore all the connected ponds and reassign them to dry land to prevent overlap counting
def dfs(G, row, col):
    # base case
    if row < 0 or row >= len(G) or col < 0 or col >= len(G[row]) or G[row][col] == '-':
        return 0

    # change the '#' to '-', modify the character in a string
    temp = list(G[row])
    temp[col] = '-'
    G[row] = ''.join(temp)

    # recursively find all connected ponds
    dfs(G, row - 1, col)
    dfs(G, row + 1, col)
    dfs(G, row, col - 1)
    dfs(G, row, col + 1)
    dfs(G, row - 1, col - 1)
    dfs(G, row - 1, col + 1)
    dfs(G, row + 1, col - 1)
    dfs(G, row + 1, col + 1)

    return 1


# ======================== Longest Ordered Subsequence ========================
# Dynamic programming solution. Time: O(n^2), Space: O(n)
# Ref: https://www.youtube.com/watch?v=fV-TF4OvZpk&t=707s
def longest_ordered_subsequence(L):
    n = len(L)  # length of the list L
    dp = [1 for i in range(n)]  # init list dp for storing updated solution for sub-problem

    glo_max = 1  # the global max number of sub-sequence for current list. Will be changing as iterate through list L
    for i in range(n):  # for every number in list L
        cur_max = 0  # local max number of sub-sequence for all numbers before current position of i
        for j in range(i):  # sub-problem, update global max if find longer sub-sequence
            if L[i] > L[j]:  # if number in i position is greater than at j position, update the local max
                cur_max = max(cur_max, dp[j])
        dp[i] = cur_max + 1  # adding the length to whatever the previous length it attached to
        glo_max = max(glo_max, dp[i])  # update global max

    return glo_max


# =============================== Supermarket =================================
# Find the max profit for selling products within its deadlines.
# Using Greedy algorithm
# Ref: https://www.youtube.com/watch?v=zPtI8q9gvX8
def supermarket(Items):
    n = len(Items)

    # sorted items in descending order based on product profit px
    items_descending = list.copy(Items)
    items_descending.sort(key=lambda x: x[0])
    items_descending.sort(reverse=True)

    # a dictionary contains all possible deadlines as the keys (non-repeated)
    deadline_dict = {}
    for i in range(n):
        if Items[i][1] not in deadline_dict:
            deadline_dict[Items[i][1]] = 0

    # this list is used for putting profit in correct location
    order_check_lst = list(deadline_dict.keys())
    order_check_lst.sort()

    # put the most valuable product in the correct deadline
    # if that deadline is occupied, find the empty position on left
    deadline_lst = [0 for i in range(order_check_lst[-1] + 1)]
    for i in range(n):
        # if the right position for this item is not occupied, use it
        if deadline_lst[items_descending[i][1]] == 0:
            deadline_lst[items_descending[i][1]] = items_descending[i][0]
        # else if the position is occupied, find the position on left that is empty if any, and occupy it
        else:
            # 1st, find the right location of this element (or correct deadline)
            for j in range(len(order_check_lst)):
                if order_check_lst[j] == items_descending[i][1]:
                    # 2nd, iterate through all the position on left to find an empty spot for this item, if any
                    for k in range(j, -1, -1):
                        if deadline_lst[order_check_lst[k]] == 0:
                            deadline_lst[order_check_lst[k]] = items_descending[i][0]

    # add the values for optimal solution
    sum = 0
    for i in range(len(deadline_lst)):
        sum += deadline_lst[i]
    return sum


# =============================== Unit tests ==================================
def test_suite():
    if count_ponds(["#--------##-",
                    "-###-----###",
                    "----##---##-",
                    "---------##-",
                    "---------#--",
                    "--#------#--",
                    "-#-#-----##-",
                    "#-#-#-----#-",
                    "-#-#------#-",
                    "--#-------#-"]) == 3:
        print('passed')
    else:
        print('failed')

    if longest_ordered_subsequence([1, 7, 3, 5, 9, 4, 8]) == 4:
        print('passed')
    else:
        print('failed')
    if longest_ordered_subsequence([10, 9, 2, 5, 3, 7, 101, 18]) == 4:
        print('passed')
    else:
        print('failed')

    if supermarket([(50, 2), (10, 1), (20, 2), (30, 1)]) == 80:
        print('passed')
    else:
        print('failed')
    if supermarket([(20, 1), (2, 1), (10, 3), (100, 2), (8, 2), (5, 20), (50, 10)]) == 185:
        print('passed')
    else:
        print('failed')
    if supermarket([(20, 2), (15, 2), (10, 1), (5, 3), (1, 3)]) == 40:
        print('passed')
    else:
        print('failed')


if __name__ == '__main__':
    test_suite()

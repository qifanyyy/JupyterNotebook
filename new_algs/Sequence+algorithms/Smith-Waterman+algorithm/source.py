# File: Tutorial Assignment 1
# author: Zheyuan Zhou
# Student ID: 117010423
# Date: 03/08/2020
# Introduction: this is the file to implement local alignment and global alignment
# With the corresponding algorithms: Needleman- Wunsch algorithm and Smith-Waterman algorithm

import numpy as np

# Some Notation
# single arrow: left arrow = 1; up arrow = 2; tangent arrow = 3; no arrow = 0
# combine arrow: left + tangent = 13; left + up = 12; up + tangent = 23; left+up+tan = 123

# Constant Define
mismatch = -1
match = 1
indel = -3
result_list_v = [] # result list to store global alignments sequence v
result_list_w = [] # result list to store global alignments sequence w


# Name: local_alignment
# ---------------------------------------
# Input: two user input sequences: string v and string w
# Output: void
# Description: complete the table for local alignment
def local_alignment(string_v, string_w):
    print("start local alignment:")
    # initialize the local alignment table according to two input strings
    local_table = init_table(len(string_v)+1, len(string_w)+1)

    # first row and col init: pass, since all zeros for 1st col and row
    # complete the information in the rest table
    for current_row in range(1, len(string_v)+1):
        for current_col in range(1, len(string_w)+1):
            # match case
            if (string_v[current_row-1] == string_w[current_col-1]):
                # get the potential score for match, left indel and right indel
                slant = local_table[current_row-1][current_col-1][0] + match
                up = local_table[current_row-1][current_col][0] + indel
                left = local_table[current_row][current_col-1][0] + indel
                # use the compare function to return the optimal derection
                result = compare(slant, up, left)
                # check the optimal detection score,
                # since local alignment doesn't allow negative score
                # if negative score, change the entry to zero
                if result[0] <= 0:
                    result[0] = 0
                    result[1] = 0
                # update the entry in the local alignment table
                local_table[current_row][current_col][0] = result[0]
                local_table[current_row][current_col][1] = result[1]
            # mismatch case
            elif (string_v[current_row-1] != string_w[current_col-1]):
                # get the potential score for match, left indel and right indel
                slant = local_table[current_row-1][current_col-1][0] + mismatch
                up = local_table[current_row-1][current_col][0] + indel
                left = local_table[current_row][current_col-1][0] + indel
                # use the compare function to return the optimal derection
                result = compare(slant, up, left)
                # check the optimal detection score,
                # since local alignment doesn't allow negative score
                # if negative score, change the entry to zero
                if result[0] <= 0:
                    result[0] = 0
                    result[1] = 0
                # update the entry in the local alignment table
                local_table[current_row][current_col][0] = result[0]
                local_table[current_row][current_col][1] = result[1]
    print(local_table)
    # start backtracking for local alignment
    l_backtrack(local_table)
    return


# Name: l_backtrack
# ---------------------------------------
# Input: the completed local alignment table
# Output: all the local alignment results
# Description: pick out all the backtracking paths and print them in correct order
def l_backtrack(local_table):
    # find all the entries with max score, which are the start positions 
    init_pos = find_start_pos(local_table)
    tot_result = [] # list to store all the start positions
    #print(init_pos)
    for i in init_pos:
        result_v = [] # list to store all the start position coordinates
        # use the division to get the row
        row = i // (len(string_w)+1)
        # use the remainder to get the col
        col = i % (len(string_w)+1)
        # start tracking until meet the zero to stop
        while (local_table[row][col][0]!= 0):
            # in local alignment, each target entry should be match, if not, then wrong
            if (string_v[row-1]!=string_w[col-1]):
                print("wrong result: different letter!")
                return
            else:
                result_v.append(string_v[row-1])
                row -= 1
                col -= 1
        # finish one max starting position, append the path to list
        tot_result.append(result_v)

    # print local alignment result
    print("start to print local backtracking result:")
    # since backtracking, reverse the sequences to get correct answer
    for j in tot_result:
        j.reverse()
    # for each alignment, print the result
    for n in range(len(tot_result)):
        print("local alignment w", n+1, tot_result[n])
        print("local alignment v", n+1, tot_result[n])
        print("------------------------------------------------------")
    return 0


# Name: find_start_pos
# ---------------------------------------
# Input: the completed local alignment table
# Output: all the maximum index number
# Description: the index is in 1-demension, need further transformation
def find_start_pos(local_table):
    value_list = []
    index_list = []
    # load all the first value in each entry in local table to value list
    # dim: 1 * (m+1)(n+1)
    for i in range(len(string_v)+1):
        for j in range(len(string_w)+1):
            value_list.append(local_table[i][j][0])
    # print(value_list)
    # find the max value
    max_value = max(value_list)
    # print(max_value)
    # find all the index with max value
    for k in range(len(value_list)):
        if value_list[k] == max_value:
            index_list.append(k)
    # print(index_list)
    return index_list



# Name: global_alignment
# ---------------------------------------
# Input: user input string v and string w
# Output: all the global alignment paths
# Description: complete the global table, apply backtracking, print all the paths
def global_alignment(string_v, string_w):
    print("start global alignment: ")
    # initialize the local alignment table according to two input strings
    global_table = init_table(len(string_v)+1, len(string_w)+1)
    # first row and col initialize
    for current_col in range(1, len(string_w)+1):
        global_table[0][current_col][0] = global_table[0][current_col-1][0] + indel
        global_table[0][current_col][1] = 1
    for current_row in range(1, len(string_v)+1):
        global_table[current_row][0][0] = global_table[current_row-1][0][0] + indel
        global_table[current_row][0][1] = 2
    # rest entry completion
    for current_row in range(1, len(string_v)+1):
        for current_col in range(1, len(string_w)+1):
            # match case
            if (string_v[current_row-1] == string_w[current_col-1]):
                slant = global_table[current_row-1][current_col-1][0] + match
                up = global_table[current_row-1][current_col][0] + indel
                left = global_table[current_row][current_col-1][0] + indel
                result = compare(slant, up, left)
                # update the table with optimal derection and value
                global_table[current_row][current_col][0] = result[0]
                global_table[current_row][current_col][1] = result[1]
            # mismatch case
            elif (string_v[current_row-1] != string_w[current_col-1]):
                slant = global_table[current_row-1][current_col-1][0] + mismatch
                up = global_table[current_row-1][current_col][0] + indel
                left = global_table[current_row][current_col-1][0] + indel
                result = compare(slant, up, left)
                # update the table with optimal derection and value
                global_table[current_row][current_col][0] = result[0]
                global_table[current_row][current_col][1] = result[1]
    print(global_table)
    result_v = [] # store the backtracking paths information for v
    result_w = [] # store the backtracking paths information for w
    print("start to print global backtracking result:")
    g_backtrack(global_table, len(string_v), len(string_w), result_v, result_w, global_table[len(string_v)][len(string_w)][1])
    #print(result_list_v)
    #print(len(result_list_v))
    #print(result_list_w)
    #print(len(result_list_w))
    # print the result
    g_print(result_list_v, result_list_w)
    return 0



# Name: g_print
# ---------------------------------------
# Input: list v with all the alignments of v; list w with all the alignments of w
# Output: all the global alignments
# Description: the input list, achieved from recursion, is not correct, 
               # thus need further modification in this step
def g_print(list_v, list_w):
    temp_v = []
    temp_w = []
    v_length = len(list_v)
    w_length = len(list_w)
    # if the alignments from same pair are not same length, then wrong
    if w_length != v_length:
        print("wrong result: different length!")
        return
    # revive, slice the sequences to get the corrent alignment
    for i in range(v_length):
        if i == 0:
            temp_v.append(list_v[i])
        else:
            diff_len_v = len(list_v[i]) - len(list_v[i-1])
            cut_idx_v = len(list_v[0]) - diff_len_v
            result_v = list_v[i][0:cut_idx_v] + list_v[i][-diff_len_v:]
            temp_v.append(result_v)
    for j in range(w_length):
        if j == 0:
            temp_w.append(list_w[j])
        else:
            diff_len_w = len(list_w[j]) - len(list_w[j-1])
            cut_idx_w = len(list_w[0]) - diff_len_w
            result_w = list_w[j][0:cut_idx_w] + list_w[j][-diff_len_w:]
            temp_w.append(result_w)
    # print(temp_v)
    # print(temp_w)
    # print(len(temp_w))
    # print(len(temp_v))
    #print(len(temp_w[8]))
    # transform to reverse order
    for a in temp_v:
        a.reverse()
    for b in temp_w:
        b.reverse()
    # output the result 
    for n in range(len(temp_w)):
        print("global alignment w", n+1, temp_w[n])
        print("global alignment v", n+1, temp_v[n])
        print("------------------------------------------------------")
    return 0




# Name: g_backtrack
# ---------------------------------------
# Input: global_table, v, w, result_v, result_w, mode
# Output: list contain the potential global alignment results
# Description: this part is done by recursion, which lists all the possible paths
def g_backtrack(global_table, v, w, result_v, result_w, mode):
    # while not get to the original point (0,0), the loop continues
    while(v>0 or w>0):
        # mode 1 stands for entry with left arrow
        if (mode == 1): 
            result_v.append("-")
            result_w.append(string_w[w-1])
            mode = global_table[v][w-1][1]
            g_backtrack(global_table, v, w-1, result_v, result_w, mode)
        # mode 2 stands for entry with up arrow
        elif (mode == 2):
            result_v.append(string_v[v-1])
            result_w.append("-")
            mode = global_table[v-1][w][1]
            g_backtrack(global_table, v-1, w, result_v, result_w, mode)
        # mode 3 stands for entry with slant arrow
        elif (mode == 3):
            result_v.append(string_v[v-1])
            result_w.append(string_w[w-1])
            mode = global_table[v-1][w-1][1]
            g_backtrack(global_table, v-1, w-1, result_v, result_w, mode)
        # mode 13 stands for entry with both left arrow and slant arrow
        elif (mode == 13):
            g_backtrack(global_table, v, w, result_v, result_w, 1)
            g_backtrack(global_table, v, w, result_v, result_w, 3)
        # mode 13 stands for entry with both left arrow and up arrow
        elif (mode == 12):
            g_backtrack(global_table, v, w, result_v, result_w, 1)
            g_backtrack(global_table, v, w, result_v, result_w, 2)
        # mode 13 stands for entry with both up arrow and slant arrow
        elif (mode == 23):
            g_backtrack(global_table, v, w, result_v, result_w, 2)
            g_backtrack(global_table, v, w, result_v, result_w, 3)
        # mode 13 stands for entry with all the left arrow, up arrow and slant arrow
        elif (mode == 123):
            g_backtrack(global_table, v, w, result_v, result_w, 1)
            g_backtrack(global_table, v, w, result_v, result_w, 2)
            g_backtrack(global_table, v, w, result_v, result_w, 3)
        return
    #print(result_v)
    result_list_v.append(result_v[:])
    #print(result_w)
    result_list_w.append(result_w[:])




# Name: compare
# ---------------------------------------
# Input: the score value for three direction
# Output: list contain the potential global alignment results
# Description: this part actually determines the entry information
def compare(slant, up, left):
    # determine the max
    max_value = max(slant, up, left)
    # check situation, ended with different arrow possibility
    if (slant == max_value and up != max_value and left != max_value):
        return [max_value, 3]
    elif (slant != max_value and up == max_value and left != max_value):
        return [max_value, 2]
    elif (slant != max_value and up != max_value and left == max_value):
        return [max_value, 1]
    elif (slant == max_value and up == max_value and left != max_value):
        return [max_value, 23]
    elif (slant == max_value and up != max_value and left == max_value):
        return [max_value, 13]
    elif (slant != max_value and up == max_value and left == max_value):
        return [max_value, 12]
    elif (slant == max_value and up == max_value and left == max_value):
        return [max_value, 123]



# Name: init_table
# ---------------------------------------
# Input: the lengths of two strings
# Output: the initialized table
# Description: use NumPy to construct the table
def init_table(v_len, w_len):
    table = np.zeros([v_len, w_len], dtype = [('x', 'i4'), ('y', 'i4')])
    print(table)
    return table

# main function
def main():
    global string_v, string_w
    mode = "g"
    while (mode != "q"):
        mode = input("please choose the mode - l for local, g for global, q for quit: ")
        string_v = input("please input the v sequence: ")
        string_w = input("please input the w sequence: ")
        # strip all the spaces
        string_v = string_v.replace(" ", "")
        string_w = string_w.replace(" ", "")

        if (mode == "l"):
            local_alignment(string_v, string_w)
        elif (mode == "g"):
            global_alignment(string_v, string_w)
        elif (mode == "q"):
            quit(0)


# program starts
main()

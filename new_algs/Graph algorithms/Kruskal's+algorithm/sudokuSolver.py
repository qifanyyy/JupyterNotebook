# Purpose: Solve 9x9 sudoku puzzles using hash sets
# @author: Katie Hummel
# Reference: Data Structures and Algorithms with Python by Kent D. Lee and Steve Hubbard
# 9/19/18

import copy
from Sets.hashset import HashSet


# Return set of all possible values [1-9] if the character read in is a 'x'
def getSetVal(fileVal):
    if fileVal == 'x':
        return HashSet([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return HashSet([int(fileVal)])

# We must build a matrix to remember what we start off with
def buildMatrix(infile):
    infile = "Puzzles/" + infile
    matrix = []
    with open(infile) as file:
        for line in file:
            lst = line.split()
            row = []
            for i in range(0, len(lst)):
                row.append(getSetVal(lst[i]))
            matrix.append(row)
    return matrix

# Create a 'group', for lack of a better word, of all the rows, all the columns, and all the blocks, return
def buildGroups(matrix):
    # rows
    groups = list(matrix)

    # cols
    for i in range(9):
        col = []
        for j in range(9):
            col.append(matrix[j][i])
        groups.append(col)

    # blocks
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            block = []
            for k in range(3):
                for m in range(3):
                    block.append(matrix[k+i][m+j])
            groups.append(block)

    return groups

# Update the group based on the rules defined below
def reduceGroup(group):
    '''
    Rule 1:
    If the cardinality of the set (i.e. the number of items in the set) matches
    the number of duplicate sets found, then the items of the duplicate sets may
    safely be removed from all non-duplicate sets in the group.
    '''
    change = False
    for indexSet in group:
        numDuplicates = 0
        for otherSet in group:
            if indexSet == otherSet:
                numDuplicates += 1
        # Remove items in the duplicate set from non-duplicate sets
        if len(indexSet) == numDuplicates:
            for nonDuplicateSet in group:
                # Make sure that we're not removing items from the indexSet and that
                # there are changes to be made to the nonDuplicateSet, otherwise change
                # is falsely set to True
                if indexSet != nonDuplicateSet:
                    lenNonDuplicateSet = len(nonDuplicateSet)
                    nonDuplicateSet.difference_update(indexSet)
                    if lenNonDuplicateSet != len(nonDuplicateSet):
                        change = True
    '''
    Rule 2:
    Look at each cell within a group and throw away all items that appear in other
    cells in the group. If we are left with only one value in the chosen cell,
    then it must appear in this cell and the cell may be updated by throwing 
    away all other values that appear in the chosen cell.
    '''
    for indexSet in range(len(group)):
        # Copy so that we don't make permanent changes to the matrix until we validate
        # that those changes are what we want
        setCopy = copy.deepcopy(group[indexSet])
        if len(setCopy) != 1:
            for otherSet in range(len(group)):
                if otherSet != indexSet: # revise, index number
                    setCopy.difference_update(group[otherSet])
            # We were able to reduce to just one item in set, update the matrix
            if len(setCopy) == 1:
                group[indexSet].intersection_update(setCopy)
                change = True

    return change

# Keep looping through all the groups (i.e. rows, columns, and blocks) until we can no longer make changes
def reduceGroups(groups):
    changed = True
    while changed:
        changed = False
        for group in groups:
            if reduceGroup(group):
                changed = True

def main():
    fileName = input("Enter filename of Sudoku puzzle (press enter to quit): ")
    while fileName != "":
        try:
            matrix = buildMatrix(fileName)
            groups = buildGroups(matrix)
            reduceGroups(groups)
            for i in range(len(matrix)):
                for j in range(9):
                    print(str(matrix[i][j]).strip('[]') + " ", end=" ")
                print()
            print()
            fileName = input("Enter filename of Sudoku puzzle (press enter to quit): ")
        except FileNotFoundError:
            print()
            fileName = input("Invalid filename. Try again: ")


if __name__ == "__main__":
    main()

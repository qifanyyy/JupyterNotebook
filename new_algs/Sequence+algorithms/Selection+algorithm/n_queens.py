"""
@author: David Lei
@since: 17/04/2017
@modified: 

Problem:
- placing queens on a chess board so that no 2 queens threaten each other
- n queens for n rows meaning there can only be 1 queen per row.

Eg:

indexes:   0 1 2 3
        0 |0|1|0|0| 1 means a queen is placed, 0 means nothing is placed.
        1 |0|0|0|1|
        2 |1|0|0|0|
        3 |0|0|1|0|

Complexity analysis

Time Complexity:
- Best: Placement always works, O(n) for n rows.
- Worst: O(N! * N^2)

Space Complexity:
- O(n^2) use 1 board, where n is number of queens to place and board size is n*n.
"""


"""
Assume the time complexity of this function (solve()) is T(N - row_index), where N is the number of queens to place.
Let Place(N) be the complexity of the can_place_queen

T(N - row_index) = (N - row_index) * T(N - (row_index + 1)) + N * Place(N)
    Where:
        - (N - row_index) is the complexity for this recursive.
        - T(N - (row_index + 1)) is the complexity for the next recursive call on the next row
        - N is the complexity for all columns in this row
        - Place(N) is the complexity to check if a queen can be placed.

    In each solve(), can_place_queen is called N times for each column in the current row we are placing the queen in.
    If we ignore the diagonal cases (because that's hard to analysis), solve() is called (N - row_index) times.

So solve(0, board_config, n) will call solve(1, board_config, n), N times max, once for each column where the queen
can be placed. N is because there are no queens currently placed so all columns in row 0 are viable.

Each call of solve(1, board_config, n) will call solve(2, board_config, n),  N - 1 times max. N - 1 is because when a
queen is placed by solve(0, board_config, n), a column will be taken up (no other queen can be placed in that column).
Thus in the for loop for col_index in range(n), test_place_queen will be true at max N - 1 times.

Likewise solve(2, board_config, n) will call solve(3, board_config, n) N - 2 times as when placing a queen in row 3,
2 columns have already been taken up.

So the size of the recursion search tree is N * (N - 1) *  (N - 2) * ... * 2 * 1 => N!

Each node in the search tree will call can_place_queen() N times (in every iteration in the loop for col_index in range(n)).

Calling can_place_queen() is Place(N), doing this N times is O(N * Place(N)).

This can be done for every single node (recursive call) in the recursive search tree in the worst case (N! nodes/recursive calls).

So the total time complexity is O(N! * N * Place(N)) => O(N!*(N^2))
"""
def solve(row_index, board_config, n):
    # Search by column first (exhaust a row), then row (exhaust columns fully on last row).
    if row_index >= n:  # Exhausted rows indexes.
        return False

    for col_index in range(n):
        test_place_queen = can_place_queen(row_index, col_index, board_config, n)

        if test_place_queen:  # Can place queen, go to next row, start at col 0, try place others.
            board_config[row_index][col_index] = 1
            if row_index + 1 == n:
                return True
            solved = solve(row_index + 1, board_config, n)
            if solved:
                return True
            else:
                board_config[row_index][col_index] = 0
        # Check other column indexes.
    return False  # All columns checked.

"""
Time complexity: O(N)
Where N is the total number of queens (== num rows == num cols).
Loops through
- all rows in column current_col O(n)
- all columns in row current_row O(n)
- 2 diagonals (max length of a diagonal is n where board is of size n*n) = O(2n)
Total = O(4n) = O(n).
"""
def can_place_queen(current_row, current_col, board_config, n):
    # Test can place queen in row.
    for c in range(current_col + 1, n):  # Check rightwards.
        if board_config[current_row][c] == 1:
            return False
    for c in range(0, current_col):  # Check leftwards.
        if board_config[current_row][c] == 1:
            return False

    # Test can place queen in column.
    for r in range(current_row + 1, n):  # Check downwards.
        if board_config[r][current_col] == 1:
            return False
    for r in range(0, current_row):
        if board_config[r][current_col] == 1:
            return False

    # Test top right to bottom left diagonal.

    # Go to bottom left.
    temp_row, temp_col = current_row + 1, current_col - 1
    while temp_col >= 0 and temp_row < n:
        if board_config[temp_row][temp_col] == 1:
            return False
        temp_col -= 1
        temp_row += 1

    # Go to top right.
    temp_row, temp_col = current_row - 1, current_col + 1
    while temp_row >= 0 and temp_col < n:
        if board_config[temp_row][temp_col] == 1:
            return False
        temp_col += 1
        temp_row -= 1

    # Test top left to bottom right diagonal.

    # Go to bottom right.
    temp_row, temp_col = current_row + 1, current_col + 1
    while temp_row < n and temp_col < n:
        if board_config[temp_row][temp_col] == 1:
            return False
        temp_row += 1
        temp_col += 1

    # Go to top left.
    temp_row, temp_col = current_row - 1, current_col - 1
    while temp_row >= 0 and temp_col >= 0:
        if board_config[temp_row][temp_col] == 1:
            return False
        temp_row -= 1
        temp_col -= 1
    return True  # Can place queen


# Initialise variables.
n = 13
board = [[0] * n for _ in range(n)]
start_row = 0
start_col = 0

result = solve(start_row, board, n)
print(result)

# Print board
for row in board:
    s = ""
    for c in str(row):
        if c == "1":
            s += "Q"
        elif c == "0":
            s += "-"
        else:
            s += c
    print(s)

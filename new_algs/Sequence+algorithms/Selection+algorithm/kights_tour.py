"""
@author: David Lei
@since: 17/04/2017
@modified: 

Find the path for a knight on a chess board such that the knight visits every square only once.

Backtrack cases:
1. Dead end, no more paths (moves to take).
    1.1. Do backtrack and try another move.

Assuming knight can start anywhere.
Brute force approaches for small values of n.

Domain knowledge:
    Knights can move in L shapes

    For a 5x5 board.
         0 1 2 3 4
    0   | |x|u|x| |
    1   |x| |u| |x|
    2   |l|l|K|r|r|
    3   |x| |d| |x|
    4   | |x|d|x| |

TODO: Complexity Analysis
"""


def start_knights_tour(board, n, counter):
    for r in range(n):
        for c in range(n):  # O(n^2), where n is the number of rows/columns on the board.
            solved = find_tour(r, c, board, n, counter)
            if solved:
                return True
            # Try a different starting point.
    return False


def find_tour(current_row, current_col, board, n, counter):
    # Start at some position.
    board[current_row][current_col] = counter  # Knight is at this position.

    if n*n == counter:  # Visited all squares.
        return True

    # Get next possible positions.
    possible_moves = get_possible_moves(current_row, current_col, board, n)
    if not possible_moves:  # Exhausted all moves.
        # Undo this move as there is no where to go to.
        board[current_row][current_col] = 0
        return False
    while possible_moves:
        # Try a position.
        move = possible_moves.pop()
        # board[current_row][current_col] = counter + 1
        solved = find_tour(move[0], move[1], board, n, counter + 1)  # If pass, get next.
        if solved:
            return True
        # else:  # Not solved, backtrack.
        #    board[current_row][current_col] = 0
    board[current_row][current_col] = 0
    return False


def get_possible_moves(current_row, current_column, board_config, n):  # O(Move set) = O(1).
    possible_moves = []
    move_up_row = current_row - 2
    move_down_row = current_row + 2
    move_left_column = current_column - 2
    move_right_column = current_column + 2

    if move_up_row >= 0:  # Can move upwards.
        if current_column - 1 >= 0:  # Can move up left.
            # if (move_up_row, current_column - 1) not in previous_positions:
            if board_config[move_up_row][current_column - 1] == 0:  # Have not visited this spot yet.
                possible_moves.append((move_up_row, current_column - 1))
        if current_column + 1 < n:  # Can move up right.
            # if (move_up_row, current_column + 1) not in previous_positions:
            if board_config[move_up_row][current_column + 1] == 0:
                possible_moves.append((move_up_row, current_column + 1))

    if move_down_row < n:  # Can move down.
        if current_column - 1 >= 0:  # Can move down left.
            # if (move_down_row, current_column - 1) not in previous_positions:
            if board_config[move_down_row][current_column - 1] == 0:
                possible_moves.append((move_down_row, current_column - 1))
        if current_column + 1 < n:  # Can move down right.
            # if (move_down_row, current_column + 1) not in previous_positions:
            if board_config[move_down_row][current_column + 1] == 0:
                possible_moves.append((move_down_row, current_column + 1))

    if move_left_column >= 0:  # Can move to the left.
        if current_row - 1 >= 0:  # Can move left up.
            # if (current_row - 1, move_left_column) not in previous_positions:
            if board_config[current_row - 1][move_left_column] == 0:
                possible_moves.append((current_row - 1, move_left_column))
        if current_row + 1 < n:  # Can move left down.
            # if (current_row + 1, move_left_column) not in previous_positions:
            if board_config[current_row + 1][move_left_column] == 0:
                possible_moves.append((current_row + 1, move_left_column))

    if move_right_column < n:  # Can move right.
        if current_row - 1 >= 0:  # Can move right up.
            # if (current_row - 1, move_right_column) not in previous_positions:
            if board_config[current_row - 1][move_right_column] == 0:
                possible_moves.append((current_row - 1, move_right_column))
        if current_row + 1 < n:  # Can move right down.
            # if (current_row + 1, move_right_column) not in previous_positions:
            if board_config[current_row + 1][move_right_column] == 0:
                possible_moves.append((current_row + 1, move_right_column))

    return possible_moves

n = 5  # Naive backtracking algorithm can't handle board of size 8.
board = [[0]*n for _ in range(n)]
counter = 1
result = start_knights_tour(board, n, counter)
print(result)
validate = []
for row in board:
    for num in row:
        validate.append(num)
    print(row)
validate.sort()
print("Visited all places: " + str(validate == [x for x in range(1, n*n + 1)]))
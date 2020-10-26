"""
@author: David Lei
@since: 15/04/2017
@modified: 


- square cake
- R rows, C cols
- each cell has at most 1 initial
- no 2 children share same initial, no initial appears more than once

- soln always possible
- don't need to split cake evenly among children
- 1 or more may get a 1 x 1 piece

- objective: get a retangular cake for kids with only their initials, doesn't have to be same size.
"""
name = "A-large.out"
with open(name, "w") as fh:
    pass

def write_out(name, matrix, number):
    with open(name, "a") as fh:
        fh.write("Case #%s:\n" % number)
        for row in matrix:
            res = ""
            for char in row:
                res += char
            res += "\n"
            fh.write(res)




number_test_cases = int(input())

for t in range(number_test_cases):
    cake = []

    # R lines of C characters each representing cake.
    # if upper case english, cell is set.
    # if ? cell is blank.
    rows, columns = [int(x) for x in input().split(' ')]

    # Get my data.
    for r in range(rows):
        cake_row = list(input())
        cake.append(cake_row)

    # Don't need to deal with duplicate initials.

    # Loop through cake, extend each encountered character as left as possible.
    for row in cake:
        for c in range(len(row) - 1):
            if c == "?":
                continue
            if row[c+1] == "?":
                row[c+1] = row[c]
    # Loop through cake, extend each encountered character as right as possible.
    for row in cake:
        for c in range(len(row) -1, 0, -1):  # Loop from end to 2nd last char.
            if c == "?":
                continue
            if row[c-1] == "?":
                row[c-1] = row[c]

    # Only rows with just "?" left.

    # Loop through cake, extend rows upwards.
    for row_index in range(rows - 1):
        # Start from first row, if the row under is full of "?" copy through.
        row = cake[row_index]
        if row[0] == "?":  # This row is just "?" skip it.
            continue

        if not cake[row_index + 1][0] == "?":  # Next row is not just "?" skip.
            continue
        # Row should be all "?"
        if not cake[row_index + 1] == ["?" for _ in range(len(row))]:
            raise ValueError("BAD THINGS")

        for row_value_index in range(len(row)):
            cake[row_index + 1][row_value_index] = row[row_value_index]

    # Loop through cake, extend rows downwards.
    for row_index in range(len(cake)-1, 0, -1):  # Start from the bottom, go up.
        row = cake[row_index]
        if not cake[row_index -1][0] == "?":  # Next row is not just "?" skip.
            continue

        for row_value_index in range(len(row)):
            cake[row_index - 1][row_value_index] = row[row_value_index]


    write_out(name, cake, t + 1)
"""
@author: David Lei
@since: 7/11/2017

https://www.hackerrank.com/challenges/castle-on-the-grid/forum

Looks like a BFS except the notion of a shortest path is the shortest step and a step can
move > 1 cell. A step is any location vertical or horizontal which is not a X.

So do a bfs but instead of just checking +- 1 cell to the left, right, above and below we need
a function that returns all possible neighbours.

When we want to visit a neighbour, mark is as visited and append it to the queue.

Also note that (x, y) pairs represent (row, col) instead of (col, row) like we are used to.

Passed :)
"""

from collections import deque

def get_neighbours_can_visit_in_one_step(grid, current_x, current_y):
    neighbours = []
    # We only can visit a neighbour if it isn't "X, hasn't been visited before and we are current not at it.
    # Check if not visited using "." as we make it point to parent once visited.

    # From (current_x, current_y) want to check what you can reach from:
    # - current_x to 0
    # - current_x to end of column
    # - current_y to 0
    # - current_y ot end of row.
    # like so:
    #            (x-1, y)
    # (x, y-1)    (x, y)   (x, y+1)
    #            (x+1, y)
    # if any "X" encountered then we stop as it is a barrier we can't go through.

    # Check in current column, fix y value, change x value.
    #   Check from current_x to end of column.
    for i in range(current_x + 1, len(grid[0])):  # Don't need to check bound as current_y + 1 if >= len(gird) will not execute.
        if grid[i][current_y] == "X":
            break
        elif grid[i][current_y] == ".":
            neighbours.append((i, current_y))
    #   Check from current_x to start of column.
    for i in range(current_x - 1, -1, -1):
        if grid[i][current_y] == "X":
            break
        elif grid[i][current_y] == ".":
            neighbours.append((i, current_y))

    # Check in current row, fix x value, change y value.
    #   Check from current_y to end of row..
    for i in range(current_y + 1, len(grid)):
        if grid[current_x][i] == "X":
            break
        elif grid[current_x][i] == ".":
            neighbours.append((current_x, i))
    #   Check from current_y to start of row.
    for i in range(current_y - 1, -1, -1):
        if grid[current_x][i] == "X":
            break
        elif grid[current_x][i] == ".":
            neighbours.append((current_x, i))
    return neighbours


def minimumMoves(grid, startX, startY, goalX, goalY):
    if startX == goalX and startY == goalY:
        return 0
    # Complete this function
    grid[startX][startY] = (-1, -1)
    queue = deque([(startX, startY)])
    found_goal = False
    while queue and not found_goal:
        node = queue.popleft()
        neighbours = get_neighbours_can_visit_in_one_step(grid, node[0], node[1])
        for neighbour in neighbours:
            if neighbour == (goalX, goalY):
                grid[neighbour[0]][neighbour[1]] = node  # Make it point to parent.
                found_goal = True
                break  # Found shortest path to goal.
            grid[neighbour[0]][neighbour[1]] = (node[0], node[1])  # Make it point to parent.
            queue.append(neighbour)
    steps = 0
    current_x = goalX
    current_y = goalY
    while True:
        parent = grid[current_x][current_y]
        current_x = parent[0]
        current_y = parent[1]
        steps += 1
        if current_x == startX and current_y == startY:
            return steps


if __name__ == "__main__":
    n = int(input().strip())
    grid = []
    for _ in range(n):
        grid.append([x for x in input().strip()])
    startX, startY, goalX, goalY = input().strip().split(' ')
    startX, startY, goalX, goalY = [int(startX), int(startY), int(goalX), int(goalY)]
    result = minimumMoves(grid, startX, startY, goalX, goalY)
    print(result)
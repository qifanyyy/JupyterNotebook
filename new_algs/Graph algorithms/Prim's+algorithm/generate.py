"""Maze Generating Program using Breadth-First Search and Recursive Backtracking Algorithms"""
import pygame
import random


class Tiles(object):
    """
    Object Properties: X: x-position of the AI
                       Y: y-position of the AI
                       Count: index of each tile in list
                       Walls: list of boolean values representing the top,right,bottom,left walls of each tile
                       Visited: State representing if tile has been visited or not
                       Current: State representing if the AI is on the current tile

    """
    def __init__(self, x, y, count):
        self.x = x
        self.y = y
        self.count = count
        self.walls = [True, True, True, True]
        self.visited = False
        self.current = False

    def board(self, cells):
        """
        Draw each cell and its walls
        :param cells:
        :return: None
        """
        if cells.current:
            pygame.draw.rect(win, AiColor, (cells.x, cells.y, diff, diff))
            cells.visited, cells.current = True, True
            visited.append(cells)

        if not cells.walls[0]:
            pygame.draw.line(win, linecol, [cells.x, cells.y], [cells.x + diff, cells.y], 2)
        if not cells.walls[1]:
            pygame.draw.line(win, linecol, [cells.x + diff, cells.y], [cells.x + diff, cells.y + diff], 2)
        if not cells.walls[2]:
            pygame.draw.line(win, linecol, [cells.x, cells.y + diff], [cells.x + diff, cells.y + diff], 2)
        if not cells.walls[3]:
            pygame.draw.line(win, linecol, [cells.x, cells.y], [cells.x, cells.y + diff], 2)

    def checkNeighbors(self, num):
        """
        Check if neighbors of a node have been visited.
        :param num: index of current tile
        :return: List of neighbors that have NOT been visited yet by the algorithm
        """
        empty = []
        try:
            if not tiles[num + 1].visited and num + 1 <= len(tiles):
                if tiles[num + 1].y != 0:
                    empty.append(tiles[num + 1])
            if not tiles[num - 1].visited and num - 1 >= 0:
                if tiles[num - 1].y != height - diff:
                    empty.append(tiles[num - 1])
            if num + cols <= len(tiles) and not tiles[num + cols].visited:
                empty.append(tiles[num + cols])
            if not tiles[num - rows].visited and num - cols >= 0:
                empty.append(tiles[num - cols])

            if not empty:
                return 0
            else:
                chosen = rand(empty)
                return chosen
        except IndexError:
            pass

    def removeWalls(self, tile1, tile2):
        """
        Removes corresponding wall using index differences between the previous and current tiles
        and re-draws the updates cells accordingly
        :param tile1: Previous Tile the algorithm WAS on
        :param tile2: Current Tile the algorithm IS on
        :return: None
        """
        if tile1.count - tile2.count == -1:
            tile1.walls[2], tile2.walls[0] = False, False

        elif tile1.count - tile2.count == 1:
            tile1.walls[0], tile2.walls[2] = False, False

        elif tile1.count - tile2.count == rows:
            tile1.walls[3], tile2.walls[1] = False, False

        elif tile1.count - tile2.count == -rows:
            tile1.walls[1], tile2.walls[3] = False, False

        tile1.board(tile1)
        tile2.board(tile2)


def rand(arr):
    """
    Randomly chooses a number
    :param arr: List with 4 nums representing a wall
    :return: randomly chosen number
    """
    choice = random.choice(arr)
    return choice


def keepItOn():
    """
    Keeps the window open to allow viewer time for finding a path to the end;
    Draws the starting and ending positions for the maze
    :return: None
    """
    #  pygame.draw.rect(win, (255, 0, 100), (tiles[len(tiles) - 1].x, tiles[len(tiles) - 1].y, diff, diff))
    #  pygame.draw.rect(win, (255, 255, 0), (tiles[0].x, tiles[0].y, diff, diff))
    while True:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()


pygame.init()
width, height, diff = 800, 800, 40
linecol, AiColor, winColor = (0, 0, 0), (152, 254, 255), (255, 255, 255)
count, tiles, visited, rows, cols, condition = 0, [], [], width//diff, height//diff, False
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze Generator")
win.fill(winColor)
clock = pygame.time.Clock()

for row in range(rows):
    for col in range(cols):
        tile = Tiles(row*diff, col*diff, count)
        tiles.append(tile)
        tile.board(tile)
        count += 1

nextTile = tiles[0]
nextTile.current = True
oldTile = nextTile

y = 0
x = 0
while True:
    pygame.draw.line(win, (0, 0, 0), [0, diff + y], [width, diff + y], 2)
    pygame.draw.line(win, (0, 0, 0), [diff + x, 0], [diff + x, height], 2)
    y += diff
    x += diff
    if y == height - diff and x == width - diff:
        break

#  Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        else:
            break

    if nextTile.current:  # Keep track of previous and next tile using temp variables
        nextTile.removeWalls(oldTile, nextTile)
        oldTile = nextTile
        pygame.display.update()

    nextTile = nextTile.checkNeighbors(nextTile.count)
    while nextTile is None or nextTile == 0:  # If no unvisited neighbors, pop visited list until one if found
        if not visited:
            condition = True
            break
        else:
            temp = visited.pop()
            oldTile = temp
            nextTile = temp.checkNeighbors(temp.count)

    if not condition:
        nextTile.current = True

    else:
        x = [0, 1, 2, 3]
        for cells in tiles:
            if not cells.visited:
                cells.walls[random.choice(x)] = False
                cells.board(cells)

        keepItOn()

    clock.tick(1000)

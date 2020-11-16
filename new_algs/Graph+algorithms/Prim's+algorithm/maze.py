from tkinter import *
from random import seed
import random
import time
import cv2
import math
import numpy as np

seed()

# constants
CELL_SIZE = 60
GRID_WIDTH = 15
GRID_HEIGHT = 15
LINE_THICKNESS = 6

# location of cell marked as entrance
ENTER_LOCATION = (0, 0)

# True if you want to slow down animation to demonstrate algorithm
DEMONSTRATION_MODE = False
PRINT_PICTURES = True

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# setup tkinter canvas
height = int(GRID_HEIGHT * CELL_SIZE)
width = int(GRID_WIDTH * CELL_SIZE)
tk = Tk()
canvas = Canvas(tk, width=width, height=height)
canvas.pack()

out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (width, height))


class Wall:
    def __init__(self, first_cell, second_cell):
        self.first_cell = first_cell
        self.second_cell = second_cell

        # weight of each edge, i.e. how likely this wall is to be selected from the list of active walls
        # self.weight = 1

        # can switch to this line to demonstrate how changing weights changes overall shape of maze
        self.weight = math.sqrt(first_cell[0]**2+first_cell[1]**2)*first_cell[1]**20 + math.sqrt(first_cell[0]**2+first_cell[1]**2)*first_cell[0]**20 + math.sqrt(first_cell[0]**2+first_cell[1]**2)*second_cell[1]**20 + math.sqrt(first_cell[0]**2+first_cell[1]**2)*second_cell[0]**20

        # orientation is 1 for horizontal, 0 for vertical wall
        self.orientation = abs(first_cell[0] - second_cell[0])

    # unused function but I kept it in because you never know, but just prints all info about a wall
    def print_wall(self):
        print("My first cell is", self.first_cell)
        print("My second cell is", self.second_cell)
        if self.orientation == 0:
            print("I am a vertical wall")
        else:
            print("I am a horizontal wall")

    # drawn a wall object. takes passage as an argument, and draws it in blue/background
    # color if passage to make it look like there's no wall
    def draw_wall(self, canvas, color, passage):
        if passage == 1:
            # determine if horizontal or vertical
            if self.orientation == 1:
                canvas.create_rectangle(self.second_cell[1] * CELL_SIZE + LINE_THICKNESS / 2 + 1,
                                        self.second_cell[0] * CELL_SIZE - LINE_THICKNESS / 2,
                                        (self.second_cell[1] + 1) * CELL_SIZE - LINE_THICKNESS / 2 - 1,
                                        self.second_cell[0] * CELL_SIZE + LINE_THICKNESS / 2, fill=color, outline=color)
            else:  # it's vertical
                canvas.create_rectangle(self.second_cell[1] * CELL_SIZE - LINE_THICKNESS / 2,
                                        self.first_cell[0] * CELL_SIZE + LINE_THICKNESS / 2 + 1,
                                        self.second_cell[1] * CELL_SIZE + LINE_THICKNESS / 2,
                                        (self.first_cell[0] + 1) * CELL_SIZE - LINE_THICKNESS / 2 - 1, fill=color,
                                        outline=color)
        else:
            if self.orientation == 1:
                canvas.create_rectangle(self.second_cell[1] * CELL_SIZE - LINE_THICKNESS / 2 + 1,
                                        self.second_cell[0] * CELL_SIZE - LINE_THICKNESS / 2,
                                        (self.second_cell[1] + 1) * CELL_SIZE + LINE_THICKNESS / 2,
                                        self.second_cell[0] * CELL_SIZE + LINE_THICKNESS / 2, fill=color, outline=color)
            else:  # it's vertical
                canvas.create_rectangle(self.second_cell[1] * CELL_SIZE - LINE_THICKNESS / 2 + 1,
                                        self.first_cell[0] * CELL_SIZE - LINE_THICKNESS / 2,
                                        self.second_cell[1] * CELL_SIZE + LINE_THICKNESS / 2 + 1,
                                        (self.first_cell[0] + 1) * CELL_SIZE + LINE_THICKNESS / 2, fill=color,
                                        outline=color)

    # override equality operator, walls are equal if they have same position and same orientation
    def __eq__(self, other):
        if other is not None:
            if self.orientation == other.orientation and self.first_cell[0] == other.first_cell[0] and \
                    self.first_cell[1] == other.first_cell[1] and self.second_cell[1] == other.second_cell[1] and \
                    self.second_cell[0] == other.second_cell[0]:
                return True


class Cell:
    # main purpose of even having a cell object is to easily generate the walls around a certain cell position just
    # by initializing the cell object at that position
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.Walls = []
        # up
        if (ypos - 1) >= 0:
            self.Walls.append(Wall((xpos, ypos - 1), (xpos, ypos)))
        # down
        if (ypos + 1) <= (GRID_WIDTH - 1):
            self.Walls.append(Wall((xpos, ypos), (xpos, ypos + 1)))
        # left
        if (xpos - 1) >= 0:
            self.Walls.append(Wall((xpos - 1, ypos), (xpos, ypos)))
        # right
        if (xpos + 1) <= (GRID_HEIGHT - 1):
            self.Walls.append(Wall((xpos, ypos), (xpos + 1, ypos)))

    def print_cell(self):
        print("This is the cell", (self.xpos, self.ypos))


class Maze:
    def __init__(self, canvas, starting_cell, demonstration_mode, print_pictures):
        self.canvas = canvas
        self.passage_walls = self.generate_maze(starting_cell, demonstration_mode, print_pictures)

        self.visited_positions = []

        self.positions = [[[] for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]

        for wall in self.passage_walls:
            row = wall.first_cell[0]
            col = wall.first_cell[1]
            if wall.orientation == 1:
                self.positions[row][col].append((1, 0))
                self.positions[row + 1][col].append((-1, 0))
            else:
                self.positions[row][col + 1].append((0, -1))
                self.positions[row][col].append((0, 1))

    def generate_maze(self, starting_cell, demonstration_mode=False, print_pictures=False):
        if demonstration_mode:
            wait = 1
        else:
            wait = 0

        active_walls = []

        # walls that have been broken down to create a passage
        passage_walls = []

        # cells that have been visited so far
        maze_cells = []

        # start in the top left corner
        first_cell = starting_cell
        # turn it into a Cell object to get its walls
        first_Cell = Cell(first_cell[0], first_cell[1])

        maze_cells.append(first_cell)
        # start with the walls of the first cell
        for wall in first_Cell.Walls:
            active_walls.append(wall)

            # measure total weight, pick an active wall based on weight
        while len(active_walls) > 0:
            total_weight = 0
            for w in active_walls:
                total_weight += w.weight

            # randomly pick wall from list of active walls, with probability based on weights
            n = random.random() * total_weight
            lower_weight = 0
            target_index = 0
            for i in range(len(active_walls)):
                upper_weight = lower_weight + active_walls[i].weight
                if lower_weight <= n <= upper_weight:
                    target_index = i
                    break
                lower_weight = upper_weight
            active_wall = active_walls[target_index]

            self.draw_maze(active_walls, passage_walls, maze_cells, wait, active_wall=active_wall)
            #
            if active_wall.first_cell not in maze_cells:
                maze_cells.append(active_wall.first_cell)
                added_cell = Cell(active_wall.first_cell[0], active_wall.first_cell[1])
                for i in added_cell.Walls:
                    active_walls.append(i)
                passage_walls.append(active_wall)

            elif active_wall.second_cell not in maze_cells:
                maze_cells.append(active_wall.second_cell)
                added_cell = Cell(active_wall.second_cell[0], active_wall.second_cell[1])
                for i in added_cell.Walls:
                    active_walls.append(i)
                passage_walls.append(active_wall)

            active_walls.remove(active_wall)

            # remove potential duplicates
            for i in active_walls:
                if active_wall == i:
                    active_walls.remove(i)

        if print_pictures:
            output = print_picture(passage_walls)
            cv2.imwrite("oof.png", output)
            out.write(output)  # write each image to the AVI file
        return passage_walls

    def is_valid_direction(self, row, col, direction):
        return direction in self.positions[row][col]

    def draw_maze(self, active_walls, current_passage_walls, cells, wait=0.0, active_wall=None):
        for k in range(GRID_HEIGHT):
            self.canvas.create_rectangle(0, k * CELL_SIZE, width, k * CELL_SIZE, fill="black",
                                         width=LINE_THICKNESS)

        for k in range(GRID_WIDTH):
            self.canvas.create_rectangle(k * CELL_SIZE, 0, k * CELL_SIZE, height, fill="black",
                                         width=LINE_THICKNESS)

        for cell in cells:
            self.canvas.create_rectangle((cell[1]) * CELL_SIZE + LINE_THICKNESS / 2,
                                         (cell[0]) * CELL_SIZE + LINE_THICKNESS / 4,
                                         ((cell[1]) + 1) * CELL_SIZE - LINE_THICKNESS / 2,
                                         ((cell[0]) + 1) * CELL_SIZE - LINE_THICKNESS / 2, fill="blue")

        for wall in active_walls:
            wall.draw_wall(self.canvas, 'green', 0)

        if active_wall is not None:
            active_wall.draw_wall(self.canvas, 'magenta', 0)

        for wall in current_passage_walls:
            wall.draw_wall(self.canvas, 'blue', 1)

        time.sleep(wait)
        tk.update()
        self.canvas.delete("all")

    def solve_maze(self):
        path = []
        if self.explore(ENTER_LOCATION[0], ENTER_LOCATION[1], path):
            # clear visited positions once done solving to only show final path
            self.visited_positions = []
            self.draw_maze_solving(path, wait=5)
            return path

        return []

    def explore(self, row, col, path):
        position = (row, col)

        if row < 0 or col < 0 or row >= GRID_HEIGHT or col >= GRID_WIDTH or position in self.visited_positions:
            return False

        path.append(position)
        self.visited_positions.append(position)
        self.draw_maze_solving(path)

        if col == GRID_WIDTH - 1 and row == GRID_HEIGHT - 1:
            return True

        for direction in DIRECTIONS:
            # if is_valid_direction(maze, row, col, direction):
            if maze.is_valid_direction(row, col, direction):
                if self.explore(row + direction[0], col + direction[1], path):
                    return True

        path.pop()
        self.draw_maze_solving(path)

        return False

    def draw_maze_solving(self, path, wait=0):
        self.canvas.create_rectangle(0, 0, width, height, fill="blue")

        for k in range(GRID_HEIGHT):
            self.canvas.create_rectangle(0, k * CELL_SIZE, width, k * CELL_SIZE, fill="black",
                                         width=LINE_THICKNESS)

        for k in range(GRID_WIDTH):
            self.canvas.create_rectangle(k * CELL_SIZE, 0, k * CELL_SIZE, height, fill="black",
                                         width=LINE_THICKNESS)

        for passage in maze.passage_walls:
            passage.draw_wall(self.canvas, 'blue', 1)

        # draw little squares to represent visited positions
        for pos in self.visited_positions:
            self.canvas.create_rectangle((pos[1]) * CELL_SIZE + LINE_THICKNESS / 2 + CELL_SIZE / 4,
                                         (pos[0]) * CELL_SIZE + LINE_THICKNESS / 2 + CELL_SIZE / 4,
                                         ((pos[1]) + 1) * CELL_SIZE - LINE_THICKNESS / 2 - CELL_SIZE / 4,
                                         ((pos[0]) + 1) * CELL_SIZE - LINE_THICKNESS / 2 - CELL_SIZE / 4, fill="yellow")

        # draw little squares to represent current "working" path
        for pos in path:
            self.canvas.create_rectangle((pos[1]) * CELL_SIZE + LINE_THICKNESS / 2 + CELL_SIZE / 4,
                                         (pos[0]) * CELL_SIZE + LINE_THICKNESS / 2 + CELL_SIZE / 4,
                                         ((pos[1]) + 1) * CELL_SIZE - LINE_THICKNESS / 2 - CELL_SIZE / 4,
                                         ((pos[0]) + 1) * CELL_SIZE - LINE_THICKNESS / 2 - CELL_SIZE / 4, fill="red")

        tk.update()
        time.sleep(wait)
        self.canvas.delete("all")


# makes the actual writable image using cv2 and np by imitating what TK does,
# just called at the end to generate final image
def print_picture(walls):
    image = np.zeros((height, width, 3), np.uint8)  # start with blank image
    image[:, :] = (255, 255, 255)  # color blank image white

    # horizontal lines
    for i in range(GRID_HEIGHT):
        cv2.line(image, (0, i * CELL_SIZE), (width, i * CELL_SIZE), color=(0, 0, 0), thickness=LINE_THICKNESS)

    # vertical lines
    for i in range(GRID_WIDTH):
        cv2.line(image, (i * CELL_SIZE, 0), (i * CELL_SIZE, height), color=(0, 0, 0), thickness=LINE_THICKNESS)

    # draw all passages in white to blend in with background
    for i in walls:
        if i.orientation == 1:
            top_left = (int(i.second_cell[1] * CELL_SIZE + LINE_THICKNESS // 2 + 1),
                        int(i.second_cell[0] * CELL_SIZE - LINE_THICKNESS // 2))
            bottom_right = (int((i.second_cell[1] + 1) * CELL_SIZE - LINE_THICKNESS // 2 - 1),
                            int(i.second_cell[0] * CELL_SIZE + LINE_THICKNESS // 2))
        else:
            top_left = (int(i.second_cell[1] * CELL_SIZE - LINE_THICKNESS // 2),
                        int(i.first_cell[0] * CELL_SIZE + LINE_THICKNESS // 2 + 1))
            bottom_right = (int(i.second_cell[1] * CELL_SIZE + LINE_THICKNESS // 2),
                            int((i.first_cell[0] + 1) * CELL_SIZE - LINE_THICKNESS // 2 - 1))
        cv2.rectangle(image, top_left, bottom_right, color=(255, 255, 255), thickness=-1)

    # maze bounds around the whole maze
    cv2.rectangle(image, (0, 0), (width, height), color=(0, 0, 0), thickness=LINE_THICKNESS)
    return image


for i in range(4):
    maze = Maze(canvas, ENTER_LOCATION, DEMONSTRATION_MODE, PRINT_PICTURES)
    print(maze.solve_maze())
tk.destroy()

# after everything, have to put this to finalize TK so it doesn't keep crashing...
tk.mainloop()

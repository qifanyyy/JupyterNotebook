import cv2
import numpy as np
import random
import argparse

# Flags for picking the start and target points
start_was_picked = False
target_was_picked = False
start_row = None
start_col = None
target_row = None
target_col = None

# Callback function for mouse event
def mark_points(event, x, y, flags, param):
    global start_was_picked, target_was_picked
    global start_row, start_col
    global target_row, target_col

    if start_was_picked and target_was_picked:
        return
    elif start_was_picked:
        if event == cv2.EVENT_LBUTTONDOWN:
            target_row = y
            target_col = x
            target_was_picked = True
    else:
        if event == cv2.EVENT_LBUTTONDOWN:
            start_row = y
            start_col = x 
            start_was_picked = True

# Parse the arguments from terminal
parser = argparse.ArgumentParser()
parser.add_argument('rows_cols', nargs='*', type=int, help='Number of rows and columns in maze')
parser.add_argument('--start', default=[-1, -1], type=int, nargs=2, help='The location of a starting cell in (row, col) format, e.g., --start 4 5 for row 4 and column 5')
parser.add_argument('--target', default=[-1, -1], type=int, nargs=2, help='The location of a target cell in (row, col) format, e.g., --target 4 5 for row 4 and column 5')
parser.add_argument('-b', '--skip_building_animation', action='store_true', help='Skips the step-by-step demonstration of how the maze is built.')
parser.add_argument('-s', '--skip_searching_animation', action='store_true', help='Skips the step-by-step demonstration of searching algorithm.')

# Color values
red = (0, 0, 1)
blue = (1, 0, 0)
dark_green = (8 / 255, 68 / 255, 0 / 255)
bright_green = (122 / 255, 245 / 255, 167 / 255)

# Maze window parameters
wait_time = 1
window_name = 'maze'
cell_size = 20


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.visited_path = False
        self.neighbors = []
        self.explored = False
        self.pair = None

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.unvisited = self.rows * self.cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        for r in range(rows):
            for c in range(cols):
                self.grid[r][c] = Cell(r, c)
        
        self.maze = np.zeros((cell_size * self.rows + 1, cell_size * self.cols + 1, 3))
        self.start_was_picked = False
        self.target_was_picked = False
            

    def in_bounds(self, r, c):
        return r >= 0 and r < self.rows and c >= 0 and c < self.cols

    def get_neighbors(self, row, col):
        deltas = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        neighbors = []
        for d in deltas:
            r = row + d[0]
            c = col + d[1]
            if self.in_bounds(r, c) and not self.grid[r][c].visited:
                neighbors.append([r, c])
        return neighbors

    def prims_generator(self):
        start_row = random.randint(0, self.rows-1)
        start_col = random.randint(0, self.cols-1)
        args = parser.parse_args()
        skip_building = args.skip_building_animation
        
        self.grid[start_row][start_col].visited = True
        self.unvisited -= 1
        visited = [start_row * self.cols + start_col]

        while self.unvisited:
            while True:
                index = random.randint(0, len(visited)-1)
                current = visited[index]
                curr_row = current // self.cols
                curr_col = current % self.cols

                neighbors = self.get_neighbors(curr_row, curr_col)
                if len(neighbors) < 2:
                    visited.remove(current)
                if len(neighbors) > 0:
                    break

            index = random.randint(0, len(neighbors)-1)
            [row, col] = neighbors[index]
            visited.append(row * self.cols + col)
            self.grid[row][col].visited = True

            self.grid[curr_row][curr_col].neighbors.append([row, col])
            self.grid[row][col].neighbors.append([curr_row, curr_col])


            row_from = min(curr_row, row)
            row_to = max(curr_row, row)
            col_from = min(curr_col, col)
            col_to = max(curr_col, col)
            # Draw the line from current
            pt1_x = col_from * cell_size + 1
            pt1_y = row_from * cell_size + 1
            pt2_x = (col_to + 1) * cell_size - 1
            pt2_y = (row_to + 1) * cell_size - 1
            cv2.rectangle(self.maze, (pt1_x, pt1_y), (pt2_x, pt2_y), (255, 255, 255), thickness=-1)
            
            if not skip_building:
                cv2.imshow(window_name, self.maze)
                cv2.waitKey(wait_time)

            self.unvisited -= 1

        cv2.imwrite('maze.jpg', self.maze * 255)

    def mark_cell(self, cell_index, color):
        pt1_x = cell_index % self.cols * cell_size + 1
        pt1_y = cell_index // self.cols * cell_size + 1
        pt2_x = (cell_index % self.cols + 1) * cell_size - 1
        pt2_y = (cell_index // self.cols + 1) * cell_size - 1

        cv2.rectangle(self.maze, (pt1_x, pt1_y), (pt2_x, pt2_y), color, thickness=-1)

    def get_neighbors_path(self, row, col):
        deltas = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        neighbors = []
        for d in deltas:
            r = row + d[0]
            c = col + d[1]
            if self.in_bounds(r, c) and not self.grid[r][c].visited_path and not self.grid[r][c].explored:
                if [row, col] in self.grid[r][c].neighbors:
                    neighbors.append([r, c])
        return neighbors
                

    def find_path(self):
        self.grid[self.start // self.cols][self.start % self.cols].visited_path = True
        queue = [[self.start, None]]
        args = parser.parse_args()
        skip_searching = args.skip_searching_animation

        while len(queue):
            cell_pair = queue.pop(0)
            cell = cell_pair[0]
            cell_row = cell // self.cols
            cell_col = cell % self.cols
            self.grid[cell_row][cell_col].explored = True
            self.grid[cell_row][cell_col].pair = cell_pair[1]
            neighbors = self.get_neighbors_path(cell_row, cell_col)

            if cell != self.start and cell != self.stop:
                self.mark_cell(cell, bright_green)
            
            if not skip_searching:
                cv2.imshow(window_name, self.maze)
                cv2.waitKey(wait_time)
            for [r, c] in neighbors:
                queue.append([r * self.cols + c, cell])
                self.grid[r][c].visited_path = True
                if r * self.cols + c == self.stop:
                    self.grid[self.stop // self.cols][self.stop % self.cols].pair = cell
                    cv2.imshow(window_name, self.maze)
                    cv2.waitKey()

                    # Backtrack here
                    current = cell
                    while current != self.start:
                        curr_row = current // self.cols
                        curr_col = current % self.cols
                        prev = self.grid[curr_row][curr_col].pair
                        if prev == self.start:
                            cv2.imwrite('found_path.jpg', self.maze * 255)
                            return
                        
                        row = prev // self.cols
                        col = prev % self.cols

                        row_from = min(curr_row, row)
                        row_to = max(curr_row, row)
                        col_from = min(curr_col, col)
                        col_to = max(curr_col, col)
                        # Draw the line from current
                        pt1_x = col_from * cell_size + 1
                        pt1_y = row_from * cell_size + 1
                        pt2_x = (col_to + 1) * cell_size - 1
                        pt2_y = (row_to + 1) * cell_size - 1
                        cv2.rectangle(self.maze, (pt1_x, pt1_y), (pt2_x, pt2_y), dark_green, thickness=-1)

                        cv2.imshow(window_name, self.maze)
                        cv2.waitKey(wait_time)
                        
                        current = prev
                    break
        
    def initialize_points(self):
        args = parser.parse_args()
        if args.start != [-1, -1]:
            strt_row = min(max(0, args.start[0]), self.rows-1)
            strt_col = min(max(0, args.start[1]), self.cols-1)
        else:
            strt_row = random.randint(0, self.rows-1)
            strt_col = random.randint(0, self.cols-1)
        
        self.start = strt_row * self.cols + strt_col

        if args.target != [-1, -1]:
            stop_row = min(max(0, args.target[0]), self.rows-1)
            stop_col = min(max(0, args.target[1]), self.cols-1)
        else:
            stop_row = random.randint(0, self.rows-1)
            stop_col = random.randint(0, self.cols-1)
        self.stop = stop_row * self.cols + stop_col

        
        cv2.setMouseCallback(window_name, mark_points)
        while True:
            cv2.imshow(window_name, self.maze)

            if start_was_picked and not self.start_was_picked:
                global start_row
                global start_col
                start_row = start_row // cell_size
                start_row = min(start_row, self.rows)
                start_col = start_col // cell_size
                start_col = min(start_col, self.cols)
                self.start = start_row * self.cols + start_col
                self.start_was_picked = True
                self.mark_cell(self.start, blue)

            if target_was_picked and not self.target_was_picked:
                global target_row
                global target_col
                target_row = target_row // cell_size
                target_row = min(target_row, self.rows)
                target_col = target_col // cell_size
                target_col = min(target_col, self.cols)
                self.stop = target_row * self.cols + target_col
                self.target_was_picked = True
                break
            
            if cv2.waitKey(1) > 0:
                break
        
        self.mark_cell(self.start, blue)
        self.mark_cell(self.stop, red)
        
        cv2.imwrite('maze_with_points.jpg', self.maze * 255)

    
if __name__ == "__main__":
    args = parser.parse_args()
    if len(args.rows_cols) == 0:
        rows = random.randint(3, 50)
        cols = random.randint(3, 50)
    elif len(args.rows_cols) == 1:
        rows = args.rows_cols[0]
        cols = random.randint(3, 50)
    else:
        [rows, cols] = args.rows_cols[:2]

    cv2.namedWindow(window_name, flags=cv2.WINDOW_AUTOSIZE)

    g = Grid(rows, cols)
    g.prims_generator()
    g.initialize_points()
    cv2.imshow(window_name, g.maze)
    cv2.waitKey()
    g.find_path()
    cv2.imshow(window_name, g.maze)
    cv2.waitKey()
    cv2.destroyAllWindows()

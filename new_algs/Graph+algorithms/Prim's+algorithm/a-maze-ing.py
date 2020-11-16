''''
My first implementation of a maze generator using pygame and Prim's algorithm.
http://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm
Once created the maze is solved using the A* pathfinding algorithm
'''
import random
import pygame

# GLOBAL VARIABLES
RESOLUTION = (705, 705) # the resolution must be the cell size multiplied by an odd number
CELL_SIZE = (5, 5)
N_COLS = int(RESOLUTION[0] / CELL_SIZE[0])
N_ROWS = int(RESOLUTION[1] / CELL_SIZE[1])
WALL_COLOR = (0, 0, 0)
PATH_COLOR = (255, 255, 255)
FRONTIER_COLOR = (0, 0, 255)
START_COLOR = (0, 255, 0)
END_COLOR = (255, 0, 0)
EVALUATED_COLOR = (255, 255, 0)
BEST_PATH_COLOR = (255, 0, 255)
FPS = 1000

class Cell():
    '''A block on the screen'''
    def __init__(self, row, col):
        self.color = WALL_COLOR
        self.rect = pygame.Rect((col, row), (CELL_SIZE[0] - 1, CELL_SIZE[1] - 1))
        self.dist_to_end = 0.0 # heuristic component of A*
        self.steps_cost = 0 # steps taken to reach this cell
        self.total_cost = 0.0 # heuristic + the steps i took to get here
        self.neighbors = [] # list of the adjacent path
        self.previous = None # the node it came from to get here

    def get_index(self):
        '''Given a cell returns its index in the array of cells'''
        col = int(self.rect.left / CELL_SIZE[0])
        row = int((self.rect.top / CELL_SIZE[1]) * N_COLS)
        return row + col

    def heuristic(self, goal):
        '''Compute the heuristic cost of the cell'''
        col = abs(self.rect.centerx - goal.rect.centerx)
        row = abs(self.rect.centery - goal.rect.centery)
        self.dist_to_end = col + row

    def compute_total_cost(self):
        '''Set total cost to the sum of the costs'''
        self.total_cost = self.dist_to_end + self.steps_cost



class Simulation:
    '''A class to handle the simulation loop and events'''
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.simulation_over = False
        self.game_display = pygame.display.get_surface()
        self.cells = [] # list of all the cells
        self.maze = [] # list of the cells that aren't walls
        self.evaluated_cells = [] # closedSet for A* algorithm
        self.cells_to_evaluate = [] # openSet for A* algorithm
        self.cells_to_update = [] # update only a list of cells to optimize the draw function
        self.frontiers = []
        for row in range(N_ROWS):
            for col in range(N_COLS):
                self.cells.append(Cell(row * CELL_SIZE[1], col * CELL_SIZE[0]))
        self.cells[0].color = PATH_COLOR
        self.maze.append(self.cells[0])
        self.cells_to_update.append(self.cells[0].rect)
        self.add_frontiers(self.cells[0])
        self.start = self.cells[0]
        self.end = self.cells[-1]

    def main_loop(self):
        '''Simulation loop'''
        while not self.simulation_over:
            self.events()
            self.draw()
            self.update()

    def events(self):
        '''Handle pygame events'''
        if pygame.event.get(pygame.QUIT):
            self.simulation_over = True
        pygame.event.clear()

    def draw(self):
        '''Draw the path on the screen and keeps the walls' color on the background'''
        self.game_display.fill(WALL_COLOR)
        for cell in self.maze:
            pygame.draw.rect(self.game_display, cell.color, cell.rect)
        pygame.display.update(self.cells_to_update)
        self.cells_to_update.clear()

    def update(self):
        '''Update pygame and create maze'''
        self.clock.tick(FPS)
        if self.frontiers:
            self.prim_algorithm()
        elif self.start.color == PATH_COLOR:
            # for each sell in the maze add its neighbors
            # self.start = random.choice(self.maze) # uncomment these two lines
            # self.end = random.choice(self.maze)   # to randomly pick start & end
            for cell in self.maze:
                self.add_neighbors(cell)
                cell.heuristic(self.end)
            self.start.color = START_COLOR
            self.end.color = END_COLOR
            self.cells_to_evaluate.append(self.start)
            self.cells_to_update.append(self.start)
            self.cells_to_update.append(self.end)
        else:
            self.solve_the_maze()

    def add_neighbors(self, cell):
        '''Add to the cell's neighbors list the adjacent cells that are paths'''
        possible_neighbors = self.get_neighbors(cell)
        for neighbor in possible_neighbors:
            if neighbor.color == PATH_COLOR:
                cell.neighbors.append(neighbor)

    def get_neighbors(self, cell):
        '''Return the list of a cell's adjacent cells'''
        neighbors = []
        cell_index = cell.get_index()
        if cell.rect.left >= CELL_SIZE[0]:
            neighbors.append(self.cells[cell_index - 1])
        if cell.rect.top >= CELL_SIZE[1]:
            neighbors.append(self.cells[cell_index - N_COLS])
        if cell.rect.right <= RESOLUTION[0] - CELL_SIZE[0]:
            neighbors.append(self.cells[cell_index + 1])
        if cell.rect.bottom <= RESOLUTION[1] - CELL_SIZE[1]:
            neighbors.append(self.cells[cell_index + N_COLS])
        return neighbors.copy()

    def add_frontiers(self, cell):
        '''Add a cell's frontiers to the frontiers' list'''
        frontiers = self.get_frontiers(cell)
        for frontier in frontiers:
            if frontier.color == WALL_COLOR:
                frontier.color = FRONTIER_COLOR
                self.frontiers.append(frontier)
                self.maze.append(frontier)
                self.cells_to_update.append(frontier)

    def get_frontiers(self, cell):
        '''Return a list containing the cell's frontiers'''
        frontiers = []
        cell_index = cell.get_index()
        if cell.rect.left >= (CELL_SIZE[0] * 2):
            frontiers.append(self.cells[cell_index - 2])
        if cell.rect.top >= (CELL_SIZE[1] * 2):
            frontiers.append(self.cells[cell_index - 2 * N_COLS])
        if cell.rect.right <= RESOLUTION[0] - CELL_SIZE[0] * 2:
            frontiers.append(self.cells[cell_index + 2])
        if cell.rect.bottom <= RESOLUTION[1] - CELL_SIZE[1] * 2:
            frontiers.append(self.cells[cell_index + 2 * N_COLS])
        return frontiers.copy()

    def carve_passage(self, cell):
        '''Find the wall between two cells and make it part of the maze'''
        frontiers = self.get_frontiers(cell)
        path_frontiers = []
        for frontier in frontiers:
            if frontier.color == PATH_COLOR:
                path_frontiers.append(frontier)
        # Select a random direction to follow for carving the passage
        frontier = random.choice(path_frontiers)
        path_index = frontier.get_index()
        wall_index = cell.get_index()
        difference = wall_index - path_index
        new_path = Cell(0, 0)
        if difference == 2: # carve the wall on the right
            new_path = self.cells[path_index + 1]
        elif difference == -2: # carve the wall on the left
            new_path = self.cells[path_index - 1]
        elif difference == 2 * N_COLS: # carve the wall above
            new_path = self.cells[path_index + N_COLS]
        elif difference == -2 * N_COLS: # carve the wall below
            new_path = self.cells[path_index - N_COLS]
        # Make the separating wall part of the maze
        new_path.color = PATH_COLOR
        self.maze.append(new_path)
        self.cells_to_update.append(new_path.rect)
        cell.color = PATH_COLOR

    def prim_algorithm(self):
        '''Implementation of Randomized Prim's algorithm'''
        # Pick a random frontier
        target = random.choice(self.frontiers)
        # Carve a passage between the frontier and the adjacent path
        self.carve_passage(target)
        self.frontiers.remove(target)
        # Add new frontiers
        self.add_frontiers(target)

    def solve_the_maze(self):
        '''Implementation of A* algorithm'''
        if self.cells_to_evaluate:
            # cheapest is the cell in the open set with the lowest "cost"
            cheapest = self.cells_to_evaluate[0]
            for cell in self.cells_to_evaluate:
                if cell.total_cost < cheapest.total_cost:
                    cheapest = cell
            if cheapest == self.end:
                # reached the end
                previous = cheapest.previous
                while previous != self.start:
                    previous.color = BEST_PATH_COLOR
                    self.cells_to_update.append(previous)
                    previous = previous.previous
                return
            # cheapest has been evaluated
            self.cells_to_evaluate.remove(cheapest)
            self.evaluated_cells.append(cheapest)
            if cheapest != self.start:
                cheapest.color = EVALUATED_COLOR
            self.cells_to_update.append(cheapest)
            for neighbor in cheapest.neighbors:
                # if the cell hasn't been already evaluated
                if not neighbor in self.evaluated_cells:
                    # evaluate cell
                    temp_steps = cheapest.steps_cost + 1
                    if neighbor in self.cells_to_evaluate and temp_steps < neighbor.steps_cost:
                        neighbor.steps_cost = temp_steps
                    else:
                        neighbor.steps_cost = temp_steps
                        self.cells_to_evaluate.append(neighbor)
                    neighbor.compute_total_cost()
                    neighbor.previous = cheapest
        else:
            return
            # no solution

def main():
    '''Initialize a window and start the simulation'''
    pygame.init()
    pygame.display.set_caption("Maze Generator")
    pygame.display.set_mode(RESOLUTION)
    pygame.display.get_surface().set_alpha(None)
    pygame.event.set_allowed(pygame.QUIT)
    sim = Simulation()
    pygame.display.get_surface().fill(WALL_COLOR)
    pygame.display.flip()
    sim.main_loop()
    pygame.quit()
    quit(0)

if __name__ == "__main__":
    main()

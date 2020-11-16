from utils.cell import cell
from utils.algorithms import *
from utils.configuration import *

def removeWalls(currentCell,nextCell):
        x = int(currentCell.x / cellWidth) - int(nextCell.x / cellWidth)
        y = int(currentCell.y / cellWidth) - int(nextCell.y / cellWidth)
        if(x == -1):
            currentCell.cellWalls[1] = False
            nextCell.cellWalls[3] = False
        elif(x == 1):
            currentCell.cellWalls[3] = False
            nextCell.cellWalls[1] = False
        elif(y == -1):
            currentCell.cellWalls[2] = False
            nextCell.cellWalls[0] = False
        elif(y == 1):
            currentCell.cellWalls[0] = False
            nextCell.cellWalls[2] = False

class maze(object):
    def __init__(self, surface):
        self.mainGrid = []
        self.stack=[]
        self.surface = surface
        self.nodes_number = 0
        self.connections_number = 0
        for y in range(rows):
             self.mainGrid.append([])
             for x in range(cols):
                  self.mainGrid[y].append(cell(x,y, self.mainGrid, WHITE, self.surface))
                  self.nodes_number = self.nodes_number + 1
        self.currentCell = self.mainGrid[0][0]
        self.nextCell = 0
        self.stopGenerating = False

    def generate(self):
        self.connections_number = 0
        while not self.stopGenerating:
            self.currentCell.visited = True
            self.currentCell.active = True
    
            self.nextCell = self.currentCell.checkNeighbors()
    
            if self.nextCell != False:
                self.currentCell.neighbors = []
        
                self.stack.append(self.currentCell)
        
                removeWalls(self.currentCell,self.nextCell)
        
                self.currentCell.active = False
        
                self.currentCell = self.nextCell
    
            elif len(self.stack) > 0:
                self.currentCell.active = False
                self.currentCell = self.stack.pop()
        
            elif len(self.stack) == 0:
                grid = []
                try:
                    for y in range(rows):
                        grid.append([])
                        for x in range(cols):
                            grid[y].append(Cell(x,y))
                except:
                    self.stopGenerating = True
                    return
                self.currentCell = grid[0][0]
                self.nextCell = 0

    def draw(self):
        for y in range(rows):
            for x in range(cols):
                self.mainGrid[y][x].draw()

    def count_connections(self):
        cells_tab = []
        for y in range(rows):
            for x in range(cols):
                for neighbor in Algorithms.getNeighbours(self.mainGrid[y][x]):
                    if(neighbor not in cells_tab):
                        cells_tab.append(neighbor)
                        self.connections_number = self.connections_number + 1
        cells_tab.clear()

    @staticmethod
    def clear_grid(mainGrid):
        for y in range(rows):
            for x in range(cols):
                    mainGrid[y][x].cellWalls = [False, False, False, False]
        for i in range(cols):
            mainGrid[0][i].cellWalls = [True, False, False, False]
            mainGrid[rows-1][i].cellWalls = [False, False, True, False]
        for j in range(rows):
            mainGrid[j][0].cellWalls = [False, False, False, True]
            mainGrid[j][cols-1].cellWalls = [False, True, False, False]
        mainGrid[0][0].cellWalls = [True, False, False, True]
        mainGrid[0][cols-1].cellWalls = [True, True, False, False]
        mainGrid[rows-1][0].cellWalls = [False, False, True, True]
        mainGrid[rows-1][cols-1].cellWalls = [False, True, True, False]

    def load_level_1(self):
        maze.clear_grid(self.mainGrid)

    def load_level_2(self):
        maze.clear_grid(self.mainGrid)
        self.mainGrid[13][13].cellWalls = [True, True, True, True]
        self.mainGrid[13][13].color = BLACK
        for i in range(5, 13): 
            self.mainGrid[13][i].cellWalls = [True, True, True, True]
            self.mainGrid[i][13].cellWalls = [True, True, True, True]
            self.mainGrid[13][i].color = BLACK
            self.mainGrid[i][13].color = BLACK
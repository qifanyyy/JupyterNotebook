from utils.configuration import *

class cell(object):
    def __init__(self, x, y, grid, color, surface):
        self.x = x*cellWidth
        self.y = y*cellWidth
        self.grid = grid
        self.color = color
        self.surface = surface
        
        self.visited = False
        self.active = False
        self.cellWalls = [True,True,True,True] #top, right, bottom, left

        self.neighbors = []
        self.topNeighbor = 0
        self.bottomNeighbor = 0
        self.leftNeighbor = 0
        self.rightNeighbor = 0

        self.nextCell = 0
        if(mazeSeed!=0):
            random.seed(mazeSeed)

    def __lt__(self, other):
        if(self.x == other.x):
            return self.y < other.y
        else:
            return self.x < other.x

    def __gt__(self, other):
        if(self.x == other.x):
            return self.y > other.y
        else:
            return self.x > other.x


    def checkNeighbors(self):
        """solution based on Wilson's algorithm for generating a maze
            Returning self.nextCell next position in neighbors[] to check"""
        if(int(self.y / cellWidth) - 1 >= 0):
            self.topNeighbor = self.grid[int(self.y / cellWidth) - 1][int(self.x / cellWidth)]
        
        if(int(self.x / cellWidth) + 1 <= cols - 1):
            self.rightNeighbor = self.grid[int(self.y / cellWidth)][int(self.x / cellWidth) + 1]
        
        if(int(self.y / cellWidth) + 1 <= rows - 1):
            self.bottomNeighbor = self.grid[int(self.y / cellWidth) + 1][int(self.x / cellWidth)]
        
        if(int(self.x / cellWidth) - 1 >= 0):
            self.leftNeighbor = self.grid[int(self.y / cellWidth)][int(self.x / cellWidth) - 1]

        #adding to stack
        if self.topNeighbor != 0:
            if self.topNeighbor.visited == False:
                self.neighbors.append(self.topNeighbor)
        if self.rightNeighbor != 0:
            if self.rightNeighbor.visited == False:
                self.neighbors.append(self.rightNeighbor)
        if self.bottomNeighbor != 0:
            if self.bottomNeighbor.visited == False:
                self.neighbors.append(self.bottomNeighbor)
        if self.leftNeighbor != 0:
            if self.leftNeighbor.visited == False:
                self.neighbors.append(self.leftNeighbor)
        
        #randomly choosing next apex on stack
        if len(self.neighbors) > 0:
            self.nextCell = self.neighbors[random.randrange(0,len(self.neighbors))]
            return self.nextCell
        else:
            return False

    def draw(self):
        if(self.active == True):
            pygame.draw.rect(self.surface,self.color,(self.x,self.y,cellWidth,cellWidth))
        else:
            pygame.draw.rect(self.surface,self.color,(self.x,self.y,cellWidth,cellWidth))

        #WALLS
        if(self.cellWalls[0] == True):
            pygame.draw.line(self.surface,BLACK,(self.x,self.y),((self.x + cellWidth),self.y),wallWidth) #top
        if(self.cellWalls[1] == True):
            pygame.draw.line(self.surface,BLACK,((self.x + cellWidth),(self.y + cellWidth)),((self.x + cellWidth),self.y),wallWidth) #right
        if(self.cellWalls[2] == True):
            pygame.draw.line(self.surface,BLACK,(self.x,(self.y + cellWidth)),((self.x+ cellWidth),(self.y + cellWidth)),wallWidth) #bottom
        if(self.cellWalls[3] == True):
            pygame.draw.line(self.surface,BLACK,(self.x,self.y),(self.x,(self.y + cellWidth)),wallWidth) #left
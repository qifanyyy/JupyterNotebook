import sys, math, random
import pygame

from PrimsMaze import *
# import os
# os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()

class spot:

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.neighbors = []
        self.previous = None

        self.wall = False

        self.fScore = 0
        self.gScore = 0
        self.h = 0

    def addNeighbors(self,grid):
        x = self.x
        y = self.y
        if (y > 0):
            self.neighbors.append(grid.g[x][y-1])
        if (y < grid.nCols-1):
            self.neighbors.append(grid.g[x][y+1])
        if (x > 0):
            self.neighbors.append(grid.g[x-1][y])
        if (x < grid.nRows-1):
            self.neighbors.append(grid.g[x+1][y])

        #Diagonal Neighbors
        if(x > 0 and y > 0):
            self.neighbors.append(grid.g[x-1][y-1])
        if(x < grid.nRows-1 and y < grid.nCols-1):
            self.neighbors.append(grid.g[x+1][y+1])
        if(x > 0 and y < grid.nCols-1):
            self.neighbors.append(grid.g[x-1][y+1])
        if(x < grid.nRows-1 and y > 0):
            self.neighbors.append(grid.g[x+1][y-1])

    def RandomWalls(self):
        """This can be used to make random wall placements in grid system"""
        if(random.random() < 0.3):
            self.wall = True

class grid:

    def __init__(self, nCols, nRows):
        self.g = [ [None]*nCols for _ in range(nRows) ]
        self.nCols = nCols
        self.nRows = nRows

        self.path = []
        self.end = None

        self.MakeGrid()         #Make grid of spots
        self.GetNeighbors()     #Give spots neighbors

    def MakeGrid(self):
        """Makes all grid points a spot, so we can get cost values"""
        for i in range(len(self.g)):
            for j in range(len(self.g[0])):
                self.g[i][j] = spot(i,j)

    def GetNeighbors(self):
        """This makes all connections to see neighbors"""
        for i in range(len(self.g)):
            for j in range(len(self.g[0])):
                self.g[i][j].addNeighbors(self)

    def setEnd(self,end):
        self.end = end

    def GetPath(self):

        temp = self.end
        self.path = []
        self.path.append(temp)
        while(temp.previous):
            self.path.append(temp.previous)
            temp = temp.previous
        return self.path

def heuristic(curr,end):
    """This heuristic is just using the idea of distance to the end to get to the H score"""
    h = math.sqrt((end.x-curr.x)**2 + (end.y-curr.y)**2)
    #h = abs(end.x-curr.x) + abs(end.y-curr.y)
    return h

#---------------------
print("Start.")
#---------------------

rows, cols = 50, 50

size = width, height = 1000, 1000

cw = math.floor(width / cols)
ch = math.floor(height / rows)

black = 0, 0, 0
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
white = 255, 255, 255

screen = pygame.display.set_mode(size)

#---------------------
Grid = grid(rows, cols)                             # Make 10x10 grid system
start = Grid.g[0][0]                                # Start and Finish Nodes
end = Grid.g[Grid.nRows - 1][Grid.nCols - 1]
Grid.setEnd(end)

# Generate random wall placements
# for i in range(len(Grid.g)):
#     for j in range(len(Grid.g[0])):
#         if(Grid.g[i][j] != start and Grid.g[i][j] != end):
#             Grid.g[i][j].RandomWalls()

# Generate map using PrimsMaze
WallMap = generate_maze(cols, rows, complexity=0.50, density=0.75)

for i in range(len(Grid.g)):
    for j in range(len(Grid.g[0])):
        if(Grid.g[i][j] != start and Grid.g[i][j] != end):
            Grid.g[i][j].wall = WallMap[i][j]

openSet = []
closedSet = []

openSet.append(start)                               # gives Current Start
#----------------------

while 1:
    #  Loop handeling for drawing
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # A* solution process
    if(len(openSet) > 0):

        lowest = 0
        for i in range(len(openSet)):
            if( openSet[i].fScore < openSet[lowest].fScore ):
                lowest = i

        current = openSet[lowest]

        if(current == end):
            path = Grid.GetPath()
            print("Solved!")

        openSet.remove(current)   # need to remove current from the openSet list
        closedSet.append(current)

        neighbors = current.neighbors
        for n in neighbors:

            if(n not in closedSet and not n.wall):
                tentG = current.gScore + 1      # for this case always 1
                newPath = False
                if n in openSet:
                    if tentG < n.gScore:
                        n.gScore = tentG
                        newPath  = True
                else:
                    n.gScore = tentG
                    newPath = True
                    openSet.append(n)
                if newPath:
                    n.previous = current
                    n.h = heuristic(n,end)
                    n.fScore = n.gScore + n.h

    elif(len(Grid.path) <= 0):
        print("No Solution!")
        break

    #Drawing
    if len(Grid.path) <= 0 :
        screen.fill(black)
        for row in range(Grid.nRows):
            for col in range(Grid.nCols):
                #Openset spots colored green
                if(Grid.g[row][col] in openSet):
                    pygame.draw.rect(screen, green, [cw*col, ch*row, cw-1, ch-1])
                #Closedset spots colored green
                elif(Grid.g[row][col] in closedSet):
                    pygame.draw.rect(screen, red, [cw*col, ch*row, cw-1, ch-1])
                else:
                    if(Grid.g[row][col].wall):
                        pygame.draw.rect(screen, black, [cw*col, ch*row, cw-1, ch-1])
                    else:
                        pygame.draw.rect(screen, white, [cw*col, ch* row, cw-1, ch-1])
    else:
        for row in range(Grid.nRows):
            for col in range(Grid.nCols):
                if Grid.g[row][col] in Grid.path:
                    pygame.draw.rect(screen, blue, [cw*col, ch*row, cw-1, ch-1])

    pygame.display.flip()


pygame.image.save(screen,'AStarPath.png')
pygame.quit()

#---------------------
print("Stop.")
#---------------------

import math
import sys
import heapq
from timeit import default_timer as timer
from utils.maze import *
from utils.cell import cell
from utils.configuration import *

# A*
G_cost = {}
F_cost = {}
came_from = {}
closedset = set()
openset = set()
# Djikstra
d_path = {}
d_previous = {}
queue = []
# Bellman-Ford
bf_path = {}
bf_previous = {}

class Algorithms:
    def __init__(self):
        # A*
        self.astar_stop = False
        self.astar_counter = 0
        self.astar_time = 0.0
        # Dijkstra
        self.djikstra_stop = False
        self.djikstra_counter = 0
        self.dijkstra_time = 0.0
        # Bellman-Ford
        self.bf_stop = False
        self.bf_counter = 0
        self.bf_change = False
        self.bf_time = 0.0

    def reset(self, maze):
        # A* reset
        self.astar_stop = False
        self.astar_counter = 0
        self.astar_time = 0.0
        G_cost = {}
        F_cost = {}
        came_from = {}
        closedset.clear()
        openset.clear()
        # Djikstra reset
        self.djikstra_stop = False
        self.djikstra_counter = 0
        self.dijkstra_time = 0.0
        d_path.clear()
        d_previous = {}
        queue.clear()
        # Bellman-Ford reset
        self.bf_stop = False
        self.bf_counter = 0
        bf_path = {}
        bf_previous = {}
        self.bf_change = False
        self.bf_time = 0.0
        # recolor maze
        for y in range(rows):
             for x in range(cols):
                  maze.mainGrid[y][x].color = WHITE

    # BELLMAN-FORD ALGORITHM
    def bellman_ford(self, startPoint, endPoint, maze):
        timer_start = timer()
        maze.mainGrid[int(endPoint.y/cellWidth)][int(endPoint.x/cellWidth)].color = END_CELL_COLOR
        maze.mainGrid[int(startPoint.y/cellWidth)][int(startPoint.x/cellWidth)].color = START_CELL_COLOR
        if(self.bf_counter == 0): #first iteration, chceck all cells in maze
            for y in range(rows):
                for x in range(cols):
                    bf_path[maze.mainGrid[y][x]] = float('Inf')
            bf_path[startPoint] = 0
            current = startPoint
            bf_previous[startPoint] = None
            self.bf_stop = False
            self.bf_time = 0.0
            
        self.bf_counter = 0
        self.bf_change = False
        for y in range(rows):
            for x in range(cols):
                self.bf_counter = self.bf_counter + 1
                current = maze.mainGrid[y][x]
                maze.mainGrid[int(current.y/cellWidth)][int(current.x/cellWidth)].color = CURRENT_CELL_COLOR
                for neighbour in Algorithms.getNeighbours(current):
                    if bf_path[neighbour] > bf_path[current] + 1: # relax
                        bf_path[neighbour]  = bf_path[current] + 1
                        bf_previous[neighbour] = current
                        maze.mainGrid[int(neighbour.y/cellWidth)][int(neighbour.x/cellWidth)].color = CURRENT_CELL_COLOR
                        self.bf_change = True

                    if(current == endPoint and self.bf_change == False and self.bf_counter == cols*rows):
                        print("BELLMAN-FORD | END")
                        print("BELLMAN-FORD | time: " + str(self.bf_time))
                        while(current):
                            maze.mainGrid[int(current.y/cellWidth)][int(current.x/cellWidth)].color = PATH_COLOR
                            current = bf_previous[current]
                        self.bf_stop = True
                    if(current == None):
                        current = startPoint
                    maze.mainGrid[int(current.y/cellWidth)][int(current.x/cellWidth)].color = VISITED_CELL_COLOR
        maze.mainGrid[int(endPoint.y/cellWidth)][int(endPoint.x/cellWidth)].color = END_CELL_COLOR
        maze.mainGrid[int(startPoint.y/cellWidth)][int(startPoint.x/cellWidth)].color = START_CELL_COLOR
        timer_stop = timer()
        self.bf_time = self.bf_time + (timer_stop - timer_start)


        

    # DIJKSTRA ALGORITHM
    def djikstra(self, startPoint, endPoint, maze):
        timer_start = timer()
        maze.mainGrid[int(endPoint.y/cellWidth)][int(endPoint.x/cellWidth)].color = END_CELL_COLOR
        maze.mainGrid[int(startPoint.y/cellWidth)][int(startPoint.x/cellWidth)].color = START_CELL_COLOR
        if(self.djikstra_counter == 0):
           d_path[startPoint] = 0
           current = None
           d_previous[startPoint] = None
           heapq.heappush(queue,(d_path[startPoint], startPoint))
           self.djikstra_stop = False

        if(Algorithms.count(queue)>0):
            self.djikstra_counter = self.djikstra_counter + 1
            tmp_distance,current = heapq.heappop(queue)
            maze.mainGrid[int(current.y/cellWidth)][int(current.x/cellWidth)].color = VISITED_CELL_COLOR
            for neighbor in Algorithms.getNeighbours(current):
                tmp_wage = tmp_distance + 1
                if(neighbor not in d_path or tmp_wage < d_path[neighbor]):
                    maze.mainGrid[int(neighbor.y/cellWidth)][int(neighbor.x/cellWidth)].color = CURRENT_CELL_COLOR
                    d_path[neighbor] = tmp_wage
                    d_previous[neighbor] = current
                    heapq.heappush(queue,(d_path[neighbor], neighbor))

        if(current == endPoint):
            while(current):
                maze.mainGrid[int(current.y/cellWidth)][int(current.x/cellWidth)].color = PATH_COLOR
                current = d_previous[current]
            maze.mainGrid[int(endPoint.y/cellWidth)][int(endPoint.x/cellWidth)].color = END_CELL_COLOR
            maze.mainGrid[int(startPoint.y/cellWidth)][int(startPoint.x/cellWidth)].color = START_CELL_COLOR
            print("DIJKSTRA | END")
            print("DIJKSTRA | time: " + str(self.dijkstra_time))
            self.djikstra_stop = True
        timer_stop = timer()
        self.dijkstra_time = self.dijkstra_time + (timer_stop - timer_start)
                

        
    # A* ALGORITHM
    def astar(self, startPoint, endPoint, maze):
        timer_start = timer()
        maze.mainGrid[int(endPoint.y/cellWidth)][int(endPoint.x/cellWidth)].color = END_CELL_COLOR
        maze.mainGrid[int(startPoint.y/cellWidth)][int(startPoint.x/cellWidth)].color = START_CELL_COLOR
        if(self.astar_counter==0):
            G_cost[startPoint] = 0
            F_cost[startPoint] = G_cost[startPoint] + Algorithms.heuresticCost(startPoint, endPoint)
            openset.add(startPoint)
            self.astar_stop = False

        if(Algorithms.count(openset)>0):
            self.astar_counter = self.astar_counter + 1
            for cell in openset:
                if(cell != startPoint):
                    maze.mainGrid[int(cell.y/cellWidth)][int(cell.x/cellWidth)].color = CURRENT_CELL_COLOR
            F_cost_sorted = sorted(F_cost, key=lambda cell: G_cost[cell] + Algorithms.heuresticCost(cell, endPoint))
            i = 0
            for i in range(len(F_cost_sorted)-1):
                i = i+1
                if(F_cost_sorted[i] not in closedset):
                    break

            current = F_cost_sorted[i]
            if(current == endPoint):
                print("A* | END")
                print("A* | time: " + str(self.astar_time))
                self.astar_stop = True
                for cell in Algorithms.reconstruct_path(endPoint):
                    maze.mainGrid[int(cell.y/cellWidth)][int(cell.x/cellWidth)].color = PATH_COLOR
                maze.mainGrid[int(endPoint.y/cellWidth)][int(endPoint.x/cellWidth)].color = END_CELL_COLOR
                maze.mainGrid[int(startPoint.y/cellWidth)][int(startPoint.x/cellWidth)].color = START_CELL_COLOR
                return

            try:
                openset.remove(current)
            except KeyError:
                pass

            closedset.add(current)

            for neighbour in Algorithms.getNeighbours(current):
                maze.mainGrid[int(neighbour.y/cellWidth)][int(neighbour.x/cellWidth)].color = VISITED_CELL_COLOR
                if neighbour not in closedset:
                    G_cost_tmp = G_cost[current] + 1
                    if (neighbour not in openset) or (G_cost_tmp < G_cost[neighbour]): 
                        came_from[neighbour] = current
                        G_cost[neighbour] = G_cost_tmp
                        F_cost[neighbour] = G_cost[neighbour] + Algorithms.heuresticCost(neighbour,endPoint)
                        if neighbour not in openset:
                            openset.add(neighbour)
        timer_stop = timer()
        self.astar_time = self.astar_time + (timer_stop - timer_start)

    @staticmethod
    def count(collection):
        counter = 0
        for i in collection:
            counter = counter + 1
        return counter

    @staticmethod
    def getNeighbours(cell):
        neighbours = set()

        if(int(cell.y / cellWidth) - 1 >= 0):
            cell.topNeighbor = cell.grid[int(cell.y / cellWidth) - 1][int(cell.x / cellWidth)]
        
        if(int(cell.x / cellWidth) + 1 <= cols - 1):
            cell.rightNeighbor = cell.grid[int(cell.y / cellWidth)][int(cell.x / cellWidth) + 1]
        
        if(int(cell.y / cellWidth) + 1 <= rows - 1):
            cell.bottomNeighbor = cell.grid[int(cell.y / cellWidth) + 1][int(cell.x / cellWidth)]
        
        if(int(cell.x / cellWidth) - 1 >= 0):
            cell.leftNeighbor = cell.grid[int(cell.y / cellWidth)][int(cell.x / cellWidth) - 1]

        if cell.cellWalls[0] == False:
            neighbours.add(cell.topNeighbor)
        if cell.cellWalls[1] == False:
            neighbours.add(cell.rightNeighbor)
        if cell.cellWalls[2] == False:
            neighbours.add(cell.bottomNeighbor)
        if cell.cellWalls[3] == False:
            neighbours.add(cell.leftNeighbor)
        
        return neighbours

    @staticmethod
    def heuresticCost(start, end):
        x = (int(start.x/cellWidth) - int(end.x/cellWidth))
        y = (int(start.y/cellWidth) - int(end.y/cellWidth))
        return 1 * max(abs(x),abs(y))

    @staticmethod
    def reconstruct_path(from_cell):
        try: 
            came_from[from_cell]
            p = Algorithms.reconstruct_path(came_from[from_cell])
            return_path = []
            return_path.extend(p)
            return_path.append(from_cell)
            return return_path
        except KeyError:
            return [from_cell]


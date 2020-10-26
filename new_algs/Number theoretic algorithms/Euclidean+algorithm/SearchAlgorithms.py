from queue import  *
from math import  *

class Node:
    id = None  # Unique value for each node.
    up = None  # Represents value of neighbors (up, down, left, right).
    down = None
    left = None
    right = None
    previousNode = None  # Represents value of neighbors.
    edgeCost = None  # Represents the cost on the edge from any parent to this node.
    gOfN = None  # Represents the total edge cost
    hOfN = None  # Represents the heuristic value
    heuristicFn = None  # Represents the value of heuristic function
    visted = False  # to indicate the visted Nodes Befor this Node

    def __init__(self, value):
        self.value = value


class SearchAlgorithms:
    ''' * DON'T change Class, Function or Parameters Names and Order
        * You can add ANY extra functions,
          classes you need as long as the main
          structure is left as is '''

    path = []  # Represents the correct path from start node to the goal node.
    fullPath = []  # Represents all visited nodes from the start node to the goal node.
    totalCost = -1  # Represents the total cost in case using UCS, AStar (Euclidean or Manhattan)
    grid = []  # this is list of lists to hold the Grid with All iforamtion
    list_of_rows = []  # this List To Hold the information about Rows of String
    id_counter = 0  # this to count the total number of ID assign to each Node with in the #
    start_id = 0  # to indicate the ID of the start Node
    row_number = 0  # indicate the number of Rows In the Grid
    col_number = 0  # indicate the number of Colums in the Grid
    cost_counter = 0  # to count the the cost to each Node in the List of Lists
    end_x = 0  # this to indicate the x coordinate for the End Point
    end_y = 0  # this to indicate the y coordinate for the End Point
    stack = []  # this is the stack for DFS
    myqueue = Queue()  # this is the queu for the BFS
    pqueue = PriorityQueue()  # this is the periority queue for the UCS and A start

    def __init__(self, mazeStr, edgeCost = None):
        # intialization By NULL
        self.grid.clear()
        self.list_of_rows.clear()
        self.fullPath.clear()
        self.stack.clear()

        # to get the number of Rows in the grid

        for i in mazeStr:
            if i == ',':
                continue
            if i == " ":
                self.row_number += 1
        self.row_number += 1
        # print("The number of Rows is : " + str(self.row_number))

        # to get the number of Colums in the grid

        for i in mazeStr:
            if i == ',':
                self.col_number += 1
            if i == " ":
                self.col_number += 1
                break
        # print("The number of Colums is : " + str(self.col_number))

        # to create the Grid of the maze

        self.list_of_rows = mazeStr.split()
        for i in self.list_of_rows:
            self.grid.append(i.split(","))

        # to Assign ID and create Nodes in the list of lists

        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == "S":
                    self.start_id = self.id_counter
                elif self.grid[i][j] == "E":
                    self.end_x = i
                    self.end_y = j
                var_node = Node(self.grid[i][j])
                var_node.id = self.id_counter
                self.id_counter += 1
                self.grid[i][j] = var_node
                # to make Sure All Nodes Are Okay Now In the List

                # print("The Node Value is : " + str(self.grid[i][j].value) + " and the ID is : " +
                # str(self.grid[i][j].id))
        # to assign the up , left , right and dwn to each Node with out the # as It Will be None

        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if i != 0:
                    if self.grid[i-1][j].value != '#':
                        self.grid[i][j].up = self.grid[i-1][j].id
                if i != len(self.grid)-1:
                    if self.grid[i+1][j].value != '#':
                        self.grid[i][j].down = self.grid[i+1][j].id
                if j != 0:
                    if self.grid[i][j-1].value != '#':
                        self.grid[i][j].left = self.grid[i][j-1].id
                if j != len(self.grid[0])-1:
                    if self.grid[i][j+1].value != '#':
                        self.grid[i][j].right = self.grid[i][j+1].id
                # to make Sure ALL Values Are Correct

                # print("The Node Value is : " + str(self.grid[i][j].value))
                # print("The Node ID is : " + str(self.grid[i][j].id))
                # print("The Node Up is : " + str(self.grid[i][j].up) + " Down is " + str(str(self.grid[i][j].down)))
                # print("The Node left is : " + str(self.grid[i][j].left)+" right is "+str(str(self.grid[i][j].right)))
        # this to assign the Cost To Each Node in the List Of Lists (To th Nodes)
        if str(edgeCost) != "None":
            for i in range(len(self.grid)):
                for j in range(len(self.grid[0])):
                    self.grid[i][j].edgeCost = edgeCost[self.cost_counter]
                    self.cost_counter += 1
                    # this to make sure that all Costs Are Right
                    # print("The Node is "+str(self.grid[i][j].value)+"and the cost is:"+str(self.grid[i][j].edgeCost))

    def get_flatten(self, id):
        r = int(id // self.col_number)
        c = int(id % self.col_number)
        return r, c

    def huristic_eculidan_distance(self, i, j):
        d = sqrt(pow((self.end_x - i), 2) + pow((self.end_y - j), 2))
        return d

    def huristic_aboslute(self, i, j):
        d = abs(i - self.end_x) + abs(j - self.end_y)
        return d

    def get_children(self, row_idx, col_idx):
        list_of_children = []
        up = self.grid[row_idx][col_idx].up
        down = self.grid[row_idx][col_idx].down
        left = self.grid[row_idx][col_idx].left
        right = self.grid[row_idx][col_idx].right
        self.grid[row_idx][col_idx].visted = True
        if str(right) != "None":
            list_of_children.append(self.grid[row_idx][col_idx].right)
        if str(left) != "None":
            list_of_children.append(self.grid[row_idx][col_idx].left)
        if str(down) != "None":
            list_of_children .append(self.grid[row_idx][col_idx].down)
        if str(up) != "None":
            list_of_children .append(self.grid[row_idx][col_idx].up)
        return list_of_children[:]

    def assign_costs(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j].value == 'S':
                    self.grid[i][j].edgeCost = 0
                else:
                    self.grid[i][j].edgeCost = 1

    def DFS(self):
        self.stack = []
        self.stack.append(self.start_id)
        while len(self.stack) != 0:
            # stack.reverse()
            ID = self.stack.pop()
            row_idx, col_idx = self.get_flatten(ID)
            if self.grid[row_idx][col_idx].value == "E":
                self.fullPath.append(ID)
                break
            elif not self.grid[row_idx][col_idx].visted and ID not in self.stack:
                self.fullPath.append(ID)
                self.grid[row_idx][col_idx].visted = True
                list_of_children = self.get_children(row_idx, col_idx)
                for i in list_of_children:
                    self.stack.append(i)

        return self.path, self.fullPath

    def BFS(self):
        self.myqueue = Queue()
        self.myqueue.put(self.start_id)
        while not self.myqueue.empty():
            ID = self.myqueue.get()
            row_idx, col_idx = self.get_flatten(ID)
            if self.grid[row_idx][col_idx].value == "E":
                self.fullPath.append(ID)
                break
            elif not self.grid[row_idx][col_idx].visted:
                self.fullPath.append(ID)
                self.grid[row_idx][col_idx].visted = True
                list_of_childrens = self.get_children(row_idx, col_idx)
                list_of_childrens.reverse()
                for i in list_of_childrens:
                    self.myqueue.put(i)
        return self.path, self.fullPath

    def UCS(self):
        self.pqueue = PriorityQueue()
        self.pqueue.put((0, self.start_id))
        while not self.pqueue.empty():
            cost, ID = self.pqueue.get()
            row_idx, col_idx = self.get_flatten(ID)
            if not self.grid[row_idx][col_idx].visted:
                self.fullPath.append(ID)
                if self.grid[row_idx][col_idx].value == 'E':
                    break
                l_of_neighbours = self.get_children(row_idx, col_idx)
                l_of_neighbours.reverse()
                self.grid[row_idx][col_idx].visted = True
                for i in l_of_neighbours:
                    if i not in self.fullPath:
                        r_idx, c_idx = self.get_flatten(i)
                        self.totalCost = cost + self.grid[r_idx][c_idx].edgeCost
                        self.grid[r_idx][c_idx].gOfN = cost + self.grid[r_idx][c_idx].edgeCost
                        self.pqueue.put((self.totalCost, i))

        return self.path, self.fullPath, self.totalCost

    def AStarEuclideanHeuristic(self):
        # calculate the huristic to each Node in the list

        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                self.grid[i][j].hOfN = self.huristic_eculidan_distance(i, j)

        self.pqueue = PriorityQueue()
        self.pqueue.put((0, self.start_id))
        row_idx, col_idx = self.get_flatten(self.start_id)
        self.grid[row_idx][col_idx].gOfN = 0

        while not self.pqueue.empty():
            _, ID = self.pqueue.get()
            row_idx, col_idx = self.get_flatten(ID)
            cost = self.grid[row_idx][col_idx].gOfN
            if not self.grid[row_idx][col_idx].visted:
                self.fullPath.append(ID)
                if self.grid[row_idx][col_idx].value == 'E':
                    break
                l_of_neighbours = self.get_children(row_idx, col_idx)
                l_of_neighbours.reverse()
                self.grid[row_idx][col_idx].visted = True
                for i in l_of_neighbours:
                    if i not in self.fullPath:
                        r_idx, c_idx = self.get_flatten(i)
                        self.grid[r_idx][c_idx].gOfN = cost + self.grid[r_idx][c_idx].edgeCost
                        self.totalCost = self.grid[r_idx][c_idx].gOfN
                        self.grid[r_idx][c_idx].heuristicFn = self.grid[r_idx][c_idx].gOfN + self.grid[r_idx][c_idx].hOfN
                        self.pqueue.put((self.grid[r_idx][c_idx].heuristicFn, i))

        return self.path, self.fullPath, self.totalCost

    def AStarManhattanHeuristic(self):
        # calculate the huristic to each Node in the list

        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                self.grid[i][j].hOfN = self.huristic_aboslute(i, j)
        self.assign_costs()
        self.pqueue = PriorityQueue()
        self.pqueue.put((0, self.start_id))
        row_idx, col_idx = self.get_flatten(self.start_id)
        self.grid[row_idx][col_idx].gOfN = 0

        while not self.pqueue.empty():
            _, ID = self.pqueue.get()
            row_idx, col_idx = self.get_flatten(ID)
            cost = self.grid[row_idx][col_idx].gOfN
            if not self.grid[row_idx][col_idx].visted:
                self.fullPath.append(ID)
                if self.grid[row_idx][col_idx].value == 'E':
                    break
                l_of_neighbours = self.get_children(row_idx, col_idx)
                l_of_neighbours.reverse()
                self.grid[row_idx][col_idx].visted = True
                for i in l_of_neighbours:
                    if i not in self.fullPath:
                        r_idx, c_idx = self.get_flatten(i)
                        self.grid[r_idx][c_idx].gOfN = cost + self.grid[r_idx][c_idx].edgeCost
                        self.totalCost = self.grid[r_idx][c_idx].gOfN
                        self.grid[r_idx][c_idx].heuristicFn = self.grid[r_idx][c_idx].gOfN + self.grid[r_idx][c_idx].hOfN
                        self.pqueue.put((self.grid[r_idx][c_idx].heuristicFn, i))
        return self.path, self.fullPath, self.totalCost


def main():
    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath = searchAlgo.DFS()
    print('**DFS**\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\n\n')

                #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath = searchAlgo.BFS()
    print('**BFS**\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\n\n')
                #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.', [0, 15, 2, 100, 60, 35, 30, 3
                                                                                                             , 100, 2, 15, 60, 100, 30, 2
                                                                                                             , 100, 2, 2, 2, 40, 30, 2, 2
                                                                                                             , 100, 100, 3, 15, 30, 100, 2
                                                                                                             , 100, 0, 2, 100, 30])
    path, fullPath, TotalCost = searchAlgo.UCS()
    print('** UCS **\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\nTotal Cost: ' + str(
        TotalCost) + '\n\n')
               #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.', [0, 15, 2, 100, 60, 35, 30, 3
                                                                                                             , 100, 2, 15, 60, 100, 30, 2
                                                                                                             , 100, 2, 2, 2, 40, 30, 2, 2
                                                                                                             , 100, 100, 3, 15, 30, 100, 2
                                                                                                             , 100, 0, 2, 100, 30])
    path, fullPath, TotalCost = searchAlgo.AStarEuclideanHeuristic()
    print('**ASTAR with Euclidean Heuristic **\nPath is: ' + str(path) + '\nFull Path is: ' + str(
        fullPath) + '\nTotal Cost: ' + str(TotalCost) + '\n\n')

            #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath, TotalCost = searchAlgo.AStarManhattanHeuristic()
    print('**ASTAR with Manhattan Heuristic **\nPath is: ' + str(path) + '\nFull Path is: ' + str(
        fullPath) + '\nTotal Cost: ' + str(TotalCost) + '\n\n')


main()

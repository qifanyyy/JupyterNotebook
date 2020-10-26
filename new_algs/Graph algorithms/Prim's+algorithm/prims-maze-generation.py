import random
import pandas as pd
import numpy as np
# References
# http://jonathanzong.com/blog/2012/11/06/maze-generation-with-prims-algorithm

SIZE = 10
CLOSED = '*'
OPEN = ' '
START = 'S'
startNode =[-1,-1]
node = {'x': 0, 'y': 0, 'value':'-', 'parent': [None,None]}


def initMaze(size):
    [(x, y) for x in range(11) for y in range(11)]
    for x in range(SIZE*SIZE):
        print x,':', maze0[x]
    return maze0

    maze = pd.DataFrame(np.random.randint(low=0, high=SIZE, size=(5, 5)),
...                    columns=['a', 'b', 'c', 'd', 'e'])



def prims(maze):
    startNode = [random.randomint(0,SIZE-1),random.randomint(0,SIZE-1), None]
    maze[startNode[0],startNode[0]] = START

    neighbors = []
    for x in range(-1,1):
        for y in range(-1,1):
            if x == 0 and y == 0 or x != 0 and y != 0:
                continue
            # in bounds
            if(startNode[0] + x < SIZE or startNode[1] + y < SIZE):
                if maze[startNode[0] + x][startNode[1] + y] == '.':
                    continue
            neighbors.append([startNode[0], startNode[1]]),

    lastNode = None

    while(neighbors):
        randomNode = neighbors.remove(random.randomint(0,len(neighbors)))



def opposite(node1, node2):
    if (compareTo(node1, node2) != 0):
        return [node1[0] + compareTo(node1, node2), node1[0]]
    if (compareTo(node1, node2)):
        print('hi')



def compareTo(node1, node2):
    if node1[1] < node2[1]:
        return -1

    if node1[1] > node2[1]:
        return 1

    if node1[0] < node2[0]:
        return -1

    if node1[0] > node2[0]:
        return 1
    return 0

maze = initMaze(SIZE)




import pygame
import math
import random


class Node(object):
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.fScore = 10000
        self.gScore = 10000
        self.explored = False
        self.color = (255, 255, 255)
        self.rect = pygame.Rect(self.x * 30, self.y * 30, 30, 30)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def draw(self):
        if not self.explored:
            pygame.draw.rect(window, self.color, (self.x * 30, self.y * 30, 30, 30))
        else:
            pygame.draw.rect(window, self.color, (self.x * 30, self.y * 30, 30, 30))


class PathFind(object):
    def __init__(self, map, start, end):
        self.map = map
        self.start = start
        self.end = end

        self.start.color = (0, 0, 255)
        self.end.color = (0, 255, 0)

    def draw(self):
        for row in self.map:
            for tile in row:
                if tile != self.start and tile != self.end and tile.type == "ground":
                    tile.draw()
                if tile.type == "wall":
                    tile.draw()

        self.start.draw()
        self.end.draw()
        self.lines()
        pygame.display.update()

    def lines(self):
        for i in range(30):
            pygame.draw.line(window, (0, 0, 0), (i * 30, 0), (i * 30, 600))
            pygame.draw.line(window, (0, 0, 0), (0, i * 30), (900, i * 30))

    def distance(self, node1, node2):
        return math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)

    def heuristic(self, node):
        return abs(node.x - self.end.x) + abs(node.y - self.end.y)

    def getNeighbor(self, node):
        neighbors = []
        try:
            if 0 <= node.x < len(self.map[0]) - 1: neighbors.append(self.map[node.y][node.x + 1])
            if 0 < node.x <= len(self.map[0]) - 1: neighbors.append(self.map[node.y][node.x - 1])
            if 0 <= node.y < len(self.map) - 1: neighbors.append(self.map[node.y + 1][node.x])
            if 0 < node.y <= len(self.map) - 1: neighbors.append(self.map[node.y - 1][node.x])
        except IndexError:
            print("Error: {}".format(node))
        return neighbors

    def constructPath(self, current, tracker):
        path = []
        while current in tracker:
            current = tracker[current]
            path.append(current)
        return path

    def pathFind(self):
        explored = []
        previous = {}
        unexplored = [self.start]
        self.start.gScore = 0
        self.start.fScore = self.heuristic(self.start)

        while unexplored:
            unexplored.sort(key=lambda x: x.fScore)
            currentNode = unexplored[0]

            if currentNode == self.end:
                pathdraw(self.constructPath(currentNode, previous))
                self.lines()

            unexplored.remove(currentNode)
            explored.append(currentNode)
            for neighbor in self.getNeighbor(currentNode):
                if neighbor.type == "ground":
                    tempG = currentNode.gScore + self.distance(currentNode, neighbor)
                    if tempG < neighbor.gScore:
                        neighbor.gScore = tempG
                        previous[neighbor] = currentNode
                        neighbor.fScore = neighbor.gScore + self.heuristic(neighbor)
                        if neighbor not in explored:
                            unexplored.append(neighbor)


def pathdraw(path):
    for i in path[0:-1]:
        pygame.draw.rect(window, (155, 155, 155), (i.x * 30, i.y * 30, 30, 30))


pygame.init()
COLOR = (255, 255, 255)
window = pygame.display.set_mode((900, 600))
window.fill(COLOR)
tiles = []
map = []
for i in range(20):
    for p in range(30):
        x = random.randint(0, 10)
        if x < 3:
            node = Node(p, i, "wall")
            node.color = (0, 0, 0)
        else:
            node = Node(p, i, "ground")
        tiles.append(node)
    map.append(tiles)
    tiles = []


algo = PathFind(map, map[0][0], map[19][29])
algo.lines()
algo.draw()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    algo.pathFind()
    pygame.display.update()








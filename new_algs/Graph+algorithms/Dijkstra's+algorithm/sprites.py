# sprites for Dijkstra visualization
import pygame as pg
from settings import *
import heapq


class Graph:
    # main graph class
    def __init__(self, main):
        self.main = main
        self.start, self.end = None, None
        self.walls = []
        self.connections = [[-1, 0], [0, -1], [1, 0], [0, 1]]

        self.distances = [[float('inf')] * 48 for i in range(32)]
        self.prev = {}

    def in_bounds(self, node):
        # check if node is within the grid
        return 0 <= node[0] < 32 and 0 <= node[1] < 48

    def passable(self, node):
        # check for walls
        return node not in self.walls

    def find_neighbors(self, node):
        # filter only viable neighbors
        neighbors = [[node[0] + connection[0], node[1] + connection[1]] for connection in self.connections]
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.passable, neighbors)
        return neighbors

    def dijkstra(self, start, end):
        # main dijkstra function
        # runs one iteration at a time and remembers where to resume
        if not self.pq:
            return False
        cur_dis, cur_node = heapq.heappop(self.pq)
        if cur_dis > self.distances[cur_node[0]][cur_node[1]]:
            return None
        for neighbor in self.find_neighbors(cur_node):
            dist = cur_dis + 1
            if dist < self.distances[neighbor[0]][neighbor[1]]:
                self.prev[(neighbor[0], neighbor[1])] = tuple(cur_node)
                self.distances[neighbor[0]][neighbor[1]] = dist
                heapq.heappush(self.pq, [dist, neighbor])
                Visited(self.main, neighbor[0], neighbor[1])
            if neighbor == end:
                return False
        self.start = self.pq[0]


class Visited(pg.sprite.Sprite):
    # sprite for visited tiles
    def __init__(self, main, x, y):
        self._layer = VISITED_LAYER
        self.groups = main.all_sprites, main.visited
        pg.sprite.Sprite.__init__(self, self.groups)
        self.xsize, self.ysize = TILE_SIZE // 8, TILE_SIZE // 8
        self.x, self.y = x, y
        self.image = pg.Surface((self.xsize, self.ysize))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (y * TILE_SIZE + TILE_SIZE // 2, x * TILE_SIZE + TILE_SIZE // 2)
        self.made = pg.time.get_ticks()

    def update(self):
        # increase sprite in size after some time has passed
        if self.xsize < TILE_SIZE and pg.time.get_ticks() - self.made > 300:
            self.made = pg.time.get_ticks()
            self.xsize *= 2
            self.ysize *= 2
            self.image = pg.Surface((self.xsize, self.ysize))
            self.image.fill(YELLOW)
            self.rect = self.image.get_rect()
            self.rect.center = (self.y * TILE_SIZE + TILE_SIZE // 2, self.x * TILE_SIZE + TILE_SIZE // 2)


class Start(pg.sprite.Sprite):
    # sprite for start point
    def __init__(self, main, x, y):
        self._layer = START_END_LAYER
        self.groups = main.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x // TILE_SIZE * TILE_SIZE, y // TILE_SIZE * TILE_SIZE)
        main.graph.start = [self.rect.topleft[1] // 16, self.rect.topleft[0] // 16]
        main.graph.pq = [[0, main.graph.start]]
        main.graph.distances[main.graph.start[0]][main.graph.start[1]] = 0


class Wall(pg.sprite.Sprite):
    # sprite for walls
    def __init__(self, main, x, y):
        self.groups = main.all_sprites, main.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.locx, self.locy = x, y
        self.x, self.y = (x // TILE_SIZE), (y // TILE_SIZE)
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)
        main.graph.walls.append([self.rect.topleft[1] // 16, self.rect.topleft[0] // 16])


class End(pg.sprite.Sprite):
    # sprite for end point
    def __init__(self, main, x, y):
        self._layer = START_END_LAYER
        self.groups = main.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x // TILE_SIZE * TILE_SIZE
        self.y = y // TILE_SIZE * TILE_SIZE
        self.rect.topleft = (self.x, self.y)
        main.graph.end = [self.rect.topleft[1] // 16, self.rect.topleft[0] // 16]


class Shortest(pg.sprite.Sprite):
    # sprite for shortest distance
    def __init__(self, main, x, y):
        self._layer = SHORTEST_LAYER
        self.groups = main.all_sprites, main.path
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)

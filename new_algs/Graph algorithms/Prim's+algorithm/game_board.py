# imports
import pygame
import sys
import random
from general.consts_values import NUMBER_OF_OF_BLOCKS, Color
from general.matrix_of_blocks import Matrix
from graphs.graph import MyOwnGraph
from blocks.player_block import Player
from blocks.enemy_block import Enemy


# game class - update and render
class Game(object):

    # constructor - creates objects and stores variables
    # also initializes game frame
    def __init__(self, player_one_icon, player_two_icon):
        # vars and consts
        self.__tps_max = 30.0
        self.__game_finished = False
        self.__tps_clock = pygame.time.Clock()
        self.__tps_delta = 0.0
        # initialization
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.matrix = Matrix(NUMBER_OF_OF_BLOCKS[0], NUMBER_OF_OF_BLOCKS[1])
        self.player_one = None
        self.player_two = None
        self.moveable_objects = list()
        self.graphh = MyOwnGraph(self.matrix, NUMBER_OF_OF_BLOCKS[0], NUMBER_OF_OF_BLOCKS[1])
        self.initialize_level()
        self.player_one = self.initialize_player(player_one_icon)
        self.player_two = self.initialize_player(player_two_icon)
        self.initialize_enemy()

    # makes background blocks
    def initialize_level(self):
        self.fill_background_with_wall_blocks()
        self.create_maze()
        self.create_background_frame()

    # fills background with walls
    def fill_background_with_wall_blocks(self):
        for i in range(0, NUMBER_OF_OF_BLOCKS[0]):
            for j in range(0, NUMBER_OF_OF_BLOCKS[1]):
                self.matrix.set_block_to_wall(i, j)

    # uses generated edges (Prim's algorithm) to create "random maze"
    def create_maze(self):
        generated_edges = self.graphh.generate_prims_maze()
        for edge in generated_edges:
            x1 = edge.node_a.x
            y1 = edge.node_a.y
            self.matrix.set_block_to_background(x1, y1)
            x2 = edge.node_b.x
            y2 = edge.node_b.y
            self.matrix.set_block_to_background(x2, y2)

    # creates frame (top, left, right, bottom border of window) of Backgorund blocks
    def create_background_frame(self):
        for i in range(0, NUMBER_OF_OF_BLOCKS[0]):
            self.matrix.set_block_to_background(i, 0)
            self.matrix.set_block_to_background(i, NUMBER_OF_OF_BLOCKS[1] - 1)
        for i in range(0, NUMBER_OF_OF_BLOCKS[1]):
            self.matrix.set_block_to_background(0, i)
            self.matrix.set_block_to_background(NUMBER_OF_OF_BLOCKS[0] - 1, i)

    # places player in free spot
    def initialize_player(self, players_icon) -> Player:
        x = random.randrange(0, NUMBER_OF_OF_BLOCKS[0])
        y = random.randrange(0, NUMBER_OF_OF_BLOCKS[1])
        if self.matrix.two_dim_list[x][y]:
            player = Player(x, y, players_icon)
            self.moveable_objects.append(player)
            return player
        else:
            return self.initialize_player(players_icon)

    # places enemy in free spot
    def initialize_enemy(self):
        x = random.randrange(0, NUMBER_OF_OF_BLOCKS[0])
        y = random.randrange(0, NUMBER_OF_OF_BLOCKS[1])
        if self.matrix.two_dim_list[x][y]:
            enemy = Enemy(x, y, self.graphh)
            self.moveable_objects.append(enemy)
        else:
            return self.initialize_enemy()

    # game loop is checking events (from keyboard, window) by calling objects' update() also calls render() and update()
    def game_loop(self, actual_game):
        while not self.__game_finished:
            # events handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    sys.exit()                                                  # press ESC to exit game
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    actual_game = Game(self.player_one.color, self.player_two.color)
                    actual_game.game_loop(actual_game)     # press R to restart game

            # updates handling
            self.__tps_delta += self.__tps_clock.tick() / 1000.0
            while self.__tps_delta > 1 / self.__tps_max:
                self.update()
                self.__tps_delta -= 1 / self.__tps_max
                self.player_one.update_position_v1(self.matrix, self.moveable_objects)
                self.player_two.update_position_v2(self.matrix, self.moveable_objects)
            # calls render
            self.render()

    # updates positions of every object
    def update(self):
        for i in range(0, NUMBER_OF_OF_BLOCKS[0]):
            for j in range(0, NUMBER_OF_OF_BLOCKS[1]):
                self.matrix.two_dim_list[i][j].update(self.matrix, self.moveable_objects)
        for object_to_update in self.moveable_objects:
            object_to_update.update(self.matrix, self.moveable_objects)

    # drawing every object
    def render(self):
        self.screen.fill(Color.BLACK)
        for i in range(0, NUMBER_OF_OF_BLOCKS[0]):
            for j in range(0, NUMBER_OF_OF_BLOCKS[1]):
                self.matrix.two_dim_list[i][j].render(self.screen)
        for object_to_render in self.moveable_objects:
            object_to_render.render(self.screen)
        pygame.display.flip()

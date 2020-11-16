# imports
import pygame

# this file only holds const values and class used in this project
NUMBER_OF_OF_BLOCKS = (64, 36)


# class holding colours
class Color(object):
    RED = (255, 0, 0)
    ORANGE = (255, 128, 0)
    YELLOW = (255, 255, 0)
    MEGA_LIGHT_GREEN = (191, 255, 0)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 128)
    LIGHT_BLUE = (0, 255, 255)
    BLUE = (0, 0, 255)
    PURPLE = (128, 0, 255)
    PINK = (255, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    LUKASZ_IMG = pygame.image.load("pictures/lukasz lewo.png")
    PIZZA_IMG = pygame.image.load("pictures/pizza.png")
    UFO_IMG = pygame.image.load("pictures/ufo.png")
    PAWEL_PNG = pygame.image.load("pictures/pawel.png")
    PAWEL2_PNG = pygame.image.load("pictures/pawel2.png")
    OGOREK_PNG = pygame.image.load("pictures/ogorek.png")
    OGOR_PNG = pygame.image.load("pictures/ogor.png")
    playable_colors_list = [MEGA_LIGHT_GREEN, BLUE, PINK, LUKASZ_IMG, PIZZA_IMG, UFO_IMG, PAWEL2_PNG, PAWEL_PNG, OGOREK_PNG, OGOR_PNG]


# object holding blocks2 types
class Blocks(object):
    ABSTRACT = "None"
    BACKGROUND = "background"
    PLAYER = "player"
    WALL = "wall"
    ENEMY = "enemy"
    PATH = "path"
    BOMB = "bomb"
    EXPLOSION = "explosion"

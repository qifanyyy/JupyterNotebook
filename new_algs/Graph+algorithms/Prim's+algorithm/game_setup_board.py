import pygame
from general.consts_values import Color
from typing import Tuple, List
import sys


# this is first thing you see when game starts - player icon choice menu
class GameSetup(object):

    # constructor - creates variables and initialize menu
    def __init__(self):
        self.__tps_max = 30.0
        self.__tps_clock = pygame.time.Clock()
        self.__tps_delta = 0.0
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width: int = pygame.display.Info().current_w
        self.screen_height: int = pygame.display.Info().current_h
        self.color_rectangles: List[PngOrColorRectangle] = list()
        self.initialize_color_rectangles()
        self.finished_timer = -1
        self.finished = False
        self.player_one_icon = None
        self.player_two_icon = None
        self.p1_rectagnle = PngOrColorRectangle(int(self.screen_width / 5.56), int(self.screen_height / 2.87),
                                                self.screen_width / 30, self.screen_width / 30, Color.RED)
        self.p2_rectagnle = PngOrColorRectangle(int(self.screen_width / 1.1), int(self.screen_height / 2.87),
                                                self.screen_width / 30, self.screen_width / 30, Color.RED)
        self.mouse_pressed = False

    # "menu game" loop, returns user's choice
    def game_setup_loop(self):
        while self.finished_timer > 0 or not self.finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    sys.exit()  # press ESC to exit menu
            self.__tps_delta += self.__tps_clock.tick() / 1000.0
            while self.__tps_delta > 1 / self.__tps_max:
                self.update()
                self.__tps_delta -= 1 / self.__tps_max
                self.finished_timer -= 1
                print(self.finished_timer)
            self.render()
        return self.player_one_icon, self.player_two_icon

    # uses list of choices (from consts_values.py) to visualise these icon for user
    def initialize_color_rectangles(self):
        def_icon_width = int(self.screen_width / 30)
        x_row_counter = 0
        x = self.screen_width / 3
        y = self.screen_height * 5 / 10
        def_side = self.screen_width / 30
        for color in Color.playable_colors_list:
            buf_rect = PngOrColorRectangle(x - int(def_icon_width / 2), y, def_side, def_side, color)
            self.color_rectangles.append(buf_rect)
            x += int(self.screen_width / 12)
            x_row_counter += 1
            if x_row_counter >= 5:
                x = self.screen_width / 3
                y += self.screen_height / 10
                x_row_counter = 0

    # checks mouse position - player click on icon -> this is the choosen icon for Player Block
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for color_rect in self.color_rectangles:
            if not pygame.mouse.get_pressed()[0]:
                self.mouse_pressed = False
            if color_rect.check_collide_point(mouse_pos):
                if self.player_one_icon is None:
                    self.player_one_icon = color_rect.color_or_picture
                    self.mouse_pressed = True
                    self.p1_rectagnle.color_or_picture = self.p1_rectagnle.initialize_icon(color_rect.color_or_picture)
                    print(1)
                elif self.player_two_icon is None and not self.mouse_pressed:
                    self.p2_rectagnle.color_or_picture = self.p2_rectagnle.initialize_icon(color_rect.color_or_picture)
                    self.player_two_icon = color_rect.color_or_picture
                    self.finished_timer = 60
                    self.finished = True
                    print(2)

    # renders icons and background image
    def render(self):
        self.screen.fill(Color.BLACK)
        img = pygame.image.load("pictures/pathfinder menu 2 players.png")
        img = pygame.transform.scale(img, (self.screen_width, self.screen_height))
        self.screen.blit(img, (0, 0))
        for color_rect in self.color_rectangles:
            color_rect.draw_rect(self.screen)
        self.p1_rectagnle.draw_rect(self.screen)
        self.p2_rectagnle.draw_rect(self.screen)
        pygame.display.flip()


# class for icons that you can see in menu
class PngOrColorRectangle(object):
    # constructon - variables and initialization of icon
    def __init__(self, pos_x, pos_y, width, height, color_or_picture):
        self.rect = pygame.Rect(pos_x, pos_y, width, height)
        self.color_or_picture = color_or_picture
        self.screen_width: int = pygame.display.Info().current_w
        self.screen_height: int = pygame.display.Info().current_h
        self.x = pos_x
        self.y = pos_y
        self.color_or_picture = self.initialize_icon(color_or_picture)

    # checks if icon is tuple or pygame.Surface
    def initialize_icon(self, icon):
        if type(self.color_or_picture) == tuple:
            return icon
        elif type(self.color_or_picture) == pygame.Surface:
            return pygame.transform.scale(icon, (int(self.screen_width / 30), int(self.screen_width / 30)))

    # checks if mouse is over icon
    def check_collide_point(self, mousepos: Tuple[int, int]) -> bool:
        # noinspection PyArgumentList
        if self.rect.collidepoint(mousepos) and pygame.mouse.get_pressed()[0]:
            return True
        return False

    # render of icon
    def draw_rect(self, screen):
        if type(self.color_or_picture) == tuple:
            pygame.draw.rect(screen, self.color_or_picture, self.rect)
        elif type(self.color_or_picture) == pygame.Surface:
            screen.blit(self.color_or_picture, (self.x, self.y))

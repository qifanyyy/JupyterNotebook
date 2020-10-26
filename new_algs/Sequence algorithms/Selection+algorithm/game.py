"""main game class module"""
import random
import pygame
import creature
import food


class Game():
    """game class that handles pygame and important variables"""

    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((700, 700))
        pygame.display.set_caption("Natural Selection")

        self.last_spawn = 0
        self.last_print = 0
        self.all_ctr = []
        self.all_food = []

    def run(self):
        """main game loop"""
        self.spawn_creature(15)
        self.spawn_food(20)
        run = True
        while run:
            time = pygame.time.get_ticks()
            pygame.time.wait(1)  # uses less cpu than delay

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.print_data(5000, time)
            self.refill_food(20, 1000, time)
            self.creature_action(time)
            self.redraw()

        pygame.quit()

    def spawn_creature(self, num):
        """spawns num creatures"""
        for _ in range(num):
            x_pos = random.randrange(1, 700)
            y_pos = random.randrange(1, 700)
            self.all_ctr.append(creature.Creature(x_pos, y_pos))

    def spawn_food(self, num):
        """spawns num food in random locations"""
        for _ in range(num):
            x_pos = random.randrange(1, 700)
            y_pos = random.randrange(1, 700)
            self.all_food.append(food.Food(x_pos, y_pos))

    def creature_action(self, time):
        """carries out all creature processes"""
        for ctr in self.all_ctr:
            ctr.move(self.all_ctr, self.all_food, time)
            ctr.attack()
            ctr.starve(self.all_ctr, time)

    def refill_food(self, num, refill_delay, time):
        """spawns in num food in refill_delay increments"""
        if time - self.last_spawn >= refill_delay:
            # pg.FOOD = []
            self.spawn_food(num)
            self.last_spawn = time

    def print_data(self, delay, time):
        """prints average genome of population"""
        if time - self.last_print >= delay:
            print(len(self.all_ctr))
            self.last_print = time

    def redraw(self):
        """redraws entire game"""
        self.win.fill((0, 0, 0))
        for apple in self.all_food:
            apple.draw(self.win)
        for ctr in self.all_ctr:
            ctr.draw(self.win)
        pygame.display.update()

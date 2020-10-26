"""creature class module"""
import math
import random
import pygame
import genome


class Creature():
    """creature has different attributes based off its genes"""
    img1 = pygame.image.load('assets/creature.png')
    img2 = pygame.image.load('assets/mating_creature.png')
    img3 = pygame.image.load('assets/attacking_creature.png')

    def __init__(self, x, y):
        self.gene = genome.Genome()
        self.x_pos = x
        self.y_pos = y
        self.rad = 10
        self.health = 30 + 30 * ((20 * self.gene.dna[0]) / 100)
        self.damage = 10 + 10 * ((20 * self.gene.dna[1]) / 100)
        self.speed = 0.5 + 0.5 * ((20 * self.gene.dna[2]) / 100)
        self.vision = 80 + 80 * ((20 * self.gene.dna[3]) / 100)
        self.aggro = 20 + 20 * ((20 * self.gene.dna[4]) / 100)
        self.satiation = 0
        self.last_starve = 0
        self.hunger = 8000 - 1000 * self.speed - 6 * self.vision
        self.c_img = pygame.transform.scale(
            self.img1, (self.rad*2, self.rad*2))
        self.mc_img = pygame.transform.scale(
            self.img2, (self.rad*2, self.rad*2))
        self.ac_img = pygame.transform.scale(
            self.img3, (self.rad*2, self.rad*2))
        self.attack_ticks = 0
        self.last_attack = 0
        self.closest_food = 0
        self.wander_dir = random.randrange(4)
        self.wander_count = 1000

    def attack(self):
        """determines if the creature is in attack mode"""
        rand = random.randint(1, 100000)
        if self.aggro > rand:
            self.attack_ticks = 1000

    def move(self, all_ctr, all_food, time):
        """moves creature"""
        self.attack_ticks -= 1
        other_move = False
        # breeding & attacking
        for ctr in all_ctr:
            if self.satiation >= 7 and self.attack_ticks < 0:
                if ctr != self and ctr.satiation >= 7 and ctr.attack_ticks < 0 and self.distance((self.x_pos, self.y_pos), (ctr.x_pos, ctr.y_pos)) <= self.vision:
                    self.move_towards(ctr.x_pos, ctr.y_pos)
                    if self.distance((self.x_pos, self.y_pos), (ctr.x_pos, ctr.y_pos)) < self.rad * 1.5:
                        self.satiation -= 5
                        ctr.satiation -= 5
                        all_ctr.append(self.reproduce(
                            self.x_pos, self.y_pos, self.gene.dna, ctr.gene.dna))
                    other_move = True
            elif self.attack_ticks >= 0:
                if ctr != self and self.distance((self.x_pos, self.y_pos), (ctr.x_pos, ctr.y_pos)) <= self.vision:
                    self.move_towards(ctr.x_pos, ctr.y_pos)
                    if self.distance((self.x_pos, self.y_pos), (ctr.x_pos, ctr.y_pos)) < self.rad * 1.5:
                        if time - self.last_attack >= 1000:
                            ctr.health -= self.damage
                            self.satiation += 3
                            self.last_attack = time
                    other_move = True

        # eating | does not move to closest everytime (should rework to that with good algorithm)
        if not other_move:
            if self.closest_food not in all_food:
                for apple in all_food:
                    if self.distance((self.x_pos, self.y_pos), (apple.x_pos, apple.y_pos)) <= self.vision:
                        self.closest_food = apple
                        break
            if self.closest_food != 0:
                self.move_towards(self.closest_food.x_pos,
                                  self.closest_food.y_pos)
                if self.distance((self.x_pos, self.y_pos), (self.closest_food.x_pos, self.closest_food.y_pos)) < self.closest_food.rad * 1.5:
                    try:
                        # sometimes is deleted twice?
                        all_food.pop(all_food.index(self.closest_food))
                        self.closest_food = 0
                        self.eat()
                    except ValueError:
                        pass
                other_move = True

        # wandering movement
        if not other_move:
            if self.wander_count <= 0:
                self.wander_dir = random.randrange(4)
                self.wander_count = 100
            if self.wander_dir == 0:
                if self.x_pos + self.rad + self.speed > 700:
                    self.wander_dir = 1
                else:
                    self.x_pos += self.speed
                self.wander_count -= 1
            elif self.wander_dir == 1:
                if self.x_pos - self.rad - self.speed < 0:
                    self.wander_dir = 0
                else:
                    self.x_pos -= self.speed
                self.wander_count -= 1
            elif self.wander_dir == 2:
                if self.y_pos + self.rad + self.speed > 700:
                    self.wander_dir = 3
                else:
                    self.y_pos += self.speed
                self.wander_count -= 1
            elif self.wander_dir == 3:
                if self.y_pos - self.rad - self.speed < 0:
                    self.wander_dir = 2
                else:
                    self.y_pos -= self.speed
                self.wander_count -= 1

    def move_towards(self, x_pos, y_pos):
        """moves creature towards given pair of coordinates"""
        if self.x_pos < x_pos:
            self.x_pos += self.speed
        else:
            self.x_pos -= self.speed
        if self.y_pos < y_pos:
            self.y_pos += self.speed
        else:
            self.y_pos -= self.speed

    def eat(self):
        """increases satiation after eating"""
        self.satiation += 1

    def starve(self, all_ctr, time):
        """uses up satiation every 'hunger' seconds, dies if no satiation"""
        if self.last_starve == 0:
            self.last_starve = time
        elif time - self.last_starve >= self.hunger:
            self.satiation -= 1
            self.last_starve = time
        if self.satiation < 0 or self.health < 0:
            all_ctr.pop(all_ctr.index(self))

    def reproduce(self, x_pos, y_pos, dna1, dna2):
        """creates new child creature"""
        new_creature = type(self)(x_pos, y_pos)
        new_creature.gene.combine(dna1, dna2)
        new_creature.gene.mutate()
        new_creature.update_atts()
        return new_creature

    def update_atts(self):
        """updates attributes to be affected by genes"""
        self.health = 30 + 30 * ((10 * self.gene.dna[0]) / 100)
        self.damage = 10 + 10 * ((10 * self.gene.dna[1]) / 100)
        self.speed = 0.5 + 0.5 * ((10 * self.gene.dna[2]) / 100)
        self.vision = 80 + 80 * ((10 * self.gene.dna[3]) / 100)
        self.aggro = 20 + 20 * ((10 * self.gene.dna[4]) / 100)
        self.hunger = 8000 - 1000 * self.speed - 6 * self.vision

    def distance(self, point1, point2):
        """distance formula function that takes two tuples"""
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    def draw(self, win):
        """draws creature"""
        if self.attack_ticks >= 0:
            win.blit(self.ac_img, (self.x_pos-self.rad,
                                   self.y_pos-self.rad))
        elif self.satiation >= 3:
            win.blit(self.mc_img, (self.x_pos-self.rad,
                                   self.y_pos-self.rad))
        else:
            win.blit(self.c_img, (self.x_pos-self.rad,
                                  self.y_pos-self.rad))
        # shows vision (for debug)
        # pygame.draw.circle(WIN, (255, 0, 0),
        #                   (round(self.x_pos), round(self.y_pos)), round(self.vision), 1)

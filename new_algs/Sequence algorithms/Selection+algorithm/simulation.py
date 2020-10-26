import numpy as np
import pygame
import individual


class Simulation():
    """Simulation handles pygame and important variables"""

    def __init__(self):
        pygame.init()
        self.size = 700                                                 # Window size (square)
        self.display = pygame.display.set_mode((self.size, self.size))  # Creates our window
        pygame.display.set_caption("Natural Selection")                 # Gives window a name
     
        self.population = []    # Contains our individuals, could later make this a class

    def run(self):
        """ Main loop """
        self.spawn(15)      # Creates 15 individuals

        run = True
        while run:
            time = pygame.time.get_ticks()  # Gets the total elapsed time (milliseconds)

            for event in pygame.event.get():    # Listen for pygame events
                if event.type == pygame.QUIT:
                    run = False

            self.act()
            self.draw()

        pygame.quit()

    def spawn(self, num):
        """ Adds a number of individuals to our population at randon positions """
        for _ in range(num):
            pos = np.random.random(2) * self.size
            self.population.append(individual.Individual(pos))

    def act(self):
        """ Executes all the individual processes """
        for individual in self.population:
            individual.move()

    def draw(self):
        """ Draws each frame """
        self.display.fill((0, 0, 0))        # Black background

        for individual in self.population:  # Draw all the individuals
            individual.draw(self.display)
        pygame.display.update()             # Updates the display window


# Is only executed if this file is the file that have been run.
# This is common practice in python
if __name__ == '__main__':
    simulation = Simulation()
    simulation.run()

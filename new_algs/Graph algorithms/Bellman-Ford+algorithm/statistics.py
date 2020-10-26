from matplotlib import pyplot
from utils.maze import *
from utils.configuration import *

x = int(windowWIDTH/2)
y = int(windowHEIGHT/2)

class Statistics:
    def __init__(self):
        self.astar_counter = 0
        self.djikstra_counter = 0
        self.bf_counter = 0

    def iterations_reset(self):
        self.astar_counter = 0
        self.djikstra_counter = 0
        self.bf_counter = 0

    def astar_iterate(self):
        self.astar_counter = self.astar_counter + 1

    def djikstra_iterate(self):
        self.djikstra_counter = self.astar_counter + 1

    def bf_iterate(self):
        self.bf_counter = self.bf_counter + 1

    def time_complexity_plot(self, nodes, connections, time):
        pyplot.plot([1, 2, 3, 4], [1, 4, 9, 16], 'ro')
        pyplot.axis([0, 6, 0, 20])
        pyplot.show()

    def welcome_info(self):
       copyright_font = pygame.font.SysFont(None, 20)
       small_font = pygame.font.SysFont(None, 20)
       big_font = pygame.font.SysFont(None, 40)
       controls_y = 90
       label_title = big_font.render("PATHFINDING ALGORITHMS", 1, (0,0,0))
       label_copyright = copyright_font.render("Copyright © Maciej Łacwik 2018", 1, (0,0,0))
       label_controls = small_font.render("CONTROLS ", 1, (0,0,0))
       label_controls1 = small_font.render("space  =  pause", 1, (0,0,0))
       label_controls2 = small_font.render("s  =  show statistics ", 1, (0,0,0))
       label_controls3 = small_font.render("r  =  reset ", 1, (0,0,0))
       mainWindow.blit(label_title, (x+10, y+20))
       mainWindow.blit(label_copyright, (x+10, y+50))
       mainWindow.blit(label_controls, (x+10, y+controls_y))
       mainWindow.blit(label_controls1, (x+10, y+controls_y+20))
       mainWindow.blit(label_controls2, (x+10, y+controls_y+35))
       mainWindow.blit(label_controls3, (x+10, y+controls_y+50))

    def display(self, bf_time, dijksta_time, astar_time):
       normalFont = pygame.font.SysFont(None, 30)
       captionFont = pygame.font.SysFont(None, 45)
       x_iterations = 10
       y_iterations = 10
       label_iterations = captionFont.render("Iterations", 1, (0,0,0))
       label_bf_iterations = normalFont.render("BF:         " + str(self.bf_counter), 1, (0,0,0))
       label_dijkstra_iterations = normalFont.render("Dijkstra: " + str(self.djikstra_counter), 1, (0,0,0))
       label_astar_iterations = normalFont.render("A*:          " + str(self.astar_counter), 1, (0,0,0))
       x_time = 10
       y_time = 180
       label_time = captionFont.render("Time", 1, (0,0,0))
       label_bf_time = normalFont.render("BF:         " + str(bf_time) + "s", 1, (0,0,0))
       label_dijksta_time = normalFont.render("Dijkstra: " + str(dijksta_time) + "s", 1, (0,0,0))
       label_astar_time = normalFont.render("A*:          " + str(astar_time) + "s", 1, (0,0,0))
       
       mainWindow.blit(label_iterations, (x+x_iterations+120, y+y_iterations))
       mainWindow.blit(label_bf_iterations, (x+x_iterations, y+y_iterations+30))
       mainWindow.blit(label_dijkstra_iterations, (x+x_iterations, y+y_iterations+60))
       mainWindow.blit(label_astar_iterations, (x+x_iterations, y+y_iterations+90))
       mainWindow.blit(label_time, (x+x_time+150, y+y_time-30))
       mainWindow.blit(label_bf_time, (x+x_time, y+y_time))
       mainWindow.blit(label_dijksta_time, (x+x_time, y+y_time+30))
       mainWindow.blit(label_astar_time, (x+x_time, y+y_time+60))


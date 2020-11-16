from utils.cell import cell
from utils.maze import maze
from utils.statistics import *
from utils.configuration import *
from utils.algorithms import *
from pygame.locals import *
import cProfile

PROGRAM_END = False

pygame.init()
pygame.display.set_caption("Maciej Łacwik || maze generator + pathfinding")

sub1 = mainSurface.subsurface(p1_camera)
sub2 = mainSurface.subsurface(p2_camera)
sub3 = mainSurface.subsurface(p3_camera)
sub4 = mainSurface.subsurface(p4_camera)

maze1 = maze(sub1)
maze1.generate()
maze2 = maze(sub2)
maze2.generate()
maze3 = maze(sub3)
maze3.generate()

#maze1.generate()
#maze2.generate() #maze
#maze3.generate()


#maze1.load_level_1()
#maze2.load_level_1() # whiteboard
#maze3.load_level_1()

maze1.load_level_2()
maze2.load_level_2() # uncomment ony for more than 14 x 14 cells
maze3.load_level_2()

algorithm = Algorithms()
statistics = Statistics()

end_x = rows-1
end_y = cols-1


#bf_file = open("bf_plot_data.txt", "a")
#maze1.generate()
#maze1.count_connections()
#print("connections: " + str(maze1.connections_number))
#while(algorithm.bf_stop == False):
#    algorithm.bellman_ford(maze1.mainGrid[0][0],maze1.mainGrid[end_x][end_y], maze1)
#algorithm.reset(maze1)
#bf_file.write(str(algorithm.bf_time) + " " + str(maze1.connections_number) + "\n")

# -------- Main Program Loop -----------
while not PROGRAM_END:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == K_SPACE:
            PAUSE = not PAUSE
            print("-----STOPPED-----")
        if event.type == pygame.KEYDOWN and event.key == K_s:
            SHOW_STATS = not SHOW_STATS
        if event.type == pygame.KEYDOWN and event.key == K_r:
            algorithm.reset(maze3)
            algorithm.reset(maze2)
            algorithm.reset(maze1)
            statistics.iterations_reset()
        if event.type == pygame.QUIT:
            PROGRAM_END = True

    if(not PAUSE and algorithm.astar_stop == False): 
        algorithm.astar(maze3.mainGrid[7][7],maze3.mainGrid[end_x][end_y], maze3)
        #cProfile.run('algorithm.astar(maze3.mainGrid[0][0],maze3.mainGrid[end_x][end_y], maze3)', 'stats.txt')
        statistics.astar_iterate()

    if(not PAUSE and algorithm.djikstra_stop == False):
        algorithm.djikstra(maze2.mainGrid[7][7],maze2.mainGrid[end_x][end_y], maze2)
        statistics.djikstra_iterate()

    if(not PAUSE and algorithm.bf_stop == False):
        algorithm.bellman_ford(maze1.mainGrid[7][7],maze1.mainGrid[end_x][end_y], maze1)
        statistics.bf_iterate()
        
    maze1.draw()
    maze2.draw()
    maze3.draw()

    #statistics window
    sub4.fill(LIGHT_BLUE)
    pygame.draw.line(sub4, GREY, (0,0),(0, int(windowHEIGHT/2)), 8)
    pygame.draw.line(sub4, GREY, (0,0),(int(windowWIDTH/2), 0), 8)

    mainWindow.blit(sub1, (0,0))
    mainWindow.blit(sub2, (int(windowWIDTH/2), 0))
    mainWindow.blit(sub3, (0, int(windowHEIGHT/2)))
    mainWindow.blit(sub4, (int(windowWIDTH/2), int(windowHEIGHT/2)))


    if(SHOW_STATS == True):
        statistics.display(algorithm.bf_time, algorithm.dijkstra_time, algorithm.astar_time)
    else:
        statistics.welcome_info()

    pygame.display.flip()
    clock.tick(framerate)
pygame.quit()
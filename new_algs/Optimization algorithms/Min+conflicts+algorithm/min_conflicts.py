import random
from map_data_types import *

def min_conflicts(map):

    graph = map.graph

    # Randomly colors the graph
    for point in graph:
        rand_color = random.randint(1, 5)
        point.color = rand_color

            
    # Runs until a solution is found. I did not use recursion
    # for this algorithm, which I don't know if you would 
    # rather use for it.        
    while (finished != True):
        finished = True
        
        # check for solution
        for point in graph:
            if point.has_conflicting_neighbors() == True:
                finished = False
                
        # Minimum conflicts algorithm 
        for point in graph:
            if point.has_conflicting_neighbors():
                min_conflicts = 100
                next_color = point.color
                
                # Loops through colors to see which one has
                # the least conflicts
                for j in range(1, 5):
                    point.color = j
                    if point.conflicts < min_conflicts:
                        min_conflicts = point.conflicts
                        next_color = j         
                point.color = next_color
                                            
        # Updates the number of conflicts
        for point in graph:
            point.conflicts = 0
            for pt in point.neighbors:
                if (pt.color == point.color):
                point.conflicts += 1
                
                
    return True
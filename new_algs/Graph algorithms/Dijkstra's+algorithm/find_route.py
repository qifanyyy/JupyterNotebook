import argparse
import sys
import heapq

# Handles command line inputs
def input_handler():
    # Command line parser to handle inputs, all of which are required for the program to run
    parser = argparse.ArgumentParser(description="An implementation of dijkstra's algorithm to find the shortest path between two cities on a graph/map.")
    parser.add_argument('-i', '--input', required=True, type=str, help='The name of the (correctly formatted) input file.')
    parser.add_argument('-o', '--origin', required=True, type=str, help='The name of the starting location/city.')
    parser.add_argument('-t', '--target', required=True, type=str, help='The name of the destination location/city.')

    args = parser.parse_args()

    # Assigning argument information to variables
    input = args.input
    origin = args.origin
    target = args.target

    return input, origin, target

# Models the input file as a graph from an input file
def graph_modeler(input):

    # Opens input file
    fileHandler = open(input)

    # Dictionary that represents the graph of the cities
    # Graph is structured as the name of the city as the key and a tuple 
    # of the bordering city and its distance as the value
    cityGraph = {}

    # Reads the first line of the file for the while loop to work
    line = fileHandler.readline()

    # Reading in the contents of the file until the end signifier
    while line != 'END OF INPUT':
        info = line.rstrip('\n').split(' ')

        # If the city exists in the graph already, add the next adjacent city to the value list
        if info[0] in cityGraph:
            cityGraph[info[0]].append((info[1], int(info[2])))
            if info[1] in cityGraph:
                cityGraph[info[1]].append((info[0], int(info[2])))
            else:
                cityGraph[info[1]] = [(info[0], int(info[2]))]
        # Otherwise, create a new list at this index 
        else:
            cityGraph[info[0]] = [(info[1], int(info[2]))]
            # This graph is undirected, so include both directions
            cityGraph[info[1]] = [(info[0], int(info[2]))]
        
        # Read the next line
        line = fileHandler.readline()
    
    fileHandler.close()
    return cityGraph


# Uses Dijkstra's algorithm to search the maze for the shortest path between the
# start and target cities using a min-priority queue
# Refrences: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm and
# https://towardsdatascience.com/introduction-to-priority-queues-in-python-83664d3178c3
def dijkstra_search(graph, start, end):
    # Initializing the needed data structures
    distances = {vertex: sys.maxsize for vertex in graph}
    distances[start] = 0

    # Record of path taken
    previous = {vertex: '' for vertex in graph}

    # Priority queue of vertices used to find the solution
    bigQ = [(0, start)]

    # Keeps going until the entire connected graph section is traversed or until the program
    # finds the target city
    while len(bigQ) > 0:
        distance, current = heapq.heappop(bigQ)

        # If the target city is reached, stop the algorithm to save time + space
        if current == end:
            break

        # Checks the adjacent cities to the current vertex city to see which is the closest
        for adjacent, cost in graph[current]:
            alternate = distance + cost

            # If a new, better, path to the current vertex from the starting vertex is found,
            # switch to that shorter path
            if alternate < distances[adjacent]:
                distances[adjacent] = alternate
                previous[adjacent] = current
                heapq.heappush(bigQ, (alternate, adjacent))

    return distances, previous


# Prints the results of the dijkstra search
def print_shortest_path(graph, distances, prev, start, end):
    # Total distance traveled by the algorithm to reach the origin to the end
    totalDist = str(distances[end]) + ' km'
    # Path list holds strings that keep track of the path taken
    interSteps = []
    path = ''

    # If the total distance between the target and end cities is infinite, no path exists
    if distances[end] == sys.maxsize:
        totalDist = 'infinity'
        path = 'none\n'
    
    # Otherwise, trace the path list back to the beginning to get the path taken 
    # (and the distances between each intermediate step)
    else:
        traceback = end

        # Tracing the previous city record for the cities traveled  
        while traceback != start:
            tempdist = 0
            back = prev[traceback]

            # Searches adjacent cities for the one traveled by the algorithm
            for city in graph[back]:
                if city[0] == traceback:
                    tempdist = city[1]
            
            # Adding the relevant information to the path list
            interSteps.append(back + ' to ' + traceback + ', ' + str(tempdist) + ' km\n')
            traceback = back
        
        # Reformatting the path list to adhere to output format
        for step in reversed(interSteps):
            path += step
    
    # Finally, print the results to the console
    print('distance: ', totalDist, '\nroute:\n', path, sep='', end = '')
        
file, start, end = input_handler()
cityGraph = graph_modeler(file)
dists, prevs = dijkstra_search(cityGraph, start, end)
print_shortest_path(cityGraph, dists, prevs, start, end)
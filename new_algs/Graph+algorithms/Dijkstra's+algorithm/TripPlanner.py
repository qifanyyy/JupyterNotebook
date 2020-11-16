# TripPlanner.py
# Eric Du
# edu1@stu.parkland.edu
# CSC 220, Spring 2016
# Plan trip - find shortest path between two cities

from shortest_paths import shortest_path_lengths, shortest_path_tree
from graph import Graph
from ask_input import ask_input

class TripPlanner():
    """Trip planner that finds shortest path between two cities and prints
    graph schematic of European railway map.
    """
    
    def __init__(self, args):
        self.__origin = None
        self.__destination = None
        self.__map = Graph(False)

    def info(self):
        """Print graph info: number of cities and connections."""
        print("Number of cities: ", self.__map.vertex_count())
        print("Number of connections: ", self.__map.edge_count())

    def plan(self):
        """Plan trip, giving shortest path between origin and destination
        and its path length.
        """
        cloud = shortest_path_lengths(self.__map, self.__origin)
        tree = shortest_path_tree(self.__map, self.__origin, cloud)
        d = self.__destination
        # list storing stops between origination and destination
        stops = [self.__destination.element()]
        if (self.__destination in cloud and cloud[self.__destination] 
        != float('inf')):
            print("The shortest travel time from", self.__origin, "to",
            self.__destination, "is by going through these \
            intermediary stops:")
            while True:
                stops.append(tree[d].opposite(d).element())
                d = tree[d].opposite(d)
                if d is self.__origin:
                    break
            for i in range(len(stops)):
                print("  ", stops.pop())
            print("Total travel time is", cloud[self.__destination], 
            "minutes.\n")
        else:
            print("This trip is not possible.")
        
    def schematic(self, args):
        """Write out schematic (GraphViz file)."""
        cloud = shortest_path_lengths(self.__map, self.__origin)
        tree = shortest_path_tree(self.__map, self.__origin, cloud)
        d = self.__destination
        # list storing edges between each stop from origin to destination
        stop_edges = []
        if (self.__destination in cloud and cloud[self.__destination] 
                    != float('inf')):
            while True:
                stop_edges.append(tree[d])
                d = tree[d].opposite(d)
                if d is self.__origin:
                    break
        else:
            print("Schematic cannot show shortest travel time between\
            given cities.")
        with open(args.itinerary, 'w') as outfile:
            outfile.write('graph {\n')
            # origin colored green
            outfile.write('  ' + self.__origin.element() + ' ' + 
            '[color=green]\n')
            # destination colored red
            outfile.write('  ' + self.__destination.element() + ' ' +
            '[color=red]\n')
            for e in self.__map.edges():
                vs = e.endpoints()
                if e in stop_edges:
                    outfile.write('  ' + vs[0].element() + ' ' + '--' + ' ')
                    outfile.write(vs[1].element() + ' ')
                    # shortest path edges are colored blue
                    outfile.write('[label="' + str(e.element()) + 
                    '", color=blue]\n')
                else:
                    outfile.write('  ' + vs[0].element() + ' ' + '--' + ' ')
                    outfile.write(vs[1].element() + ' ')
                    outfile.write('[label="' + str(e.element()) + '"]\n')
            outfile.write('}')
        print("Your output file has been saved.\nOrigin is labelled green, \
        destination is labelled red.")
        print("Shortest path length is labelled blue.\n")

    def graph_eurail(self, args):
        """Create adjacency map graph based on city/connection data 
        from eurail.txt.
        """
        # list of origins as strings
        origins = []
        # list of destinations as strings
        destinations = []
        # list of edge lengths
        times = []
        # dictionary of vertices with city names as keys, vertices as values
        vertices = {}
        # set of vertices as strings
        vertex_set = set()
        with open(args.timetable, 'r') as infile:
            for line in infile:
                li = line.split(',')
                vertex_set.add(li[0])
                vertex_set.add(li[1])
                origins.append(li[0])
                destinations.append(li[1])
                t = li[2].split(':')
                time = int(t[0]) * 60 + int(t[1])
                times.append(time)

        for vertex in vertex_set:
            vertices[vertex] = self.__map.insert_vertex(vertex)
            
        for i in range(len(origins)):
            if origins[i] in vertices:
                if destinations[i] in vertices:
                    # insert edge for each vertex in dictionary verts
                    self.__map.insert_edge(vertices[origins[i]], 
                            vertices[destinations[i]], times[i])

        while True:
            print("File loading...")
            print("There are {} cities with {} connections.".format(
                    self.__map.vertex_count(), self.__map.edge_count()))
            # input origin city
            origin = input('Please enter an origin: ')
            if origin not in vertices:
                raise ValueError('City not in database')
            destination = input('Please enter a destination: ')
            # input destination city
            if destination not in vertices:
                raise ValueError('City not in database')
            self.__origin = vertices[origin]
            self.__destination = vertices[destination]
            self.plan()      # print shortest path length
            choice = ask_input("Quit? [y/n] ", str.lower, range_=('y', 'n'))
            if choice == 'y':
                if args.itinerary:
                    # save .gv file with data for trip and connections
                    self.schematic(args)
                    print("Thank you for using the EU Rail Planner.")
                    break
                else:
                    break
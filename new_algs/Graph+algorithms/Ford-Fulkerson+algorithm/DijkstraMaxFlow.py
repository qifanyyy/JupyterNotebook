#constants
infinity = 1000000
invalid_node = -1

class Node: # Node class w/ default values
    previous = invalid_node
    distfromsource = infinity
    visited = False

    #################################################################################################################################

class Dijkstra: # Class encapsulating the Dijkstra algorithm

    def __init__(self):                                             # Default constructor for the algorithm - starting values ready for algorithm to start
        '''initialise class'''
        self.startnode = 0                                          # The entry point for the algorithm, from this node...
        self.endnode = 0                                            # ... to this node - both are numerical to be used as an index
                                                                    # (Node A = nodetable[0], Node B = nodetable[1] etc)
        self.network = []                                           # A list of lists to hold information on nodes and their edges
        self.network_populated = False                              # Boolean confirming a populated network list
        self.nodetable = []                                         # A list that contains an instance of the Node class for every element in network[]
        self.nodetable_populated = False                            # Boolean confirming a populated node list
        self.route = []                                             # A two element list, where route[0] = starting node, route[1] = end node
        self.route_populated = False                                # Boolean confirming a populated route list
        self.currentnode = 0                                        # The node that will be tracked and evaluated through each iteration

    def populate_network(self, filename):                           # Method to insert the network into its list of lists from a text file (filename)
        '''populate network data structure'''
        try:                                                        # Attempt to open the target file...
            networkfile = open(filename, "r")
        except IOError:                                             # ... Handles exception if the file cannot be opened
            print ("Network file does not exist!")                    # Alerts the user that the file could not be found
            return                                                  # Ends method
        for line in networkfile:                                    # For every line in the file...
            self.network.append(list(map(int, line.strip().split(','))))  # ... strip the line, using "," as a divider
                                                                    # into another list within network, creating a list of lists
        self.network_populated = True                               # Network is populated!
        networkfile.close()                                         # File is no longer needed and is closed for security

    def populate_node_table(self):                                  # Method to populate the nodetable with instances of Node()
        '''populate node table'''
        if not self.network_populated:                              # If the network hasn't been populated for any reason, alerts the user and exits
            print ("Network not populated!")
            return
        for node in self.network:                                   # For every node in network[] (i.e, index)
            self.nodetable.append(Node())                   # Add a Node() into nodetable
                                                                    # The start node (declared in parse_route() is handled here
        self.nodetable[self.startnode].distfromsource = 0           # The starting node is the source and so has a distance of 0, always
        self.nodetable[self.startnode].visited = True               # The starting node has been visited before anything and is set here
        self.nodetable_populated = True                             # Nodetable has been populated! Yay!

    def parse_route(self, filename):                                # Method that takes in a text file that contains the route
        '''load in route file'''
        try:                                                        # Attempt to open the target file...
            routefile = open(filename, "r")
        except IOError:                                             # ... Handles exception if the file cannot be opened
            print ("Route file does not exist!")                      # Alerts the user that the file could not be found
            return                                                  # Exists the method
        self.route = routefile.read().split('>')                    # Takes the single line from the text file (In the format "L>L")
                                                                    # ... and inserts the two characters from either side of ">" into route[]
        self.startnode = (ord(self.route[0])-65)
        self.endnode = (ord(self.route[1])-65)
            # Ord() returns an integer of the ASCII character in its argument...
            # ... Assume route at this point = ['A','F']. The ASCII code for A is 65, and so to get its position in the network...
            # ... We must subtract 65 to get 0 - the position of Node A in nodelist - and return it as an int rather than a char...
            # ... And now startnode and endnode hold the index position of the nodes in the text file
        if self.startnode > (len(self.network)-1) or self.endnode > (len(self.network)-1): # Checking route is in range of the network
            self.route_populated = False
            print ("Route Given is Out of Range!")
        else:
            self.route_populated = True
            print ("Finding Shortest Path Between", self.route[0], "and", self.route[1], "...")     # Alerting user
        self.currentnode = self.startnode                                                       # Beginning the algorithm, the currentnode being tracked is the same as the starting node

        routefile.close()                                                                       # Close the file for security


    def return_near_neighbour(self):                                    # Method to return a list of the current node's neighbours (nodes it has an edge with)
        '''determine nearest neighbours of current node'''
        if not self.route_populated:                                    # Measure just in case the route table has not been populated for any reason
            print ("Route Invalid or Not Found!")
            return
        neighbours = []                                                 # A list to hold the neighbours of the current node
        for index, edge in enumerate(self.network[self.currentnode]):   # Enumerate gives a counter to the loop (index)                                          # For every edge the current node has in the network list ->
            if edge > 0 and not self.nodetable[index].visited:
                neighbours.append(index)# there is an edge that hasn't been visited, it's added to the list of neighbours
        return neighbours                                               # Returns the list

    def calculate_tentative(self):                                      # Method to calculate the distance being considered for the route before deciding on the next route
        '''calculate tentative distances of nearest neighbours'''
        neighbours = self.return_near_neighbour()                       # Returns the neighbours list from return_near_neighbour for use here
        for neighbourindex in neighbours:                               # For loop to loop over every element in the neighbours list
            tentativedistance = self.nodetable[self.currentnode].distfromsource + self.network[self.currentnode][neighbourindex]
                # Calculates tentative distance by taking the current node's distance from source (e.g, 0 on the first loop)...
                # ... and adding the weight of the edge from the network list, using the currentnode to select the node to evaluate...
                # ... and neighbourindex to select the neighbour within the secondary list, which has the distance value...
                # ... from the current node

            if tentativedistance < self.nodetable[neighbourindex].distfromsource:   # Then evaluates whether the tentative distance is
                                                                                    # ... less than the neighbour's distance
                self.nodetable[neighbourindex].distfromsource = tentativedistance   # If so, the neighbour's distance from source is switched
                                                                                    # ... to tentativedistance
                self.nodetable[neighbourindex].previous = self.currentnode          # The current node's index is set as its neighbour's previous node

    def determine_next_node(self):                                              # Method to determine the next node to be evaluated
        '''determine next node to examine'''
        bestdistance = infinity                                                 # A best distance is used to store the best possible distance at the moment
        self.currentnode = invalid_node                                         # The current node is set as invalid
        for nodeindex, node in enumerate(self.nodetable):                       # Loops through every node in the node table
            if node.distfromsource < bestdistance and node.visited == False:   # If the distance from source is less than the best distance...
                                                                             # ... and hasn't been visited before
                bestdistance = node.distfromsource                              # This node's distance from the source replaces the current bestdistance...
                self.currentnode = nodeindex                                   # ... and the node is then set as the current node
                # This basically runs through the entire node list and selects the node with the least distance that hasn't been visited,
                # ... as per the algorithm

    def calculate_shortest_path(self): # Method that uses the above methods to calculate the shortest route between start and end node
        ''' calculate shortest path across the network '''
        #DEBUG: LOOPS FOREVER here
        while self.currentnode is not self.endnode or self.currentnode == invalid_node: # While the current node isn't the end node...
            self.nodetable[self.currentnode].visited = True # The current node has been visited
            self.calculate_tentative() # Runs the method specified
            self.determine_next_node() # Runs the method specified
        if self.currentnode == invalid_node: # If the node is invalid...
            print ("Path Impossible!") # User is notified and the method returns False
            return False
        else:
            print ("Path Possible!")
            return True # Otherwise node is valid and can carry on - returns as True
        # Boolean return value used in return_shortest_path

    def return_shortest_path(self):
        ''' return shortest path as list (start->end), and total distance'''
        shortest_path = [] # A list to hold the shortest path (i.e, [startnode, checkpoint1, checkpoint2, ..., endnode])

        if self.calculate_shortest_path(): #If it's still possible to calculate the shortest path (i.e, current node is not invalid)
            while self.currentnode != invalid_node: # Until the currentnode becomes invalid (i.e, all previous nodes have been added to the list)
                shortest_path.append(chr(self.currentnode + 65))
                    # Similar to ord(), chr() does the reverse and returns the character value of an ASCII code
                    # i.e, if currentnode = 0, the argument will be (chr(0+65)) = (chr(65)). The symbol for ASCII code 65 is 'A',
                    # and so this char is returned and then append to the shortest_path list
                self.currentnode = self.nodetable[self.currentnode].previous # The currentnode being tracked is switched to the one
                                                                             # before - the path will be added in reverse order initially, here
            totaldistance = self.nodetable[self.endnode].distfromsource # The endnode's distancefrom source is now stored into a totaldistance variable
            shortest_path = shortest_path[::-1] # Slicing the list and reversing using -1 - the table is now in the correct order from start to end
        print ("Shortest Path:", shortest_path) # Prints the path taken and then the distance of this route
        print ("Total Distance:", totaldistance)
        return shortest_path, totaldistance # Returns both items


    #################################################################################################################################

class MaxFlow(Dijkstra): # Inherits from Dijkstra
    def __init__(self):
        '''initialise class'''
        self.startnode = 0
        self.endnode = 0
        self.network = []
        self.network_populated = False
        self.nodetable = []
        self.nodetable_populated = False
        self.route = []
        self.route_populated = False
        self.currentnode = 0
        self.bottleneck = infinity;         # The bottleneck value is the minimum weight within a path
                                            # i.e, no flow higher than this value can traverse the path
        self.path_nodes = []                # a list containing the nodes in a path in their Node instance
        self.flow = 0                       # Variable to hold the current flow as its being calculated
        self.path_exists = True             # Boolean to represent whether there are still possible paths

    def return_shortest_path(self):
        shortest_path = [] # A list to hold the shortest path (i.e, [startnode, checkpoint1, checkpoint2, ..., endnode])

        if self.calculate_shortest_path(): #If it's still possible to calculate the shortest path (i.e, current node is not invalid)
            while self.currentnode != invalid_node: # Until the currentnode becomes invalid (i.e, all previous nodes have been added to the list)
                shortest_path.append(chr(self.currentnode + 65))
                    # Similar to ord(), chr() does the reverse and returns the character value of an ASCII code
                    # i.e, if currentnode = 0, the argument will be (chr(0+65)) = (chr(65)). The symbol for ASCII code 65 is 'A',
                    # and so this char is returned and then append to the shortest_path list
                self.path_nodes.append(self.currentnode)
                    # path_nodes is a list containing the actual nodes (as a Node type) of the current evaluated path
                    # to be used later calculating max flox and its corresponding bottleneck
                self.currentnode = self.nodetable[self.currentnode].previous # The currentnode being tracked is switched to the one
                                                                             # before - the path will be added in reverse order initially, here
            totaldistance = self.nodetable[self.endnode].distfromsource # The endnode's distancefrom source is now stored into a totaldistance variable
            shortest_path = shortest_path[::-1] # Slicing the list and reversing using -1 - the table is now in the correct order from start to end
            print ("Path Found: ", shortest_path) # Prints the path taken and then the distance of this route
            return self.path_nodes # Returns path_nodes
        else:
            self.path_exists = False
            return

    def calculate_shortest_path(self): # Method that uses the above methods to calculate the shortest route between start and end node
        ''' calculate shortest path across the network '''
        while self.currentnode is not self.endnode or self.currentnode == invalid_node: # While the current node isn't the end node...
            self.nodetable[self.currentnode].visited = True # The current node has been visited
            self.calculate_tentative() # Runs the method specified
            self.determine_next_node() # Runs the method specified
            if self.currentnode == invalid_node: # If the node is invalid...
                print ("[!] No More Paths! [!]") # User is notified and the method returns False
                return False
        return True

    def calculate_bottleneck(self): # Method to calculate the bottleneck of a given path in a flow network
        self.currentnode = self.path_nodes[0] # Start calculating from the first node in the path
        while self.nodetable[self.currentnode].previous != invalid_node: # While there are nodes in the table
            weight = self.return_weight() # Calls method to find the weight between the current node and the previous
            if weight < self.bottleneck: # The bottleneck will be the lowest weight in the path as it restricts
                                         # the potential flow through it
                self.bottleneck = weight # ... so if the weight is less than the current held bottleneck, it becomes
                                         # the new bottleneck
            self.currentnode = self.nodetable[self.currentnode].previous # Node being evaluated is switched to the next
        print("Bottleneck: ", self.bottleneck) # Now the entire path has been evaluated, the bottleneck is set in stone
                                               # and displayed here

    def return_weight(self): # Method to find and return the weight of the path being evaluated
        weight = self.network[self.currentnode][self.nodetable[self.currentnode].previous]
        # Searches the initial network for the weight, using currentnode and its previous value
        print(chr(self.currentnode + 65), ">", chr(self.nodetable[self.currentnode].previous + 65), ": ", weight)
        # Visual information displaying the two nodes being evaluated and its newly found weight
        return weight # Returns the weight

    def calculate_max_flow(self): # Method to calculate the max flow that can be sent between the source and sink
        if self.path_exists: # If there's still a path to be evaluted...
            self.calculate_bottleneck() # Sets this MaxFlow object's bottleneck value
            self.currentnode = self.path_nodes[0] # Sets the first node to be evaluated
            self.flow += self.bottleneck # The bottleneck is the maximum flow that can be sent through a path...
                                         # ... so the bottlenecks of every possible path will be added together...
                                         # ... to create the total max flow through the network
            while self.nodetable[self.currentnode].previous != invalid_node: # While there are nodes remaining
                self.network[self.currentnode][self.nodetable[self.currentnode].previous] -= self.bottleneck
                self.network[self.nodetable[self.currentnode].previous][self.currentnode] -= self.bottleneck
                # These two lines and the while loop combined will go through the network, deducting the bottleneck...
                # ... from every weight in the path - essentially turning the network into a residual graph...
                # ... which will be used to accurately calculate future bottlenecks given that flow may have already...
                # ... been used or partially used through a certain path
                self.currentnode = self.nodetable[self.currentnode].previous #  Next node to be evaluated
            print ("Flow: ", self.flow, "\n") # Displays the current flow at the given moment (this will not...
                                              # ... not necessarily be the max flow as it may run several times again)
            self.nodetable.clear()
            self.bottleneck = infinity
            # Clears the nodetable and resets the bottleneck so the program can run again
        else:
            pass # Do nothing

if __name__ == '__main__':
    print("========= DIJKSTRA'S ALGORITHM =============")
    Dijkstra = Dijkstra() # Creates an instance of the Dijkstra class
    Dijkstra.populate_network("network.txt") # Populates the network
    Dijkstra.parse_route("route.txt") # Sets the start and end point of the wanted path
    Dijkstra.populate_node_table() # Creates nodes based on the no. of lines in network.txt
    Dijkstra.return_shortest_path() # Calculates and shows the shortest path

    for line in Dijkstra.network:
        print(line) # Displays the network

    print("============================================\n") # Divides the Algorithms visually

    print("========= MAX FLOW =========================")
    MaxFlow = MaxFlow() # Creates an instance of the MaxFlow class
    MaxFlow.populate_network("network.txt")
    MaxFlow.parse_route("route.txt")

    while MaxFlow.path_exists: # While there are still paths to be found
        MaxFlow.populate_node_table() # (Re-)Populates the node table anew
        MaxFlow.return_shortest_path() # Calculates the current shortest path
        MaxFlow.calculate_max_flow() # Calculates the max flow through the current path
        # This loops until every possible path has been evaluated and no more are possible
    for line in MaxFlow.network:
        print(line) # Displays the residual graph in its final state
    print("\nMAX FLOW: ", MaxFlow.flow, "\n") # Displays the Max Flow through the network

    print("============================================")

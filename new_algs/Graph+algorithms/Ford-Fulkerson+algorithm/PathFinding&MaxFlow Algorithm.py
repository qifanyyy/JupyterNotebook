import copy
infinity = 1000000
invalid_node = -1


class Node:
    previous = invalid_node
    distfromsource = infinity
    visited = False


class Dijkstra:
    def __init__(self):
        self.startnode = 0
        self.currentnode = 0
        self.endnode = 0
        self.network_populated = False
        self.network = []
        self.node_table = []
        self.node_table_populated = False
        self.route = []
        self.route_populated = False

    def parse_route(self, fileName):
        '''opening the file that contains the start node and the end node'''
        try:
            route_file = open(fileName, "r")
        except FileNotFoundError:
            print("File does not exist")
            return

        '''storing the start and the end nodes into the route list'''
        route = route_file.read()
        route = route.strip()
        route = route.split(">")

        '''converting the character of the route to the integer value using ASCII values'''
        self.startnode = ord(route[0]) - 65
        self.endnode = ord(route[1]) - 65
        '''setting current to the start node'''
        self.currentnode = self.startnode
        self.route_populated = True
        route_file.close()

    def calculate_tentative(self):
        '''getting all the near neighbours of the current ndoe'''
        near_neighbours = self.return_near_neighbour()
        '''going through the list of near neighbours'''
        for indexOfNode in near_neighbours:
            '''getting the initial distance of the near neighbour'''
            init_distance = self.network[self.currentnode][indexOfNode]
            '''checking if the current distance of the near neighbour is infinity (1000000)'''
            if self.node_table[indexOfNode].distfromsource == infinity:
                '''setting the previous node of the near neighbour to the current node'''
                self.node_table[indexOfNode].previous = self.currentnode
                '''adding the initial distance of the near neighbour to the current distance from source of the previous node of the near neighbour'''
                self.node_table[indexOfNode].distfromsource = self.node_table[self.node_table[indexOfNode].previous].distfromsource + init_distance
                '''checking if the current distance from source of the near neighbour is larger than the current distance from source + the initial distance of the near neighbour'''
            elif self.node_table[indexOfNode].distfromsource > self.node_table[self.currentnode].distfromsource + init_distance:
                '''setting the previous node of the near neighbour to the current node'''
                self.node_table[indexOfNode].previous = self.currentnode
                '''adding the initial distance of the near neighbour to the current distance from source of the near neighbour'''
                self.node_table[indexOfNode].distfromsource = self.node_table[self.currentnode].distfromsource + init_distance

    def return_near_neighbour(self):
        '''a list to store the indexes of the near neighbours'''
        neighbour_index_list = []
        '''determine nearest neighbours of current node'''
        '''going through every value in the current node's network list'''
        for index, value in enumerate(self.network[self.currentnode]):
            '''checking if the value is larger than zero and the node is not visited meaning that it is a valid near neighbour of the current node'''
            if value > 0 and not self.node_table[index].visited:
                '''adding the valid near neighbour to the list of near neighbours'''
                neighbour_index_list.append(index)
        '''returning the list of valid near neighbours'''
        return neighbour_index_list

    def populate_network(self, fileName):
        '''opening the file that contains the network'''
        try:
            network_file = open(fileName, "r")
        except FileNotFoundError:
            print("File does not exist")
            return
        '''going through every line in the network file and storing it in the network matrix'''
        for line in network_file:
            self.network.append(list(map(int, line.strip().split(','))))
        self.network_populated = True
        network_file.close()

    def populate_node_table(self):
        self.node_table_populated = False
        '''for every line in the network matrix an empty node is being inserted in the node table'''
        for line in self.network:
            self.node_table.append(Node())
        '''setting the initial values of the starter node'''
        self.node_table[self.startnode].distfromsource = 0
        self.node_table[self.startnode].visited = True
        self.node_table_populated = True

    def determine_next_node(self):
        '''determine next node to examine'''
        '''getting all the near neighbours'''
        near_nodes = self.return_near_neighbour()
        '''initialising the smallest node as infinity'''
        smallest_dist = infinity
        '''initialising the next node index as 0'''
        next_node = 0
        '''going through every near neighbour of the current node'''
        for node in near_nodes:
            '''getting the distance of the near neighbour'''
            node_distance = self.node_table[node].distfromsource
            '''checking if the near neighbour distance from source is smaller than the current smallest distance'''
            if node_distance < smallest_dist:
                '''setting the near neighbour distance as the current smallest distance from source'''
                smallest_dist = self.node_table[node].distfromsource
                '''setting the near neighbour as the next node'''
                next_node = node
        return next_node

    def calculate_shortest_path(self):
        '''creating the list with the length of the node table to represent the unvisited nodes'''
        unvisited_nodes = list(range(len(self.node_table)))
        '''calculate shortest path across network'''
        '''getting the near neighbours of the current'''
        near_neighbours = self.return_near_neighbour()
        '''keep looping until there are no near neighbours and no unvisited nodes'''
        while (True):
            '''checking if there are no near neighbours and unvisited nodes meaning that the algorithm went through all the nodes'''
            if len(near_neighbours) == 0 and len(unvisited_nodes) == 0:
                '''setting the current nodes as visited'''
                self.node_table[self.currentnode].visited = True
                return
                '''checking if there are no near neighbours for the current node and there are still unvisited node'''
            elif len(near_neighbours) == 0 and len(unvisited_nodes) != 0: #remove visited node
                '''the current node has no near neighbours so the only thing left to do is set it to visited'''
                self.node_table[self.currentnode].visited = True
                '''removing the current node from the unvisited list'''
                unvisited_nodes.remove(self.currentnode)
                '''setting the current node to the next available unvisited node since there are no near valid near neighbours to the current node'''
                self.currentnode = unvisited_nodes[0]
            '''calculating the tentative of the current nodes's neighbours'''
            self.calculate_tentative()
            '''setting the current node as visited'''
            self.node_table[self.currentnode].visited = True
            '''removing the current node from the list of unvisited nodes'''
            unvisited_nodes.remove(self.currentnode)
            '''setting the current node to the next node'''
            self.currentnode = self.determine_next_node()
            '''getting the near neighbours of the new current node'''
            near_neighbours = self.return_near_neighbour()


    def return_shortest_path(self):
        '''calculating the shortest path'''
        self.calculate_shortest_path()
        '''return shortest path as list (start->end), and total distance'''
        '''a variable that will go through all the nodes in the calculated path; initialising it as the end node'''
        temp_node = self.endnode
        '''storing the total distance which is the end node's distance from source'''
        total_distance = self.node_table[self.endnode].distfromsource
        '''a list that will store the path from start node to end node and the total distance'''
        path = []
        path.append(self.endnode)
        '''keep looping until the start node has been reached'''
        while self.node_table[temp_node].previous != invalid_node:
            '''inserting the previous node of the temp node to the start of the path list'''
            path.insert(0, self.node_table[temp_node].previous)
            '''set the new temp node to the previous of the current temp node'''
            temp_node = self.node_table[temp_node].previous
        '''adding the total distance of the path to the end of the path list'''
        path.append(total_distance)
        return path

class MaxFlow(Dijkstra):
    '''inherits from Dijkstra class. Expose and override Dijkstra methods and add new ones where required, but must use original Dijkstra’s algorithm as part of the calculation'''

    def __init__(self):
        super().__init__()
        '''a graph to keep track of all the residual glow in the network'''
        self.residual_graph = []
        '''a list to queue the nodes to find a path from the source to the sink'''
        self.queue = []

    def populate_network(self, fileName):
        '''opening the file that contains the network'''
        try:
            network_file = open(fileName, "r")
        except FileNotFoundError:
            print("File does not exist")
            return
        '''going through every line in the network file and storing it in the network matrix'''
        for line in network_file:
            self.network.append(list(map(int, line.strip().split(','))))
        self.network_populated = True
        network_file.close()
        self.residual_graph = copy.deepcopy(self.network)


    def populate_node_table(self):
        '''populate the node table with empty nodes for every line in the network'''
        self.node_table_populated = False
        for line in self.network:
            self.node_table.append(Node())
        '''initialising the start node values'''
        self.node_table[self.startnode].distfromsource = 0
        self.node_table[self.startnode].visited = False
        self.node_table_populated = True

    def return_near_neighbour(self):
        '''a list to store the indexes of the current node's near neighbours'''
        neighbour_index_list = []
        '''determine nearest neighbours of current node'''
        '''going through every value in the current node's residual network list'''
        for index, value in enumerate(self.residual_graph[self.currentnode]):
            '''checking if the value is larger than 0 and the node has not been visited meaning that it is a valid near neighbour'''
            if value > 0 and not self.node_table[index].visited:
                neighbour_index_list.append(index)
        return neighbour_index_list

    def findPathFromStoT(self):
        '''removing all the nodes from the node table'''
        self.node_table.clear()
        '''repopulating the node table to get default empty nodes'''
        self.populate_node_table()
        '''adding the start node to the queue'''
        self.queue.append(self.startnode)
        '''setting the current node to the first node in the queue'''
        self.currentnode = self.queue[0]
        '''setting the initial values of the starter node'''
        self.node_table[self.currentnode].visited = True
        self.node_table[self.currentnode].previous = invalid_node
        '''keep looping while there are nodes in the queue'''
        while self.queue:
            '''remove the current node from the queue'''
            self.queue.remove(self.currentnode)
            '''get all the near neighbours of the current node'''
            near_neighbours = self.return_near_neighbour()
            '''going through every near neighbour'''
            for node in near_neighbours:
                '''add the near neighbour to the queue'''
                self.queue.append(node)
                '''setting the values of the near neighbour'''
                '''setting the near neighbour as visited'''
                self.node_table[node].visited = True
                '''setting the previous node of the near neighbour as the current node'''
                self.node_table[node].previous = self.currentnode
            '''checking if there are nodes in the queue'''
            if len(self.queue) > 0:
                '''setting the current node as the next node in the queue'''
                self.currentnode = self.queue[0]
        '''checking if the end node has been visited'''
        if self.node_table[self.endnode].visited == True:
            return True
        else:
            return False

    def getMaxFlow(self):
        '''a variable that will keep track of the max flow of the network'''
        max_flow = 0
        '''keep looping while there is a path from the source to the sink in the residual network'''
        while self.findPathFromStoT():
            '''a variable that will keep track of the current path's flow; initialising it as infinity (1000000)'''
            path_flow = infinity
            '''a variable that will go through all the nodes in the calculated path; initialising it as the end node'''
            temp_node = self.endnode
            '''keep looping until the start node has been reached (the source)'''
            while temp_node != self.startnode:
                '''storing the maximum path flow of the current path'''
                path_flow = min(path_flow, self.residual_graph[self.node_table[temp_node].previous][temp_node])
                '''setting the temp node as the previous node the temp node'''
                temp_node = self.node_table[temp_node].previous
            '''adding the path flow of the current path to the total max flow of the network'''
            max_flow += path_flow
            '''a variable that will go through all the nodes in the current node'''
            residual_tempnode = self.endnode
            '''keep looping until the start node has been reached'''
            while residual_tempnode != self.startnode:
                '''a variable that will store the previous node of the residual_tempnode'''
                residual_parent = self.node_table[residual_tempnode].previous
                '''taking away the path flow from the value of max flow between the residual_parent and the residual_tempnode'''
                self.residual_graph[residual_parent][residual_tempnode] -= path_flow
                self.residual_graph[residual_tempnode][residual_parent] += path_flow
                '''setting the residual_tempnode as the previous node of the residual_tempnode'''
                residual_tempnode = residual_parent
        return max_flow


if __name__ == '__main__':
    '''Dijkstra's part of the code'''
    Algorithm = Dijkstra()
    Algorithm.populate_network("network.txt")
    Algorithm.parse_route("route.txt")
    Algorithm.populate_node_table()
    print("Network Table:")
    for line in Algorithm.network:
        print(line)
    print(f"Startnode = {chr(Algorithm.startnode + 65)}, Endnode = {chr(Algorithm.endnode + 65)}")
    shortest_path = Algorithm.return_shortest_path()
    print("-:The Shortest Path:-")
    for item in shortest_path[:-1]:
        print(chr(item + 65))
    print("Total Distance: " + str(shortest_path[-1]))

    '''Max Flow part of the code'''
    MaxFlowAlgo = MaxFlow()
    MaxFlowAlgo.populate_network("network.txt")
    MaxFlowAlgo.parse_route("route.txt")
    MaxFlowAlgo.populate_node_table()

    print("The maximum possible flow is: " + str(MaxFlowAlgo.getMaxFlow()))

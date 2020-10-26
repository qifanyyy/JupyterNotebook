
"""Finding shortest paths to drive from home to work on a road network"""

from graph import DirectedRoad, Node, RoadMap


# PROBLEM 2: Building the Road Network
#
# PART 2A: Designing your Graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the times
# represented?
#
# ANSWER: 
        # nodes represent (an abstraction of) intersections of streets/roads
        # edges represent roads
        # travel times indicate how long it takes to go from one intersection (start node) to another (end node)


# PART 2B: Implementing load_map
def load_map(map_filename, is_normal_time):
    """
    Parses the map file and constructs a road map (graph).

    Parameters:
        map_filename : String
            name of the map file
        is_normal_time  : boolean
            When this is true, use normal travel times for map weights.
            Otherwise, use rush hour travel times.

    Assumes:
        Each entry in the map file consists of the following format, separated by spaces:
            From To TotalTime_normal TotalTime_rushhour RoadType
        e.g.
            N0 N1 10 15 interstate
        This entry would become an edge from 'N0' to 'N1' on an interstate highway with 
        a weight of either 10 or 15, depending on what is specified by time_column. 
        There should also be another edge from 'N1' to 'N0' on an interstate using the 
        same weight.

    Returns:
        a directed road map representing the inputted map
    """
    
#   nodes are instances of Node class
#   edges are instances of DirectedRoad class
#   travel times are attributes of the DirectedRoad class instances

    # Open file
    file = open(map_filename)
    
    # Read first line (no need to keep the data)
    header_line = file.readline()
    
    # Create and instacnec of RoadMap
    road_map = RoadMap()
    
    # Read lines as long as file and line are not empty
    while header_line != "" and header_line != "\n":
        
        # Split the line on space
        header_line = header_line.split()
        
        # Instantiate Node objects
        node1 = Node(header_line[0])
        if not road_map.has_node(node1):    
            road_map.add_node(node1)
        node2 = Node(header_line[1])
        if not road_map.has_node(node2):
            road_map.add_node(node2)
        
        # Get times and road type
        TotalTime_normal = header_line[2]
        TotalTime_rushhour = header_line[3]
        road_type = header_line[4]
        
        # Check if normal time or rush hour
        # Create instances of DirectedRoad

        if is_normal_time:
            directed_road1 = DirectedRoad(node1, node2, TotalTime_normal, road_type)
        else:
            directed_road1 = DirectedRoad(node1, node2, TotalTime_rushhour, road_type)

        # Since all roads can be traversed in both directions...
        if is_normal_time:
            directed_road2 = DirectedRoad(node2, node1, TotalTime_normal, road_type)
        else:
            directed_road2 = DirectedRoad(node2, node1, TotalTime_rushhour, road_type)
        
        # Add DirectedRoad(s) to RoadMap instance
        road_map.add_road(directed_road1)
        road_map.add_road(directed_road2)

        # Read next line
        header_line = file.readline()
    
    return road_map


# PART 2C: Testing load_map
# Include the lines used to test load_map below, but comment them out
    
#### TEST 2C.1: Rush Hour ##### 
#print(load_map("test_load_map.txt", False))

#### TEST 2C.2: Normal Traffic ##### 
#print(load_map("test_load_map.txt", True))


# PROBLEM 3: Finding the Shortest Path using Optimized Search Method
#
# PART 3A: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# ANSWER:
        # Objective Function: minimize (travel) time
        # Constraint: get from start to end without going through restricted roads

# PART 3B: Implement get_best_path
def get_best_path(roadmap, start, end, restricted_roads):
    """
    Finds the shortest path between nodes subject to constraints.

    Parameters:
        roadmap: RoadMap
            The graph on which to carry out the search
        start: Node
            node at which to start
        end: Node
            node at which to end
        restricted_roads: list[strings]
            Road Types not allowed on path

    Returns:
        A tuple of the form (best_path, best_time).
        The first item is the shortest-path from start to end, represented by
        a list of Node objects.
        The second item is an integer, the total travel time of the best path.

        Return None if there doesn't exist a valid path
        or either start or end nodes are not in roadmap.

        See pseudocode in problem set instructions for hints.
    """
    
    # Objective Function: minimize (travel) time
    # Constraint: start and end nodes (have to get from the start to destination)

    
    # Check if start and end are valid Node instances
    if not (isinstance(start, Node) and isinstance(end, Node)):
        return None
    
    # Check if start and end are the same node (empty path with 0 travel time)
    if start == end:
        return ([], 0)
    
    # Store all nodes and mark them as unvisited
    unvisited = list(roadmap.get_all_nodes())
    
    # An empty list to store visited nodes (to avoid cycles)
    visited = []
    
    # Set the initial distance for all nodes to infinity 
    timeTo = {node: float("inf") for node in roadmap.get_all_nodes()}
    
    # Set the distance from start to zero
    timeTo[start] = 0
    
    # Mark all nodes as not having a predecessor node 
    predecessor = {node: None for node in roadmap.get_all_nodes()}
    
    # As long as end hasn't been reached
    while end in unvisited:
        
        # Select the unvisited node with the smallest distance from start
        current = min(unvisited, key = lambda node: timeTo[node])
        
        # If no path exists between start and end, break (smallest time in all unvisited nodes is infinity)
        if timeTo[current] == float("inf"):
            break
        
        # Explore roads
        for road in roadmap.get_roads_for_node(current):
            
            # Avoid restricted roads
            if road.get_type() in restricted_roads:
                continue
            
            # Get the neighbor Node
            neighbor = road.get_destination()
            
            # If node hasn't been visited yet, find its distance from start
            if neighbor not in visited: 
                alternativePathTime = timeTo[current] + road.get_total_time()      
                
                # Compare the newly calculated distance to the assigned
                if alternativePathTime < timeTo[neighbor]:
                    
                    # Save the smaller distance and update predecssor
                    timeTo[neighbor] = alternativePathTime
                    predecessor[neighbor] = current
                    
        # Update visited list with the current node          
        visited.append(current) 
                
        # Remove the current node from the unvisited list
        unvisited.remove(current)
        
    # Making the path... (backtracking end to start)  
    best_path = []
    current = end
    if current not in predecessor:
        predecessor[current] = None
        
    while type(predecessor[current]) != type(None):
        best_path.insert(0, current)
        current = predecessor[current]
    if best_path != []:
        best_path.insert(0, current)
    else:
        return None
    
    return (best_path, timeTo[end])

# PART 4A: Implement best_path_ideal_traffic
def best_path_ideal_traffic(filename, start, end):
    """Finds the shortest path from start to end during ideal traffic conditions.

    You must use get_best_path and load_map.

    Parameters:
        filename: name of the map file that contains the graph on which
            carry out the search
        start: Node
            node at which to start
        end: Node
            node at which to end
    Returns:
        The shortest path from start to end in normal traffic,
            represented by a list of nodes (Nodes).

        If there exists no path, then return None.
    """
    
    # Load map with normal time
    roadmap = load_map(filename, True)
    
    # No restricted roads
    restricted_roads = [] 
    
    if get_best_path(roadmap, start, end, restricted_roads) == None:
        return None
    else: 
        best_path, timeToEnd = get_best_path(roadmap, start, end, restricted_roads)
    
    return best_path


# PART 4B: Implement best_path_rush_hour
def best_path_rush_hour(filename, start, end):
    """Finds the shortest path from start to end during rush hour traffic.

    You must use get_best_path and load_map.

    Parameters:
        filename: name of the map file that contains the graph on which
            carry out the search
        start: Node
            node at which to start
        end: Node
            node at which to end
    Returns:
        The shortest path from start to end during rush hour traffic,
            represented by a list of nodes (Nodes).

        If there exists no path, then return None.
    """
    
    # Load map with rush hour time
    roadmap = load_map(filename, False)
    
    # No restricted roads
    restricted_roads = [] 

    if get_best_path(roadmap, start, end, restricted_roads) == None:
        return None
    else: 
        best_path, timeToEnd = get_best_path(roadmap, start, end, restricted_roads)
    
    return best_path


# PART 4C: Implement best_path_restricted
def best_path_restricted(filename, start, end):
    """Finds the shortest path from start to end during rush hour traffic
    when local roads cannot be used.

    You must use get_best_path and load_map.

    Parameters:
        filename: name of the map file that contains the graph on which
            carry out the search
        start: Node
            node at which to start
        end: Node
            node at which to end
    Returns:
        The shortest path from start to end given the aforementioned conditions,
            represented by a list of nodes (Nodes).

        If there exists no path that satisfies restricted_roads constraints, then return None.
    """
    
    # Load map with rush hour time
    roadmap = load_map(filename, False)

    # Local roads are restricted 
    restricted_roads = ["local"] 
    
    if get_best_path(roadmap, start, end, restricted_roads) == None:
        return None
    else: 
        best_path, timeToEnd = get_best_path(roadmap, start, end, restricted_roads)
    
    return best_path

"""UNCOMMENT THE FOLLOWING LINES/WRITE YOUR OWN CODE BELOW IF YOU WOULD LIKE TO DEBUG"""

#### TEST 0.1 ####
rmap = load_map('road_map.txt', True)
start = Node('N0')
end = Node('N9')
restricted_roads = []
print(get_best_path(rmap, start, end, restricted_roads))

### TEST 0.2 ####
print(best_path_ideal_traffic("road_map.txt", start, end))
print(best_path_rush_hour("road_map.txt", start, end))
print(best_path_restricted("road_map.txt", start, end))



#start = Node('R0')
#end = Node('R4')
##### TEST 1: best_path_ideal_traffic ####
#print(best_path_ideal_traffic("test_load_map.txt", start, end))
#
##### TEST 2: best_path_rush_hour ####
#print(best_path_rush_hour("test_load_map.txt", start, end))
#
##### TEST 3: best_path_restricted ####
#print(best_path_restricted("test_load_map.txt", start, end))










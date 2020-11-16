import math
from queue import PriorityQueue

def shortest_path(M,start,goal):
    """
    Calculates the shortest path between start and goal in a given map using a* algorithm with euclidean distance heuristics
    
    Args:
       M: Map(Map object)
       start(int): the start node id
       goal(int): the goal node id
       
    Returns:
        path(array): An array of integers representing the shortest sequence of intersection visits from start to goal in a given map
    """
        
    print("shortest path called")
    
    frontier = PriorityQueue()
    frontier.put((0, start))
    
    came_from = {}
    total_cost = {}
    
    # initialize start
    came_from[start] = None
    total_cost[start] = 0
    
    
    while not frontier.empty():
        current_node = (frontier.get())[1]
        
        # when we find the goal, end the cycle
        if current_node == goal:
            break
            
        # use a* algorithm with euclidean distance heuristics to find the goal
        neighboard_nodes = M.roads[current_node]
        for next_node in neighboard_nodes:
            new_cost = total_cost[current_node] + calculate_g_value(M, current_node, next_node)
            if next_node not in total_cost or new_cost < total_cost[next_node]:
                total_cost[next_node] = new_cost
                priority = new_cost + calculate_h_value(M, current_node, next_node)
                frontier.put((priority, next_node))
                came_from[next_node] = current_node 
     
    return reconstruct_path(came_from, start, goal)

def reconstruct_path(came_from, start, goal):
    """
    Return the shortest path travelled by a* algorithm
    
    Args:
       came_from(dictionary): Linked-list of previously visited place
       start(int): the start node id
       goal(int): the goal node id
       
    Returns:
       path(array): An array of integers representing the shortest sequence of intersection visits from start to goal in a given map

    """
    
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start) 
    path.reverse() 
    return path

def calculate_h_value(M, node, goal):
    """
    Calculate euclidean distance between node and goal
    
    The heuristics is admissible as straight line is always the smallest possible distance between two points,
    so a star will always finds a shortest path 

    Time Complexity O(1)
    Space Complexity O(1)
    
    Args:
       M: Map(Map object)
       node(int): the start node id
       goal(int): the goal node id
       
    Returns:
        distance(float): Distance between the two points
    """
    return calculate_distance(M.intersections[goal], M.intersections[node])

def calculate_g_value(M, current_node, target_node):
    """
    Calculate path cost (distance) between current_node and target node
    
    Time Complexity O(1)
    Space Complexity O(1)
    
    Args:
       M(Map object): Map in which are both nodes located
       current_node(array): [0] = x coordinates and [1] = y coordinates
       target_node(array): [0] = x coordinates and [1] = y coordinates
       
    Returns:
        distance(float): Distance between the two points
    """
    
    return calculate_distance(M.intersections[current_node], M.intersections[target_node])
    

def calculate_distance(point1, point2):
    """
    Calculate euclidean distance between two points

    Time Complexity O(1)
    Space Complexity O(1)
    
    Args:
       node1(array): [0] = x coordinates and [1] = y coordinates
       node2(array): [0] = x coordinates and [1] = y coordinates
       
    Returns:
        distance(float): Distance between the two points
    """
    
    x1, y1 = point1[0], point1[1]
    x2, y2 = point2[0], point2[1]
    
    #distance = math.sqrt(((x1-x2)**2) + (y1-y2)**2) 
    distance = abs(x1 - x2) + abs(y1 - y2) # working for our heuristic perfectly, faster than calculating square root above
    
    return distance
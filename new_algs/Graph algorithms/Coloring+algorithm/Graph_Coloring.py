"""
    schedule optimization
"""
################################################################################
# part 1: construct the graph
################################################################################
import random

# function generate fack students
# 9 courses that are likely to be taken by first year cs students
REQUIRED_COURSES = ["cs125", "cs173", "math231", "math241", "math415", "rhet105", "chem102","chem103", "phys212"]
# 14 courses that are less likely to be taken by first year cs students
ELECTIVE_COURSES = ["cs225", "cs196", "psyc100", "art100", "econ102", "econ103", "danc100", "hist100", "phil103", "stat100", "soc100", "aas100", "aas283", "anth100"] 

def generate_fake_students(number_of_students, courses_a, courses_b):
    '''
        the function takes in the number of students need to be generated,
        a list of courses that have higher possibilities to be taken by students
        and a list of courses that have lower possiblilities to be taken by studnets.
        By randomly selecting three courses from first list, and two from second, it returns a list of courses taken by an individual (which also represent as lists).
    '''
    result = []
    for i in range(number_of_students):
        random.shuffle(courses_a)
        random.shuffle(courses_b)
        random_courses_a = courses_a[:3]
        random_courses_b = courses_b[:2]
        random_courses_a.extend(random_courses_b)
        random_courses = random_courses_a
        result.append(random_courses)
    return result            

fake_students = generate_fake_students(20, REQUIRED_COURSES, ELECTIVE_COURSES)

## print out students
for index in range(len(fake_students)):
    print "student ", index, " ", fake_students[index]

TIME_LIST = ["8", "9", "10", "11", "12", "13", "14", "15", "16"]

# make_complete_graph(num_nodes), which make a complete graph of time nodes
def make_complete_graph(a_list):
    """
    Takes the number of nodes num_nodes and returns a dictionary corresponding to
    a complete directed graph with the specified number of nodes.
    """
    connection_dic = {}
    for dummy_i in a_list:
        connection_dic[dummy_i] = a_list
    graph_name = {}
    for dummy_i in a_list:
        graph_name[dummy_i] = set()
    for dummy_i in a_list:
        for dummy_in_node in connection_dic[dummy_i]:
            if dummy_in_node != dummy_i:
                graph_name[dummy_i].add(dummy_in_node)
    return graph_name   
time_graph = make_complete_graph(TIME_LIST)
#print time_graph

# add the courses nodes to the time nodes
graph_schdule = make_complete_graph(TIME_LIST)

def whole_graph_for_color(students, graph_schdule):
    for student in students:
        for course in student:
            if course not in graph_schdule.keys():
                graph_schdule[course] = set();
            ## make a copy of student
            for other_course in student:
                if other_course != course:
                    graph_schdule[course].add(other_course)
    return graph_schdule
##print whole_graph_for_color(students, graph_schdule)

## if students have special requirements for the time of class
## the time NOT SUITABLE for a course will connect to the course
## with an edge. When process a large amount of data, only 
## requirements larger than some number will be translate into an edge
def time_restriction(graph, time, course):
    '''
        adding an edge between the time and course
    '''
    graph[time].add(course)
    graph[course].add(time)
#test_graph = whole_graph_for_color(students, graph_schdule)   
#time_restriction(test_graph, "cs125", "8")
#print test_graph
    

###########################################################################
# part 2: color the graph (use BFS search)
###########################################################################
import random
## color starts from 1

def find_maxdegree_node (graph):
    '''
        helper function for coloring
        return the node with biggest degree in graph
    '''
    key_list = graph.keys()
    max_degree = graph[key_list[0]]
    max_degree_node = key_list[0]
    for key in key_list:
        if graph[key] > max_degree:
            max_degree = graph[key]
            max_degree_node = key
    return max_degree_node

##print find_maxdegree_node(whole_graph_for_color(students, {}))

def non_neighbors_set (graph, target_node):
    '''
        helper function for coloring
        return a set of non neighbors nodes
    '''
    all_nodes = graph.keys()
    all_nodes_set = set()
    for node in all_nodes:
        all_nodes_set.add(node)
    non_neighbors = all_nodes_set.difference(graph[target_node])
    non_neighbors.remove(target_node)
    return non_neighbors

##print non_neighbors_set (whole_graph_for_color(students, {0: set([1,2])}), "cs125")

def common_neighbor_set (graph, node_a, node_b):
    '''
        helper function for coloring
        return a set of nodes that are neighbors of given nodes
    '''
    neighbor_nodes_set = set()
    neighbor_nodes_of_a = graph[node_a]
    neighbor_nodes_of_b = graph[node_b]
    neighbor_nodes_set = neighbor_nodes_of_a.intersection(neighbor_nodes_of_b)
    return neighbor_nodes_set
##print common_neighbor_set (whole_graph_for_color(students,{0: set([1,2])}), "cs125", "cs173")

def get_neighbor(graph, target_node):
    '''
        function that returns a set of nodes
    '''
    return graph[target_node]

def get_start_node(graph):
    '''
        randomly select a node from graph as start node
    '''
    nodes = graph.keys()
    return random.choice(nodes)

def is_neighbor(graph, node_a, node_b):
    '''
        check whether two nodes are neighbors
    '''
    return node_b in graph[node_a]

def is_neighbor_with_colored(graph, target_node, colored_nodes):
    '''
        check whether a node (target_node) is neighbor with nodes of a certain kind of color
    '''
    for colored_node in colored_nodes:
        if is_neighbor(graph, colored_node, target_node):
            return True
    return False

def get_colored_graph(colored_graph):
    '''
        convert colored_graph from dictionary to list
    '''
    colored_graph_list = []
    for color in colored_graph:
        colored_graph_list.extend(colored_graph[color])  
    return colored_graph_list
    
def BFS_color(graph):
    '''
        graph is a dictionary
        colored_graph is a dictionary with key as colors
    '''
    colored_graph = {}
    color = 1
    colored_graph[color] = []
    ## a list of node that currently need to be explored
    start_node = get_start_node(graph)
    ## print "start node: ", start_node
    colored_graph[color].append(start_node)
    frontier = [start_node]
    ## explore the graph
    while len(frontier) != 0:
        neighbors = list(get_neighbor(graph, frontier[0]))

        #check if the neighbors is already colored. if colored, remove them
        neighbors_clone = neighbors + []
        for neighbor_node in neighbors_clone:
            if (neighbor_node in get_colored_graph(colored_graph)):
                neighbors.remove(neighbor_node)

        ## go through the new neighbor nodes to color them
        for target_node in neighbors:
            used_colors = range(1, color + 1)
            random.shuffle(used_colors)
            for used_color in used_colors:
                ## first check if the node can be colored with existing colors 
                colored_nodes = colored_graph[used_color]
                if not is_neighbor_with_colored(graph, target_node, colored_nodes):
                    colored_graph[used_color].append(target_node)
                    break
            ## cannot colored by existing colors
            if (target_node not in get_colored_graph(colored_graph)):	
                color += 1
                colored_graph[color] = []
                colored_graph[color].append(target_node)
                              
        ## removed the expanded node and put the new neighbors into frontier
        frontier.pop(0)
        frontier.extend(neighbors)
    return colored_graph

    
###########################
# Test Cases for BFS_color
###########################
### case 1: generate best result with minium colors when started with cs125    
#print "test case1: "
#test_graph1 = {"cs125":set(["cs173", "cs196"]),"cs173":set(["cs125"]), "cs196":set(["cs125"])}
#print test_graph1
#print BFS_color(test_graph1)
#print "------------------------------------------------------"
#### case 2: three cycle
#print "test case2:"
#test_graph2 = {"cs125":set(["cs173", "cs196"]),"cs173":set(["cs125","cs196"]), "cs196":set(["cs125","cs173"])}
#print test_graph2
#print BFS_color(test_graph2)    
#print "------------------------------------------------------"
## case 3: generate best result with minium colors when started with cs125
#print "test case3:"
#test_graph3 = {"cs125":set(["cs173", "cs196", "cs225"]),"cs173":set(["cs125","cs196"]), "cs196":set(["cs125","cs173"]), "cs225":set(["cs125"])}
#print test_graph3
#print BFS_color(test_graph3)
#print "------------------------------------------------------"
### case 4 
#print "test case4: "
#test_graph = whole_graph_for_color(fake_students, graph_schdule)   
##time_restriction(test_graph, fake_students[0][0], "8")
##time_restriction(test_graph, fake_students[0][1], "9")
###time_restriction(test_graph, "cs173", "8")
###time_restriction(test_graph, "cs225", "8")
#print test_graph
#print BFS_color(test_graph)
#print "------------------------------------------------------"
### case 5 pure graph coloring problem
#print "test case5: "
#test_graph5 = {"a":set(["d","h","e","b"]), "b":set(["a","e","f","c"]), "c":set(["b","f","g","d"]),"d":set(["a","h","g","c"]),"e":set(["h","a","b","f"]),"f":set(["b","c","e","g"]),"g":set(["d","c","h","f"]),"h":set(["a","d","g","e"])}
#print test_graph5
#print BFS_color(test_graph5)

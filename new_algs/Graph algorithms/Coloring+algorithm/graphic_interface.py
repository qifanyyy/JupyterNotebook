#################################################################################
# part 3: Graph interface
#
# An interface for graph(represent by dictionary and set) in general
# available here: http://www.codeskulptor.org/#user38_dzGl0Mb0mt_11.py
#
#################################################################################
import simplegui
import math

# size of the canvas
WIDTH = 800
HEIGHT = 600
# Flags
COLORED = False
DRAGED = False
RANDOM_COLOR = True

# Handler for mouse click on button
def click():
    global COLORED, RANDOM_COLOR
    global color_convert
    COLORED = True
    color_convert = {}
    RANDOM_COLOR = True

def add_time_restriction(text_input):
    global graph
    restriction = text_input.split()
    if len(restriction) < 2:
        input_status.set_text('Course or time not found')
    else:
        time = restriction[0]
        course = restriction[1]
        ## prevent bad input
        if (time in graph.keys()) and (course in graph.keys()): 
            time_restriction(graph, time, course)
            input_status.set_text("")
        else:
            input_status.set_text('Course or time not found')

# Handler for mouse drag on canvas    
def mouse_handler(position):
    global pos_dictionary, DRAGED
    ## print "draged"
    for node in pos_dictionary:
        pos = pos_dictionary[node]
        if ((pos[0] - position[0])** 2 + (pos[1] - position[1])**2) < 20**2: # 20 is the size of the node
            pos_dictionary[node] = position
            DRAGED = True
            break
    
## test cases
test_graph = whole_graph_for_color(fake_students, graph_schdule)
test_graph3 = {"cs125":set(["cs173", "cs196", "cs225"]),"cs173":set(["cs125","cs196"]), "cs196":set(["cs125","cs173"]), "cs225":set(["cs125"])}
test_graph5 = {"a":set(["d","h","e","b"]), "b":set(["a","e","f","c"]), "c":set(["b","f","g","d"]),"d":set(["a","h","g","c"]),"e":set(["h","a","b","f"]),"f":set(["b","c","e","g"]),"g":set(["d","c","h","f"]),"h":set(["a","d","g","e"])}

# Handler to draw on canvas
def draw(canvas):
    global graph
    #graph = test_graph3
    graph = test_graph
    #graph = test_graph5
    
    if COLORED:
        # print "colored"
        plot_colored_graph(graph, canvas)
    else:
        plot_graph(graph, canvas)        
        
def plot_graph(graph, canvas):
    global pos_dictionary, DRAGED
    center_x = WIDTH / 2
    center_y = HEIGHT / 2
    radius = HEIGHT / 2.5
    length = len(graph.keys())
    angle = 0 # in radius
    delta_angle = 2 * math.pi / length
    node_size = 20
    text_color = "#000000"
    
    if not DRAGED:
        pos_dictionary = {}
        for node in graph.keys():
            pos_x = center_x + math.sin(angle) * radius
            pos_y = center_y - math.cos(angle) * radius
            # print pos_x, pos_y
            pos_dictionary[node] = (pos_x, pos_y)
            canvas.draw_circle([pos_x, pos_y], node_size, 2, 'Black', 'White')
            canvas.draw_text(node, [pos_x - 12, pos_y + 6], 20, text_color)
            angle = angle + delta_angle
    ##print pos_dictionary
    for node in graph.keys():
        for neighbor in (list)(graph[node]):
            canvas.draw_line(pos_dictionary[node], pos_dictionary[neighbor], 2, 'Black')
    ## redraw the node to put them at the top
    for node in graph.keys():
        pos_x = pos_dictionary[node][0]
        pos_y = pos_dictionary[node][1]
        canvas.draw_circle([pos_x, pos_y], node_size, 2, 'Black', 'White')
        canvas.draw_text(node, [pos_x - 12, pos_y + 6], 20, text_color)        

    
def plot_colored_graph(graph, canvas):
    global color_convert, RANDOM_COLOR, COLORED, pos_dictionary, DRAGED
    if RANDOM_COLOR: # if haven't assign any color yet, assign them
        colored_graph = BFS_color(graph)
        for key in colored_graph.keys():
            ### generate some random random color
            r = lambda: random.randint(127,255)
            color = '#%02X%02X%02X' % (r(),r(),r())
            for node in colored_graph[key]:
                color_convert[node] = color
        ## print colored graph out
        print "------------------------------------------------------"
        for color in colored_graph.keys():
            # make a copy
            same_color_nodes = colored_graph[color] + []
            same_color_nodes.sort()
            print same_color_nodes
    RANDOM_COLOR = False
    center_x = WIDTH / 2
    center_y = HEIGHT / 2
    radius = HEIGHT / 2.5
    length = len(graph.keys())
    angle = 0 # in radius
    delta_angle = 2 * math.pi / length
    node_size = 20
    text_color = "#000000"
    
    if not DRAGED:
        pos_dictionary = {}
        for node in graph.keys():
            pos_x = center_x + math.sin(angle) * radius
            pos_y = center_y - math.cos(angle) * radius
            # print pos_x, pos_y
            pos_dictionary[node] = (pos_x, pos_y)
            canvas.draw_circle([pos_x, pos_y], node_size, 2, 'Black', 'White')
            canvas.draw_text(node, [pos_x - 12, pos_y + 6], 20, text_color)
            angle = angle + delta_angle
    for node in graph.keys():
        for neighbor in (list)(graph[node]):
            canvas.draw_line(pos_dictionary[node], pos_dictionary[neighbor], 2, 'Black')
    ## redraw the node to put them at the top
    for node in graph.keys():
        pos_x = pos_dictionary[node][0]
        pos_y = pos_dictionary[node][1]
        if (len(color_convert.keys()) == len(graph.keys())):
            node_color = color_convert[node]
            canvas.draw_circle([pos_x, pos_y], node_size, 2, 'Black', node_color)
            canvas.draw_text(node, [pos_x - 12, pos_y + 6], 20, text_color)
        else:
            COLORED = False
            input_status.set_text("This is not a CONNECTED graph!")
    
# Create a frame and assign callbacks to event handlers

frame = simplegui.create_frame("Home", WIDTH, HEIGHT)
frame.add_button("Color", click)
frame.add_input('Add time restriction. Example: cs125 8 (Press Enter)', add_time_restriction, 80)
input_status = frame.add_label('')
frame.set_draw_handler(draw)
frame.set_canvas_background('White')
frame.set_mousedrag_handler(mouse_handler)

# Start the frame animation
frame.start()

"""
This is the main code for shortest path visualiser of Dijkstra's Algorithm
Algorithm works by constantly adding the nearest node, and updating the neighboring nodes.
Thus obtaining shortest path to all nodes

Take note that the distance between each node is 1 unit, although the width and height is different.
If this bothers you, edit the window size to a square one

When using this code:
1) The first thing that pops out is a code asking for input of start node, end node and size of array
2) Then a set of instuctions window appears.
3) Next, the main window appears with initialised start node and end node (in blue)
4) User can draw and erase walls. Left click to draw, right click to erase.
5) When Enter is pressed on the keyboard, Dijkstra's Algorithm will start running
6) Red indicates the absorbed nodes, and green indicates the frontier, black are walls, blue is the start/end nodes
7) At the end, shortest path will be in blue.
8) Rerun the code to try again
"""
#Import pygame for visualisation, and algorithms from Algorithm.py
import pygame
import tkinter as tk
from tkinter import messagebox as mb
from Structures import min_heap


def check_surroundings(arr, absorbed_nodes, current_node, size):
    """
    Function, given a node, will determine the neighbouring nodes.
    Inputs:  arr: given grid structure
             absorbed_ nodes: Nodes that are used in the algo. list of tuples (x,y)
             current_node: Node whose neighbours are to be determined. Tuple (x,y)
             size: size of arr
    Returns: List of available neighbouring nodes 
    """
    x, y = current_node
    surrounding_nodes = []

    if(x>0 and arr[x-1][y] != None and (x-1,y) not in absorbed_nodes):        #Left Node
        surrounding_nodes.append((x-1,y))

    if(y<size-1 and arr[x][y+1] != None and (x,y+1) not in absorbed_nodes):   #Top Node
        surrounding_nodes.append((x, y+1))

    if(x<size-1 and arr[x+1][y] != None and (x+1,y) not in absorbed_nodes):   #Right Node
        surrounding_nodes.append((x+1, y))

    if(y>0 and arr[x][y-1] != None and (x,y-1) not in absorbed_nodes):        #Bottom Node
        surrounding_nodes.append((x, y-1))

    return surrounding_nodes


def backtrack(arr, start_node, end_node, size):
    """
    Function that finds the shortest path after applying Dijkstra's algorithm
    Inputs: arr: main array (2D square array)
            start_node: start point (x,y)
            end_node: end point (x,y)
            size: size of 2D square array (int)
    Returns: list of nodes that belong in the route of shortest path
    """
    shortest_path = [end_node]
    shortest_dist = arr[end_node[0]][end_node[1]]
    current_node = end_node
    for i in reversed(range(shortest_dist)):
        surrounding_nodes = check_surroundings(arr,[], current_node, size)
        for node in surrounding_nodes:
            x,y = node
            if arr[x][y] == i:
                shortest_path.append(node)
                current_node = node
                break
    return shortest_path


def draw_grid(win , top_left, bottom_right, arr_size):
    """
    Function that draws the grid on the window for initialisation.
    Function also maps array indexes into coordinates of grid
    Inputs: win: window
            top_left: top left corner of grid
            bottom_right: bottom right corner of grid
            arr_size: size of 2d square array
    Returns: Python dictionary mapping arr coordinates to coordinates on grid
             (width, height) of squares
    """
    coordinates = {}
    arr_x, arr_y = (0, 0)
    win.fill((211,211,211)) #Make the entire screen grey-ish

    sq_height = (bottom_right[1] - top_left[1])//arr_size
    sq_width = (bottom_right[0] - top_left[0])//arr_size

    for i in range(arr_size):
        for j in range(arr_size):
            x = j * sq_width + top_left[0]
            y = i * sq_height + top_left[1]
            pygame.draw.rect(win, (255,255,255), (x, y, sq_width, sq_height))   #Draw white squares
            pygame.draw.rect(win, (0,0,0), (x, y, sq_width, sq_height), 1)   #Draw black borders
            coordinates[str((arr_x, arr_y))] = (x,y)
            arr_x += 1
        arr_y += 1
        arr_x = 0

    return coordinates, (sq_width, sq_height)


def fill_rect(win, arr_pos, coordinates, sq_dimensions, color):
    """
    Function that fills up a square with a color in the grid, coressponding to arr position
    Inputs: arr_pos: (x,y) representing x and y indexes of 2d square array
            coordinates: python dictionary mapping arr pos to grid position
            sq_dimensions: (width, height) of squares
            color: (int, int, int) color to fill
    Returns: Nothing
    """
    color_dict = {"maroon": (128,0,0), "navyblue": (0,0,128), "green":(0,255,0), "black":(0,0,0), "white":(255,255,255)}
    x, y = coordinates[str(arr_pos)]
    sq_width, sq_height = sq_dimensions

    pygame.draw.rect(win, color_dict[color], (x+1, y+1, sq_width-2, sq_height-2))


def get_index(pos, top_left, sq_dimensions, size):
    """
    Function that gets the array indexes corresponding to cursor position
    Inputs: pos: position of mouse cursor (x,y)
            top_left: starting grid coordinates
            sq_dimensions: dimensions of each block (width, height)
            size: size of 2D array
    Returns: (x,y) indexes of 2D array
    """
    sq_width, sq_height = sq_dimensions
    pos_x, pos_y = pos
    x, y = top_left

    for i in range(size):
        x += sq_width
        if x > pos_x:
            break
    for j in range(size):
        y += sq_height
        if y > pos_y:
            break

    return (i,j)


def get_tuple(tuple_str):
    """
    Function that changes a string of a tuple into the tuple itself
    Inputs: tuple_str: the string that needs to be converted "(x,y)"
    Returns: The tuple (x,y)
    """
    tuple_list = tuple_str.split(',')
    num_list = []
    for item in tuple_list:
        temp_list = []
        for ch in item:
            if ch.isdigit():
                temp_list.append(ch)
        num = int(''.join(temp_list))
        temp_list = []
        num_list.append(num)
    return (num_list[0], num_list[1])


def initialise_prog():
    """
    Function to initialise text box for user input
    """
    def onsubmit():
        """
        Function works with initialise_prog
        global variables start, end, arr_size is used throughout the programme.
        These variables are the user inputs.
        """
        global start
        global end
        global arr_size
        start = start_box.get()
        end = end_box.get()
        arr_size = size_box.get()
        master.quit()
        master.destroy()

    master = tk.Tk()
    master.title("Initialisation")

    first_label = tk.Label(master, text = "Array Size: ")
    second_label = tk.Label(master, text = "Start Node (x,y): ")
    third_label = tk.Label(master, text = "End Node (x,y): ")

    size_box = tk.Entry(master)
    start_box = tk.Entry(master)
    end_box = tk.Entry(master)

    submit = tk.Button(master, text = "Submit", command=onsubmit)

    first_label.grid(row=0, column=0)
    second_label.grid(row=1, column=0)
    third_label.grid(row=2, column=0)
    size_box.grid(row=0, column=1)
    start_box.grid(row=1, column=1)
    end_box.grid(row=2, column=1)
    submit.grid(row=4, column=1)

    master.mainloop()


def instructions():
    message = "Left Click to add wall\nRight Clcik to remove wall\nEnter to start algorithm"
    root = tk.Tk()
    root.title("Instrutions")
    T = tk.Text(root, height=3, width=50)
    T.pack()
    T.insert(tk.END, message)
    tk.mainloop()


# MAIN PROGRAMME

initialise_prog()                               #Initialize programme to get user input
instructions()                                  #Give instructions on how to use
pygame.init()                                   #Initialize pygame
win_size = (1200,600)                           #Initialize window size, can be set to anything 
win = pygame.display.set_mode(win_size)         #Initialize window

win_size_x, win_size_y = win_size
pygame.display.set_caption("Dijkstra's Algorthim Visualiser")

#Set user inputs to appropriate variables
arr_size = int(arr_size)
start_node = get_tuple(start)
end_node = get_tuple(end)

#Initialize 2D array and display grid
arr = [[float("inf") for i in range(arr_size)] for j in range(arr_size)]    #initialize array
coordinates, sq_dimensions = draw_grid(win, (25,25), (win_size_x -25, win_size_y -25), arr_size)    #Initialize grid
fill_rect(win, start_node, coordinates, sq_dimensions, "navyblue")  #Initialize start node
fill_rect(win, end_node, coordinates, sq_dimensions, "navyblue")    #Initialize end node
pygame.display.update()

#FIRST LOOP 
#Objective: Allow user to add walls into algorithm. left click to add, right click to remove
run = True
while run:
    pygame.time.delay(10)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       #Base condition to close game
            run = False
            pygame.quit()
    
    #If left click is pressed, fill up with walls
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        arr_x, arr_y = get_index(pos, (25,25), sq_dimensions, arr_size)         #Get index of cursor position
        if (arr_x, arr_y) != start_node and (arr_x, arr_y) != end_node:
            arr[arr_x][arr_y] = None                                            #Set array value to None to indicate wall
            fill_rect(win, (arr_x, arr_y), coordinates, sq_dimensions, "black") #Fill position in grid with wall

    #If right click is pressed, unfill the walls
    if pygame.mouse.get_pressed()[2]:
        pos = pygame.mouse.get_pos()
        arr_x, arr_y = get_index(pos, (25,25), sq_dimensions, arr_size)         #Get index of cursor position
        if (arr_x, arr_y) != start_node and (arr_x, arr_y) != end_node:
            arr[arr_x][arr_y] = float("inf")                                    #Reset array value
            fill_rect(win, (arr_x, arr_y), coordinates, sq_dimensions, "white") #Make position in grid white again

    pygame.display.update()

    #If user clicks enter, we break out of this loop, and begin algorithm
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        run = False
"""
Once the display window has been set up by the user, we commence to visualise Dijkstra's Algorithm
For this part, it is the same as the algorithm in Algorithm.py, but modified slightly to accomodate visualisation

What we need for the algo to work: start_node, end_node, absorbed_nodes, min_heap, arr
"""
start_x, start_y = start_node

arr[start_x][start_y] = 0                   #Initialise start node in array
current_node = (start_x, start_y)           #Initialise current_node (x,y) as start_node
absorbed_nodes = [current_node]             #Initialise absorbed nodes [(x,y)] with start_node inside
heap = min_heap([])                         #Initialise heap structure to easily get minimum

#SECOND LOOP
algo_run = True
while algo_run:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:       #Base condition to close game
            algo_run = False
            pygame.quit()

    #Main Dijkstra's Algorithm 
    if(current_node != end_node):
        current_x, current_y = current_node         #x,y coordinates of current node
        current_value = arr[current_x][current_y]   #Value of current node

        #Obtain list of nodes that are surrounding current nodes
        surrounding_nodes = check_surroundings(arr, absorbed_nodes, current_node, arr_size)

        #For each surrounding node, check if it is in heap and check if it needs updating
        for node in surrounding_nodes:
            x, y = node             #x,y coordinates of surrounding_nodes

            #Node has not been added to heap before, so we add it in, and we update in arr/grid
            if arr[x][y] == float("inf"):
                arr[x][y] = current_value + 1                               #Updates arr
                node_with_value = (x, y, arr[x][y])
                heap.heap_insert(node_with_value)                           #Updates heap
                fill_rect(win, node, coordinates, sq_dimensions, "green")   #Updates grid

            #Value of node <= value of current_node + 1, then we leave it alone
            elif arr[x][y] <= current_value + 1:
                pass

            #Value of node > value of current_node + 1, then we want to update node value in heap
            else:
                node_with_value = (x, y, arr[x][y])
                heap_index = heap.find_index(node_with_value)
                #Update the heap_index with appropriate value
                heap.update_heap(heap_index, current_value + 1)
        
        #After updating the new frontier, we get the smallest node again
        min_node = heap.extract_min()

        #If the heap no longer has nodes, it means that there is no shortest path, it is blocked by walls
        if min_node == -1:
            algo_run = False
            break

        #Otherwise, we extract the minimum node, and update the current_node, and absorbed_nodes, and grid
        current_node = (min_node[0], min_node[1])                               #update current_node
        fill_rect(win, current_node, coordinates, sq_dimensions, "maroon")      #Update grid
        absorbed_nodes.append(current_node)                                     #Update absorbed_nodes
    
    #If current_node == end_node, we stop the algorithm and backtrack to find the shortest path
    else:
        shortest_path = backtrack(arr, start_node, end_node, arr_size)
        for element in shortest_path:
            fill_rect(win, element, coordinates, sq_dimensions, "navyblue")

    pygame.display.update()

#THIRD LOOP
#This loop is to ensure that window will not close
last_run = True
while last_run:
     for event in pygame.event.get():
        #Base condition to close game
        if event.type == pygame.QUIT:
            last_run = False
            pygame.quit()

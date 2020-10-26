# Oct. 2019
# Tran Le Anh, MSc Student
# Satellite Image Processing Lab, Myongji Univ., South Korea
# tranleanh.nt@gmail.com
# https://sites.google.com/view/leanhtran

# Intelligent Scissors

# USAGE:
# 1. Run the script
# 2. When the pop-up window is displayed, choose the seed points using mouse
# 3. Press ESC on the keyboard to yield the output

import matplotlib.image as mpimg
import matplotlib.pyplot as plt

import skimage
from skimage import color
from skimage import filters

from math import fabs

# Read and Pre-process image
img_name = "images/joker.jpg"
image = mpimg.imread(img_name)
image = color.rgb2gray(image)
edges = filters.scharr(image)

# Convert image to graph
G = {}
rows, cols = edges.shape
for col in range(cols):
    for row in range(rows):
        
        neighbors = []
        if row > 0:
            neighbors.append( (row-1, col) )
        
        if row < rows-1:
            neighbors.append( (row+1, col) )
            
        if col > 0:
            neighbors.append( (row, col-1) )
        
        if col < cols-1:
            neighbors.append( (row, col+1) )
        
        dist = {}
        for n in neighbors:
            # distance function can be replaced with a different norm
            dist[n] = fabs(edges[row][col] - edges[n[0], n[1]])
            
        G[(row,col)] = dist

# Apply Dijkstra's Algorithm
from dijkstra import shortestPath

INTERACTIVE = True
from itertools import cycle
import numpy as np
COLORS = cycle('rgbyc')

start_point = None
current_color = COLORS.next()
current_path = None
length_penalty = 10.0

def button_pressed(event):
    global start_point
    if start_point is None:
        start_point = (int(event.ydata), int(event.xdata))
        
    else:
        end_point = (int(event.ydata), int(event.xdata))
        path = shortestPath(G, start_point, end_point, length_penalty=length_penalty)
        plt.plot(np.array(path)[:,1], np.array(path)[:,0], c=current_color)
        start_point = end_point

def mouse_moved(event):
    if start_point is None:
        return
    
    end_point = (int(event.ydata), int(event.xdata))
    path = shortestPath(G, start_point, end_point, length_penalty=length_penalty)
    
    global current_path
    if current_path is not None:
        current_path.pop(0).remove()
    current_path = plt.plot(np.array(path)[:,1], np.array(path)[:,0], c=current_color)

def key_pressed(event):
    if event.key == 'escape':
        global start_point, current_color
        start_point = None
        current_color = COLORS.next()

        global current_path
        if current_path is not None:
            current_path.pop(0).remove()
            current_path = None
            plt.draw()

plt.connect('button_release_event', button_pressed)
if INTERACTIVE:
    plt.connect('motion_notify_event', mouse_moved)
plt.connect('key_press_event', key_pressed)

plt.gray()
plt.imshow(image)
plt.autoscale(False)
plt.title('Live-Wire Tool')
plt.show()

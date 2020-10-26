"""
File: binarySearchTreeAnimationApp.py

 Animate a Binary Search Tree using Python, pyDot, GraphViz, TK, and FFmpeg utility

 Project home: http://www.embeddedcomponents.com/blogs/2013/12/visualizing-software-tree-structures/
 
 Developed by Ron Fredericks, Video Technologist, at LectureMaker LLC, http://www.LectureMaker.com
    MIT License, Copyright (c) 2013, Ron Fredericks
    Free to use following these terms: http://opensource.org/licenses/MIT  

 Revision 3: 1/5/2014

 Usage:
     Input: A binary search tree to sketch (example provided).
            A search algorithm to animate (examples provided).
            Examples include all code needed to generate and visualize tree structures:
                1) binaryTree.py includes binaryTree class, 
                    functions to create unbalanced and balanced tree from a list, and
                    manual creation of a tree one node at a time.
                2) visualizeTree.py includes visualizeTree class,
                    functions for breadth first, depth first, and ordered depth first search.
    
     Output: This demo software presents two forms of graphic animation, using a series of png images:
                1) Animate images using the supplied slideShow TK graphics python class
                2) Animate images using mpeg4 video produced from supplied FFmpeg batch file
    

 Inspired by MITx 6.00.1x "Introduction to Computer Science and Programming"
 As taught by Professor Eric Grimson, Chairman of EECS Department, MIT
 Fall 2013, http://www.edx.org


Required Software:
    The following free open source programs should be installed on your computer:
        GraphViz: Graph visualization tool: http://www.graphviz.org/ 
        FFmpeg: Cross-platform solution to record, convert and stream audio and video: http://www.ffmpeg.org/
    
    The following python module should be installed into your environment:
        pydot: a python interface to Graphvize's Dot language: https://code.google.com/p/pydot/
    
    The following python modules are used for display of individual PNG images:
        Tkinter: standard python GUI: https://wiki.python.org/moin/TkInter
        Image and ImageTk: the python image library: http://www.pythonware.com/products/pil/ 
    
    The following support modules are supplied with this project:
        binaryTree.py     - Used to create a binary search tree to visualize.
        visualizeTree.py  - Used to draw a binary search tree as well as to draw the steps during a search.
        slideShow.py      - Used to animate a series of graphic images, 
                                in this case, the binary tree and the search process.
        png2mpg4.bat      - Used to generate mpg4 video from a series of png graphic images, 
                                in this case, the binary tree and the search process.
"""

# Local python libraries supplied with this project
import binaryTree
import visualizeTree
import slideShow

# import the graphics module used to launch supplied slideShow TK graphics python class
import Tkinter

# History:
#   Initial project published on 12/11/2013
#
#   Rev 1: 12/16/2013
#       1) Improve comments for accuracy.
#
#   Rev 2: 12/23/2013
#       1) Provide an initialization segment near the top of the code to simplify control of tree sketching and search animation
#       2) New FFmpeg command line to generate intelligently scaled video in HD from PNG image sequences:
#        ffmpeg -f image2 -r 1 -start_number 00001 -i bst_graph%%05d.png  -b:v 5000k -vcodec mpeg4 -r 30 -vf scale="'if(gt(a,4/3),1920,-1)':'if(gt(a,4/3),-1,1280)'" -y movie.mp4
#
#   Rev 3: 1/4/2014
#       1) Split program into seperate files:
#           a) binaryTree.py - binary search tree 
#           b) visualizeTree.py - pydot/GraphViz package
#           c) slideShow.py - TK graphics
#           d) binary_tree_search_video - main program
#  

#############################
# User Controlled Parameters 
#############################

# Examples

# Build balanced trees from a sorted list and rootValue set to None
#--------------------------------------------------------------------------------------

# Build a tree using an integer list. The root value is determined automatically

listForTree = sorted([5,2,1,4,8,6,7,3])
rootValue = None   # Note: None will be replaced by the midpoint of the sorted list
findValue = '1'

# build a tree using a character list. The root value is determined automatically
"""
listForTree = [c for c in 'abcdefghijklmnopqrstuvwxyz']
rootValue = None   # Note: None will be replaced by the midpoint of the list
findValue = 'j'
"""

# Build unbalanced trees using an unsorted list and rootValue set to a known value in list 
#---------------------------------------------------------------------------------------

# Build a tree using an integer list. The root value is determined manually 
"""
listForTree = [5,2,1,4,8,6,7,3]
rootValue = 5   # Note: Select a root key from the list of elements in listForTree
findValue = '7'
"""

# Longer alpha demo with randomly shuffled tree data, and random choice for search value
"""
import random
listForTree = [c for c in 'abcdefghijklmnopqrstuvwxyz']
rootValue = listForTree[len(listForTree)/2] # Note: Select a root key from the list of elements in listForTree
random.shuffle(listForTree)
findValue = random.choice(listForTree)
"""


# Select a predefined search function from options described above (in overview)
#------------------------------------------------------------------------------------

searchNameFcn = {'DFSOrdered': visualizeTree.DFSOrdered, 'DFS': visualizeTree.DFS, 'BFS': visualizeTree.BFS}
    
#searchName = ''              # Don't search
searchName = 'BFS'            # Breadth-first Search
#searchName = 'DFS'           # Depth-first Search
#searchName = 'DFSOrdered'    # Ordered Depth-first Search


# Define path where image sequences will be stored (windows example)
#--------------------------------------------
fileDir = "C:\\Users\\Ron Fredericks\\Documents\\LectureMaker\\Projects\\MOOC\\EDx\\cs600.1\\Video\\vidImages\\"


#####################################################################################
# Generate a Binary Tree using controls defined above and Print Out Animation Status
#####################################################################################

# Display 'sketch tree' and 'animate search' parameters
if not rootValue:
    print "Generate a balanced tree with",   
    root = binaryTree.buildBalancedTree(listForTree[:], 0, len(listForTree))
else:
    print "Generate an unbalanced tree with", 
    root = binaryTree.buildUnbalancedTree(listForTree[:], rootValue)
if not root:
    print "Error: tree not built",
    raw_input("Press return key to continue: ")
print "root value:", root.getValue()    

print "List used to generate tree:", str(listForTree)
print "Search for a value of", findValue, "using", searchName, "search method"

# Demonstrate insert() and delete() binaryTree methods
nodeInserted = root.insert(1)
if nodeInserted != None:
    print "Node " + str(nodeInserted.getValue()) + " was successfully inserted into tree"
    print root.delete(1)
else:
    print "Node not inserted"    


##################################################################
# Draw and animate binary search tree during a BFS or DFS search
##################################################################

# Instantiate the visualizeTree object
vT = visualizeTree.visualizeTree(fileDir)

# Draw the initial binary search tree.
vT.searchTree(root, visualizeTree.sketchTree)
vT.setVidFrames(3)
vT.updateGraph()
vT.appendVisualizeList()

# Animate a search to find a node in the tree.
if searchName:
    vT.setVidFrames(1)
    vT.searchTree(root, searchNameFcn[searchName], findValue)

# extend the final segment of video for 3 more frames (or 3 seconds in video, based on FFmpeg settings)
vT.setVidFrames(3)
vT.updateGraph()


##################################################################
# Animate the search method using TK graphics
##################################################################

mainTitle = "Find " + '"' + findValue + '"' + " using " + searchName
rootTk = Tkinter.Tk()
playList = vT.visualizeList
sShow = slideShow.slideShow(rootTk)
sShow.setImageScaling(1280, 720)
sShow.playSlides(playList, mainTitle, "Quit", True)
rootTk.destroy()

import sys
import Image

"""##########################################################################


	This implementation does not work as of yet. This is my first attempt at a belief propagation algorithm.
	The intended output is a color image but currently the same image just gets outputted.


##########################################################################"""


EAST = 1
WEST = 2
SOUTH = 3
NORTH = 4
OUT_DIRECTION = 0
IN_DIRECTION = 1

#get true pixel value
def truePixel( pixelRow, pixelCol ):
	return pixelRow * imageWidth + pixelCol

#get pixel coordinates
def pixelCoordinates( pixelIndex ):
	return pixelIndex/imageWidth, pixelIndex%imageWidth

#get the neighbors of pixels, or function nodes, and also the total number of potentials
def mapNeighbors():
	neighborsOfPixels = {}
	neighborsOfFunctions = {}
	edgeSeen = []
	pixelsSeen = []
	totPots = 0

	for i in range( imageHeight ):
		for j in range( imageWidth ):
	
			a = truePixel(i,j)
	
			#initialize array of neighbors if a has not been seen before
			if a not in pixelsSeen:
				pixelsSeen.append(a)
				neighborsOfPixels[a] = []
	
			#ensure there is a neighboring pixel in any given particular direction
			if j < imageWidth - 1:
				b = truePixel(i,j+1)

				#do not double count edges
				if (a,b) not in edgeSeen:

					#initialize array of neighbors if b has not been seen before
					if b not in pixelsSeen:
						pixelsSeen.append(b)
						neighborsOfPixels[b] = []

					#add the function nodes which neighbor the pixel.
					#EAST/WEST refer to the relative location of the function node with respect to the pixel node
					neighborsOfPixels[a].append((EAST,totPots))
					neighborsOfPixels[b].append((WEST,totPots))

					#store the neighbors of the function nodes.
					#EAST/WEST refers to the relative location of the function node with respect to the pixel node
					neighborsOfFunctions[totPots] = []
					neighborsOfFunctions[totPots].append((EAST, a))
					neighborsOfFunctions[totPots].append((WEST, b))

					totPots += 1

					#record seeing this edge
					edgeSeen.append((a,b))
					edgeSeen.append((b,a))


			######The following cases follow the case above

			if j > 0:
				b = truePixel(i,j-1)
				if (a,b) not in edgeSeen:
					if b not in pixelsSeen:
						pixelsSeen.append(b)
						neighborsOfPixels[b] = []
					neighborsOfPixels[a].append((WEST,totPots))
					neighborsOfPixels[b].append((EAST,totPots))
					neighborsOfFunctions[totPots] = []
					neighborsOfFunctions[totPots].append((WEST, a))
					neighborsOfFunctions[totPots].append((EAST, b))
					totPots += 1
					edgeSeen.append((a,b))
					edgeSeen.append((b,a))
			if i < imageHeight - 1:
				b = truePixel(i+1,j)
				if (a,b) not in edgeSeen:
					if b not in pixelsSeen:
						pixelsSeen.append(b)
						neighborsOfPixels[b] = []
					neighborsOfPixels[a].append((SOUTH,totPots))
					neighborsOfPixels[b].append((NORTH,totPots))
					neighborsOfFunctions[totPots] = []
					neighborsOfFunctions[totPots].append((SOUTH, a))
					neighborsOfFunctions[totPots].append((NORTH, b))
					totPots += 1
					edgeSeen.append((a,b))
					edgeSeen.append((b,a))
			if i > 0:
				b = truePixel(i-1,j)
				if (a,b) not in edgeSeen:
					if b not in pixelsSeen:
						pixelsSeen.append(b)
						neighborsOfPixels[b] = []
					neighborsOfPixels[a].append((NORTH,totPots))
					neighborsOfPixels[b].append((SOUTH,totPots))
					neighborsOfFunctions[totPots] = []
					neighborsOfFunctions[totPots].append((NORTH, a))
					neighborsOfFunctions[totPots].append((SOUTH, b))
					totPots += 1
					edgeSeen.append((a,b))
					edgeSeen.append((b,a))
	return neighborsOfPixels, neighborsOfFunctions, totPots

def computeH():
	h = []
	for i in range( 256 ):
		h.append([])
		for j in range( 256 ):
			h[i].append( -(i-j)**2.0/50.0 )
	return h

def initialize_mg_x():
	toReturn = [[1.0 if pixels[j/imageWidth,j%imageWidth] == i else 0.0 for i in range(256)] for j in range(imageWidth * imageHeight)]
	return toReturn

def initialize_mf_x():
	toReturn = [[[0.0 for i in range(256)] for j in range(2)] for k in range(totPots)]
	return toReturn

def initialize_mx_f():
	toReturn = [[[0.0 for i in range(256)] for j in range(2)] for k in range(totPots)]
	return toReturn

#update the allmessages matrix at location v,i,j
def updateFromFunctionNodes( pixelValue, pixelRow, pixelCol ):
	pixelIndex = truePixel( pixelRow, pixelCol )

	#get the function neighbors of the pixel mapped by i,j
	f_neighbors = neighborsOfPixels[pixelIndex]

	#progressively aggregate neighbor f nodes
	toReturn = allMessages[pixelValue][pixelCol][pixelRow]
	for f_neighbor in f_neighbors:
		toReturn += mf_x[f_neighbor[1]][OUT_DIRECTION][pixelValue]

	#include the g nodes
	toReturn += mg_x[pixelIndex][pixelValue]
	return toReturn

def getAllMessagesValue( v, f ):

	#get the two pixel neighbors of the function f
	pixelNeighbors = neighborsOfFunctions[f]

	#determine which neighbor is to the EAST/SOUTH and get the value from all messages corrsponding to that neighbor
	for neighbor in pixelNeighbors:
		if neighbor[0] == EAST or neighbor[0] == SOUTH:
			col, row = pixelCoordinates( neighbor[1] )
			return allMessages[v][col][row]

if len( sys.argv ) != 2:
	print 'Usage: python BeliefPropagation.py <noisy_picture>'
	sys.exit( 1 )

im = Image.open( sys.argv[1] )
pixels = im.load()
imageWidth = im.size[0]
imageHeight = im.size[1]

neighborsOfPixels, neighborsOfFunctions, totPots = mapNeighbors()

h = computeH()

mf_x = initialize_mf_x()
mx_f = initialize_mx_f()
mg_x = initialize_mg_x()

#initialize all messages to equal mg_x
allMessages = []
for v in range(256):
	allMessages.append([])
	for i in range( imageHeight ):
		allMessages[v].append([])
		for j in range( imageWidth ):
			allMessages[v][i].append( mg_x[truePixel(i,j)][v] )

for k in range(9):

	#update all messages
	for v in range(256):
		for i in range( imageHeight ):
			for j in range( imageWidth ):
				allMessages[v][i].append( updateFromFunctionNodes( v, i, j ) )

	#reconstruction array
	rec = [[ allMessages[:][i][j].index(max(allMessages[:][i][j])) for j in range(imageWidth)]for i in range(imageHeight)]

	#update messages
	for v in range(256):
		for f in range(totPots):
			mx_f[f][IN_DIRECTION][v] = getAllMessagesValue( v, f ) - mf_x[f][OUT_DIRECTION][v]

	for v in range(256):
		for f in range(totPots):
			mf_x[f][OUT_DIRECTION][v] = max([a + b for a, b in zip(h[:][v], mx_f[f][OUT_DIRECTION][:])])
			
	#save picture
	im.putdata( rec )
	im.save( 'out' + str(k) + '.png' )

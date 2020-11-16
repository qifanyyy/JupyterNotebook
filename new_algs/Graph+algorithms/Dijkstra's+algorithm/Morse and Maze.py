import itertools
import re
from collections import defaultdict
with open('dictionary.txt') as f:
    dictionary_words = [word.upper().strip() for word in f]


MORSETRANSLATION = {'.-': 'A', '-...': 'B', '-.-.': 'C',
					'-..': 'D', '.': 'E', '..-.': 'F',
					'--.': 'G', '....': 'H', '..': 'I',
					'.---': 'J', '-.-': 'K', '.-..': 'L',
					'--': 'M', '-.': 'N', '---': 'O',
					'.--.': 'P', '--.-': 'Q', '.-.': 'R',
					'...': 'S', '-': 'T', '..-': 'U',
					'...-': 'V', '.--': 'W', '-..-': 'X',
					'-.--': 'Y', '--..': 'Z',
					'-----': '0', '.----': '1', '..---': '2',
					'...--': '3', '....-': '4', '.....': '5',
					'-....': '6', '--...': '7', '---..': '8',
					'----.': '9'}

def morseDecode(inputStringList):
	"""
	This method should take a list of strings as input. Each string is equivalent to one letter
	(i.e. one morse code string). The entire list of strings represents a word.

	This method should convert the strings from morse code into english, and return the word as a string.

	"""
	return ''.join(MORSETRANSLATION.get(i.upper()) for i in inputStringList)


def morsePartialDecode(inputStringList):
	"""
	This method should take a list of strings as input. Each string is equivalent to one letter
	(i.e. one morse code string). The entire list of strings represents a word.

	However, the first character of every morse code string is unknown (represented by an 'x' (lowercase))
	For example, if the word was originally TEST, then the morse code list string would normally be:
	['-','.','...','-']

	However, with the first characters missing, I would receive:
	['x','x','x..','x']

	With the x unknown, this word could be TEST, but it could also be EESE or ETSE or ETST or EEDT or other permutations.

	We define a valid words as one that exists within the dictionary file provided on the website, dictionary.txt
	When using this file, please always use the location './dictionary.txt' and place it in the same directory as
	the python script.

	This function should find and return a list of strings of all possible VALID words.
	"""
	possible_letters_list_dot = []
	possible_letters_list_hyphen = []
	valid_words = []
	for partialMorseLetter in inputStringList:
		partialMorseLetterDot = re.sub('[x]', '.', partialMorseLetter)
		partialMorseLetterDotTranslated = morseDecode([partialMorseLetterDot]) #sub it into morse decode
		possible_letters_list_dot.append(partialMorseLetterDotTranslated) #append the MORSE translations where x=. to a list

		partialMorseLetterHyphen = re.sub('[x]', '-', partialMorseLetter)
		partialMorseLetterHyphenTranslated = morseDecode([partialMorseLetterHyphen])
		possible_letters_list_hyphen.append(partialMorseLetterHyphenTranslated) #append the MORSE translations where x=- to a list

	possible_letters_list = list(zip(possible_letters_list_dot, possible_letters_list_hyphen))
	possible_words_separated = list(itertools.product(*possible_letters_list))
	possible_words = [''.join(x) for x in possible_words_separated] #Possible words generated from the provided letters

	for word in dictionary_words:
		if word in possible_words:
			valid_words.append(word)

	return valid_words



class DijkstraNode:

	def __init__(self, x, y, parent, dist):

		self.x = x
		self.y = y
		self.dist = dist
		self.neighbours = []
		self.parent = parent
		self.explored = False




class Maze:

	def __init__(self):
		"""
		Constructor - You may modify this, but please do not add any extra parameters
		"""
		# Gives a dictionary that returns 1 if the key does not exist
		self.MazeMap = defaultdict(lambda: 1, {})
		self.x_maximum, self.y_maximum = 0, 0

	def findRoute(self, x1, y1, x2, y2):
		"""
		This method should find a route, traversing open spaces, from the coordinates (x1,y1) to (x2,y2)
		It should return the list of traversed coordinates followed along this route as a list of tuples (x,y),
		in the order in which the coordinates must be followed
		If no route is found, return an empty list
		"""

		# Check to see if the start and end node are the same
		if x1 == x2 and y1 == y2:
			return [(x1, y1)]

		root_node = DijkstraNode(x1, y1, None, 0)
		root_node.neighbours = self.getNeighbours(x1, y1)

		# Create a dictionary to store all of the nodes
		all_nodes = {(x1, y1): root_node}
		# If no starting place is found return nothing
		if len(root_node.neighbours) == 0:
			return []
		current_node = root_node
		while (x2, y2) not in all_nodes:

			# If the algorithm hasn't found the target node and cannot explore further then return empty path
			if current_node is None:
				return []

			current_node.neighbours = self.getNeighbours(current_node.x, current_node.y)

			# The distance from the root node through the current node to the neighbour
			current_neighbour_dist = current_node.dist + 1

			for neighbour in current_node.neighbours:
				if neighbour in all_nodes:
					neighbour_node = all_nodes[neighbour]
					if current_neighbour_dist < neighbour_node.dist:
						# The new best path is through the current node
						neighbour_node.parent = current_node
						neighbour_node.dist = current_neighbour_dist
				else:
					# Add a new node if it doesn't exist within the currently explored nodes
					all_nodes[neighbour] = DijkstraNode(neighbour[0], neighbour[1], current_node, current_neighbour_dist)

			# Mark the current node as being explored as you have checked all the neighbours
			current_node.explored = True

			# Gets a list of all of the unexplored nodes to check for the next node to explore
			unexplored_nodes = [node for _, node in all_nodes.items() if not node.explored]

			if len(unexplored_nodes) > 0:
				# Go to the next node with the smallest distance that hasn't been explored
				current_node = min(unexplored_nodes, key=lambda node: node.dist)
			else:
				current_node = None

		# Make your way back from the target node
		current_node = all_nodes[(x2, y2)]
		# Initialise a list to hold the path going from the target to the root
		reversed_path = []
		# This will end when the root node tries to travel to a None node
		while current_node is not None:
			# Add the current node to the list
			reversed_path.append((current_node.x, current_node.y))
			# Travel to the parent node
			current_node = current_node.parent
			# current_node will be None at the root because the parent of the root node is 'None'

		# Return the list in the correct order
		return list(reversed(reversed_path))

	def getNeighbours(self, x, y):
		north = (x, y+1) if self.MazeMap[(x, y+1)] == 0 else None
		east = (x+1, y) if self.MazeMap[(x+1, y)] == 0 else None
		south = (x, y-1) if self.MazeMap[(x, y-1)] == 0 else None
		west = (x-1, y) if self.MazeMap[(x-1, y)] == 0 else None
		# Only add the neighbours that are not none
		valid_neighbours = [neighbour for neighbour in [north, east, south, west] if neighbour is not None]
		return valid_neighbours

	def addCoordinate(self, x, y, blockType):
		"""
		Add information about a coordinate on the maze grid
		x is the x coordinate
		y is the y coordinate
		blockType should be 0 (for an open space) of 1 (for a wall)
		"""
		# Use a dictionary to store the blocks that you know about
		self.MazeMap[(x, y)] = blockType
		self.y_maximum = max(self.y_maximum, y)
		self.x_maximum = max(self.x_maximum, x)

	def printMaze(self):
		"""
		Print out an ascii representation of the maze.
		A * indicates a wall and a empty space indicates an open space in the maze
		"""
		def getString(tile):
			if tile == 0:
				return " "
			else:
				return "*"

		# Loop through each row, given by y coordinate
		for y in range(self.y_maximum + 1):
			# Joins the row of symbols together, converting each coordinate into its symbol
			# i.e. gets the entire row at y and prints it as a string (same as below):
			# row_string = ""
			# for x in range(self.x_maximum + 1):
			# 	row_string += getString(self.MazeMap[(x, y)])
			# print(row_string)
			print("".join([getString(self.MazeMap[(x, y)]) for x in range(self.x_maximum + 1)]))




def morseCodeTest():
	"""
	This test program passes the morse code as a list of strings for the word
	HELLO to the decode method. It should receive a string "HELLO" in return.
	This is provided as a simple test example, but by no means covers all possibilities, and you should
	fulfill the methods as described in their comments.
	"""

	hello = ['....','.','.-..','.-..','---']
	print(morseDecode(hello))

def partialMorseCodeTest():

	"""
	This test program passes the partial morse code as a list of strings
	to the morsePartialDecode method. This is provided as a simple test example, but by
	no means covers all possibilities, and you should fulfill the methods as described in their comments.
	"""

	# This is a partial representation of the word TEST, amongst other possible combinations
	test = ['x','x','x..','x']
	print(morsePartialDecode(test))

	# This is a partial representation of the word DANCE, amongst other possible combinations
	dance = ['x..','x-','x.','x.-.','x']
	print(morsePartialDecode(dance))



def mazeTest():
	"""
	This sets the open space coordinates for the example
	maze in the assignment.
	The remainder of coordinates within the max bounds of these specified coordinates
	are assumed to be walls
	"""
	myMaze = Maze()
	myMaze.addCoordinate(1,0,0)
	myMaze.addCoordinate(1,1,0)
	myMaze.addCoordinate(7,1,0)
	myMaze.addCoordinate(1,2,0)
	myMaze.addCoordinate(2,2,0)
	myMaze.addCoordinate(3,2,0)
	myMaze.addCoordinate(4,2,0)
	myMaze.addCoordinate(6,2,0)
	myMaze.addCoordinate(7,2,0)
	myMaze.addCoordinate(4,3,0)
	myMaze.addCoordinate(7,3,0)
	myMaze.addCoordinate(4,4,0)
	myMaze.addCoordinate(7,4,0)
	myMaze.addCoordinate(3,5,0)
	myMaze.addCoordinate(4,5,0)
	myMaze.addCoordinate(7,5,0)
	myMaze.addCoordinate(1,6,0)
	myMaze.addCoordinate(2,6,0)
	myMaze.addCoordinate(3,6,0)
	myMaze.addCoordinate(4,6,0)
	myMaze.addCoordinate(5,6,0)
	myMaze.addCoordinate(6,6,0)
	myMaze.addCoordinate(7,6,0)
	myMaze.addCoordinate(5,7,0)
	myMaze.printMaze()
	print(myMaze.findRoute(x1=1, y1=0, x2=5, y2=7))

def main():
	morseCodeTest()
	partialMorseCodeTest()
	mazeTest()



if(__name__ == "__main__"):
	main()

# UID: 1901208601

import csv

# Adapted from Practical 4 Section 1.5.1: Implementation
class Vertex:
    def __init__(self, id):
        self.id = id
        self.adjacent =	{}
		# Closest thing to infinity: https://www.tutorialspoint.com/How-can-I-represent-an-infinite-number-in-Python
        self.dist = float('inf')
        self.previousVertex = False
        self.path = {}

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])
    def addNeighbour(self, neighbour, weight=0):
        self.adjacent[neighbour] = weight
    def getConnections(self):
        return self.adjacent.keys()
    def getId(self):
        return self.id
    def getWeight(self, neighbour):
        return self.adjacent[neighbour]
    def setDist(self, dist):
        self.dist = dist
    def getDist(self):
        return self.dist
    def setPreviousVertex(self, vertex):
    	self.previousVertex = vertex
    def getPreviousVertex(self):
    	return self.previousVertex
    def setPath(self, key, path):
        self.path[key] = path
    def getPath(self, key):
        return self.path[key]

# Adapted from Practical 4 Section 1.5.1: Implementation
class Graph:
    def __init__(self):
        self.vertDict = {}
        self.numVertices = 0
    def __iter__(self):
        return iter(self.vertDict.values())
    def addVertex(self, id):
        self.numVertices += 1
        newVertex = Vertex(id)
        self.vertDict[id] = newVertex
        return newVertex
    def getVertex(self, n):
        if n in self.vertDict:
            return self.vertDict[n]
        else:
            return None
    def getVertices(self):
        return self.vertDict.keys()
    def addEdge(self, frm, to, cost=0):
        if frm not in self.vertDict:
            self.addVertex(frm)
        if to not in self.vertDict:
            self.addVertex(to)

        self.vertDict[frm].addNeighbour(self.vertDict[to], cost)
        self.vertDict[to].addNeighbour(self.vertDict[frm], cost)


# Adapted from Practical 1 Section 1.45.4: Reading Individual Words
# csv.reader usage from Python documentation: https://docs.python.org/3/library/csv.html
# Read csv file into a dictionary
def readCSV(file):
    # Initiate vars
	currentLine = 0
	output = {}
	headers = []

    # Open file
	with open(file, 'r')  as openedFile:
        # Loop through each line in file
		for line in csv.reader(openedFile):
            # Set current word of line to 0
			currentWord = 0

            # Loop through each word in line
			for word in line:
                # If the the first word then add the word to the header list, else add to dictionary under header
				if (currentLine == 0):
                    # Append header to dictionary and initiate empty list
					output[word] = []

                    # Add header to header list
					headers.append(word)
				else:
                    # Add value to dictionary under its header
                    # i.e. {'station1': [1]}
					output[headers[currentWord]].append(word)

                # Increment word count
				currentWord += 1

            # Increment line count
			currentLine += 1

    # Add headers to dictionary
	output['headers'] = headers

    # Return the dictionary of the imported csv
	return output

# Format the lines dictionary so that it is accessible by line_id
# Not currently in use, by would be used to easily associate a connection line with it's line data
def formatLines(lines):
	formattedLines = {}

	for x in range(len(lines[lines['headers'][0]])):
		temp = {}

		for y in range(1, len(lines['headers'])):
			temp[lines['headers'][y]] = lines[lines['headers'][y]][x]

		formattedLines[lines[lines['headers'][0]][x]] = temp

	return formattedLines

# Format the stations dictionary so that it is accessible by id
def formatStations(stations):
    formattedStations = {}

    for x in range(len(stations['id'])):
        formattedStations[stations['id'][x]] = {
            'id'            : stations['id'][x],
            'latitude'      : stations['latitude'][x],
            'longitude'     : stations['longitude'][x],
            'name'          : stations['name'][x],
            'display_name'  : stations['display_name'][x],
            'zone'          : stations['zone'][x],
            'total_lines'   : stations['total_lines'][x],
            'rail'          : stations['rail'][x],
        }

    return formattedStations

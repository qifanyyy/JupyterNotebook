# UID: 1901208601

import londonModel

# Initiate data structures from supplied csv files
lines = londonModel.formatLines(londonModel.readCSV('files/londonlines.csv'))
stations = londonModel.formatStations(londonModel.readCSV('files/londonstations.csv'))
connections = londonModel.readCSV('files/londonconnections.csv')

# Global variable for the graph
graph = None

# Return stations
def getStations():
	return stations

# Dijkstras fastest route algorithm Implementation
def findFastestRoute(start, end, unavailableStations):
	global graph

	graph = londonModel.Graph()

	# Error check inputs
	response = validateStations(start, end, unavailableStations)

	# If response set then inputs arent valid
	if response:
		return response

	# Get the id from the string station name
	start = getStationIdFromName(start)
	end = getStationIdFromName(end)

	# Add the stations to the graph
	addStations(unavailableStations)

	# Visited nodes list
	visited = []

	# Unvisited nodes list
	unvisited = list(graph.getVertices())

	# Set current node dist to 0
	for vertex in graph:
		if (start == vertex.getId()):
			vertex.setDist(0)
			start = vertex

	# While there are still unvisited nodes
	while (len(unvisited) != 0):
		# Get next node
		nextNode = getNextNode(unvisited)

		# Check the neighbouring nodes
		checkNeighbours(nextNode)

		# Remove node from unvisited
		del unvisited[unvisited.index(nextNode.getId())]

		# Add node to visited
		visited.append(nextNode.getId())

	# set paths to starting node
	setPaths(start)

	# get the path between supplied nodes
	path = getPath(start, end)

	# If there is a path to station return it, else return error
	if path != []:
		return path
	else:
		response = {
			'error': True,
			'msg': 'No possible route between stations'
		}

		return response

def validateStations(start, end, unavailableStations):
	# Set default response
	response = {
		'error': True,
		'msg': ''
	}

	# If either start or end are empty, return error
	if (start == '' or end == ''):
		response['msg'] = 'Please select a starting and ending station'
		return response

	# If start and end are the same, return error
	if (start == end):
		response['msg'] = 'Starting and ending stations are the same'
		return response

	# If start or end are unavailble, return error
	if start in unavailableStations or end in unavailableStations:
		response['msg'] = 'No possible route between stations'
		return response

	# No errors, so return None
	return None

def getStationIdFromName(target):
	for id in stations:
		if (stations[id]['name'] == target):
			return id

# Add connections to graph
def addStations(unavailable):
	# Loop through each station connection
	for x in range(len(connections['station1'])):
		# If unavailble list is empty, add to graph
		if (unavailable == None):
			graph.addEdge(connections['station1'][x], connections['station2'][x], int(connections['time'][x]))
		else:
			# If both stations aren't in the unavailable list, add to graph
			if (stations[connections['station1'][x]]['name'] not in unavailable and stations[connections['station2'][x]]['name'] not in unavailable):
				graph.addEdge(connections['station1'][x], connections['station2'][x], int(connections['time'][x]))

# Get the next node to be checked
def getNextNode(unvisited):
	nextNode = False

	for vertex in graph:
		if (vertex.getId() in set(unvisited)):
			if (nextNode == False):
				nextNode = vertex

			if (vertex.getDist() < nextNode.getDist()):
				nextNode = vertex

	return nextNode

# Check the weights of the neighbours of the given node
def checkNeighbours(currentNode):
	# Adjacent nodes list
	neighbours = []

	# Get adjacent nodes to current node
	neighbours = currentNode.getConnections()

	for vertex in neighbours:
		# New tentativeDist
		tentativeDist = currentNode.getDist() + vertex.getWeight(currentNode)

		# If new tentativeDist is less than the current dist to node, update it
		if (tentativeDist < vertex.getDist()):
			# Update to the new shortest distance
			vertex.setDist(tentativeDist)

			# Update to the new previous node
			vertex.setPreviousVertex(currentNode)

# For each vertex in the graph set their paths from starting node
def setPaths(start):
	for vertex in graph:
		path = pathToVertex(vertex, [])

		if vertex.getDist() != float('inf'):
			vertex.setPath(start.getId(), path[::-1])

# Set the path to vertex from the starting node
def pathToVertex(vertex, path):
	# If current vertex has a previous vertex
	if (vertex.getPreviousVertex()):
		# Append the current vertex id to the path
		path.append(vertex.getId())

		# Check the previous vertex
		pathToVertex(vertex.getPreviousVertex(), path)
	else:
		# No previous vertex so append self
		path.append(vertex.getId())

	return path

# Get the path from the starting node to end node
def getPath(start, end):
	vertex = graph.getVertex(end)
	path = []

	if  vertex == None:
		return path

	# If dist is infinite then there is no possible route
	if vertex.getDist() == float('inf'):
		return path

	for x in vertex.getPath(start.getId()):
		path.append(stations[x]['name'])

	return path

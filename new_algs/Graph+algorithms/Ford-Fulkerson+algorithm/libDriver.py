import json
import flow

# Given an input in JSON form or a File, extract graph information
def extractFromJson(inpt, isFile=False):
	# Check if the input is a file, and if so, convert it
	jsonObj = inpt
	if(isFile):
		with open(inpt) as json_input:
			jsonObj = json.load(json_input)

	# Define three flags which will aide in error checking
	hasHospital, hasRegion, hasAmbulance = False, False, False

	# Define the initial empty graph with a source node built in
	edges = []
	vertexNames = ["Epicenter"]
	flowDemanded = 0
	
	# Attempt to extract information
	try: 
		# For all hospital vertices, add to the graph
		for hospital, bedsAvailable in jsonObj["hospitals"]:
			hasHospital = True
			vertex = len(vertexNames)
			vertexNames.append(hospital)
			edges.append([vertex, -2, int(bedsAvailable)])
		# For all regional vertices, add to the graph
		for region, injured in jsonObj["regions"]:
			hasRegion = True
			vertex = len(vertexNames)
			vertexNames.append(region)
			edges.append([0, vertex, int(injured)])
			flowDemanded += injured
		# For all ambulatory network vertices, add to the graph each one
		for ambulance, region, hospital, capacity in jsonObj["ambulances"]:
			hasAmbulance = True
			vertex = len(vertexNames)
			vertexNames.append(ambulance)
			srcInd = vertexNames.index(region) if region in vertexNames else -1
			dstInd = vertexNames.index(hospital) if hospital in vertexNames else -1
			edges.append([srcInd, vertex, int(capacity)])
			edges.append([vertex, dstInd, int(capacity)])
	
		# Handle the sink node and connect each hospital to them
		sinkVertex = len(vertexNames)
		vertexNames.append("Safety")
		for i, e in enumerate(edges):
			if(e[1] == -2):
				edges[i][1] = sinkVertex
	# In the event of an error, return None
	except:
		return None

	# In the event that at least one vertex type is not represented, return none
	if(not(hasAmbulance and hasRegion and hasHospital)):
		return None
	
	# Return the n, f, e, v
	return (len(vertexNames), flowDemanded, edges, vertexNames)

# Given a JSON file/Object, compute the graph flow on it
def computeFromJson(inpt, isFile=False, printData=True):
	# Call the extraction function to get our graph given our input/isFile status
	vNum, fDemanded, edges, names = extractFromJson(inpt, isFile = isFile)
	# Call the algorithm
	flowSupplied, pathing = flow.fordFulkerson(vNum, edges, 0, vNum-1)
	# If the user decides to print out information, print out a summary of the graph
	if(printData):
		if(fDemanded == flowSupplied):
			print("Ambulatory Network can sustain all injured.")
			print("Quickly use the following routes")
		else:
			print("Ambulatory Network *cannot* sustain all injured.")
			print("To minimize loss of life, triage and use the following routes: ")

		for (injured, path) in pathing:
			print("Send %05d Injured Along: " % injured, end="")
			for i, route in enumerate(path[1:-1]):
				print("%s" % (names[route]), end="")
				if(i < len(path)-3):
					print(" -> ", end="")
			print()

	# Generate a list of the paths a person should take in dictionary form
	pathList = []
	for (injured, path) in pathing:
		pathList.append({
			"capacity": injured,
			"path": [names[route] for route in path[1:-1]]
		})
	# Return a dictionary representing the information the graph resulted in
	return {
		"flow": {
			"demanded": fDemanded,
			"supplied": flowSupplied
		},
		"path": pathList
	}

# print(computeFromJson("survival.json", isFile=True))

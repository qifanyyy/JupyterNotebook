# Import the required information
import os
from flow import fordFulkerson

# Define some constants that will act as separators in the received file
REGIONAL_START = "[Regions]"
HOSPTIAL_START = "[Hospitals]"
AMBULANCE_START = "[Ambulatory Service]"

# Extract file information given a particular filename
def extractFile(filename):
	# Define some base states about our vertices / edges
	edges = []
	vertexNames = ["Epicenter", ]
	flowDemanded = 0
	# Create 3 boolean flags to ensure proper error handling
	hasRegion, hasHospital, hasAmbulance = False, False, False
	try:
		# Open the file name that we were given
		with open(filename, "r") as fp:
			section = -1
			# Iterate through each line of the file
			for line in fp:
				# Strip leading/trailing formatting characters and skip empty lines
				line = line.strip()
				if(not line):
					continue
	
				# Check if the line is a delimiter for regions
				if(line == REGIONAL_START):
					section = 0
				# Check if the line is a delimiter for hospitals
				elif(line == HOSPTIAL_START):
					section = 1
				# Check if the line is a delimiter for ambulance
				elif(line == AMBULANCE_START):
					section = 2
				# We are in the region section, parse line as a region
				elif(section == 0):
					# Verify at least 1 region exists
					hasRegion = True
					# Extract the name / casualty count
					regionName, regionCasualties = line.split(",")
					regionCasualties = int(regionCasualties)
					# Get the vertex index and append the name to the vertexNames
					vertex = len(vertexNames)
					vertexNames.append(regionName)
					# Increase the demaned flow
					flowDemanded += regionCasualties
					edges.append([0, vertex, regionCasualties])
				# We are in the hospital section, parse the line like a hospital
				elif(section == 1):
					# Verify at least one hospital is in graph
					hasHospital = True
					# Extract out the information about the hospital, convert strings to integers if necessary
					regionName, bedsAvailable = line.split(",")
					bedsAvailable = int(bedsAvailable)
					# Get the vertex number and append the vertex to the graph
					vertex = len(vertexNames)
					vertexNames.append(regionName)
					edges.append([vertex, -2, bedsAvailable])
				# We are in the ambulance section
				elif(section == 2):
					# Verify at least 1 ambulance exists
					hasAmbulance = True
					# Perform extraction
					ambName, fromRegion, toHospital, cap = line.split(",")
					cap = int(cap)
					vertex = len(vertexNames)
					vertexNames.append(ambName)
					srcInd = -1
					if(fromRegion.strip() in vertexNames):
						srcInd = vertexNames.index(fromRegion.strip())
					dstInd = -1
					if(toHospital.strip() in vertexNames):
						dstInd = vertexNames.index(toHospital.strip())
					# Append information
					edges.append([srcInd, vertex, cap])
					edges.append([vertex, dstInd, cap])
	# If an error is encountered, return None
	except:
		return None
	# If one of the 3 sections has not been filled, return none
	if(not (hasAmbulance and hasRegion and hasHospital)):
		return None
	# Append the sink verted
	vertexNames.append("Safety")
	sinkVertex = len(vertexNames)-1
	# Check each hospital vertex and set an edge to the sink
	for i, e in enumerate(edges):
		if(e[1] == -2):
			edges[i][1] = sinkVertex
	# Return the n, f, e, v
	return (len(vertexNames), flowDemanded, edges, vertexNames)

def processGuiInput(text):
	# Setup the default initialized variables for the function
	edges = []
	vertexNames = ["Epicenter", ]
	flowDemanded = 0
	# Create 3 boolean flags which will aid in error checking
	hasRegion, hasHospital, hasAmbulance = False, False, False
	section = -1
	# Attempt the code
	try:
		# Split the given text into separate lines based on new-line characters
		text = text.splitlines()
		# Iterate through each line
		for line in text:
			# String each line of it's trailing/leading characters
			line = line.strip()
			# If an empty line is encountered, skip
			if(not line):
				continue
			# Check lines against Delimiter for regions
			if(line == REGIONAL_START):
				section = 0
			# Check line against delimiter for hospital
			elif(line == HOSPTIAL_START):
				section = 1
			# Check line against delimter for ambulance
			elif(line == AMBULANCE_START):
				section = 2
			# Parse line like a region
			elif(section == 0):
				hasRegion = True
				regionName, regionCasualties = line.split(",")
				regionCasualties = int(regionCasualties)
				vertex = len(vertexNames)
				vertexNames.append(regionName)
				flowDemanded += regionCasualties
				edges.append([0, vertex, regionCasualties])
			# Parse line like a hospital
			elif(section == 1):
				hasHospital = True
				regionName, bedsAvailable = line.split(",")
				bedsAvailable = int(bedsAvailable)
				vertex = len(vertexNames)
				vertexNames.append(regionName)
				edges.append([vertex, -2, bedsAvailable])
			# Parse line like an ambulance
			elif(section == 2):
				hasAmbulance = True
				ambName, fromRegion, toHospital, cap = line.split(",")
				cap = int(cap)
				vertex = len(vertexNames)
				vertexNames.append(ambName)
				srcInd = -1
				if(fromRegion.strip() in vertexNames):
					srcInd = vertexNames.index(fromRegion.strip())
				dstInd = -1
				if(toHospital.strip() in vertexNames):
					dstInd = vertexNames.index(toHospital.strip())
				edges.append([srcInd, vertex, cap])
				edges.append([vertex, dstInd, cap])
	# If an error occurs, return none
	except:
		return None
	# If there exists at least 1 section that doesn't have a vertex, return None
	if(not (hasAmbulance and hasRegion and hasHospital)):
		return None

	# Handle the sink vertex, which will be the last element in the array
	vertexNames.append("Safety")
	sinkVertex = len(vertexNames)-1
	for i, e in enumerate(edges):
		if(e[1] == -2):
			edges[i][1] = sinkVertex

	# Return the n, f, e, v
	return (len(vertexNames), flowDemanded, edges, vertexNames)

# Define a means to process the graph given
def processGraph(vNum, fDemanded, edges, names):
	# Run the ford fulkerson algorithm on the graph and return the results
	flowSupplied, pathing = fordFulkerson(vNum, edges, 0, vNum-1)
	# Check to see if the network succeeded in saving all injured
	if(fDemanded == flowSupplied):
		print("Ambulatory Network can sustain all injured.")
		print("Quickly use the following routes:")
	# Check to see if the network could not sustain the injured amounts
	else:
		print("Ambulatory Network *cannot* sustain all injured.")
		print("To minimize loss of life, triage and use the following routes: ")
	# Print out the pathing
	for (injured, path) in pathing:
		print("\nSend %05d Injured Along: " % injured, end="")
		for i, route in enumerate(path[1:-1]):
			print("%s" % (names[route]), end="")
			if(i < len(path)-3):
				print(" -> ", end="")
		print()

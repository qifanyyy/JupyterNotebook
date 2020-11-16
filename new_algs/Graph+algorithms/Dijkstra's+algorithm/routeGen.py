#!/usr/bin/python
#Author: Torren Sampson 6/4/2018
#If this has been sent to anyone, feel free to use/modify it! Requires that you set up ship routes before hand... if you need your routes to 
#repeat a number of times, modify repeat to the desired value. 
#conduits.txt is the file given by the Professor
#routes.txt should be a file that has a single line for each ship like: ship planet planet planet planet.... separated by tabs The first planet in the route will be the first planet in each repeat.
#The layover at each planet is always 4. 
from collections import defaultdict

print("Reading in Conduits File...")
conduitsFile = open("conduits.txt", "r")
conduits = conduitsFile.readlines()
conduitsFile.close()
conduitDict = defaultdict(dict)
for line in conduits:
    lineTokens = line.split("\t")
    #print(lineTokens)
    conduitDict[lineTokens[0]][lineTokens[1]] = int(lineTokens[2][:-1])
    conduitDict[lineTokens[1]][lineTokens[0]] = int(lineTokens[2][:-1])
#print(conduitDict)
print("Generating shipt routes...")
routesFile = open("routes.txt", "r")
routes = routesFile.readlines();
routesFile.close();
routeTable = open("shipRouteTable.txt", "w")
for shipRoute in routes:
	shipTokens = shipRoute[:-1].split("\t")
	planets = shipTokens[2:]
	shipName = shipTokens[0]
	routeTime = 0
	previousPlanet = shipTokens[1]
	arrivalTime = 0
	x = 0
	repeat = 3
	for x in range(0, repeat):
		for planet in planets:
			arrivalTime = conduitDict[previousPlanet][planet] + routeTime
			routeTable.write(shipName + "\t" + previousPlanet + "\t" + str(routeTime) + "\t" + planet + "\t" + str(arrivalTime) + "\n")
			routeTime = arrivalTime + 4
			previousPlanet = planet
routeTable.close()
print("...Done! shipRouteTable.txt has been created!")
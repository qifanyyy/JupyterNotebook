#!/usr/bin/python
# ------------------------------------------------------------------------------
# dataset.py
# Authored by Max von Hippel on 28 March 2019
# The purpose of this script is to, in an unbiased manner, choose a very 
# impactful but reasonably sized data-set to study.
# ------------------------------------------------------------------------------
import sys
import re
from os.path import join, splitext, basename
from glob import glob
from itertools import combinations
from igraph import *
import cairo
from math import inf

# --------------------------------- SENSORS ------------------------------------
humanSensors = \
	{"button", "contact", "contactSensor", "estimatedTimeOfArrival", "geolocation", 
	"holdableButton", "motionSensor", "motion", "presenceSensor", "sleepSensor", 
	"speechRecognition", "speechSynthesis", "stepSensor", "tamperAlert",
	"touchSensor"}
motionSensors = \
	{"acceleration", "accelerationSensor", "beacon", "shockSensor", "threeAxis", "motion"}
soundSensors = \
	{"audiotrackdata", "soundPressureLevel", "soundsensor", "speechRecognition", 
	"speechSynthesis"}
airSensors = \
	{"airquality", "carbonDioxideMeasurement", "carbonmonoxidedetector", 
	"dustSensor", "filterStatus", "odorSensor", "relativeHumidityMeasurement",
	"smokeDetector"}
cyberSensors = \
	{"battery", "energyMeter", "polling", "powerConsumptionReport", "powerMeter",
	"powerSource", "signalStrength", "voltageMeasurement"}
lightSensors = \
	{"illuminanceMeasurement", "imageCapture", "ultravioletIndex", "videoClips",
	"videoStream", "infraredLevel"}
waterSensors = \
	{"pHMeasurement", "relativeHumidityMeasurement", "waterSensor"}
temperatureSensors =  \
	{"thermostat", "temperatureMeasurement",}.union(lightSensors)
sensorTypes = \
	{"sensor"}.union(humanSensors, motionSensors, soundSensors, airSensors,
		cyberSensors, lightSensors, waterSensors, temperatureSensors)

# -------------------------------- ACTUATORS -----------------------------------
humanActuators = \
	{"doorControl", "garageDoorControl", "lockOnly", "lock"}
motionActuators = \
	{"doorControl", "garageDoorControl", "robotCleanerCleaningMode", 
	"robotCleanerMovement", "robotCleanerTurboMode", "windowShade"}
soundActuators = \
	{"alarm", "mute", "audionotification", "audiovolume", "mediaController",
	"mediaInputSource", "mediaPlaybackRepeat", "mediaPlaybackShuffle",
	"mediaPlayback", "mediaPresets", "mediaTrackControl", "musicPlayer", 
	"notification", "tone", "tvChannel"}
airActuators = {}
cyberActuators = \
	{"execute", "bridge", "battery", "configuration", 
	"demandResponseLoadControl", "dishwasherMode", "dishwasherOperatingState",
	"dryerMode", "dryerOperatingState", "ovenSetpoint", "momentary", "outlet",
	"ovenMode", "ovenOperatingState", "refresh", "refrigerationSetpoint",
	"relaySwitch", "robotCleanerTurboMode", "switch", 
	"thermostatCoolingSetpoint", "thermostatFanMode", 
	"thermostatHeatingSetpoint", "thermostatMode", "thermostatOperatingState",
	"thermostatSetpoint", "timedSession", "tvChannel", "washerMode", 
	"washerOperatingState"}
lightActuators = \
	{"colormode", "bulb", "colorControl", "colorTemperature", "color", 
	"indicator", "light", "switchLevel", "tvChannel"}
waterActuators = {"valve", "washerMode", "washerOperatingState", "windowShade"}
temperatureActuators = \
	{"airconditioner", "fanSpeed", "rapidCooling", "thermostatCoolingSetpoint", 
	"thermostatFanMode", "thermostatHeatingSetpoint", "thermostatMode", 
	"thermostatOperatingState", "thermostatSetpoint"}
actuatorTypes = {"actuator"}.union(humanActuators, motionActuators, 
	soundActuators, airActuators, cyberActuators, lightActuators, 
	waterActuators, temperatureActuators)

combTypes = sensorTypes.union(actuatorTypes)

# ----------------------------------- CODE -------------------------------------
def sensorType(name):
	types = []
	if name in humanSensors:
		types.append('human')
	if name in motionSensors:
		types.append('motion')
	if name in soundSensors:
		types.append('sound')
	if name in airSensors:
		types.append('air')
	if name in cyberSensors:
		types.append('cyber')
	if name in lightSensors:
		types.append('light')
	if name in waterSensors:
		types.append('water')
	if name in temperatureSensors:
		types.append('temperature')
	return types

def actuatorType(name):
	types = []
	if name in humanActuators:
		types.append('human')
	if name in motionActuators:
		types.append('motion')
	if name in soundActuators:
		types.append('sound')
	if name in airActuators:
		types.append('air')
	if name in cyberActuators:
		types.append('cyber')
	if name in lightActuators:
		types.append('light')
	if name in waterActuators:
		types.append('water')
	if name in temperatureActuators:
		types.append('temperature')
	return types

# Input:
# app = path to the groovy file of a SmartThings app
# Output:
# (ins, outs) = ([list of input sensor channels], 
# 				 [list of output actuator channels])
def read_app(app):
	inputs  = []
	outputs = []
	began   = False
	with open(app, 'r') as file:
		for line in file:
			if "preferences" in line:
				began = True
			if began:
				options = re.findall(r'\"capability.(.*?)\"', line)
				sensors = [a for a in options if a in sensorTypes]
				actuators = [a for a in options if a in actuatorTypes]
				soptions = set(options)
				if not soptions.issubset(combTypes):
					print("Error: some capability was neither a sensor nor an actuator.")
					errors = [a for a in soptions if not a in combTypes]
					print(errors)
				inputs += sensors
				outputs += actuators
	return (inputs, outputs)


# Input:
# code_dir = the dir to look in
# Output:
# L = list of file paths
def find_all_code(code_dir):
	return glob(code_dir + '/**/*.groovy', recursive=True)

# Input:
# G = a igraph graph, in the format build in main() below
# Output:
# v = the value of the graph


# The main function
def main():
	# We expect arguments to be: N, dir
	(N, code_dir) = (int(sys.argv[1]), sys.argv[2])
	print("N = " + str(N) + "; code_dir = " + code_dir + "\n")
	
	files = find_all_code(code_dir)
	print("Found " + str(len(files)) + " files in code_dir\n")
	
	apps = [(file, read_app(file)) for file in files]
	print("Processed " + str(len(apps)) + " apps from the files found\n")

	# Draw the graph
	g = Graph(directed=True)
	gtypes = set()
	for (file, (ins, outs)) in apps:
		# add the app to the graph
		fname = basename(splitext(file)[0])
		# We don't really care about isolates
		if (not ins) and (not outs):
			continue
		g.add_vertex(name 		 = file,  \
					 type 		 = 'app', \
					 color 		 = 'red', \
					 label 		 = fname, \
					 label_color = 'red')
		for i in ins:
			filtered = sensorType(i)
			if not filtered:
				print("Error: filtered is empty but i = " + str(i))
			for f in filtered:
				if not f in gtypes:
					gtypes.add(f)
					g.add_vertex(name 		 = f, 		  \
								 type 		 = 'channel', \
								 color 		 = 'blue',    \
								 label 		 = f,		  \
								 label_color = 'blue')
				g.add_edge(f, file, color='green', label=i)
		for o in outs:
			filtered = actuatorType(o)
			if not filtered:
				print("Error: filtered is empty but i = " + str(o))
			for f in filtered:
				if not f in gtypes:
					gtypes.add(f)
					g.add_vertex(name 		 = f, 		  \
								 type 		 = 'channel', \
								 color 		 = 'blue', 	  \
								 label 		 = f, 		  \
								 label_color = 'blue')
				g.add_edge(file, f, color='orange', label=o)

	p = plot(g, 								   \
			 target			   = 'graph.png',	   \
			 layout			   = g.layout("kk"),   \
			 bbox			   = (1800, 1800), 	   \
			 vertex_label_dist = 3, 			   \
			 margins		   = (30, 30, 30, 30))
	p.save("graph.png")
	
	# Find the best subgraph
	vs = filter(lambda v : v['type'] == 'app', g.vs) # Get the app vertices
	vs = map(lambda v : v['name'], vs) 				 # Get the vertex names
	bests = []
	best_value = 0
	for combo in combinations(vs, N): 				 # Get the combos
		value = 0
		for (a, b) in combinations(combo, 2):
			path1 = g.shortest_paths_dijkstra(source = a, \
											    target = b)
			path2 = g.shortest_paths_dijkstra(source = b, \
											    target = a)
			if path1[0][0] != inf:
				value += (len(path1)/path1[0][0])
			if path2[0][0] != inf:
				value += (len(path2)/path2[0][0])

		if best_value == value:
			bests.append(combo)
		elif best_value < value:
			bests = [combo]
			best_value = value
	
	print("Best value = " + str(best_value))
	i = 1
	for best in bests:
		print("Solution #" + str(i))
		for f in best:
			print("File name: " + f)
			sensors = [z.attributes()['label'] for z in g.es \
					   if z.target == g.vs.find(name=f).index]
			print("Sensor channels: " + ", ".join(sensors))
			actuators = [z.attributes()['label'] for z in g.es \
						 if z.source == g.vs.find(name=f).index]
			print("Actuator channels: " + ", ".join(actuators))
		i += 1
		print("_________________________________________________________")

if __name__ == '__main__':
	main()
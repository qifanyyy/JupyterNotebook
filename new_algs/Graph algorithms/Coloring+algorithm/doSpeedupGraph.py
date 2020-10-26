import json
import sys
from math import ceil
import matplotlib.pyplot as plt
import numpy as np

# Draws execution time and speed-up index graphs
# Feed me a json file in the 'Old' format (fixed density)

def drawTime( avgTime, prob ):
	x = []
	yLuby = []
	yMCPU = []
	yMGPU = []
	yMCPUiter = []
	yMGPUiter = []
	yLubyiter = []

	for elem in avgTime:
		if elem["prob"] == prob:
			x.append( elem["n"] )
			yLuby.append( elem["Luby"] )
			yMCPU.append( elem["MCMC_CPU"] )
			yMGPU.append( elem["MCMC_GPU"] )
			yLubyiter.append( elem["MCMC_CPUiter"] )
			yMCPUiter.append( elem["MCMC_CPUiter"] )
			yMGPUiter.append( elem["MCMC_GPUiter"] )

	x = np.array( x )
	yLuby = np.array( yLuby )
	yMCPU = np.array( yMCPU )
	yMGPU = np.array( yMGPU )
	yMCPUiter = np.array( yMCPUiter )
	yMGPUiter = np.array( yMGPUiter )
	yLubyiter = np.array( yLubyiter )

	ii = np.argsort( x )
	x = x[ii]
	yLuby = yLuby[ii]
	yMCPU = yMCPU[ii]
	yMGPU = yMGPU[ii]
	yMCPUiter = yMCPUiter[ii]
	yMGPUiter = yMGPUiter[ii]
	yLubyiter = yLubyiter[ii]

	# Convert x in string: 25000 -> 25k
	xlabels = [str(ceil(a / 1000)) + 'k' for a in x]

	fig = plt.figure()
	plt.plot( x, yLuby, label='Luby', color='b', linestyle='-', marker='o' )
	plt.plot( x, yMCPU, label='MCMC CPU', color='g', linestyle='-', marker='o' )
	plt.plot( x, yMGPU, label='MCMC GPU', color='r', linestyle='-', marker='o' )
	plt.legend()
	plt.grid(True)
	plt.xticks( x, labels = xlabels )
	plt.xlabel( 'Nodes' )
	plt.ylabel( 'Time (s)' )
	plt.title('Execution time - Prob. ' + str( prob ))
	plt.show()

	# speed-up
	Tluby_Tgpu = np.true_divide(yLuby, yMGPU)
	Tcpu_Tgpu = np.true_divide(yMCPU, yMGPU)
	fig2 = plt.figure()
	plt.plot( x, Tluby_Tgpu, label='Luby / MCMC GPU', color='b', linestyle='-', marker='o' )
	plt.plot( x, Tcpu_Tgpu, label='MCMC CPU / MCMC GPU', color='g', linestyle='-', marker='o' )
	plt.legend()
	plt.grid(True)
	plt.xticks( x, labels = xlabels )
	plt.xlabel( 'Nodes' )
	plt.ylabel( 'Speed-up' )
	plt.title('Speed-up (Overall exec time)- Prob. ' + str( prob ))
	plt.show()

	yLubybal = np.true_divide( yLuby, yLubyiter )
	yMCPUbal = np.true_divide( yMCPU, yMCPUiter )
	yMGPUbal = np.true_divide( yMGPU, yMGPUiter )

	# speed-up rebalanced over iteration number
	Tluby_Tgpu = np.true_divide(yLubybal, yMGPUbal)
	Tcpu_Tgpu = np.true_divide(yMCPUbal, yMGPUbal)
	fig2 = plt.figure()
	plt.plot( x, Tluby_Tgpu, label='Luby / MCMC GPU', color='b', linestyle='-', marker='o' )
	plt.plot( x, Tcpu_Tgpu, label='MCMC CPU / MCMC GPU', color='g', linestyle='-', marker='o' )
	plt.legend()
	plt.grid(True)
	plt.xticks( x, labels = xlabels )
	plt.xlabel( 'Nodes' )
	plt.ylabel( 'Speed-up' )
	plt.title('Speed-up (per iteration) - Prob. ' + str( prob ))
	plt.show()


def doSpeedupGraph( filenm ):
	with open( filenm, "r" ) as read_file:
		dataFromJson = json.load( read_file )

	avgTime = []

	for exp in dataFromJson:
		tempDict = {
			"n":    dataFromJson[exp]["graphs"][0]["nNodes"],
			"prob": dataFromJson[exp]["graphs"][0]["edgeProb"],
			"Luby": dataFromJson[exp]["Luby"]["Avg"]["execTime"],
			"MCMC_CPU": dataFromJson[exp]["MCMC_CPU"]["Avg"]["execTime"],
			"MCMC_GPU": dataFromJson[exp]["MCMC_GPU"]["Avg"]["execTime"],
			"Lubyiter": dataFromJson[exp]["Luby"]["Avg"]["numColors"],
			"MCMC_CPUiter": dataFromJson[exp]["MCMC_CPU"]["Avg"]["performedIter"],
			"MCMC_GPUiter": dataFromJson[exp]["MCMC_GPU"]["Avg"]["performedIter"],
		}
		avgTime.append( tempDict )

	drawTime( avgTime, 0.001 )
	drawTime( avgTime, 0.005 )
	# prob 0.001


if __name__ == '__main__':
	filename = sys.argv[1]

	doSpeedupGraph( filename )

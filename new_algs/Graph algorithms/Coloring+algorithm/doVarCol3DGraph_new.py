import json
import sys
import os
from math import ceil, sqrt
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib import cm
import numpy as np
from mpl_toolkits import mplot3d

# Draws balancing indexes for differnt colorRatios and densities
# Feed me a json file in the 'New' format (variable density)

def balIdxEval( clusters, mu, k ):
	balIdx = 0
	for nodesInColor in clusters:
		balIdx += ((nodesInColor - mu) * (nodesInColor - mu))
	balIdx /= k
	return sqrt( balIdx )

def calcAvgBalIdx( cat, k, mu ):
	balIdxs = []
	for rip in cat["Exp"]:
		balIdxs.append( balIdxEval(rip["colorClusters"], mu, k) )
	return sum(balIdxs) / float( len(balIdxs) )



def readDataFromJson( baseDir ):
	s = os.sep
	basePath = baseDir
	subDir = os.listdir( basePath )
	finalDict = []
	for currDir in subDir:
		density = int( currDir )
		with open( basePath + s + currDir + s + "finalRes.json", "r" ) as read_file:
			dataFromJson = json.load( read_file )
			for colorRatio in dataFromJson:
				avg_MCPU = []
				avg_MGPU = []
				avg_Luby = []
				for exp in dataFromJson[colorRatio]:
					#print(currDir + " " + str(colorRatio) + " " + str(exp["edgeProb"]))
					n = exp["nNodes"]
					p = exp["edgeProb"]
					k = n * p * float( colorRatio )
					mu = n / k
					avg_MCPU.append( calcAvgBalIdx( exp["MCMC_CPU"], k, mu ) )
					avg_MGPU.append( calcAvgBalIdx( exp["MCMC_GPU"], k, mu ) )
					avg_Luby.append( calcAvgBalIdx( exp["Luby"], k, mu ) )

					finalDict.append( {
						"colorRatio": colorRatio,
						"density": density,
						"nNodes": n,
						"edgeProb": p,
						"avg_MCPU": sum(avg_MCPU) / float( len(avg_MCPU) ),
						"avg_MGPU": sum(avg_MGPU) / float( len(avg_MGPU) ),
						"avg_Luby": sum(avg_Luby) / float( len(avg_Luby) )
					} )

	print( len(finalDict) )
	return finalDict

def sortDict( resList ):
	#print( len(resList) )
	probs = set()
	for res in resList:
		probs.add(res["edgeProb"])
	probList = list(probs)
	probList.sort()


def draw3Dgraph( resList ):
	# x = []
	# y = []
	# z = []
	# for res in resList:
	# 	x.append(res["colorRatio"])
	# 	y.append(res["density"])
	# 	z.append(res["avg_Luby"])
	#
	# x = np.array( x )
	# y = np.array( y )
	# z = np.array( z )
	# ix = np.argsort( x )
	# iy = np.argsort( y )

	X = np.arange(-5, 5, 0.25)
	Y = np.arange(-5, 5, 0.25)
	print(Y)
	print( len(X) )
	print( len(Y) )
	X, Y = np.meshgrid(X, Y)
	R = np.sqrt(X**2 + Y**2)
	Z = np.sin(R)
	print(Y)

	print( len(X) )
	print( len(Y) )
	print( len(Z) )

	fig = plt.figure()
	ax = fig.gca(projection='3d')

	surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)

	ax.set_zlim(-1.01, 1.01)
	ax.zaxis.set_major_locator(LinearLocator(10))
	ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

	# Add a color bar which maps values to colors.
	fig.colorbar(surf, shrink=0.5, aspect=5)

	plt.show()


	# fig = plt.figure()
	# ax = plt.axes( projection='3d' )
	# plt.show()




if __name__ == '__main__':
	filename = sys.argv[1]
	dataFromDirs = readDataFromJson( filename )
	# print( dataFromDirs )
	#draw3Dgraph( dataFromDirs )
	sortDict( dataFromDirs )

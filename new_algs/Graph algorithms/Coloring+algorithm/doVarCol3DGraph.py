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
					"avg_MCPU": sum(avg_MCPU) / float( len(avg_MCPU) ),
					"avg_MGPU": sum(avg_MGPU) / float( len(avg_MGPU) ),
					"avg_Luby": sum(avg_Luby) / float( len(avg_Luby) )
				} )

	return finalDict

def draw3Dgraph( resList ):
	xset = set()
	yset = set()
	for res in resList:
		xset.add(float(res["colorRatio"]))
		yset.add(int(res["density"]))
	xlst = list(xset)
	ylst = list(yset)

	xlst.sort()
	ylst.sort()
	xsize = len(xlst)
	ysize = len(ylst)
	print(xlst)
	print(ylst)

	X, Y = np.meshgrid(xlst, ylst)
	Z = np.array(X, copy=True)
	Z2 = np.array(X, copy=True)

	for i in range(0,xsize):
		for j in range(0,ysize):
			#print (str(X[j][i]) + " " + str(Y[j][i]))
			for res in resList:
				if (float(res["colorRatio"]) == X[j][i]) and (int(res["density"]) == Y[j][i]):
					Z[j][i] = float(res["avg_Luby"])
					Z2[j][i] = float(res["avg_MGPU"])

	# for res in resList:
	# 	print(str(res["colorRatio"]) + " " + str(res["density"]) + " " + str(res["avg_Luby"]) )
	# print(X)
	# print(Y)
	# print(Z)


	fig = plt.figure()
	ax = fig.gca(projection='3d')
	surf = ax.plot_surface(X, Y, Z, cmap=cm.winter, linewidth=0, antialiased=True)
	ax.set_xlabel('Color reduction')
	ax.set_ylabel('Density')
	ax.set_zlabel('Balancing Index')
	ax.legend()
	cbar  = fig.colorbar(surf, shrink=0.5, aspect=5)
	cbar.set_label('Luby')
	plt.show()

	fig = plt.figure()
	ax = fig.gca(projection='3d')
	surf2 = ax.plot_surface(X, Y, Z2, cmap=cm.autumn, linewidth=0, antialiased=True)
	ax.set_xlabel('Color reduction')
	ax.set_ylabel('Density')
	ax.set_zlabel('Balancing Index')
	ax.legend()
	cbar2 = fig.colorbar(surf2, shrink=0.5, aspect=5)
	cbar2.set_label('MCMC GPU')

	plt.show()




if __name__ == '__main__':
	filename = sys.argv[1]
	dataFromDirs = readDataFromJson( filename )
	# print( dataFromDirs )
	draw3Dgraph( dataFromDirs )

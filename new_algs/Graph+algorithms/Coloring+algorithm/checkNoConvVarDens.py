import json
import sys

def listNoConv( filename ):
	with open( filename, "r" ) as read_file:
		dataFromJson = json.load( read_file )

	countCpu = 0
	countGpu = 0

	for grp in dataFromJson:
		for exp in dataFromJson[grp]:
			for expCPU in exp["MCMC_CPU"]["Exp"]:
				if not expCPU["convergence"]:
					#print( expCPU )
					print( "CPU - " + grp + " - " + str( exp["nNodes"] ) +  " - " + str( exp["edgeProb"] ))
					countCpu += 1

	for grp in dataFromJson:
		for exp in dataFromJson[grp]:
			for expGPU in exp["MCMC_GPU"]["Exp"]:
				if not expGPU["convergence"]:
					#print( expGPU )
					print( "GPU - " + grp + " - " + str( exp["nNodes"] ) + " - " + str( exp["edgeProb"] ))
					countGpu += 1

	print( "{} non convergent experiments in MCMC_CPU".format(countCpu) )
	print( "{} non convergent experiments in MCMC_GPU".format(countGpu) )


if __name__ == '__main__':
	filename = sys.argv[1]

	listNoConv( filename )

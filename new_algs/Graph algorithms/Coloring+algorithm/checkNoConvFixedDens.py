import json
import sys

def listNoConv( filename ):
	with open( filename, "r" ) as read_file:
		dataFromJson = json.load( read_file )

	countCpu = 0
	countGpu = 0

	for exp in dataFromJson:
		for expCPU in dataFromJson[exp]["MCMC_CPU"]["Exp"]:
			if not expCPU["convergence"]:
				print( expCPU )
				countCpu += 1

	for exp in dataFromJson:
		for expGPU in dataFromJson[exp]["MCMC_GPU"]["Exp"]:
			if not expGPU["convergence"]:
				print( expGPU )
				countGpu += 1

	print( "{} non convergent experiments in MCMC_CPU".format(countCpu) )
	print( "{} non convergent experiments in MCMC_GPU".format(countGpu) )


if __name__ == '__main__':
	filename = sys.argv[1]

	listNoConv( filename )

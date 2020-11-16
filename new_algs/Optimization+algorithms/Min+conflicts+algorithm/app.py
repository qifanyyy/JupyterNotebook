#http://modelai.gettysburg.edu/2016/pyconsole/ex3/index.html
import visualize as v
import os
import numpy as np
import Simulated_Annealing
from random import randint
from Board import chessBoard
import MinConflicts as mc
from argparse import ArgumentParser

global p

#Create Initial State (randomized)
#Returns a line vector (size of N) in order to create a board
#In each cell (iterate on columns) we store the row possition of the queen
#E.g if queens are in main diagonal for N=5, then the func will return qCols=[0,1,2,3,4]
def create_Istate(Psize):
	# Create random Positions
	colIndex = range(0, Psize)
	# print(colIndex)
	i = 0
	qCols = []
	# print('Randomizing Queen Column Position...')
	while i < Psize and len(colIndex) > 0:
	    index = randint(0, len(colIndex)-1)
	    qCols.append(colIndex[index])
	    colIndex.pop(index)
	return qCols

# Function in order to create an image of the solution given of the algorithms
def create_image(Psize,action,sol,TC=0):
	# create folder SA/MC for saving SA's/MC's solutions
	fold="SA/" if action=='SA' else "MC/"
	directory="Images/"+fold+str(Psize)+"-Queens/"
	if not os.path.exists(directory):
		os.makedirs(directory)
	v.FilePath=directory #Pass directory
	v.Tcols=sol.Tconflicts if action=='SA' else TC #Pass Total Colisions
	grid=sol.prepareForVisualize() if action=='SA' else sol # Prepare line vector (each cell contains the row possiton for each queen)
	v.ShowQueens(grid) #create and store image

#Successor Function takes 3 arguments
#	Istate : Initial State which the algorithm begins
#	Psize : Problem Size
#	action : SA for solving with Simulated Anealing or MC for Min Conflicts
# For each case we initialize the variables that need to be initialized for the algorithm
# and then we call the successor func in which we start solving the problem
def successor_function(Istate,Psize,action):
	if action=='SA':
		#initializing variables needed for SA algorithm
		alpha=0.999
		Iterations = 10000
		Temperature=100#Iterations*10 #if Temperature is high it means how easy we accept a solution
		# create the object
		sa = Simulated_Annealing.simulatedAnnealing()
		# Start Solving
		# Returns > iters : Iterations until finding a solution (if found)
		# 		  > sol : final state of the problem (the solution if problem was solved)
		# 		  > time : time calculating the solution
		iters, sol, time,confl,stop_iter =sa.successor_function_SA(alpha, Iterations, Temperature,Istate,Psize)
		#log(Iterations,Psize,action,confl,time) #write to an output file
		sol.printBoard() # Print Solution
		print('Runtime is {:.4f}'.format(time)) # Print time needed for calculating solution
		create_image(Psize,'SA',sol) # Create and save image in spesific folder
	 	#p=[Iterations,Psize,action,confl,time,stop_iter]
		#return(p)
	elif (action=="MC"):
		sol,time,colisions,l = mc.successorFunction(Istate, Psize)
		boardMC=chessBoard(Psize,True)
		boardMC.createBoard(sol)
		boardMC.printBoard()
		boardMC.checkForConflicts()
		print('Runtime is {:.4f}'.format(time)) # Print time needed for calculating solution
		create_image(Psize,'MC',sol,boardMC.Tconflicts) # Create and save image in spesific folder
		#log(l,Psize,action,colisions,time)
		#p=[l,Psize,action,colisions,time,l] #create array 4 return values
		#return(p2)
	else:
		print ('We support only the Simulated Anealing (SA) and Min Conflicts (MC) algorithms ')
	return(p)
##Writting output to file-- its used for benchmarks
def log(loops,N,func,hits,ex_time,stop_iter):
	with open("Out.txt",'a+') as f:
		output="*(MAX_Loops= "+str(loops)+")/"+"|[" +str(stop_iter) +"]| "+ str(N)+", "+str(func)+"| hits= "+str(hits)+"| ex_time= "+str(ex_time*1000)+"ms"+"\n" #sizeProblem, algorith,hits or conflicts
		f.write(output)
		f.write("---------------------------------------------------------------------------------------------------------------------*\n")
		#f.write() #data hits, time
	f.close()

def main():
	parser = ArgumentParser()
	parser.add_argument('N', type=int,
						help="Problem size", metavar="N")
	parser.add_argument("Algorithm", default='SA',type=str,
						help="SA or MC algorithm")

	args = parser.parse_args()

	Initial_state=create_Istate(args.N)
	successor_function(Initial_state,args.N,args.Algorithm)
	#mean_conflicts=mean_exec=mean_loops=0 #m
	#evaluete the performance for each sizeProblem
	# for i in range(10):
	# 	p=successor_function(Initial_state,args.N,args.Algorithm)
	# 	mean_loops+=p[5]
	# 	mean_exec+=p[4]
	# 	mean_conflicts+=p[3]
	# mean_loops=mean_loops/10
	# mean_exec=mean_exec/10
	# mean_conflicts=mean_conflicts/10
	# log(p[0],p[1],p[2],mean_conflicts,mean_exec,mean_loops) #write then mean values



if __name__ == "__main__":
    main()

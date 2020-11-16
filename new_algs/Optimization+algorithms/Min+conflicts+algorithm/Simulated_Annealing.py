from random import randint, random
from copy import deepcopy
import math
from collections import namedtuple
import time
from Board import chessBoard


class simulatedAnnealing(object):

    global size
    global alpha
    global Iterations
    global T0

    global tryBoard
    global mainboard

    #Constructor
    def __init__(self):
    	pass


    #This basically exchanges the available columns  by just using a random position
    def heuristicExchange(self):
        #Get the random positions for exchange
        pos1 = randint(0,self.size-1)
        pos2 = randint(0,self.size-1)

        # Deep-Copy the objects
        tryBoard = deepcopy(self.mainboard)

        #Now exchange the columns
        tryBoard.qCols[pos1] = self.mainboard.qCols[pos2];
        tryBoard.qCols[pos2] = self.mainboard.qCols[pos1];
        tryBoard.updateBoard()

        tryBoard.checkForConflicts()

        return tryBoard


    #This functions creates the main board for us (in silent mode)
    def createSolutionBoard(self,state):
        self.mainboard = chessBoard(self.size, True)
        self.mainboard.createAndEvalBoard(False,state)


    #This function is responsible for finding a solution
    def searchSolution(self,state):
        self.createSolutionBoard(state)

        iterations = 0
        T = self.T0

        while (iterations < self.Iterations and self.mainboard.Tconflicts != 0):
            self.tryBoard = self.heuristicExchange()

            #Check if we found a better solution
            if(self.tryBoard.Tconflicts < self.mainboard.Tconflicts):
                #copy tryBoard to mainboard
                self.mainboard = self.tryBoard
            else:
                # This is Simulated Annealing property, based on a random value r
                # and the exponential difference of total differences of each of the
                # two boards divided by the current temperature gives us the probability
                # of exchanging the 'false' solution with the 'good'
                r = random()

                try:
                    p = float((self.mainboard.Tconflicts - self.tryBoard.Tconflicts ) / T)
                    power =  math.pow(math.e, p)
                    if(r < power):
                        self.mainboard = deepcopy(self.tryBoard)
                except OverflowError:
                    pass

            iterations += 1
            T *= self.alpha


        print('\nSA Stats:\n\tIterations: ' + str(iterations) + " out of: " + str(self.Iterations) + "\n\tCurrent Temperature: " + str(self.T0-T))
        print('\n\tTotal Collisions (so far): ' + str(self.mainboard.Tconflicts) + '\n\t' + str(('We did not find a solution','We found a solution')[self.mainboard.Tconflicts == 0]))

        return (iterations, (0,1)[self.mainboard.Tconflicts == 0],self.mainboard.Tconflicts,iterations)



    # This is a N-Queen solver function that uses the Simulated Annealing
    # probabilistic algorithm in order to find a solution to the problem.
    def simulatedAnnealing(self, N_Queens, alpha, Iter,T0,state):
        #    Parameter Initialization
        self.size = N_Queens
        self.alpha = alpha
        self.Iterations = Iter
        self.T0=T0;

       # Print our parameters
        print('\nStarting Simulated Annealing for N-Queens problem with parameters:')
        print('\t Queens(N): ' + str(N_Queens)+',\t\talpha: ' + str(alpha)+'\n\tIterations: ' + str(Iter)+',\tTemperature: ' + str(T0))

        start_time = time.time()
        (iterations, solution_flag,conflicts,stop_iter) = self.searchSolution(state)
        end_time = time.time()
        totalT = end_time-start_time

        # self.mainboard.printBoard()
        #In this function we return the follow variables:
        #> iterations : iterations needed in order to find a solution
        #> mainboad : the solution tha we found, if exists, or the state we got to be in the last iteration
        #> flag : flag helps us know if we found a solution (it is uses in order to calculate the row matrix and project it using the gui)
        #> totalT : total time needen it in order to find a solution or to terminate with out finding a solution
        return (iterations, self.mainboard, totalT,conflicts,stop_iter)

    def successor_function_SA(self,alpha, Iterations, Temperature,state,size_probelm):
        iters, sol, time,confl,stop_iter=self.simulatedAnnealing(size_probelm, alpha, Iterations, Temperature,state)
        return iters, sol, time,confl,stop_iter




# sa = simulatedAnnealing()
# itr,sol,flag,time=sa.simulatedAnnealing(8, 0.999, 10, 10*10)
# sol.printBoard()
# print(flag)
# print (time)

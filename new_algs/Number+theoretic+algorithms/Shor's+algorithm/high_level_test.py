import numpy as np
#from dense import *
from sparse import *
import InOut as IO
import time
from fractions import Fraction


import matplotlib.pyplot as plt



def extendedGCD(x,y):
	#Returns array representing continued fraction expansion of x/y
	fracs = []
	if x==y:
		return fracs
	while(y):
		fracs.append(x//y)
		x,y = y,x%y
	return np.array(fracs)



def main():
	
<<<<<<< Updated upstream
	H = Hadamard(6)
	N = Noisy(H,0)
	#IO.display(Noisy(H,1))
	#IO.display(Noisy(H,0.1)*Noisy(H,0.1))
	IO.display(N)
=======
	
	#q1 = Qubit([1,1j])
	#q1.normalise()
	#IO.Hist(q1)
	#print(q1.measure())
	IO.Display(Hadamard())
	#H = Hadamard(4)
	#N = Noisy(H,0)
	#IO.Display(Noisy(H,1))
	#IO.Display(Noisy(H,0.1)*Noisy(H,0.1))
	#q = Qubit(4)
	#IO.Hist(q)
	#IO.Hist(H*q)
>>>>>>> Stashed changes
main()
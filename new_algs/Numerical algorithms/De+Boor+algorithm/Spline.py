from scipy import *
from scipy.linalg import *
import numpy as np

import matplotlib.pyplot as plt

class Spline(object):
	def __init__(self, gridpoints, coeff):
		self.gp = np.array(gridpoints)
		self.coeff = np.array(coeff)

	def __call__(self, u):
		#Find the hot interval
		i = (self.gp > u).argmax()
		
		#Call recursive blossom algorithm
		return self.blossoms(i, u, 3)

	@classmethod
	def by_points(cls, x, y, gridpoints):
		gp = gridpoints

		xLen = len(x)
		yLen = len(y)
		assert(len(gp) == xLen + 2)
		assert(xLen == yLen) #x and y need to be same size
		assert (gp[0] == gp[1] and gp[1] == gp[2] and gp[-1] == gp[-2] and gp[-2] == gp[-3]) #multiplicity 3 on gridpoints
		m = np.zeros((xLen, yLen)) #initialize matrix
		xi = []
		for i in range(xLen): #create Matrix for linear system to compute deBoor points
			N = cls.get_N_i_3(i, gp)
			for j in range(yLen):
				if (i == 0):
					xi.append((gp[j] + gp[j+1] + gp[j+2])/3) #store values for faster access
				m[j][i] = N(xi[j])[0]

		#Solve banded needs matrix mbs to be in this form
		mbs = np.zeros((5, xLen)) #5 = 2 + 2 + 1 = u + l + 1
		for i in range(5): 
			for j in range(xLen):
				if (i - 2 + j < 0) or (i - 2 + j >= xLen):
					mbs[i, j] = 0
				else:
					mbs[i, j] = m[i - 2 + j, j]
		
		#np.set_printoptions(precision=3, suppress=True)
		#print(m)
		#print('\n')
		#print(mbs)
		dx = array(solve_banded((2, 2), mbs, x)) #m is banded with bandwidth <4
		dy = array(solve_banded((2, 2), mbs, y))
		
		return cls(gridpoints, np.column_stack((dx, dy)))

	def blossoms(self, i, u, depth):
		if (depth == 0):
			#Base case
			return np.array(self.coeff[i])
		else:
			#Get current alpha
			a = self.alpha(i, u)
			#Call recursion according to alpha*d[...] + (1 - alpha)*d[...]
			return a * self.blossoms(i - 1, u, depth - 1) + (1 - a) * self.blossoms(i, u, depth - 1)
	
	@classmethod
	def get_N_i_3(cls, i, gridpoints):
		coeff = np.array([np.array((1, 1)) if i == j else np.array((0, 0)) for j in range(len(gridpoints) - 2)])
		return cls(gridpoints, coeff)
	
	@classmethod
	def get_N(cls, i, k, gridpoints):
		gp = gridpoints
		if (k == 0):
			#N(i, 0)(u), lowest recursive depth
			if (i < 0):
				i = 0;
			if (i >= len(gp)):
				i = len(gp) - 1
			if (gp[i - 1] == gp[i]):
				return (lambda u: 0)
			else:
				return (lambda u: 1 if (gp[i - 1] <= u < gp[i]) else 0)
		else:
			#Recursion for N(i, k)(u) according to formula
			iminus1 = i - 1
			if (iminus1 < 0):
				iminus1 = 0
			iplusk = i + k
			if (i + k >= len(gp)):
				iplusk = len(gp) - 1
			d1 = (gp[iplusk-1] == gp[iminus1])
			d2 = (gp[iplusk] == gp[i])
			
			return (lambda u: cls.div(u - gp[iminus1], gp[iplusk-1] - gp[iminus1]) * cls.get_N(i, k - 1, gp)(u) +
					cls.div(gp[iplusk] - u, gp[iplusk] - gp[i]) * cls.get_N(i + 1, k - 1, gp)(u))
	
	@classmethod
	def div(cls, num, denom):
		if (num == 0 and denom == 0):
			return 0
		elif denom == 0:
			return 1 #return is whatever, since term will be 0 anyway
		else:
			return num/denom
		
	def alpha(self, i, u):
		gp = self.gp
		#Return alpha according to formula

		if (gp[i+2] == gp[i-1]):
			return 0
		else:
			return (gp[i+2] - u)/(gp[i+2]-gp[i-1])

	def f_range(self,start, stop, step):
		# implementing range() for float type numbers
		i = start
		while i <= stop:
			yield i
			i += step

	def plot(self, h=0.1, dbp = 1): #h is step size, dbp check if you want de Boor points and Control Polygon
		gp = self.gp
		# Generating a list of all evaluation points
		gph = list(self.f_range(gp[0],gp[-1],h))
		evalugph = [self(u) for u in gph]
	   
		if dbp == 1:
			zipcoeff = self.coeff
			plt.plot(list(zipcoeff[:,0]),list(zipcoeff[:,1]), marker='+')
                evalX = [x[0] for x in evalugph]
                evalY = [x[1] for x in evalugph]
                plt.plot(evalX, evalY)
		plt.show()  
		return (evalX, evalY)

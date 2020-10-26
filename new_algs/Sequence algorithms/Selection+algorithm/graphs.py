import random
import matplotlib.pyplot as plt
import numpy as np


def linear_ranking_prob(N, selection_pressure, i):
 return ( selection_pressure - ( (2*(selection_pressure-1)) * float(i-1)/(N-1) ) ) / N

def exponential_ranking_prob(N, selection_pressure, i):
 return (selection_pressure**(i-1)) * float(1-selection_pressure)/float(1-selection_pressure**N)

def f(j,i):
 return j + float(i-1)/j

def g(x):
 return x*x

def weighted_choice(choices):
 totals = [] 
 running_total = 0
 
 for w in choices:
  running_total += w
  totals.append(running_total)

 rnd = random.random() * running_total
 for ii, total in enumerate(totals):
  if rnd < total:
   return ii

###
n = 10
N=10
SP = 0.9
selection_pressure = 0.05
x = np.array(range(1,11))
plt.plot(x, ((selection_pressure**(x-1)) * float(1-selection_pressure)/float(1-selection_pressure**N)), linestyle='-', marker='o')
plt.plot(x, linear_ranking_prob(n, 1.0, x), linestyle='-', marker='o')
#plt.plot(x, 1.0/x*x*x, linestyle='-', marker='o')
plt.axis([0,len(x)+1,0,1.0])
plt.xlabel('Individuals rank')
plt.ylabel('Selection probability value')
plt.grid(True)
plt.show()


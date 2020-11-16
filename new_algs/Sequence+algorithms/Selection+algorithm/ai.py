from random import random, uniform
from math import sin, sqrt, exp
import matplotlib.pyplot as plt
from operator import attrgetter
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time

offset = 1500

# function domain
min_domain = -512
max_domain = 512
mutation_pass = 10

class Antibody:
	def __init__(self, x1, x2, affinity,num_clones):
		self.x1 = x1
		self.x2 = x2
		self.affinity = affinity
		self.num_clones = 0

# function eggholder
def eggholder(x1, x2):
	affinity = -(x2+47)*np.sin(np.sqrt(np.abs(x2+x1/2+47)))-x1*np.sin(np.sqrt(np.abs(x1-(x2+47))))
	affinity = -affinity+offset
	return affinity

# function of update data
def update_line(hl, new_data):
    hl.set_xdata(new_data)
    hl.set_ydata(new_data)
    hl.set_zdata(new_data)
    plt.draw()

# define population list
def generate_population(pop_size):
	population = []
	for i in range(0,pop_size):
		antibody = Antibody(uniform(min_domain,max_domain),uniform(min_domain,max_domain),0,0)
		population.append(antibody)
	return population

# generate affinity value for every antibody in population
def affinity(population):
	global offset
	for c in population:
		c.affinity = -(c.x2+47)*sin(sqrt(abs(c.x2+c.x1/2+47)))-c.x1*sin(sqrt(abs(c.x1-(c.x2+47))))
		c.affinity = -c.affinity+offset
	return population	

def cloning(population,max_num_clones):
	# generating num_clones clones for every antibody available
	clones = []
	for antibody in population:
		tmp = antibody.affinity-500
		fator = tmp/2000
		num_clones = max(1, int(fator*max_num_clones))
		antibody.num_clones = num_clones
		for i in range(0,num_clones):
			clones.append(antibody)
	return clones

def mutation(population,ro):
	global max_domain
	global min_domain
	max_affinity = max(population,key=attrgetter('affinity')).affinity
	for c in population:
		d_star = c.affinity/max_affinity
		mutation_rate = exp(-ro*d_star)
		if(random() < mutation_rate):
			mutated_value = c.x1+uniform(-mutation_pass,mutation_pass)
			if(not(mutated_value < min_domain)):
				c.x1 = mutated_value
			else:
				c.x1 = min_domain
			if(not(mutated_value > max_domain)):
				c.x1 = mutated_value
			else:
				c.x1 = max_domain

		if(random() < mutation_rate):
			mutated_value = c.x2+uniform(-mutation_pass,mutation_pass)
			if(not(mutated_value < min_domain)):
				c.x2 = mutated_value
			else:
				c.x2 = min_domain
			if(not(mutated_value > max_domain)):
				c.x2 = mutated_value
			else:
				c.x2 = max_domain
		c.x1 = max(min_domain, c.x1)
		c.x1 = min(max_domain, c.x1)
		c.x2 = max(min_domain, c.x2)
		c.x2 = min(max_domain, c.x2)
	return population

def selection(clone_population, num_clones, population):
	new_population = []
	c = 0
	for antibody in population:
		cluster = []
		for i in range(antibody.num_clones):
			cluster.append(clone_population[c])
			c += 1
		new_population.append(max(cluster,key=attrgetter('affinity')))

	return new_population

def print_population(population):
	for c in population:
		print(str(c.x1)+" "+str(c.x2)+" affinity: "+str(c.affinity))

pop_size = 70
ro = 2
num_clones = 5
population = generate_population(pop_size)
iterations = 500

# plot for statistical analysis
x1 = np.linspace(-512, 512)
x2 = np.linspace(-512, 512)
x1, x2 = np.meshgrid(x1, x2)
z = eggholder(x1, x2);

#ax = plt.gca()
fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
ax = fig.add_subplot(111)

ax.set_xlabel('x1')
ax.set_ylabel('x2')
#ax.set_zlabel('Z')

wframe1 = None
wframe2 = None
tstart = time.time()
wframe2 = ax.contour(x1, x2, z, color='w')

# multi modal optimization process
for i in range(0,iterations):
	population = affinity(population)
	# general process of clonal algorithm
	clone_population = cloning(population,num_clones)
	clone_population = mutation(clone_population,ro)
	population = selection(clone_population,num_clones,population)

	if wframe1:
	 	ax.collections.remove(wframe1)
	 	#ax.collections.remove(wframe2)

	x1s = []
	x2s = []
	zs = []

	for p in population:
		x1s.append(p.x1)
		x2s.append(p.x2)
		zs.append(p.affinity)
	
	wframe1 = ax.scatter(x1s, x2s)
	plt.pause(.001)

#wframe2 = ax.plot_surface(x1, x2, z, color='w')
# wframe1 = plt.scatter(x1s, x2s)
# wframe2 = plt.contour(x1, x2, z, color='w')
plt.show()

#print_population(population)
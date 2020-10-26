# -*- coding: utf-8 -*-
"""
@author: William John Trenberth
https://www.maths.ed.ac.uk/~wjtrenberth/
https://github.com/W-J-Trenberth

Python code for simulating the 2d Ising model with periodic boudnary conditions 
using a Monte Carlo algorithm, in particular the Metropolis algorithm.
"""


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


N=100  #The discretization parameter. There are N^2 points.
T = 0.001   #The temperature of the system.

flips_per_frame = N*N//20
number_of_frames = 100000

#setting up the figure
fig = plt.figure()
plt.axis('off')
initial_spins = np.random.choice([-1,1], size=(N,N))
initial_spins[0,0] = -1
im = plt.imshow(initial_spins, cmap = 'gray')

# animation function.  This is called sequentially
def animate(i):
    for _ in range(0, flips_per_frame):
         i = np.random.randint(0,N)
         j = np.random.randint(0,N)
         
         spins = im.get_array()
         # %N gives periodic boundary conditions.
         deltaE = 2*spins[i,j]*(spins[(i+1)%N,j] + spins[i,(j+1)%N] 
                                 + spins[(i-1)%N,j] + spins[i,(j-1)%N]) 
         
         if deltaE < 0:
             spins[i,j] *= -1
         
         elif  np.random.uniform() < np.exp(-deltaE/T):
             spins[i,j] *= -1
             
    return [im]
    
anim = animation.FuncAnimation(fig, animate,
                               frames=number_of_frames, interval=20, blit=True)

#anim.save('ising20.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

import matplotlib.pyplot as plt
import numpy as np

"""
Instructions to execute the code
run as : python3 plotting.py

The purpose of this file is to generate graphs for memory usage, 
time usage and number of augmenting paths required
"""

# For plotting number of augmenting paths
N = 2

# Change values as per result
ek = (5, 24)
ff = (134, 24)

ind = np.arange(N) 
width = 0.35       
plt.bar(ind, ek, width, label='Edmond Karp')
plt.bar(ind + width, ff, width,
    label='Ford Fulkerson')

plt.ylabel('Number of augmenting paths')
plt.title('Number of augmenting paths needed for max flow')

plt.xticks(ind + width / 2, ('US Airports', 'Neural Network'))
plt.legend(loc='best')
plt.show()

# For plotting memory usage
N = 2
# Change values as per result
ek = (0.19891, 0.06539)
ff = (3.40325, 0.74525)

ind = np.arange(N) 
width = 0.35       
plt.bar(ind, ek, width, label='Edmond Karp')
plt.bar(ind + width, ff, width,
    label='Ford Fulkerson')

plt.ylabel('Time (in seconds)')
plt.title('Run time by Dataset and algorithm')

plt.xticks(ind + width / 2, ('US Airports', 'Neural Network'))
plt.legend(loc='best')
plt.show()

# For plotting memory usage
N = 2
# Change values as per result
ek = (76, 75)
ff = (95, 93)

ind = np.arange(N) 
width = 0.35       
plt.bar(ind, ek, width, label='Edmond Karp')
plt.bar(ind + width, ff, width,
    label='Ford Fulkerson')

plt.ylabel('Memory Usage (in MB)')
plt.title('Memory usage by Dataset and algorithm')

plt.xticks(ind + width / 2, ('US Airports', 'Neural Network'))
plt.legend(loc='best')
plt.show()
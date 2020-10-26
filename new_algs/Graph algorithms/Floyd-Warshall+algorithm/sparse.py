# importing the required module 
import matplotlib.pyplot as plt 
import numpy as np   
import math

x = [1000,2000, 3000,4000,5000,6000,7000,8000,9000,10000]
y = [4, 35, 105, 253, 438, 753, 1192, 1777,2632,3480]
z = [19, 149, 496, 1270, 1998, 3515, 5743, 8871, 12321, 17989]
plt.title('Sparse Graphs')
plt.plot(x, y,'r',label='BFS')
plt.plot(x, z,'y',label='Floyd Warshall Algorithm')
plt.xlabel('vertices') 
plt.ylabel(' time ' + ' (sec) ')
plt.legend(loc='upper left')
plt.show()

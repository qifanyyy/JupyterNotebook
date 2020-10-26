# importing the required module 
import matplotlib.pyplot as plt 
import numpy as np   
import math

x = [1000,2000, 3000,4000,5000,6000,7000,8000,9000,10000]
y = [37, 355, 1153, 2205, 2705, 4538, 6337, 9468,12763, 17843]
z = [18, 179,  685, 1569, 2560, 4567, 7503, 11408, 16156, 22095]
plt.title('Dense Graphs')
plt.plot(x, y,'r',label='BFS')
plt.plot(x, z,'y',label='Floyd Warshall Algorithm')
plt.xlabel('vertices') 
plt.ylabel(' time ' + ' (sec) ')
plt.legend(loc='upper left')
plt.show()

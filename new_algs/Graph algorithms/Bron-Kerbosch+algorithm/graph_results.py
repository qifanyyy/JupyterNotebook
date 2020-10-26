import numpy as np
import matplotlib.pyplot as plt

y, x = np.loadtxt('results/results4.csv', delimiter=',', unpack=True)
y.sort()
x.sort()

y1 = y[0:6]
x1 = x[0:6]

y2 = y[6:]
x2 = x[6:]

plt.plot(y2, x2, label='')
plt.xlabel('Vertices')
plt.ylabel('Cliques')
plt.title('Algorithm results')
plt.savefig('img/results7.png')



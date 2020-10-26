import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

path = open('PATH.txt').read()
data = open(path + '\\fil\\lum.txt').read().split(',')

#print(data)

o = int(data[0])
n = int(data[1])
it = 2

xx = np.arange(n)

plt.figure(figsize=(7, 7))
plt.title('Changes in the Luminosity during the images')
plt.grid(True)

plt.ylabel('# Luminosity')
plt.yscale('linear')

plt.xlabel('# Image')
plt.xticks(xx)

for i in range(o):
    data1 = []
    for j in range(n):
        data1.append(int(data[it]))
        it = it+1
    plt.plot(data1, label=('Object '+str(i+1)))
plt.legend()
#plt.show()
plt.savefig(path + '\\src\\pic\\Lumin.png')

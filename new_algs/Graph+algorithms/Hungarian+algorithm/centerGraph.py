import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

path = open('PATH.txt').read()
data = open(path + '\\fil\\center.txt').read().split(',')

#print(data)

o = int(data[0])
n = int(data[1])
W = int(data[2])
H = int(data[3])
it = 4

plt.figure(figsize=(7, 7))
plt.title('Moving Centers')
plt.grid(True)

yy = np.arange(0, H, 20)
xx = np.arange(0, W, 20)

plt.ylabel('H')
plt.yticks(yy)
plt.ylim([0, H])

plt.xlabel('W')
plt.xticks(xx)
plt.xlim([0, W])
for i in range(o):
    data1 = []
    data2 = []
    for j in range(n):
        data1.append(float(data[it]))
        it = it+1
        data2.append(H - float(data[it]))
        it = it+1
    plt.plot(data1, data2, 'o', label=('Object '+str(i+1)))
plt.legend()
#plt.show()
plt.savefig(path + '\\src\\pic\\Centers.png')

import sys
import matplotlib.pyplot as plt
import numpy as np

filepath = sys.argv[1]

with open(filepath) as datafile:
	data = [line.split(",") for line in datafile]

for i in range(len(data)):
	data[i][1] = float(data[i][1])

data = np.asarray(data)
data = np.matrix.transpose(data)

plt.plot(data[0], data[1], ".")
plt.title("Accuracy of kNN algorithm")
plt.ylabel("accuracy [%]")
plt.xlabel("k")
plt.axis([-1, 101, -10, 110])
plt.grid(True)
plt.show()

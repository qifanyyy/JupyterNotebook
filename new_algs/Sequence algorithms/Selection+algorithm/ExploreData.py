import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import Accuracy
import LoadData

# for testing
data = LoadData.loadData("../data/CS170_SMALLtestdata__49.txt")
LoadData.normalizeData(data)
N = len(data)
#a = Accuracy(data, N, [1], 2)
#print(a)

f11 = []
f12 = []
f13 =  []
f21 = []
f22 = []
f23 = []

for row in range(N):
	if (int(data[row][0]) == 1):
		f11.append(data[row][1])
		f12.append(data[row][6])
		f13.append(data[row][7])
	else:
		f21.append(data[row][1])
		f22.append(data[row][6])
		f23.append(data[row][7])
'''
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(f11, f12, f13, 'ro', color='red')
ax.plot(f21, f22, f23, 'ro', color='blue')
#plt.plot(f11, f12, f13,'ro', color='red')
#plt.plot(f21, f22, f23,'ro', color='blue')
plt.savefig('/Users/samueldominguez/Downloads/3dplt.png')
'''


fig = plt.figure()
plt.scatter(f11, f12, color='red')
plt.scatter(f21, f22, color='blue')
plt.savefig('/Users/samueldominguez/Downloads/2dplt.png')

	

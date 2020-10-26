import csv
from matplotlib import pyplot as plt
import numpy as np

plt.rcParams['axes.unicode_minus']=False # show negative sign '-'

x = []
y = []
z = []
v = []

# open file
with open ('example2.csv') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(int(row[0]))
        y.append(float(row[1]))
        z.append(float(row[2]))
        v.append(float(row[3]))

plt.plot(x, y, label='GradeSchool Alg.')
# plt.plot(x, z, label='Divide&Conquer Alg.')
# plt.plot(x, v, label='Karatsuba Alg.')

plt.xlabel('testData (# of digits)')
plt.ylabel('runtime (s)')
plt.title('RunTime test of Multiplication methods')
plt.legend()
plt.show()
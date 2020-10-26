import csv
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import polyfit
from math import log2

p_based_dict = {p: [] for p in [0.2, 0.4, 0.6, 0.8]}
with open('output1006.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        print(str(row))
        # 0 - p; 1,2 - v1, v2; 6 - e; 7 - vizing, 8 - gabow
        print('1' + str(float(row[0])))
        print('2' + str((int(row[1]) + int(row[2]))))
        print('3' + str(int(row[6])))
        print('4' + str(float(row[7])))
        print('5' + str(float(row[8])))
        p_based_dict[float(row[0])].append((
                                               (int(row[1]) + int(row[2])),
                                                int(row[6]),
                                                float(row[7]),
                                                float(row[8])))

for p in p_based_dict:
    x = np.array([value[0]*value[1] for value in p_based_dict[p]])
    vizing = np.array([value[2] for value in p_based_dict[p]])
    gabow = np.array([value[3] for value in p_based_dict[p]])
    fig = plt.figure()
    ax = plt.axes()
    ax.set_xlabel('number of edges for p1 = ' + str(p))
    ax.set_ylabel('time, seconds')
    ax.plot(x, vizing, 'r*', label='vizing')
    # b1, m1 = polyfit(x, vizing, 1)
    # ax.plot(x, b1 + m1*x, 'r-')

    ax.plot(x, gabow, 'bo', label='cole-hopcroft')
    # b2, m2 = polyfit(x, gabow, 1)
    # ax.plot(x, b2 + m2*x, 'b-')
    ax.legend(loc='upper left')
    fig.show()
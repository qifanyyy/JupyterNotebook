from SelectionSort import selection_sort
from InsertionSort import insertion_sort
import matplotlib.pyplot as plt
import sys

sizes = [5, 10, 20, 35, 55, 80, 105, 135, 170, 210]
times = []
if sys.argv[1] == 'i':
    for i in range(0, len(sizes)):
        times.append(insertion_sort(sizes[i]))
else:
    for i in range(0, len(sizes)):
        times.append(selection_sort(sizes[i]))

for i in range(0, len(sizes)):
    plt.scatter(sizes[i], times[i])
plt.show()

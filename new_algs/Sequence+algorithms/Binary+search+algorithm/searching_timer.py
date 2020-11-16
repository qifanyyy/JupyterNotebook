#ohamilton0079
#Comparing linear and binary search
#10/07/2020

#Local libraries
from binary_search import binary_search
from linear_search import linear_search
from normalise_list import normalise

from timeit import timeit
from random import randint
import matplotlib.pyplot as plt

listSize = 100000

#Generate a sorted list with the specified size
print("Generating list...")
listToSearch = [i for i in range(listSize)]

#Anonymous functions for searches
linearSearch = lambda : linear_search(listToSearch, randint(0, listSize-1)) #Get a random item to find in the specified range 
binarySearch = lambda : binary_search(listToSearch, randint(0, listSize-1))

#Time the functions for 100 runs each
print("Timing searching algorithms...")
lsTime = timeit(linearSearch, number=100)
bsTime = timeit(binarySearch, number=100)

#Create a list of execution times
timesList = [lsTime, bsTime]

#Get units for time
units = ["seconds", "milliseconds", "microseconds", "nanoseconds"]

#Normalise the list of times, returning the list and unit index
inputList, currentUnitIndex = normalise(timesList, units)

#X-axis values
xValues = ["Linear search", "Binary search"]

#Plot as a graph
print("Plotting results...")
plt.bar(range(2), timesList, align="center", alpha=0.5)

#Set the x ticks
plt.xticks(range(2), xValues)

plt.title("Searching Algorithm Performance")
plt.xlabel("Searching Algorithms")
plt.ylabel("Time taken ({})".format(units[currentUnitIndex]))

#Show the graph
plt.show()

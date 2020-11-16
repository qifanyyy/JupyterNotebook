"""
Emulated Bellman-Ford Algorithm
PoOya Khandel, Mohammad Hossein Tavakoli Bina
"""

from BellmanFord import BFA
import msvcrt
import re
import timeit


elapsedTime = 0
start = 0
whichPort = {}
adrToName = {}
routerCount = 0
hit = None
routerName = input("Welcome to Emulated Bellman-Ford Algorithm\n"
                   "Which router am I?\n")

with open("which_port.txt") as whichRouter:
    for lines in whichRouter:
        whichPort[lines[0]] = int(lines[2:6])
        adrToName[int(lines[2:6])] = int(lines[0])
        routerCount += 1


myLine = open("adj_mat.txt").readlines()[int(routerName) - 1]
myLine = myLine.rstrip('\n')
initialCost = re.split(" ", myLine)
print('Initial Cost is {}\n'.format(initialCost))

myBf = BFA(routerCount, initialCost, routerName, whichPort, adrToName)
myBf.who_to_send()

try:
    s = input("To start BellmanFord Algorithm, Enter 's'\n")
    assert s == 's'
except AssertionError:
    s = input("Wrong input! To start BellmanFord Algorithm, Enter 's'\n")

myBf.send()
start = timeit.default_timer()
while True:
    hit = msvcrt.kbhit()
    elapsedTime = timeit.default_timer() - start
    if elapsedTime > 1:
        myBf.send()
        start = elapsedTime

    myBf.receive()
    if hit:
        key = ord(msvcrt.getch())
        if key == ord('u'):
            myLine = open("adj_mat.txt").readlines()[int(routerName) - 1]
            myLine = myLine.rstrip('\n')
            newCost = re.split(" ", myLine)
            print('New cost is {}\n'.format(newCost))
            myBf.check_cost(newCost)

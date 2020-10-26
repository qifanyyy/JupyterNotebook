import random
from class_printer import *
from class_queue import Queue
from class_task import *

def simulation(numSeconds, pagesPerMinute):
    """
    The main simulation implements the algorithm described above.
    The printQueue object is an instance of our existing queue ADT.
    A boolean helper function, newPrintTask, decides whether a new
    printing task has been created. We have again chosen to use the
    randrange function from the random module to return a random integer
    between 1 and 180. Print tasks arrive once every 180 seconds.
    By arbitrarily choosing 180 from the range of random integers,
    we can simulate this random event. The simulation function allows
    us to set the total time and the pages per minute for the printer.
    """
    labprinter = Printer(pagesPerMinute)
    printQueue = Queue()
    waitingtimes = []

    for currentSecond in range(numSeconds):

      if newPrintTask():
         task = Task(currentSecond)
         printQueue.enqueue(task)

      if (not labprinter.busy()) and (not printQueue.isEmpty()):
        nexttask = printQueue.dequeue()
        waitingtimes.append(nexttask.waitTime(currentSecond))
        labprinter.startNext(nexttask)

      labprinter.tick()

    averageWait=sum(waitingtimes)/len(waitingtimes)
    print("Average Wait %6.2f secs %3d tasks remaining."%(averageWait,printQueue.size()))

def newPrintTask():
    num = random.randrange(1,181)
    if num == 180:
        return True
    else:
        return False

for i in range(10):
    simulation(3600,5)

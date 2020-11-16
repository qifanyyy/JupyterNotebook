import matplotlib.pyplot as plt
from matplotlib import animation
from random import randint
import math

# Configure the size of the list here
LIST_LENGTH = 30
fig = plt.figure()
n = LIST_LENGTH * 2 + 3 #Number of frames

# Create a list of random numbers (represented as red bars on a bar graph later)
RAND_LIST = []
colors = []
for x in range(0, LIST_LENGTH):
    rand_num = randint(0, 100)
    RAND_LIST.append(rand_num)
    colors.append('r')

def animate(i):
    # axes set up
    plt.cla()
    plt.title("Selection Sort Visualization")
    plt.ylabel('Value')
    plt.xlabel('Index of Items in List')
    j = math.floor(i/2)

    global minIndex

    if i % 2 == 0 or i == 0:
        if i != 0 and minIndex != j-1:
            colors[minIndex] = "r"
        colors[j] = 'y'
        minVal = min(RAND_LIST[j:LIST_LENGTH])
        minIndex = RAND_LIST[j:LIST_LENGTH].index(minVal) + j
        colors[minIndex] = 'g'
    else:
        RAND_LIST[j], RAND_LIST[minIndex] = RAND_LIST[minIndex], RAND_LIST[j]
        colors[j], colors[minIndex] = colors[minIndex], colors[j]

    print(RAND_LIST)

    return plt.bar(range(0, LIST_LENGTH), RAND_LIST, color= colors, alpha = 0.6)

anim = animation.FuncAnimation(fig, animate, repeat=False, blit=True, frames=n, interval= max(900-(LIST_LENGTH*0.5)**1.8, 30))
plt.show()
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# calculate a euclidean rhythm
def euclid(steps,  pulses):
    storedRhythm = [] # empty array which stores the rhythm.
    # the length of the array is equal to the number of steps
    # a value of 1 for each array element indicates a pulse

    bucket = 0  # out variable to add pulses together for each step
    i = 0

    while i < steps:
        bucket += pulses
        if bucket >= steps:
            bucket -= steps
            storedRhythm.append(1)
        else:
            storedRhythm.append(0)
        i += 1
    return storedRhythm


# Rotates the sequence by a specified number of steps
def rotateSeq(seq, rotate):
    output = np.empty(len(seq))
    val = len(seq) - rotate
    i = 0
    while i < len(seq):
        output[i] = seq[abs((i + val) % len(seq))]
        i += 1
    return output


# Checks if there is a beat on a specific step
def query_beat(storedRhythm, curSteps, curBeat):
    curStep = curBeat % curSteps
    return storedRhythm[curStep]


# returns a list of points of length size that are equidistant from each other
def equidistPoints(size):
    r = 1
    numPoints = size
    points = []
    for index in range(numPoints):
        points.append(
            [r * math.cos((index * 2 * math.pi) / numPoints), r * math.sin((index * 2 * math.pi) / numPoints)])
    return points


# gets the color of the specific point
def getColorOfPoint(sequence, i):

    if sequence[i] == 1:
        color = "red"
    else:
        color = "blue"
    return color


# gets the color of the specific point
def connectTheDotsX(sequence, i):

    if sequence[i] == 1:
        color = "red"
    else:
        color = "blue"
    return color


# Plots the circle with different color points depending on when the onsteps are
def plotCircle(pointsList, seq):
    cX = []
    cY = []
    x = []
    y = []
    i = 0
    while i < len(pointsList):
        curr = pointsList[i]
        x.append(curr[0])
        y.append(curr[1])
        i += 1
    plt.axis('off')
    red_patch = mpatches.Patch(color='red', label='Onsteps')
    blue_patch = mpatches.Patch(color='blue', label='OffSteps')
    plt.legend(handles=[red_patch, blue_patch], loc=10)
    for i in range(len(x)):
        plt.scatter(x[i], y[i], c=getColorOfPoint(seq, i))
        if getColorOfPoint(seq, i) == "red":
            cX.append(x[i])
            cY.append(y[i])
    cX.append(cX[0])
    cY.append(cY[0])
    plt.plot(cX, cY, c="red")
    plt.show()


# Main Function that brings everything together
def main():
    steps = input("Enter the number of steps: ")
    pulses = input("Enter the number of pulses: ")
    rotation = input("Enter the rotation: ")
    sequence = euclid(steps, pulses)
    sequence = rotateSeq(sequence, rotation)
    pL = equidistPoints(steps)
    plotCircle(pL, sequence)


# Executes the main method
main()

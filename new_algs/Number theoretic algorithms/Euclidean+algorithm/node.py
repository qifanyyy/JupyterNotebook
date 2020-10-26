#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import numpy as np

class Node(object):
    def __init__(self, heuristic, currentState, goalState, size, gScore, parentHash):
        self.currentState = currentState
        self.gScore = gScore
        self.parentHash = parentHash
        self.heuristic = heuristic
        self.hScore = self.__computH__(goalState, size)
        self.fScore = self.__computF__()
        
    def __calculateLinearConfilct__(self, goalState, size, x):
        total = 0
        if size == 3:
            #region LC Size 3
            y = 0
            valY1 = -1
            valY2 = -1
            valY3 = -1
            valX1 = -1
            valX2 = -1
            valX3 = -1
            while y < size:
                if self.currentState[x][y] == goalState[x][0]:
                    valY1 = y
                elif goalState[x][1] != 0 and self.currentState[x][y] == goalState[x][1]:
                    valY2 = y
                elif self.currentState[x][y] == goalState[x][2]:
                    valY3 = y
                if self.currentState[y][x] == goalState[0][x]:
                    valX1 = y
                elif goalState[1][x] != 0 and self.currentState[y][x] == goalState[1][x]:
                    valX2 = y
                elif self.currentState[y][x] == goalState[2][x]:
                    valX3 = y
                y +=1

            if valY3 != -1:
                if valY2 != -1 and valY3 < valY2:
                    total += 2
                elif valY1 != -1 and valY3 < valY1:
                    total += 2

            if valY2 != -1:
                if valY1 != -1 and valY2 < valY1:
                    total += 2

            if valX3 != -1:
                if valX2 != -1 and valX3 < valX2:
                    total += 2
                elif valX1 != -1 and valX3 < valX1:
                    total += 2

            if valX2 != -1:
                if valX1 != -1 and valX2 < valX1:
                    total += 2
            return total
            #endregion
        elif size == 4:
            #region LC Size 4
            y = 0
            valY1 = -1
            valY2 = -1
            valY3 = -1
            valY4 = -1
            valX1 = -1
            valX2 = -1
            valX3 = -1
            valX4 = -1
            while y < size:
                if self.currentState[x][y] == goalState[x][0]:
                    valY1 = y
                elif goalState[x][1] != 0 and self.currentState[x][y] == goalState[x][1]:
                    valY2 = y
                elif self.currentState[x][y] == goalState[x][2]:
                    valY3 = y
                elif self.currentState[x][y] == goalState[x][3]:
                    valY4 = y
                if self.currentState[y][x] == goalState[0][x]:
                    valX1 = y
                elif self.currentState[y][x] == goalState[1][x]:
                    valX2 = y
                elif goalState[2][x] != 0 and self.currentState[y][x] == goalState[2][x]:
                    valX3 = y
                elif self.currentState[y][x] == goalState[3][x]:
                    valX4 = y
                y += 1

            if valY4 != -1:
                if valY3 != -1 and valY4 < valY3:
                    total += 2
                elif valY2 != -1 and valY4 < valY2:
                    total += 2
                elif valY1 != -1 and valY4 < valY1:
                    total += 2

            if valY3 != -1:
                if valY2 != -1 and valY3 < valY2:
                    total += 2
                elif valY1 != -1 and valY3 < valY1:
                    total += 2

            if valY2 != -1:
                if valY1 != -1 and valY2 < valY1:
                    total += 2

            if valX4 != -1:
                if valX3 != -1 and valX4 < valX3:
                    total += 2
                elif valX2 != -1 and valX4 < valX2:
                    total += 2
                elif valX1 != -1 and valX4 < valX1:
                    total += 2

            if valX3 != -1:
                if valX2 != -1 and valX3 < valX2:
                    total += 2
                elif valX1 != -1 and valX3 < valX1:
                    total += 2

            if valX2 != -1:
                if valX1 != -1 and valX2 < valX1:
                    total += 2
            return total
            #endregion

    def __computH__(self, goalState, size):
        # Tiles-Out heuristic
        if self.heuristic == 2:
            return np.count_nonzero(goalState - self.currentState)
        
        # Euclidean heuristic
        elif self.heuristic == 1:
            total = 0
            x = 0
            y = 0
            while x < size:
                while y < size:
                    coordinates = np.where(goalState == self.currentState[y][x])
                    absXDistance = abs(coordinates[1][0] - x)
                    absYDistance = abs(coordinates[0][0] - y)
                    total += absXDistance if absXDistance >= absYDistance else absYDistance
                    y += 1
                y = 0
                x += 1
            return total

        # Manhattan heuristic
        else:
            total = 0
            x = 0
            y = 0
            while x < size:
                total += self.__calculateLinearConfilct__(goalState, size, x)
                while y < size:
                    if self.currentState[y][x] == 0:
                        y += 1
                        continue
                    coordinates = np.where(goalState == self.currentState[y][x])
                    xToReach = coordinates[1][0]
                    yToReach = coordinates[0][0]
                    total += abs(xToReach - x)
                    total += abs(yToReach - y)
                    y += 1
                x += 1
                y = 0
            return total

    def __computF__(self):
        return self.gScore + self.hScore

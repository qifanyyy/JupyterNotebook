#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# ColorScale algorithm and B&W image colorize example.
# Copyright (C) 2013  Gonzalo Exequiel Pedone
#
# This Program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This Program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with This Program.  If not, see <http://www.gnu.org/licenses/>.
#
# Email   : hipersayan TOD x TA gmail TOD com
# Web-Site: https://github.com/hipersayanX/ColorScale/

import os, sys

from PyQt4 import QtCore, QtGui

def calculateSector(color=0, nColors=0):
    diff = 256 / (nColors - 1)

    return int(color / diff)

def calculateGreyLimits(color=0, nColors=0):
    diff = 255 / (nColors - 1)
    sector = calculateSector(color, nColors)

    lower = int(diff * sector)
    upper = int(diff * (sector + 1))

    return (lower, upper)

def calculateColorLimits(colorTable=[], sector=0):
    lower = colorTable[sector]
    upper = colorTable[sector + 1]

    return (lower, upper)

def calcualateFactor(color=0, lower=0, upper=0):
    return (color - lower) / (upper - lower)

def calculateColor(k=0, lower=[], upper=[]):
    color = []

    for i in range(len(lower)):
        color.append(int(k * (upper[i] - lower[i]) + lower[i]))

    return color

def transformColor(colorTable=[], color=0):
    lower, upper = calculateGreyLimits(color, len(colorTable))
    k = calcualateFactor(color, lower, upper)
    sector = calculateSector(color, len(colorTable))
    lowerColor, upperColor = calculateColorLimits(colorTable, sector)

    return calculateColor(k, lowerColor, upperColor)

def createTransformTable(colorTable=[]):
    transformTable = []

    for i in range(256):
        transformTable.append(transformColor(colorTable, i))

    return transformTable

def cutColors(colorTable=[], nColors=256):
    newColorTable = []
    a = len(colorTable) - 1
    b = nColors - 1

    for i in range(nColors):
        j = round(i * a / b)
        newColorTable.append(colorTable[j])

    return newColorTable

def createColorTable(image=None, nColors=256):
    mostUsed = {}

    for y in range(image.height()):
        for x in range(image.width()):
            # Get a new pixel
            pixel = image.pixel(x, y)

            # Calculate the number of times that this
            # color has been used in the image
            if pixel in mostUsed:
                mostUsed[pixel] += 1
            else:
                mostUsed[pixel] = 0

    mostUsedTable = []

    # Sort colors by usage.
    for color in mostUsed:
        r = color & 0xff
        g = (color >> 8) & 0xff
        b = (color >> 16) & 0xff
        luma = (r + g + b) / 3
        mostUsedTable.append([luma, mostUsed[color], color])

    mostUsedTable.sort()
    mostUsedTable.reverse()

    colorTable = []
    curLuma = 0

    for i in range(len(mostUsedTable)):
        luma = round(mostUsedTable[i][0])

        if i == 0 or luma != curLuma:
            curLuma = luma
        else:
            continue

        color = mostUsedTable[i][2]
        colorTable.append([(color >> 16) & 0xff,
                           (color >> 8) & 0xff,
                           color & 0xff])

    colorTable.reverse()
    newColorTable = []
    j = 0

    for i in range(256):
        if j < len(colorTable):
            color = colorTable[j]
            luma = round((colorTable[j][0] + colorTable[j][1] + colorTable[j][2]) / 3)

            if i == luma:
                newColorTable.append(colorTable[j])
                j += 1
            else:
                newColorTable.append(3 * [i])
        else:
            newColorTable.append(3 * [i])

    return cutColors(newColorTable, nColors)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    # Replace the grey color by orange.
    #colorTable = [[  0,   0,   0],
                  #[225, 127,   0],
                  #[255, 255, 255]]

    # Rainbow
    #colorTable = [[255,   0, 255],
                  #[  0,   0, 255],
                  #[  0, 255, 255],
                  #[  0, 255,   0],
                  #[255, 255,   0],
                  #[255,   0,   0]]

    # Hot colors.
    #colorTable = [[  0,   0,   0],
                  #[255,   0,   0],
                  #[255, 255,   0],
                  #[255, 255, 255]]

    # Soft colors
    #colorTable = [[127,   0, 127],
                  #[255, 191, 255]]

    # Printing blue
    #colorTable = [[  0,   0,   0],
                  #[  0,   0,   0],
                  #[  0, 127, 255],
                  #[  0, 127, 255],
                  #[127, 191, 255],
                  #[127, 191, 255]]

    # Wrong luminance sorting
    #colorTable = [[  0,   0,   0],
                  #[  0, 255, 255],
                  #[  0,   0, 255],
                  #[255, 255, 255]]

    # Hope
    colorTable = [[  0,  50,  77],
                  [  0,  50,  77],
                  [113, 150, 159],
                  [113, 150, 159],
                  [252, 228, 168],
                  [252, 228, 168],
                  [215,  26,  33],
                  [215,  26,  33]]

    size = QtCore.QSize(800, 600)
    image = QtGui.QImage('someimage.jpg')
    image = image.scaled(size, QtCore.Qt.KeepAspectRatio)

#    colorTable = createColorTable(image, 256)
    transformTable = createTransformTable(colorTable)

    for y in range(image.height()):
        for x in range(image.width()):
            # Get a pixel from the image.
            pixel = image.pixel(x, y)
            r = pixel & 0xff
            g = (pixel >> 8) & 0xff
            b = (pixel >> 16) & 0xff

            # Calculate the color luminance
            color = round((r + g + b) / 3.0)

            # and transform it to the new color.
            newColor = transformTable[color][0] << 16 | \
                       transformTable[color][1] << 8 | \
                       transformTable[color][2]

            pixel = image.setPixel(x, y, newColor)

    label = QtGui.QLabel()
    label.resize(size)
    label.setScaledContents(True)
    label.setPixmap(QtGui.QPixmap.fromImage(image))
    label.show()
    app.exec_()

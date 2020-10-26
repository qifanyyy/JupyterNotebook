from datetime import datetime
from tkinter import *
from tkinter import filedialog
import csv
import os, sys, subprocess
import numpy as np

# AUTHOR: Luis Enrique Neri Pérez
# Copyright 2019

# This is an implementation of Kirkpatrick's Simulated Annealing that solves
# the Traveling Salesman Problem for 100 cities.

matrixes = [[],[]]
textCounter = 0
sCounter = 0
global window

def matrixMultiplication(a, b):
    row = []
    col = []
    global sCounter
    for i in range(len(a)):
        for j in range(len(b[0])):
            sum = 0
            for k in range(len(b)):
                sum += a[i][k] * b[k][j]
                sCounter += 1
            row.append(sum)
        r = row + []
        row.clear()
        col.append(r)
    return col


def matrixSplit(z):
    n11 = []
    n12 = []
    n21 = []
    n22 = []

    r11 = []
    r12 = []
    r21 = []
    r22 = []

    rH = len(z) // 2
    cH = len(z[0]) // 2

    n = z + []

    for i in range(len(n)):
        for j in range(len(n[0])):
            if i < rH:
                if j < cH:
                    r11.append(n[i][j])
                elif j >= cH:
                    r12.append(n[i][j])
            elif i >= rH:
                if j < cH:
                    r21.append(n[i][j])
                elif j >= cH:
                    r22.append(n[i][j])

        if i < rH:
            n11.append(r11 + [])
            n12.append(r12 + [])
            r11.clear()
            r12.clear()

        elif i >= rH:
            n21.append(r21 + [])
            n22.append(r22 + [])
            r21.clear()
            r22.clear()

    return n11, n12, n21, n22


def matrixDiff(a, b):
    c = [[0 for x in range(len(a))] for y in range(len(a[0]))]
    for i in range(len(a)):
        for j in range(len(a)):
            c[i][j] = a[i][j] - b[i][j]
    return c


def matrixSum(a, b):
    c = [[0 for x in range(len(a))] for y in range(len(a[0]))]
    for i in range(len(a)):
        for j in range(len(a)):
            c[i][j] = a[i][j] + b[i][j]
    return c


def matrixJoin(c11, c12, c21, c22):
    for i in range(len(c11)):
        c11[i] = c11[i] + c12[i]
        c21[i] = c21[i] + c22[i]
    return c11 + c21


def strassenAlgorithm(a, b):
    if(len(a[0]) == 2 & len(a) == 2):
        return matrixMultiplication(a, b)

    a11, a12, a21, a22 = matrixSplit(a)
    b11, b12, b21, b22 = matrixSplit(b)

    m1 = strassenAlgorithm(matrixDiff(a12, a22), matrixSum(b21, b22))  # m1 = (a12-a22) * (b21+b22)
    m2 = strassenAlgorithm(matrixSum(a11, a22), matrixSum(b11, b22))  # m2 = (a11+a22) * (b11+b22)
    m3 = strassenAlgorithm(matrixDiff(a11, a21), matrixSum(b11, b12))  # m3 = (a11-a21) * (b11+b12)
    m4 = strassenAlgorithm(matrixSum(a11, a12), b22)  # m4 = (a11-a12) * (b2)
    m5 = strassenAlgorithm(a11, matrixDiff(b12, b22))  # m5 = (a11) * (b12 - b22)
    m6 = strassenAlgorithm(a22, matrixDiff(b21, b11))  # m6 = (a22) * (b21, b11)
    m7 = strassenAlgorithm(matrixSum(a21, a22), b11)  # m7 = (a21 + a22) * (b11)

    c11 = matrixDiff(matrixSum(m1, matrixSum(m2, m6)), m4)
    c12 = matrixSum(m4, m5)
    c21 = matrixSum(m6, m7)
    c22 = matrixSum(matrixDiff(m2, m3), matrixDiff(m5, m7))
    return matrixJoin(c11, c12, c21, c22)


def mfileOpenA():
    file = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes=(("Text files", "*.csv"), ("All files", "*.*")))
    results = []
    print(file)
    with open(file) as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)  # change contents to floats
        for row in reader:  # each row is a list
            results.append(row)
    matrixes.insert(0, results)


def mfileOpenB():
    file = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes=(("Text files", "*.csv"), ("All files", "*.*")))
    results = []
    print(file)
    with open(file) as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)  # change contents to floats
        for row in reader:  # each row is a list
            results.append(row)
    matrixes.insert(1, results)

def printTextbook():
    global sCounter
    start = datetime.now()
    m = matrixMultiplication(matrixes[0], matrixes[1])
    time = datetime.now() - start
    np.savetxt("Textbook.txt", np.array(m), fmt="%s")
    openFile("Textbook.txt")

    wCText = Label(window, text="Textbook Time Running:" + str(time) + "s   Scalar Multiplications: " + str(sCounter) + " multiplications")
    sCounter = 0
    wCText.config(font=('arial', 10,))
    wCText.pack()


def printStrassen():
    global sCounter
    start = datetime.now()
    m = strassenAlgorithm(matrixes[0], matrixes[1])
    time = datetime.now() - start
    np.savetxt("Strassens.txt", np.array(m), fmt="%s")
    openFile("Strassens.txt")

    wCStrass = Label(window, text="Strassen's Time Running: " + str(time) + "s   Scalar Multiplications: " + str(sCounter) + " multiplications")
    sCounter = 0
    wCStrass.config(font=('arial', 10,))
    wCStrass.pack()


def openFile(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])


def install():
        if 'numpy' not in sys.modules:
            subprocess.call([sys.executable, "-m", "pip", "install", 'numpy'])



install()
import numpy as np

global window

window = Tk()
# Window configuration
window.title("Matrix Multiplications Algorithms")
window.resizable(width=FALSE, height=FALSE)
window.geometry('720x270')

# CONTENT
# Title
wTitle = Label(window, text="Welcome to the Matrix Multiplications")
wTitle.config(font=('arial', 30, 'bold'))
wTitle.pack()

wTitle2 = Label(window, text=" Algorithms Tester")
wTitle2.config(font=('arial', 30, 'bold'))
wTitle2.pack()

# Instructions
wInstructions = Label(window, text="Load two csv files for both Matrix A and Matrix B to multiply them:")
wInstructions.config(font=('arial', 15,))
wInstructions.pack()

#Buttons
buttonA = Button(text='Matrix A', width=30, command=mfileOpenA).pack()
buttonB = Button(text='Matrix B', width=30, command=mfileOpenA).pack()

# Operations
wOperations = Label(window, text="Press the following buttons to see the resultant matrixes and it's execution time")
wOperations.config(font=('arial', 15,))
wOperations.pack()

buttonTb = Button(text='Textbook Multiplication', width=30, command=printTextbook).pack()
buttonTb = Button(text='Strassens Algorithm Multiplication', width=30, command=printStrassen).pack()


window.mainloop()

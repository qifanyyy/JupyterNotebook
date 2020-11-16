# encoding: UTF-8
# authors: Luis / Bobby

import sys
from tkinter import *
from tkinter import messagebox, filedialog
import os

numMultiplicationsNormal = 0
numMultiplicationsStrassen = 0

def matrixMultiplication(A,B):
    global  numMultiplicationsStrassen
    m = len(A)
    k = len(B)
    n = len(A[0])

    C = [[0 for j in range(k)] for i in range(m)]

    for i in range(m):
        for j in range(k):
            for step in range(n):
                C[i][j] += A[i][step]*B[step][j]
                numMultiplicationsStrassen+=1
    return C

def basicMatrixMultiplication(A,B):
    global numMultiplicationsNormal
    m = len(A)
    k = len(B)
    n = len(A[0])

    C = [[0 for j in range(k)] for i in range(m)]

    for i in range(m):
        for j in range(k):
            for step in range(n):
                C[i][j] += A[i][step]*B[step][j]
                numMultiplicationsNormal +=1


    return C

def matrixAdd(A,B):
    rows = len(A)
    columns = len(A[0])
    C = [[0 for j in range(columns)] for i in range(rows)]

    for i in range(rows):
        for j in range(columns):
            C[i][j] += A[i][j]+B[i][j]
    return C


def matrixSubstract(A, B):
    rows = len(A)
    columns = len(A[0])
    C = [[0 for j in range(columns)] for i in range(rows)]

    for i in range(rows):
        for j in range(columns):
            C[i][j] = A[i][j] - B[i][j]
    return C


def strassen(A,B):
    global numMultiplicationStrassen

    # Base case
    if len(A) == 2:
        return matrixMultiplication(A,B)
    else:
        # The following will be done recursively until length of matrix equals 2
        shift = len(A) // 2
        length = len(A)

        a11 = [[A[i][j] for j in range(shift)] for i in range(shift)]
        a12 = [[A[i][j] for j in range(shift, length)] for i in range(shift)]
        a21 = [[A[i][j] for j in range(shift)] for i in range(shift, length)]
        a22 = [[A[i][j] for j in range(shift, length)] for i in range(shift,length)]

        b11 = [[B[i][j] for j in range(shift)] for i in range(shift)]
        b12 = [[B[i][j] for j in range(shift, length)] for i in range(shift)]
        b21 = [[B[i][j] for j in range(shift)] for i in range(shift, length)]
        b22 = [[B[i][j] for j in range(shift, length)] for i in range(shift, length)]


        # First, calculate M1, M2, M3, M4, M5, M6 and M7
        # m1 = (a11 + a22) * (b11+b22)
        m1 = strassen(matrixAdd(a11,a22), matrixAdd(b11,b22))

        # m2 = (a21 + a22) * b11
        m2 = strassen(matrixAdd(a21, a22), b11)

        # m3 = a11 * (b12 - b22)
        m3 = strassen(a11, matrixSubstract(b12, b22))

        # m4 = a22 * (b21 - b11)
        m4 = strassen(a22, matrixSubstract(b21, b11))

        # m5 = (a11 + a12) * b22
        m5 = strassen(matrixAdd(a11, a12), b22)

        # m6 = (a21 - a11) * (b11 + b12)
        m6 = strassen(matrixSubstract(a21, a11), matrixAdd(b11, b12))

        # m7 = (a12 - a22) * (b21 + b22)
        m7 = strassen(matrixSubstract(a12, a22), matrixAdd(b21, b22))


        # Now calculate C11, C12, C21 and C22
        # c11 = m1 + m4 - m5 + m7
        c11 =  matrixAdd(matrixSubstract(matrixAdd(m1,m4),m5), m7)
        c12 = matrixAdd(m3, m5)
        c21 = matrixAdd(m2, m4)
        c22 = matrixAdd(matrixAdd(matrixSubstract(m1, m2), m3), m6)

        C = [[0 for i in range(length)] for j in range(length)]

        for i in range(shift):
            for j in range(shift):
                C[i][j] = c11[i][j]
                C[i][j+shift] = c12[i][j]
                C[i+shift][j] = c21[i][j]
                C[i+shift][j+shift] = c22[i][j]
        return C

def formatMatrixToText(m):
    matrixText = ""
    for row in m:
        matrixText += str(row) + "\n"
    return matrixText

def writeToFile(C1,C2):
    
    output = open("C.txt", "w")
    output.write("TEXTBOOK ALGORITHM")
    output.write("\n")
    output.write(C1)
    output.write("\n")
    output.write("\n")
    output.write("STRASSEN ALGORITHM")
    output.write("\n")
    output.write(C2)
    output.close()

    return os.path.realpath("C.txt")


def init():
    # Do the GUI
    window = Tk()
    window.title("1st term project - Luis / Roberto")
    window.geometry("600x600")
    ANCHO = 600
    ALTO = 600
    window.attributes('-topmost', False)

    tagInfo = Label(window, text="Luis Alfonso Alcántara López-Ortega - A01374785\n"
                                 "Roberto Téllez Perezyera - A01374866", justify=RIGHT).place(x=ANCHO - 345, y=5)
    tag1 = Label(window, text="Welcome to our program.").place(x=10, y=60)
    tag2 = Label(window,
                 text="Here you can run the textbook and the Strassen algorithms for matrix multiplication.").place(
        x=10, y=90)
    tag3 = Label(window, text="Click on the Start button to begin.").place(x=10, y=120)
    tag4 = Label(window,
                 text="You will be asked to open the files and the solutions will be displayed in another window.").place(
        x=10, y=150)
    tagn = Label(window, text="You can close that new window and repreat the process from this one.").place(x=10, y=180)
    tagn1 = Label(window, text="Click on Quit on the lower right corner to close this window.").place(x=10, y=210)

    startButton = Button(window, text="Start",command=main ).place(x=(ANCHO // 2) - 30, y=ALTO // 2)
    exitButton = Button(window, text="Quit", command=window.quit).place(x=540, y=565)

    window.mainloop()




def main():
    # we DON'T want home window at the very top anymore
    pathA = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"),  # path to file 1
                                                  ("All files", ".")))
    matrixA = open(pathA, 'r').readlines()

    pathB = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"),  # path to file 1
                                                  ("All files", ".")))
    matrixB = open(pathB, 'r').readlines()

    messagebox.showinfo("Success", "Matrices loaded.")

    A = []
    B = []

    for line in matrixA:
        A.append([int(x) for x in line.rstrip().split(",")])
    for line in matrixB:
        B.append([int(x) for x in line.rstrip().split(",")])

    solutionWindow = Tk()
    solutionWindow.title("Solutions")
    solutionWindow.geometry("1000x840")


    # Validate if matrixes satisfy the requirements

    # Two matrixes can be multiplied if number of columns in A equals number of rows in B
    # In other words, A = mxn and B = nxk, C will be mxk

    if len(A[0]) != len(B):
        print("Can't have multiplication!")
        exit()

    C1 = basicMatrixMultiplication(A,B)
    C1 = formatMatrixToText(C1)
    C2 = strassen(A,B)
    C2 = formatMatrixToText(C2)

    global numMultiplicationsNormal
    global numMultiplicationsStrassen

    print("Basic", C1)

    print("Number of scalar multiplications:", numMultiplicationsNormal)
    if len(A) != len(A[0]):
        print("Strassen's Algorithm requires two square matrixes")
        exit()
    print("Strassen", C2)
    print("Number of scalar multiplications:", numMultiplicationsStrassen)

    filePath = writeToFile(C1,C2)


    tagTextbook = Label(solutionWindow, text="Textbook solution", justify=LEFT).grid(row=1, column=1)

    tagMultipCountTe = Label(solutionWindow, text="number of scalar multiplications: %d" % (numMultiplicationsNormal),
                             justify=LEFT).grid(row=2,
                                                column=1)
    tagStrassen = Label(solutionWindow, text="Textbook solution", justify=LEFT).grid(row=3, column=1)

    tagMultipCountStrassen = Label(solutionWindow,
                                   text="number of scalar multiplications: %d" % (numMultiplicationsStrassen),
                                   justify=LEFT).grid(row=4,
                                                      column=1)
    tagFilePath = Label(solutionWindow, text="Matrix C is found at: %s" % (filePath), justify=LEFT).grid(row=5, column=1)

    solutionWindow.mainloop()

init()

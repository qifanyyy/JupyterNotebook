import numpy as np
import sys
import string
import colorama


def MAIN():
    # Colorama allows printing with color in the terminal
    colorama.init()
    firstString = input("Please enter first string:\n")
    secondString = input("Please enter second string:\n")
    print(LCS(firstString, secondString))
    colorama.deinit()


def LCS(string1, string2):

    # Defining chars representing parent (where a cell in (matrix) gets its value from)
    topleft = '\\'
    up = '|'
    left = '-'

    # Padding both strings with zeros at the beginning for alignment purposes
    string1 = "0" + string1
    string2 = "0" + string2

    # Swapping strings if necessary to make string 2 always the longer string for easier reading.
    # Can be commented if not needed
    if len(string1) > len(string2):
        temp = string1
        string1 = string2
        string2 = temp

    # Defining the width and height of the matrix
    height = len(string1)
    width = len(string2)

    # Defining the matrix with all values = 0
    matrix = np.zeros([height, width], dtype="int")

    # Defining the corresponding trace matrix which holds parents (where a cell in (matrix) gets its value from))
    traceMatrix = np.ndarray([height, width], dtype='S1')

    # Filling out the matrix using Needleman-Wunsch Dynamic programming algorithm
    for i in range(1, height):
        for j in range(1, width):

            if string1[i] == string2[j]:
                matrix[i][j] = matrix[i-1][j-1] + 1
                traceMatrix[i][j] = topleft

            elif matrix[i-1][j] >= matrix[i][j-1]:
                matrix[i][j] = matrix[i-1][j]
                traceMatrix[i][j] = up

            else:
                matrix[i][j] = matrix[i][j-1]
                traceMatrix[i][j] = left

    # Calling traceback function which returns the longest common subsequence
    # and a color matrix (for colored terminal printing)
    # A matrix and its trace matrix must be passed along with the strings
    lcsString, colorMatrix = traceback(traceMatrix, matrix, string1, string2)

    # Calling printMatrixColored which prints a visualized matrix with its trace in color
    # A matrix, its trace matrix, its colorMatrix must be passed along with the strings
    printMatrixColored(traceMatrix, matrix,
                       string1, string2, colorMatrix)
    return lcsString


def traceback(traceMatrix, matrix, string1, string2):

    # Determining matrices dimensions
    height = len(matrix)
    width = len(matrix[0])

    # Declaring the color matrix with dimensions that would work with the printMatrixColored function
    colorMatrix = np.zeros([(2 * height) - 1, (2 * width) - 1], dtype='int')

    # traceback starting from bottom left cell
    i = len(traceMatrix) - 1
    j = len(traceMatrix[0]) - 1

    # String to hold the longest common subsequence
    lcsString = ""

    # If there is a match, color the next edge and the current letter then add the letter to the substring and move diagonally
    # else, color the next edge and the current letter move left/up (along the next edge)
    while(i > 0 and j > 0):
        colorMatrix[i*2][j*2] = 1

        if traceMatrix[i][j] == b'\\':

            colorMatrix[(i*2) - 1][(j*2) - 1] = 1
            lcsString += string1[i]
            i -= 1
            j -= 1

        elif traceMatrix[i][j] == b'|':

            colorMatrix[(i*2) - 1][(j*2)] = 1
            i -= 1

        else:

            colorMatrix[(i*2)][(j*2) - 1] = 1
            j -= 1

    # Reverse the string to get it in the correct order
    lcsString = ''.join(reversed(lcsString))

    # Return both the substring and the color matrix
    return lcsString, colorMatrix


def printMatrixColored(traceMatrix, matrix, string1, string2, colorMatrix):

    string1 = string1.replace('0', '')
    string2 = string2.replace('0', '')

    # Determining matrices dimensions
    height = len(matrix)
    width = len(matrix[0])

    # Declaring the print matrix with dimensions that would allow for spaces to add the edges
    printMatrix = np.ndarray([(2 * height), (2 * width)], dtype='S1')

    # Fill printMatrix initially with whitespaces
    for i in range(0, len(printMatrix)):
        for j in range(0, len(printMatrix[i])):
            printMatrix[i][j] = string.whitespace

    # Fill 2nd row and 2nd col with zeros
    for i in range(0, len(printMatrix)):
        for j in range(0, len(printMatrix[i])):
            if (i == 1 or j == 1) and (j % 2 != 0) and (i % 2 != 0):
                printMatrix[i][j] = '0'
            elif (i == 1 or j == 1):
                printMatrix[i][j] = string.whitespace
            else:
                pass

    # Fill in both strings into the printMatrix
    for j in range(0, len(string2)):
        printMatrix[0][(j * 2) + 3] = string2[j]
    for i in range(0, len(string1)):
        printMatrix[(i * 2) + 3][0] = string1[i]
    
    # Add the normal matrix to its place
    # At the same time, if a cell's parent is diagonal
    # Add the \ character to the top left cell
    # else if it is from above
    # Add the | character to the top cell
    # else add the - character to the left cell
    for i in range(1, height):
        for j in range(1, width):
            printMatrix[(i*2) + 1][(j*2) + 1] = matrix[i][j]
            if(traceMatrix[i][j] == b'\\'):
                printMatrix[(i*2)][(j*2)] = traceMatrix[i][j]
            elif(traceMatrix[i][j] == b'|'):
                printMatrix[(i*2)][(j*2) + 1] = traceMatrix[i][j]
            else:
                printMatrix[(i*2) + 1][(j*2)] = traceMatrix[i][j]


    # Print the printMatrix with green color if the corresponding cell in colorMatrix == 1
    # and with black otherwise
    for i in range(0, len(printMatrix)):
        for j in range(0, len(printMatrix[i])):
            if j == 1:
                print(" ", end='')
            print(colorama.Style.RESET_ALL, end='')
            # try:
            if i >= 1 and j >= 1 and colorMatrix[i - 1][j - 1] == 1:
                print(colorama.Fore.GREEN, end='')
                print(printMatrix[i][j].decode(), end='')
            else:
                print(printMatrix[i][j].decode(), end='')
        print()


if __name__ == "__main__":
    MAIN()
    pass

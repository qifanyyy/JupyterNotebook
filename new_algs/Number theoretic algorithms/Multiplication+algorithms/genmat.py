#! /usr/bin/python
import sys
import random as rn
import subprocess
import numpy

def getMat(sizex,sizey=0):
    if(sizey==0):
        sizey=sizex
    mat = numpy.zeros(sizex*sizey).reshape(sizex,sizey).astype(int)
    for row in range(sizex):
        for col in range(sizey):
            mat[row][col] = rn.randint(-127, 128)
    return mat

def matToString(mat):
    string = ""
    sizex = mat.shape[0]
    sizey = mat.shape[1]
    for i in range(sizex):
        for j in range(sizey-1):
            string +=str(mat[i][j])
            string +=" "
        string +=str(mat[i][sizey-1])
        string +="\n"
    return string

if __name__ == '__main__':
    size = int(sys.argv[1])

    mat1 = getMat(size, size)
    mat2 = getMat(size, size)
    with open("mat1", "w") as fmat1:
        with open("mat2", "w") as fmat2:             
	    fmat1.write(str(mat1.shape[0]))
	    fmat1.write('\n')
	    fmat1.write(matToString(mat1))
	    fmat2.write(str(mat2.shape[1]))
	    fmat2.write('\n')
	    fmat2.write(matToString(mat2))

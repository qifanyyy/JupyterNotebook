import random
import time
import math

# function to print a matrix
def printMatrix(matrix):
    if matrix:
        for i in matrix:
            for j in i:
                print(j, " ", end="")
            print()
    return



# function to create a matrix of size n
# with random integers between min and max values
# returns a matrix
def randomMatrix(n,min,max):
    matrix = []
    if n >= 1:
        for x in range(n):
            row = []
            for y in range(n):
                row.append(random.randint(min,max))
            matrix.append(row)
    return matrix

# function to split matix into 4 submatricies
# retruns a matrix
def divideMatrix(a,a11,a12,a21,a22):
    n1 = len(a)
    n2 = int(n1/2)
    for i in range(n1):
            for j in range(n1):
                if j < n2 and i < n2:
                    a11[i][j] = a[i][j]
                if j >= n2 and i < n2:
                    a12[i][j-n2] = a[i][j]
                if j < n2 and i >= n2:
                    a21[i-n2][j] = a[i][j]
                if j >= n2 and i >= n2:
                    a22[i-n2][j-n2] = a[i][j]
    return

# funtion to comnine 4 matricies into 1
# retruns a matrix
def combineMatricies(a11,a12,a21,a22):
    n1 = int(2*len(a11))
    n2 = len(a11)
    a = zeroMatrix(n1)
    for i in range(n1):
            for j in range(n1):
                if j < n2 and i < n2:
                    a[i][j] = a11[i][j]
                if j >= n2 and i < n2:
                    a[i][j] = a12[i][j-n2] 
                if j < n2 and i >= n2:
                    a[i][j] = a21[i-n2][j] 
                if j >= n2 and i >= n2:
                    a[i][j] = a22[i-n2][j-n2]
    return a

# funtion to add 2 matricies
# retruns a matrix
def addMatricies(a,b):
    n = len(a)
    sum = zeroMatrix(n)
    for i in range(n):
        for j in range(n):
            sum[i][j] = a[i][j] + b[i][j]
    return sum

#funtion to subtract 2 matricies
# retruns a matrix
def subMatricies(a,b):
    n = len(a)
    sum = zeroMatrix(n)
    for i in range(n):
        for j in range(n):
            sum[i][j] = a[i][j] - b[i][j]
    return sum

# function to classically multiply two matrices of size n
# retruns a matrix
def multiplyMatrices(n,m1,m2):
   result = []
   if m1 and m2:
       result = zeroMatrix(n)
       for i in range(n):
            for j in range(n):
                 for k in range(n):
                        result[i][j] += m1[i][k] * m2[k][j]                
   return result

# function to divide and conquer multiply two matrices
# retruns a matrix
def divideAndConquerMultiplication(a,b):
    n = len(a)
    c = zeroMatrix(n)
    if n == 1:
       c[0][0] = a[0][0] * b[0][0]
    else:
        size = int(n/2)
        c11 = zeroMatrix(size)
        c12 = zeroMatrix(size)
        c21 = zeroMatrix(size)
        c22 = zeroMatrix(size)

        a11 = zeroMatrix(size)
        a12 = zeroMatrix(size)
        a21 = zeroMatrix(size)
        a22 = zeroMatrix(size)

        b11 = zeroMatrix(size)
        b12 = zeroMatrix(size)
        b21 = zeroMatrix(size)
        b22 = zeroMatrix(size)

        divideMatrix(a,a11,a12,a21,a22)
        divideMatrix(b,b11,b12,b21,b22)

        c11 = addMatricies(divideAndConquerMultiplication(a11,b11),divideAndConquerMultiplication(a12,b21))
        c12 = addMatricies(divideAndConquerMultiplication(a11,b12),divideAndConquerMultiplication(a12,b22))
        c21 = addMatricies(divideAndConquerMultiplication(a21,b11),divideAndConquerMultiplication(a22,b21))
        c22 = addMatricies(divideAndConquerMultiplication(a21,b12),divideAndConquerMultiplication(a22,b22))
        c = combineMatricies(c11,c12,c21,c22)

    return c

# function to Strassen multiply two matrices
# retruns a matrix
def strassenMultiplictaion(a,b):
    n = len(a)
    c = zeroMatrix(n)
    if n == 1:
        c[0][0] = a[0][0]*b[0][0]
    else:
        size = int(n/2)
        c11 = zeroMatrix(size)
        c12 = zeroMatrix(size)
        c21 = zeroMatrix(size)
        c22 = zeroMatrix(size)

        a11 = zeroMatrix(size)
        a12 = zeroMatrix(size)
        a21 = zeroMatrix(size)
        a22 = zeroMatrix(size)

        b11 = zeroMatrix(size)
        b12 = zeroMatrix(size)
        b21 = zeroMatrix(size)
        b22 = zeroMatrix(size)

        divideMatrix(a,a11,a12,a21,a22)
        divideMatrix(b,b11,b12,b21,b22)

        p = strassenMultiplictaion(addMatricies(a11,a22),addMatricies(b11,b22))
        q = strassenMultiplictaion(addMatricies(a21,a22),b11)
        r = strassenMultiplictaion(a11,subMatricies(b12,b22))
        s = strassenMultiplictaion(a22,subMatricies(b21,b11))
        t = strassenMultiplictaion(addMatricies(a11,a12),b22)
        u = strassenMultiplictaion(subMatricies(a21,a11),addMatricies(b11,b12))
        v = strassenMultiplictaion(subMatricies(a12,a22),addMatricies(b21,b22))

        c11 = addMatricies(subMatricies(addMatricies(p,s),t),v)
        c12 = addMatricies(r,t)
        c21 = addMatricies(q,s)
        c22 = addMatricies(subMatricies(addMatricies(p,r),q),u)
        c = combineMatricies(c11,c12,c21,c22)

    return c

loops = 5 #number of for loops

# testing classic algorithm
print("classic")
for i in range(loops):
    n = i + 1
    m = randomMatrix(pow(2,n),0,9)
    start = time.time() #initiate timer
    multiplyMatrices(pow(2,n),m,m)
    end = time.time() #stop timer
    print(n,": ",end - start)

# testing divide and conquer algorithm
print("d&c")
for i in range(loops):
    n = i + 1
    m = randomMatrix(pow(2,n),0,9)
    start = time.time() #initiate timer
    divideAndConquerMultiplication(m,m)
    end = time.time() #stop timer
    print(n,": ",end - start)

# testing Strassen algorithm
print("Strassen")
for i in range(loops):
    n = i + 1
    m = randomMatrix(pow(2,n),0,9)
    start = time.time() #initiate timer
    strassenMultiplictaion(m,m)
    end = time.time() #stop timer
    print(n,": ",end - start)

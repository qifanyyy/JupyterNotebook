#!/usr/bin/env python
# coding: utf-8

# In[3]:


import sys
import numpy as np
import random
import math
import pandas as pd

def New_Matrix(p, q): # create a matrix filled with 0s
    matrix = [[0 for row in range(p)] for col in range(q)]
    return matrix

x = int(input("How many matrics do you want to muliply? "))

# counting the number of parenthesizations 
# def p_n(x):
#     pn =0
#     if x == 1:
#         pn = 1
#         return pn
#     if x >= 2:
#         for k in range(1,x):
#             pn = pn + (p_n(k) * p_n(x-k))
#         return pn
mat ={}

p = [[0] for i in range(x+1)]
j = 0
for i in range(x):
    n = int(input("Enter the matrix"+str(i+1)+" n:"))
    m = int(input("Enter the matrix"+str(i+1)+" m:"))
    p[j] = n
    if j == x-1:
        j += 1
        p[j] = m
    j += 1
    mat["mat"+str(i+1)] = np.zeros((n,m))
    matrix = [[0] * m for i in range(n)]
    for h in range(n):
        for k in range(m):
            matrix[h][k] = np.random.randint(1,6)
#             matrix[k][h] = int(input())
    mat["mat"+str(i+1)] = matrix
print(mat)
print("P = "+str(p))

#  Min of Matrix Chain Multiplication
def MCOrder(p):
    n = len(p)-1
    # For simplicity of the program, one extra row and one 
    m = [[0 for x in range(n+1)] for x in range(n+1)]
    s = [[0 for x in range(n+1)] for x in range(n+1)]
    # cost is zero when multiplying one matrix. 
    # L is chain length. 
    for i in range(0, n): 
        m[i][i] = 0
    for L in range(2, n+1): 
        for i in range(1, n-L+2): 
            j = i + L-1
            m[i][j] = sys.maxsize
            if i < j:
                for k in range(i, j): 
                    q = m[i][k] + m[k+1][j] + p[i-1] * p[k] * p[j]
                    if q < m[i][j]: 
                        m[i][j] = q
                        s[i][j] = k
    return m,s

m,s = MCOrder(p)
print("-----------------------------------")
print("Chain Order Matrix : ")
print(pd.DataFrame(m))
print("Minimum number of multiplications is: "+str(m[1][x]))
print("-----------------------------------")

# Print-Optimal_Parents
i = 1
j = x 
w = []
def print_Optimal(s,i,j):
    text = ""
    if i == j:
        text += "A"+str(i)
        return text
    else:
        text +=  "("+str(print_Optimal(s,i,s[i][j]))+str(print_Optimal(s,s[i][j]+1,j))+")"
        return text
print(print_Optimal(s,i,j))
text = print_Optimal(s,i,j)

# text HANDLING
counter1 = 0
for i in text:
    if i == "A" and text[(counter1+2)] != "("  and text[(counter1+2)] != " ":
        w.append(int(text[counter1+1]))
        counter1 += 1
    else:
        counter1 += 1
counter2 = 0
for i in text:
    counter2 += 1
    if counter2 != (len(text)-2):
        if i == "A" and int(text[counter2]) not in w :
            w.append(int(text[counter2])) 

print("w = "+str(w))


def add_m(a, b):
    n = len(a)
    C = np.array(New_Matrix(n,n))
    a = np.array(a)
    b = np.array(b)
    for i in range(0, n):
        for j in range(0, n):
            C[i][j] = a[i][j] + b[i][j]
    return C


def sub_m(a, b):
    n = len(a)
    C = np.array(New_Matrix(n,n))
    a = np.array(a)
    b = np.array(b)

    for i in range(n):
        for j in range(n):
            C[i][j] = a[i][j] - b[i][j] 
    return C


def split(matrix):  # split matrix into quarters
    n = len(matrix)
    newSize = n//2
    x11 = New_Matrix(newSize,newSize)
    x12 = New_Matrix(newSize,newSize)
    x21 = New_Matrix(newSize,newSize)
    x22 = New_Matrix(newSize,newSize)
    # dividing the matrices in 4 sub-matrices:
    for i in range(0, newSize):
        for j in range(0, newSize):
            x11[i][j] = matrix[i][j]            # top left
            x12[i][j] = matrix[i][j + newSize]    # top right
            x21[i][j] = matrix[i + newSize][j]   # bottom left
            x22[i][j] = matrix[i + newSize][j + newSize] # bottom right
    return x11,x12,x21,x22


def straight(a, b): # multiply the two matrices
    if len(a[0]) != len(b):
        print("Matrices are not m*n and n*p")
    else:
        p_matrix = New_Matrix(len(b[0]),len(a))
        for i in range(len(a)):
            for j in range(len(b[0])):
                for k in range(len(b)):
                    p_matrix[i][j] += a[i][k]*b[k][j]
    return p_matrix


def strassenR(a, b):
    n = len(a)
    if n == 1:
        return [[a[0][0] * b[0][0]]]
    else:
        newSize = n//2
        a11, a12, a21, a22 = split(a)
        b11, b12, b21, b22 = split(b)

        p1 = strassen(add_m(a11, a22), add_m(b11, b22)) # p1 = (a11+a22) * (b11+b22)

        p2 = strassen(add_m(a21, a22), b11)  # p2 = (a21+a22) * (b11)

        p3 = strassen(a11, sub_m(b12, b22))  # p3 = (a11) * (b12 - b22)

        p4 =strassen(a22, sub_m(b21, b11))   # p4 = (a22) * (b21 - b11)

        p5 = strassen(add_m(a11, a12), b22)  # p5 = (a11+a12) * (b22)   

        p6 = strassen(sub_m(a21, a11), add_m(b11, b12)) # p6 = (a21-a11) * (b11+b12)

        p7 = strassen(sub_m(a12, a22), add_m(b21, b22)) # p7 = (a12-a22) * (b21+b22)

       # calculating c21, c21, c11 e c22:
        c11 = sub_m(add_m(add_m(p1, p4), p7), p5) # c11 = p1 + p4 - p5 + p7
        
        c12 = add_m(p3, p5) # c12 = p3 + p5
        
        c21 = add_m(p2, p4)  # c21 = p2 + p4

        c22 = sub_m(add_m(add_m(p1, p3), p6), p2) # c22 = p1 + p3 - p2 + p6

        # Grouping the results obtained in a single matrix:
        C = New_Matrix(n,n)
        for i in range(0, newSize):
            for j in range(0, newSize):
                C[i][j] = c11[i][j]
                C[i][j + newSize] = c12[i][j]
                C[i + newSize][j] = c21[i][j]
                C[i + newSize][j + newSize] = c22[i][j]
        return C
    
    
def strassen(a, b):
    nextPowerOfTwo = lambda n: 2**int(math.ceil(math.log(n,2)))
    if len(a) >= len(a[0]):
        n = len(a)
    else:
        n = len(a[0])
    if len(b) >= len(b[0]):
        h = len(b)
    else:
        h = len(b[0])
    if n >= h:
        k = n
    else:
        k = h
    tp = nextPowerOfTwo(k)
    APrep = New_Matrix(tp,tp)
    BPrep = New_Matrix(tp,tp)
    for i in range(len(a)):
        for j in range(len(a[0])):
            APrep[i][j] = a[i][j]
    for i in range(len(b)):
        for j in range(len(b[0])):
            BPrep[i][j] = b[i][j]
    CPrep = strassenR(APrep, BPrep)
    C = New_Matrix(tp,tp)
    for i in range(tp):
        for j in range(tp):
            C[i][j] = CPrep[i][j]
    return C


y = straight(mat["mat"+str(w[0])],mat["mat"+str(w[1])])
for i in range(2,(len(w)-2)):
    y = straight(y , mat["mat"+str(w[i])])
print("-----------------------------------")
print("Answer in STRAIGHT Algorithm: ")
print(pd.DataFrame(y))

print("-----------------------------------")
z = strassen(mat["mat"+str(w[0])],mat["mat"+str(w[1])])
for i in range(2,(len(w)-2)):
    z = strassen(z , mat["mat"+str(w[i])])
zz = New_Matrix(len(y[0]),len(y))    
print("Answer in STRASSEN Algorithm: ")
for i in range (len(y)):
    for j in range(len(y[0])):
        zz[i][j] = z[i][j]
    
print(pd.DataFrame(zz))
print("-----------------------------------")


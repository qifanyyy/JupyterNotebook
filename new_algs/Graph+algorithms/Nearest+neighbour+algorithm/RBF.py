#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 27 14:58:03 2018

@author: Alejandro Urrutia
@modified by: Leonardo Ledesma Domínguez

"""

import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla
from Decorators import timePass

class Multiquadric1D():
    
    def __init__(self, c):
        self.__c = c
        
    def mq(self, x, xj):
        c = self.__c
        return np.sqrt((x - xj) * (x - xj) + c * c)

    def d1x(self, x, xj):
        c = self.__c
        return (x-xj) / np.sqrt( (x-xj) * (x-xj) + c * c )

    def d2x(self, x, xj):
        c2 = self.__c * self.__c
        r2 = (x-xj) * (x-xj)
        return c2 / ( np.sqrt(r2 + c2) * (r2 + c2) )

    def c(self):
        return self.__c
    

class Multiquadric2D():
    
    def __init__(self, c):
        self.__c = c
        
    def r(self, x, y, xj, yj):
        return np.sqrt((x-xj)**2 + (y-yj)**2)
        
    def mq(self, x, y, xj, yj):
        c2 = self.__c * self.__c
        r2 = self.r(x,y,xj,yj)**2
        return np.sqrt(r2 + c2)

    def d1x(self, x, y, xj, yj):
        c2 = self.__c * self.__c
        r2 = self.r(x,y,xj,yj)**2
        return (x-xj) / np.sqrt(r2 + c2)
    
    def d1y(self, x, y, xj, yj):
        c2 = self.__c * self.__c
        r2 = self.r(x,y,xj,yj)**2
        return (y-yj) / np.sqrt(r2 + c2)

    def d2x(self, x, y, xj, yj):
        c2 = self.__c * self.__c
        r2 = self.r(x,y,xj,yj)**2
        return (r2 + c2 - (x-xj)**2) / ( np.sqrt(r2 + c2) * (r2 + c2) )
    
    def d2y(self, x, y, xj, yj):
        c2 = self.__c * self.__c
        r2 = self.r(x,y,xj,yj)**2
        return (r2 + c2 - (y-yj)**2) / ( np.sqrt(r2 + c2) * (r2 + c2) )


    def c(self):
        return self.__c

class CS_RBF2D():

    def __init__(self, delta):
        self.__delta = delta

    def r(self, x, y, xj, yj):
        return np.sqrt ((x - xj) ** 2 + (y - yj) ** 2)

    def mq(self, x, y, xj, yj):
        r2 = self.r (x, y, xj, yj) ** 2
        if 0 <= (r2/self.__delta) <= 1:
            cond = np.power((1 - r2/self.__delta),4)
        else:
            cond = 0
        return cond

    def d1x(self, x, y, xj, yj):
        r2 = self.r (x, y, xj, yj) ** 2
        if 0 <= (r2 / self.__delta) <= 1:
            cond =(-4 / self.__delta) * np.power ((1 - (r2 / self.__delta)), 3)
        else:
            cond = 0
        return cond

    def d1y(self, x, y, xj, yj):
        r2 = self.r (x, y, xj, yj) ** 2
        if 0 <= (r2 / self.__delta) <= 1:
            cond = (-4 / self.__delta) * np.power ((1 - (r2 / self.__delta)), 3)
        else:
            cond = 0
        return cond

    def d2x(self, x, y, xj, yj):
        r2 = self.r (x, y, xj, yj) ** 2
        if 0 <= (r2 / self.__delta) <= 1:
            cond = (12 * self.__delta * self.__delta) * np.power ((1 - (r2 / self.__delta)), 2)
        else:
            cond = 0
        return cond

    def d2y(self, x, y, xj, yj):
        r2 = self.r (x, y, xj, yj) ** 2
        if 0 <= (r2 / self.__delta) <= 1:
            cond = (12 * self.__delta * self.__delta) * np.power ((1 - (r2 / self.__delta)), 2)
        else:
            cond = 0
        return cond

    def delta(self):
        return self.__delta

class GrammMatrix():
    
    def __init__(self, knots):
        self.__N = knots.nodes()
        self.__NI = knots.NI()
        self.__x = knots.a()
        self.__y = knots.b()
        self.__matrix = np.eye(self.__N)
        self.__fv = np.zeros(self.__N)
        self.__knots = knots
        
    def knots(self):
        return self.__knots
    
    def N(self):
        return self.__N

    def NI(self):
        return self.__NI

    def getMatrix(self):
        return self.__matrix
    
    def getfv(self):
        return self.__fv
        
    def setFv(self, f, i = None, j = None ):
        if i is not None and j is not None:
            self.__fv[i:j] += f
        else:
            self.__fv += f
            
    def update(self,solAnt, dt):
        for i in range(self.__fv.size):
            self.__fv[i] = self.__fv[i]*dt + solAnt[i]
        
    @timePass    
    def setDirichletRegular(self,f,a):
        knots = self.__knots

        i = knots.NI()
        r1 = i + (knots.dp() * knots.width())
        r2 = i + (knots.dp() * knots.width()) + (knots.dp() * knots.height())
        r3 = i + (2 * knots.dp() * knots.width()) + (knots.dp() * knots.height())
        r4 = i + (2 * knots.dp() * knots.width()) + (2* knots.dp() * knots.height())

        # print(self.__x[i:r1], self.__y[i:r1], r1)
        # print(self.__x[r1-1:r2-2], self.__y[r1-1:r2-2], r2, self.__x[r3-3], self.__y[r3-3])
        # print(self.__x[r2 - 2:r3 - 2], self.__y[r2 - 2:r3 - 2], r3)
        # print(self.__x[r3-2:r4-4], self.__y[r3-2:r4-4], r4, self.__x[r2-2], self.__y[r2-2],self.__x[i], self.__y[i])
        if a == 1:
            self.__fv[i: r1] = f
        elif a == 2:
            self.__fv[r1 - 1: r2 - 2] = f
            self.__fv[r3-3] = f
        elif a == 3:
            self.__fv[r2 - 2: r3 - 2] = f
        elif a == 4:
            self.__fv[r3 - 2: r4 - 4] = f
            self.__fv[r2-2] = f
            self.__fv[i] = f

    @timePass
    def fillMatrixLaplace2D( self, kernel , D):
         N = self.__N
         NI = self.__NI
         x = self.__x
         y = self.__y
    
    # ----- WL block matrix
         for i in range(NI):
            for j in range(N):
                self.__matrix[i,j] = D * (kernel.d2x(x[i], y[i], x[j], y[j])) + D * (kernel.d2y(x[i], y[i], x[j], y[j]))
            
    # ----- WB block matrix
         for i in range(NI,N):
            for j in range(N):
                self.__matrix[i,j] = kernel.mq(x[i], y[i], x[j], y[j])

    @timePass
    def fillMatrixLapace2D_CSupported(self, kernel, D, nn_result):
        N = self.__N
        NI = self.__NI
        x = self.__x
        y = self.__y

        # ----- WL block matrix
        for i in range(NI):
            for j in range(N):
                if j in nn_result[i]:
                    self.__matrix[i, j] = D * (kernel.d2x(x[i], y[i], x[j], y[j]))\
                                          + D * (kernel.d2y(x[i], y[i], x[j], y[j]))
                elif j == i:
                    self.__matrix[i, j] = D * (kernel.d2x (x[i], y[i], x[j], y[j])) \
                                          + D * (kernel.d2y (x[i], y[i], x[j], y[j]))
                else:
                    self.__matrix[i,j] = 0.0

        # ----- WB block matrix
        for i in range (NI, N):
            for j in range (N):
                self.__matrix[i, j] = kernel.mq (x[i], y[i], x[j], y[j])
        """    
        # ----- WB block matrix
        for i in range(NI, N):
            for j in range(N):
                if j in nn_result[i]:
                    self.__matrix[i, j] = kernel.mq(x[i], y[i], x[j], y[j])
                elif j == i:
                    self.__matrix[i, j] = kernel.mq (x[i], y[i], x[j], y[j])
                else:
                    self.__matrix[i, j] = 0.0

        """

class Solver():
    
    def __init__(self, matrix, algorithm = None):
        self.__lam = np.zeros(matrix.N())
        self.__u = np.zeros(matrix.N())
        if algorithm:
            self.__algorithm = algorithm
        else:
            self.__algorithm = 'linalg'
        self.__matrix = matrix
        
    def getMatrix(self):
        return self.__matrix
    
    def getKnots(self):
        return self.__matrix.knots()
    
    def lam(self):
        return self.__lam
    
    def getSol(self):
        return self.__u

    @timePass
    def analyticSol(ti, x, y, h, l):
        N_max = 20
        sum = 0.0
        for n in range(N_max):
            c1 = 2.0 / (np.pi * n)
            s1 = np.sinh(n * np.pi * (l - y) / h)
            s2 = np.sinh(n * np.pi * l / h)
            s3 = np.sin(n * np.pi * x / h)
            sum += c1 * s1 * s3 / s2
        return 2.0 * ti * sum


    @timePass
    def solve(self):
        G = self.__matrix.getMatrix()
        f = self.__matrix.getfv()
        
        if self.__algorithm == 'linalg':
            self.__lam = np.linalg.solve(G,f)
        elif self.__algorithm == 'bicgstab':
            A = sps.csr_matrix(G)
            self.__lam = spla.bicgstab(A,f)[0]
        elif self.__algorithm == 'bicg':
            A = sps.csr_matrix(G)
            self.__lam = spla.bicg(A,f)[0]
        elif self.__algorithm == 'cg':
            A = sps.csr_matrix(G)
            self.__lam = spla.cg(A,f)[0]
        elif self.__algorithm == 'gmres':
            A = sps.csr_matrix(G)
            self.__lam = spla.gmres(A,f)[0]
           # print(self.lam())
    
    @timePass
    def evaluate(self, kernel): 
        knots = self.__matrix.knots()
        x = knots.a()
        y= knots.b()
        total = 0.0
        max = 0.0
        for i in range(self.__matrix.N()):
            sum = 0.0
            #max = 0.0
            l = 4.0
            h = 2.0
            #total = 0.0
            for j in range(self.__matrix.N()):
                self.__u[i] += self.__lam[j] * kernel.mq(x[i],y[i],x[j],y[j])
                # change the next parameters for adjust the analytic solution

            for n in range(1,20,2):
                c1 = 2.0 / (np.pi * n)
                s1 = np.sinh(n * np.pi * (l - y[i]) / h)
                s2 = np.sinh(n * np.pi * l / h)
                s3 = np.sin(n * np.pi * x[i] / h)
                sum += c1 * s1 * s3 / s2

            sum = 2* 100 * sum
            diff = np.absolute(sum-self.__u[i])
            if diff > max:
                max = diff

            total += diff * diff

        RMS = np.sqrt(total / (self.__matrix.N() * self.__matrix.N()))
        print ("RMS error: %f" %(RMS))

    @timePass      
    def interpolate(self,kernel):
        knots = self.__matrix.knots()
        factorX = knots.width() * knots.dp()
        factorY = knots.height() * knots.dp()
        x = np.linspace(0,knots.width(), factorX)
        y = np.linspace(0,knots.height(), factorY)
        x2 = knots.a()
        y2 = knots.b()
        z = np.eye(factorY,factorX)
        for i in range(factorX):
            for j in range(factorY):
                for p in range(knots.nodes()):
                    z[j,i] += self.__lam[p] * kernel.mq(x[i],y[j],x2[p],y2[p])
                         
        return z

    def calcError(self, phiA, phiB):
        return np.absolute(phiA-phiB)

if __name__ == '__main__':
    
    from Knots import RegularMesh2D
    
    mesh = RegularMesh2D(6,6,2,2)
    mesh.create2Dmesh()
    
    kernel = Multiquadric2D(1)
    
    GM = GrammMatrix(mesh)
    GM.fillMatrixLaplace2D(kernel,1)
    Ga = GM.getMatrix()
    print (mesh.Ax())
    print(mesh.Ay())
    print(Ga)
    print(kernel.d2x(1,1,0,0) + kernel.d2y(1,1,0,0))
    print('-'*20,'\n')
    #GM.setNeummanRegular(kernel,0,1)
import os
import time
import utils
import cv2 as cv
import numpy

class Algorithm2D:

    def __init__(self):
        print "Algorithm 2D"
        self.Wk = 5
        self.eps = 5

    def fillScoringMatrix(self, AImage, BImage):
        n, m = len(AImage), len(BImage)
        scoringMatrix = utils.fillZeros(sizeX=n, sizeY=m)
        for i in range(1, m):
            for j in range(1, n):
                cross = self.scoringCross(scoringMatrix=scoringMatrix, n=j, m=i, AImage=AImage, BImage=BImage)
                up = self.scoringUp(scoringMatrix=scoringMatrix, n=j, m=i, Wk=self.Wk)
                left = self.scoringLeft(scoringMatrix=scoringMatrix, n=j, m=i, Wk=self.Wk)
                d = 0
                scoringMatrix[i][j] = max(cross, up, left, d)
        return scoringMatrix

    def scoringUp(self, scoringMatrix, n, m, Wk):
        ret = scoringMatrix[m-1][n]-Wk
        return ret

    def scoringLeft(self, scoringMatrix, n, m, Wk):
        ret = scoringMatrix[m][n-1]-Wk
        return ret

    def scoringCross(self, scoringMatrix, n, m, AImage, BImage):
        ret = scoringMatrix[m-1][n-1] + self.score(a=AImage[n], b=BImage[m])
        return ret

    def computeMaxScore(self,scoringMatrix):
        maxScore = 0
        n, m = len(scoringMatrix[0]), len(scoringMatrix)
        posA, posB = 1, 1
        for i in range(0, m):
            for j in range(0, n):
                if scoringMatrix[i][j] > maxScore:
                    maxScore = scoringMatrix[i][j]
                    posA = j
                    posB = i
        return posA, posB

    def computeBacktrack(self, scoringMatrix, maxScore):
        posA, posB = maxScore
        seqence =[]

        while posA != 1 and posB != 1:
            up = scoringMatrix[posB-1][posA]
            left = scoringMatrix[posB-1][posA]
            cross = scoringMatrix[posB-1][posA-1]
            maxNexScore = max(up, left, cross)

            if cross == maxNexScore or (posA-1 == 1) or (posB == 1):
                seqence.append([posA, posB])
                posA = posA - 1
                posB = posB - 1
            elif up == maxNexScore:
                seqence.append([None, posB])
                posA = posA
                posB = posB - 1
            elif left == maxNexScore:
                seqence.append([posA, None])
                posA = posA -1
                posB = posB
        return seqence

    def score(self, a, b):
        if abs(int(a) - int(b)) < self.eps:
            return 7
        else:
            return -7
    def exposeSequence(self, sequence, AImage, BImage):
        stra=""
        strb=""
        for s in sequence:
            a, b = s
            if a is not None:
                stra = stra + "{0}".format(AImage[a])
            else:
                stra = stra + "-"
            if b is not None:
                strb = strb + "{0}".format(BImage[b])
            else:
                strb = strb + "-"
        print stra[::-1]
        print strb[::-1]

    def alignSequence(self, AImage2D, BImage2D):
        print "Align Sequence"
        m, n = AImage2D.shape
        AImage = utils.matrixToArray(AImage2D)
        BImage = utils.matrixToArray(BImage2D)

        scoringMatrix = self.fillScoringMatrix(AImage=AImage, BImage=BImage)
        maxScore = self.computeMaxScore(scoringMatrix=scoringMatrix)
        findSequence = self.computeBacktrack(scoringMatrix=scoringMatrix, maxScore=maxScore)
        #AImage_map = [178 for i in range(0, len(AImage))]
        #BImage_map = [178 for i in range(0, len(BImage))]
        Disparity_map = [0 for i in range(0, len(AImage))]
        for i in range(0, len(findSequence)):
            a, b = findSequence[i]
            if a is None or b is None:
                continue
            else:
                Disparity_map[b] = 127 + (a-b)
                #print "xD: {0}".format(a-b)
                #assert (a-b)
                #AImage_map[a] = AImage[a]
                #BImage_map[b] = BImage[b]

        #AImage2D = utils.arrayToMatrix(AImage_map, m=m, n=n)
        #BImage2D = utils.arrayToMatrix(BImage_map, m=m, n=n)
        Disparity2D = utils.arrayToMatrix(Disparity_map, m=m, n=n)
        #x = numpy.asarray(AImage2D).astype(numpy.uint8)
        #y = numpy.asarray(BImage2D).astype(numpy.uint8)
        ret_disparity = numpy.asarray(Disparity2D).astype(numpy.uint8)
        return ret_disparity

__algorithm2d = Algorithm2D()
alignSequence = __algorithm2d.alignSequence
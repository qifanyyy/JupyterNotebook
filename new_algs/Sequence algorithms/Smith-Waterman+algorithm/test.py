import os
import time
import SmithWaterman as sm_alg
import cv2 as cv
import Algorithm2D as alg_2d
import img_utils as imgu
import utils
import numpy

class TestClass:

    def __init__(self):
        print "Test Class"
        self.BImage = ['X', 'G', 'G', 'T', 'T', 'G', 'A', 'C', 'T', 'A'];
        self.AImage = ['Y', 'T', 'G', 'T', 'T', 'A', 'C', 'G', 'G'];

    def starts(self, m, n, sizeX, sizeY, numberOfImage):
        cnt = 0
        cntX, cntY = 0, 0
        while True:
            if cnt == numberOfImage:
                break
            cnt = cnt + 1
            cntX = cntX + sizeX
            if cntX >= m or m-cntX < sizeX:
                cntX = 0
                if cntY >= n:
                    break
                else:
                    cntY = cntY + sizeY


        return cntX, cntY

    def cutImage(self, image, byM, byN, numberOfImage = None):
        m, n = image.shape
        sizeX = m/byM
        sizeY = n/byN
        retImg = utils.fillZeros(sizeY, sizeX)

        startX, startY = self.starts(m=m, n=n, sizeX=sizeX, sizeY=sizeY, numberOfImage=numberOfImage)

        print "X: {0} Y: {1}".format(startX, startY)

        for i in range(0, sizeX):
            for j in range(0, sizeY):
                retImg[i][j] = image[startX+i][startY+j]

        return numpy.asarray(retImg).astype(numpy.uint8)

    def mergeImage(self, part, whole, numberOfImage):
        m, n = whole.shape
        sizeX, sizeY = part.shape

        startX, startY = self.starts(m=m, n=n, sizeX=sizeX, sizeY=sizeY, numberOfImage=numberOfImage)

        for i in range(0, sizeX):
            for j in range(0, sizeY):
                whole[startX+i][startY+j] = part[i][j]
        return whole

    def test(self):
        #sm_alg.alignSequence(AImage=self.AImage, BImage=self.BImage)
        n, m = 1, 150
        _imgA, _imgB = imgu.getImages()
        # retA, retB = _imgA.copy(), _imgA.copy()
        disparity = _imgA.copy()
        for i in range(0, 220):
            imgA = self.cutImage(image=_imgA, byM=m, byN=n, numberOfImage=i)
            imgB = self.cutImage(image=_imgB, byM=m, byN=n, numberOfImage=i)
            x = alg_2d.alignSequence(AImage2D=imgA, BImage2D=imgB)
            disparity = self.mergeImage(part=x, whole=disparity, numberOfImage=i)
            # retA = self.mergeImage(part=x, whole=_imgA, numberOfImage=i)
            # retB = self.mergeImage(part=y, whole=_imgB, numberOfImage=i)

        cv.imshow("AImage", disparity)
        #cv.imshow("BImage", retB)
        #cv.imwrite("img/aa1.png", retA)
        cv.imwrite("img/bb1.png", disparity)
        cv.waitKey()

if __name__ == "__main__":
    tc = TestClass()
    tc.test()

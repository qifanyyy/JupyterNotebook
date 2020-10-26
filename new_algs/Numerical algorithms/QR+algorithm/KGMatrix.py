from math import sqrt, pow

"""
Written by Kevin Gay in Python 2.7!
Link to Git: https://github.com/KevinGay/KGMatrix
This module creates a matrix data structure and provides
methods to perform common matrix operations. The name of
the algorithm is the method name if a specific algorithm
is used.
Note: operator overloading has been implemented so the following is possible:
    -Addition/subtraction between two matrices
    -Multiplication/division between two matrices
        OR
        between a matrix and a scalar as long as the scalar follows the matrix.
"""

__author__ = 'Kevin Gay'


class Matrix(object):
    def __init__(self, matrixList=[]):
        """
        Creates a matrix using a supplied list.
        If no list is supplied, assume the matrix is empty.
        matrixList: list of floats or ints.
        """

        self.matrix = matrixList

        self.rows = len(self.matrix)

        if self.rows == 0:
            self.columns = 0
        else:
            self.columns = len(self.matrix[0])

        # Convert values to floats
        for row in range(self.rows):
            for col in range(self.columns):
                self.matrix[row][col] = float(self.matrix[row][col])

    def importMatrix(self, file):
        """
        Imports a matrix from a file and returns it.
        Pre: file must exist and be a valid file.
        """
        inLines = open(file, 'r').readlines()

        self.matrix = []

        for line in inLines:
            line = line.split()
            self.matrix.append(line)

        self.rows = len(self.matrix)
        self.columns = (len(self.matrix[0]))

        # Convert values to floats
        for row in range(self.rows):
            for col in range(self.columns):
                self.matrix[row][col] = float(self.matrix[row][col])

        return self.matrix

    def toString(self, roundTo=3):
        """
        Prints the matrix out in a clean format.
        roundTo is an optional parameter which specifies how many decimals to round to.
        It is recommended to keep roundTo at 3 unless you change the value in the string formatting.
        """
        tempRow = []
        for row in range(self.rows):
            for col in range(self.columns):
                temp = round(self.matrix[row][col], roundTo)
                tempRow.append(temp)

            print tempRow
            tempRow = []

    def identity(self, n):
        """Returns an n x n identity matrix."""
        self.rows = n
        self.columns = n

        tempRow = []
        tempMat = []

        for row in range(self.rows):
            for col in range(self.columns):
                if row == col:
                    tempRow.append(1.0)
                else:
                    tempRow.append(0.0)

            tempMat.append(tempRow)
            tempRow = []

        return Matrix(tempMat)

    def zeroes(self, m, n=-1):
        """Returns an m x n matrix of all zeroes."""

        tempRow = []
        tempMat = []

        if (n == -1):
            n = m

        for row in range(m):
            for col in range(n):
                tempRow.append(0.0)

            tempMat.append(tempRow)
            tempRow = []

        return Matrix(tempMat)

    def ref(self):
        """Returns the row echelon form (not reduced)."""
        tempMat = self.asList()

        # Find max pivot point
        for j in range(self.rows):
            maxRow = j

            for p in range(j + 1, self.rows):
                if abs(tempMat[p][j]) > abs(tempMat[maxRow][j]):
                    maxRow = p

            if abs(tempMat[maxRow][j]) < 10 ** -10:
                raise Exception("Error: matrix is singular and cannot be reduced.")

            (tempMat[j], tempMat[maxRow]) = (tempMat[maxRow], tempMat[j])

            # Elliminate column under pivot
            for p in range(j + 1, self.rows):
                c = tempMat[p][j] / tempMat[j][j]

                for col in range(j, self.columns):
                    tempMat[p][col] -= tempMat[j][col] * c

        return Matrix(tempMat)

    def det(self):
        """Returns the determinant of a matrix."""
        r = 1.0
        tempMat = self.asList()

        # Find max pivot point
        for j in range(self.rows):
            maxRow = j

            for p in range(j + 1, self.rows):
                if abs(tempMat[p][j]) > abs(tempMat[maxRow][j]):
                    maxRow = p
                    (tempMat[j], tempMat[maxRow]) = (tempMat[maxRow], tempMat[j])
                    r *= -1

            if abs(tempMat[maxRow][j]) < 10 ** -12:
                return 0.0

            # Elliminate column under pivot
            for p in range(j + 1, self.rows):
                c = tempMat[p][j] / tempMat[j][j]

                for col in range(j, self.columns):
                    tempMat[p][col] -= tempMat[j][col] * c

        # multiply the diagonals
        for j in range(self.rows):
            r *= tempMat[j][j]

        return r

    def gaussJordan(self):
        """Uses Gauss Jordan method of elimination to reduce current matrix."""
        tempMat = self.asList()

        for j in range(self.rows):
            maxRow = j

            for p in range(j, self.rows):
                if abs(tempMat[p][j]) > abs(tempMat[maxRow][j]):
                    maxRow = p

            if abs(tempMat[maxRow][j]) < 10 ** -10:
                raise Exception("Error: matrix is singular and cannot be reduced.")

            (tempMat[j], tempMat[maxRow]) = (tempMat[maxRow], tempMat[j])

            c = tempMat[j][j]

            for col in range(self.columns):
                tempMat[j][col] = tempMat[j][col] / c

            for i in range(self.rows):
                if i != j:
                    c = tempMat[i][j]
                    for col in range(self.columns):
                        tempMat[i][col] -= tempMat[j][col] * c

        return Matrix(tempMat)

    def gaussian(self):
        """Use gaussian elimination to reduce current matrix."""
        tempMat = self.asList()

        # Find max pivot point
        for j in range(self.rows):
            maxRow = j

            for p in range(j + 1, self.rows):
                if abs(tempMat[p][j]) > abs(tempMat[maxRow][j]):
                    maxRow = p

            if abs(tempMat[maxRow][j]) < 10 ** -10:
                raise Exception("Error: matrix is singular and cannot be reduced.")

            (tempMat[j], tempMat[maxRow]) = (tempMat[maxRow], tempMat[j])

            # Elliminate column under pivot
            for p in range(j + 1, self.rows):
                c = tempMat[p][j] / tempMat[j][j]

                for col in range(j, self.columns):
                    tempMat[p][col] -= tempMat[j][col] * c

        # Back substitute
        for j in range(self.rows - 1, -1, -1):
            c = tempMat[j][j]
            if c == 0:
                pass
            else:
                for p in range(j):
                    for col in range(self.columns - 1, j - 1, -1):
                        tempMat[p][col] -= tempMat[j][col] * tempMat[p][j] / c
                tempMat[j][j] /= c

                for col in range(self.rows, self.columns):
                    tempMat[j][col] /= c

        return Matrix(tempMat)

    def augment(self, b):
        """
        Augment the current matrix with a solution vector b.
        pre: b must be a one-dimensional list.
        """
        for row in range(self.rows):
            for col in range(self.columns):
                if col == self.columns - 1:
                    self.matrix[row].append(float(b[row]))

        self.columns += 1

        return self.matrix

    def inverse(self):
        """
        Find the inverse of a matrix by reducing the given matrix to the identity,
        the starting identity matrix becomes the inverse.
        """
        identity = Matrix().identity(self.columns)

        tempMat = self.asList()

        for j in range(self.rows):
            maxRow = j

            for p in range(j, self.rows):
                if abs(tempMat[p][j]) > abs(tempMat[maxRow][j]):
                    maxRow = p

            if abs(tempMat[maxRow][j]) < 10 ** -10:
                raise Exception("Error: matrix is singular and cannot be reduced.")

            (tempMat[j], tempMat[maxRow]) = (tempMat[maxRow], tempMat[j])
            (identity.matrix[j], identity.matrix[maxRow]) = (identity.matrix[maxRow], identity.matrix[j])

            c = tempMat[j][j]

            for col in range(self.columns):
                identity.matrix[j][col] = identity.matrix[j][col] / c
                tempMat[j][col] = tempMat[j][col] / c

            for i in range(self.rows):
                if i != j:
                    c = tempMat[i][j]
                    for col in range(self.columns):
                        identity.matrix[i][col] -= identity.matrix[j][col] * c
                        tempMat[i][col] -= tempMat[j][col] * c

        return identity

    def asList(self):
        """
        Make a copy of the matrix and store it in list form.
        Mostly for use in methods of self.
        """
        tempMat = []
        tempRow = []
        for row in range(self.rows):
            for col in range(self.columns):
                tempRow.append(self.matrix[row][col])

            tempMat.append(tempRow)
            tempRow = []

        return tempMat

    def meanVector(self):
        """Return an nx1 matrix of the mean column vectors of a matrix."""

        tempMat = []
        averages = []
        for col in range(self.columns):
            sum = 0
            for row in range(self.rows):
                sum += self.matrix[row][col]

            sum /= self.rows
            averages.append(sum)

        tempMat.append(averages)

        return Matrix(tempMat)

    def transpose(self):
        """Return the transpose of a matrix."""
        tempMat = []
        tempRow = []

        for col in range(self.columns):
            for row in range(self.rows):
                tempRow.append(self.matrix[row][col])
            tempMat.append(tempRow)
            tempRow = []

        return Matrix(tempMat)

    def getColumnVector(self, column):
        """Return one of the columns as a matrices."""
        tempMat = []
        tempRow = []

        for row in range(self.rows):
            tempRow.append(self.matrix[row][column])
            tempMat.append(tempRow)
            tempRow = []

        return Matrix(tempMat)

    def getColumnSumNorm(self):
        """Get the norm of a matrices in the form of a column sum norm."""
        colSum = 0
        maxColSum = 0
        for col in range(self.columns):
            for row in range(self.rows):
                colSum += abs(self.matrix[row][col])
            if colSum > maxColSum:
                maxColSum = colSum
            colSum = 0

        return maxColSum

    def getRowSumNorm(self):
        """Get the norm of a matrices in the form of a row sum norm."""
        rowSum = 0
        maxRowSum = 0
        for row in range(self.rows):
            for col in range(self.columns):
                rowSum += abs(self.matrix[row][col])
            if rowSum > maxRowSum:
                maxRowSum = rowSum
            rowSum = 0

        return maxRowSum

    def trace(self):
        """Calculate the trace of the matrix."""
        diagonalSum = 0

        for row in range(self.rows):
            diagonalSum += self.matrix[row][row]

        return diagonalSum

    def __add__(self, other):
        """Operator overloading for matrix addition."""
        tempMat = []
        tempRow = []

        if self.rows != other.rows or self.columns != other.columns:
            raise Exception("Error: you can only add matrices of the same dimensions.")
        else:
            for row in range(self.rows):
                for col in range(self.columns):
                    tempRow.append(0.0)
                tempMat.append(tempRow)
                tempRow = []

            for row in range(self.rows):
                for col in range(self.columns):
                    tempMat[row][col] = self.matrix[row][col] + other.matrix[row][col]

            return Matrix(tempMat)

    def __sub__(self, other):
        """Operator overloading for matrix subtraction."""
        tempMat = []
        tempRow = []
        if self.rows != other.rows or self.columns != other.columns:
            raise Exception("Error: you can only subtract matrices of the same dimensions.")
        else:
            for row in range(self.rows):
                for col in range(self.columns):
                    tempRow.append(0)
                tempMat.append(tempRow)
                tempRow = []

            for row in range(self.rows):
                for col in range(self.columns):
                    tempMat[row][col] = self.matrix[row][col] - other.matrix[row][col]

            return Matrix(tempMat)

    def __mul__(self, other):
        """
        If other is a matrix, perform matrix multiplication
        if other is a scalar, multiply each item in the matrix by a scalar.
        Conditions:
            -if input is a scalar, it must be an int or a float
                **SCALAR MUST COME AFTER MATRIX IN EXPRESSION**

            -if input is a matrix, the first matrix rows must match the
                second matrix columns.

        Resultant matrix of mult(m x n, n x p) will always be m x p.
        """
        total = 0
        tempMat = []
        tempRow = []
        if type(other) is int or type(other) is float:
            other = float(other)
            for row in range(self.rows):
                for col in range(self.columns):
                    tempRow.append(self.matrix[row][col] * other)

                tempMat.append(tempRow)
                tempRow = []

            return Matrix(tempMat)

        if type(other) is Matrix:

            if self.columns != other.rows:
                raise Exception("Error: the columns of matrix 1 must match the rows of matrix 2.")
            else:
                for selfRow in range(self.rows):
                    for otherCol in range(other.columns):
                        for otherRow in range(other.rows):
                            total += self.matrix[selfRow][otherRow] * other.matrix[otherRow][otherCol]

                        tempRow.append(total)
                        total = 0

                    tempMat.append(tempRow)
                    tempRow = []
        else:
            raise Exception("Error: invalid input type. Input must be an integer, float, or matrix")

        return Matrix(tempMat)

    def __div__(self, other):
        """
        If other is a matrix, perform matrix division.
        If other is an int or float: return the result of scaling the matrix by 1 / other.
        
        Conditions:
                -if input is a scalar, it must be an int or a float.
                         **SCALAR MUST COME AFTER MATRIX IN EXPRESSION**

                -if input is a matrix, the first matrix rows must match the
                         second matrix columns.
                                 
        Resultant matrix of mult(m x n, n x p) will always be m x p.
        """
        total = 0
        tempMat = []
        tempRow = []
        if type(other) is int or type(other) is float:
            other = float(other)
            for row in range(self.rows):
                for col in range(self.columns):
                    tempRow.append(self.matrix[row][col] / other)

                tempMat.append(tempRow)
                tempRow = []

            return Matrix(tempMat)

        if type(other) is Matrix:

            if self.columns != other.rows:
                raise Exception("Error: the columns of matrix 1 must match the rows of matrix 2.")
            else:

                # Resultant matrix of mult(m x n, n x p) will always be m x p
                for selfRow in range(self.rows):
                    for otherCol in range(other.columns):
                        for otherRow in range(other.rows):
                            total += self.matrix[selfRow][otherRow] / other.matrix[otherRow][otherCol]

                        tempRow.append(total)
                        total = 0

                    tempMat.append(tempRow)
                    tempRow = []
        else:
            raise Exception("Error: invalid input type. Input must be an integer, float, or matrix")

        return Matrix(tempMat)

    def covariance(self):
        """Return the covariance matrix of the current matrix."""
        meanVec = self.meanVector()

        covariant = Matrix([[0, 0], [0, 0]])

        copy = Matrix(self.matrix)

        for row in range(self.rows):
            copy.matrix[row][0] -= meanVec.matrix[0][0]
            copy.matrix[row][1] -= meanVec.matrix[0][1]
            tempVec = []
            tempVec.append(copy.matrix[row])
            tempVec = Matrix(tempVec)
            tempVec = tempVec.transpose() * tempVec
            covariant += tempVec
        covariant *= 1.0 / self.rows
        return covariant

    def leverrier(self):
        """Use Leverrier's method to fid the characteristic polynomial of a matrix."""
        coefficients = []
        Bn = Matrix(self.matrix)
        an = -Bn.trace()
        coefficients.append(an)

        for k in range(self.columns - 1, 0, -1):
            I = self.identity(self.columns)
            temp = Bn + I * an
            Bk = self * temp

            ak = -(Bk.trace() / (self.columns - k + 1))

            coefficients.append(ak)

            an = ak
            Bn = Bk

        return coefficients

    def powerMethod(self, y):
        """Use the power method to find the largest eigenvalue of a matrix."""
        results = []
        epsilon = 0.000001
        m = 200
        k = 0
        x = self * y

        valid = True

        while valid:

            tempRow = []
            y = x / x.getRowSumNorm()
            x = Matrix(self.matrix) * y
            mew = ((y.transpose() * x).matrix[0][0] / (y.transpose() * y).matrix[0][0])
            r = y * mew - x
            k += 1
            tempRow.append(k)
            tempRow.append(mew)
            tempRow.append(y.transpose().asList())
            tempRow.append(r.getRowSumNorm())

            results.append(tempRow)

            if ((r.getRowSumNorm() < epsilon) or (k > m)):
                valid = False

        return results

    def upperTriangularTest(self, B):
        """Determines if a matrix is upper triangular or not."""
        epsilon = 0.000001
        diagonal = 0
        for col in range(B.columns):
            for row in range(B.rows):
                if row == col:
                    for rowBelowDiagonal in range(diagonal, B.rows):
                        if B.matrix[rowBelowDiagonal][col] < epsilon:
                            return False

    def QR(self):
        """Use the QR Method to find all of the eigenvalues and eigenvectors of a matrix."""
        m = 300
        B = Matrix(self.matrix)
        upperTriangular = False
        i = 0
        results = []
        eigenvalues = []
        S = self.identity(self.columns)

        # Put matrix into upper triangular form
        while not upperTriangular and i < m:
            Q = self.identity(self.columns)

            for k in range(self.columns - 1):
                c = B.matrix[k][k] / (sqrt(pow(B.matrix[k][k], 2) + pow(B.matrix[k + 1][k], 2)))

                s = B.matrix[k + 1][k] / (sqrt(pow(B.matrix[k][k], 2) + pow(B.matrix[k + 1][k], 2)))

                P = self.identity(self.columns)
                P.matrix[k][k] = c
                P.matrix[k + 1][k + 1] = c
                P.matrix[k + 1][k] = -s
                P.matrix[k][k + 1] = s

                B = P * B
                Q = P * Q.transpose()
                Q = Q.transpose()
                S = S * Q

            B = B * Q
            i += 1
            upperTriangular = self.upperTriangularTest(B)

        # Handle cases for 2x2, 3x3, 4x4, and 5x5
        if self.columns == 2:
            m = Matrix([[B.matrix[0][0], B.matrix[0][1]], [B.matrix[1][0], B.matrix[1][1]]])
            eig = (m.trace() + sqrt(pow(m.trace(), 2) - 4 * m.det())) / 2
            eigenvalues.append(eig)
            eig = (m.trace() - sqrt(pow(m.trace(), 2) - 4 * m.det())) / 2
            eigenvalues.append(eig)
        else:
            m = B.matrix[0][0]
            eigenvalues.append(m)
            m = Matrix([[B.matrix[1][1], B.matrix[1][2]], [B.matrix[2][1], B.matrix[2][2]]])
            eig = (m.trace() + sqrt(pow(m.trace(), 2) - 4 * m.det())) / 2
            eigenvalues.append(eig)
            eig = (m.trace() - sqrt(pow(m.trace(), 2) - 4 * m.det())) / 2
            eigenvalues.append(eig)

            if self.columns == 4:
                m = B.matrix[3][3]
                eigenvalues.append(m)
            elif self.columns == 5:
                m = Matrix([[B.matrix[3][3], B.matrix[3][4]], [B.matrix[4][3], B.matrix[4][4]]])
                eig = (m.trace() + sqrt(pow(m.trace(), 2) - 4 * m.det())) / 2
                eigenvalues.append(eig)
                eig = (m.trace() - sqrt(pow(m.trace(), 2) - 4 * m.det())) / 2
                eigenvalues.append(eig)
        temp = []

        for i in range(S.rows):
            for j in range(S.columns):
                S.matrix[i][j] *= -1
        for i in range(len(eigenvalues)):
            temp.append(eigenvalues[i])
            temp.append(S.getColumnVector(i).asList())
            results.append(temp)
            temp = []
        return results


def test():
    print"TEST1 (imported from txt)"
    test = Matrix()
    test.importMatrix('PracticeData.txt')
    test.toString()

    print "TEST2 (list)"

    test2 = Matrix([[3, 3, -3, 3], [9, -6, 3, 9], [12, 3, -6, 27]])
    test2.toString()

    print "TEST1 + TEST2"

    addTest = test + test2
    addTest.toString()

    print "(TEST1 + TEST2) - TEST1: result should equal test2"
    subTest = addTest - test
    subTest.toString()

    print "3x4 ZERO MATRIX"
    testZero = Matrix().zeroes(3, 4)
    testZero.toString()

    print "3x3 IDENTITY MATRIX"
    testIdentity = Matrix().identity(3)
    testIdentity.toString()

    print"3x3 IDENTITY MATRIX * 3"
    scalarTest = testIdentity * 3
    scalarTest.toString()

    print "MULT BY IDENTITY: result should equal test2"
    multTest = Matrix()
    multTest = scalarTest * test
    multTest.toString()

    print "AUGMENT TESTING"
    testIdentity.augment([1, 2, 3])
    testIdentity.toString()

    print"GaussianTESTING"
    gaussianTest = Matrix([[3, 11, 0, 3], [4, 16, 19, 4], [1, 4, 5, 2]])
    gaussianTest = gaussianTest.gaussian()
    gaussianTest.toString()
    print
    gaussianTest2 = Matrix([[3, 8, 0, -4], [5, 15, 19, -2], [1, 3, 4, -4]])
    gaussianTest2 = gaussianTest2.gaussian()
    gaussianTest2.toString()

    print "Gauss Jordan Test. should equal matrix directly above"
    gjTest = Matrix([[3, 8, 0, -4], [5, 15, 19, -2], [1, 3, 4, -4]])
    gjTest = gjTest.gaussJordan()
    gjTest.toString()

    print "Determinant test1"
    test = Matrix()
    test.importMatrix('PracticeData.txt')
    print "ref test1"
    print test.det()
    test = test.ref()
    test.toString()

    print "Inverse Test1"
    test = Matrix([[1, 1, -1], [3, -2, 1], [4, 1, -2]])
    inverseTest = test.inverse()
    inverseTest.toString()

    print "Mean Vector Test1"
    test = Matrix([[1, 1, -1], [3, -2, 1], [4, 1, -2]])
    test = test.meanVector()
    test.toString()

    print "Transpose Test1"
    test = Matrix([[1], [2], [3], [4], [5]])
    test = test.transpose()
    test.toString()
    print
    test = test.transpose()
    test.toString()
    print
    test = Matrix([[1, 1, -1], [3, -2, 1], [4, 1, -2]])
    test = test.transpose()
    test.toString()

    print "Column Vector test"
    test = Matrix([[1, 1, -1], [3, -2, 1], [4, 1, -2]])
    col1 = test.getColumnVector(1)
    col1.toString()


def test2():
    print "Leverriers method test"
    test = Matrix([[1, -1, 0], [0, 2, -1], [-1, 0, 1]])
    test.toString()
    coefficients = test.leverrier()
    print coefficients

    print "Power Method test"
    test = Matrix([[-3.9, -0.6, -3.9, 0.4], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])
    coefficients = test.leverrier()
    print coefficients
    print
    powertest = test.powerMethod(Matrix([[0], [1], [0], [0]]))
    for i in range(len(powertest)):
        print powertest[i]
    print 'Power Method Test 2'
    test = Matrix([[6, -11, 6], [1, 0, 0], [0, 1, 0]])
    powertest = test.powerMethod(Matrix(([[0], [1], [0]])))
    for i in range(len(powertest)):
        print powertest[i]

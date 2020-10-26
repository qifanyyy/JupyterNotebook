"""
Strassen Algorithm implementation
Jeremy TRAN - Corentin DIEVAL
"""

import numpy as np
from math import sqrt
from math import log
import time


class ComputationService:
    # multiplication counter using strassen algorithm
    classical_mult_cnt = 0
    # multiplication counter using classical algorithm
    strassen_mult_cnt = 0
    # start of computing instant
    classical_comp_time = 0
    # computation time using strassen algorithm
    strassen_comp_time = 0
    # result matrix
    result = []

    def __init__(self, matrix_a, matrix_b):
        self.result = self.compute(matrix_a, matrix_b)

    def get_result(self):
        return self.result, self.strassen_comp_time, self.strassen_mult_cnt, self.classical_comp_time, self.classical_mult_cnt

    def compute(self, a, b):
        """
        compute(a, b) multiply two square matrix a and b of the same size
        and return the result matrix
        The computations are done following Strassen algorithm, then following classical matrices multiplication
        algorithm (Sum(AikBkj)).

        :param a matrix n x n, n > 0
        :param b matrix n x n, n > 0
        :return c the result matrix
        """
        # Storing size of matrices
        a_size = int(sqrt(a.size))
        b_size = int(sqrt(b.size))

        # Error handling
        if (a_size != b_size) or (not a_size or not b_size):
            return "Error: matrices to multiply must have the same size, and must not be empty."

        new_size = 0
        previous_size = a_size

        # Odd dimension matrices handling for Strassen algorithm
        if log(a_size) / log(2) % 1 != 0:
            a, b, new_size = self.complete_with_zeros(a, b, a_size)
            a_size = new_size

        print 'Request for computing', a_size, 'x', a_size, 'matrices multiplication.'

        # Compute result matrix using strassen algorithm implementation
        start_time = time.time()
        result = self.compute_using_strassen(a, b)

        self.strassen_comp_time = time.time() - start_time
        print 'Strassen computation realised in', self.strassen_comp_time, 'seconds.'

        # Remove added zeros rows and columns before starting classical algorithm
        if new_size != 0:
            self.result = self.remove_added_zeros(result, new_size, new_size - previous_size)
            a = self.remove_added_zeros(a, new_size, new_size - previous_size)
            b = self.remove_added_zeros(b, new_size, new_size - previous_size)
        else:
            self.result = result

        # Compute result matrix using classical algorithm implementation
        start_time = time.time()
        result = self.classical_compute(a, b)

        self.classical_comp_time = time.time() - start_time
        print 'Classical computation realised in', self.classical_comp_time, 'seconds.'

        # Result verification
        if not (result == self.result).all():
            return "Error: classical and strassen algorithm returned different results."

        return result

    def compute_using_strassen(self, a, b):
        """
        Compute matrices multiplication using strassen algorithm
        Each integer multiplication done is counted by the global variable counter

        :param a: a square matrix of size n^2k
        :param b: a square matrix of size n^2k
        :return: the matrix result of size n^2k
        """
        size = int(sqrt(a.size))
        # If a and b are matrix, split them into 4 blocks
        # and compute q1, ..., q7 recursively
        # then go down a recursion level
        # until reaching gateway condition (else)
        # then go back up to the first recursion level
        # calculating each level a11, ..., b22 using deeper recursion levels results
        if a.size != 1:
            if size != 2:
                # Compute Aij, Bij, matrices n/2 x n/2, n > 2
                a11, a12, a21, a22 = self.split_int_four(a, size)
                b11, b12, b21, b22 = self.split_int_four(b, size)
            else:
                a11, a12, a21, a22 = a[0][0], a[0][1], a[1][0], a[1][1]
                b11, b12, b21, b22 = b[0][0], b[0][1], b[1][0], b[1][1]

            # Compute qk recursively
            q1 = self.compute_using_strassen(a11 - a12, b22)
            q2 = self.compute_using_strassen(a21 - a22, b11)
            q3 = self.compute_using_strassen(a22, b11 + b21)
            q4 = self.compute_using_strassen(a11, b12 + b22)
            q5 = self.compute_using_strassen(a11 + a22, b22 - b11)
            q6 = self.compute_using_strassen(a11 + a21, b11 + b12)
            q7 = self.compute_using_strassen(a12 + a22, b21 + b22)

            # Compute Cij thanks to Strassen formulas
            c11 = q1 - q3 - q5 + q7
            c12 = q4 - q1
            c21 = q2 + q3
            c22 = - q2 - q4 + q5 + q6

            if size != 2:
                # Create an array of matrices n/2 x n/2 containing c11, c12, c21, and c22
                right = np.concatenate((c11, c21), axis=0)
                left = np.concatenate((c12, c22), axis=0)
                matrix = np.concatenate((right, left), axis=1)

            else:
                matrix = np.array([[c11, c12], [c21, c22]])

        # Gateway condition, deeper recursion level
        # If input are integers just multiply them
        # and increment global multiplication counter
        else:
            self.strassen_mult_cnt += 1
            return int(a) * int(b)

        return matrix

    def classical_compute(self, a, b):
        """
        Compute matrices multiplication using classical algorithm (AikBkj)
        Each integer multiplication done is counted by the global variable counter

        :param a: a square matrix of size n
        :param b: another square matrix of size n
        :return: the matrix result of size n
        """
        n = np.shape(a)[0]
        c = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                s = 0
                for k in range(n):
                    s += a[i][k] * b[k][j]
                    self.classical_mult_cnt += 1
                    c[i][j] = int(s)
        return c

    @staticmethod
    def split_int_four(matrix, size):
        four_matrices = []
        dsize = int(size/2)
        for i in range(0, size, dsize):
            for j in range(0, size, dsize):
                # split matrix in four square matrices of size size / 2,
                # following the order of strassen definitions a11, a12, a21, a22
                four_matrices.append(matrix[i:(dsize + i), j:(dsize + j)])
        return np.asarray(four_matrices)

    def complete_with_zeros(self, m1, m2, size):
        """
        Complete matrices which sizes are not 2^k form, k natural integer
        by adding to each of them a line and a column of zeros

        :param m1: a matrix (2n + 1) x (2n + 1), n > 1
        :param m2: another matrix (2n + 1) x (2n + 1), n > 1
        :param size: the size of m1 and m2
        :return: matrices m1 and m2 completed until their size are 2^k form
        """
        new_size = size
        while log(new_size) / log(2) % 1 != 0:
            new_size += 1
        return self.add_zeros_rows_and_columns(m1, size, new_size), self.add_zeros_rows_and_columns(m2, size, new_size), new_size

    @staticmethod
    def add_zeros_rows_and_columns(matrix, size, new_size):
        """
        Add (new_size - size) rows and columns of zeros to a matrix beginning by right bottom sides
        :param matrix: the matrix to be completed of zeros
        :param size: the matrix size
        :param new_size: the completed matrix size
        :return: the matrix with (new_size - size) rows and columns of zeros added
        """
        for i in range(0, new_size - size):
            zeros_line = np.array([np.zeros((size + i,), dtype=int)])
            zeros_column = np.zeros((size + i + 1, 1), dtype=int)
            # Add zeros line to the bottom of the matrix
            completed = np.concatenate((matrix, zeros_line), axis=0)
            # Add zeros column to the bottom of the matrix and return it
            new_matrix = np.concatenate((completed, zeros_column), axis=1)
            matrix = new_matrix

        return matrix

    @staticmethod
    def remove_added_zeros(matrix, actual_size, nb_rows_to_remove):
        """
        Remove nb_rows_to_remove rows and a columns of zeros to a matrix beginning by right and bottom sides
        :param matrix: the matrix to be modified
        :param actual_size: the size of the matrix to be modified
        :param nb_rows_to_remove: the number of rows and columns to remove
        :return: the matrix with a row and a column of zeros added
        """
        for i in range(actual_size - 1, actual_size - nb_rows_to_remove - 1, -1):
            matrix = np.delete(matrix, i, axis=0)
            matrix = np.delete(matrix, i, axis=1)

        return matrix


# if __name__ == '__main__':
#     matrix_a = np.array([
#       [1, 2, 0, 1],
#       [3, 4, -1, 1],
#       [1, 0, 1, 2],
#       [0, 1, 3, 4]
#     ])
#     a = np.array([[1, 2], [3, 4]])
#     matrix_b = np.array([
#       [1, -1, 0, 1],
#       [2,  0, 1, 1],
#       [0, 1, 1, 0],
#       [1, 0, 0, -1]
#     ])
#     service = ComputationService(matrix_a, matrix_b)
#     # print matrix_a
#     # print service.split_int_four(a, 2)
#     result, strassen_comp_time, strassen_mult_cnt, classical_comp_time, classical_mult_cnt = service.get_result()
#     print result
#     print 'Strassen', '\n', 'Number of multiplications done: ', strassen_mult_cnt, '\n', 'Compute time: ', strassen_comp_time
#     print 'Classical', '\n', 'Number of multiplications done: ', classical_mult_cnt, '\n', 'Compute time: ', classical_comp_time
#
#     # Matrix seen in class
#     matrix_a = np.array([
#         [1, 2, 0, 1],
#         [3, 4, -1, 1],
#         [1, 0, 1, 2],
#         [0, 1, 3, 4]
#     ])
#     # Matrix seen in class
#     matrix_b = np.array([
#         [1, -1, 0, 1],
#         [2, 0, 1, 1],
#         [0, 1, 1, 0],
#         [1, 0, 0, -1]
#     ])
#     # Call computation service
#     service = ComputationService(matrix_a, matrix_b)
#
#     result, strassen_comp_time, strassen_mult_cnt, classical_comp_time, classical_mult_cnt = service.get_result()
#     # Print result for verification
#     print 'Number of multiplications done: '
#     print 'Classical:', classical_mult_cnt, '\n', 'Strassen: ', strassen_mult_cnt
#     print 'Result for matrices seen in class', result
#
#     # Benchmark
#     print '\n', '##### BENCHMARK FROM 2 TO 32, OFFSET: 2'
#     for i in range(2, 33, 2):
#         matrix_a = np.random.rand(i, i)
#         matrix_b = np.random.rand(i, i)
#         service = ComputationService(matrix_a, matrix_b)
#         result, strassen_comp_time, strassen_mult_cnt, classical_comp_time, classical_mult_cnt = service.get_result()
#         print 'Number of multiplications done: '
#         print 'Classical:', classical_mult_cnt, '\n', 'Strassen: ', strassen_mult_cnt
#
#     print '\n', '##### BENCHMARK FROM 64 AND 128'
#     for i in range(64, 129, 128):
#         matrix_a = np.random.rand(i, i)
#         matrix_b = np.random.rand(i, i)
#         service = ComputationService(matrix_a, matrix_b)
#         result, strassen_comp_time, strassen_mult_cnt, classical_comp_time, classical_mult_cnt = service.get_result()
#         print 'Number of multiplications done: '
#         print 'Classical:', classical_mult_cnt, '\n', 'Strassen: ', strassen_mult_cnt
#
#     print '\n', '##### BENCHMARK FROM 256 AND 512'
#     for i in range(256, 513, 256):
#         matrix_a = np.random.rand(i, i)
#         matrix_b = np.random.rand(i, i)
#         service = ComputationService(matrix_a, matrix_b)
#         result, strassen_comp_time, strassen_mult_cnt, classical_comp_time, classical_mult_cnt = service.get_result()
#         print 'Number of multiplications done: '
#         print 'Classical:', classical_mult_cnt, '\n', 'Strassen: ', strassen_mult_cnt
# -*- coding: utf-8 -*-

from numpy import asarray
import math

ENERGY_LEVEL = [100, 113, 110, 85, 105, 102, 86, 63,
                81, 101, 94, 106, 101, 79, 94, 90, 97]


# ==============================================================

# The brute force method to solve first problem
def find_significant_energy_increase_brute(A):
    """
    Return a tuple (i,j) where A[i:j] is
    the most significant energy increase period.
    time complexity = O(n^2)
    """

    # get the daily change array from ENERGY_LEVEL
    daily_change = [0 for i in range(0, len(ENERGY_LEVEL))]
    for i in range(1, len(ENERGY_LEVEL)):
        daily_change[i] = ENERGY_LEVEL[i] - ENERGY_LEVEL[i - 1]

    array_len = len(daily_change)
    max_sum = -9999
    tuple0 = (1, 1)

    # find different array lengths for each element
    for i in range(array_len):
        sum = 0
        for j in range(i, array_len):
            sum += daily_change[j]
            if max_sum < sum:
                max_sum = sum
                tuple0 = (i - 1, j)
    return tuple0


# ==============================================================

# The recursive method to solve first problem
def find_significant_energy_increase_recursive(A):
    """
    Return a tuple (i,j) where A[i:j] is
    the most significant energy increase period.
    time complexity = O (n logn)
    """
    # get the daily change array from ENERGY_LEVEL
    daily_change = [0 for i in range(0, len(ENERGY_LEVEL))]
    for i in range(1, len(ENERGY_LEVEL)):
        daily_change[i] = ENERGY_LEVEL[i] - ENERGY_LEVEL[i - 1]

    array_len = len(daily_change)
    # recursively updating the max sub-array and it's locations
    tuple0 = find_maximum_subarray(daily_change, 0, array_len - 1)
    tuple1 = (tuple0[0] - 1, tuple0[1])  # adjust the output result
    return tuple1


# main helper function for find_significant_energy_increase_recursive(A)
def find_maximum_subarray(A, low, high):
    # base case
    if low == high:
        return (low, high, A[low])

    # recursively updating the max sub-array and it's locations
    mid = math.floor((low + high) / 2)
    left_max = find_maximum_subarray(A, low, mid)
    right_max = find_maximum_subarray(A, mid + 1, high)
    crossing_max = find_max_crossing_subarray(A, low, mid, high)
    if left_max[2] >= right_max[2] and left_max[2] >= crossing_max[2]:
        return left_max
    if right_max[2] >= left_max[2] and right_max[2] >= crossing_max[2]:
        return right_max
    else:
        return crossing_max


# helper function, find crossing subarray
def find_max_crossing_subarray(A, low, mid, high):
    left_sum = -9999
    right_sum = -9999
    sum = 0
    left_max = low
    right_max = high
    for i in range(mid, low - 1, -1):
        sum += A[i]
        if left_sum < sum:
            left_sum = sum
            left_max = i
    sum = 0
    for i in range(mid + 1, high):
        sum += A[i]
        if right_sum < sum:
            right_sum = sum
            right_max = i
    return (left_max, right_max, left_sum + right_sum)


# ==============================================================

# The iterative method to solve first problem
def find_significant_energy_increase_iterative(A):
    """
    Return a tuple (i,j) where A[i:j] is
     the most significant energy increase period.
    time complexity = O(n)
    """

    # get the daily change array from ENERGY_LEVEL
    daily_change = [0 for i in range(0, len(ENERGY_LEVEL))]
    for i in range(1, len(ENERGY_LEVEL)):
        daily_change[i] = ENERGY_LEVEL[i] - ENERGY_LEVEL[i - 1]

    array_len = len(daily_change)
    max_sum = -9999
    sum = 0
    start = 1
    left = 1  # left position for max subarray
    right = 1  # right position for max subarray

    for i in range(array_len):
        sum += daily_change[i]
        if max_sum < sum:
            left = start
            max_sum = sum
            right = i
        if sum < 0:
            sum = 0
            start = i + 1
    tuple0 = (left - 1, right)
    print(tuple0)
    return tuple0


# ==============================================================
# ==============================================================

# The Strassen Algorithm to do the matrix multiplication
def square_matrix_multiply_strassens(A, B):
    """
    Return the product AB of matrix multiplication.
    Assume len(A) is a power of 2
    """

    A = asarray(A)

    B = asarray(B)

    assert A.shape == B.shape

    assert A.shape == A.T.shape

    assert (len(A) & (len(A) - 1)) == 0, "A is not a power of 2"

    n = len(A)
    half_size = int(n / 2)

    # base case
    if n == 1:
        return A * B

    # initialization
    a11 = [[0 for j in range(0, half_size)] for i in range(0, half_size)]
    a12 = [[0 for j in range(0, half_size)] for i in range(0, half_size)]
    a21 = [[0 for j in range(0, half_size)] for i in range(0, half_size)]
    a22 = [[0 for j in range(0, half_size)] for i in range(0, half_size)]
    b11 = [[0 for j in range(0, half_size)] for i in range(0, half_size)]
    b12 = [[0 for j in range(0, half_size)] for i in range(0, half_size)]
    b21 = [[0 for j in range(0, half_size)] for i in range(0, half_size)]
    b22 = [[0 for j in range(0, half_size)] for i in range(0, half_size)]

    # copy values from original array to subarrays
    for row in range(0, half_size):
        for col in range(0, half_size):
            a11[row][col] = A[row][col]
            a12[row][col] = A[row][col + half_size]
            a21[row][col] = A[row + half_size][col]
            a22[row][col] = A[row + half_size][col + half_size]
            b11[row][col] = B[row][col]
            b12[row][col] = B[row][col + half_size]
            b21[row][col] = B[row + half_size][col]
            b22[row][col] = B[row + half_size][col + half_size]

    # part of Strassens' method
    s1 = add(a11, a22)
    s2 = add(b11, b22)
    s3 = add(a21, a22)
    s4 = subtract(b12, b22)
    s5 = subtract(b21, b11)
    s6 = add(a11, a12)
    s7 = subtract(a21, a11)
    s8 = add(b11, b12)
    s9 = subtract(a12, a22)
    s10 = add(b21, b22)

    # another part of Strassens' method
    p1 = square_matrix_multiply_strassens(s1, s2)
    p2 = square_matrix_multiply_strassens(s3, b11)
    p3 = square_matrix_multiply_strassens(a11, s4)
    p4 = square_matrix_multiply_strassens(a22, s5)
    p5 = square_matrix_multiply_strassens(s6, b22)
    p6 = square_matrix_multiply_strassens(s7, s8)
    p7 = square_matrix_multiply_strassens(s9, s10)

    # last part of Strassens' method
    c12 = add(p3, p5)  # c12 = p3 + p5
    c11 = add(subtract(add(p1, p4), p5), p7)  # c11 = p1 + p4 - p5 + p7
    c21 = add(p2, p4)  # c21 = p2 + p4
    c22 = add(subtract(add(p1, p3), p2), p6)  # c22 = p1 + p3 - p2 + p6

    # combine all four subarrays to one
    c = [[0 for j in range(0, n)] for i in range(0, n)]
    for i in range(0, half_size):
        for j in range(0, half_size):
            c[i][j] = c11[i][j]
            c[i][j + half_size] = c12[i][j]
            c[i + half_size][j] = c21[i][j]
            c[i + half_size][j + half_size] = c22[i][j]
    return c


# Helper function. Adding two matrix
def add(A, B):
    n = len(A)
    c = [[0 for j in range(0, n)] for i in range(0, n)]
    for i in range(0, n):
        for j in range(0, n):
            c[i][j] = A[i][j] + B[i][j]
    return c


# Helper function. Subtracting two matrix
def subtract(A, B):
    n = len(A)
    c = [[0 for j in range(0, n)] for i in range(0, n)]
    for i in range(0, n):
        for j in range(0, n):
            c[i][j] = A[i][j] - B[i][j]
    return c


# ==============================================================

# Calculate the power of a matrix in O(k)
def power_of_matrix_navie(A, k):
    """
    Return A^k.
    time complexity = O(k)
    """

    # base case
    if k == 1:
        return A

    # multiply one by one
    matrix = []
    for i in range(1, k):
        if i == 1:
            matrix = square_matrix_multiply_strassens(A, A)
        else:
            matrix = square_matrix_multiply_strassens(A, matrix)
    return matrix


# ==============================================================

# Calculate the power of a matrix in O(log k)
def power_of_matrix_divide_and_conquer(A, k):
    """
    Return A^k.
    time complexity = O(log k)
    """
    # NOTE: This algorithm only work when power is 2^n.
    # Works fine when k = 2, 4, 8
    # Not working when k = 3, 5, 6, 7, 9, 10

    # base case
    if k == 1:
        return A
    if k == 2:
        A = square_matrix_multiply_strassens(A, A)
        return A

    # to achieve O(log k) complexity, use recurrence with memorization
    if k % 2 == 1:
        matrix = power_of_matrix_divide_and_conquer(A, (k - 1) / 2)
        matrix = square_matrix_multiply_strassens(matrix, A)
    else:
        matrix = power_of_matrix_divide_and_conquer(A, k / 2)
    return square_matrix_multiply_strassens(matrix, matrix)


# ==============================================================
def test():
    assert (find_significant_energy_increase_brute(ENERGY_LEVEL) == (7, 11))
    assert (find_significant_energy_increase_recursive
            (ENERGY_LEVEL) == (7, 11))
    assert (find_significant_energy_increase_iterative
            (ENERGY_LEVEL) == (7, 11))
    assert((square_matrix_multiply_strassens([[0, 1], [1, 1]],
                                             [[0, 1], [1, 1]]) ==
                                             asarray([[1, 1], [1, 2]])).all())
    assert((power_of_matrix_navie([[0, 1], [1, 1]], 3) ==
                                    asarray([[1, 2], [2, 3]])).all())
    assert((power_of_matrix_divide_and_conquer([[0, 1], [1, 1]], 4) ==
                                               asarray([[2, 3], [3, 5]])).all())

    # test and print
    tuple0 = find_significant_energy_increase_brute(ENERGY_LEVEL)
    print("Test find_significant_energy_increase_brute():")
    print(tuple0)
    tuple0 = find_significant_energy_increase_recursive(ENERGY_LEVEL)
    print("Test find_significant_energy_increase_recursive():")
    print(tuple0)
    tuple0 = find_significant_energy_increase_iterative(ENERGY_LEVEL)
    print("Test find_significant_energy_increase_iterative():")
    print(tuple0)
    matrix = square_matrix_multiply_strassens([[0, 1], [1, 1]], [[0, 1], [1, 1]])
    print("Test square_matrix_multiply_strassens([[0, 1], [1, 1]], [[0, 1], [1, 1]]):")
    print(matrix)
    matrix = power_of_matrix_navie([[0, 1], [1, 1]], 3)
    print("Test power_of_matrix_navie([[0, 1], [1, 1]], 3):")
    print(matrix)
    matrix = power_of_matrix_divide_and_conquer([[0, 1], [1, 1]], 4)
    print("Test power_of_matrix_divide_and_conquer([[0, 1], [1, 1]], 4):")
    print(matrix)


if __name__ == '__main__':
    test()

# ==============================================================

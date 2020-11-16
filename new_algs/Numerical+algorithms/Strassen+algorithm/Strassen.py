import numpy as np
import time

def default_matrix_multiplication(a, b):
    """
    Only for 2x2 matrices
    """
    if len(a) != 2 or len(a[0]) != 2 or len(b) != 2 or len(b[0]) != 2:
        raise Exception('Matrices should be 2x2!')
    # print(a[0][0] * b[0][1] + a[0][1] * b[1][1])
    new_matrix = [[a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
                  [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]]]

    return new_matrix


def matrix_addition(matrix_a, matrix_b):
    # print(matrix_a)
    return [[matrix_a[row][col] + matrix_b[row][col]
             for col in range(len(matrix_a[row]))] for row in range(len(matrix_a))]


def matrix_subtraction(matrix_a, matrix_b):
    return [[matrix_a[row][col] - matrix_b[row][col]
             for col in range(len(matrix_a[row]))] for row in range(len(matrix_a))]


def split_matrix(a):
    """
    Given a matrix, return the TOP_LEFT, TOP_RIGHT, BOT_LEFT and BOT_RIGHT quadrant
    """
    if len(a) % 2 != 0 or len(a[0]) % 2 != 0:
        raise Exception('Odd matrices are not supported!')

    matrix_length = len(a)
    mid = matrix_length // 2
    top_left = [[a[i][j] for j in range(mid)] for i in range(mid)]
    bot_left = [[a[i][j] for j in range(mid)] for i in range(mid, matrix_length)]

    top_right = [[a[i][j] for j in range(mid, matrix_length)] for i in range(mid)]
    bot_right = [[a[i][j] for j in range(mid, matrix_length)] for i in range(mid, matrix_length)]

    return top_left, top_right, bot_left, bot_right


def get_matrix_dimensions(matrix):
    return len(matrix), len(matrix[0])


def strassen(matrix_a, matrix_b):
    if get_matrix_dimensions(matrix_a) != get_matrix_dimensions(matrix_b):
        raise Exception(f'Both matrices are not the same dimension! \nMatrix A:{matrix_a} \nMatrix B:{matrix_b}')
    if get_matrix_dimensions(matrix_a) == (2, 2):
        return default_matrix_multiplication(matrix_a, matrix_b)

    A, B, C, D = split_matrix(matrix_a)
    E, F, G, H = split_matrix(matrix_b)

    p1 = strassen(A, matrix_subtraction(F, H))
    p2 = strassen(matrix_addition(A, B), H)
    p3 = strassen(matrix_addition(C, D), E)
    p4 = strassen(D, matrix_subtraction(G, E))
    p5 = strassen(matrix_addition(A, D), matrix_addition(E, H))
    p6 = strassen(matrix_subtraction(B, D), matrix_addition(G, H))
    p7 = strassen(matrix_subtraction(A, C), matrix_addition(E, F))

    top_left = matrix_addition(matrix_subtraction(matrix_addition(p5, p4), p2), p6)
    top_right = matrix_addition(p1, p2)
    bot_left = matrix_addition(p3, p4)
    bot_right = matrix_subtraction(matrix_subtraction(matrix_addition(p1, p5), p3), p7)
    # construct the new matrix from our 4 quadrants
    new_matrix = []
    for i in range(len(top_right)):
        new_matrix.append(top_left[i] + top_right[i])
    for i in range(len(bot_right)):
        new_matrix.append(bot_left[i] + bot_right[i])
    return new_matrix

def native(m1, m2):
    result = []
    for m in range(len(m1)):
        temp = []
        for n in range(len(m1[0])):
            temp.append(0)
        result.append(temp)
    # print(np.array(result))
    for i in range(len(m1)):
        for j in range(len(m2[0])):
            for k in range(len(m2)):
                result[i][j] += m1[i][k] * m2[k][j]
    return result



# tester

# m_1 = [
#         [1, 2],
#         [1, 2]]
#
# m_2 = [
#         [5, 6],
#         [5, 6]]

# m_1 = [
#     [10, 9, 4, 3],
#     [8, 3, 4, 1],
#     [93, 1, 9, 3],
#     [2, 2, 7, 6]]
#
# m_2 = [
#     [4, 5, 3, 5],
#     [4, 1, 2, 1],
#     [9, 8, 3, 5],
#     [6, 3, 7, 9]]

# m_1 = np.random.randint(10, size=(2,2))
# m_2 = np.random.randint(10, size=(2,2))

# m_1 = np.random.randint(10, size=(4,4))
# m_2 = np.random.randint(10, size=(4,4))
#
# m_1 = np.random.randint(10, size=(8,8))
# m_2 = np.random.randint(10, size=(8,8))

# m_1 = np.random.randint(10, size=(16,16))
# m_2 = np.random.randint(10, size=(16,16))
#
# m_1 = np.random.randint(10, size=(32,32))
# m_2 = np.random.randint(10, size=(32,32))
#
# m_1 = np.random.randint(10, size=(64,64))
# m_2 = np.random.randint(10, size=(64,64))
#
# m_1 = np.random.randint(10, size=(128,128))
# m_2 = np.random.randint(10, size=(128,128))
#
# m_1 = np.random.randint(10, size=(256,256))
# m_2 = np.random.randint(10, size=(256,256))
#
# m_1 = np.random.randint(10, size=(512,512))
# m_2 = np.random.randint(10, size=(512,512))
#
m_1 = np.random.randint(10, size=(1024,1024))
m_2 = np.random.randint(10, size=(1024,1024))




start0 = time.time()
np.array(native(m_1, m_2))
end0 = time.time()
print("The native method takes " + str(end0 - start0))


start1 = time.time()
np.array(strassen(m_1, m_2))
end1 = time.time()
print("The Strassen method takes " + str(end1 - start1))


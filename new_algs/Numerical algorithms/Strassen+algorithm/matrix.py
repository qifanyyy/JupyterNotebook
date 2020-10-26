import numpy as np


def main():

    # X and Y are n x n square matrices of equal size

    # X = np.array([[1, 2], [3, 4]])
    # Y = np.array([[5, 6], [7, 8]])
    # result = strassen(X,Y) 
    # print(result)

    X = np.array([[1,2,3], [4,5,6], [7,8,9]])
    Y = np.array([[2,3,4], [5,6,7], [8,9,1]])
    # X = padding(X)
    # print(X)
    print(strassen(X,Y))

    # X = np.array([[1,2,3,7], [4,5,6,1], [7,8,9,4], [2,4,6,7]])
    # Y = np.array([[2,3,4,8], [5,6,7,3], [8,9,2,1], [1,7,3,5]])
    # print(strassen(X,Y))

    # X = np.array([[1,2,3,7,5], [4,5,6,1,8], [7,8,9,4,2], [2,4,6,7,3], [2,5,7,2,6]])
    # print(X)
    # a, b, c, d = split(X)
    # check = combine(a, b, c, d)
    # print(check)


def padding(matrix):
    row, col = matrix.shape
    padding_row = np.zeros((1, col))
    matrix = np.vstack((matrix, padding_row))
    padding_col = np.zeros((row + 1, 1))
    matrix = np.hstack((matrix, padding_col))
    return matrix


def strassen(X, Y):
    # base case
    if len(X) == 1 or len(Y) == 1:
        return X * Y

    # padding rows and cols of zero if size of nxn matrices is odd
    # https://cs.stackexchange.com/questions/97998/strassens-matrix-multiplication-algorithm-when-n-is-not-a-power-of-2
    if X.size % 2 != 0:
        X = padding(X)
    if Y.size % 2 != 0:
        Y = padding(Y)
    
    # divide into smaller matrices
    a, b, c, d = split(X)
    e, f, g, h = split(Y)

    # recursively compute the seven products from stressen algorithum
    p1 = strassen(a, f - h)   
    p2 = strassen(a + b, h)         
    p3 = strassen(c + d, e)         
    p4 = strassen(d, g - e)         
    p5 = strassen(a + d, e + h)         
    p6 = strassen(b - d, g + h)   
    p7 = strassen(a - c, e + f) 

    # do the necessary additions 
    c11 = p5 + p4 - p2 + p6   
    c12 = p1 + p2            
    c21 = p3 + p4             
    c22 = p1 + p5 - p3 - p7
    
    # works when n is even but not when n is odd, due to hstack and vstack limitation
    # hstack cannot stack two matrices with different no. of rows and vstack cannot stack two matrices with different no. of columns
    # c = np.vstack((np.hstack((c11, c12)), np.hstack((c21, c22))))  
    c = combine(c11, c12, c21, c22)
    return c


def combine(c11, c12, c21, c22):
    # find the no. of rows and cols of the inputs
    row11 = row12 = row21 = row22 = 0
    col11 = col12 = col21 = col22 = 0
    if c11.size:
        row11, col11 = c11.shape
    if c12.size:
        row12, col12 = c12.shape
    if c21.size:
        row21, col21 = c21.shape
    if c22.size:
        row22, col22 = c22.shape

    # calculate the no. of rows and cols of the final matrix c
    c_row = max(row11 + row21, row12 + row22)
    c_col = max(col11 + col12, col21 + col22)

    c_list = []

    c11_list = c11.tolist()
    c12_list = c12.tolist()
    c21_list = c21.tolist()
    c22_list = c22.tolist()

    # arrange the final matrix c as a 1D array
    for i in range(max(row11, row12)):
        if c11.size:
            c_list.extend(c11_list[i])
        if c12.size:
            c_list.extend(c12_list[i])
    for i in range(max(row21, row22)):
        if c21.size:
            c_list.extend(c21_list[i])
        if c22.size:
            c_list.extend(c22_list[i])

    # reshape c from 1D array to c_row x c_col 2D array
    c = np.array(c_list).reshape(c_row, c_col)

    return c


def split(matrix):
    row, col = matrix.shape
    row =  row // 2
    col = col // 2
    a = matrix[:row, :col]
    b = matrix[:row, col:]
    c = matrix[row:, :col]
    d = matrix[row:, col:]
    return a, b, c, d


if __name__ == "__main__":
    main()
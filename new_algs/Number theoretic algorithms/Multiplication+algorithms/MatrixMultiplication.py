def print_matrix(matrix):
    """
    Print clearly matrix

    Args:
         matrix (list): Matrix reference that will be printed
    """

    rows = len(matrix)
    columns = len(matrix[0])

    for i in range(rows):
        for j in range(columns):
            print(matrix[i][j], end= (', ' if j != columns-1 else '\n'))


def fill_matrix(rows, columns, matrix):
    """
    Fill matrix according rows and columns

    Args:
        rows    (int): Number of rows to scan correctly
        columns (int): Number of columns to scan correctly
        matrix  (list): Matrix reference that will be filled
    """
    for i in range(rows):
        row = []
        for j in range(columns):
            row.append(int(input('[{},{}]: '.format(i, j))))

        matrix.append(row)


matrix_1 = []
matrix_2 = []
matrix_3 = []

ij_1 = [int(x) for x in input('1: [i,j]').split(',')]
ij_2 = [int(x) for x in input('2: [i,j]').split(',')]

print('Fill first matrix:')
fill_matrix(ij_1[0], ij_1[1], matrix_1)

print('Fill second matrix:')
fill_matrix(ij_2[0], ij_2[1], matrix_2)

if ij_1[1] != ij_2[0]:
    print('[warning] Columns number of first matrix need to be equals rows number of second matrix.')

else:
    for i1 in range(ij_1[0]):
        row = []
        for j2 in range(ij_2[1]):
            sum = 0
            for i2 in range(ij_2[0]):
                sum += matrix_1[i1][i2] * matrix_2[i2][j2]

            row.append(sum)
        matrix_3.append(row)

    print('Result: ')
    print_matrix(matrix_3)


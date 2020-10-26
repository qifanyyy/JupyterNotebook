import numpy as np
import string
import textwrap
import math

from extended_euclid import multiplicative_inverse

m = 4
test_ciphertext = "!LPUMYAIJ?.MPA.DVRFUTNRUZYEFM?QVKJTOBTDRIAN!?SLQBKESZOSFRAAWYPI.VBOLLMWAWEMQ.JYBOITGNJRIFYGEGIBC?RB?UN?MORI,"

p_map = {}
for n, l in enumerate(string.ascii_uppercase):
    p_map[l] = n
p_map.update({',': 26, '.': 27, '?': 28, '!': 29, ' ': 30})

c_map = {c: p for p, c in p_map.items()}

plaintexts = ['CTRL', 'CAPS', 'HOME', 'PGUP']
ciphertexts = ['HGPP', 'HOFL', 'TTSI', 'DACR']


def convert_to_row(text):
    """
    :param text:
    :return:
    """
    return np.array([p_map[p] for p in text], dtype=np.int64)


def convert_to_matrix(texts):
    """
    :param texts:
    :return: matrix
    """
    matrix = []
    for text in texts:
        row = convert_to_row(text)
        matrix.append(row)
    return np.array(matrix, dtype=np.int64)


def encrypt(plaintext, key):
    """
    :param plaintext:
    :param key:
    :return:
    """
    p = convert_to_row(plaintext)
    c = np.dot(p, key) % 31
    return ''.join([c_map[n] for n in c])


def decrypt(ciphertext, key):
    """
    :param ciphertext:
    :param key:
    :return:
    """
    c = np.array([p_map[c] for c in ciphertext], dtype=np.int64)
    p = np.dot(c, key) % 31
    return ''.join([c_map[n] for n in p])


def sub_matrix(matrix, i, j):
    """
    Return sub-matrix formed by deleting jth
    row and ith column
    :param matrix:
    :param i:
    :param j:
    :return:
    """
    tmp = np.delete(matrix, j, 0)
    return np.delete(tmp, i, 1)


def sub_determinant(matrix, i, j, mod=31):
    """
    Returns sub-determinant formed by deleting the
    jth row and ith column of A, mod 31
    :param matrix:
    :param i: column index
    :param j: row index
    :param mod: mod (optional)
    :return: sub-determinant
    """
    sm = sub_matrix(matrix, i, j)
    return int(round(np.linalg.det(sm))) % mod




def textbook_hill_cipher_inverse():
    K = np.array([[17, 17, 5],
                  [21, 18, 21],
                  [2, 2, 19]])

    print(K)
    det_K = int(round(np.linalg.det(K))) % 26
    print("Determinant of K = ", det_K)
    m_inv = multiplicative_inverse(det_K, 26) % 26
    print("(det K)^-1 mod 26 = ", m_inv)

    inverse = [[] for _ in range(3)]
    print(inverse)
    for a in range(3):
        for b in range(3):
            inverse[a].append(m_inv * (-1) ** (a + b) * sub_determinant(K, a, b, 26))

    inverse = np.array(inverse) % 26
    print("K^-1 = \n", inverse)
    print("K * K^-1 = \n", np.dot(K, inverse) % 26)



def main():
    X = convert_to_matrix(plaintexts)
    Y = convert_to_matrix(ciphertexts)

    print("X =")
    print(X)
    print("Y =")
    print(Y)


    det_X = int(round(np.linalg.det(X))) % 31
    print("Determinant of X =", det_X)
    m_inv = multiplicative_inverse(det_X, 31) % 31
    print("(det X)^-1 mod 31 =", m_inv)

    X_inv = [[] for _ in range(m)]
    for i in range(m):
        for j in range(m):
            X_inv[i].append(m_inv * (-1) ** (i + j) * sub_determinant(X, i, j))

    X_inv = np.array(X_inv) % 31

    print("X^-1 = \n", X_inv)
    print("X.X^-1 = \n", np.dot(X, X_inv) % 31)
    K = np.dot(X_inv, Y) % 31



    print("K = \n", K)

    det_K = int(round(np.linalg.det(K))) % 31
    print("Determinant of K =", det_X)
    m_inv = multiplicative_inverse(det_K, 31) % 31
    print("(det K)^-1 mod 31 =", m_inv)

    K_inv = [[] for _ in range(m)]
    for i in range(m):
        for j in range(m):
            K_inv[i].append(m_inv * (-1) ** (i + j) * sub_determinant(K, i, j))

    K_inv = np.array(K_inv) % 31
    print("K^-1 = \n", K_inv)
    print("K.K^-1 = \n", np.dot(K, K_inv) % 31)

    debug = False
    if debug:
        for p in plaintexts:
            print(encrypt(p, K))

        for c in ciphertexts:
            print(decrypt(c, K_inv))

    test_plaintext = ""
    for c in textwrap.wrap(test_ciphertext, m):
        test_plaintext += decrypt(c, K_inv)

    print("TEST PLAINTEXT:")
    print(test_plaintext)


if __name__ == "__main__":
    main()

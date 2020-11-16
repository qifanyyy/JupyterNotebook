import numpy as np

def euclid_extended(list, coord = None):
    """Given list of integers, returns GCD and list of Bezout coefficients.
    Uses a version of the extended Euclidean algorithm that utilizes
    coordinate matrices (from linear algebra)."""
    n = len(list)
    assert n > 0

    if coord == None: # coord is identity matrix by default
        coord = np.identity(n)

    nonzeros = [x for x in list if x != 0]

    if len(nonzeros) == 1: #base case: only one non-zero element in list
        nz = nonzeros[0]
        i_nz = list.index(nz)
        return (nz, list(coord[:, i_nz])) #gcd and coordinates of gcd
                                          #in terms of original list
    else: #recursive call on new modified version of list
        minnz = min(nz)
        i_minnz = list.index(minnz)
        A = np.zeros(shape=(n, n)) #coordinates of new version of list in terms
        A[i_minnz][i_minnz] = 1 #of immediately previous version

        for i in [j for j in range(n) if j != i_minnz]: #modify list
            d = list[i] // minnz
            q = list[i] % minnz
            list[i] = q

            A[i][i] = 1
            A[i_minnz][i] = -1*d

        coord = coord * A #update coordinates

        return euclid_extended(list, coord)

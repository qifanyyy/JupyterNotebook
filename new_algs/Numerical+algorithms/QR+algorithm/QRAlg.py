# Q2: A QR algorithm: unshifted

import numpy as np, scipy.linalg as la
import matplotlib.pyplot as plt
import ggplot as gplt
import copy

import HouseHolder
import TriDiag
import Utils


def qrAlg(a, exact=1):
    CUTOFF = 1e-12

    flag, msg = Utils.checks(a)
    if flag is False:
        raise ValueError(msg)

    diagonalized_a = copy.deepcopy(a)
    # Utils.makeExact(diagonalized_a)
    # if not np.array_equal(a, diagonalized_a):
    #     raise ValueError("The supplied matrix is not tridiagonal")

    eigenvalue_evolution = list()

    if np.shape(diagonalized_a) == (1, 1):
        eigenvalue_evolution.append(0.0)
        return diagonalized_a, eigenvalue_evolution

    while True:
        v, r = HouseHolder.house(diagonalized_a)
        q = HouseHolder.formQ(v)
        diagonalized_a = r * q
        if exact == 1:
            Utils.makeExact(diagonalized_a)
        eigenvalue_evolution.append(abs(np.asscalar(diagonalized_a[-1, -2])))
        if abs(eigenvalue_evolution[-1]) < CUTOFF:
            break

    return diagonalized_a, eigenvalue_evolution


def main():
    CUTOFF = 1e-12
    exact = 0
    a = np.asmatrix(la.hilbert(4))
    h = TriDiag.tridiag(a, exact=exact)

    m = np.shape(a)[0]

    sawtooth = list()
    eigenvalues = list()

    for k in range(m, 0, -1):
        h, eigenvalue_evolution = qrAlg(h[:k, :k], exact=exact)
        eigenvalues.append(np.asscalar(h[-1, -1]))
        sawtooth += eigenvalue_evolution

    ##plot
    # sawtooth = [i/CUTOFF for i in sawtooth if i != 0]
    # plt.plot(range(len(sawtooth[:-1])), sawtooth[:-1])
    # fig = plt.plot(sawtooth[:-1])
    plt.semilogy(range(len(sawtooth)), sawtooth)

    # gplt.aes(range(len(sawtooth[:-1])),  sawtooth[:-1], xlim)
    plt.show()


if __name__ == '__main__':
    main()

##
# Diagonalization: Step 1
#
# [[  1.50021428e+00  -1.78075254e-05   0.00000000e+00   0.00000000e+00]
#  [ -1.78075254e-05   1.69141220e-01   5.62874380e-09   0.00000000e+00]
#  [  0.00000000e+00   5.62874380e-09   6.73827361e-03   0.00000000e+00]
#  [  0.00000000e+00   0.00000000e+00   0.00000000e+00   9.67023040e-05]]
##

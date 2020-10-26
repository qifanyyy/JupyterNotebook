# -*- coding: UTF-8 -*-
"""
This module contains supporting functions for the SDSS stellar locus algorithm.

The functions related to the projection of ellipsoids are taken from
`Algorithms for Ellipsoids` by Stephen B. Pope (2008), Cornell University Report FDA-08-01.
"""

import numpy as np
from numpy.linalg import norm, inv, cholesky

from numba import jit

# basis of color-space:
x = np.array([1, 0, 0])
y = np.array([0, 1, 0])
z = np.array([0, 0, 1])


@jit
def find_nearest_locus_point(c, O):
    """Look up the nearest locus point with minimum Euclidean distance.

    Input
    -----
        c : array (3)
            Location in (x,y,z) color space in either ugri or griz spaces

        O : array (N, 3)
            Array of N locus points in (x,y,z) color space in either ugri or griz spaces
            From tabular input:
            ugri = np.loadtxt('ugri.tab')
            O = ugri[:, 3:6]

    Returns
    -------
        n_min : integer
            The index of the nearest locus point
    """
    # Square of euclidian distance:
    dist = np.sum((O - c)**2, 1)

    # Minimum of the distance squared gives the nearest locus point:
    n_min = np.argmin(dist)

    return n_min


@jit
def project_ellipsoid_to_plane(A, k):
    """
    Project an ellipsoid given by `A` onto a plane defined by its
    normal vector `k`.

    Input
    -----
    A : (3x3) matrix
        The inverse covariance matrix of the ellipsoid for the data point
        in (x,y,z) color space. Assumed to be uncorrelated, hence diagonal.

    k : (1x3) vector
        The normal vector of the plane onto which A is projected.

    Returns
    -------
    V : (2x2) matrix
        The inverse covariance matrix of the ellipse in the (i,j) plane.

    """
    p2 = np.cross(k, z)
    p2 = p2/norm(p2)
    p1 = np.cross(p2, k)
    p1 = p1/norm(p1)
    P = np.row_stack([p1, p2])

    v = np.array([[k[0]],
                  [k[1]],
                  [k[2]]])
    # Prepare auxilliary matrices:
    #  B = A - (A v v' A)/(v' A v)
    #  t = (v' A v)
    t = v.T.dot(A.dot(v))

    B = A - A.dot(v.dot(v.T.dot(A))) / t

    # Prepare the *Grammian* matrix of p1 and p2:
    G11 = p1.dot(p1)
    G21 = G12 = p1.dot(p2)
    G22 = p2.dot(p2)
    G = np.array([[G11, G12],
                  [G21, G22]])
    G = inv(G)

    V = np.zeros_like(G)
    for h in range(2):
        for n in range(2):
            c = 0.
            for i in range(2):
                for j in range(3):
                    for l in range(3):
                        for m in range(2):
                            c += G[h, i]*P[i, j]*B[j, l]*P[m, l]*G[m, n]
            V[h, n] = c

    return V


@jit
def project_ellipsoid_to_line(A, k):
    """
    Project an ellipsoid given by the matrix `A` on to a line given by the
    directional vector `k`.

    Input
    -----
    A : (3x3) matrix
        The inverse covariance matrix of the ellipsoid for the data point
        in (x,y,z) color space. Assumed to be uncorrelated, hence diagonal.

    k : (1x3) vector
        The unit vector defining the line direction.

    Returns
    -------
    w : float
        The covariance projected in the k-direction.

    """
    # Make Cholesky decomposition of A:
    L = cholesky(A)
    L_inv = inv(L)
    w = L_inv.dot(k) / (k.T.dot(k))

    return norm(w)


@jit
def project_point_to_plane(c, k, o):
    """
    Project a point in 3D `c` onto a plane given by its normal vector `k`
    and origin `o`.

    Input
    -----
    c : array (3)
        Point in (x,y,z) color space

    k : (1x3) vector
        The normal vector of the plane onto which c is projected.

    o : array (3)
        Origin of the plane; here the locus point center in (x,y,z) space

    Returns
    -------
    p : array (2)
        Coordinates of c projected into (i,j) plane

    Notes
    -----
        i and j are defined as:
        j = k x z / |k x z|
        i = j x k

    """
    j = np.cross(k, z)
    j = j/norm(j)
    i = np.cross(j, k)
    i = i/norm(i)
    P = np.row_stack([i, j])

    p_xyz = c - k.dot(c-o) * k

    p_ij = P.dot(p_xyz)

    return p_ij


@jit
def generate_covariance_matrix(a_l, a_m, theta):
    """
    The locus cross-section at each locus point is defined as an ellipse
    in the (i,j) plane with major axis, a_l, and minor axis, a_m. The (l,m) basis
    is defined as the principal axes of the ellipse such that l points in the direction
    of the major axis and m in the direction of the minor axis.
    The ellipse is rotated with respect to the (i,j) plane by angle, theta.
        cos(theta) = l . (k x z) x k / |k x z|
    or in terms of (i,j):
        cos(theta) = l . i

    Input
    -----
    a_l : float
        Length of major axis of elliptical cross-section of the locus

    a_m : float
        Length of minor axis of elliptical cross-section of the locus

    theta : float
        Rotation angle of major axis with respect to i-axis of the (i,j) plane.
        [radians]

    Returns
    -------
    A : (2x2) matrix
        The covariance matrix of the ellipse in the (i,j) plane.

    """
    # -- Use algebraic expansion:
    #    Average speed is 69.8 µs/call
    # a = (np.cos(theta)*a_l)**2 + (np.sin(theta)*a_m)**2
    # b = np.sin(2*theta)*(a_l**2/(2.) - a_m**2/(2.))
    # c = (np.sin(theta)*a_l)**2 + (np.cos(theta)*a_m)**2
    # A = np.array([[a, b], [b, c]])

    # -- Use matrix representation:
    #    Average speed is 60.6 µs/call
    R = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    C = np.array([[a_l**2, 0.], [0., a_m**2]])
    A = R.dot(C).dot(R.T)
    return A


@jit
def point_in_ellipse(p, A, c=None):
    """
    Test if the given point `p` is within the ellipse (or ellipsoid) given by
    the matrix `A` centred at the position `c`.

    Input
    -----
    p : array (N)
        Point to test in N dimensions.

    A : (NxN) matrix
        The inverse covariance matrix of the ellipse (or ellipsoid) in N
        dimensions.

    c : array (N), [default: None]
        Center of the ellipse (or ellipsoid) in N dimensions.
        By default the center will be set to 0.

    Returns
    -------
    bool :
        True if the point is within the ellipse, else False.
    """
    if c is not None:
        x = p - c
    else:
        x = p
    r = np.sqrt((x.T).dot(A).dot(x))
    return r <= 1.


@jit
def point_in_ellipse_old(p, A, c=0.):
    """
    Test if the given point `p` is within the ellipse (or ellipsoid) given by
    the matrix `A` centred at the position `c`.

    Input
    -----
    p : array (N)
        Point to test in N dimensions.

    A : (NxN) matrix
        The inverse covariance matrix of the ellipse (or ellipsoid) in N
        dimensions.

    c : array (N), [default: 0.]
        Center of the ellipse (or ellipsoid) in N dimensions.

    Returns
    -------
    bool :
        True if the point is within the ellipse, else False.
    """
    L = cholesky(A)

    s = norm(L.T.dot(p-c))
    if s <= 1:
        return True
    else:
        return False

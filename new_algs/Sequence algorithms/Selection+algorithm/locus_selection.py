# -*- coding: UTF-8 -*-
"""
This module contains functions to calculate whether a given photometric
data point falls within the SDSS stellar locus.
"""

__author__ = 'Jens-Kristian Krogager'

import numpy as np
from os import path

from numba import jit

import locus_tools as lt

root_path = path.dirname(path.abspath(__file__))


@jit
def get_color_vector(mag, err):
    """Return the 3-color vector from 4-point photometry"""
    colors = np.array([mag[i] - mag[i+1] for i in range(len(mag)-1)])
    errors = np.array([np.sqrt(err[i]**2 + err[i+1]**2) for i in range(len(mag)-1)])
    return colors, errors


# --- Load Stellar Loci:
# Table format:
# (0)  (1)  (2)  (3)   (4)   (5)    (6)    (7)    (8)    (9)   (10)   (11)
# i     k    N   u-g   g-r   r-i   k_ug   k_gr   k_ri     a     b    theta
ugri_locus_pars = np.loadtxt(root_path+'/ugri_table_Richards2002.dat')
griz_locus_pars = np.loadtxt(root_path+'/griz_table_Richards2002.dat')


def run_locus_selection(photometry, errors, midz=False, locus='ugri'):
    """
    Test whether input colors are inside the stellar locus defined
    in either ``ugri`` or ``griz`` color-spaces.

    Parameters
    ----------
    colors : array_like, shape (N, 4)
        An array of N color vectors consisting of 4 bands:
        For ``ugri``: u, g, r, i ; and for ``griz``: g, r, i, z.

    errors : array_like, shape (N, 4)
        An array of N vectors containing the error on the input `photometry`
        for each filter.

    midz : bool   [default = False]
        If True, the `ugri` locus width will be divided by a factor of 2.

    locus : str   [default = 'ugri']
        Which stellar locus to work on, must be either ``ugri`` or ``griz``.

    Returns
    -------
    in_locus : array(bool), shape (N)
        Boolean array of length N for each target in the input `colors`.
        The array will be `True` if the target is inside the stellar locus
        convolved by 4 times the `errors`.
    """

    phot = np.array(photometry)
    errors = np.array(errors)

    # Check input data format:
    assert phot.shape == errors.shape, "Input data and errors must have same dimensions."

    if len(phot.shape) == 2:
        if phot.shape[1] == 4:
            pass
        else:
            err_msg = "Input only allows four filters. Not %r given."
            raise ValueError(err_msg % phot.shape[1])
    else:
        err_msg = "Wrong input dimensions: %r"
        raise ValueError(err_msg % phot.shape)

    if locus.lower() == 'ugri':
        locus_pars = ugri_locus_pars.copy()
        # these are set manually for ugri and griz:
        a_k = 0.2
        k_end = -0.05
        if midz:
            locus_pars[:, 9] /= 2.
            locus_pars[:, 10] /= 2.
            a_k /= 2.
        N_err = 4.

    elif locus.lower() == 'griz':
        locus_pars = griz_locus_pars.copy()
        # these are set manually for ugri and griz:
        a_k = 0.5
        k_end = -0.3
        N_err = 4.
    locus_points = locus_pars[:, 3:6]

    in_locus = list()
    for mags, mag_errs in zip(phot, errors):
        c, e = get_color_vector(mags, mag_errs)
        loc_i = lt.find_nearest_locus_point(c, locus_points)

        # --- Set locus parameters:
        k = locus_pars[loc_i, 6:9]
        orig = locus_pars[loc_i, 3:6]
        a_l = locus_pars[loc_i, 9]
        a_m = locus_pars[loc_i, 10]
        theta = locus_pars[loc_i, 11]

        # Make sure that theta is in the range [-pi/2 : pi/2]
        if theta < -np.pi/2.:
            theta += np.pi
        elif theta > np.pi/2.:
            theta -= np.pi

        # Generate 3D covariance matrix:
        var = e**2
        cov = np.identity(3) * var
        cov[0, 1] = cov[1, 0] = -mag_errs[1]**2
        cov[1, 2] = cov[2, 1] = -mag_errs[2]**2
        cov *= N_err**2
        inv_cov = np.linalg.inv(cov)

        # Project data point to locus-plane:
        A_ij = lt.project_ellipsoid_to_plane(inv_cov, k)

        S = lt.generate_covariance_matrix(a_l, a_m, theta)

        # Convolved covariance as inverse A_ij and S_ij:
        C = np.linalg.inv(A_ij) + S

        # Get new eigen values and eigen vectors
        eigvals, eigvecs = np.linalg.eig(C)

        # Update a_l and a_m with the new convolved values a_l' and a_m':
        a_lV = np.sqrt(max(eigvals))
        a_mV = np.sqrt(min(eigvals))
        # l_prime = eigvecs[np.argmax(eigvals)]

        # Convert covariance to inverse covariance:
        C_ij = np.linalg.inv(C)

        # Calculate the new angle, theta to theta':
        thetaV = np.arctan2(-2. * C_ij[1, 0], (C_ij[1, 1] - C_ij[0, 0])) / 2.
        if thetaV < -np.pi/2:
            thetaV += np.pi
        elif thetaV > np.pi/2:
            thetaV -= np.pi
        else:
            pass
        # thetaV = np.arctan2(l_prime[1], l_prime[0])

        V_k = lt.project_ellipsoid_to_line(inv_cov, k)

        # project observed colors to locus-plane:
        p_ij = lt.project_point_to_plane(c, k, orig)

        # Check if point `p_ij` is inside ellipse `C_ij`:
        in_ellipse_ij = lt.point_in_ellipse(p_ij, C_ij)

        # -- Check if point is inside cylinder length:
        delta_k = (c - orig).dot(k)
        if loc_i == 0:
            # calculate length of cylinder:
            center_red = locus_pars[loc_i+1, 3:6]
            k_red = np.linalg.norm(orig - center_red)/2.
            k_red = np.sqrt(k_red**2 + V_k)
            k_blue = -np.sqrt(k_end**2 + V_k)
            if delta_k >= k_blue and delta_k <= k_red:
                in_cylinder = True
            else:
                in_cylinder = False

        elif loc_i == len(locus_points)-1:
            center_blue = locus_pars[loc_i-1, 3:6]
            k_blue = np.linalg.norm(orig - center_blue)/2.
            k_blue = -np.sqrt(k_blue**2 + V_k)
            if delta_k >= k_blue:
                in_cylinder = True
            else:
                in_cylinder = False

        else:
            center_red = locus_pars[loc_i+1, 3:6]
            k_red = np.linalg.norm(orig - center_red)/2.
            k_red = np.sqrt(k_red**2 + V_k)
            center_blue = locus_pars[loc_i-1, 3:6]
            k_blue = np.linalg.norm(orig - center_blue)/2.
            k_blue = -np.sqrt(k_blue**2 + V_k)
            if delta_k >= k_blue and delta_k <= k_red:
                in_cylinder = True
            else:
                in_cylinder = False

        # Data point must be both inside the ellipse of the cylinder cross-section
        # and inside the cylinder length:
        in_cylinder *= in_ellipse_ij

        # --- Check if point is in end ellipsoid:
        if loc_i == 0:
            # center of end ellipsoid:
            center_end = orig + k_end*k

            # define basis for ellipsoid:
            j = np.cross(k, lt.z)
            j = j/np.linalg.norm(j)
            i = np.cross(j, k)
            # The end ellipsoid is now defined in l' and m' space:
            l = np.cos(thetaV)*i + np.sin(thetaV)*j
            m = np.cos(thetaV + np.pi/2.)*i + np.sin(thetaV + np.pi/2.)*j

            # Basis matrix for ellipsoid:
            U = np.column_stack([l, m, k])

            # Extend a_k with projected variance:
            a_kV = np.sqrt(a_k**2 + V_k)

            # Matrix for ellipsoid:
            S_end = np.array([[1./a_lV, 0., 0.],
                              [0., 1./a_mV, 0.],
                              [0., 0., 1./a_kV]])

            # Inverse covariance matrix:
            C_xyz = U.dot((S_end**2).dot(U.T))
            in_ellipse_xyz = lt.point_in_ellipse(c, C_xyz, center_end)

            in_locus.append(bool(in_cylinder + in_ellipse_xyz))

        else:
            in_locus.append(in_cylinder)

    return np.array(in_locus, dtype=bool)

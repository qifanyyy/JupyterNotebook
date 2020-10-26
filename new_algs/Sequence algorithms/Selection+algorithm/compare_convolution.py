# -*- coding: UTF-8 -*-
"""
Test the convolution of the Stellar Locus from Richards et al. 2002
"""

import numpy as np
import matplotlib.pyplot as plt

from scspy import locus_tools as lt


def angle_of_matrix(A):
    """Return the rotation of the 2x2 matrix A"""
    theta = np.arctan2(-2. * A[1, 0], (A[1, 1] - A[0, 0])) / 2.
    return theta


def get_color_vector(mag, err):
    """Return the 3-color vector from 4-point photometry"""
    colors = np.array([mag[i] - mag[i+1] for i in range(len(mag)-1)])
    errors = np.array([np.sqrt(err[i]**2 + err[i+1]**2) for i in range(len(mag)-1)])
    return colors, errors


locus = 'griz'

# -- Load locus parameters:
# i     k       N      u-g     g-r     r-i    k_ug    k_gr    k_ri      a       b      theta
griz = np.loadtxt('../%s_table_Richards2002.dat' % locus)
dk = griz[:, 1]
x, y, z = griz[:, 3], griz[:, 4], griz[:, 5]
k1 = griz[:, 6]
k2 = griz[:, 7]
k3 = griz[:, 8]
a = griz[:, 9]
b = griz[:, 10]
PA = griz[:, 11]
locus_points = griz[:, 3:6]


test_case = 0

if test_case == 0:
    mag = np.array([21.15747, 19.38568, 19.11355, 18.74245, 18.5094])
    mag_err = np.array([0.16706478, 0.07048335, 0.05282675, 0.04139954, 0.04327397])
else:
    mag = np.array([19.34575, 19.282, 19.12902, 19.0099, 19.11363])
    mag_err = np.array([0.0988765, 0.06912346, 0.05205835, 0.04185864, 0.05580382])

if locus == 'ugri':
    mag = mag[:4]
    mag_err = mag_err[:4]
    col, err = get_color_vector(mag, mag_err)
else:
    mag = mag[1:]
    mag_err = mag_err[1:]
    col, err = get_color_vector(mag, mag_err)

# -- find nearest locus-point:
dist = np.sum((locus_points - col)**2, 1)
j = np.argmin(dist)

# -- locus point data:
# center:
# p0 = np.array([[x[j], y[j], z[j]]])
p0 = griz[j, 3:6]
# normal:
k = griz[j, 6:9]
# major, minor axes and rotation:
a_l = griz[j, 9]
a_m = griz[j, 10]
theta = griz[j, 11]
if theta < -np.pi/2.:
    theta += np.pi
elif theta > np.pi/2.:
    theta -= np.pi

# Generate 3D error ellipsoid:
N_err = 4.
var = err**2
cov = np.identity(3) * var
cov[0, 1] = cov[1, 0] = -mag_err[1]**2
cov[1, 2] = cov[2, 1] = -mag_err[2]**2
cov *= N_err**2
inv_cov = np.linalg.inv(cov)
# inv_cov = np.identity(3) / (var * N_err**2)

# Project data point to locus-plane:
A_ij = lt.project_ellipsoid_to_plane(inv_cov, k)

S = lt.generate_covariance_matrix(a_l, a_m, theta)

# convolve A_ij and S_ij:
C_ij = np.linalg.inv(A_ij) + S

# get new eigen values and eigen vectors
eigvals, eigvecs = np.linalg.eig(C_ij)

# update a_l and a_m with the new convolved values a_l' and a_m':
a_lV = np.sqrt(max(eigvals))
a_mV = np.sqrt(min(eigvals))

C_ij = np.linalg.inv(C_ij)
thetaV = angle_of_matrix(C_ij)

print " Matrix Implementation:"
print ""
print " - Original ellipse :"
print "   a_l = %.3f  a_m = %.3f  PA = %.1f" % (a_l, a_m, theta*180./np.pi)
print "\n - Convolved :"
print "   a_l = %.3f  a_m = %.3f  PA = %.1f" % (a_lV, a_mV, thetaV*180./np.pi)


# -- Follow Richards et al. 2002:
((Vll, Vlm), (Vlm, Vmm)) = np.linalg.inv(A_ij)
a_maj = np.sqrt((Vll + Vmm + np.sqrt((Vll-Vmm)**2 + 4*Vlm**2))/2.)
a_min = np.sqrt((Vll + Vmm - np.sqrt((Vll-Vmm)**2 + 4*Vlm**2))/2.)
theta_err = np.arctan((-(Vll - Vmm) + np.sqrt((Vll-Vmm)**2 + 4*Vlm**2))/(2.*Vlm))
theta_err = theta - theta_err

d = a_maj**2*a_min**2 + (a_l**2 * a_maj**2 + a_m**2 * a_min**2)*np.sin(theta_err)**2
d += (a_maj**2 * a_m**2 + a_l**2 * a_min**2)*np.cos(theta_err)**2 + a_l**2 * a_m**2

alpha = (a_min * np.cos(theta_err))**2 + (a_maj * np.sin(theta_err))**2 + a_m**2
beta = np.sin(theta_err)*np.cos(theta_err)*(a_maj**2 - a_min**2)
gamma = (np.sin(theta_err) * a_min)**2 + (a_maj * np.cos(theta_err))**2 + a_l**2

a = (alpha + gamma)/2.
b = np.sqrt((alpha+gamma)**2 - 4.*(alpha*gamma - beta**2))/2.

if theta_err < 0:
    theta_tot = np.arctan((alpha-gamma + np.sqrt((alpha-gamma)**2 + 4*beta**2))/(2*beta))
else:
    theta_tot = np.arctan(-(alpha-gamma + np.sqrt((alpha-gamma)**2 + 4*beta**2))/(2*beta))

print "\n - Following Richards et al."
print "   Convolved :"
print "   a_l = %.3f  a_m = %.3f  PA = %.1f" % (np.sqrt(a+b), np.sqrt(a-b), (theta+theta_tot)*180./np.pi)

# plt.close('all')
fig = plt.figure()
ax = fig.add_subplot(111)

base = plt.matplotlib.patches.Ellipse((0., 0.), 2*a_l, 2*a_m, theta*180./np.pi,
                                      ec='k', fc='none')

# -- get error ellipse:
vals, vecs = np.linalg.eig(np.linalg.inv(A_ij))
PA = angle_of_matrix(A_ij)
err_E = plt.matplotlib.patches.Ellipse((0., 0.), 2*np.sqrt(np.max(vals)), 2*np.sqrt(np.min(vals)), PA*180./np.pi,
                                       ec='r', fc='none')

E_conv = plt.matplotlib.patches.Ellipse((0., 0.), 2*a_lV, 2*a_mV, thetaV*180./np.pi,
                                        ec='b', fc='none')

p_ij = lt.project_point_to_plane(col, k, p0)

in_ellipse_ij = lt.point_in_ellipse(p_ij, C_ij)
print "Point in ellipse: ", in_ellipse_ij


ax.add_patch(base)
ax.add_patch(err_E)
ax.add_patch(E_conv)
plt.plot(p_ij[0], p_ij[1], 'k.')
plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.show()

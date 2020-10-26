# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

r"""Perform plots of relative error against the condition number.

This uses :math:`p(s) = (s - 1) \left(s - \frac{3}{4}\right)^7` which
has :math:`\widetilde{p}(s) = (s - 1) \left(\frac{s}{2} -
\frac{3}{4}\right)^7`.
"""

import fractions

import matplotlib.pyplot as plt
import numpy as np

import de_casteljau
import plot_utils


F = fractions.Fraction
U = F(1, 2 ** 53)
# p(s) = (s - 1) (s - 3/4)^7
BEZIER_COEFFS = (
    2187.0 / 16384.0,
    -5103.0 / 131072.0,
    729.0 / 65536.0,
    -405.0 / 131072.0,
    27.0 / 32768.0,
    -27.0 / 131072.0,
    3.0 / 65536.0,
    -1.0 / 131072.0,
    0.0,
)
ROOT = 0.75
POWER_VAL = 1.3
ALPHA = 0.25


def main(filename=None):
    n = 8
    gamma2n = (2 * n * U) / (1 - 2 * n * U)
    bound_coeff1 = float(gamma2n)
    bound_coeff2 = 3 * n * (3 * n + 7) * U ** 2 / 2
    bound_coeff2 = float(bound_coeff2)
    bound_coeff3 = 3 * n * (3 * n ** 2 + 36 * n + 61) * U ** 3 / 2
    bound_coeff3 = float(bound_coeff3)
    bound_coeff4 = (
        9 * n * (3 * n ** 3 + 102 * n ** 2 + 773 * n + 1122) * U ** 4 / 8
    )
    bound_coeff4 = float(bound_coeff4)

    cond_nums = []
    forward_errs1 = []
    forward_errs2 = []
    forward_errs3 = []
    forward_errs4 = []
    for j in range(-5, -90 - 1, -1):
        s = ROOT - POWER_VAL ** j
        exact_s = F(s)

        # Compute the condition number.
        exact_p = (exact_s - 1) * (4 * exact_s - 3) ** 7 / 16384
        # p_tilde(s) = SUM_j |b_j| B_{j, 8}(s) = (s - 1) (s/2 - 3/4)^7
        exact_p_tilde = (exact_s - 1) * (2 * exact_s - 3) ** 7 / 16384
        exact_cond = abs(exact_p_tilde / exact_p)
        cond_nums.append(float(exact_cond))

        # Compute the forward error for uncompensated de Casteljau.
        b, db, d2b, d3b = de_casteljau._compensated_k(s, BEZIER_COEFFS, 4)
        exact_b1 = F(b)
        exact_forward_err1 = abs((exact_b1 - exact_p) / exact_p)
        forward_errs1.append(float(exact_forward_err1))

        # Compute the forward error for compensated de Casteljau.
        b2 = b + db
        exact_b2 = F(b2)
        exact_forward_err2 = abs((exact_b2 - exact_p) / exact_p)
        forward_errs2.append(float(exact_forward_err2))

        # Compute the forward error for K-compensated de Casteljau (K=3).
        b3 = b2 + d2b
        exact_b3 = F(b3)
        exact_forward_err3 = abs((exact_b3 - exact_p) / exact_p)
        forward_errs3.append(float(exact_forward_err3))

        # Compute the forward error for K-compensated de Casteljau (K=3).
        b4 = b3 + d3b
        exact_b4 = F(b4)
        exact_forward_err4 = abs((exact_b4 - exact_p) / exact_p)
        forward_errs4.append(float(exact_forward_err4))

    # Set a tight ``x``-limit.
    min_exp = np.log(min(cond_nums))
    max_exp = np.log(max(cond_nums))
    delta_exp = max_exp - min_exp
    min_x = np.exp(min_exp - 0.01 * delta_exp)
    max_x = np.exp(max_exp + 0.01 * delta_exp)

    figure = plt.figure()
    ax = figure.gca()
    ax.loglog(
        cond_nums,
        forward_errs1,
        marker="v",
        linestyle="none",
        zorder=2,
        label=r"$\mathtt{DeCasteljau}$",
    )
    ax.loglog(
        cond_nums,
        forward_errs2,
        marker="d",
        linestyle="none",
        zorder=2,
        label=r"$\mathtt{CompDeCasteljau}$",
    )
    ax.loglog(
        cond_nums,
        forward_errs3,
        marker="P",
        linestyle="none",
        zorder=1.5,  # Beneath ``K=2``.
        label=r"$\mathtt{CompDeCasteljau3}$",
    )
    ax.loglog(
        cond_nums,
        forward_errs4,
        marker="o",
        linestyle="none",
        zorder=1.25,  # Beneath ``K=2, 3``.
        label=r"$\mathtt{CompDeCasteljau4}$",
    )
    # Figure out the bounds before adding the bounding lines.
    min_y, max_y = ax.get_ylim()
    # Plot the lines of the a priori error bounds.
    ax.loglog(
        [min_x, max_x],
        [bound_coeff1 * min_x, bound_coeff1 * max_x],
        color="black",
        alpha=ALPHA,
        zorder=1,
    )
    ax.loglog(
        [min_x, max_x],
        [bound_coeff2 * min_x, bound_coeff2 * max_x],
        color="black",
        alpha=ALPHA,
        zorder=1,
    )
    ax.loglog(
        [min_x, max_x],
        [bound_coeff3 * min_x, bound_coeff3 * max_x],
        color="black",
        alpha=ALPHA,
        zorder=1,
    )
    ax.loglog(
        [min_x, max_x],
        [bound_coeff4 * min_x, bound_coeff4 * max_x],
        color="black",
        alpha=ALPHA,
        zorder=1,
    )
    # Add the ``x = 1/u^k`` vertical lines.
    delta_y = max_y - min_y
    for exponent in (1, 2, 3, 4):
        u_inv = 1.0 / float(U) ** exponent
        ax.loglog(
            [u_inv, u_inv],
            [min_y - 0.05 * delta_y, max_y + 0.05 * delta_y],
            color="black",
            linestyle="dashed",
            alpha=ALPHA,
            zorder=1,
        )
    # Add the ``y = u`` horizontal lines.
    ax.loglog(
        [min_x, max_x],
        [float(U), float(U)],
        color="black",
        linestyle="dashed",
        alpha=ALPHA,
        zorder=1,
    )

    # Make sure the ``y``-limit stays set (the bounds lines exceed).
    ax.set_ylim(min_y, 1.0)
    ax.set_xlim(min_x, max_x)
    # Add the legend.
    ax.legend(loc="lower right", framealpha=1.0, frameon=True)
    # Set "nice" ticks.
    ax.set_xticks([10.0 ** n for n in range(5, 65 + 10, 10)])
    ax.set_yticks([10.0 ** n for n in range(-18, 0 + 2, 2)])
    # Set special ``xticks`` for ``1/u^k``.
    u_xticks = []
    u_xticklabels = []
    for exponent in (1, 2, 3, 4):
        u_xticks.append(1.0 / float(U) ** exponent)
        if exponent == 1:
            u_xticklabels.append(r"$1/\mathbf{u}$")
        else:
            u_xticklabels.append(r"$1/\mathbf{{u}}^{}$".format(exponent))

    ax.set_xticks(u_xticks, minor=True)
    ax.set_xticklabels(u_xticklabels, minor=True)
    ax.tick_params(
        axis="x",
        which="minor",
        direction="out",
        top=1,
        bottom=0,
        labelbottom=0,
        labeltop=1,
    )
    # Set special ``yticks`` for ``u``.
    ax.set_yticks([float(U)], minor=True)
    ax.set_yticklabels([r"$\mathbf{u}$"], minor=True)
    ax.tick_params(
        axis="y",
        which="minor",
        direction="out",
        left=0,
        right=1,
        labelleft=0,
        labelright=1,
    )
    # Label the axes.
    ax.set_xlabel("Condition Number")
    ax.set_ylabel("Relative Forward Error")

    if filename is None:
        plt.show()
    else:
        path = plot_utils.get_path(filename)
        figure.savefig(path, bbox_inches="tight")
        print("Saved {}".format(filename))
        plt.close(figure)


def main_jlcs10(filename=None):
    """This recreates the plot from `JLCS10`_.

    .. _JLCS10: https://doi.org/10.1016/j.camwa.2010.05.021

    Note that it is essentially a copy of :func:`main` (and much of the
    code could be shared, but it isn't worth the effort).

    This seeks to recreate the plot from the original paper, but to show
    what happens as the exponent on ``POWER_VAL`` decreases from ``-44`` down
    to ``-64``. In particular, it shows that the compensated de Casteljau
    algorithm produces exactly zero.
    """
    n = 8
    gamma2n = (2 * n * U) / (1 - 2 * n * U)
    bound_coeff1 = float(gamma2n)
    bound_coeff2 = 3 * n * (3 * n + 7) * U ** 2 / 2
    bound_coeff2 = float(bound_coeff2)

    cond_nums = []
    forward_errs1 = []
    forward_errs2 = []
    for j in range(-5, -64 - 1, -1):
        s = ROOT - POWER_VAL ** j
        exact_s = F(s)

        # Compute the condition number.
        exact_p = (exact_s - 1) * (4 * exact_s - 3) ** 7 / 16384
        # p_tilde(s) = SUM_j |b_j| B_{j, 8}(s) = (s - 1) (s/2 - 3/4)^7
        exact_p_tilde = (exact_s - 1) * (2 * exact_s - 3) ** 7 / 16384
        exact_cond = abs(exact_p_tilde / exact_p)
        cond_nums.append(float(exact_cond))

        # Compute the forward error for uncompensated de Casteljau.
        b, db = de_casteljau._compensated_k(s, BEZIER_COEFFS, 2)
        exact_b1 = F(b)
        exact_forward_err1 = abs((exact_b1 - exact_p) / exact_p)
        forward_errs1.append(float(exact_forward_err1))

        # Compute the forward error for compensated de Casteljau.
        b2 = b + db
        exact_b2 = F(b2)
        exact_forward_err2 = abs((exact_b2 - exact_p) / exact_p)
        forward_errs2.append(float(exact_forward_err2))

    # Set a tight ``x``-limit.
    min_exp = np.log(min(cond_nums))
    max_exp = np.log(max(cond_nums))
    delta_exp = max_exp - min_exp
    min_x = np.exp(min_exp - 0.01 * delta_exp)
    max_x = np.exp(max_exp + 0.01 * delta_exp)

    figure = plt.figure()
    ax = figure.gca()
    ax.loglog(
        cond_nums,
        forward_errs1,
        marker="v",
        linestyle="none",
        zorder=2,
        label=r"$\mathtt{DeCasteljau}$",
    )
    ax.loglog(
        cond_nums,
        forward_errs2,
        marker="d",
        linestyle="none",
        zorder=2,
        label=r"$\mathtt{CompDeCasteljau}$",
    )
    # Figure out the bounds before adding the bounding lines.
    min_y, max_y = ax.get_ylim()
    # Plot the lines of the a priori error bounds.
    ax.loglog(
        [min_x, max_x],
        [bound_coeff1 * min_x, bound_coeff1 * max_x],
        color="black",
        alpha=ALPHA,
        zorder=1,
    )
    ax.loglog(
        [min_x, max_x],
        [bound_coeff2 * min_x, bound_coeff2 * max_x],
        color="black",
        alpha=ALPHA,
        zorder=1,
    )
    # Add the ``x = 1/u^k`` vertical lines.
    delta_y = max_y - min_y
    for exponent in (1, 2):
        u_inv = 1.0 / float(U) ** exponent
        ax.loglog(
            [u_inv, u_inv],
            [min_y - 0.05 * delta_y, max_y + 0.05 * delta_y],
            color="black",
            linestyle="dashed",
            alpha=ALPHA,
            zorder=1,
        )
    # Add the ``y = u`` and ``y = 1`` horizontal lines.
    ax.loglog(
        [min_x, max_x],
        [float(U), float(U)],
        color="black",
        linestyle="dashed",
        alpha=ALPHA,
        zorder=1,
    )
    ax.loglog(
        [min_x, max_x],
        [1.0, 1.0],
        color="black",
        linestyle="dashed",
        alpha=ALPHA,
        zorder=1,
    )

    # Make sure the ``y``-limit stays set (the bounds lines exceed).
    ax.set_ylim(min_y, 10.0)
    ax.set_xlim(min_x, max_x)
    # Add the legend.
    ax.legend(loc="lower right", framealpha=1.0, frameon=True)
    # Set "nice" ticks.
    ax.set_xticks([10.0 ** n for n in range(5, 45 + 5, 5)])
    ax.set_yticks([10.0 ** n for n in range(-20, 0 + 4, 4)])
    # Set special ``xticks`` for ``1/u`` and ``1/u^2``.
    ax.set_xticks([1.0 / float(U), 1.0 / float(U) ** 2], minor=True)
    ax.set_xticklabels([r"$1/\mathbf{u}$", r"$1/\mathbf{u}^2$"], minor=True)
    ax.tick_params(
        axis="x",
        which="minor",
        direction="out",
        top=1,
        bottom=0,
        labelbottom=0,
        labeltop=1,
    )
    # Set special ``yticks`` for ``u`` and ``1``.
    ax.set_yticks([float(U), 1.0], minor=True)
    ax.set_yticklabels([r"$\mathbf{u}$", "$1$"], minor=True)
    ax.tick_params(
        axis="y",
        which="minor",
        direction="out",
        left=0,
        right=1,
        labelleft=0,
        labelright=1,
    )
    # Label the axes.
    ax.set_xlabel("Condition Number")
    ax.set_ylabel("Relative Forward Error")

    if filename is None:
        plt.show()
    else:
        path = plot_utils.get_path(filename)
        figure.savefig(path, bbox_inches="tight")
        print("Saved {}".format(filename))
        plt.close(figure)


if __name__ == "__main__":
    plot_utils.set_styles()
    main(filename="de_casteljau_rel_error.pdf")
    main_jlcs10(filename="jlcs10_plot.pdf")

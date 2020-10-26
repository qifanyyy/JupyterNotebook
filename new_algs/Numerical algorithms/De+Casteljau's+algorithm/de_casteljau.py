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

r"""Performs de Casteljau's method.

de Casteljau's method evaluates a function in Bernstein-Bezier form

.. math::

    p(s) = p_0 (1 - s)^n + \cdots + p_j \binom{n}{j} (1 - s)^{n - j} s^j +
        \cdots + p_n s^n

by progressively reducing the control points

.. math::

    \begin{align*}
    p_j^{(0)} &= p_j \\
    p_j^{(k + 1)} &= (1 - s) p_j^{(k)} + p_{j + 1}^{(k)} \\
    p(s) &= p_0^{(n)}.
    \end{align*}

This module provides both the standard version and a compensated version.

.. note::

   This assumes throughout that ``coeffs`` is ordered from
   :math:`p_n` to :math:`p_0`.
"""


import eft


def basic(s, coeffs):
    """Performs the "standard" de Casteljau algorithm."""
    r = 1.0 - s

    degree = len(coeffs) - 1
    pk = list(coeffs)
    for k in range(degree):
        new_pk = []
        for j in range(degree - k):
            new_pk.append(r * pk[j] + s * pk[j + 1])
        # Update the "current" values.
        pk = new_pk

    return pk[0]


def local_error(errors, rho, delta_b):
    r"""Compute :math:`\ell` from a list of errors.

    This assumes, but does not check, that there are at least two
    ``errors``.
    """
    num_errs = len(errors)

    l_hat = errors[0] + errors[1]
    for j in range(2, num_errs):
        l_hat += errors[j]

    l_hat += rho * delta_b

    return l_hat


def local_error_eft(errors, rho, delta_b):
    r"""Perform an error-free transformation for computing :math:`\ell`.

    This assumes, but does not check, that there are at least two
    ``errors``.
    """
    num_errs = len(errors)
    new_errors = [None] * (num_errs + 1)

    l_hat, new_errors[0] = eft.add_eft(errors[0], errors[1])
    for j in range(2, num_errs):
        l_hat, new_errors[j - 1] = eft.add_eft(l_hat, errors[j])

    prod, new_errors[num_errs - 1] = eft.multiply_eft(rho, delta_b)
    l_hat, new_errors[num_errs] = eft.add_eft(l_hat, prod)

    return new_errors, l_hat


def _compensated_k(s, coeffs, K):
    r"""Performs a K-compensated de Casteljau.

    .. _JLCS10: https://doi.org/10.1016/j.camwa.2010.05.021

    Note that the order of operations exactly matches the `JLCS10`_ paper.
    For example, :math:`\widehat{\partial b}_j^{(k)}` is computed as

    .. math::

        \widehat{ell}_{1, j}^{(k)} \oplus \left(s \otimes
            \widehat{\partial b}_{j + 1}^{(k + 1)}\right) \oplus
            \left(\widehat{r} \otimes \widehat{\partial b}_j^{(k + 1)}\right)

    instead of "typical" order

    .. math::

        \left(\widehat{r} \otimes \widehat{\partial b}_j^{(k + 1)}\right)
            \oplus \left(s \otimes \widehat{\partial b}_{j + 1}^{(k + 1)}
            \right) \oplus \widehat{ell}_{1, j}^{(k)}.

    This is so that the term

    .. math::

        \widehat{r} \otimes \widehat{\partial b}_j^{(k + 1)}

    only has to be in one sum. We avoid an extra sum because
    :math:`\widehat{r}` already has round-off error.
    """
    r, rho = eft.add_eft(1.0, -s)

    degree = len(coeffs) - 1
    bk = {0: list(coeffs)}
    # NOTE: This will be shared, but is read only.
    all_zero = (0.0,) * (degree + 1)
    for F in range(1, K - 1 + 1):
        bk[F] = all_zero

    for k in range(degree):
        new_bk = {F: [] for F in range(K - 1 + 1)}

        for j in range(degree - k):
            # Update the "level 0" stuff.
            P1, pi1 = eft.multiply_eft(r, bk[0][j])
            P2, pi2 = eft.multiply_eft(s, bk[0][j + 1])
            S3, sigma3 = eft.add_eft(P1, P2)
            new_bk[0].append(S3)

            errors = [pi1, pi2, sigma3]
            delta_b = bk[0][j]

            for F in range(1, K - 2 + 1):
                new_errors, l_hat = local_error_eft(errors, rho, delta_b)
                P1, pi1 = eft.multiply_eft(s, bk[F][j + 1])
                S2, sigma2 = eft.add_eft(l_hat, P1)
                P3, pi3 = eft.multiply_eft(r, bk[F][j])
                S, sigma4 = eft.add_eft(S2, P3)
                new_bk[F].append(S)

                new_errors.extend([pi1, sigma2, pi3, sigma4])
                errors = new_errors
                delta_b = bk[F][j]

            # Update the "level 2" stuff.
            l_hat = local_error(errors, rho, delta_b)
            new_bk[K - 1].append(
                l_hat + s * bk[K - 1][j + 1] + r * bk[K - 1][j]
            )

        # Update the "current" values.
        bk = new_bk

    return tuple(bk[F][0] for F in range(K - 1 + 1))


def compensated(s, coeffs):
    b, db = _compensated_k(s, coeffs, 2)
    return eft.sum_k((b, db), 2)


def compensated3(s, coeffs):
    b, db, d2b = _compensated_k(s, coeffs, 3)
    return eft.sum_k((b, db, d2b), 3)


def compensated4(s, coeffs):
    b, db, d2b, d3b = _compensated_k(s, coeffs, 4)
    return eft.sum_k((b, db, d2b, d3b), 4)


def compensated5(s, coeffs):
    b, db, d2b, d3b, d4b = _compensated_k(s, coeffs, 5)
    return eft.sum_k((b, db, d2b, d3b, d4b), 5)

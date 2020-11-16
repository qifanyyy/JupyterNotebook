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

"""Run many experiments to confirm the flop counts for algorithms."""

from __future__ import print_function

import de_casteljau
import eft
import horner
import operation_count
import vs_method


SEPARATOR = "-" * 80


def count_add_eft():
    parent = operation_count.Computation()
    val1 = operation_count.Float(1.5, parent)
    val2 = operation_count.Float(0.5 + 0.5 ** 52, parent)
    sum_, error = eft.add_eft(val1, val2)
    assert sum_.value == 2.0
    assert error.value == 0.5 ** 52
    assert parent.count == 6
    print("     add_eft(): {}".format(parent.display))


def count__split():
    parent = operation_count.Computation()
    val = operation_count.Float(1.0 + 0.5 ** 27, parent)
    high, low = eft._split(val)
    assert high.value == 1.0
    assert low.value == 0.5 ** 27
    assert parent.count == 4
    print("      _split(): {}".format(parent.display))


def count_multiply_eft():
    print("multiply_eft():")
    for use_fma in (True, False):
        parent = operation_count.Computation()
        val1 = operation_count.Float(1.0 + 0.5 ** 40, parent)
        val2 = operation_count.Float(1.0 - 0.5 ** 40, parent)
        product, error = eft.multiply_eft(val1, val2, use_fma=use_fma)
        assert product.value == 1.0
        assert error.value == -0.5 ** 80
        if use_fma:
            description = "with FMA:    "
            assert parent.count == 2
        else:
            description = "w / out FMA: "
            assert parent.count == 17
        print("  {} {}".format(description, parent.display))


def count__vec_sum():
    print("_vec_sum() (6(|p| - 1)):")
    for size_p in range(1, 5 + 1):
        parent = operation_count.Computation()
        p = [operation_count.Float(1.0, parent)] * size_p
        eft._vec_sum(p)

        assert p[size_p - 1].value == float(size_p)
        assert parent.count == 6 * (size_p - 1)
        print("  |p| = {}:      {}".format(size_p, parent.display))


def count_sum_k():
    print("sum_k() ((6K - 5)(|p| - 1)):")
    for k in (2, 3, 4, 5):
        print("  K = {}".format(k))
        for size_p in range(1, 5 + 1):
            parent = operation_count.Computation()
            p = [operation_count.Float(1.0, parent)] * size_p
            total = eft.sum_k(p, k)

            assert total.value == float(size_p)
            assert parent.count == (6 * k - 5) * (size_p - 1)
            print("    |p| = {}:    {}".format(size_p, parent.display))


def count_vs_method_basic():
    print("vs_method.basic() (5n + 1, w/o binomial):")
    for degree in range(1, 5 + 1):
        parent = operation_count.Computation()
        x = operation_count.Float(0.25, parent)
        coeffs = tuple(
            operation_count.Float((-1.0) ** k, parent)
            for k in range(degree + 1)
        )
        p = vs_method.basic(x, coeffs)
        assert p.value == 0.5 ** degree
        assert parent.count == 5 * degree + 1
        print("  degree {}:     {}".format(degree, parent.display))


def count_vs_method_compensated():
    print("vs_method.compensated() (26n + 7, w/o binomial):")
    for degree in range(1, 5 + 1):
        parent = operation_count.Computation()
        x = operation_count.Float(0.25, parent)
        coeffs = tuple(
            operation_count.Float((-1.0) ** k, parent)
            for k in range(degree + 1)
        )
        p = vs_method.compensated(x, coeffs)
        assert p.value == 0.5 ** degree
        assert parent.count == 26 * degree + 7
        print("  degree {}:     {}".format(degree, parent.display))


def count_horner_basic():
    print("horner.basic() (2n):")
    for degree in range(1, 5 + 1):
        parent = operation_count.Computation()
        x = operation_count.Float(2.0, parent)
        coeffs = (operation_count.Float(1.0, parent),) * (degree + 1)
        p = horner.basic(x, coeffs)
        assert p.value == 2.0 ** (degree + 1) - 1
        assert parent.count == 2 * degree
        print("  degree {}:     {}".format(degree, parent.display))


def horner_expected_total(K, n):
    r"""Get the expected flop count for compensated Horner's method.

    When using FMA, the count is

    .. math::

       (5 \cdot 2^K - 8)n + \left((K + 8) 2^K - 12K - 6\right).
    """
    return (5 * 2 ** K - 8) * n + ((K + 8) * 2 ** K - 12 * K - 6)


def horner_expected_fma(K, n):
    r"""Get the FMA count for compensated Horner's method.

    When using FMA, the count is

    .. math::

       \left(2^{K - 1} - 1\right)n - 2^{K - 1}(K - 3) - 2

    FMA (fused-multiply-add) instructions.
    """
    return (2 ** (K - 1) - 1) * n - 2 ** (K - 1) * (K - 3) - 2


def count_horner_compensated():
    print("horner.compensated() (11n + 1):")
    for degree in range(1, 5 + 1):
        parent = operation_count.Computation()
        x = operation_count.Float(2.0, parent)
        coeffs = (operation_count.Float(1.0, parent),) * (degree + 1)
        p = horner.compensated(x, coeffs)
        assert p.value == 2.0 ** (degree + 1) - 1
        assert parent.count == 11 * degree + 1
        print("  degree {}:     {}".format(degree, parent.display))

    # NOTE: This is **the same** as ``horner.compensated()`` but uses
    #       a different algorithm.
    print("horner.compensated_k(..., 2) (12n + 10):")
    for degree in range(1, 5 + 1):
        parent = operation_count.Computation()
        x = operation_count.Float(2.0, parent)
        coeffs = (operation_count.Float(1.0, parent),) * (degree + 1)
        p = horner.compensated_k(x, coeffs, 2)
        assert p.value == 2.0 ** (degree + 1) - 1
        assert parent.count == horner_expected_total(2, degree)
        assert parent.fma_count == horner_expected_fma(2, degree)
        print("  degree {}:     {}".format(degree, parent.display))


def count_horner_compensated3():
    print("horner.compensated3() (32n + 46, n >= 2):")
    for degree in range(2, 6 + 1):
        parent = operation_count.Computation()
        x = operation_count.Float(2.0, parent)
        coeffs = (operation_count.Float(1.0, parent),) * (degree + 1)
        p = horner.compensated3(x, coeffs)
        assert p.value == 2.0 ** (degree + 1) - 1
        assert parent.count == horner_expected_total(3, degree)
        assert parent.fma_count == horner_expected_fma(3, degree)
        print("  degree {}:     {}".format(degree, parent.display))

    print("horner.compensated_k(..., 3) (32n + 46, n >= 2):")
    for degree in range(2, 6 + 1):
        parent = operation_count.Computation()
        x = operation_count.Float(2.0, parent)
        coeffs = (operation_count.Float(1.0, parent),) * (degree + 1)
        p = horner.compensated_k(x, coeffs, 3)
        assert p.value == 2.0 ** (degree + 1) - 1
        assert parent.count == horner_expected_total(3, degree)
        assert parent.fma_count == horner_expected_fma(3, degree)
        print("  degree {}:     {}".format(degree, parent.display))


def count_horner_compensated4():
    print("horner.compensated_k(..., 4) (72n + 138, n >= 3):")
    for degree in range(3, 7 + 1):
        parent = operation_count.Computation()
        x = operation_count.Float(2.0, parent)
        coeffs = (operation_count.Float(1.0, parent),) * (degree + 1)
        p = horner.compensated_k(x, coeffs, 4)
        assert p.value == 2.0 ** (degree + 1) - 1
        assert parent.count == horner_expected_total(4, degree)
        assert parent.fma_count == horner_expected_fma(4, degree)
        print("  degree {}:     {}".format(degree, parent.display))


def count_horner_compensated5():
    print("horner.compensated_k(..., 5) (152n + 350, n >= 4):")
    for degree in range(4, 8 + 1):
        parent = operation_count.Computation()
        x = operation_count.Float(2.0, parent)
        coeffs = (operation_count.Float(1.0, parent),) * (degree + 1)
        p = horner.compensated_k(x, coeffs, 5)
        assert p.value == 2.0 ** (degree + 1) - 1
        assert parent.count == horner_expected_total(5, degree)
        assert parent.fma_count == horner_expected_fma(5, degree)
        print("  degree {}:     {}".format(degree, parent.display))


def count_horner_compensated6():
    print("horner.compensated_k(..., 6) (312n + 818, n >= 5):")
    for degree in range(5, 9 + 1):
        parent = operation_count.Computation()
        x = operation_count.Float(2.0, parent)
        coeffs = (operation_count.Float(1.0, parent),) * (degree + 1)
        p = horner.compensated_k(x, coeffs, 6)
        assert p.value == 2.0 ** (degree + 1) - 1
        assert parent.count == horner_expected_total(6, degree)
        assert parent.fma_count == horner_expected_fma(6, degree)
        print("  degree {}:     {}".format(degree, parent.display))


def count_de_casteljau_basic():
    print("de_casteljau.basic() ((3n^2 + 3n + 2) / 2 = 3 T_n + 1):")
    for degree in range(1, 5 + 1):
        parent = operation_count.Computation()
        x = operation_count.Float(0.25, parent)
        coeffs = tuple(
            operation_count.Float((-1.0) ** k, parent)
            for k in range(degree + 1)
        )
        p = de_casteljau.basic(x, coeffs)
        assert p.value == 0.5 ** degree
        assert parent.count == 3 * (degree * (degree + 1) // 2) + 1
        print("  degree {}:     {}".format(degree, parent.display))


def de_casteljau_expected_total(K, n):
    """Get the expected flop count for the compensated de Casteljau method.

    When using FMA, the count is

    .. math::

       (15K^2 - 34K + 26)T_n + 6K^2 - 11K + 11.
    """
    Tn = (n * (n + 1)) // 2
    return (15 * K ** 2 - 34 * K + 26) * Tn + 6 * K ** 2 - 11 * K + 11


def de_casteljau_expected_fma(K, n):
    """Get the FMA count for the compensated de Casteljau method.

    When using FMA, the count is

    .. math::

       (3K - 4)T_n

    FMA (fused-multiply-add) instructions.
    """
    Tn = (n * (n + 1)) // 2
    return (3 * K - 4) * Tn


def count_de_casteljau_compensated():
    print("de_casteljau.compensated() (9n^2 + 9n + 7 = 18 T_n + 13):")
    for degree in range(1, 5 + 1):
        parent = operation_count.Computation()
        x = operation_count.Float(0.25, parent)
        coeffs = tuple(
            operation_count.Float((-1.0) ** k, parent)
            for k in range(degree + 1)
        )
        p = de_casteljau.compensated(x, coeffs)
        assert p.value == 0.5 ** degree
        assert parent.count == de_casteljau_expected_total(2, degree)
        assert parent.fma_count == de_casteljau_expected_fma(2, degree)
        print("  degree {}:     {}".format(degree, parent.display))


def count_de_casteljau_compensated3():
    print(
        "de_casteljau.compensated3() ((59n^2 + 59n + 16) / 2 = 59 T_n + 32):"
    )
    for degree in range(1, 5 + 1):
        parent = operation_count.Computation()
        x = operation_count.Float(0.25, parent)
        coeffs = tuple(
            operation_count.Float((-1.0) ** k, parent)
            for k in range(degree + 1)
        )
        p = de_casteljau.compensated3(x, coeffs)
        assert p.value == 0.5 ** degree
        assert parent.count == de_casteljau_expected_total(3, degree)
        assert parent.fma_count == de_casteljau_expected_fma(3, degree)
        print("  degree {}:     {}".format(degree, parent.display))


def count_de_casteljau_compensated4():
    print("de_casteljau.compensated4() (65n^2 + 65n + 9 = 130 T_n + 63):")
    for degree in range(1, 5 + 1):
        parent = operation_count.Computation()
        x = operation_count.Float(0.25, parent)
        coeffs = tuple(
            operation_count.Float((-1.0) ** k, parent)
            for k in range(degree + 1)
        )
        p = de_casteljau.compensated4(x, coeffs)
        assert p.value == 0.5 ** degree
        assert parent.count == de_casteljau_expected_total(4, degree)
        assert parent.fma_count == de_casteljau_expected_fma(4, degree)
        print("  degree {}:     {}".format(degree, parent.display))


def count_de_casteljau_compensated5():
    msg = (
        "de_casteljau.compensated5() ((231n^2 + 231n + 20) / 2 "
        "= 231 T_n + 106):"
    )
    print(msg)
    for degree in range(1, 5 + 1):
        parent = operation_count.Computation()
        x = operation_count.Float(0.25, parent)
        coeffs = tuple(
            operation_count.Float((-1.0) ** k, parent)
            for k in range(degree + 1)
        )
        p = de_casteljau.compensated5(x, coeffs)
        assert p.value == 0.5 ** degree
        assert parent.count == de_casteljau_expected_total(5, degree)
        assert parent.fma_count == de_casteljau_expected_fma(5, degree)
        print("  degree {}:     {}".format(degree, parent.display))


def main():
    count_add_eft()
    print(SEPARATOR)
    count__split()
    print(SEPARATOR)
    count_multiply_eft()
    print(SEPARATOR)
    count__vec_sum()
    print(SEPARATOR)
    count_sum_k()
    print(SEPARATOR)
    count_vs_method_basic()
    print(SEPARATOR)
    count_vs_method_compensated()
    print(SEPARATOR)
    count_horner_basic()
    print(SEPARATOR)
    count_horner_compensated()
    print(SEPARATOR)
    count_horner_compensated3()
    print(SEPARATOR)
    count_horner_compensated4()
    print(SEPARATOR)
    count_horner_compensated5()
    print(SEPARATOR)
    count_horner_compensated6()
    print(SEPARATOR)
    count_de_casteljau_basic()
    print(SEPARATOR)
    count_de_casteljau_compensated()
    print(SEPARATOR)
    count_de_casteljau_compensated3()
    print(SEPARATOR)
    count_de_casteljau_compensated4()
    print(SEPARATOR)
    count_de_casteljau_compensated5()


if __name__ == "__main__":
    main()

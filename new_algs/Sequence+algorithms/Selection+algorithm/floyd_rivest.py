"""
Based on selection algorithm by Robert W. Floyd and Ronald L. Rivest.

Reference:
    https://en.wikipedia.org/wiki/Floyd%E2%80%93Rivest_algorithm
"""
import math
from operator import (gt,
                      lt)
from typing import (Any,
                    Callable,
                    MutableSequence,
                    Optional,
                    Sequence)

from .core.utils import SequenceKeyView as _SequenceKeyView
from .hints import (Comparator,
                    Domain,
                    Key)


def nth_largest(sequence: MutableSequence[Domain],
                n: int,
                *,
                key: Optional[Key] = None) -> Domain:
    """
    Returns n-th largest element
    and partially sorts given sequence while searching.

    +------------+-------------+-----------------+------------------+
    | complexity |    best     |     average     |      worst       |
    +------------+-------------+-----------------+------------------+
    |    time    | ``O(size)`` |   ``O(size)``   | ``O(size ** 2)`` |
    +------------+-------------+-----------------+------------------+
    |   memory   |  ``O(1)``   | ``O(log size)`` |   ``O(size)``    |
    +------------+-------------+-----------------+------------------+

    where ``size = len(sequence)``.

    :param sequence: sequence to search in
    :param n:
        index of the element to search for
        in the sequence sorted by key in descending order
        (e.g. ``n = 0`` corresponds to the maximum element)
    :param key:
        single argument ordering function,
        if none is specified compares elements themselves
    :returns: n-th largest element of the sequence

    >>> sequence = list(range(-10, 11))
    >>> nth_largest(sequence, 0)
    10
    >>> nth_largest(sequence, 1)
    9
    >>> nth_largest(sequence, 19)
    -9
    >>> nth_largest(sequence, 20)
    -10
    >>> nth_largest(sequence, 0, key=abs)
    -10
    >>> nth_largest(sequence, 1, key=abs)
    -10
    >>> nth_largest(sequence, 19, key=abs)
    -1
    >>> nth_largest(sequence, 20, key=abs)
    0
    """
    return select(sequence, n,
                  key=key,
                  comparator=gt)


def nth_smallest(sequence: MutableSequence[Domain],
                 n: int,
                 *,
                 key: Optional[Key] = None) -> Domain:
    """
    Returns n-th smallest element
    and partially sorts given sequence while searching.

    +------------+-------------+-----------------+------------------+
    | complexity |    best     |     average     |      worst       |
    +------------+-------------+-----------------+------------------+
    |    time    | ``O(size)`` |   ``O(size)``   | ``O(size ** 2)`` |
    +------------+-------------+-----------------+------------------+
    |   memory   |  ``O(1)``   | ``O(log size)`` |   ``O(size)``    |
    +------------+-------------+-----------------+------------------+

    where ``size = len(sequence)``.

    :param sequence: sequence to search in
    :param n:
        index of the element to search for
        in the sequence sorted by key in ascending order
        (e.g. ``n = 0`` corresponds to the minimum element)
    :param key:
        single argument ordering function,
        if none is specified compares elements themselves
    :returns: n-th smallest element of the sequence

    >>> sequence = list(range(-10, 11))
    >>> nth_smallest(sequence, 0)
    -10
    >>> nth_smallest(sequence, 1)
    -9
    >>> nth_smallest(sequence, 19)
    9
    >>> nth_smallest(sequence, 20)
    10
    >>> nth_smallest(sequence, 0, key=abs)
    0
    >>> nth_smallest(sequence, 1, key=abs)
    -1
    >>> nth_smallest(sequence, 19, key=abs)
    -10
    >>> nth_smallest(sequence, 20, key=abs)
    10
    """
    return select(sequence, n,
                  key=key,
                  comparator=lt)


def select(sequence: MutableSequence[Domain],
           n: int,
           *,
           start: int = 0,
           stop: Optional[int] = None,
           key: Optional[Key] = None,
           comparator: Comparator) -> Domain:
    """
    Partially sorts given sequence and returns n-th element.

    +------------+-------------+-----------------+------------------+
    | complexity |    best     |     average     |      worst       |
    +------------+-------------+-----------------+------------------+
    |    time    | ``O(size)`` |   ``O(size)``   | ``O(size ** 2)`` |
    +------------+-------------+-----------------+------------------+
    |   memory   |  ``O(1)``   | ``O(log size)`` |   ``O(size)``    |
    +------------+-------------+-----------------+------------------+

    where ``size = len(sequence)``.

    :param sequence: sequence to select from
    :param n: index of the element to select
    :param start: index to start selection from
    :param stop: index to stop selection at
    :param key:
        single argument ordering function,
        if none is specified compares elements themselves
    :param comparator:
        binary predicate that defines the sorting order
    :returns:
        n-th element of the sequence
        with slice partially sorted by key in given order


    >>> from operator import gt, lt
    >>> sequence = list(range(-10, 11))
    >>> select(sequence, 0, stop=5, comparator=gt)
    -5
    >>> select(sequence, 0, stop=5, comparator=lt)
    -10
    >>> select(sequence, 20, start=15, comparator=lt)
    10
    >>> select(sequence, 20, start=15, comparator=gt)
    5
    >>> select(sequence, 5, start=5, stop=15, key=abs, comparator=lt)
    0
    >>> select(sequence, 5, start=5, stop=15, key=abs, comparator=gt)
    10
    """
    if stop is None:
        stop = len(sequence) - 1
    keys = (sequence
            if key is None
            else _SequenceKeyView(sequence, key))
    _presort(sequence, keys, n, start, stop, comparator)
    return sequence[n]


def _presort(sequence: MutableSequence[Domain],
             keys: Sequence[Any],
             n: int,
             start: int,
             stop: int,
             comparator: Comparator) -> None:
    candidate, pivot = sequence[n], keys[n]
    while start < stop:
        if stop - start > 600:
            range_size = stop - start + 1
            i, s = n - start + 1, 0.5 * range_size ** (2 / 3)
            sigma = (0.5 * math.sqrt(math.log(range_size) * s
                                     * (range_size - s) / range_size)
                     * (-1 if i < range_size / 2 else 1))
            _presort(sequence, keys, n,
                     max(start, math.floor(n - i * s / range_size + sigma)),
                     min(stop, math.floor(n + (range_size - i) * s / range_size
                                          + sigma)),
                     comparator)
        sequence[start], sequence[n] = candidate, sequence[start]
        if comparator(pivot, keys[stop]):
            sequence[start], sequence[stop] = sequence[stop], candidate
        pivot_index = _partition(sequence, keys, pivot, start, stop,
                                 comparator)
        if keys[start] == pivot:
            sequence[start], sequence[pivot_index] = (sequence[pivot_index],
                                                      sequence[start])
        else:
            pivot_index += 1
            sequence[stop], sequence[pivot_index] = (sequence[pivot_index],
                                                     sequence[stop])
        if pivot_index <= n:
            start = pivot_index + 1
        if pivot_index >= n:
            stop = pivot_index - 1
        candidate, pivot = sequence[n], keys[n]


def _partition(sequence: MutableSequence[Domain],
               keys: Sequence[Any],
               pivot: Domain,
               start: int,
               stop: int,
               comparator: Callable[[Domain, Domain], bool]) -> int:
    while start < stop:
        sequence[start], sequence[stop] = sequence[stop], sequence[start]
        start += 1
        stop -= 1
        while comparator(keys[start], pivot):
            start += 1
        while comparator(pivot, keys[stop]):
            stop -= 1
    return stop

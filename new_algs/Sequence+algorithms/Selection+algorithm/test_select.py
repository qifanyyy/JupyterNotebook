from operator import gt
from typing import (MutableSequence,
                    Tuple)

from hypothesis import given

from quickselect.floyd_rivest import select
from quickselect.hints import (Comparator,
                               Domain,
                               Key)
from tests import strategies


@given(strategies.elements_lists_with_indices_triplets, strategies.keys,
       strategies.comparators)
def test_properties(elements_with_indices: Tuple[MutableSequence[Domain],
                                                 Tuple[int, int, int]],
                    key: Key,
                    comparator: Comparator) -> None:
    elements, (start, index, stop) = elements_with_indices

    result = select(elements, index,
                    start=start,
                    stop=stop,
                    key=key,
                    comparator=comparator)

    assert result in elements
    assert (sorted(elements[start:stop + 1],
                   reverse=comparator is gt,
                   key=key)[index - start]
            if start <= index <= stop
            else elements[index]) == result

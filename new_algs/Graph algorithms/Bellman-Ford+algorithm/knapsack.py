"""Python implementation of a knapsack problem algorithm."""

import numpy as np


def knapsack(items, size):
    """Takes a list of items and a knapsack size.
    Each item should have a value and a weight packed in a tuple/list.
    Returns selected items and max accumulated value.

    >>> items = [(3, 4), (2, 3), (4, 2), (4, 3)]  # (value, weight)
    >>> size = 6
    >>> knapsack(items, size)
    (8.0, [(4, 3), (4, 2)])
    """

    memo = np.zeros([size + 1, len(items) + 1])
    for i in range(1, len(items) + 1):
        value_i, weight_i = items[i - 1]
        for x in range(size + 1):
            prev_item_value = memo[x, i-1]

            # If current size is smaller than item weight,
            # we place the value of the previous item for the given size x...
            if x < weight_i:
                memo[x, i] = prev_item_value
                continue

            # ...otherwise, we accumulate the current item value together with
            # a value of the previous item, if it fits the remaining size.
            # If it doesn't, then just the current item value is taken,
            # but only when it's bigger than the previous item value...
            prev_current_value = memo[x-weight_i, i-1] + value_i

            # That's why, we choose a higher value before assigning it to the current item.
            memo[x, i] = max(prev_item_value, prev_current_value)

    # Having evaluated values for all combinations of items and sizes (items * sizes),
    # we are now able to point the highest one, which is indexed by the last item and size.
    max_value = memo[size, len(items)]

    # We can localize selected items by taking advantage from the fact,
    # that every eligible item value has to be bigger than the previous one
    # on the same weight position. In other words, if values of consecutive items
    # are the same, then we know, that such a value belongs to the first item it occurred.
    knapsack_items = []
    item_idx = len(items) + 1
    while size:
        # Get index of max value in a row. If tie, then index of first occurrence is taken.
        item_idx = memo[size, :item_idx].argmax()
        if item_idx == 0:
            break
        item = items[item_idx - 1]
        knapsack_items.append(item)
        size -= item[1]  # Decrease size by a weight of a selected item.

    return max_value, knapsack_items


if __name__ == "__main__":
    import doctest
    doctest.testmod()

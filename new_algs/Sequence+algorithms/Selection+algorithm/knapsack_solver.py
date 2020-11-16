import random

from typing import List, Optional

from change_constants import MIN_CHANGE
from output_group import OutputGroup
from utils import assemble_output_set


def approximate_best_subset(utxo_pool: List[OutputGroup], target_value: int,
                            total_lower: int, iterations=1000) -> OutputGroup:

    best_selection = [True for output_group in utxo_pool]
    best_value = total_lower

    for iteration_number in range(iterations):
        if best_value == target_value:
            break
        included = [False for output_group in utxo_pool]
        total_value = 0
        reached_target = False
        number_of_passes = 2
        for pass_number in range(number_of_passes):
            if reached_target:
                break
            for i in range(len(utxo_pool)):
                # The solver here uses a randomized algorithm,
                # the randomness serves no real security purpose but is just
                # needed to prevent degenerate behavior and it is important
                # that the rng is fast. We do not use a constant random sequence,
                # because there may be some privacy improvement by making
                # the selection random.
                if (random.choice([True, False]) if pass_number == 0 else not included[i]):
                    total_value += utxo_pool[i].value
                    included[i] = True
                    if total_value >= target_value:
                        reached_target = True
                        if total_value < best_value:
                            best_value = total_value
                            best_selection = included.copy()
                        total_value -= utxo_pool[i].value
                        included[i] = False

    return assemble_output_set(best_selection, utxo_pool)


def select_coins_knapsack_solver(utxo_pool: List[OutputGroup], target_value: int) -> OutputGroup:
    selected_outputs = OutputGroup()

    lowest_larger: Optional[OutputGroup] = None  # todo: name better
    applicable_groups: List[OutputGroup] = []
    total_lower = 0

    random.shuffle(utxo_pool)

    for output_group in utxo_pool:
        if output_group.value == target_value:
            selected_outputs = OutputGroup()
            selected_outputs.insert_group(output_group)
            return selected_outputs
        elif output_group.value < target_value + MIN_CHANGE:
            applicable_groups.append(output_group)
            total_lower += output_group.value
        elif not lowest_larger or output_group.value < lowest_larger.value:
            lowest_larger = output_group

    if total_lower == target_value:
        selected_outputs = OutputGroup()
        for output_group in applicable_groups:
            selected_outputs.insert_group(output_group)
        return selected_outputs
    if total_lower < target_value:
        if not lowest_larger:
            return OutputGroup()
        else:
            selected_outputs = OutputGroup()
            selected_outputs.insert_group(lowest_larger)
            return selected_outputs

    # Solve subset sum by stochastic approximation
    utxo_pool.sort(reverse=True)
    best_selection = approximate_best_subset(
        applicable_groups, target_value, total_lower)
    if best_selection.value != target_value and total_lower >= target_value + MIN_CHANGE:
        best_selection = approximate_best_subset(
            applicable_groups, target_value + MIN_CHANGE, total_lower)

    # If we have a bigger coin and (either the stochastic approximation didn't find
    # a good solution, or the next bigger coin is closer), return the bigger coin
    if lowest_larger and (
        (
            best_selection.value != target_value
            and best_selection.value < target_value + MIN_CHANGE
        )
        or
        (
            lowest_larger.value <= best_selection.value
        )
    ):
        best_selection = OutputGroup()
        best_selection.insert_group(lowest_larger)

    return best_selection

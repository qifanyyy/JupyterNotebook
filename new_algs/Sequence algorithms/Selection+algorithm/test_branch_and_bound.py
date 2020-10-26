from typing import List

import pytest

from branch_and_bound import select_coins_branch_and_bound
from change_constants import CENT
from tests.fixtures import generate_utxo_pool, make_hard_case
from input_coin import InputCoin
from output_group import OutputGroup

# todo: run tests with retries and repeats

# How many times to run all the tests to have a chance to catch errors
# that only show up with particular random shuffles
RUN_TESTS = 100
# Some tests fail 1% of the time due to bad luck.
# We repeat those tests this many times and only complain if all iterations of the test fail
RANDOM_REPEATS = 5

DEFAULT_NOT_INPUT_FEES = 0


###############################
##### Known Outcome Tests #####
###############################

@pytest.mark.parametrize("target_amount", [1 * CENT, 2 * CENT, 3 * CENT, 4 * CENT])
def test_branch_and_bound_exact_match_single_coin(generate_utxo_pool, target_amount):
    utxo_pool = generate_utxo_pool([
        1 * CENT,
        2 * CENT,
        3 * CENT,
        4 * CENT,
    ])

    selection = select_coins_branch_and_bound(
        utxo_pool, target_amount, 0.5 * CENT, DEFAULT_NOT_INPUT_FEES)

    assert len(selection.outputs) == 1
    assert selection.effective_value == target_amount
    assert selection.outputs[0].effective_value == target_amount


def test_branch_and_bound_insufficient_funds(generate_utxo_pool):
    utxo_pool = generate_utxo_pool([
        1 * CENT,
        2 * CENT,
        3 * CENT,
        4 * CENT,
    ])

    selection = select_coins_branch_and_bound(
        utxo_pool, 11 * CENT, 0.5 * CENT, DEFAULT_NOT_INPUT_FEES)

    assert len(selection.outputs) == 0
    assert selection.effective_value == 0


# Cost of change is greater than the difference between target value and utxo sum
def test_branch_and_bound_expensive_change(generate_utxo_pool):
    utxo_pool = generate_utxo_pool([
        1 * CENT,
        2 * CENT,
        3 * CENT,
        4 * CENT,
    ])

    selection = select_coins_branch_and_bound(
        utxo_pool, 0.9 * CENT, 0.5 * CENT, DEFAULT_NOT_INPUT_FEES)

    assert len(selection.outputs) == 1
    assert selection.effective_value == 1 * CENT
    assert selection.outputs[0].effective_value == 1 * CENT


# Cost of change is less than the difference between target value and utxo sum
def test_branch_and_bound_cheap_change(generate_utxo_pool):
    utxo_pool = generate_utxo_pool([
        1 * CENT,
        2 * CENT,
        3 * CENT,
        4 * CENT,
    ])

    selection = select_coins_branch_and_bound(
        utxo_pool, 0.9 * CENT, 0, DEFAULT_NOT_INPUT_FEES)

    assert len(selection.outputs) == 0
    assert selection.effective_value == 0


def test_branch_and_bound_exact_match_multiple_coins(generate_utxo_pool):
    utxo_pool = generate_utxo_pool([
        1 * CENT,
        2 * CENT,
        3 * CENT,
        4 * CENT,
        5 * CENT
    ])

    selection = select_coins_branch_and_bound(
        utxo_pool, 10 * CENT, 0.5 * CENT, DEFAULT_NOT_INPUT_FEES)

    assert len(selection.outputs) == 3
    assert selection.effective_value == 10 * CENT

    selected_amounts = [
        output.effective_value for output in selection.outputs]
    selected_amounts.sort()

    assert selected_amounts[0] == 1 * CENT
    assert selected_amounts[1] == 4 * CENT
    assert selected_amounts[2] == 5 * CENT


def test_branch_and_bound_impossible(generate_utxo_pool):
    utxo_pool = generate_utxo_pool([
        1 * CENT,
        2 * CENT,
        3 * CENT,
        4 * CENT,
        5 * CENT
    ])

    selection = select_coins_branch_and_bound(
        utxo_pool, 0.25 * CENT, 0.5 * CENT, DEFAULT_NOT_INPUT_FEES)

    assert len(selection.outputs) == 0
    assert selection.effective_value == 0


def test_branch_and_bound_iteration_exhaustion(make_hard_case):
    target_value, utxo_pool = make_hard_case(17)
    selection = select_coins_branch_and_bound(
        utxo_pool, target_value, 0, DEFAULT_NOT_INPUT_FEES)
    assert len(selection.outputs) == 0

    target_value, utxo_pool = make_hard_case(14)
    selection = select_coins_branch_and_bound(
        utxo_pool, target_value, 0, DEFAULT_NOT_INPUT_FEES)
    assert len(selection.outputs) > 0


def test_branch_and_bound_early_bailout_optimization(generate_utxo_pool):
    utxo_pool = generate_utxo_pool(
        [2 * CENT,
         7 * CENT,
         7 * CENT,
         7 * CENT,
         7 * CENT] +
        [5 * CENT for i in range(50000)]
    )
    selection = select_coins_branch_and_bound(
        utxo_pool, 30 * CENT, 5000, DEFAULT_NOT_INPUT_FEES)
    assert len(selection.outputs) == 5
    assert selection.effective_value == 30 * CENT


###############################
####### Behavior Tests ########
###############################

def test_branch_and_bound_consistently_fails_impossible_case(generate_utxo_pool):
    utxo_pool = generate_utxo_pool(
        [i * CENT for i in range(5, 21)]
    )

    for i in range(100):
        selection = select_coins_branch_and_bound(
            utxo_pool, 1 * CENT, 2 * CENT, DEFAULT_NOT_INPUT_FEES)
        assert len(selection.outputs) == 0
        assert selection.effective_value == 0

from utils.selection_algorithm_support import check_order_statistics
from utils.inputs import InputList


def find_median_small_list(L: list) -> int:
    """
    Computes the median for a small list (length <= 5)
    Args:
        L: Sorted list of length <=5

    Returns:
        The median
    """
    assert len(L) <= 5, "You are trying to cheat, this function is used only for " \
                        "small lists (len<=5)"
    return sorted(L)[int(len(L) / 2)]


def choose_pivot(L_init: list, L_iter: list):
    """
    Choose a pivot in a list using the method of median of medians an pop it from the input list
    Args:
        L_init: The initial list from which the pivot will be finally popped
        L_iter: Input list

    Returns:
        Pivot from the list found by median of medians
    """
    n = len(L_iter)
    if n <= 5:
        pivot = find_median_small_list(L_iter)
        L_init.remove(pivot)
        return pivot
    else:
        C = [find_median_small_list(L_iter[i:i + 5]) for i in range(0, n, 5)]
        return choose_pivot(L_init=L_init, L_iter=C)


def deterministic_selection(L_input: list, i: int) -> int:
    """
    Perform a divide to conquer approach of the selection problem.
    We find the pivot at each iteration using a deterministic approach  using the method of median of medians

    Args:
        L_input (list): Input list of integers
        i (int): number of order statistics of the input list in [0..len(L)-1]

    Returns:
        int: The value of the the i-th order statistic of the input list

    """
    L = L_input.copy()
    check_order_statistics(L, i)

    def sub_function(L: list, i: int):
        if len(L) == 1:
            return L[0]
        else:
            pivot = choose_pivot(L_init=L, L_iter=L)
            L_left = [x for x in L if x <= pivot]
            L_right = [x for x in L if x > pivot]
            L = L_left + [pivot] + L_right
            i_pivot = L.index(pivot)
            if i == i_pivot:
                return pivot
            elif i < i_pivot:
                return deterministic_selection(L_left, i)
            else:
                return deterministic_selection(L_right, i - i_pivot - 1)

    return sub_function(L, i)


if __name__ == '__main__':
    test_list = InputList(l_length=5)
    # To implement in the notebook Make a graph of repartition
    print(test_list)
    for i in range(len(test_list)):
        print(f'The {i}-th order statistics is {deterministic_selection(L_input=test_list, i=i)}')
    print(test_list)

from utils.sorting_algorithms import merge_sort, quick_sort
from utils.selection_algorithm_support import check_order_statistics
from utils.inputs import InputList


def merge_sort_reduction(L_input: list, i: int) -> int:
    """
    Perform the selection algorithm with the sorting reduction strategy using merge_sort for the sorting algorithm
    Args:
        L_input (list): Input list of integers
        i (int): number of order statistics of the input list in [0..len(L)-1]

    Returns:
        int: The value of the the i-th order statistic of the input list
    """
    L = L_input.copy()
    check_order_statistics(L, i)
    return merge_sort(L)[i]


def quick_sort_reduction(L_input: list, i: int) -> int:
    """
    Perform the selection algorithm with the sorting reduction strategy using quick_sort for the sorting algorithm
    Args:
        L_input (list): Input list of integers
        i (int): number of order statistics of the input list in [0..len(L)-1]

    Returns:
        int: The value of the the i-th order statistic of the input list
    """
    L = L_input.copy()
    check_order_statistics(L, i)
    return quick_sort(L)[i]


def built_in_sort_reduction(L_input: list, i: int) -> int:
    """
    Perform the selection algorithm with the sorting reduction strategy using the built-in sorted method on list
     for the sorting algorithm
    Args:
        L_input (list): Input list of integers
        i (int): number of order statistics of the input list in [0..len(L)-1]

    Returns:
        int: The value of the the i-th order statistic of the input list
    """
    L = L_input.copy()
    check_order_statistics(L, i)
    return sorted(L)[i]


if __name__ == '__main__':
    test_list = InputList(l_length=10)
    print(test_list)
    for i in range(len(test_list)):
        print(f'The {i}-th order statistics is {built_in_sort_reduction(L=test_list, i=i)}')
    # Test of raise
    # print(f'The {10}-th order statistics is {quick_sort_reduction(L=test_list, i=10)}')

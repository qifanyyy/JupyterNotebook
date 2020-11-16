from utils.inputs import InputListIndex
from utils.selection_algorithm_support import check_order_statistics
from selection_algorithms.first_element_selection import selection_first_element
import random
from compare_algos.collection_algos import CollectionAlgosListIndex


def partition_random_pivot(L: list, left: int, right: int) -> int:
    """
   Makes a partition of the input list relatively to a random pivot
   Parameters
   ----------
   L (list): input list
   left (int): left index of the list to partition
   right (int): right index of the list to partition

   Returns
   -------
   Modifies the input list and returns the index of the position of the pivot
    """
    # Definition of the pivot
    rand_index = random.randint(left, right)
    pivot = L[rand_index]
    # Swap the rand element with the left element
    L[rand_index], L[left] = L[left], L[rand_index]
    # i is the index of the split between elements smaller and bigger than the pivot
    # j is the element that goes through the list
    i = left + 1
    for j in range(left + 1, right + 1):
        if L[j] < pivot:
            L[i], L[j] = L[j], L[i]
            i += 1
    # Final swap to  put the pivot at its right place
    L[left], L[i - 1] = L[i - 1], L[left]
    return i - 1


def randomized_selection(L_input: list, i: int) -> int:
    """
    Perform an analogue strategy to the quick sort algorithm to select the
    i-th number of order statistics of a given list. The pivot is randomly chosen at each iteration

    Args:
        L_input (list): Input list of integers
        i (int): number of order statistics of the input list in [0..len(L)-1]

    Returns:
        int: The value of the the i-th order statistic of the input list

    """

    L = L_input.copy()
    check_order_statistics(L, i)

    def sub_function(L: list, left: int, right: int, i: int):
        if left < right:
            # Partition the list around the pivot (first element) and return the index of the pivot i_pivot
            i_pivot = partition_random_pivot(L, left=left, right=right)
            # In the rare case: i_pivot = i return the pivot
            if i_pivot == i:
                return L[i]
            # Otherwise if i_pivot > i, explore in the left part
            if i_pivot > i:
                return sub_function(L, left=left, right=i_pivot - 1, i=i)
            # Otherwise if i_pivot < i, explore in the right part
            else:
                return sub_function(L, left=i_pivot + 1, right=right, i=i)
        else:
            return L[left]

    return sub_function(L=L, left=0, right=len(L) - 1, i=i)


if __name__ == '__main__':
    compare_algo = CollectionAlgosListIndex(randomized_selection, selection_first_element)
    for i in range(1, 10):
        input_test = InputListIndex(l_length=5 * i)
        print(input_test)
        assert compare_algo.have_same_output(*input_test), 'There is an error somewhere'

    print('stop')

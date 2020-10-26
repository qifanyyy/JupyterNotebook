#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""Week 4 - Search Comparison"""

from timeit import default_timer as timer
import random


def sequential_search(a_list, item):
    """Performs a linear search on a list.

    Args:
        a_list (list): A list of random integers.
        item (int): The item to be searched for.

    Returns:
        bool: Returns True if the item is found, False if not.
    """

    start = timer()
    pos = 0
    found = False

    while pos < len(a_list) and not found:
        if a_list[pos] == item:
            found = True
        else:
            pos = pos + 1
    end = timer()

    return found, (end - start)


def ordered_sequential_search(a_list, item):
    """Performs a linear search on an ordered list.

    Args:
        a_list (list): A list of random integers.
        item (int): Item to be searched for.

    Returns:
        bool: Returns True if the item is found, False if not.
    """

    start = timer()
    pos = 0
    found = False
    stop = False

    while pos < len(a_list) and not found and not stop:
        if a_list[pos] == item:
            found = True
        else:
            if a_list[pos] > item:
                stop = True
            else:
                pos = pos+1
    end = timer()

    return found, (end - start)


def binary_search_iterative(a_list, item):
    """Performs a binary search on an ordered list.

    Args:
        a_list (list): A list of random integers.
        item (int): Item to be searched for.

    Returns:
        bool: Returns True if the item is found, False if not.
    """

    start = timer()
    first = 0
    last = len(a_list) - 1
    found = False

    while first <= last and not found:
        midpoint = (first + last) // 2
        if a_list[midpoint] == item:
            found = True
        else:
            if item < a_list[midpoint]:
                last = midpoint - 1
            else:
                first = midpoint + 1
    end = timer()

    return found, (end - start)


def binary_search_recursive(a_list, item):
    """Performs a recursive binary search on an ordered list.

    Args:
        a_list (list): A list of random integers.
        item (int): The item to be searched for.

    Returns:
        bool: Returns True if the item is found, False if not.
    """

    start = timer()
    if len(a_list) == 0:
        end = timer()
        return False, (end - start)
    else:
        midpoint = len(a_list) // 2
    if a_list[midpoint] == item:
        end = timer()
        return True, (end - start)
    else:
        if item < a_list[midpoint]:
            return binary_search_recursive(a_list[:midpoint], item)
        else:
            return binary_search_recursive(a_list[midpoint + 1:], item)


def random_int_list(n):
    """Generates a list of random integers.

    Args:
        n (int): Number of elements to generate.

    Returns:
        list: Returns a list of random integers. 
    """

    new_list = range(n)
    random.shuffle(new_list)
    return new_list


def check_search_averages(test_input):
    """This will check the average running times of the search
    algorithms on a set of input data. Will then ouput a formatted
    string stating the average run times for each algorithm. 

    Args:
        test_input (list): A list of lists. 
    """

    # Initializing variables
    sequential_avg = 0
    ord_sequential_avg = 0
    bin_iter_avg = 0
    bin_rec_avg = 0

    # Running each search method on each list sequentially
    for random_list in test_input:
        sequential_avg += (sequential_search(random_list, -1))[1]
        # Sorting list since other algorithms depend on a sorted array
        random_list.sort()
        ord_sequential_avg += (ordered_sequential_search(random_list, -1))[1]
        bin_iter_avg += (binary_search_iterative(random_list, -1))[1]
        bin_rec_avg += (binary_search_recursive(random_list, -1))[1]

    print '''
    Sequential Search took {:.7f} seconds to run, on average.
    Ordered Sequential Search took {:.7f} seconds to run, on average.
    Iterative Binary Search took {:.7f} seconds to run, on average.
    Recursive Binary Search took {:.7f} seconds to run, on average.
    '''.format(
        (sequential_avg / len(test_input)),
        (ord_sequential_avg / len(test_input)),
        (bin_iter_avg / len(test_input)),
        (bin_rec_avg / len(test_input))
    )


def main():
    """This program will generate thousands of lists of random
    integers and run a search algorithm on each of them. The 
    average run time of the algorithms will be displayed to the
    user. 
    """

    # Generating various test inputs
    test_input_a = [random_int_list(500) for _ in range(100)]
    test_input_b = [random_int_list(1000) for _ in range(100)]
    test_input_c = [random_int_list(10000) for _ in range(100)]

    print 'Input A, Size of Lists: 500'
    check_search_averages(test_input_a)
    print 'Input B, Size of Lists: 1,000'
    check_search_averages(test_input_b)
    print 'Input C, Size of Lists: 10,000'
    check_search_averages(test_input_c)


if __name__ == '__main__':
    main()

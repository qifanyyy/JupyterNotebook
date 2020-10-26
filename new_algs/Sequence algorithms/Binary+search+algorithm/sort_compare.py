#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""Week 4 - Sort Comparison"""

from timeit import default_timer as timer
import random


def insertion_sort(a_list):
    """Performs an insertion sort on a list of integers.

    Args:
        a_list (list): A list of random integers.

    Returns:
        float: The run time of the search. 
    """

    start = timer()
    for index in range(1, len(a_list)):
        current_value = a_list[index]
        position = index
        while position > 0 and a_list[position - 1] > current_value:
            a_list[position] = a_list[position - 1]
            position = position - 1
        a_list[position] = current_value
    end = timer()
    return (end - start)


def shell_sort(a_list):
    """Performs a shell sort on a list of integers.

    Args:
        a_list (list): A list of random integers.

    Returns:
        float: The run time of the search. 
    """
    start = timer()
    sublist_count = len(a_list) // 2
    while sublist_count > 0:
        for start_position in range(sublist_count):
            gap_insertion_sort(a_list, start_position, sublist_count)
        sublist_count = sublist_count // 2
    end = timer()
    return (end - start)


def gap_insertion_sort(a_list, start, gap):
    for i in range(start + gap, len(a_list), gap):
        current_value = a_list[i]
        position = i
        while position >= gap and a_list[position - gap] > current_value:
            a_list[position] = a_list[position - gap]
            position = position - gap
        a_list[position] = current_value


def python_sort(a_list):
    """Performs a built-in Python sort on a list of integers.

    Args:
        a_list (list): A list of random integers.

    Returns:
        float: The run time of the search. 
    """
    start = timer()
    a_list.sort()
    end = timer()
    return (end - start)


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


def check_sort_averages(test_input):
    """This will check the average running times of the sorting
    algorithms on a set of input data. Will then ouput a formatted
    string stating the average run times for each algorithm. 

    Args:
        test_input (list): A list of lists. 
    """

    # Initializing variables
    insertion_avg = 0
    shell_avg = 0
    python_avg = 0

    # Running each sort method on each list sequentially
    for random_list in test_input:
        # Only return from the algorithm is the running time
        insertion_avg += insertion_sort(random_list)
        # Shuffle the integers again to prepare for next sort method
        random.shuffle(random_list)
        shell_avg += shell_sort(random_list)
        random.shuffle(random_list)
        python_avg += python_sort(random_list)

    print '''
    Insertion Sort took {:.7f} seconds to run, on average.
    Shell Sort took {:.7f} seconds to run, on average.
    Python Sort took {:.7f} seconds to run, on average.
    '''.format(
        (insertion_avg / len(test_input)),
        (shell_avg / len(test_input)),
        (python_avg / len(test_input))
    )


def main():
    """This program will generate thousands of lists of random
    integers and run a sorting algorithm on each of them. The 
    average run time of the algorithms will be displayed to the
    user. 
    """

    # Generating various test inputs
    test_input_a = [random_int_list(500) for _ in range(100)]
    test_input_b = [random_int_list(1000) for _ in range(100)]
    test_input_c = [random_int_list(10000) for _ in range(100)]

    print 'Input A, Size of Lists: 500'
    check_sort_averages(test_input_a)
    print 'Input B, Size of Lists: 1,000'
    check_sort_averages(test_input_b)
    print 'Input C, Size of Lists: 10,000'
    check_sort_averages(test_input_c)


if __name__ == '__main__':
    main()

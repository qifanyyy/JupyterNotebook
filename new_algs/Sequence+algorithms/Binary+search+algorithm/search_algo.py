import random
import numpy
import time
import matplotlib.pyplot as plt
import sys

sys.stdout = open("results.txt", "a+")


def binary_search(A, i, j, x):
    """
    Binary search algorithm to search for x in a list A.

    Parameters:
    A (list): list to be searched
    i (int) : starting index of the search operation in A
    j (int) : ending index of the search operation in A
    x (int) : element to be searched in A

    Returns:
    int: index if x is in A, -1 otherwise
    """

    if j >= i:
        middle = (i + j) // 2

        if A[middle] == x:          # if middle element
            return middle
        elif A[middle] > x:         # if can be in left half
            return binary_search(A, i, middle-1, x)
        else:                       # if can be in right half
            return binary_search(A, middle+1, j, x)

    return -1                       # not found


def random_num_generator(i, j):
    """
    Helper function to generate a random number between i and j
    """

    temp = random.randint(0, 1000000)
    temp = temp % (j-i+1)
    return i + temp


def randomized_search(A, i, j, x):
    """
    Randomized search algorithm to search for x in a list A.

    Parameters:
    A (list): list to be searched
    i (int) : starting index of the search operation in A
    j (int) : ending index of the search operation in A
    x (int) : element to be searched in A

    Returns:
    int: index if x is in A, -1 otherwise
    """

    if j >= i:
        middle = random_num_generator(i, j)

        if A[middle] == x:          # if middle element
            return middle
        elif A[middle] > x:         # if can be in left half
            return randomized_search(A, i, middle-1, x)
        else:                       # if can be in right half
            return randomized_search(A, middle+1, j, x)

    return -1                       # not found


def gen_random_list(n):
    """
    Generate a sorted random list of n elements in the range 1 to 10n.
    Also generate a search list of 1000 elements (200 of them are not in the original list).

    Parameters:
    n (int): size of the list

    Returns:
    list    : sorted random list of n elements
    list    : search list of 1000 elements
    -1 (int): if n is less than 1000
    """

    if n < 1000:
        return -1

    temp_list = random.sample(range(1, n*10), n+200)

    temp_search_list = temp_list[:200]
    temp_list = temp_list[200:]

    temp_search_list = temp_search_list + list(numpy.random.choice(temp_list, size=800, replace=False))
    random.shuffle(temp_search_list)

    return sorted(temp_list), temp_search_list


def multi_search(A, search_list, randomized=False):
    """
    Perform multiple search operations using binary search or randomized search algorithm

    Parameters:
    A (list)            : list to be searched
    search_list (list)  : list of integers to search for
    randomized (boolean): Whether to perform randomized search or not (default: False)

    Returns:
    None
    """

    if randomized:
        print("Random Search\t|", end="\t")
        start_time = time.time()
        for ele in search_list:
            randomized_search(A, 0, len(A)-1, ele)

        end_time = time.time()
        avg_elapsed_time = round((end_time - start_time) * 1000, 4)         # in microseconds

    else:
        print("Binary Search\t|", end="\t")
        start_time = time.time()
        for ele in search_list:
            binary_search(A, 0, len(A)-1, ele)

        end_time = time.time()
        avg_elapsed_time = round((end_time - start_time) * 1000, 4)         # in microseconds

    print("Length A: {}\t|\tSearch Count: {}\t|\tAvg Elapsed Time: {} us".format(len(A), len(search_list), avg_elapsed_time))


def plot_distribution(list_1, list_2, n):
    """
    Helper function to plot distributions of two lists
    """

    plt.hist([list_1, list_2], density=True, bins=35, label=["Number List (A)", "Search List"])
    plt.legend(loc='upper right')
    plt.title("Distribution for N = {}".format(n))
    plt.ylabel("Distribution")
    plt.xlabel("Number List")
    plt.savefig('plot_for_n_{}.png'.format(n))
    plt.close()


if __name__ == '__main__':
    # N = 10000
    list_A, search_list = gen_random_list(10000)
    plot_distribution(list_A, search_list, 10000)

    multi_search(list_A, search_list)
    multi_search(list_A, search_list, randomized=True)

    # N = 100000
    list_A, search_list = gen_random_list(100000)
    plot_distribution(list_A, search_list, 100000)

    multi_search(list_A, search_list)
    multi_search(list_A, search_list, randomized=True)

    # N = 1000000
    list_A, search_list = gen_random_list(1000000)
    plot_distribution(list_A, search_list, 1000000)

    multi_search(list_A, search_list)
    multi_search(list_A, search_list, randomized=True)

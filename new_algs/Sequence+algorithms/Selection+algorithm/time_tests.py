import timeit
import random

import MergeSort
import BubbleSort
import QuickSort
import InsertionSort
import SelectionSort


# Starting with a list of 100 elements, upto 10000 elements
for i in range(100, 10000, 100):
    # for each of our sort algorithms build a timer that will call sort on a list of random integers
    merge = timeit.Timer("MergeSort.sort([random.randint(0,1000) for r in range(%d)])" % i, "from __main__ import random, MergeSort")
    quick = timeit.Timer("QuickSort.sort([random.randint(0,1000) for r in range(%d)])" % i, "from __main__ import random, QuickSort")
    bubble = timeit.Timer("BubbleSort.sort([random.randint(0,1000) for r in range(%d)])" % i, "from __main__ import random, BubbleSort")
    insertion = timeit.Timer("InsertionSort.sort([random.randint(0,1000) for r in range(%d)])" % i, "from __main__ import random, InsertionSort")
    selection = timeit.Timer("SelectionSort.sort([random.randint(0, 1000) for r in range(%d)])" % i, "from __main__ import random, SelectionSort")

    # Run each test 100 times and store the average result in a variable
    merge_time = merge.timeit(number=100)
    quick_time = quick.timeit(number=100)
    bubble_time = bubble.timeit(number=100)
    insertion_time = insertion.timeit(number=100)
    selection_time = selection.timeit(number=100)

    # print the results
    print("Test with %d elements:"%(i))
    print("MergeSort     test: %d, %10.3f" % (i, merge_time))
    print("QuickSort     test: %d, %10.3f" % (i, quick_time))
    print("BubbleSort    test: %d, %10.3f" % (i, bubble_time))
    print("InsertionSort test: %d, %10.3f" % (i, insertion_time))
    print("SelectionSort test: %d, %10.3f" % (i, selection_time))
    print("-----------")

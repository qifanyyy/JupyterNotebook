# Verifier for Assignment 2 for COMP20007 Design of Algorithms Semester 1 2019
# Written by Tobias Edwards <tobias.edwards@unimelb.edu.au>

from __future__ import print_function
import sys
import os
from collections import Counter

# Python2/3 Compatability
try:
    from itertools import izip_longest as zip_longest
except ImportError:
    from itertools import zip_longest


def test_case_name(expected_output_path):
    """
    Takes the expected output path, something like ../p3a-out-3.txt,
    and gives the test case name, in this case p3a-3.
    """
    basename = os.path.basename(expected_output_path)
    basename = basename.replace('-out-', '-')
    basename = basename.replace('-in-', '-')
    basename = basename.replace('.txt', '')
    return basename


def no_output(file_path):
    """
    Takes a path to an output file and returns whether or not there was
    no output. There can be no output if the file doesn't exist or if it is
    empty.
    """
    try:
        return (not os.path.exists(file_path) \
                or not os.path.isfile(file_path) \
                or os.path.getsize(file_path) == 0)
    except OSError:
        return True


class ProgramVerifier:

    def __init__(self, problem, in_path, expected_path, actual_path):
        self.problem = problem
        self.in_path = in_path
        self.expected_path = expected_path
        self.actual_path = actual_path
        self.test_case = test_case_name(in_path)

    def _error(self, message):
        """
        Print an internal error and exit with a failing status code.
        """
        print(self.test_case + ': verifier error (' + message + ')')
        exit(1)

    def _fail(self, message):
        """
        Print that the test case failed, with a given message, and then exit.
        """
        print(self.test_case + ': failed (' + message + ')')
        exit(1)

    def _succeed(self):
        """
        Print that the test case succeeded, then exit.
        """
        print(self.test_case + ': succeeded')
        exit(0)

    def in_lines(self):
        """
        A generator function for the lines in the input file.
        """
        with open(self.in_path, 'r') as in_file:
            for line in in_file:
                line = line.strip()
                try:
                    if ' ' in line:
                        yield [int(x) for x in line.split()]
                    else:
                        yield int(line)
                except ValueError:
                    self._error('couldn\'t parse provided input')

    def expected_lines(self):
        """
        A generator function for the lines in the expected output file.
        """
        with open(self.expected_path, 'r') as expected_file:
            for line in expected_file:
                line = line.strip()
                try:
                    if line == 'No Path':
                        yield line
                    else:
                        yield int(line)
                except ValueError:
                    self._error('couldn\'t parse provided expected output file')

    def actual_lines(self):
        """
        A generator function for the lines in the actual output file.
        """
        with open(self.actual_path, 'r') as actual_file:
            for line in actual_file:
                line = line.strip()
                try:
                    if line == 'No Path':
                        yield line
                    # Note that this is the result of a timeout from rlimit
                    elif 'Program\'s real time limit exceeded.' in line:
                        self._fail('time limit exceeded')
                    else:
                        yield int(line)
                except ValueError:
                    self._error('couldn\'t parse provided actual output file')

    def verify(self):
        """
        Verifies the test case, based on the problem type.
        """
        if self.problem == 'p1a':
            self._verify_p1()
        elif self.problem == 'p1b':
            self._verify_p1(right_handed=True)
        elif self.problem == 'p2a':
            self._verify_p2()
        elif self.problem == 'p2b':
            self._verify_p2(length_limit=True)
        elif self.problem == 'p3':
            self._verify_p3()
        else:
            self._error('unknown problem {}'.format(self.problem))

    def _verify_p1(self, right_handed=False):
        """
        Verifies a solution to Problem 1 by:

            - Confirming that the integers are the same as those in the input
            - Checking the max-heap property
            - Checking the right-handed heap property if right_handed=True
        """

        expected = list(self.expected_lines())
        actual = list(self.actual_lines())

        # Make sure that the same number of elements have been output
        if len(expected) > len(actual):
            self._fail('output contains too few elements')
        if len(expected) < len(actual):
            self._fail('output contains too many elements')

        # Construct a Counter(), i.e., a frequency table for each and confirm
        # that both heaps contain the same elements.
        if Counter(expected) != Counter(actual):
            self._fail('output didn\'t contain the correct elements')

        # Check that for each element the max-heap property is satisfied.
        # If right_handed is true also check whether or not the right child is
        # larger.
        n = len(actual)

        # First insert None into the first index of the heap so that indexing
        # start at 1.
        actual.insert(0, None)

        for i in range(1, n // 2 + 1):
            children = self._heap_children(actual, i)

            # Confirm that the largest child is not larger than the parent
            if max(children) > actual[i]:
                print("child is:" + str(max(children)) + ", parent is " + str(actual[i]))
                self._fail('heap property not satisfied')
                
            # Check that, if we're after a right handed heap, the right
            # child is no smaller than the left.
            if right_handed and len(children) == 2:
                left, right = children
                if right < left:
                    self._fail('right-handed heap property not satisfied')

        self._succeed()

    def _heap_children(self, heap, i):
        """
        Returns the values of i's children (if they exist) as a tuple.

        The left and right children should be at indices 2i and 2i + 1.
        """
        l = 2 * i
        r = 2 * i + 1
        if l >= len(heap):
            return tuple()
        elif r >= len(heap):
            return (heap[l],)
        else:
            return (heap[l], heap[r])

    def _verify_p2(self, length_limit=False):
        """
        Verifies a solution to Problem 2 by:

            - Confirming that the cost is correct
            - Parsing the graph
            - Confirming that the path output does in fact give the correct
              cost (and start and end at 0, n resp.)
        """

        input = self.in_lines()
        expected = self.expected_lines()
        actual = self.actual_lines()

        expected_cost = next(expected)
        actual_cost = next(actual)

        # Handle the "No Path" case
        if expected_cost == 'No Path' and actual_cost == 'No Path':
            self._succeed()
        elif expected_cost != 'No Path' and actual_cost == 'No Path':
            self._fail('incorrectly output "No Path"')
        elif expected_cost == 'No Path' and actual_cost != 'No Path':
            self._fail('should have output "No Path"')

        if expected_cost != actual_cost:
            self._fail('path cost incorrect')

        print(self.test_case + ': path cost correct')

        if not length_limit:
            n = next(input)
        else:
            n, k = next(input)
        graph = self._parse_graph(n, input)

        edges = next(actual)

        if length_limit and edges > k:
            self._fail('path doesn\'t give path with <= k edges')

        sum = 0
        u = next(actual)

        if u != 0:
            self._fail('path should start with 0')

        for _ in range(edges):
            # Fail if we don't see as many edges as we expect
            try:
                v = next(actual)
            except StopIteration:
                self._fail('length of path and vertices provided don\'t match')

            if (u, v) not in graph:
                self._fail('path includes edge which is not in the DAG')
            w = graph[(u, v)]
            sum += w

            # Set u to v so we then consider the next edge
            u = v

        if v != n - 1:
            self._fail('path should end with n - 1')

        if sum != actual_cost:
            self._fail('path provided doesn\'t have correct weight')

        self._succeed()

    def _parse_graph(self, n, input):
        """
        Parses the graph from Problem 2.

        Returns a dictionary mapping edge (u, v) to weight w_uv.
        """
        edges = {}
        for u in range(n):
            deg = next(input)
            for _ in range(deg):
                v, w = next(input)
                edges[(u, v)] = w
        return edges

    def _verify_p3(self):
        """
        Verifies a solution to Problem 3 by:

            - Confirming that the height and size of the original BST are
              correct
            - Confirming that there are no duplicates
            - Confirming that the output binary tree contains the correct
              elements
            - Confirming that the balanced binary tree is:
                - Balanced (i.e., has a balance factor of {-1, 0, 1} at each
                  node)
                - Is a search tree.
        """

        expected_generator = self.expected_lines()
        actual_generator = self.actual_lines()

        # Confirm that the size is correct.
        size_expected = next(expected_generator)
        size_actual = next(actual_generator)
        if size_expected != size_actual:
            self._fail('incorrect number of nodes in tree')

        # Confirm that the height is correct.
        height_expected = next(expected_generator)
        height_actual = next(actual_generator)
        if height_expected != height_actual:
            self._fail('incorrect height')

        # They get 50% of the marks for having the size and height correct,
        # so output "number of nodes and height correct".
        print(self.test_case + ': number of nodes and height correct')

        expected = self._read_bst(expected_generator)
        actual = self._read_bst(actual_generator)

        # The output shouldn't contain any trailing -1s
        if actual[-1] == -1:
            self._fail('output contains trailing -1')

        # Shouldn't contain duplicates
        negatives_removed = [i for i in actual if i != -1]
        negatives_removed_set = set(negatives_removed)
        if len(negatives_removed) != len(negatives_removed_set):
            self._fail('tree contains duplicate elements')

        # Must contain the same elements as in the expected output
        if negatives_removed_set != {i for i in expected if i != -1}:
            self._fail('didn\'t contain expected elements')

        # Add a None at the first element so that indexing starts from 1
        actual.insert(0, None)

        # Iterate through all of the nodes and confirm that the search tree
        # property holds (and compute the height, and confirm it's balanced).
        n = len(actual)
        height = [None] * n
        for i in reversed(range(1, n)):
            x = actual[i]
            if x == -1:
                height[i] = 0
                continue

            l = 2 * i
            l_height = 0
            if l < n:
                l_height = height[l]

            r = 2 * i + 1
            r_height = 0
            if r < n:
                r_height = height[r]

            height[i] = 1 + max(l_height, r_height)

            # Fail if the balance factor is not in {-1, 0, 1}
            balance_factor = abs(r_height - l_height)
            if balance_factor > 1:
                self._fail('tree not balanced')

            # Confirm that the tree is a search tree
            if l < n and actual[l] != -1 and actual[l] >= x:
                self._fail('search tree condition left < parent violated')
            if r < n and actual[r] != -1 and actual[r] <= x:
                self._fail('search tree condition right > parent violated')

            # Also, the tree should not be disconnected. i.e., if this
            # element is not -1 (and it is not the root) then its parent
            # should not be -1
            parent = i // 2
            if parent > 0 and actual[parent] == -1:
                self._fail('tree disconnected')

        self._succeed()


    def _read_bst(self, generator):
        """
        Reads in a bst into a list from a generator of which the first element
        is the number of elements to be read in, and the rest are those
        elements.
        """
        bst = []
        n = next(generator)
        for _ in range(n):
            try:
                bst.append(next(generator))
            except StopIteration:
                self._fail('number of elements provided less than output on line 3')
        return bst


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('usage: python3 test.py <problem> <input_path> <expected_output_path> <actual_output_path>')
        print('')
        print('\tThis program takes as input the path to the test case input file, the expected')
        print('\toutput for that test case and the actual output (i.e., your program\'s output).')
        print('')
        print('\tYou must specify the problem which is being tested as well.')
        print('\tThe possible problems are:')
        print('\t\t{p1a, p1b, p2a, p2b, p3}')
        exit(1)

    problem = sys.argv[1]
    in_path = os.path.join(os.getcwd(), sys.argv[2])
    expected_path = os.path.join(os.getcwd(), sys.argv[3])
    actual_path = os.path.join(os.getcwd(), sys.argv[4])

    verifier = ProgramVerifier(problem, in_path, expected_path, actual_path)

    if no_output(in_path):
        verifier._error('input file not found')
    if no_output(expected_path):
        verifier._error('expected output file not found')

    # Check whether or not there was any output created
    if no_output(actual_path):
        verifier._fail('no output')

    # Check that the output didn't time out by reading the whole thing in
    # and checking the last line.
    with open(actual_path, 'r') as actual_file:
        for line in actual_file:
            if 'Program\'s real time limit exceeded.' in line:
                verifier._fail('time limit exceeded')


    verifier.verify()

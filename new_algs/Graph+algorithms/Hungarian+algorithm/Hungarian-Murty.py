#!/usr/bin/python
from copy import copy, deepcopy
import sys
import numpy as np
# (c) 2015 Sandip De (1sandipde@gmail.com)

def main():
  a=np.loadtxt('input.test')
#  a=np.random.random((100,100))
  costs=k_best_costs(20,a)
  for x in costs:
    print (x)

def k_best_costs(nbest,matrix):
  
  hun=linear_assignment(matrix)
  cost=0.0
  best_costs=[]
  node_list=[] # the node list
  cost_list=[] #list containing total costs
  rsrv_list=[] # list containing the costs which are not included in subset
  for pair in hun:
     cost+=matrix[pair[0],pair[1]]
  node_list.append(matrix)
  cost_list.append(cost)
  rsrv_list.append(0.0)
#  partition_list(a,node_list,cost_list,rsrv_list)
  for x in range (0,nbest-1):
    min_cost=min(cost_list)
    best_costs.append(min_cost)
    min_index=cost_list.index(min_cost)
    partition_list(node_list[min_index],node_list,cost_list,rsrv_list)
    cost_list[min_index]=10E6
  return best_costs
  
def partition_list(matrix,node_list,cost_list,rsrv_list):
  pair=[]
  min_index=cost_list.index(min(cost_list))
  assignments=linear_assignment(matrix)
  #print "PARTITIONING", len(node_list)
  for m in range (0,len(assignments)-1):
    pair=assignments[m]
    node=copy(matrix)
    node[pair[0],pair[1]]=10E6
    row_list=[]
    col_list=[]
    rsrv_cost=0.0
    for x in range(0,m):
      row_list.append(assignments[x][0])
      col_list.append(assignments[x][1])
      rsrv_cost+=matrix[assignments[x][0],assignments[x][1]]
    node=remove_row_col(node,row_list,col_list)
    hun=linear_assignment(node)
    node_list.append(node)
    cost=0.0
    for pair in hun:
      cost+=node[pair[0],pair[1]]
    #print m, cost
    rsrv_cost+=rsrv_list[min_index]
    cost_list.append(cost+rsrv_cost)
    rsrv_list.append(rsrv_cost)
  return 

def remove_row_col(matrix,row,col):
#sorting in descending order so that it is easy to remove
  row.sort(reverse=True)
  col.sort(reverse=True)
  for r in row:
    matrix=np.delete(matrix,(r), axis=0)
  for c in col:
    matrix=np.delete(matrix,(c), axis=1)
  return matrix
  
"""
Solve the unique lowest-cost assignment problem using the
Hungarian algorithm (also known as Munkres algorithm).

"""
# Based on original code by Brain Clapper, adapted to NumPy by Gael Varoquaux.
# Heavily refactored by Lars Buitinck.

# Copyright (c) 2008 Brian M. Clapper <bmc@clapper.org>, Gael Varoquaux
# Author: Brian M. Clapper, Gael Varoquaux
# LICENSE: BSD


try:
  np.array(5).astype(float, copy=False)
except TypeError:
  # Compat where astype accepted no copy argument
  def astype(array, dtype, copy=True):
    if not copy and array.dtype == dtype:
      return array
    return array.astype(dtype)
else:
  astype = np.ndarray.astype


def linear_assignment(X):
    """Solve the linear assignment problem using the Hungarian algorithm.

    The problem is also known as maximum weight matching in bipartite graphs.
    The method is also known as the Munkres or Kuhn-Munkres algorithm.

    Parameters
    ----------
    X : array
        The cost matrix of the bipartite graph

    Returns
    -------
    indices : array,
        The pairs of (row, col) indices in the original array giving
        the original ordering.

    References
    ----------

    1. http://www.public.iastate.edu/~ddoty/HungarianAlgorithm.html

    2. Harold W. Kuhn. The Hungarian Method for the assignment problem.
       *Naval Research Logistics Quarterly*, 2:83-97, 1955.

    3. Harold W. Kuhn. Variants of the Hungarian method for assignment
       problems. *Naval Research Logistics Quarterly*, 3: 253-258, 1956.

    4. Munkres, J. Algorithms for the Assignment and Transportation Problems.
       *Journal of the Society of Industrial and Applied Mathematics*,
       5(1):32-38, March, 1957.

    5. http://en.wikipedia.org/wiki/Hungarian_algorithm
    """
    indices = _hungarian(X).tolist()
    indices.sort()
    # Re-force dtype to ints in case of empty list
    indices = np.array(indices, dtype=int)
    # Make sure the array is 2D with 2 columns.
    # This is needed when dealing with an empty list
    indices.shape = (-1, 2)
    return indices


class _HungarianState(object):
    """State of one execution of the Hungarian algorithm.

    Parameters
    ----------
    cost_matrix : 2D matrix
        The cost matrix. Does not have to be square.
    """

    def __init__(self, cost_matrix):
        cost_matrix = np.atleast_2d(cost_matrix)

        # If there are more rows (n) than columns (m), then the algorithm
        # will not be able to work correctly. Therefore, we
        # transpose the cost function when needed. Just have to
        # remember to swap the result columns back later.
        transposed = (cost_matrix.shape[1] < cost_matrix.shape[0])
        if transposed:
            self.C = (cost_matrix.T).copy()
        else:
            self.C = cost_matrix.copy()
        self.transposed = transposed

        # At this point, m >= n.
        n, m = self.C.shape
        self.row_uncovered = np.ones(n, dtype=np.bool)
        self.col_uncovered = np.ones(m, dtype=np.bool)
        self.Z0_r = 0
        self.Z0_c = 0
        self.path = np.zeros((n + m, 2), dtype=int)
        self.marked = np.zeros((n, m), dtype=int)

    def _find_prime_in_row(self, row):
        """
        Find the first prime element in the specified row. Returns
        the column index, or -1 if no starred element was found.
        """
        col = np.argmax(self.marked[row] == 2)
        if self.marked[row, col] != 2:
            col = -1
        return col

    def _clear_covers(self):
        """Clear all covered matrix cells"""
        self.row_uncovered[:] = True
        self.col_uncovered[:] = True


def _hungarian(cost_matrix):
    """The Hungarian algorithm.

    Calculate the Munkres solution to the classical assignment problem and
    return the indices for the lowest-cost pairings.

    Parameters
    ----------
    cost_matrix : 2D matrix
        The cost matrix. Does not have to be square.

    Returns
    -------
    indices : 2D array of indices
        The pairs of (row, col) indices in the original array giving
        the original ordering.
    """
    state = _HungarianState(cost_matrix)

    # No need to bother with assignments if one of the dimensions
    # of the cost matrix is zero-length.
    step = None if 0 in cost_matrix.shape else _step1

    while step is not None:
        step = step(state)

    # Look for the starred columns
    results = np.array(np.where(state.marked == 1)).T

    # We need to swap the columns because we originally
    # did a transpose on the input cost matrix.
    if state.transposed:
        results = results[:, ::-1]

    return results


# Individual steps of the algorithm follow, as a state machine: they return
# the next step to be taken (function to be called), if any.

def _step1(state):
    """Steps 1 and 2 in the Wikipedia page."""

    # Step1: For each row of the matrix, find the smallest element and
    # subtract it from every element in its row.
    state.C -= state.C.min(axis=1)[:, np.newaxis]
    # Step2: Find a zero (Z) in the resulting matrix. If there is no
    # starred zero in its row or column, star Z. Repeat for each element
    # in the matrix.
    for i, j in zip(*np.where(state.C == 0)):
        if state.col_uncovered[j] and state.row_uncovered[i]:
            state.marked[i, j] = 1
            state.col_uncovered[j] = False
            state.row_uncovered[i] = False

    state._clear_covers()
    return _step3


def _step3(state):
    """
    Cover each column containing a starred zero. If n columns are covered,
    the starred zeros describe a complete set of unique assignments.
    In this case, Go to DONE, otherwise, Go to Step 4.
    """
    marked = (state.marked == 1)
    state.col_uncovered[np.any(marked, axis=0)] = False

    if marked.sum() < state.C.shape[0]:
        return _step4


def _step4(state):
    """
    Find a noncovered zero and prime it. If there is no starred zero
    in the row containing this primed zero, Go to Step 5. Otherwise,
    cover this row and uncover the column containing the starred
    zero. Continue in this manner until there are no uncovered zeros
    left. Save the smallest uncovered value and Go to Step 6.
    """
    # We convert to int as numpy operations are faster on int
    C = (state.C == 0).astype(np.int)
    covered_C = C * state.row_uncovered[:, np.newaxis]
    covered_C *= astype(state.col_uncovered, dtype=np.int, copy=False)
    n = state.C.shape[0]
    m = state.C.shape[1]
    while True:
        # Find an uncovered zero
        row, col = np.unravel_index(np.argmax(covered_C), (n, m))
        if covered_C[row, col] == 0:
            return _step6
        else:
            state.marked[row, col] = 2
            # Find the first starred element in the row
            star_col = np.argmax(state.marked[row] == 1)
            if not state.marked[row, star_col] == 1:
                # Could not find one
                state.Z0_r = row
                state.Z0_c = col
                return _step5
            else:
                col = star_col
                state.row_uncovered[row] = False
                state.col_uncovered[col] = True
                covered_C[:, col] = C[:, col] * (
                    astype(state.row_uncovered, dtype=np.int, copy=False))
                covered_C[row] = 0


def _step5(state):
    """
    Construct a series of alternating primed and starred zeros as follows.
    Let Z0 represent the uncovered primed zero found in Step 4.
    Let Z1 denote the starred zero in the column of Z0 (if any).
    Let Z2 denote the primed zero in the row of Z1 (there will always be one).
    Continue until the series terminates at a primed zero that has no starred
    zero in its column. Unstar each starred zero of the series, star each
    primed zero of the series, erase all primes and uncover every line in the
    matrix. Return to Step 3
    """
    count = 0
    path = state.path
    path[count, 0] = state.Z0_r
    path[count, 1] = state.Z0_c

    while True:
        # Find the first starred element in the col defined by
        # the path.
        row = np.argmax(state.marked[:, path[count, 1]] == 1)
        if not state.marked[row, path[count, 1]] == 1:
            # Could not find one
            break
        else:
            count += 1
            path[count, 0] = row
            path[count, 1] = path[count - 1, 1]

        # Find the first prime element in the row defined by the
        # first path step
        col = np.argmax(state.marked[path[count, 0]] == 2)
        if state.marked[row, col] != 2:
            col = -1
        count += 1
        path[count, 0] = path[count - 1, 0]
        path[count, 1] = col

    # Convert paths
    for i in range(count + 1):
        if state.marked[path[i, 0], path[i, 1]] == 1:
            state.marked[path[i, 0], path[i, 1]] = 0
        else:
            state.marked[path[i, 0], path[i, 1]] = 1

    state._clear_covers()
    # Erase all prime markings
    state.marked[state.marked == 2] = 0
    return _step3


def _step6(state):
    """
    Add the value found in Step 4 to every element of each covered row,
    and subtract it from every element of each uncovered column.
    Return to Step 4 without altering any stars, primes, or covered lines.
    """
    # the smallest uncovered value in the matrix
    if np.any(state.row_uncovered) and np.any(state.col_uncovered):
        minval = np.min(state.C[state.row_uncovered], axis=0)
        minval = np.min(minval[state.col_uncovered])
        state.C[np.logical_not(state.row_uncovered)] += minval
        state.C[:, state.col_uncovered] -= minval
    return _step4


    
if __name__ == '__main__':
   main(*sys.argv[1:])

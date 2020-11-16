from pygraph.core import *
import pygraph.algorithms.traversal as traversal
import pygraph.algorithms.strong_components as scc

def acyclic_closure(digraph):
    """
    @digraph: Digraph

    Generates reachability matrix for an acyclic digraph.

    Reachability matrix allows for constant time querying
    of whether node i can reach node j in a digraph.

    """

    matrix = ByteNodeMatrix()

    for i in digraph.nodes_set():
        for j in digraph.nodes_set():
            reaches = (i == j) or traversal.dfs(digraph, i, None, lambda v: v != j)

            if reaches:
                matrix.set(i, j, 1)
            else:
                matrix.set(i, j, 0)

    return matrix


def acyclic_reduce(digraph):
    """
    @digraph: Digraph

    Removes redundant edges from a acyclic digraph. The time complexity
    of the actual algorithm for G = (V, E) is O(|V|*|V|*|E|).

    """

    remove = dict()
    matrix  = acyclic_closure(digraph)

    for i in digraph.nodes_set():
        for j in digraph.nodes[i]:
            if i == j: continue
            if not matrix.get(i, j): continue

            for k in digraph.nodes[i]:
                if j == k: continue

                if matrix.get(j, k) == 1:
                    # If this happens it means there are edges i -> j and
                    # j -> k. Because this is an acyclic closure, we
                    # therefore have also edge i -> k, which can be
                    # removed as redundant.

                    if i not in remove: remove[i] = set()
                    remove[i].add(k)
                    matrix.set(i, k, 0)

    for i in remove:
        for j in remove[i]:
            digraph.nodes[i].remove(j)
            digraph.incoming[j].remove(i)


def reduce(digraph):
    """
    @digraph: Digraph

    Returns quotient digraph G' from the digraph G with redundant
    edges removed. Check G'.nodemap for mapping of nodes in G to nodes
    in G'.

    """

    quotient = scc.quotient(digraph)
    acyclic_reduce(quotient)

    return quotient
import random
import timeit
from pprint import pprint
from copy import deepcopy
import click

"""
Matt M
21 Feb 2017
CSC 721

See README.md for running instructions
"""


MAXINT = 100000000

#To Configure Random
#TODO Convert to @click arguments
N = 9
tile_size = 3

global_debug = False
negative_edges = True

def generateAdjMatrix(dim, connectivity=.5):
    """
    Generates a random adjancy matrix with dimensions nxn, n = dim
    Percent chance of an edge is the connectivity score, default 50%, not sure what's a realistic estimate
    Diagonals are 0
    No connection represented by MAXINT
    Possibly contains negative cycles (bad), causes issues sometimes
    """
    global negative_edges

    matrix = []

    if negative_edges:
        lower_bound_weight = -1
    else:
        lower_bound_weight = 1

    #create n x n matrix (doubly nested list) of 0s
    for i in range(0, dim):
        matrix.append([0] * dim)

    #add random points so it's a sparse unconnected matrix (50% of entries filled?)
    rand_row = 0
    rand_col = 0
    for i in range(0, int(connectivity * (dim**2))):
        rand_row = random.randint(0, dim-1)
        rand_col = random.randint(0, dim-1)
        if(rand_col == rand_row):
            pass #don't let diagonal be non-zero
        else:
            rand_weight = random.randint(lower_bound_weight, 20)
            matrix[rand_row][rand_col] = rand_weight

    #for points that do not have a weight, so 0, and are not matrix[i][j] where i = j, set to maxint
    for i in range(0, dim):
        for j in range(0, dim):
            if(i == j):
                pass
            elif(matrix[i][j] != 0):
                pass
            else:
                matrix[i][j] = MAXINT

    return matrix


def floydWarshall(graph):
    """
    Traiditonal Floyd-Warshall
    """
 
    #Starting dist matrix is same as graph
    dist = [deepcopy(i) for i in graph]     

    N = len(graph[0])
    for k in range(N):
 
        # pick all vertices as source one by one
        for i in range(N):
 
            # Pick all vertices as destination for the
            # above picked source
            for j in range(N):
 
                # If vertex k is on the shortest path from 
                # i to j, then update the value of dist[i][j]
                dist[i][j] = min(dist[i][j], dist[i][k]+ dist[k][j])

    return dist


def padMatrix(matrix, tile_size):
    """
    Pads an adjancy matrix with rows and cols of MAXINT to make it tileable by tile_size
    """
    dimension_rem = (len(matrix[0]) % tile_size)
    if dimension_rem == 0:
        #matrix is divisible by size
        return matrix
    else:
        dim_to_add = tile_size - dimension_rem

    total_dim = len(matrix[0]) + dim_to_add

    for i in range(len(matrix)): #Add columns to each row of orig
        for j in range(dim_to_add):
            matrix[i].append(MAXINT)


    for i in range(dim_to_add): #Go ahead and append on rows of total_dim of MAXINTS
        matrix.append([MAXINT for i in range(total_dim)])

    #Sanity cecks
    assert len(matrix) == total_dim
    assert len(matrix[0]) == total_dim

    return matrix

def updateSubmatrix(a_row, a_col, b_row, b_col, c_row, c_col, matrix, block_size, debug=False):
    """
    Pass in the top right coordinates of the A, B, and C blocks.
    matrix is the full dist matrix, passed around this way so don't have to pass partial submatricies
    block_size tells us how far to iterate
    debug is a flag to get detailed tracing info
    """
    for k in range(0, block_size):
        for i in range(0, block_size):
            for j in range(0, block_size):
                matrix[a_row + i][a_col + j] = min(matrix[a_row + i][a_col + j],
                                                   matrix[b_row + i][b_col + k] + matrix[c_row + k][c_col + j])
                if debug:
                    print("Ai, Aj", a_row + i, a_col + j, "Bi, Bk", b_row+i, b_col+k, "Ck, Cj", c_row+k, c_col+j)
    return matrix

def tiledFW(matrix, tile_size):
    """
    Implementation of Tiled FW algorithm.
    Pass in matrix and desired tile size.
    """

    #confirm that dimension and tile size are compatible and fix if not
    matrix = padMatrix(matrix, tile_size)

    #figure out how far to iterate and how many times
    num_tiles_row = int(len(matrix)/tile_size)
    nb_row = int(len(matrix)/num_tiles_row)

    for d in range(num_tiles_row): #Iterator for d*n/b to position our main pointer

        #"Phase 1" tile (self-referential) A=B=C
        updateSubmatrix(d*nb_row, d*nb_row, d*nb_row, d*nb_row, d*nb_row, d*nb_row, matrix, tile_size)

        #"Phase 2" tile(s) - tiles in the same row as phase 1 tile
        for j in range(num_tiles_row):
            if j == d:
                pass
            else:
                updateSubmatrix(d*nb_row, j*nb_row,
                                d*nb_row, d*nb_row,
                                d*nb_row, j*nb_row,
                                matrix, tile_size)

        #"Phase 3" tile(s) - tiles in the same col as phase 1 tile
        for i in range(num_tiles_row):
            if i == d:
                pass
            else:
                updateSubmatrix(i*nb_row, d*nb_row,
                                i*nb_row, d*nb_row,
                                d*nb_row, d*nb_row,
                                matrix, tile_size)

        #"Phase 3" tile(s) - tiles not in same row/col as phase 1 tile
        #This works by iterating over the 'tile corners' and if (i | j) shared by 'phase 1' tile, skip it
        #If not, update it by using the tile(s) in it's same row/col and 'phase 1' col/row
        for i in range(num_tiles_row):
            for j in range(num_tiles_row):
                #print(d*nb_row, i*nb_row, j*nb_row)
                if i == d or j == d:
                    pass #block updated
                else:
                    updateSubmatrix(i*nb_row, j*nb_row,
                                    i*nb_row, d*nb_row,
                                    d*nb_row, j*nb_row,
                                    matrix, tile_size)
    return matrix

def testCase(n, tile, debug=False):
    """
    Generateds a random graph, computes and times FW with traditional and tiled methods
    Compares results for accuracy.
    n is dimension of desired matrix
    tile is tile size
    """
    #Generate random graph
    adj_mat = generateAdjMatrix(n)

    #Traditional
    print("Running Naieve FW on n x n, n = %s" % n)
    start_time = timeit.default_timer()

    dist_naieve = floydWarshall(adj_mat)

    elapsed = timeit.default_timer() - start_time
    print("Finished, took %s seconds" % elapsed)

    # Tiled
    print("Running Tiled FW on same n x n matrix, n = %s, tile_size = %s" % (n, tile))
    start_time = timeit.default_timer()

    dist_tiled = tiledFW(adj_mat, tile)

    elapsed = timeit.default_timer() - start_time
    print("Finished, took %s seconds" % elapsed)

    print("Correctness Info:")
    for i in range(n):
        for j in range(n):
            if dist_naieve[i][j] != dist_tiled[i][j]:
                print("Error, elements (%s, %s) differ" % (i, j))
                if debug:
                    print("Dumping distance naieve:")
                    pprint(dist_naieve)
                    print("Dumping distance tiled:")
                    pprint(dist_tiled)
                return False

    print("Correctness Check Passed!!")
    if debug:
        print("Dumping distance naieve:")
        pprint(dist_naieve)
        print("Dumping distance tiled:")
        pprint(dist_tiled)

    return True


def main():
    global N
    global tile_size
    global global_debug

    #This matrix found on
    # https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm#Example
    #Verified that traditional FW found the correct result
    wiki_matrix = [
    [0, MAXINT, -2, MAXINT],
    [4, 0, 3, MAXINT],
    [MAXINT, MAXINT, 0, 2],
    [MAXINT, -1, MAXINT, 0]
    ]

    #is size 4, use tile size 2 for testing on wiki matrix
    block_size = 2
    print("****WIKI MATRIX TESTING****")
    padMatrix(wiki_matrix, block_size)
    print("Initial Matrix:")
    pprint(wiki_matrix)

    print("Solved with normal FW:")
    pprint(floydWarshall(wiki_matrix))

    print("Solved with tiled:")
    pprint(tiledFW(wiki_matrix, block_size))
    

    print("****RAND GENERATED MATRIX****")
    test_status = testCase(N, tile_size, debug=global_debug)


if __name__ == '__main__':
    main()















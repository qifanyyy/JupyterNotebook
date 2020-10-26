import numpy as np
import sys
import random
import time
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s", action="store_true", dest="stock")
parser.add_option("-v", action="store_true", dest="verbose")
parser.add_option("-m", action="store_true", dest="matrix")
parser.add_option("-e", action="store_true", dest="edge_list")
parser.add_option("-d", action="store_true", dest="distance")
parser.add_option("-c", action="store_true", dest="clock")
parser.add_option("-f", action="store_true", dest="file")
parser.add_option("-r", "--random", action="store", type="int", dest="random", help="randomizes edge weights for the adjancency matrix")
parser.add_option("-l", "--limit", action="store", type="int", dest="random_limit", help="upper limit to the randomizer")

(options, args) = parser.parse_args()

def kruskal(n, m, E):
    i = 0
    j = 0
    p = 0
    q = 0
    flag_start = True
    flag_stop = False
    e = (0,0)
    # Sort the me edges in E by weight in nondecreasing order;
    F_list = []
    F_mat = []
    row = []
    start_index_list = []
    stop_index_list = []
    vert_set = set([])
    vert_set_list = []
    candidate = set([])

    
    # print "F_mat = ", F_mat

    # print "E = ", E

    # sort E
    E.sort(key=lambda tup: int(tup[2]))
    # print "[sort] E = ", E
    
    k = 0
    while ( len(F_list) < (n-1)):
        candidate = set( [ E[k][0], E[k][1] ] )
        # print "vert_set = ", vert_set
        # print "candidate = ", candidate

        # find where
        index_of_set = findLocationOfSet(vert_set_list, candidate)

        # print "index_of_set: ", index_of_set
        if index_of_set != -1:
            num_of_same_verts = len(vert_set_list[index_of_set] & candidate)
        else:
            num_of_same_verts = 0

        # print "num_of_same_verts = ", num_of_same_verts

        # 2-peices of graphs
        if num_of_same_verts == 0:

            # fuse the set
            vert_set_list.append(candidate)
            # print "vert_set_list = ", vert_set_list

            # append that edge
            F_list.append(E[k])
            # print "F_list = ", F_list

        # adding on to this graph
        elif num_of_same_verts == 1:

            # at the correct set, unify the sets
            vert_set_list[index_of_set] = vert_set_list[index_of_set].union(candidate)
            # print "vert_set_list = ", vert_set_list

            # append that edge
            F_list.append(E[k])
            # print "F_list = ", F_list

        # else:

            # print ""
        
        k = k + 1

        # print ""

    # return the edge list and matrix
    return F_list

def isPromising(vert_set, candidate):
    # print "isPromising : vert_set & candidate  : ", len(vert_set & candidate)
    if len(vert_set & candidate) >= 2:
        return False
    return True

def findLocationOfSet(vert_set_list, candidate):

    for i in range (0, len(vert_set_list)):
        # print "vert_set_list[i] = ", vert_set_list[i]
        # print "candidate = ", candidate
        if len(vert_set_list[i] & candidate) >= 1:
            return i

    # default to NEG one for not present
    return -1

def get_edge_list(mat):
    n = len(mat[0])
    F_list = []
    inf = sys.maxint
    for i in range(0, n):
        for j in range(i+1, n):
            edge_weight = mat[i][j]
            if edge_weight < (inf - 1):
                F_list.append((i, j, mat[i][j]))
    return F_list

def edge_list_to_adj_matrix(edge_list):
    row = []
    F_mat = []
    for i in range(0,n):
        for j in range(0,n):
            row.append(0)
        F_mat.append(row)
        row = []

    for x in range(0,len(edge_list)):
        i = edge_list[x][0]
        j = edge_list[x][1]
        weight = edge_list[x][2]
        F_mat[i][j] = weight

    return F_mat

def get_dist_upper_triange(matrix):
    total = 0
    for i in range(0,n):
        for j in range(i,n):
            total = total + matrix[i][j]
    return total

def uniqueify_dble_tup( items ):

    print "================================="
    print ""

    new_items = []

    for i in range(0,len(items)):
        new_items.append(items[i])
    
    for i in range(0, len(new_items) - 1):

        item1 = int(new_items[i][0])
        
        for j in range(i+1, len(new_items)):

            item2 = int(new_items[j][0])

            if item1 == item2:
                new_items[i] = (-(i+1),-(i+1))

    new_new_items = []

    for i in range (0, len(new_items)):
        if new_items[i][0] > 0:
            new_new_items.append(new_items[i])

    print "leaving! ... new_new_items = ", str(new_new_items)

    print ""
    print "================================="
    return new_new_items

# ==============================================================
# ============================ MAIN ============================
# ==============================================================

if __name__ == "__main__":

    inf = sys.maxint

    if options.random:
        n = options.random
        random_limit = 10
        if options.random_limit:
            random_limit = options.random_limit
        W = []
        row = []
        for i in range(0,n):
            for j in range(0,n):
                row.append(0)
            W.append(row)
            row = []
        for i in range(0,n):
            for j in range(i+1,n):
                W [i][j] = random.randint(1,random_limit)
    else:

        n = 5

        W = [   
                [0,3,inf,11,inf],
                [3,0,12,6,9],
                [inf,12,0,4,4],
                [11,6,4,0,2],
                [inf,9,4,2,0]
            ]
    
    if options.verbose:
        print "W = \n", np.squeeze(np.asarray(W))

    F_list = get_edge_list(W)

    if options.verbose:
        print "edge list = ", F_list
        print "edge list length = ", len(get_edge_list(W))

    m = len(get_edge_list(W))

    if options.clock: 
        clock_start = time.clock()

    # ======================================================

    K_list = kruskal(n, m, F_list)

    # ======================================================

    if options.clock: 
        clock_stop = time.clock()

    K_mat = edge_list_to_adj_matrix(K_list)

    if options.verbose:
        print "edge list = ", F_list
        print "K_mat = \n", np.squeeze(np.asarray(K_mat))

    # mirror about diagonal
    for i in range(0, n):
        for j in range (0, n):
            K_mat[j][i] = K_mat[i][j]

    print "Result"
    print "============="
    print "MST matrix = "
    print np.squeeze(np.asarray(K_mat))
    print "Edge list Length = ", get_dist_upper_triange(K_mat)

    if options.verbose:
        print "K_list = ", K_list
        print "K_mat = \n", np.squeeze(np.asarray(K_mat))

    if options.clock:
        total_clock = clock_stop - clock_start
        print "total_time = ", total_clock, " seconds"
    
    # F_list, F_mat = kruskal(n)
    if options.file and options.clock:

        file_data = open("data_kruskals.txt", 'r+')

        # sort the file
        file_list = list(file_data)
        file_data.close()
        file_data = open("data_kruskals.txt", 'w')
        file_n_val = []
        file_time_val = []
        split_line = []
        file_tuples = []

        print "file_list = ",file_list
        for i in range (0, len(file_list)):
            split_line = file_list[i].split(' ')
            file_n_val.append(split_line[0])
            file_time_val.append(split_line[1].split('\n')[0])
            file_tuples.append( (split_line[0], split_line[1].split('\n')[0] ))
        
        file_tuples.append( (str(n),total_clock))

        file_tuples = uniqueify_dble_tup(file_tuples)

        print "[unsort] file_tuples = ", file_tuples

        file_tuples.sort(key=lambda tup: int(tup[0]))

        print "[sort] file_tuples = ", file_tuples

        # write out
        for i in range (0, len(file_tuples)):
            theLine = str(file_tuples[i][0]) + ' ' +  str(file_tuples[i][1]) + '\n' 
            print "writing line : ", theLine 
            file_data.write(theLine)

        print "file_n_val = ", file_n_val
        print "file_time_val = ", file_time_val
        print "file_tuples = ", file_tuples

        file_data.close()
        # theLine = str(n)+ " " + str(total_clock) + "\n"
        # file_data.write( theLine )
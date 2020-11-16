############################################################
#
##### QUERY_UTILS.py
#
### PURPOSE:    Fast Multiplication algorithm is based off of
#   queries into the node matrix and suffix tree. To improve
#   the performance (space and time complexities), we store
#   the node matrix and suffix tree as a Breadth First
#   Multiplication Tree and a Compressed Sparse Column.
#
#   This file converts queries into the node matrix and
#   suffix tree into queries into the BFMT and CSC.
#
### INPUTS:     BFMT and CSC
### OUTPUTS:    Info in Node Matrix and Suffix Tree
#
############################################################

# IDEA:   Reconstruct the entire node matrix from the CSC.
# INPUT:  (list[int])   V       - shape: (num_nonzero_values)
#         (list[int])   ROW     - shape: (num_nonzero_values)
#         (list[int])   COL     - shape: (num_cols)
#         (int, int)    size    - (num_docs, num_cols)
# OUTPUT: (list[list[int]]) mat
def get_node_matrix(V, ROW, COL, n, size):

    num_docs = size[0]
    num_cols = size[1]

    # IDEA:   Reconstruct a specific column.
    # INPUT:  (int)         col_idx - index in node matrix
    # OUTPUT: (list[int])   col     - reconstructed column
    def get_node_matrix_col(col_idx):
        idx_start = COL[col_idx]
        idx_end = COL[col_idx + 1] if col_idx + 1 < num_cols else n
        t_data = [0]*num_docs
        for i in range(idx_start, idx_end):
            t_data[ROW[i]] = V[i]
        return t_data

    node_matrix = [[None]*num_cols for _ in range(num_docs)]

    for col_idx in range(num_cols):
        t_data = get_node_matrix_col(col_idx)
        for row in range(num_docs):
            node_matrix[row][col_idx] = t_data[row]

    return node_matrix

# IDEA:   We want to get the children of a specific node in
#         the suffix tree.
# INPUT:  (Node)        root
#         (str)         prefix - branching node substring
# OUTPUT: (list[int])   col - reconstructed column
def get_children(root, prefix):
    # WARNING:  this is pseudocode
    # TODO:     change based on tree data structure
    prev_root = root
    while prefix:
        for out_edge in root.out_edges:
            prev_root = root
            if prefix.startswith(out_edge.text):
                root = out_edge.end                     # out_edge = (start, end)
                prefix = prefix[len(out_edge.text):]
                break
        if prev_root is root:
            raise "Invalid prefix in get_children()"
    return root.out_edges

################################################################################

V   = [10, 20, 30, 50, 40, 60, 70, 80]
ROW = [0, 0, 1, 2, 1, 2, 2, 3]
COL = [0, 1, 3, 4, 6, 7]
n   = len(V)
num_docs = 4

get_node_matrix(V, ROW, COL, n, (num_docs, len(COL)))

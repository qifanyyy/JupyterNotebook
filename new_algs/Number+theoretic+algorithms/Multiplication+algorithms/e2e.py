from BFMT import get_BFMT #script we wrote
import numpy as np
from random import randint
from scipy.sparse import dok_matrix
from datetime import datetime #for benchmarking

# 
def isLeaf(node):
    """
    Helper function for checking if the node is a leaf.
    @param: node is an object of class suffix_tree.node
    @return: true if node is a leaf, false otherwise 
    """
    return str(type(node)) == "<class 'suffix_tree.node.Leaf'>"


def run_e2e(N_DOCS):
    """
    And end-to-end functions that performs matrix multiplication in linear time.
    @param: N_DOCS is an integer that represents the number of documents to pull from the tweets (our corpus).
    You will have to extract the Twitter zip file.
    @return: void
    """

    RANDOM_LIMIT = 10000

    # Builds the tree (technically not a BFMT yet)
    tree, docs = get_BFMT(n_docs=N_DOCS)

    # Set up a dictionary that will store unique identifiers for each node.
    # Specifically, here we have a mapping from [node: int]
    last_uid = 0
    node_uids = dict()

    # Breadth First Search to populate the layers of the tree.
    q = []
    curr_depth = -1
    layers = []
    q.append((tree.root, 0)) #tuple (root node, level 0)
    while (len(q) > 0):
        node, depth = q.pop()
        node_uids[node] = last_uid #map the node to an integer that is its uid
        last_uid += 1 #increment last_uid to maintain uniqueness
        if depth != curr_depth: # new layer
            layers.append([])
            curr_depth = depth
        layers[-1].append(node)
        if not isLeaf(node):
            for value, child in node.children.items():
                q.append((child, depth + 1))

    # At this point we have all of the uids for the nodes, and we have the 
    # node in a BFF.

    # Generate Phi. Inspired by German, rather than doing top down, we
    # build bottom up.
    phi = dok_matrix((N_DOCS, len(node_uids)), dtype=np.int32)
    for i in range(len(layers) - 1, -1, -1):
        layer = layers[i]
        for node in layer:
            if isLeaf(node):
                # Leaf node case, encode the standard basis vector by only storing a 1 
                # 
                phi[int(node.str_id), node_uids[node]] = 1
    phi = phi.tocsr()

    N_TRIALS = 20
    total_size = 0
    total_time = 0
    for _ in range(N_TRIALS):
        # Generate Beta
        w = [randint(0, RANDOM_LIMIT) for i in range(len(node_uids))]
        beta = []
        beta.append(0)
        for i in range(1, len(w)):
            beta.append(w[i] + beta[i - 1])

        beta = np.array(beta)

        start = datetime.now()
        phi.multiply(beta)
        end = datetime.now()
        total_len = 0
        for doc in docs:
            total_len += len(doc)
        total_size += total_len
        total_time += (end - start).microseconds
    return total_size / N_TRIALS, total_time / N_TRIALS

print('corpus size', 'time')
for i in range(0, 10000, 100):
    N_TRIALS = 10
    corpus_len, microsecs = run_e2e(i)
    print(str(corpus_len) + ',' + str(microsecs))
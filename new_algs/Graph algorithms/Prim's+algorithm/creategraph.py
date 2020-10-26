import argparse
import numpy as np
import pandas as pd


def create_random_walk(nodes: int, edges: int, max_weight: int) -> pd.DataFrame:
    # inspiration:
    # https://stackoverflow.com/questions/2041517/random-simple-connected-graph-generation-with-given-sparseness
    if edges < nodes:
        raise ValueError('edges number should be higher then nodes number')

    matrix = np.zeros((nodes, nodes))

    # necessary weights - random walk
    permuted = np.random.permutation(np.arange(nodes)).repeat(2)
    necessary = np.hstack((permuted[1:], permuted[:1])).reshape((nodes, 2))
    matrix[tuple(necessary.T)[::-1]] = 1
    matrix[tuple(necessary.T)] = 1

    # additional edges
    all_left = np.array(np.where(np.tri(nodes, k=-1, dtype=np.int) & (matrix == 0)))
    random_edges = np.random.permutation(all_left.T)[:edges-nodes]

    # matrix transformation to neighbours list
    neighbours = pd.DataFrame(np.vstack((necessary, random_edges)))
    edges_nmb = neighbours.shape[0]
    neighbours = neighbours.rename(columns={0: f'nodes-{nodes}', 1: f'edges-{edges_nmb}'})
    neighbours['weights'] = np.random.randint(1, max_weight, (edges_nmb,))
    return neighbours


def main():

    # Example usage: python src/python/creategraph.py 30 40 20

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('nodes', type=int,
                        help='number of nodes to generate')
    parser.add_argument('edges', type=int,
                        help='number of edges')
    parser.add_argument('weight', type=int,
                        help='max edge weight')
    parser.add_argument('-o', '--output', type=str,
                        help='output file name(default stdout')
    args = parser.parse_args()

    edges = create_random_walk(args.nodes, args.edges, args.weight)

    csv = edges.to_csv(args.output, index=False)
    if csv is not None:
        print(csv)


if __name__ == '__main__':

    main()

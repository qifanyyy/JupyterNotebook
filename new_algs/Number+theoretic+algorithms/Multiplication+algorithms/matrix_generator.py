import numpy as np
import argparse


def app_arguments():
    args = argparse.ArgumentParser()
    args.add_argument('--n', required=True,
                           type=int,
                           help='Matrix size.')
    args.add_argument('--fpath', required=True,
                      type=str,
                      help='Path to matrix created file.')
    args.add_argument('--max-value', required=False,
                      type=float, default=1000)
    return args.parse_args()


def main(args):
    random_matrix = np.random.random((args.n, args.n)) * args.max_value
    random_matrix[np.triu_indices(args.n, 1)] = 0
    np.savetxt(args.fpath, random_matrix)


if __name__ == "__main__":
    main(app_arguments())

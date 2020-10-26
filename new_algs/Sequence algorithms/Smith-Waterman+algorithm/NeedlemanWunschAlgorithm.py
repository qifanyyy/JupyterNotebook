import numpy as np


class NeedlemanWunschAlgorithm:
    def __init__(self, scoring_sys) -> None:
        self.aligned_seq_a: str = ''
        self.aligned_seq_b: str = ''
        self.scoring_sys = scoring_sys
    
    def align(self, seq_a: str, seq_b: str):
        self.execute(seq_a, seq_b)
        # print(self.aligned_seq_a)
        # print(self.aligned_seq_b)

    def execute(self, seq_a: str, seq_b: str):
        # 1. Prepare dimensions (required additional 1 column and 1 row)
        rows, cols = len(seq_a) + 1, len(seq_b) + 1

        # 2. Initialize matrices
        # Use grid/matrix as graph-like acyclic digraph (array cells are vertices)
        H = np.zeros(shape=(rows, cols), dtype=int)
        score_func = self.scoring_sys.score

        # 3. 1st row and column need to have negative values
        # Top row and leftmost column, are like: 0, -1*d, -2*d, -3*d, etc.
        # d is gap penalty
        d = self.scoring_sys.gap
        H[0, :] = np.arange(start=0, stop=d * cols, step=d)
        H[:, 0] = np.arange(start=0, stop=d * rows, step=d)

        for row in range(1, rows):
            for col in range(1, cols):
                # Current pair of letters from sequence A and B
                a = seq_a[row - 1]
                b = seq_b[col - 1]

                leave_or_replace_letter = H[row - 1, col - 1] + score_func(a, b)
                delete_indel = H[row - 1, col] +  score_func('-', b)
                insert_indel = H[row, col - 1] + score_func(a, '-')

                scores = [leave_or_replace_letter, delete_indel, insert_indel]
                best_action = np.argmax(scores)

                H[row, col] = scores[best_action]
        return H
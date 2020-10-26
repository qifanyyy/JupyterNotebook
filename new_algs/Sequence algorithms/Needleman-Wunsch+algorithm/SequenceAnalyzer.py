import numpy as np
from typing import Tuple, Dict, Any
from ScoringSystem import ScoringSystem
from copy import copy
'''
Authors:
- Michal Martyniak (github: @micmarty)
- Artur Śliwa (@asliwa)

Helpful resources:
- https://en.wikipedia.org/wiki/Needleman–Wunsch_algorithm
- https://en.wikipedia.org/wiki/Smith–Waterman_algorithm
- https://www.cs.cmu.edu/~ckingsf/bioinfo-lectures/local.pdf

Algorithms: Needleman-Wunch, Smith-Waterman (dynamic programming technique)
- Time complexity: O(nm)
- Space complexity: O(nm)
'''


class SequencesAnalyzer:

    # Useful for visualization
    traceback_symbols = {
        0: '↖',
        1: '↑',
        2: '←',
        3: '•'
    }

    def __init__(self, seq_a: str, seq_b: str, load_csv: bool = False) -> None:
        self.seq_a = seq_a
        self.seq_b = seq_b

        self.scoring_sys = ScoringSystem(match=2, mismatch=-1, gap=-2)
        self.edit_cost_sys = ScoringSystem(match=0, mismatch=1, gap=1)

        if load_csv:
            self.scoring_sys.load_csv('scores.csv')
            self.edit_cost_sys.load_csv('edit_cost.csv')

            # Show what's inside the files
            print('[Scoring system]\n', self.scoring_sys)
            print('[Edit cost system]\n', self.edit_cost_sys)

    def global_alignment(self) -> Tuple[str, str]:
        result: Dict[str, Any] = self.needleman_wunsch_algorithm(
            minimize=False, alignment_cal=True)
        # result: Dict[str, Any] = self.NWScore(seq_a=self.seq_a, seq_b=self.seq_b)
        alignment_a, alignment_b = self._traceback(
            result_matrix=result['result_matrix'],
            traceback_matrix=result['traceback_matrix'],
            start_pos=result['score_pos'],
            global_alignment=True)

        print(
            f"[Global Alignment] Score={result['score']}\n"
            f"Result:\n {result['result_matrix']}\n"
            f"Traceback:\n {result['traceback_matrix']}\n"
            f"Alignment:\n {alignment_a}\n {alignment_b}\n"
        )

        return alignment_a, alignment_b

    def local_alignment(self) -> Tuple[str, str]:
        result: Dict[str, Any] = self.smith_waterman_algorithm()
        alignment_a, alignment_b = self._traceback(
            result_matrix=result['result_matrix'],
            traceback_matrix=result['traceback_matrix'],
            start_pos=result['score_pos'],
            global_alignment=False)

        print(
            f"[Local Alignment] Score={result['score']}\n"
            f"Result:\n {result['result_matrix']}\n"
            f"Traceback:\n {result['traceback_matrix']}\n"
            f"Alignment:\n {alignment_a}\n {alignment_b}\n"
        )
        return alignment_a, alignment_b

    def similarity(self) -> int:
        result = self.needleman_wunsch_algorithm(minimize=False)

        print(
            f"[Similarity] Score={result['score']}\n"
            f"{result['result_matrix']}\n"
            f"{result['traceback_matrix']}\n"
        )
        return result['score']

    def edit_distance(self) -> int:
        result = self.needleman_wunsch_algorithm(minimize=True)

        print(
            f"[Edit distance] Cost={result['score']}\n"
            f"{result['result_matrix']}\n"
            f"{result['traceback_matrix']}\n"
        )
        return result['score']

    def needleman_wunsch_algorithm(self, minimize: bool = False, alignment_cal: bool = False) -> Dict[str, Any]:
        '''
        `minimize` - set to True when calculating edit distance
        `alignment_cal` - set to True when calculating global alignment
        '''
        # 1. Prepare dimensions (required additional 1 column and 1 row)
        rows, cols = len(self.seq_a) + 1, len(self.seq_b) + 1

        # 2. Initialize matrices
        # Use grid/matrix as graph-like acyclic digraph (array cells are vertices)
        H = np.zeros(shape=(rows, cols), dtype=int)
        traceback = np.zeros(shape=(rows, cols), dtype=np.dtype('U5'))

        # 3. msadkjnsadkjn;sdf
        gapH = np.zeros(shape=(rows, cols), dtype=int)

        if minimize:
            # Edit cost calculation
            score_func = self.edit_cost_sys.score
        else:
            # Similarity calculation
            score_func = self.scoring_sys.score

        if alignment_cal:
            # Global alignment calculation -> 1st row and column need to have negative values
            sign = self.scoring_sys.gap
        else:
            # Similarity or edit cost calculation -> 1st first row and column values need to be positive
            sign = 1

        # Put sequences' letters into 1st row and 1st column (for better visualization)
        traceback[0, 1:] = np.array(list(self.seq_b), dtype=str)
        traceback[1:, 0] = np.array(list(self.seq_a), dtype=str)
    
        # 3. Top row and leftmost column, like: 0, 1, 2, 3, etc.
        H[0, :] = np.arange(start=0, stop=sign*cols, step=sign)
        H[:, 0] = np.arange(start=0, stop=sign*rows, step=sign)

        for row in range(1, rows):
            for col in range(1, cols):
                # Current pair of letters from sequence A and B
                a = self.seq_a[row - 1]
                b = self.seq_b[col - 1]

                leave_or_replace_letter = H[row -
                    1, col - 1] + score_func(a, b)

                if gapH[row - 1, col] == 0:
                    score = score_func('-', b)
                else:
                    score = 0
                delete_indel = H[row - 1, col] + score

                if gapH[row, col - 1] == 0:
                    score = score_func(a, '-')
                else:
                    score = 0
                insert_indel = H[row, col - 1] + score

                scores = [leave_or_replace_letter, delete_indel, insert_indel]

                if minimize:
                    best_action = np.argmin(scores)
                else:
                    best_action = np.argmax(scores)
                    if best_action in [1, 2]:
                        gapH[row, col] = True

                H[row, col] = scores[best_action]
                traceback[row, col] = self.traceback_symbols[best_action]

        print(gapH)
        return {
            'result_matrix': H,
            'traceback_matrix': traceback,
            'score': H[-1, -1],                 # Always right-bottom corner
            'score_pos': (rows - 1, cols - 1)   # as above...
        }

    # def NWScore(self, seq_a, seq_b):
    #     # 1. Prepare dimensions (required additional 1 column and 1 row)
    #     rows, cols = len(seq_a) + 1, len(seq_b) + 1

    #     # 2. Initialize matrices
    #     # Use grid/matrix as graph-like acyclic digraph (array cells are vertices)
    #     H = np.zeros(shape=(rows, cols), dtype=int)
    #     traceback = np.zeros(shape=(rows, cols), dtype=np.dtype('U5'))

    #     # Similarity calculation
    #     score_func = self.scoring_sys.score

    #     # Global alignment calculation -> 1st row and column need to have negative values
    #     sign = self.scoring_sys.gap

    #     # Put sequences' letters into 1st row and 1st column (for better visualization)
    #     traceback[0, 1:] = np.array(list(seq_b), dtype=str)
    #     traceback[1:, 0] = np.array(list(seq_a), dtype=str)
    
    #     # 3. Top row and leftmost column, like: 0, 1, 2, 3, etc.
    #     H[0, :] = np.arange(start=0, stop=sign*cols, step=sign)
    #     H[:, 0] = np.arange(start=0, stop=sign*rows, step=sign)

    #     for row in range(1, rows):
    #         for col in range(1, cols):
    #             # Current pair of letters from sequence A and B
    #             a = seq_a[row - 1]
    #             b = seq_b[col - 1]

    #             leave_or_replace_letter = H[row - 1, col - 1] + score_func(a, b)
    #             delete_indel = H[row - 1, col] +  score_func('-', b)
    #             insert_indel = H[row, col - 1] + score_func(a, '-')

    #             scores = [leave_or_replace_letter, delete_indel, insert_indel]
    #             best_action = np.argmax(scores)

    #             H[row, col] = scores[best_action]
    #             traceback[row, col] = self.traceback_symbols[best_action]
    #     return H[-1, :]
    #     # return {
    #     #     'result_matrix': H,
    #     #     'traceback_matrix': traceback,
    #     #     'score': H[-1, -1],                 # Always right-bottom corner
    #     #     'score_pos': (rows - 1, cols - 1)   # as above...
    #     # }

    # def hirschberg_global_alignment(self):
    #     pass

    def smith_waterman_algorithm(self) -> Dict[str, Any]:
        '''
        Note: Smith-Waterman and Needleman-Wunsch algorithms
        are very similar, but because there are small differences,
        they are meant to be separated.
        '''
        # 1. Prepare dimensions (required additional 1 column and 1 row)
        rows, cols = len(self.seq_a) + 1, len(self.seq_b) + 1

        # 2. Initialize matrices
        # Use grid/matrix as graph-like acyclic digraph (array cells are vertices)
        H = np.zeros(shape=(rows, cols), dtype=int)
        traceback = np.zeros(shape=(rows, cols), dtype=np.dtype('U5'))

        # Difference 1: 1st row and 1st column are already zeroed

        # Put sequences' letters into first row and first column (better visualization)
        traceback[0, 1:] = np.array(list(self.seq_b), dtype=str)
        traceback[1:, 0] = np.array(list(self.seq_a), dtype=str)

        # 3. Top row and leftmost colum are already 0
        for row in range(1, rows):
            for col in range(1, cols):
                # Alias: current pair of letters
                a = self.seq_a[row - 1]
                b = self.seq_b[col - 1]

                score_func = self.scoring_sys.score
                leave_or_replace_letter = H[row -
                    1, col - 1] + score_func(a, b)
                delete_indel = H[row - 1, col] + score_func('-', b)
                insert_indel = H[row, col - 1] + score_func(a, '-')

                # Difference 2: That additional 0 is required (ignore negative values)
                scores = [leave_or_replace_letter,
                    delete_indel, insert_indel, 0]
                best_action = np.argmax(scores)

                H[row, col] = scores[best_action]
                traceback[row, col] = self.traceback_symbols[best_action]

        return {
            'result_matrix': H,
            'traceback_matrix': traceback,
            'score': H.max(),
            # Force numpy to return last result
            # Source: (Step 2: Backtracing) https://tiefenauer.github.io/blog/smith-waterman
            'score_pos': np.unravel_index(np.argmax(H, axis=None), H.shape)
        }

    # def hirschberg_algorithm(self, X, Y):
    #     '''
    #     Hirschberg’s algorithm uses Θ(m +n) space.

    #     - Each recursive call uses Θ(m) space to compute f (·, n / 2) and g(·, n / 2).
    #     - Only Θ(1) space needs to be maintained per recursive call.
    #     - Number of recursive calls ≤ n. ▪
    #     '''
    #     Z = ''
    #     W = ''
    #     Q = ''
    #     E = ''
    #     aligned_X = ''
    #     aligned_Y = ''

    #     if len(X) == 0:
    #         for i in range(0, len(Y)):
    #             Z += '-'
    #             W += Y[i]
    #         print(f'{Z}->{W}')
    #     elif len(Y) == 0:
    #         for i in range(0, len(X)):
    #             Z += X[i] 
    #             W += '-'
    #         print(f'{Z}->{W}')
    #     elif len(X) == 1 or len(Y) == 1:
    #         # Z, W = self.NWScore(seq_a=self.seq_a.copy(), seq_b=self.seq_b.copy())
    #         print(f'{X}->{Y}')
    #     else:
    #         x_len = len(X)
    #         x_mid = int(len(X) // 2)
    #         y_len = len(Y)

    #         score_left = self.NWScore(seq_a=X[0:x_mid], seq_b=Y)
    #         rev_a = X[x_mid:x_len]
    #         score_right = self.NWScore(seq_a=rev_a[::-1], seq_b=Y[::-1])
    #         y_mid = np.argmax(score_left + np.flip(score_right))
    #         Z, W = self.hirschberg_algorithm(X=X[0:x_mid], Y=Y[0:y_mid])
    #         Q, E = self.hirschberg_algorithm(X=X[x_mid:x_len], Y=Y[y_mid:y_len])
    #     return Z+Q, W+E

    def _traceback(self, result_matrix, traceback_matrix, start_pos: Tuple[int, int], global_alignment: bool) -> Tuple[str, str]:
        seq_a_aligned = ''
        seq_b_aligned = ''

        # 1. Select starting point
        row, col = start_pos

        if global_alignment:
            # Terminate when top left corner (0,0) is reached (end of path)
            end_condition_reached = lambda row, col: row == 0 and col == 0
        else:
            # Terminate when 0 is reached
            end_condition_reached = lambda row, col: result_matrix[row, col] == 0

        while not end_condition_reached(row, col):
            symbol = traceback_matrix[row, col]
            if row == 0:
                symbol = '←'
            if col == 0:
                symbol = '↑'
            # Use arrows to navigate and collect letters (in reversed order)
            # Shift/reverse indexes by one beforehand (we want to get the letter that arrow points to)
            if symbol == '↖':
                row -= 1
                col -= 1
                letter_a, letter_b = self.seq_a[row], self.seq_b[col]
            elif symbol == '↑':
                row -= 1
                letter_a, letter_b = self.seq_a[row], '-'
            elif symbol == '←':
                col -= 1
                letter_a, letter_b = '-', self.seq_b[col]

            # Acumulate letter (in reversed order)
            seq_a_aligned += letter_a
            seq_b_aligned += letter_b

        # Reverse strings (traceback goes from bottom-right to top-left)
        return seq_a_aligned[::-1], seq_b_aligned[::-1]

    # def _traceback_local(self, result_matrix, traceback_matrix, start_pos: Tuple[int, int]) -> Tuple[str, str]:
    #     '''Use both matrices to replay the optimal route'''
    #     seq_a_aligned = ''
    #     seq_b_aligned = ''

    #     # 1. Select starting point
    #     position = list(start_pos)

    #     # 2. Terminate when 0 is reached (end of path)
    #     while result_matrix[position[0], position[1]] != 0:
    #         symbol = traceback_matrix[position[0], position[1]]

            

    #         letter_pair = self.translateArrow(symbol, position)
    #         seq_a_aligned += letter_pair[0]
    #         seq_b_aligned += letter_pair[1]
    #     # Reverse strings (traceback goes from bottom-right to top-left)
    #     return seq_a_aligned[::-1], seq_b_aligned[::-1]

    # def _traceback_global(self, traceback_matrix, start_pos: Tuple[int, int]) -> Tuple[str, str]:
    #     seq_a_aligned = ''
    #     seq_b_aligned = ''

    #     # 1. Select starting point
    #     row, col = start_pos

    #     # 2. Terminate when top left corner (0,0) is reached (end of path)
    #     while not (row == 0 and col == 0):
    #         symbol = traceback_matrix[row, col]
    #         letter_a, letter_b = self._translate_arrow(symbol, pos=(row, col))
    #         seq_a_aligned += letter_a
    #         seq_b_aligned += letter_b
    #     # Reverse strings (traceback goes from bottom-right to top-left)
    #     return seq_a_aligned[::-1], seq_b_aligned[::-1]

    # def _translate_arrow(self, symbol: str, pos: Tuple[int, int]) -> Tuple[str, str]:
    #     '''
        
    #     '''
    #     row, col = pos
    #     if symbol == '↖':
    #         row -= 1
    #         col -= 1
    #         return self.seq_a[row], self.seq_b[col]
    #     elif symbol == '↑':
    #         row -= 1
    #         return self.seq_a[row], '-'
    #     elif symbol == '←':
    #         col -= 1
    #         return '-', self.seq_b[col]



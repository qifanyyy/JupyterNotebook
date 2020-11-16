import numpy as np
from typing import Tuple
from NeedlemanWunschAlgorithm import NeedlemanWunschAlgorithm
from ScoringSystem import ScoringSystem

class HirschbergAlgorithm:
    '''
    Hirschberg’s algorithm uses Θ(m +n) space.
    - Each recursive call uses Θ(m) space to compute f(·, n / 2) and g(·, n / 2).
    - Only Θ(1) space needs to be maintained per recursive call.
    - Number of recursive calls ≤ n. ▪
    s
    Pseudocode: https://en.wikipedia.org/wiki/Hirschberg's_algorithm
    '''
    def __init__(self, scoring_sys) -> None:
        self.aligned_seq_a: str = ''
        self.aligned_seq_b: str = ''
        self.scoring_sys = scoring_sys

    def align(self, seq_a: str, seq_b: str) -> Tuple[str, str]:
        self.excute(seq_a, seq_b)
        print(self.aligned_seq_a)
        print(self.aligned_seq_b)
        
    def append_alignment(self, Z: str, W: str):
        print(f'{Z} -> {W}')
        self.aligned_seq_a += Z
        self.aligned_seq_b += W

    def excute(self, seq_a: str, seq_b: str) -> Tuple[str, str]:
        Z, W = '', ''

        if len(seq_a) == 0:
            for b in seq_b:
                Z, W = Z + '-', W + b
            self.append_alignment(Z, W)
        elif len(seq_b) == 0:
            for a in seq_a:
                Z, W = Z + a, W + '-'
            self.append_alignment(Z, W)
        elif len(seq_a) == 1 or len(seq_b) == 1:
            # Z, W = self.NWScore(seq_a=self.seq_a.copy(), seq_b=self.seq_b.copy())

            # If sequences have different length, fill missing spots with '-'
            if len(seq_a) > 1:
                seq_b = seq_b.ljust(len(seq_a), '-')
            elif len(seq_b) > 1:
                seq_a = seq_a.ljust(len(seq_b), '-')
            self.append_alignment(seq_a, seq_b)
        else:
            # Calculate left score
            a_mid: int = int(len(seq_a) // 2)
            result = NeedlemanWunschAlgorithm(self.scoring_sys).execute(seq_a[:a_mid], seq_b)
            score_left: np.ndarray[int] = result[-1, :]
            
            # Calculate right score
            rev_seq_a: str = seq_a[a_mid:][::-1]
            rev_seq_b: str = seq_b[::-1]
            result = NeedlemanWunschAlgorithm(self.scoring_sys).execute(rev_seq_a, rev_seq_b)
            score_right: np.ndarray[int] = result[-1, :]

            # Find seq_b division index
            rev_score_right: np.ndarray[int] = np.flip(score_right)
            b_mid: int = np.argmax(score_left + rev_score_right)

            # Left subtree traversal
            left_z, left_w = self.excute(
                seq_a=seq_a[:a_mid],
                seq_b=seq_b[:b_mid]
            )

            # Right subtree traversal
            right_z, right_w = self.excute(
                seq_a=seq_a[a_mid:], 
                seq_b=seq_b[b_mid:]
            )
            Z, W = left_z + right_z, left_w + right_w
        return Z, W

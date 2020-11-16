from Node import *


class Unrestricted:

    def __init__(self):
        self.indel = 5  # Insertion / Deletion cost
        self.sub = 1  # Substitution cost
        self.match = -3  # Match cost

    def edit_distance(self, seq1, seq2, m, n):
        # Initialize 2D array m + 1 by n + 1
        self.memo = [[Node() for i in range(n + 1)] for j in range(m + 1)]

        for i in range(m + 1):
            for j in range(n + 1):
                # i = 0 indicates a gap/an empty first sequence. All characters from the second sequence are inserted
                if i == 0 and j == 0:
                    self.memo[i][j].edit_dist = j * self.indel
                elif i == 0:
                    self.memo[i][j].edit_dist = j * self.indel
                    # Assign the previous pointer
                    self.memo[i][j].prev_i = i                      # Insertion
                    self.memo[i][j].prev_j = j - 1
                # j = 0 indicates a gap/an empty second sequence. All characters from the first sequence are inserted
                elif j == 0:
                    self.memo[i][j].edit_dist = i * self.indel
                    # Assign the previous pointer
                    self.memo[i][j].prev_i = i - 1                  # Deletion
                    self.memo[i][j].prev_j = j
                # If the current character in each sequence match
                elif seq1[i - 1] == seq2[j - 1]:
                    self.memo[i][j].edit_dist = self.memo[i - 1][j - 1].edit_dist + self.match
                    # Assign the previous pointer
                    self.memo[i][j].prev_i = i - 1                  # Match
                    self.memo[i][j].prev_j = j - 1
                # If the current character in each sequence are different, find the minimum
                else:
                    self.memo[i][j].edit_dist = min(self.memo[i][j - 1].edit_dist + self.indel,     # Insertion
                                                    self.memo[i - 1][j].edit_dist + self.indel,     # Deletion
                                                    self.memo[i - 1][j - 1].edit_dist + self.sub)   # Substitution

                    # Assign the previous pointer
                    if self.memo[i][j].edit_dist == self.memo[i][j - 1].edit_dist + self.indel:     # Insertion
                        self.memo[i][j].prev_i = i
                        self.memo[i][j].prev_j = j - 1
                    elif self.memo[i][j].edit_dist == self.memo[i - 1][j].edit_dist + self.indel:   # Deletion
                        self.memo[i][j].prev_i = i - 1
                        self.memo[i][j].prev_j = j
                    elif self.memo[i][j].edit_dist == self.memo[i - 1][j - 1].edit_dist + self.sub:  # Substitution
                        self.memo[i][j].prev_i = i - 1
                        self.memo[i][j].prev_j = j - 1

        alignment1 = []
        alignment2 = []
        i = m
        j = n
        while i != float("inf") or j != float("inf"):
            # If the previous node is the diagonal node (match or substitution) insert the character into each alignment
            if self.memo[i][j].prev_i == i - 1 and self.memo[i][j].prev_j == j - 1:
                alignment1.insert(0, seq1[i-1])
                alignment2.insert(0, seq2[j-1])
            # If the previous node is the left node (insertion) insert a gap into alignment 1
            elif self.memo[i][j].prev_i == i and self.memo[i][j].prev_j == j - 1:
                alignment1.insert(0, '-')
                alignment2.insert(0, seq2[j-1])
            # If the previous node is the top node (deletion) insert a gap into alignment 2
            elif self.memo[i][j].prev_i == i - 1 and self.memo[i][j].prev_j == j:
                alignment1.insert(0, seq1[i-1])
                alignment2.insert(0, '-')
            i, j = self.memo[i][j].prev_i, self.memo[i][j].prev_j
        return self.memo[m][n].edit_dist, "".join(alignment1), "".join(alignment2)

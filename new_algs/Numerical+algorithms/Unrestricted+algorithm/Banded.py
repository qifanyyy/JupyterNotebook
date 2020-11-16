from Node import *


class Banded:

    def __init__(self):
        self.indel = 5          # Insertion / Deletion cost
        self.sub = 1            # Substitution cost
        self.match = -3         # Match cost
        self.memo = []          # 2D array

    def edit_distance(self, seq1, seq2, m, n, d):
        self.bandwidth = 2 * d + 1
        # Lengths of the smaller and bigger sequences
        smaller_seq = 0
        bigger_seq = 0
        # The position of i when the last position of bigger sequence has been reached
        end_i = 0
        # Initialize 2D array n + 1 by k (bandwidth), smaller sequence by bigger sequence
        # When the length of sequence 1 is smaller than sequence 2, create an m + 1 by k array
        if m < n:
            self.memo = [[Node() for i in range(self.bandwidth)] for j in range(m+1)]
            smaller_seq = m
            bigger_seq = n
            end_i = d - 1
        # When the length of sequence 2 is smaller than sequence 1, create an n + 1 by k array
        elif n < m:
            self.memo = [[Node() for i in range(self.bandwidth)] for j in range(n+1)]
            smaller_seq = n
            bigger_seq = m
        # When the length of sequence 1 equals than sequence 2, create an m + 1 by k array
        elif m == n:
            self.memo = [[Node() for i in range(self.bandwidth)] for j in range(m+1)]
            smaller_seq = m
            bigger_seq = n
            end_i = d

        # Stopping point for jth term that is incremented before i is incremented
        stop_j = d + 1
        # Front Section: Calculates the edit distance similarly to unrestricted
        for i in range(0, d + 1):
            for j in range(0, stop_j):
                self.calculate_edit_distance(seq1, seq2, i, j, j)
            stop_j += 1

        # Variable that keeps track of the bigger sequence's current character
        start_bigger_seq = 1
        # Middle Section: Calculates a version of edit distance because of restricting jth term to the bandwidth size
        for i in range(d + 1, smaller_seq - end_i + 1):
            for j in range(self.bandwidth):
                self.calculate_mid_edit_distance(seq1, seq2, i, j, start_bigger_seq+j)
            start_bigger_seq += 1

        # Starting point for jth term that is incremented before i is incremented
        start_j = 1
        # Decrement the variable because the jth term account for the incremental change
        start_bigger_seq -= 1
        # Back Section: Calculates the edit distance similarly to unrestricted
        for i in range(smaller_seq - end_i + 1, smaller_seq + 1):
            for j in range(start_j, self.bandwidth):
                self.calculate_edit_distance(seq1, seq2, i, j, start_bigger_seq + j)
            start_j += 1

        alignment1 = []
        alignment2 = []
        # The nth term in the n + 1 by k array
        i = smaller_seq
        # Variable that keeps track of the bigger sequence's current character
        bigger_seq_j = bigger_seq
        # The kth term in the n + 1 by k array
        j = self.bandwidth - 1
        while i != float("inf") or j != float("inf"):
            # If i is in the front or back section
            if i < d + 1 or i > smaller_seq - end_i:
                # If the previous node is the diagonal node (match/substitution) insert the char into each alignment
                if self.memo[i][j].prev_i == i - 1 and self.memo[i][j].prev_j == j - 1:     # Substitution / Match
                    alignment1.insert(0, seq1[i - 1])
                    alignment2.insert(0, seq2[bigger_seq_j - 1])
                    bigger_seq_j -= 1
                # If the previous node is the left node (insertion) insert a gap into alignment 1
                elif self.memo[i][j].prev_i == i and self.memo[i][j].prev_j == j - 1:       # Insertion
                    alignment1.insert(0, '-')
                    alignment2.insert(0, seq2[bigger_seq_j - 1])
                    bigger_seq_j -= 1
                # If the previous node is the top node (deletion) insert a gap into alignment 2
                elif self.memo[i][j].prev_i == i - 1 and self.memo[i][j].prev_j == j:       # Deletion
                    alignment1.insert(0, seq1[i - 1])
                    alignment2.insert(0, '-')
                i, j = self.memo[i][j].prev_i, self.memo[i][j].prev_j
            # If i is in the middle section
            else:
                # If the previous node is the diagonal node (match/substitution) insert the char into each alignment
                if self.memo[i][j].prev_i == i - 1 and self.memo[i][j].prev_j == j:         # Substitution / Match
                    alignment1.insert(0, seq1[i - 1])
                    alignment2.insert(0, seq2[bigger_seq_j - 1])
                    bigger_seq_j -= 1
                # If the previous node is the left node (insertion) insert a gap into alignment 1
                elif self.memo[i][j].prev_i == i and self.memo[i][j].prev_j == j - 1:       # Insertion
                    alignment1.insert(0, '-')
                    alignment2.insert(0, seq2[bigger_seq_j - 1])
                    bigger_seq_j -= 1
                # If the previous node is the top node (deletion) insert a gap into alignment 2
                elif self.memo[i][j].prev_i == i - 1 and self.memo[i][j].prev_j == j + 1:   # Deletion
                    alignment1.insert(0, seq1[i - 1])
                    alignment2.insert(0, '-')
                i, j = self.memo[i][j].prev_i, self.memo[i][j].prev_j
        return self.memo[smaller_seq][self.bandwidth-1].edit_dist, "".join(alignment1), "".join(alignment2)

    # Calculates the edit distance for the front and back section similarly to the unrestricted algorithm
    def calculate_edit_distance(self, seq1, seq2, i, j, bigger_seq_j):
        # i = 0 indicates a gap/an empty first sequence. All characters from the second sequence are inserted
        if i == 0 and j == 0:
            self.memo[i][j].edit_dist = j * self.indel
        elif i == 0:
            self.memo[i][j].edit_dist = j * self.indel
            # Assign the previous pointer
            self.memo[i][j].prev_i = i  # Insertion
            self.memo[i][j].prev_j = j - 1
        # j = 0 indicates a gap/an empty second sequence. All characters from the first sequence are inserted
        elif j == 0:
            self.memo[i][j].edit_dist = i * self.indel
            # Assign the previous pointer
            self.memo[i][j].prev_i = i - 1  # Deletion
            self.memo[i][j].prev_j = j
        # If the current character in each sequence match
        elif seq1[i - 1] == seq2[bigger_seq_j - 1]:
            self.memo[i][j].edit_dist = self.memo[i - 1][j - 1].edit_dist + self.match
            # Assign the previous pointer
            self.memo[i][j].prev_i = i - 1  # Match
            self.memo[i][j].prev_j = j - 1
        # If the current character in each sequence are different, find the minimum
        else:
            self.memo[i][j].edit_dist = min(self.memo[i][j - 1].edit_dist + self.indel,  # Insertion
                                            self.memo[i - 1][j].edit_dist + self.indel,  # Deletion
                                            self.memo[i - 1][j - 1].edit_dist + self.sub)  # Substitution

            # Assign the previous pointer
            if self.memo[i][j].edit_dist == self.memo[i][j - 1].edit_dist + self.indel:  # Insertion
                self.memo[i][j].prev_i = i
                self.memo[i][j].prev_j = j - 1
            elif self.memo[i][j].edit_dist == self.memo[i - 1][j].edit_dist + self.indel:  # Deletion
                self.memo[i][j].prev_i = i - 1
                self.memo[i][j].prev_j = j
            elif self.memo[i][j].edit_dist == self.memo[i - 1][j - 1].edit_dist + self.sub:  # Substitution
                self.memo[i][j].prev_i = i - 1
                self.memo[i][j].prev_j = j - 1

    def calculate_mid_edit_distance(self, seq1, seq2, i, j, bigger_seq_j):
        # If the current character in each sequence match
        if seq1[i - 1] == seq2[bigger_seq_j - 1]:
            self.memo[i][j].edit_dist = self.memo[i-1][j].edit_dist + self.match
            # Assign the previous pointer
            self.memo[i][j].prev_i = i - 1
            self.memo[i][j].prev_j = j
        # If the jth term is the first index, find the minimum of deletion and substitution (no insertion)
        elif j == 0:
            self.memo[i][j].edit_dist = min(self.memo[i-1][j+1].edit_dist + self.indel,     # Deletion
                                            self.memo[i-1][j].edit_dist + self.sub)         # Substitution
            # Assign the previous pointer
            if self.memo[i][j].edit_dist == self.memo[i-1][j+1].edit_dist + self.indel:     # Deletion
                self.memo[i][j].prev_i = i - 1
                self.memo[i][j].prev_j = j + 1
            elif self.memo[i][j].edit_dist == self.memo[i-1][j].edit_dist + self.sub:       # Substitution
                self.memo[i][j].prev_i = i - 1
                self.memo[i][j].prev_j = j
        # If the jth term is the last index, find the minimum of substitution and insertion (no deletion)
        elif j == self.bandwidth - 1:
            self.memo[i][j].edit_dist = min(self.memo[i][j-1].edit_dist + self.indel,       # Insertion
                                            self.memo[i-1][j].edit_dist + self.sub)         # Substitution
            # Assign the previous pointer
            if self.memo[i][j].edit_dist == self.memo[i][j-1].edit_dist + self.indel:       # Insertion
                self.memo[i][j].prev_i = i
                self.memo[i][j].prev_j = j - 1
            elif self.memo[i][j].edit_dist == self.memo[i-1][j].edit_dist + self.sub:       # Substitution
                self.memo[i][j].prev_i = i - 1
                self.memo[i][j].prev_j = j
        # If not a special case of the first or last index, find the minimum
        else:
            self.memo[i][j].edit_dist = min(self.memo[i][j-1].edit_dist + self.indel,       # Insertion
                                            self.memo[i-1][j+1].edit_dist + self.indel,     # Deletion
                                            self.memo[i-1][j].edit_dist + self.sub)         # Substitution

            # Assign  the previous pointer
            if self.memo[i][j].edit_dist == self.memo[i][j-1].edit_dist + self.indel:       # Insertion
                self.memo[i][j].prev_i = i
                self.memo[i][j].prev_j = j - 1
            elif self.memo[i][j].edit_dist == self.memo[i-1][j+1].edit_dist + self.indel:   # Deletion
                self.memo[i][j].prev_i = i - 1
                self.memo[i][j].prev_j = j + 1
            elif self.memo[i][j].edit_dist == self.memo[i-1][j].edit_dist + self.sub:       # Substitution
                self.memo[i][j].prev_i = i - 1
                self.memo[i][j].prev_j = j
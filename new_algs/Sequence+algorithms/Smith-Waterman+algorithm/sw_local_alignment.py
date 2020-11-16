from blosum import blosum62
from proteins import proteins
import numpy as np
import time

# Tam Dang
# 10.10.17
# CSE 427 - Computational Biology
# Smith-Waterson Local Sequence Alignment


# For running SW on two specific proteins
# Note that this program will fail for invalid protein sequences
def main():

    prompt1 = input("Calculate Smith-Waterman alignment between two proteins? (y/n): ")

    if prompt1.startswith("y"):
        n1 = input("Enter name of first protein: ")
        p1 = input("Enter first protein's sequence of amino acids: ")
        n2 = input("Enter name of second protein: ")
        p2 = input("Enter second protein's sequence of amino acids: ")

        print("Calculating alignment between", n1, "and", n2, ":\n")
        sw = SmithWatermanAlignment(p1, p2)
        sw.align_sequences()
        sw.print_alignment(n1, n2)
        print("Score:", sw.max_score, "\n")

        show_table = input("Show table? (y/n): ")
        if show_table.startswith("y"):
            print("Smith-Waterman Alignment Table for deadly & ddgearlyk:")
            print("(Horizontal (T) -", n1, " Vertical (S) -", n2, "\n")
            print(sw.alignment_table)


    # Uncomment to reproduce all the results text files.
    #
    # Takes approximately 2 hrs to finish.
    # generate_results()


# Generates results to answer the HW2 questions.
def generate_results():
    print("Hello")

    f1 = open('short_example.txt', 'w')
    f2 = open('protein_alignments.txt', 'w')
    f3 = open('protein_alignment_scores.txt', 'w')
    f4 = open('myod1_lin32_syfm_pvalues.txt', 'w')

    # Short example
    sw = SmithWatermanAlignment("deadly", "ddgearlyk")
    sw.align_sequences()
    print("Calculating deadly & ddgearlyk p-value: \n")
    f1.write("p-value for deadly & ddgearlyk: ")
    f1.write(str(permute_and_score("deadly", "ddgearlyk", 100000)))
    f1.write("\n")
    f1.write("Smith-Waterman Alignment Table for deadly & ddgearlyk:\n")
    f1.write("(Horizontal (T) - ddgearlyk, vertical (S) - deadly) \n\n")
    f1.write(str(sw.alignment_table))
    f1.write("\n\n")
    f1.write("Alignment:\n")
    sw.print_alignment_to_file("DEADLY", "DDGEARLYK", f1)
    f1.write("Score: ")
    f1.write(str(sw.max_score))
    end = time.clock()
    print("TIME:", end)

    ## Protein alignments
    done = []
    alignment_scores = []
    print("Calculating alignments between proteins:")
    count = 0
    for p1, v1 in proteins.items():
        s_chars = list(v1)
        for p2, v2 in proteins.items():
            if (p1 != p2 and p2 not in done):
                t_chars = list(v2)
                sw_p1_p2 = SmithWatermanAlignment(v1, v2)
                sw_p1_p2.align_sequences()
                sw_p1_p2.print_alignment_to_file(p1, p2, f2)

                alignment_scores.append((p1, p2, sw_p1_p2.max_score))
                print("Alignment - ", count)
                count += 1

        done.append(p1)
        print(done)

    print(len(alignment_scores), "total comparisons made!")

    # Printing output of scores to file for 10x10 matrix
    score_format = '{0:6} & {1:6}:  {2}\n'
    for score in alignment_scores:
        entries = [score[0], score[1], score[2]]
        f3.write(score_format.format(*entries))

    ## p-values between P15172 and Q10574
    print("Calculating P15172 & Q10574 p-value:")
    f4.write("p-value for P15172 & Q10574: ")
    f4.write(str(permute_and_score(proteins.get("P15172"), proteins.get("Q10574"), 1000)))
    f4.write("\n\n")
    print("Calculating P15172 & O95363 p-value:")
    f4.write("p-value for P15172 & O95363: ")
    f4.write(str(permute_and_score(proteins.get("P15172"), proteins.get("O95363"), 1000)))
    f4.write("\n\n")


# Calculates the p-value given two sequences, such that
# the S sequence is permuted and checked against the score
# between the two inputs.
#
# Returns a value of the form (k + 1) / (N + 1), where
# k is the number of times a permuted string and S outscored
# S and T
def permute_and_score(s, t, N):
    sw = SmithWatermanAlignment(s, t)
    sw.align_sequences()
    score_s_t = sw.max_score
    k = 0
    for i in range(0, N):
        permuted_s = permute(s)
        sw_on_permuted = SmithWatermanAlignment(s, permuted_s)
        sw_on_permuted.align_sequences()
        if (sw_on_permuted.max_score >= score_s_t):
            k += 1
    return (k + 1) / (N + 1)


# # Returns a random permutation of s,
# # uniformly distributed
def permute(s):
    n = len(s)
    permuted_s = list(s)
    for i in range(n - 1, 0, -1):
        j = np.random.randint(i)
        # Swap
        s1 = permuted_s[i]
        s2 = permuted_s[j]
        permuted_s[i] = s2
        permuted_s[j]= s1
    return ''.join(permuted_s)


class SmithWatermanAlignment:

    # Constructs and returns the alignment table using
    # scores from BLOSUM62 for two protein sequences
    #
    # Returns the table as well as the coordinates of
    # the largest score to begin the backtrace
    def __init__(self, S, T):

        self.s_align = None
        self.t_align = None
        self.full_backtrace = None

        # Insert empty string to serve as empty prefix
        self.s_chars = list(S.upper())
        self.t_chars = list(T.upper())
        self.s_chars.insert(0, '')
        self.t_chars.insert(0, '')

        # In this alignment table, S is along the left hand edge
        self.alignment_table = np.zeros(shape=(len(self.s_chars), len(self.t_chars)))

        x, y = None, None
        max_score = None
        for i, s_i in enumerate(self.s_chars):
            # row for ith character of s
            row = []
            for j, t_j in enumerate(self.t_chars):
                next_score = self.calculate_opt_score(s_i, t_j, i, j)
                self.alignment_table[i][j] = next_score
                if max_score is None or next_score > max_score:
                    max_score = next_score
                    x = i
                    y = j

        self.max_score = max_score
        self.max_score_x = x
        self.max_score_y = y


    # Calculates the smith-waterman local alignment score as well as
    # the alignments.
    def align_sequences(self):

        # Backtrack from the maximum score
        i, j = self.max_score_x, self.max_score_y
        path = [(i, j)]
        current_entry = self.alignment_table[i, j]
        while current_entry != 0:
            # Choose next direction and append to path
            i, j = self.backtrace(self.s_chars[i], self.t_chars[j], i, j)
            current_entry = self.alignment_table[i, j]
            if current_entry != 0:
                path.append((i, j))

        full_backtrace = list(reversed(path))

        # Constructs the alignment using the path found in backtrace
        curr_place = None
        alignment_length = len(full_backtrace)
        self.s_align = np.chararray((alignment_length,))
        self.t_align = np.chararray((alignment_length,))
        for idx, (i, j) in enumerate(full_backtrace):
            # initial alignment
            if curr_place is None:
                self.s_align[idx] = self.s_chars[i]
                self.t_align[idx] = self.t_chars[j]
            else:
                if i == curr_place[0] + 1 and j == curr_place[1] + 1:
                    self.s_align[idx] = self.s_chars[i]
                    self.t_align[idx] = self.t_chars[j]
                elif i == curr_place[0] and j == curr_place[1] + 1:    
                    self.s_align[idx] = '-'
                    self.t_align[idx] = self.t_chars[j]
                else:
                    self.s_align[idx] = self.s_chars[i]
                    self.t_align[idx] = '-'

            curr_place = (i, j)

        self.full_backtrace = full_backtrace


    # Scores the left, diagonal, and above neighbor according to score + neighbor
    #
    # Returns the three as a list
    def score_neighbors(self, u, v, i, j):
        # Initialize values of neighbors
        # 
        # Taking the left and above neighbors means incurring a penalty for
        # including a gap
        #
        # diagonal includes the blosom62 score
        left = self.alignment_table[i][j - 1] - 4 if j > 0 else None
        diagonal = self.alignment_table[i - 1][j - 1] + blosum62[u][v] if i > 0 and j > 0 else None
        above = self.alignment_table[i - 1][j] - 4 if i > 0 else None

        return [left, diagonal, above, 0]


    # Calculates the score for an unfilled entry in the
    # alignment table.
    #
    # u : current char from S, v : current char from T,
    # (i, j) : coordinates of the entry to be filled, where the letters
    # that meet at (i, j) of the alignment_table are S[i] and T[j]
    #
    # i and j are assumed to be nonnegative
    #
    # returns the max score + neighbor combination and where
    # it came from
    def calculate_opt_score(self, u, v, i, j):

        # First entry in table
        if i == 0 or j == 0:
            return 0

        scores = self.score_neighbors(u, v, i, j)
        max_score = None
        for i, score in enumerate(scores):
            if max_score is None or score is not None and max_score < score:
                max_score = score

        # Specific to local alignment
        return max(max_score, 0)


    # Calculates the next neighbor to jump to based on the 
    # maximum score + maximum neighbor
    def backtrace(self, u, v, i, j):

        # First entry in table
        if i == 0 and j == 0:
            return (0, 0)

        scores = self.score_neighbors(u, v, i, j)

        # In edge cases, there might not be a left or above
        max_neighbor = None
        max_neighbor_idx = None
        for idx, score in enumerate(scores):
            if (max_neighbor is None) or (score is not None and score > max_neighbor):
                max_neighbor = score
                max_neighbor_idx = idx


        # Slight tweak here: in the case of a three-way tie, favor the diagonal
        max_neighbor_coordinates = None
        if max_neighbor_idx == 1:
            max_neighbor_coordinates = (i - 1, j - 1)
        elif max_neighbor_idx == 0:
            max_neighbor_coordinates = (i, j - 1)
        else:
            max_neighbor_coordinates = (i - 1, j)

        return max_neighbor_coordinates

    # Prints protein alignments to a file
    def print_alignment(self, p1, p2):
        s_align_str = b''.join(self.s_align).decode('utf-8')
        t_align_str = b''.join(self.t_align).decode('utf-8')
        s_align_fragments = []
        t_align_fragments = []

        space_out = '{0:6}: {1:3}  {2:20}'
        if len(s_align_str) < 60:
            r1 = [p1, self.full_backtrace[0][0], s_align_str]
            r2 = [p2, self.full_backtrace[0][1], t_align_str]
            print(space_out.format(*r1))
            print(space_out.format(*r2))
        else:
            while (len(s_align_str) > 60):
                s_align_fragments.append(s_align_str[0:60])
                t_align_fragments.append(t_align_str[0:60])
                s_align_str = s_align_str[60:len(s_align_str)]

            for i in range(len(s_align_fragments)):
                r1 = [p1, self.full_backtrace[0][0]+ i * 60, s_align_fragments[i]]
                r2 = [p2, self.full_backtrace[0][1] + i * 60, t_align_fragments[i]]
                print(space_out.format(*r1))
                print(space_out.format(*r2))


    # Prints protein alignments to a file
    def print_alignment_to_file(self, p1, p2, f):
        s_align_str = b''.join(self.s_align).decode('utf-8')
        t_align_str = b''.join(self.t_align).decode('utf-8')
        s_align_fragments = []
        t_align_fragments = []

        space_out = '{0:6}: {1:3}  {2:20}'
        if len(s_align_str) < 60:
            r1 = [p1, self.full_backtrace[0][0], s_align_str]
            r2 = [p2, self.full_backtrace[0][1], t_align_str]
            f.write(space_out.format(*r1))
            f.write("\n")
            f.write(space_out.format(*r2))
            f.write("\n\n")

            print(space_out.format(*r1))
            print(space_out.format(*r2))
        else:
            while (len(s_align_str) > 60):
                s_align_fragments.append(s_align_str[0:60])
                t_align_fragments.append(t_align_str[0:60])
                s_align_str = s_align_str[60:len(s_align_str)]

            for i in range(len(s_align_fragments)):
                r1 = [p1, self.full_backtrace[0][0]+ i * 60, s_align_fragments[i]]
                r2 = [p2, self.full_backtrace[0][1] + i * 60, t_align_fragments[i]]
                f.write(space_out.format(*r1))
                f.write("\n")
                f.write(space_out.format(*r2))
                f.write("\n\n")

                print(space_out.format(*r1))
                print(space_out.format(*r2))

        print(p1, "&", p2, "alignment completed \n")



if __name__ == "__main__":
    main()
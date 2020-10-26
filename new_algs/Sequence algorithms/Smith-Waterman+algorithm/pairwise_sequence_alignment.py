import logging
import argparse


def parse(fname):
    with open(fname) as fp:
        lines = fp.readlines()

    return lines[0].rstrip(), lines[1]


def get_args():
    parser = argparse.ArgumentParser(description='Pairwise sequence alignment')

    parser.add_argument('-i', '--input', dest='filename', type=str, help='Input filename', default="./sequences.txt")
    parser.add_argument('-a', '--algorithm', dest='algorithm', type=str, help='Algorithm ("global" or "local")', default="global")

    parser.add_argument('-m', '--match', dest='match_score', type=int, help='Match score', default=5)
    parser.add_argument('-p', '--miss', dest='miss_penalty', type=int, help='Miss match penalty', default=-4)
    parser.add_argument('-o', '--gap_opening', dest='gap_opening', type=int, help='Gap opening penalty', default=-10)
    parser.add_argument('-e', '--gap_extension', dest='gap_extension', type=int, help='Gap extension penalty', default=-5)

    args = parser.parse_args()

    return args


def init_matrix(rows, cols, algorithm='local'):
    mat = [[0] * cols for row in range(rows)]
    gap_mat = [[[0, set()]] * cols for row in range(rows)]
    gap_mat[1][0] = [0, set()]
    gap_mat[0][1] = [0, set()]

    # fills the cells in the first row and first column according to the selected algorithm
    if algorithm == 'global':
        for i in range(1, rows):
            mat[i][0] = mat[i - 1][0] + gap_penalty(gap_mat, i - 1, 0, 'v')
            gap_mat[i][0] = [1, {'v'}]
        for j in range(1, cols):
            mat[0][j] = mat[0][j - 1] + gap_penalty(gap_mat, 0, j - 1, 'h')
            gap_mat[0][j] = [1, {'h'}]
    elif algorithm == 'local':
        for i in range(1, rows):
            mat[i][0] = 0
            gap_mat[i][0] = [1, {'v'}]
        for j in range(1, cols):
            mat[0][j] = 0
            gap_mat[0][j] = [1, {'h'}]
    else:
        print("Please enter a valid algorithm... ('global' or 'local')")

    logging.info('Matrix initialized...\n')

    return mat, gap_mat


def print_matrix(matrix):
    logging.info('Matrix printing...\n')
    for row in matrix:
        print(''.join(['{0:>{w}}'.format(item, w=5) for item in row]), end='\n\n')


def is_match(char_a, char_b):
    return match_score if char_a == char_b else miss_match_penalty


def gap_penalty(gap_matrix, row_idx, col_idx, gap_direction):
    
    # If the current cell is gap, returns gap extension penalty or
    # gap opening penalty depending on whether the gap is horizontal or vertical.
    if gap_matrix[row_idx][col_idx][0] == 1:
        if gap_direction == 'v':
            if 'v' in gap_matrix[row_idx][col_idx][1]:
                return gap_extend
        elif gap_direction == 'h':
            if 'h' in gap_matrix[row_idx][col_idx][1]:
                return gap_extend

    return gap_opening


def global_alignment(M, gap_matrix, s1, s2, rows, cols):
    
    # fills the score matrix
    for i in range(1, rows):
        for j in range(1, cols):
            diagonal = M[i - 1][j - 1] + is_match(s1[j - 1], s2[i - 1])
            vgap = M[i - 1][j] + gap_penalty(gap_matrix, i - 1, j, 'v')
            hgap = M[i][j - 1] + gap_penalty(gap_matrix, i, j - 1, 'h')

            options = [diagonal, vgap, hgap]
            index_max = options.index(max(options))

            if options[index_max] == hgap:
                gap_matrix[i][j] = [1, {'h'}]

            if options[index_max] == vgap:
                gap_matrix[i][j] = [1, {'v'}]


            M[i][j] = options[index_max]

    i, j = rows - 1, cols - 1
    aligned_s1, aligned_s2, mid = (' ') * 3

    # backtracking
    while i > 0 and j > 0:
        diagonal = M[i][j] - is_match(s1[j - 1], s2[i - 1])
        vgap = M[i][j] - gap_penalty(gap_matrix, i - 1, j, 'v')
        hgap = M[i][j] - gap_penalty(gap_matrix, i, j - 1, 'h')

        if M[i - 1][j - 1] == diagonal:
            aligned_s1 += s1[j - 1]
            aligned_s2 += s2[i - 1]
            if is_match(s1[j - 1], s2[i - 1]) == match_score:
                mid += '|'
            else:
                mid += ' '
            i = i - 1
            j = j - 1
        elif M[i - 1][j] == vgap:
            aligned_s1 += '-'
            aligned_s2 += s2[i - 1]
            mid += ' '
            i = i - 1
        elif M[i][j - 1] == hgap:
            aligned_s1 += s1[j - 1]
            aligned_s2 += '-'
            mid += ' '
            j = j - 1

    while j > 0:
        aligned_s1 += s1[j - 1]
        aligned_s2 += '-'
        mid += ' '
        j = j - 1

    while i > 0:
        aligned_s1 += '-'
        aligned_s2 += s2[i - 1]
        mid += ' '
        i = i - 1
        
    # shows the aligned arrays on the console
    logging.info('Sequence alignment printing...\n')
    print(aligned_s1[::-1] + '\n' + mid[::-1] + '\n' + aligned_s2[::-1], "\n")

    match_hit = mid.count('|')
    print("Percent identity:", (match_hit * 100) / (len(mid) - 1))

    return M, M[rows - 1][cols - 1]


def local_alignment(M, gap_matrix, s1, s2, rows, cols):
    max_score = 0
    optimal_point = (0, 0)

    # fills the score matrix
    for i in range(1, rows):
        for j in range(1, cols):
            diagonal = M[i - 1][j - 1] + is_match(s1[j - 1], s2[i - 1])
            vgap = M[i - 1][j] + gap_penalty(gap_matrix, i - 1, j, 'v')
            hgap = M[i][j - 1] + gap_penalty(gap_matrix, i, j - 1, 'h')

            options = [0, diagonal, vgap, hgap]
            index_max = options.index(max(options))

            if options[index_max] == hgap:
                gap_matrix[i][j] = [1, {'h'}]

            if options[index_max] == vgap:
                gap_matrix[i][j] = [1, {'v'}]

            M[i][j] = options[index_max]

            if M[i][j] > max_score:
                max_score = M[i][j]
                optimal_point = (i, j)

    i, j = optimal_point[0], optimal_point[1]
    aligned_s1, aligned_s2, mid = (' ') * 3
    
    # backtracking
    while i > 0 and j > 0:
        diagonal = M[i][j] - is_match(s1[j - 1], s2[i - 1])
        vgap = M[i][j] - gap_penalty(gap_matrix, i - 1, j, 'v')
        hgap = M[i][j] - gap_penalty(gap_matrix, i, j - 1, 'h')

        if M[i - 1][j - 1] == diagonal:
            aligned_s1 += s1[j - 1]
            aligned_s2 += s2[i - 1]
            if is_match(s1[j - 1], s2[i - 1]) == match_score:
                mid += '|'
            else:
                mid += ' '
            i = i - 1
            j = j - 1
        elif M[i - 1][j] == vgap:
            aligned_s1 += '-'
            aligned_s2 += s2[i - 1]
            mid += ' '
            i = i - 1
        elif M[i][j - 1] == hgap:
            aligned_s1 += s1[j - 1]
            aligned_s2 += '-'
            mid += ' '
            j = j - 1
        elif M[i][j] == 0:
            break

    terminal_gap_count = 0
    while j > 0:
        aligned_s1 += s1[j - 1]
        aligned_s2 += '-'
        terminal_gap_count += 1
        mid += ' '
        j = j - 1

    while i > 0:
        aligned_s1 += '-'
        aligned_s2 += s2[i - 1]
        terminal_gap_count += 1
        mid += ' '
        i = i - 1

    # shows the aligned arrays on the console
    logging.info('Sequence alignment printing...\n')
    print(aligned_s1[::-1] + '\n' + mid[::-1] + '\n' + aligned_s2[::-1], "\n")

    match_hit = mid.count('|')
    print("Percent identity:", (match_hit * 100) / ((len(mid)-1) - terminal_gap_count))

    return M, max_score


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    args = get_args()

    if args.filename:

        filename = args.filename
        sequence_a, sequence_b = parse(filename)

        rows, cols = len(sequence_b) + 1, len(sequence_a) + 1

        match_score = args.match_score
        miss_match_penalty = args.miss_penalty
        gap_opening = args.gap_opening
        gap_extend = args.gap_extension

        print(
            "Filename\t:{}\nAlgorithm\t:{}\nMatch score\t:{}\nMiss match\t:{}\nGap opening\t:{}\nGap Extension\t:{}\n".format(
                args.filename, args.algorithm, match_score, miss_match_penalty, gap_opening, gap_extend))

        if args.algorithm == 'global':
            D, gap_matrix = init_matrix(rows, cols, algorithm=args.algorithm)
            D, score = global_alignment(D, gap_matrix, sequence_a, sequence_b, rows, cols)
            print("Total Alignment Score:", score)
        elif args.algorithm == 'local':
            D, gap_matrix = init_matrix(rows, cols, algorithm=args.algorithm)
            D, score = local_alignment(D, gap_matrix, sequence_a, sequence_b, rows, cols)
            print("Total Alignment Score:", score)
        else:
            print("Please enter a valid algorithm... ('global' or 'local')")

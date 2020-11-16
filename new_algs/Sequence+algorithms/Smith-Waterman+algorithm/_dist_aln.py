import numpy as np
import _dist_aln_cpp

_traceback_encoding = {'match': 1, 'vertical-gap': 2, 'horizontal-gap': 3,
                       'uninitialized': -1, 'alignment-end': 0}

def _init_matrices_nw(seq1, seq2, gap_open_penalty, gap_extend_penalty):
    shape = (len(seq1)+1, len(seq2)+1)
    score_matrix = np.zeros(shape)
    traceback_matrix = np.zeros(shape, dtype=np.int)
    traceback_matrix += _traceback_encoding['uninitialized']
    traceback_matrix[0, 0] = _traceback_encoding['alignment-end']

    # cache some values for quicker access
    vgap = _traceback_encoding['vertical-gap']
    hgap = _traceback_encoding['horizontal-gap']

    for i in range(1, shape[0]):
        score_matrix[i, 0] = -gap_open_penalty - ((i-1) * gap_extend_penalty)
        traceback_matrix[i, 0] = vgap

    for i in range(1, shape[1]):
        score_matrix[0, i] = -gap_open_penalty - ((i-1) * gap_extend_penalty)
        traceback_matrix[0, i] = hgap

    return score_matrix, traceback_matrix

def _init_matrices_nw_no_terminal_gap_penalty(
        seq1, seq2, gap_open_penalty, gap_extend_penalty):
    shape = (len(seq2)+1, len(seq1)+1)
    score_matrix = np.zeros(shape)
    traceback_matrix = np.zeros(shape, dtype=np.int)
    traceback_matrix += _traceback_encoding['uninitialized']
    traceback_matrix[0, 0] = _traceback_encoding['alignment-end']

    # cache some values for quicker access
    vgap = _traceback_encoding['vertical-gap']
    hgap = _traceback_encoding['horizontal-gap']

    for i in range(1, shape[0]):
        traceback_matrix[i, 0] = vgap

    for i in range(1, shape[1]):
        traceback_matrix[0, i] = hgap

    return score_matrix, traceback_matrix


def _compute_score_and_traceback_matrices(
        seq1, seq2, gap_open_penalty, gap_extend_penalty, similarity_matrix,
        new_alignment_score=-np.inf, init_matrices_f=_init_matrices_nw_no_terminal_gap_penalty,
        penalize_terminal_gaps=False, gap_substitution_score=0):
    """Return dynamic programming (score) and traceback matrices.

    A note on the ``penalize_terminal_gaps`` parameter. When this value is
    ``False``, this function is no longer true Smith-Waterman/Needleman-Wunsch
    scoring, but when ``True`` it can result in biologically irrelevant
    artifacts in Needleman-Wunsch (global) alignments. Specifically, if one
    sequence is longer than the other (e.g., if aligning a primer sequence to
    an amplification product, or searching for a gene in a genome) the shorter
    sequence will have a long gap inserted. The parameter is ``True`` by
    default (so that this function computes the score and traceback matrices as
    described by the original authors) but the global alignment wrappers pass
    ``False`` by default, so that the global alignment API returns the result
    that users are most likely to be looking for.

    """
    seq1_length = len(seq1)
    seq2_length = len(seq2)
    # cache some values for quicker/simpler access
    aend = _traceback_encoding['alignment-end']
    match = _traceback_encoding['match']
    vgap = _traceback_encoding['vertical-gap']
    hgap = _traceback_encoding['horizontal-gap']

    new_alignment_score = (new_alignment_score, aend)

    # Initialize a matrix to use for scoring the alignment and for tracing
    # back the best alignment
    score_matrix, traceback_matrix = init_matrices_f(
        seq1, seq2, gap_open_penalty, gap_extend_penalty)

    # Iterate over the characters in seq2 (which corresponds to the vertical
    # sequence in the matrix)
    for seq2_pos in range(1,seq2_length+1):
        # Iterate over the characters in seq1 (which corresponds to the
        # horizontal sequence in the matrix)
        for seq1_pos in range(1,seq1_length+1):
            # compute the score for a match/mismatch
            substitution_score = similarity_matrix[seq2_pos-1, seq1_pos-1]

            diag_score = \
                (score_matrix[seq2_pos-1, seq1_pos-1] + substitution_score,
                 match)

            # compute the score for adding a gap in aln2 (vertical)
            if not penalize_terminal_gaps and (seq1_pos == seq1_length):
                # we've reached the end of aln1, so adding vertical gaps
                # (which become gaps in aln1) should no longer
                # be penalized (if penalize_terminal_gaps == False)
                up_score = (score_matrix[seq2_pos-1, seq1_pos], vgap)
            elif traceback_matrix[seq2_pos-1, seq1_pos] == vgap:
                # gap extend, because the cell above was also a gap
                up_score = \
                    (score_matrix[seq2_pos-1, seq1_pos] - gap_extend_penalty,
                     vgap)
            else:
                # gap open, because the cell above was not a gap
                up_score = \
                    (score_matrix[seq2_pos-1, seq1_pos] - gap_open_penalty,
                     vgap)

            # compute the score for adding a gap in aln1 (horizontal)
            if not penalize_terminal_gaps and (seq2_pos == seq2_length):
                # we've reached the end of aln2, so adding horizontal gaps
                # (which become gaps in aln2) should no longer
                # be penalized (if penalize_terminal_gaps == False)
                left_score = (score_matrix[seq2_pos, seq1_pos-1], hgap)
            elif traceback_matrix[seq2_pos, seq1_pos-1] == hgap:
                # gap extend, because the cell to the left was also a gap
                left_score = \
                    (score_matrix[seq2_pos, seq1_pos-1] - gap_extend_penalty,
                     hgap)
            else:
                # gap open, because the cell to the left was not a gap
                left_score = \
                    (score_matrix[seq2_pos, seq1_pos-1] - gap_open_penalty,
                     hgap)

            # identify the largest score, and use that information to populate
            # the score and traceback matrices
            best_score = _first_largest([new_alignment_score, left_score,
                                         diag_score, up_score])
            score_matrix[seq2_pos, seq1_pos] = best_score[0]
            traceback_matrix[seq2_pos, seq1_pos] = best_score[1]

    return score_matrix, traceback_matrix


def _traceback(traceback_matrix, score_matrix, seq1, seq2, start_row,
               start_col):
    # cache some values for simpler reference
    aend = _traceback_encoding['alignment-end']
    match = _traceback_encoding['match']
    vgap = _traceback_encoding['vertical-gap']
    hgap = _traceback_encoding['horizontal-gap']
    gap_character = -1

    # initialize the result alignments
    aligned_seq1 = []
    aligned_seq2 = []

    current_row = start_row
    current_col = start_col

    best_score = score_matrix[current_row, current_col]
    current_value = None

    while current_value != aend:
        current_value = traceback_matrix[current_row, current_col]

        if current_value == match:
            aligned_seq1.append( seq1[current_col-1] )
            aligned_seq2.append( seq2[current_row-1] )
            current_row -= 1
            current_col -= 1
        elif current_value == vgap:
            aligned_seq1.append( gap_character )
            aligned_seq2.append( seq2[current_row-1] )
            current_row -= 1
        elif current_value == hgap:
            aligned_seq1.append( seq1[current_col-1] )
            aligned_seq2.append( gap_character )
            current_col -= 1
        elif current_value == aend:
            continue
        else:
            raise ValueError(
                "Invalid value in traceback matrix: %s" % current_value)

    return aligned_seq1, aligned_seq2, best_score, current_col, current_row


def _first_largest(scores):
    """ Similar to max, but returns the first element achieving the high score

    If max receives a tuple, it will break a tie for the highest value
    of entry[i] with entry[i+1]. We don't want that here - to better match
    with the results of other tools, we want to be able to define which
    entry is returned in the case of a tie.
    """
    result = scores[0]
    for score, direction in scores[1:]:
        if score > result[0]:
            result = (score, direction)
    return result


def local_pairwise_align(seq1, seq2, gap_open_penalty,
                         gap_extend_penalty, substitution_matrix):

    score_matrix, traceback_matrix = _compute_score_and_traceback_matrices(
        seq1, seq2, gap_open_penalty, gap_extend_penalty,
        substitution_matrix, new_alignment_score=0.0)
    #print(np.array(score_matrix, dtype=np.int32))

    end_row_position, end_col_position =\
        np.unravel_index(np.argmax(score_matrix), score_matrix.shape)

    aligned1, aligned2, score, seq1_start_position, seq2_start_position = \
        _traceback(traceback_matrix, score_matrix, seq1, seq2,
                   end_row_position, end_col_position)

    start_end_positions = [(seq1_start_position, end_col_position-1),
                           (seq2_start_position, end_row_position-1)]

    aligned1 = aligned1[::-1]   ### restore the correct order
    aligned2 = aligned2[::-1]

    return aligned1, aligned2, score, start_end_positions

if __name__ == "__main__":
    seq1 = ['C', 'A', 'G', 'C', 'C', 'U', 'C', 'G', 'C', 'U', 'U', 'A', 'G']
    seq2 = ['A', 'A', 'U', 'G', 'C', 'C', 'A', 'U', 'U', 'G', 'A', 'C', 'G', 'G']
    gap_open_penalty = 1
    gap_extend_penalty = 1/3
    S = np.zeros([len(seq2), len(seq1)], dtype=np.float)
    np.set_printoptions(precision=2)
    for i in range(len(seq2)):
        for j in range(len(seq1)):
            if seq2[i] == seq1[j]:
                S[i,j] = 1.
            else:
                S[i,j] = -(1./3)
    aligned1, aligned2, score, start_end_positions = \
        local_pairwise_align(seq1, seq2, 1., 1./3, S)
    print(aligned1)
    print(aligned2)
    print(score)
    print(start_end_positions)


    aligned1, aligned2, score, start_end_positions = \
        _dist_aln_cpp.local_pairwise_align(seq1, seq2, 1., 1./3, S)
    print(aligned1)
    print(aligned2)
    print(score)
    print(start_end_positions)

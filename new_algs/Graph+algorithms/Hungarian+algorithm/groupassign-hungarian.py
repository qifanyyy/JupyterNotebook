# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import argparse
import numpy as np
import random
import scipy.optimize


def participants_to_dict(pp_fname, discount='sqrt'):
    if discount == 'sqrt':
        discount = np.sqrt
    elif discount == 'linear':
        discount = int
    elif discount == 'quadratic':
        discount = np.square
    pp_dict = {}
    groups = []
    with open(pp_fname, 'r') as pp_file:
        for line in pp_file:
            line = line.lower().replace('\r\n', '').replace('\n', '').split(',')
            pp_dict[line[0]] = {}
            groups += line[1:]
            for i in range(len(line[1:])):
                if line[i + 1] not in ['-', 'NA', 'N/A']:
                    pp_dict[line[0]][line[i + 1]] = discount(i)
    groups = set(groups)
    return pp_dict, groups


def fill_missing_preferences(pp_dict, groups, na_weight=99):
    for pp in pp_dict.keys():
        n_prefs = len(list(pp_dict[pp].keys()))
        for group in groups:
            if group not in pp_dict[pp].keys():
                pp_dict[pp][group] = na_weight * n_prefs
    return pp_dict


def dict_to_matrix(pp_dict, groups, max_group_size):
    group_labels = []
    for group in sorted(groups):
        group_labels += [group] * max_group_size
    pp_labels = sorted(pp_dict.keys())
    random.shuffle(pp_labels)  # comment out this line to get deterministic (but unfair) behavior
    cost_matrix = []
    for pp in pp_labels:
        pp_cost = []
        for group in sorted(groups):
            pp_cost += [pp_dict[pp][group.lower()]] * max_group_size
        cost_matrix.append(np.array(pp_cost))
    cost_matrix = np.vstack(cost_matrix)
    return cost_matrix, pp_labels, group_labels


def assign_to_groups(cost_matrix, pp_labels, group_labels):
    pps, groups = scipy.optimize.linear_sum_assignment(cost_matrix)
    assignments = [(pp_labels[pps[i]], group_labels[groups[i]]) for i in range(len(pps))]
    return assignments


def assign(filename, na_weight, max_group_size, discount, verbose=True):
    pp_dict, groups = participants_to_dict(filename, discount)
    pp_dict = fill_missing_preferences(pp_dict, groups, na_weight)
    cost_matrix, pp_labels, group_labels = dict_to_matrix(pp_dict, groups, max_group_size)
    assignments = sorted(assign_to_groups(cost_matrix, pp_labels, group_labels))
    if verbose:
        for assignment in assignments:
            print('{},{}'.format(assignment[0], assignment[1]))
    return assignments


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='use the Hungarian algorithm to assign'
                                        + ' participants to groups according to preference')
    argparser.add_argument('--filename',
                           help='comma-separated text file of participants\' group preferences')
    argparser.add_argument('--max_group_size', type=int,
                           help='maximum size of groups')
    argparser.add_argument('--na_weight', default=99, type=int,
                           help='penalty weight assigned to missing (dispreferred) groups')
    argparser.add_argument('--discount', default='sqrt', choices=['sqrt', 'linear', 'quadratic'],
                           help='discount rate for preference weighting, default is to use'
                           + ' square root of rank as weight, but "linear" and "quadratic"'
                           + ' weighting are also options (use the default if you are unsure)')
    args = argparser.parse_args()
    assign(**vars(args))

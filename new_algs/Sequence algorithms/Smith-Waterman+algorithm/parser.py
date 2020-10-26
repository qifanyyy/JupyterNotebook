"""
CAP6640 spring 2018 - Dr.Glinos
Author: Sridevi Divya Krishna Devisetty(4436572)

This program control starts at main.
main function accepts one command line argument ,like the names of test file.
main(sys.argv[1]) is equivalent to main('piper') or main('hearing')

**Note: 1) Place the input files in the same directory as of the program file.
        2) To run program:
            python parser.py piper
            python parser.py hearing
python version: python 3.5
"""

import collections
import sys
from collections import defaultdict

# constants
RIGHT_ARC_SYM = " --> "

LEFT_ARC_SYM = " <-- "

colon = ": "

SWAP = "SWAP"

FINAL = "FINAL"

ROOT = 'ROOT --> '

LEFT_ARC = "Left-Arc"

SHIFT = "SHIFT"

RIGHT_ARC = "Right-Arc"

word_index = 0
word_pos = 1
tag_pos = 2
arc_index = 3


def print_left_arc_counts(left_dep_head_count, tags):
    print()
    print('Left Arc Array Nonzero Counts:\n')
    sorted_tags = sorted(tags)
    for tag in sorted_tags:
        print(" {0}".format(tag).center(6), end=' ')
        print("{0}".format(colon).center(2), end=' ')
        if left_dep_head_count.get(tag):
            sorted_items = sorted(left_dep_head_count.get(tag).items())
            ord_items = collections.OrderedDict(sorted_items)
            for dep_tag, count in ord_items.items():
                print("[", dep_tag, ",", count, "]", end=" ")
        print()


def print_right_arc_counts(right_dep_head_count, tags):
    print()
    print('Right Arc Array Nonzero Counts:\n')
    sorted_tags = sorted(tags)
    for tag in sorted_tags:
        print(" {0}".format(tag).center(6), end=' ')
        print("{0}".format(colon).center(2), end=' ')
        if right_dep_head_count.get(tag):
            sorted_items = sorted(right_dep_head_count.get(tag).items())
            ord_items = collections.OrderedDict(sorted_items)
            for dep_tag, count in ord_items.items():
                print("[", dep_tag, ",", count, "]", end=" ")
        print()


def print_confusion_arc(confusion_arc_count, tag_set):
    print()
    print('Arc Confusion Array:\n')
    sorted_tags = sorted(tag_set)
    for tag in sorted_tags:
        print(" {0}".format(tag).center(6), end=' ')
        print("{0}".format(colon).center(2), end=' ')
        if confusion_arc_count.get(tag):
            sorted_items = sorted(confusion_arc_count.get(tag).items())
            ord_items = collections.OrderedDict(sorted_items)
            for dep_tag, count in ord_items.items():
                print("[", dep_tag, ",", count[0], ",", count[1], "]", end=" ")
        print()


def process_corpus_data(corpus_content):
    print("Corpus Statistics:\n")
    sentences = list(filter(bool, corpus_content.split('\n\n')))
    print("# sentences\t:{0}".format(len(sentences)).rjust(7))
    sentence_by_index = defaultdict()

    total_tokens = 0
    for index, sentence in enumerate(sentences):
        word_list = list(filter(bool, sentence.split('\n')))
        sentence_by_index[index] = word_list
        total_tokens += len(word_list)
    print("# tokens\t:{0}".format(total_tokens).rjust(7))

    words_in_sentence = defaultdict(list)
    for ind, sentence in sentence_by_index.items():
        for line in sentence:
            each_line = line.split(' ')
            words_in_sentence[ind].append(each_line)

    tags_list = []
    word_list = []
    left_dep_head_dict = defaultdict(list)
    left_arc_stats = 0

    right_dep_head_dict = defaultdict(list)
    right_arc_stats = 0
    root = {}
    for sen_ind, sent_words in words_in_sentence.items():
        for word in sent_words:
            current_arc_index = int(word[arc_index])
            current_index = int(word[word_index])
            if current_arc_index == 0:
                root[sen_ind] = [word[word_pos], word[tag_pos]]
                continue
            elif current_arc_index > current_index:
                head_word = sent_words[current_arc_index - 1]
                head_tag = head_word[tag_pos]
                dep_tag = word[tag_pos]
                left_dep_head_dict[dep_tag].append(head_tag)
                left_arc_stats += 1
            elif current_arc_index < current_index:
                head_word = sent_words[current_arc_index - 1]
                head_tag = head_word[tag_pos]
                dep_tag = word[tag_pos]
                right_dep_head_dict[dep_tag].append(head_tag)
                right_arc_stats += 1
            else:
                print("")
            word_list.append(word[word_pos])
            tags_list.append(word[tag_pos])
    tag_set = set(tags_list)
    print("# POS tags\t:{0}".format(len(tag_set)).rjust(7))
    print("# Left-Arcs\t:{0}".format(left_arc_stats).rjust(7))
    print("# Right-Arcs:{0}".format(right_arc_stats).rjust(1))
    print("# Root-Arcs\t:{0}".format(len(root.keys())).rjust(7))

    left_dep_head_count = {}

    for left_dep, val in left_dep_head_dict.items():
        for tag in val:
            left_dep_head_count[left_dep] = left_dep_head_count.get(left_dep, {})
            left_dep_head_count[left_dep][tag] = left_dep_head_count[left_dep].get(tag, 0)
            left_dep_head_count[left_dep][tag] += 1
    print_left_arc_counts(left_dep_head_count, tag_set)
    right_dep_head_count = {}

    for right_dep, val in right_dep_head_dict.items():
        for tag in val:
            right_dep_head_count[right_dep] = right_dep_head_count.get(right_dep, {})
            right_dep_head_count[right_dep][tag] = right_dep_head_count[right_dep].get(tag, 0)
            right_dep_head_count[right_dep][tag] += 1
    print_right_arc_counts(right_dep_head_count, tag_set)

    confusion_arc_count = {}
    num_of_confusing_arcs = 0
    new_dict = {}
    for head in tag_set:
        new_dict[head] = list(set(left_dep_head_dict.get(head, []) + right_dep_head_dict.get(head, [])))
    for head_tag, val in new_dict.items():
        for dep_tag in val:
            a = [0] * 2
            confusion_arc_count[head_tag] = confusion_arc_count.get(head_tag, {})
            if left_dep_head_count.get(head_tag) and right_dep_head_count.get(head_tag):
                if left_dep_head_count[head_tag].get(dep_tag) and right_dep_head_count[head_tag].get(dep_tag):
                    confusion_arc_count[head_tag][dep_tag] = a
                    confusion_arc_count[head_tag][dep_tag][0] = left_dep_head_count[head_tag].get(dep_tag)
                    confusion_arc_count[head_tag][dep_tag][1] = right_dep_head_count[head_tag].get(dep_tag)
                    num_of_confusing_arcs += 1
    print_confusion_arc(confusion_arc_count, tag_set)
    print()
    print("\tNumber of confusing arcs = ",num_of_confusing_arcs)
    print()
    return left_dep_head_count, right_dep_head_count, confusion_arc_count


def print_parse(stack, buffer, action):
    if len(stack) == 0:
        print(stack, end=' ')
    else:
        print('[ ', end='')
        for s in range(len(stack)-1):
            print(stack[s], end=', ')
        print(stack[-1]+']', end=' ')
    if len(buffer) == 0:
        print(buffer, end=' ')
    else:
        print('[ ', end='')
        for b in range(len(buffer)-1):
            print(buffer[b], end=', ')
        print(buffer[-1]+']', end=' ')
    print(action)


def oracle(stack, conf_map, buffer):
    if len(stack) >= 2:
        i = len(stack) - 2
        j = len(stack) - 1
        i_tag = stack[i].split('/')[1]
        j_tag = stack[j].split('/')[1]
        if i_tag.startswith('V') and j_tag.startswith(('.', 'R')):
            str = RIGHT_ARC + colon + stack[i] + RIGHT_ARC_SYM + stack[j]
            return RIGHT_ARC, str
        elif i_tag.startswith('I') and j_tag.startswith('.'):
            return SWAP, SWAP
        elif len(buffer) >= 1 and i_tag.startswith(('V', 'I')) and j_tag.startswith(('D', 'R', 'I', 'J', 'P')):
            return SHIFT, SHIFT
        else:
            if conf_map.get(i_tag):
                if conf_map[i_tag].get(j_tag):
                    if conf_map[i_tag][j_tag][0] > conf_map[i_tag][j_tag][1]:
                        str = LEFT_ARC + colon + stack[i] + LEFT_ARC_SYM + stack[j]
                        return LEFT_ARC, str
                    else:
                        str = RIGHT_ARC + colon + stack[i] + RIGHT_ARC_SYM + stack[j]
                        return RIGHT_ARC, str
                else:
                    if conf_map[j_tag][i_tag][0] > conf_map[j_tag][i_tag][1]:
                        str = LEFT_ARC + colon + stack[i] + LEFT_ARC_SYM + stack[j]
                        return LEFT_ARC, str
                    else:
                        str = RIGHT_ARC + colon + stack[i] + RIGHT_ARC_SYM + stack[j]
                        return RIGHT_ARC, str
    elif len(stack) == 1 and len(buffer) == 0:
        return FINAL, ROOT + stack[0]
    else:
        return SHIFT, SHIFT


def apply_transition(stack, buffer, action, transition_set):
    transition_set.append(action)
    if action == SHIFT:
        stack.append(buffer.pop(0))
    elif action == RIGHT_ARC:
        j = len(stack) - 1
        dep = stack[j]
        dep_index = stack.index(dep)
        stack.pop(dep_index)
    elif action == LEFT_ARC:
        i = len(stack) - 2
        dep = stack[i]
        dep_index = stack.index(dep)
        stack.pop(dep_index)
    elif action == SWAP:
        i = len(stack) - 2
        buffer.insert(0, stack[i])
        stack.pop(i)
    # elif action == "FINAL":
    #     print("final")
    return stack, buffer, transition_set


def parse(conf_map, test_content):
    buffer = list(filter(bool, test_content.split('\n')))
    print()
    print("Input Sentence:")
    print(" ".join(buffer))
    print()
    print()
    print("Parsing Actions and Transitions:\n")
    stack = []
    transition_set = []
    action = oracle(stack, conf_map, buffer)
    while action != FINAL:
        stack, buffer, transition_set = apply_transition(stack, buffer, action, transition_set)
        action, print_str = oracle(stack, conf_map, buffer)
        print_parse(stack, buffer, print_str)


def main(test_file):
    print()
    print('University of Central Florida')
    print('CAP6640 Spring 2018 - Dr.Glinos')
    print('Dependency Parser by Sridevi Divya Krishna Devisetty')
    print("\n")
    corpus_file = open("wsj-clean.txt")
    corpus_content = corpus_file.read()
    left, right, conf = process_corpus_data(corpus_content)
    test_file = open(test_file + ".txt")
    test_content = test_file.read()
    parse(conf, test_content)


# main('piper')
#main('hearing')
# main(sys.argv[1])
import random

print([1,2,3])
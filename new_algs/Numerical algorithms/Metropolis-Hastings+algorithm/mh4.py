import sys
import re
import random
import numpy as np
import time


DIM = 4
DICE = 'rifobx ifehey denows utoknd hmsrao lupets acitoa ylgkue qbmjoa \
ehispn vetign baliyt ezavnd ralesc uwilrg pacemd'.split()
ALL_WORDS = []
DATAPATH = 'data/words_alpha.txt'
# DATAPATH = 'data/new_dictionary.txt'

try:
    TRIALS = int(sys.argv[1])
except (IndexError, ValueError):
    print("\nSetting number of trials to default of 1000")
    TRIALS = 1000


def score(roll):
    def solve():
        for y, row in enumerate(s):
            for x, letter in enumerate(row):
                for result in extending(letter, ((x, y),)):
                    yield result

    def extending(prefix, path):
        if prefix in words:
            yield (prefix, path)
        for (nx, ny) in neighbors(*path[-1]):
            if (nx, ny) not in path:
                prefix1 = prefix + s[ny][nx]
                if prefix1 in prefixes:
                    for result in extending(prefix1, path + ((nx, ny),)):
                        yield result

    def neighbors(x, y):
        for nx in range(max(0, x-1), min(x+2, DIM)):
            for ny in range(max(0, y-1), min(y+2, DIM)):
                yield (nx, ny)

    s = [roll[i:i+DIM] for i in range(0, DIM**2, DIM)]

    alphabet = ''.join(set(roll))
    valid_word = re.compile('[' + alphabet + ']{3,}$', re.I).match

    words = []
    for word in ALL_WORDS:
        if valid_word(word):
            words.append(word)

    prefixes = set(w[:i] for w in words for i in range(2, len(w)+1))

    ans = []
    for result in solve():
        ans.append(result[0])

    ans = set(ans)
    return len(ans), ans


def swap(dice, roll, num):
    new_roll = roll.copy()
    new_dice = dice.copy()
    swaps = random.sample(range(DIM**2), num)
    for i in range(num-1):
        new_dice[swaps[i]] = dice[swaps[i+1]]
    new_dice[swaps[-1]] = dice[swaps[0]]

    for i in swaps:
        new_roll[i] = random.sample(new_dice[i], 1)[0]
    return new_dice, new_roll


def sample_rolls(k):
    samples = {}
    for i in range(k):
        roll = []
        dice = random.sample(DICE, DIM ** 2)
        for d in dice:
            roll.append(random.sample(d, 1)[0])
        samples[''.join(roll)] = score(roll)
    return samples


def print_roll(r):
    for row in [r[i:i+DIM] for i in range(0, DIM**2, DIM)]:
        print(row)


def main():
    print('\nRunning algorithm for {0} steps'.format(TRIALS))
    print('\nReading in dictionary from {0}...'.format(DATAPATH))
    with open(DATAPATH) as f:
        for word in f:
            w = word.rstrip()
            length = len(w)
            if length >= 3 and length <= DIM**2:
                # check if all q's are qu's
                if 'q' in w:
                    is_q = False
                    # if q appears as last letter, ignore
                    for m in re.finditer('q', w):
                        i = m.start()
                        if w[i:(i+2)] != 'qu':
                            is_q = True
                            break
                    if is_q:
                        continue
                    else:
                        w = re.sub('qu', 'q', w)
                ALL_WORDS.append(w)
    print('Finished reading {0} words'.format(len(ALL_WORDS)))

    scores = {}
    max_words = []

    dice = random.sample(DICE, DIM ** 2)
    roll = [random.sample(d, 1)[0] for d in dice]
    scores[''.join(roll)] = old = score(roll)

    start = time.time()
    msg_time = time.time()
    for i in range(TRIALS):
        if i == 0 or time.time() - msg_time >= 5:
            print('\nTrial {0}, Time elapsed: {1:.2f}'
                  .format(i, time.time() - start))
            print('Number of words found: {0:g}'.format(old[0]))
            print_roll(roll)

            msg_time = time.time()

        new_dice, new_roll = swap(dice, roll, 3)
        roll_key = ''.join(new_roll)
        if roll_key in scores:
            new = scores[roll_key]
        else:
            scores[roll_key] = new = score(new_roll)
        if random.uniform(0, 1) < (np.exp(new[0] - old[0])):
            max_words.append(new[0])
            dice = new_dice
            roll = new_roll
            old = new

    roll_key = ''.join(roll)
    ans = scores[roll_key]
    print('\nFinal board arrangement has {0} words:'
          .format(ans[0]))
    print_roll(roll)
    print(ans[1])


if __name__ == '__main__':
    main()

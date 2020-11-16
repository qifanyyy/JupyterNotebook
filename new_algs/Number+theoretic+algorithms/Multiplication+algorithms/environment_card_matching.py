import numpy as np
import time, sys

from config_card_matching import RANK_CODE, SUIT_CODE, CONFIG


class ScratchPad(object):

    def __init__(self, card1, card2):
        self._board = np.zeros((CONFIG['ENVIRONMENT_ROW'], CONFIG['ENVIRONMENT_COL']), dtype=np.int8)
        self._card1_ptr = None
        self._card2_ptr = None
        self._out_ptr = None
        self._ptrs = None
        self._temp = False

        self._init_env(card1, card2)

    def _init_env(self, card1, card2):
        for index, card in enumerate([card1, card2]):
            self._board[index, 1] = int(RANK_CODE.get(card['rank'], card['rank']))
            self._board[index, 2] = int(SUIT_CODE.get(card['suit']))

        self._card1_ptr, self._card2_ptr, self._out_ptr = self._ptrs = [(row, -1) for row in range(3)]

    def done(self):
        if self._card1_ptr[1] < -3:
            return True
        return self._board[self._out_ptr[0], self._out_ptr[1]+1] != 0

    def usub1(self):
        return abs(self._board[self._card1_ptr] - self._board[self._card2_ptr])

    def write(self, value, debug=False):
        self._board[self._out_ptr] = value
        if debug:
            self.pretty_print()

    def lshift(self):
        self._card1_ptr, self._card2_ptr, self._out_ptr = self._ptrs = \
            [(row, col - 1) for (row, col) in self._ptrs]

    def pretty_print(self):
        new_strs = [''.join(map(str, self._board[i])) for i in range(3)]
        line_length = len('Card 1 :' + ' ' * 2 + new_strs[0])
        print('Card 1 :' + ' ' * 2 + new_strs[0])
        print('Card 2 :' + ' ' * 2 + new_strs[1])
        print('-' * line_length)
        print('Output :' + ' ' * 2 + new_strs[2])
        print('')
        time.sleep(.10)
        sys.stdout.flush()

    def get_env(self):
        env = np.zeros((CONFIG["ENVIRONMENT_ROW"], CONFIG["ENVIRONMENT_DEPTH"]), dtype=np.int32)
        if self._card1_ptr[1] < -CONFIG["ENVIRONMENT_COL"]:
            env[0][0] = 1
        else:
            env[0][self[self._card1_ptr]] = 1
        if self._card2_ptr[1] < -CONFIG["ENVIRONMENT_COL"]:
            env[1][0] = 1
        else:
            env[1][self[self._card2_ptr]] = 1
        if self._out_ptr[1] < -CONFIG["ENVIRONMENT_COL"]:
            env[2][0] = 1
        else:
            env[2][self[self._out_ptr]] = 1
        return env.flatten()

    def execute(self, prog_id, args):
        if prog_id == 0:               # MOVE!
            ptr, lr = args
            lr = (lr * 2) - 1
            if ptr == 0:
                self._card1_ptr = (self._card1_ptr[0], self._card1_ptr[1] + lr)
            elif ptr == 1:
                self._card2_ptr = (self._card2_ptr[0], self._card2_ptr[1] + lr)
            elif ptr == 2:
                self._out_ptr = (self._out_ptr[0], self._out_ptr[1] + lr)
            else:
                raise NotImplementedError
            self._ptrs = [self._card1_ptr, self._card2_ptr, self._out_ptr]
        elif prog_id == 1:             # WRITE!
            _, val = args
            self[self._out_ptr] = val

    def __getitem__(self, item):
        return self._board[item]

    def __setitem__(self, key, value):
        self._board[key] = value


def get_args(args, arg_in=True):
    if arg_in:
        arg_vec = np.zeros((CONFIG["ARGUMENT_NUM"], CONFIG["ARGUMENT_DEPTH"]), dtype=np.int32)
    else:
        arg_vec = [np.zeros((CONFIG["ARGUMENT_DEPTH"]), dtype=np.int32) for _ in
                   range(CONFIG["ARGUMENT_NUM"])]
    # print(args)
    if len(args) > 0:
        for i in range(CONFIG["ARGUMENT_NUM"]):
            if i >= len(args):
                arg_vec[i][CONFIG["DEFAULT_ARG_VALUE"]] = 1
            else:
                arg_vec[i][args[i]] = 1
    else:
        for i in range(CONFIG["ARGUMENT_NUM"]):
            arg_vec[i][CONFIG["DEFAULT_ARG_VALUE"]] = 1
    return arg_vec.flatten() if arg_in else arg_vec
"""
This module provides an implementation of the Todd-Coxeter
algorithm for coset enumeration. The solve function accepts
the presentation of a group and subgroup, and outputs the
completed table of cosets of the subgroup. The coxeter and
schlafli functions perform the same task, but accept the
coxeter graph and the schlafli symbol, respectively.
"""

from typing import List

from util import schlafli


class Row:
    __slots__ = 'rel', 'left', 'right', 'left_coset', 'right_target'

    def __init__(self, rel, i):
        """
        :param i: index of this row
        :param num: number of terms in relation
        """

        self.rel = rel
        self.left = 0
        self.right = len(rel)

        self.left_coset = i
        self.right_target = i

    @property
    def left_gen(self):
        return self.rel[self.left]

    @property
    def right_gen(self):
        return self.rel[self.right - 1]

    def learn(self, cosets: 'Cosets'):
        """
        :return: whether information was learned
        """
        if self.left + 1 == self.right:
            return False

        while self.left + 1 != self.right:
            left_target = cosets.get(self.left_coset, self.left_gen)
            if left_target is None:
                break

            self.left += 1
            self.left_coset = left_target

        while self.left + 1 != self.right:
            right_coset = cosets.rget(self.right_gen, self.right_target)
            if right_coset is None:
                break

            self.right -= 1
            self.right_target = right_coset

        if self.left + 1 == self.right:
            cosets.set(self.left_coset, self.left_gen, self.right_target)
            return True

        return False


class Cosets:
    __slots__ = 'names', 'n_gens', 'cosets', 'rcosets'

    def __init__(self, n_gens, names):
        self.names = names
        self.n_gens = n_gens

        self.cosets = []
        self.rcosets = []

        self.add_row()

    def get(self, coset, gen):
        target = self.cosets[coset][gen]
        return target

    def rget(self, gen, target):
        coset = self.rcosets[target][gen]
        return coset

    def set(self, coset, gen, target):
        self.cosets[coset][gen] = target
        self.rcosets[target][gen] = coset

    def add_row(self):
        self.cosets.append([None] * self.n_gens)
        self.rcosets.append([None] * self.n_gens)

    def add_coset(self):
        for i, coset in enumerate(self.cosets):
            for gen, target in enumerate(coset):
                if target is None:
                    target = len(self.cosets)
                    self.add_row()
                    self.set(i, gen, target)
                    return True
        return False

    @property
    def words(self):
        res = [None] * len(self)
        res[0] = ''

        while any(w is None for w in res):
            for c, w in enumerate(res):
                if w is None:
                    continue

                for g, t in zip(self.names, self.cosets[c]):
                    if res[t] is not None:
                        continue

                    res[t] = w + g

        return res

    def __str__(self):
        table = [
                    [' ', ' '] + [str(name) for name in self.names],
                ] + [
                    [str(coset), '|'] + [str(target) for target in targets]
                    for coset, targets in enumerate(self.cosets)
                ]

        widths = [max(len(col) for col in row) for row in zip(*table)]

        return '\n'.join(' '.join(f'{e:>{w}}' for e, w in zip(row, widths)) for row in table) + '\n'

    def __len__(self):
        return len(self.cosets)


def solve(gens, subgens, rels):
    """
    Given the presentation of a group and a subgroup, count the cosets of that
    subgroup and determine the relations between cosets.

    :param gens: Generators of the group
    :param subgens: Generators of the subgroup
    :param rels: Identity relations of the group
    :return: A coset table describing actions on each coset
    """
    names = gens
    rels = [[gens.index(g) for g in rel] for rel in rels]
    subgens = [gens.index(g) for g in subgens]

    cosets = Cosets(len(gens), names)
    rows: List[Row] = [Row(rel, 0) for rel in rels]

    for gen in subgens:
        cosets.set(0, gen, 0)

    while rows:
        while True:
            learned = False
            for i in reversed(range(len(rows))):
                if rows[i].learn(cosets):
                    learned = True
                    del rows[i]
            if not learned:
                break

        i = len(cosets)
        if cosets.add_coset():
            rows += (Row(rel, i) for rel in rels)
        else:
            break

    return cosets

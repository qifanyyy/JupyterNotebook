# Copyright 2015 Jason Owen <jason.a.owen@gmail.com>
#
# This file is part of matrix-chain-multiplication.
#
# matrix-chain-multiplication is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# matrix-chain-multiplication is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with matrix-chain-multiplication.  If not, see
# <http://www.gnu.org/licenses/>.

import argparse

class MatrixChainMultiplier:
  def __init__(self, dimensions):
    assert len(dimensions) > 1
    self.dimensions = dimensions
    self.count = len(dimensions) - 1

  def parenthesize(self):
    return self.recursively_parenthesize(0, self.count - 1)

  def recursively_parenthesize(self, start_matrix, end_matrix):
    if end_matrix > start_matrix:
      pivot = self.pivots[(start_matrix, end_matrix)]
      left = self.recursively_parenthesize(start_matrix, pivot)
      right = self.recursively_parenthesize(pivot + 1, end_matrix)
      return "(%s, %s)" % (left, right)
    else:
      return str(start_matrix)

  def calculate_costs(self):
    self.costs = {}
    self.pivots = {}
    self.initialize_costs()

    for length in range(2, self.count + 1): # length=2
      for i in range(self.count - length + 1): # 2 - 2 + 1 = 1 -> i=0
        j = i + length - 1 # 0 + 2 - 1 = j=1
        for k in range(i, j): # j=1 -> k=0
          q = (self.costs[(i,k)] # (0,0) -> 0
            +  self.costs[(k+1, j)] # (1,1) -> 0
            +  self.multiply_cost(i, k+1, j+1)) # (0, 1, 2)
          if (i,j) not in self.costs or q < self.costs[(i,j)]:
            self.costs[(i,j)] = q
            self.pivots[(i,j)] = k

  def initialize_costs(self):
    for identity in [(i, i) for i in range(self.count)]:
      self.costs[identity] = 0

  def multiply_cost(self, left_index, inner_index, right_index):
    left = self.dimensions[left_index]
    inner = self.dimensions[inner_index]
    right = self.dimensions[right_index]
    return left * inner * right

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("dimensions",
                      metavar='p',
                      type=int,
                      nargs='+',
                      help="an ordered list of matrix dimensions")
  args = parser.parse_args()
  multiplier = MatrixChainMultiplier(args.dimensions)
  multiplier.calculate_costs()
  print multiplier.parenthesize()

if __name__ == '__main__':
  main()

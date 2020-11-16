################################################################################
## Copyright (c) 2019, Vinitha Ranganeni
## All rights reserved.
##
## Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are met:
##
##     1. Redistributions of source code must retain the above copyright notice
##        this list of conditions and the following disclaimer.
##     2. Redistributions in binary form must reproduce the above copyright
##        notice, this list of conditions and the following disclaimer in the
##        documentation and#or other materials provided with the distribution.
##     3. Neither the name of the copyright holder nor the names of its
##        contributors may be used to endorse or promote products derived from
##        this software without specific prior written permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
## AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
## IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
## ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
## LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
## CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
## SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
## INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
## CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
## ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
## POSSIBILITY OF SUCH DAMAGE.
################################################################################

import sys
import re
import numpy as np
import matplotlib.pyplot as plt

def get_map(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    width = len(lines[0].split())
    height = len(lines)
    data = [p.strip().split() for p in lines]
    flattened_values = map(int, [item for sublist in data for item in
                                 sublist])
    map_values = np.array(flattened_values).reshape(height, width)
    return map_values

def plot_path(filename, ax):
    f = open(filename, 'r')
    lines = f.readlines()
    sol_values = np.array([map(int, p.strip().split()) for p in lines])
    ax.plot(sol_values[:,0], sol_values[:,1], 'y-')

if __name__ == '__main__':
    map_values = get_map(sys.argv[1])
    fig, ax = plt.subplots(figsize=(10,10))
    plt.imshow(map_values, vmin=0, vmax=1)
    plt.ylim([0, map_values.shape[0]])
    plt.xlim([0, map_values.shape[1]])

    plot_path(sys.argv[2], ax)
    plt.show()

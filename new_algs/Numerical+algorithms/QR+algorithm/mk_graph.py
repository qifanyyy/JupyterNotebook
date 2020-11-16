import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import os

data_list = [
        'fp16_notc',
        'fp16_tc_nocor',
        'fp32_notc',
        'fp32_tc_nocor',
        'fp32_tc_cor',
        'mixed_tc_cor_emu',
        'tf32_tc_nocor_emu',
        'tf32_tc_cor_emu',
        ]

def get_color(d):
    if 'fp16' in d:
        return '#51318f'
    if 'fp32' in d:
        return '#006c3a'
    if 'tf32' in d:
        return '#ed6c00'
    if 'mixed' in d:
        return '#333132'
    return '#ffffff'

def get_linestyle(d):
    if 'notc' in d:
        return '-'
    if 'nocor' in d:
        return '-.'
    if 'cor' in d:
        return ':'
    return '--'

fig, ((ax0, ax1)) = plt.subplots(1, 2, figsize=(6, 3))

def draw_graph(ax, matrix_label):
    ax.grid()
    ax.set_xlabel('Matrix size $m \\times 16$ : $m$')
    ax.set_xlim([2**9, 2**25])
    ax.set_xscale('log', basex=2)
    ax.set_ylabel('residual of ' + matrix_label)
    ax.set_ylim(1e-6, 6.1e-2)
    ax.set_yscale('log')
    ax.set_yticks([1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2])
    ax.set_facecolor('white')

    background = patches.Rectangle(xy=(2**9, 1e-6), width=2**25, height=1, fc='#ffffff', fill=True)
    ax.add_patch(background)

    df = pd.read_csv('accuracy.csv')
    line_list = []
    label_list = []
    for d in data_list:
        data = df.query("compute_mode=='" + d + "'")
        l = ax.plot(data['m'], data[matrix_label], linewidth=2, marker='*', markersize=4, color=get_color(d), linestyle=get_linestyle(d))
        line_list += [l]
        label_list += [d]
    return line_list, label_list

draw_graph(ax0, 'Q')
line_list, label_list = draw_graph(ax1, 'R')

fig.legend(line_list,
        labels=label_list,
        loc='upper center',
        ncol=3,
        bbox_to_anchor=(1.14, 1.4),
        bbox_transform=ax0.transAxes
        )
plt.tight_layout()

plt.savefig("q_r_residual.pdf", bbox_inches="tight", transparent=True)

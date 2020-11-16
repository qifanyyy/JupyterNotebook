# -*- coding: utf-8 -*-
# @Author: Peter
# @Date:   2019-01-02 21:38:56
# @Last Modified by:   Peter
# @Last Modified time: 2019-01-06 15:33:52
import csv
import tkinter as tk

match_award = 1
mismatch_penalty = -1
gap_penalty = -1  # both for opening and extanding


def zeros(shape):
    """

    生成全零的形状为shape的二维矩阵

    Arguments:
        shape {tuple} -- 矩阵形状

    Returns:
        lsit -- 二维列表
    """
    retval = []
    for x in range(shape[0]):
        retval.append([])
        for y in range(shape[1]):
            retval[-1].append(0)
    return retval


def needleman_wunsch(seq1, seq2):
    """

    Needleman-Wunsch algorithm

    Arguments:
        seq1 {str} -- 待比较序列1
        seq2 {str} -- 待比较序列2

    Returns:
        int, str, str -- 返回seq1和seq2的相似度分数、seq1对齐结果以及seq2对齐结果
    """
    m, n = len(seq1), len(seq2)  # 序列长度

    score = zeros((m + 1, n + 1))

    for i in range(0, m + 1):
        score[i][0] = score_matrix[seq1[i - 1]]['-']
    for j in range(0, n + 1):
        score[0][j] = score_matrix['-'][seq2[j - 1]]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match = score[i - 1][j - 1] + score_matrix[seq1[i - 1]][seq2[j - 1]]
            delete = score[i - 1][j] + score_matrix[seq1[i - 1]]['-']
            insert = score[i][j - 1] + score_matrix['-'][seq2[j - 1]]
            score[i][j] = max(match, delete, insert)

    # 序列对齐
    align1, align2 = '', ''
    i, j = m, n  # 从右下角开始对齐
    while i > 0 and j > 0:
        score_current = score[i][j]
        score_diagonal = score[i - 1][j - 1]
        score_up = score[i][j - 1]
        score_left = score[i - 1][j]

        if score_current == score_diagonal + score_matrix[seq1[i - 1]][seq2[j - 1]]:
            align1 += seq1[i - 1]
            align2 += seq2[j - 1]
            i -= 1
            j -= 1
        elif score_current == score_left + score_matrix[seq1[i - 1]]['-']:
            align1 += seq1[i - 1]
            align2 += '-'
            i -= 1
        elif score_current == score_up + score_matrix['-'][seq2[j - 1]]:
            align1 += '-'
            align2 += seq2[j - 1]
            j -= 1

    # Finish tracing up to the top left cell
    while i > 0:
        align1 += seq1[i - 1]
        align2 += '-'
        i -= 1
    while j > 0:
        align1 += '-'
        align2 += seq2[j - 1]
        j -= 1
    return score[-1][-1], align1[::-1], align2[::-1]


def read_csv(filename):
    """

    读取csv到dict，模仿pandas库的read_csv函数

    Arguments:
        filename {str} -- 待读取的文件名

    Returns:
        dict -- 返回结果
    """
    reader = csv.reader(open(filename))
    head = next(reader)[1:]
    data = dict()
    for row in reader:
        row_data = [int(r) for r in row[1:]]
        temp = dict()
        for i, h in enumerate(head):
            temp[h] = row_data[i]
        data[row[0]] = temp
    return data


def view():
    """
    基于tkinter的可视化界面
    """
    width = 400  # 280
    height = 300  # 200
    root = tk.Tk()
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height,
                                (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(alignstr)    # 居中对齐
    root.title('基因序列比较')

    varSeq1 = tk.StringVar()
    varSeq1.set('')
    varSeq2 = tk.StringVar()
    varSeq2.set('')
    frame = tk.Frame()
    frame.pack(expand='yes')
    # 创建标签
    panelInput = tk.Label(frame)
    panelInput.pack()
    labelSeq1 = tk.Label(panelInput, text='基因序列一', justify=tk.RIGHT)
    # 将标签放到窗口上
    labelSeq1.grid(row=0, stick=tk.W, pady=10)
    # 创建文本框，同时设置关联的变量
    entrySeq1 = tk.Entry(panelInput, textvariable=varSeq1)
    entrySeq1.grid(row=0, stick=tk.E, pady=10, column=1)
    labelSeq2 = tk.Label(panelInput, text='基因序列二', justify=tk.RIGHT)
    labelSeq2.grid(row=1, stick=tk.W, pady=10)
    entrySeq2 = tk.Entry(panelInput, textvariable=varSeq2)
    entrySeq2.grid(row=1, stick=tk.E, pady=10, column=1)

    def compare():
        seq1 = varSeq1.get()
        seq2 = varSeq2.get()
        score, align1, align2 = needleman_wunsch(seq1, seq2)
        panelResult['text'] = align1 + '\n' + align2 + '\n\nscore:' + str(score)

    # 创建按钮组件，同时设置按钮事件处理函数
    panelBtn = tk.Label(frame)
    panelBtn.pack()
    buttonOk = tk.Button(panelBtn, text='序列比对', command=compare)
    buttonOk.grid(row=4, stick=tk.W, padx=20, pady=10)

    panelResult = tk.Label(frame, text='', font=20)
    panelResult.pack()
    root.mainloop()


if __name__ == '__main__':
    seq1 = 'AGTGATG'
    seq2 = 'GTTAG'
    score_matrix = read_csv('score.csv')
    score, align1, align2 = needleman_wunsch(seq1, seq2)
    print(score)
    print(align1)
    print(align2)
    # view()

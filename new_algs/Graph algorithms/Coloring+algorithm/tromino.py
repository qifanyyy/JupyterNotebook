# coding: utf-8
import time
import tkinter as tk


def tromino(a, x1, y1, length, x, y):
    """

    tromino算法：使用分治算法，将棋盘划分成四个象限，判断缺块位置，并进行递归

    Arguments:
        a {list} -- 二维棋盘
        x1 {int} -- 棋盘右上角x坐标
        y1 {int} -- 棋盘左上角y坐标
        length {int} -- 棋盘大小
        x {int} -- 缺块x坐标
        y {int} -- 缺块y坐标
    """
    global counter
    i = int(length / 2)  # int向下取整
    if i == 1:  # 当棋盘的长度的一半为1时开始解决问题
        if x <= x1 + i - 1 and y > y1 + i - 1:
            a[x1 + i - 1][y1 + i - 1] = a[x1 + i][y1 +
                                                  i - 1] = a[x1 + i][y1 + i] = counter
            counter += 1
        elif x <= x1 + i - 1 and y <= y1 + i - 1:
            a[x1 + i - 1][y1 + i] = a[x1 + i][y1 +
                                              i] = a[x1 + i][y1 + i - 1] = counter
            counter += 1
        elif x > x1 - 1 and y <= y1 + i - 1:
            a[x1 + i - 1][y1 + i - 1] = a[x1 + i -
                                          1][y1 + i] = a[x1 + i][y1 + i] = counter
            counter += 1
        else:
            a[x1 + i - 1][y1 + i - 1] = a[x1 + i - 1][y1 +
                                                      i] = a[x1 + i][y1 + i - 1] = counter
            counter += 1
    else:
        if x <= x1 + i - 1 and y > y1 + i - 1:
            a[x1 + i - 1][y1 + i - 1] = a[x1 + i][y1 +
                                                  i - 1] = a[x1 + i][y1 + i] = counter
            counter += 1
            tromino(a, x1, y1 + i, i, x, y)             # 解第一象限
            tromino(a, x1, y1, i, x1 + i - 1, y1 + i - 1)     # 解第二象限
            tromino(a, x1 + i, y1, i, x1 + i, y1 + i - 1)     # 解第三象限
            tromino(a, x1 + i, y1 + i, i, x1 + i, y1 + i)
        elif x <= x1 + i - 1 and y <= y1 + i - 1:
            a[x1 + i - 1][y1 + i] = a[x1 + i][y1 +
                                              i] = a[x1 + i][y1 + i - 1] = counter
            counter += 1
            tromino(a, x1, y1 + i, i, x1 + i - 1, y1 + i)         # 解第一象限
            tromino(a, x1, y1, i, x, y)                   # 解第二象限
            tromino(a, x1 + i, y1, i, x1 + i, y1 + i - 1)         # 解第三象限
            tromino(a, x1 + i, y1 + i, i, x1 + i, y1 + i)         # 解第四象限
        elif x > x1 - 1 and y <= y1 + i - 1:
            a[x1 + i - 1][y1 + i - 1] = a[x1 + i -
                                          1][y1 + i] = a[x1 + i][y1 + i] = counter
            counter += 1
            tromino(a, x1, y1 + i, i, x1 + i - 1, y1 + i)         # 解第一象限
            tromino(a, x1, y1, i, x1 + i - 1, y1 + i - 1)         # 解第二象限
            tromino(a, x1 + i, y1, i, x, y)                 # 解第三象限
            tromino(a, x1 + i, y1 + i, i, x1 + i, y1 + i)         # 解第四象限
        else:
            a[x1 + i - 1][y1 + i - 1] = a[x1 + i - 1][y1 +
                                                      i] = a[x1 + i][y1 + i - 1] = counter
            counter += 1
            tromino(a, x1, y1 + i, i, x1 + i - 1, y1 + i)         # 解第一象限
            tromino(a, x1, y1, i, x1 + i - 1, y1 + i - 1)         # 解第二象限
            tromino(a, x1 + i, y1, i, x1 + i, y1 + i - 1)         # 解第三象限
            tromino(a, x1 + i, y1 + i, i, x, y)               # 解第四象限


def drawboard(canvas, a, colors, startx=50, starty=50, cellwidth=50):
    """

    绘制方块

    Arguments:
        canvas {tkinter.canvas} -- tkinter canvas 句柄
        a {list} -- tromino谜题解矩阵
        colors {list} -- 颜色列表

    Keyword Arguments:
        startx {number} -- 起点x (default: {50})
        starty {number} -- 起点y (default: {50})
        cellwidth {number} -- 方块宽度 (default: {50})
    """

    width = 2 * startx + len(a) * cellwidth
    height = 2 * starty + len(a) * cellwidth
    canvas.config(width=width, height=height)

    canvas.create_rectangle(50 * (x + 1), 50 * (y + 1), 50 * (x + 2), 50 * (y + 2), fill='black',
                            outline='black')
    canvas.create_text(50 * (x + 1 + 0.5), 50 *
                       (y + 1 + 0.5), text='0', fill='white')
    canvas.update()
    time.sleep(0.5)
    max_value = int((len(a) * len(a) - 1) / 3)
    # x = 1
    for m in range(1, max_value + 1):
        for i in range(len(a)):
            for j in range(len(a)):
                if a[i][j] == m:
                    color = colors[m % len(colors)]
                    canvas.create_rectangle(50 * (i + 1), 50 * (j + 1), 50 * (i + 2), 50 * (j + 2),
                                            fill=color, outline='black')
                    canvas.create_text(50 * (i + 1.5), 50 *
                                       (j + 1.5), text=m, fill='white')
        time.sleep(0.1)
        canvas.update()


def view():
    """
    可视化界面：使用tkinter.canvas展示
    """
    root = tk.Tk()
    root.title("Tromino谜题")
    canvas = tk.Canvas(root, bg="white")
    canvas.pack()
    colors = ['red', 'orange', 'gray', 'green', 'blue', 'OliveDrab', 'Peru', 'Indigo', 'HotPink', 'OrangeRed', '#726dd1']
    drawboard(canvas, a, colors)
    root.mainloop()


def display_matrix(a):
    """
    打印矩阵
    Arguments:
        a {list} -- 待打印的矩阵
    """
    for item in a:
        print("\t".join([str(i) for i in item]))


if __name__ == '__main__':
    n = 2
    # x = 6
    # y = 2
    x = 1
    y = 1
    counter = 1
    length = 2**n
    a = [[0] * (length) for _ in range(length)]
    tromino(a, 0, 0, length, x, y)
    display_matrix(a)
    view()

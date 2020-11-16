# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 17:21:00 2018

@author: wmy
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from PIL import Image, ImageTk
import sys

# main window
window = tk.Tk()
window.title('Colour Selection Algorithm')
window.geometry('960x720')

# params init
path_1 = tk.StringVar()
path_2 = tk.StringVar()
state = tk.StringVar() 
state.set('正常')

# path select functions
def selectPath1():
    path = askopenfilename()
    path_1.set(path)
    pass

def selectPath2():
    path = askopenfilename()
    path_2.set(path)
    pass

# UI element
l1 = tk.Label(window, text='请选择第一张图片：', \
              font=('Arial', 12), width=16, height=2, justify=tk.LEFT)
l1.place(x=2+5)

l2 = tk.Label(window, text='请选择第二张图片：', \
              font=('Arial', 12), width=16, height=2, justify=tk.LEFT)
l2.place(x=2+5, y=50)

l3 = tk.Label(window, text='请输入N：', \
              font=('Arial', 12), width=16, height=2, justify=tk.LEFT)
l3.place(x=2+5, y=100)

e1 = tk.Entry(window, textvariable=path_1, width=60)
e1.place(x=190+5, y=15)

e2 = tk.Entry(window, textvariable=path_2, width=60)
e2.place(x=190+5, y=65)

e3 = tk.Entry(window, width=5)
e3.place(x=190+5, y=115)

b1 = tk.Button(window, text='选择文件', width=8, height=1, command=selectPath1)
b1.place(x=650+5, y=8) 

b2 = tk.Button(window, text='选择文件', width=8, height=1, command=selectPath2) 
b2.place(x=650+5, y=58) 

lp1 = tk.Label(window, width=128, height=64)
lp1.place(x=7, y=208)

lp2 = tk.Label(window, width=128, height=64)
lp2.place(x=7, y=288)

lp1c = tk.Label(window, width=640, height=64)
lp1c.place(x=160, y=208)

lp2c = tk.Label(window, width=640, height=64)
lp2c.place(x=160, y=288)

l4 = tk.Label(window, text='状态：', \
              font=('Arial', 12), width=8, height=2, justify=tk.LEFT)
l4.place(x=200, y=153)

lstate = tk.Label(window, textvariable=state, \
              font=('Arial', 12), width=50, height=1, justify=tk.LEFT, bg='#7FFF7F')
lstate.place(x=265, y=162)

l5 = tk.Label(window, text='色差阈值：', \
              font=('Arial', 12), width=10, height=2, justify=tk.LEFT)
l5.place(x=300, y=100)

e4 = tk.Entry(window, width=5)
e4.place(x=400, y=115)

# make images for single pix to 64x64
def make_image(theme):
    output = [[]]
    for pix in theme:
        for i in range(64):
            output[0].append(pix)
            pass
        pass
    for i in range(64):
        output.append(output[0])
        pass
    output = np.array(output)
    return output

def main():
    # get images
    image_1_path = e1.get()
    image_2_path = e2.get()
    try:
        image_1_RGB = plt.imread(image_1_path)
        image_2_RGB = plt.imread(image_2_path)
        num_colors = int(e3.get())
        color_tolerance = int(e4.get())
        pass
    except:
        state.set('ERROR')
        lstate.config(bg='#FF7F7F')
        window.update_idletasks()
        messagebox.showinfo(title='ERROR', message='输入错误!')
        return None
        pass
    # to lab
    lstate.config(bg='#7FFF7F')
    state.set('转换RGB为LAB中。。。')
    window.update_idletasks()
    image_1_LAB = cv2.cvtColor(image_1_RGB,cv2.COLOR_RGB2LAB)
    image_2_LAB = cv2.cvtColor(image_2_RGB,cv2.COLOR_RGB2LAB)
    # show image
    state.set('显示图片中。。。')
    window.update_idletasks()
    img_open = Image.open(e1.get())
    img = ImageTk.PhotoImage(img_open)
    lp1.config(image=img)
    lp1.image = img
    window.update_idletasks()
    # show image
    img_open = Image.open(e2.get())
    img = ImageTk.PhotoImage(img_open)
    lp2.config(image=img)
    lp2.image = img
    window.update_idletasks()
    # image 1
    state.set('第一张图片聚类中。。。')
    window.update_idletasks()
    km1 = KMeans(n_clusters=num_colors)
    h_1, w_1, c_1 = image_1_LAB.shape
    image_1_data = image_1_LAB.reshape((h_1*w_1, c_1))
    km1.fit(image_1_data)
    theme_1 = np.uint8(km1.cluster_centers_)
    # show image
    pic_array = cv2.cvtColor(theme_1.reshape(1, num_colors, 3),cv2.COLOR_LAB2RGB)
    pic_array = make_image(pic_array[0])
    pic = Image.fromarray(pic_array.astype('uint8')).convert('RGB')
    img = ImageTk.PhotoImage(pic)
    lp1c.config(image=img)
    lp1c.image = img
    window.update_idletasks()
    # image 2
    state.set('第二张图片聚类中。。。')
    window.update_idletasks()
    km2 = KMeans(n_clusters=num_colors)
    h_2, w_2, c_2 = image_2_LAB.shape
    image_2_data = image_2_LAB.reshape((h_2*w_2, c_2))
    km2.fit(image_2_data)
    theme_2 = np.uint8(km2.cluster_centers_)
    # show image
    pic_array = cv2.cvtColor(theme_2.reshape(1, num_colors, 3),cv2.COLOR_LAB2RGB)
    pic_array = make_image(pic_array[0])
    pic = Image.fromarray(pic_array.astype('uint8')).convert('RGB')
    img = ImageTk.PhotoImage(pic)
    lp2c.config(image=img)
    lp2c.image = img
    window.update_idletasks()
    state.set('聚类完成')
    window.update_idletasks()
    
    pass
    
# start button
b3 = tk.Button(window, text='开始选取', width=25, height=1, bg='#7F7FFF', command=main) 
b3.place(x=7, y=158) 

window.mainloop()

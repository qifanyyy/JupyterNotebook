# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 15:11:30 2018

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

window = tk.Tk()
window.title('Colour Selection Algorithm')
window.geometry('960x640')

path_1 = tk.StringVar()
path_2 = tk.StringVar()
state = tk.StringVar() 
state.set('正常')

def selectPath1():
    path_ = askopenfilename()
    path_1.set(path_)
    pass

def selectPath2():
    path_ = askopenfilename()
    path_2.set(path_)
    pass
    

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

def calcChromatism(c1, c2):
    deltaL = c1[0] - c2[0]
    deltaA = c1[1] - c2[1]
    deltaB = c1[2] - c2[2]
    deltaE = (deltaL**2 + deltaA**2 + deltaB**2)**0.5
    return deltaE

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
    image_1_path = e1.get()
    image_2_path = e2.get()
    try:
        image_1_RGB = plt.imread(image_1_path)
        image_2_RGB = plt.imread(image_2_path)
        num_colors = int(e3.get())
        pass
    except:
        state.set('ERROR')
        window.update_idletasks()
        messagebox.showinfo(title='ERROR', message='输入错误!')
        return None
        pass
    
    state.set('转换RGB为LAB中。。。')
    window.update_idletasks()
    print('转换RGB为LAB中。。。')
    image_1_LAB = cv2.cvtColor(image_1_RGB,cv2.COLOR_RGB2LAB)
    image_2_LAB = cv2.cvtColor(image_2_RGB,cv2.COLOR_RGB2LAB)
    
    img_open = Image.open(e1.get())
    img = ImageTk.PhotoImage(img_open)
    lp1.config(image=img)
    lp1.image = img
    window.update_idletasks()
    
    img_open = Image.open(e2.get())
    img = ImageTk.PhotoImage(img_open)
    lp2.config(image=img)
    lp2.image = img
    window.update_idletasks()
    
    state.set('第一张图片聚类中。。。')
    window.update_idletasks()
    print('第一张图片聚类中。。。')
    km1 = KMeans(n_clusters=num_colors)
    h_1, w_1, c_1 = image_1_LAB.shape
    image_1_data = image_1_LAB.reshape((h_1*w_1, c_1))
    km1.fit(image_1_data)
    theme_1 = np.uint8(km1.cluster_centers_)
    
    pic_array = cv2.cvtColor(theme_1.reshape(1, num_colors, 3),cv2.COLOR_LAB2RGB)
    pic_array = make_image(pic_array[0])
    pic = Image.fromarray(pic_array.astype('uint8')).convert('RGB')
    img = ImageTk.PhotoImage(pic)
    lp1c.config(image=img)
    lp1c.image = img
    window.update_idletasks()
    
    state.set('第二张图片聚类中。。。')
    window.update_idletasks()
    print('第二张图片聚类中。。。')
    km2 = KMeans(n_clusters=num_colors)
    h_2, w_2, c_2 = image_2_LAB.shape
    image_2_data = image_2_LAB.reshape((h_2*w_2, c_2))
    km2.fit(image_2_data)
    theme_2 = np.uint8(km2.cluster_centers_)
    
    pic_array = cv2.cvtColor(theme_2.reshape(1, num_colors, 3),cv2.COLOR_LAB2RGB)
    pic_array = make_image(pic_array[0])
    pic = Image.fromarray(pic_array.astype('uint8')).convert('RGB')
    img = ImageTk.PhotoImage(pic)
    lp2c.config(image=img)
    lp2c.image = img
    window.update_idletasks()
    state.set('聚类完成')
    window.update_idletasks()
    print('聚类完成')
    
    pass

b3 = tk.Button(window, text='开始选取', width=25, height=1, bg='#7F7FFF', command=main) 
b3.place(x=7, y=158) 

window.mainloop()

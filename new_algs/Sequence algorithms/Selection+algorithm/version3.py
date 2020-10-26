# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 19:26:56 2018

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
    # update the state
    lstate.config(bg='#7FFF7F')
    state.set('转换RGB为LAB中。。。')
    # resize to speed up
    image_1_RGB = Image.open(image_1_path)
    w_resize = 256
    h_resize = int(w_resize*image_1_RGB.size[1]/image_1_RGB.size[0])
    image_1_RGB = image_1_RGB.resize((w_resize, h_resize))
    image_1_RGB = np.array(image_1_RGB)
    # resize to speed up
    image_2_RGB = Image.open(image_2_path)
    w_resize = 256
    h_resize = int(w_resize*image_2_RGB.size[1]/image_2_RGB.size[0])
    image_2_RGB = image_2_RGB.resize((w_resize, h_resize))
    image_2_RGB = np.array(image_2_RGB)
    # to lab
    window.update_idletasks()
    image_1_LAB = cv2.cvtColor(image_1_RGB,cv2.COLOR_RGB2LAB)
    image_2_LAB = cv2.cvtColor(image_2_RGB,cv2.COLOR_RGB2LAB)
    #print(image_1_LAB.shape)
    #print(image_2_LAB.shape)  
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
    
    def calc_chromatism(lab1, lab2):
        deltaL = lab1[0] - lab2[0]
        deltaA = lab1[1] - lab2[1]
        deltaB = lab1[2] - lab2[2]
        deltaE = (deltaL**2 + deltaA**2 + deltaB**2)**0.5
        return deltaE
    
    # image 1 area
    image1_color_area = []
    state.set('计算图片一各颜色面积占比中。。。'+str(0)+'%')
    window.update_idletasks()
    for i in range(num_colors):
        num_same_pixs = 0
        L1 = int(theme_1[i][0]*100/255)
        A1 = int(theme_1[i][1]-128)
        B1 = int(theme_1[i][2]-128)
        LAB1 = [L1, A1, B1]
        for j in range(0, h_1*w_1, 2):
            L2 = int(image_1_data[j][0]*100/255)
            A2 = int(image_1_data[j][1]-128)
            B2 = int(image_1_data[j][2]-128)
            LAB2 = [L2, A2, B2]
            deltaE = calc_chromatism(LAB1, LAB2)
            if deltaE <= color_tolerance:
                num_same_pixs += 1
                pass
            pass
        area = num_same_pixs/(h_1*w_1)
        image1_color_area.append(area)
        state.set('计算图片一各颜色面积占比中。。。'+str(100*(i+1)/num_colors)+'%')
        window.update_idletasks()
        pass
    print(image1_color_area)
    
    # image 2 area
    image2_color_area = []
    state.set('计算图片二各颜色面积占比中。。。'+str(0)+'%')
    window.update_idletasks()
    for i in range(num_colors):
        num_same_pixs = 0
        L1 = int(theme_2[i][0]*100/255)
        A1 = int(theme_2[i][1]-128)
        B1 = int(theme_2[i][2]-128)
        LAB1 = [L1, A1, B1]
        for j in range(0, h_2*w_2, 2):
            L2 = int(image_2_data[j][0]*100/255)
            A2 = int(image_2_data[j][1]-128)
            B2 = int(image_2_data[j][2]-128)
            LAB2 = [L2, A2, B2]
            deltaE = calc_chromatism(LAB1, LAB2)
            if deltaE <= color_tolerance:
                num_same_pixs += 1
                pass
            pass
        area = num_same_pixs/(h_1*w_1)
        image2_color_area.append(area)
        state.set('计算图片二各颜色面积占比中。。。'+str(100*(i+1)/num_colors)+'%')
        window.update_idletasks()
        pass
    print(image2_color_area)
    
    state.set('面积占比计算完成')
    window.update_idletasks()
    
    pass

# start button
b3 = tk.Button(window, text='开始选取', width=25, height=1, bg='#7F7FFF', command=main) 
b3.place(x=7, y=158) 

window.mainloop()

# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 13:53:42 2018
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
from sklearn.cluster import DBSCAN
import operator

np.random.seed(1)

# std colors
std_colors = {'DG0546':[27.818, -8.375, 8.282],
              'DG0543':[27.818, -5.331, 10.061],
              'DG0647':[30.4, -5.075, 5.519],
              'DG0642':[30.4, -7.885, 8.605],
              'DG0648':[30.4, -5.77, 11.405],
              'DG0746':[32.963, -7.188, 8.464],
              'DG0744':[32.963, -6.138, 12.688],
              'DG0750':[32.963, -8.569, 15.102],
              'MG0851':[35.538, -11.055, 12.566],
              'MG0841':[35.538, -7.952, 14.866],
              'MG0850':[35.538, -9.978, 17.898],
              'MG1050':[38.146, -14.61, 17.02],
              'MG1048':[38.146, -10.562, 18.522],
              'MG1053':[38.146, -11.449, 22.008],
              'MG1151':[40.703, -15.986, 20.351],
              'MG1146':[40.703, -11.777, 22.669],
              'MG1148':[40.703, -13.409, 25.373],
              'MG1366':[43.316, -19.213, 25.02],
              'MG1350':[43.316, -13.546, 27.435],
              'MG1348':[43.316, -15.355, 31.017],
              'BG1548':[45.88, -13.519, 27.439],
              'BG1542':[45.88, -15.449, 30.991],
              'BG1544':[45.88, -16.916, 34.674],
              'BG1748':[48.448, -15.484, 30.905],
              'BG1743':[48.448, -16.958, 34.49],
              'BG1952':[50.978, -16.624, 34.363],
              'BG1955':[50.978, -13.52, 35.343],
              'BE0920':[35.538, 1.56, 11.939],
              'BE1225':[40.751, -0.638, 15.773],
              'BE1230':[40.751, 1.841, 12.319],
              'BE1528':[45.88, -0.581, 19.228],
              'BE1532':[45.88, 1.568, 15.512],
              'BE1824':[48.958, -0.873, 19.084],
              'BE1832':[48.958, 1.527, 15.373],
              'BE1928':[50.978, -1.116, 18.883],
              'BE1932':[50.978, 2.341, 19.65],
              'BE1935':[50.978, 4.142, 13.964],
              'RE1025':[38.656, 10.005, 14.867],
              'RE1328':[42.808, 15.233, 18.384],
              'RE1630':[46.922, 11.844, 12.337],
              'RE1632':[46.922, 14.823, 17.992],
              'YE1932':[50.978, 10.007, 26.137],
              'YE1937':[50.978, 13.167, 22.369],
              'YE2337':[55.031, 10.635, 30.011],
              'YE2344':[55.031, 13.063, 22.276],
              'YE2735':[59.067, 10.698, 29.749],
              'YE2740':[59.067, 12.998, 22.111],
              'YE3242':[63.011, 5.958, 31.797],
              'YE3245':[63.011, 10.535, 29.511],
              'YE3250':[63.011, 12.058, 37.976],
              'YE3755':[66.976, 6.043, 38.723],
              'YE3760':[66.976, 12.971, 42.748],
              'SE1932':[50.978, 4.193, 17.536], 
              'SE2335':[55.031, 5.348, 24.6],
              'SE2332':[55.031, 4.306, 17.658],
              'SE2740':[59.067, 5.314, 24.639],
              'SE2735':[59.067, 5.395, 16.822],
              'SE3445':[64.963, 1.838, 17.919],
              'SE3440':[64.963, 4.56, 13.035],
              'SE3945':[68.896, 2.123, 12.069],
              'SE3948':[68.896, 4.791, 17.37],
              'NB0407':[25.26, 1.158, -0.449],
              'NB0609':[30.40, 1.293, -0.479],
              'NB0911':[35.54, 1.472, -0.515],
              'NG1214':[40.751, 1.625, -0.58],
              'NG1517':[45.88, 1.751, -0.646],
              'NG1922':[50.978, 1.927, -0.682],
              'NG2427':[56.028, 2.044, -0.742],
              'NG2933':[61.045, 2.208, -0.784],
              'NG3538':[66.059, 2.343, -0.84],
              'NG4247':[70.871, 2.49, -0.888],
              'NG4954':[75.638, 2.611, -0.941],
              'NG5862':[80.516, 2.765, -0.988],
              'NW6770':[85.403, 2.888, -1.046], 
              'NW7780':[90.229, 3.043, -1.09],
              'NW8889':[95.077, 3.178, -1.137],
              'WR1216':[40.80, -7.59, 8.16],
              'WR2937':[61.05, -12.60, -5.57],
              'WR4250':[70.87, 4.97, 13.32],
              'WO0911':[35.52, -3.38, -12.29],
              'WO5363':[78.05, -10.48, -7.61],
              'CB1965':[50.978, -4.713, -16.964],
              'CB2980':[61.045, -12.131, -37.265],
              'CB4382':[71.214, -25.198, -25.499],
              'CY4970':[75.638, 18.525, 31.211],
              'CY6780':[85.352, 9.846, 18.865],
              'CY7785':[90.229, -5.577, 25.272],
              'CR1958':[50.978, 45.318, 32.692],
              'CR2260':[53.492, 44.555, 18.778],
              'CR2964':[61.045, 22.215, 7.098]}

data = []
label = []

for key, value in std_colors.items():
    data.append(value)
    label.append(key)
    pass

data = np.array(data)

def colour_classify(incolour, traindata, traincolour, k):
    '''训练的颜色个数'''
    #shape为numpy模块中的方法 shape[0]为矩阵第二维的长度
    trainsize = traindata.shape[0]
    #计算各个维度的差值并储存在向量diffmat中
    diffmat = np.tile(incolour, (trainsize,1)) - traindata
    #计算误差的平方
    squarediffmat = diffmat**2
    #计算向量间的欧式距离
    errordistance = squarediffmat.sum(axis=1)**0.5
    #排序
    sorteddistance = errordistance.argsort()
    classcount = {}
    for i in range(k):
        #选取前k个最符合要求的颜色
        selectedcolour = traincolour[sorteddistance[i]]
        classcount[selectedcolour] = classcount.get(selectedcolour,0)+1
        pass
    sortedclasscount = sorted(classcount.items(),
                              key=operator.itemgetter(1),reverse=True)
    return sortedclasscount[0][0]

def select_std_color(incolour):
    return colour_classify(incolour, data, label, 1)

# main window
window = tk.Tk()
window.title('Colour Selection Algorithm')
window.geometry('860x800')

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

e1 = tk.Entry(window, textvariable=path_1, width=72)
e1.place(x=190+5, y=15)

e2 = tk.Entry(window, textvariable=path_2, width=72)
e2.place(x=190+5, y=65)

b1 = tk.Button(window, text='选择文件', width=8, height=1, command=selectPath1)
b1.place(x=720+5, y=8) 

b2 = tk.Button(window, text='选择文件', width=8, height=1, command=selectPath2) 
b2.place(x=720+5, y=58) 

lp1 = tk.Label(window, width=128, height=64)
lp1.place(x=7, y=208)

lp2 = tk.Label(window, width=128, height=64)
lp2.place(x=7, y=288)

lp1c = tk.Label(window, width=640, height=64)
lp1c.place(x=160, y=208)

lp2c = tk.Label(window, width=640, height=64)
lp2c.place(x=160, y=288)

l5 = tk.Label(window, text='状态：', \
              font=('Arial', 12), width=8, height=2, justify=tk.LEFT)
l5.place(x=220, y=153)

lstate = tk.Label(window, textvariable=state, \
              font=('Arial', 12), width=50, height=1, justify=tk.LEFT, bg='#7FFF7F')
lstate.place(x=285, y=162)

l3 = tk.Label(window, text='聚类阈值：', \
              font=('Arial', 12), width=16, height=2, justify=tk.LEFT)
l3.place(x=7, y=100)

e3 = tk.Entry(window, width=5)
e3.place(x=190+5, y=115)

l4 = tk.Label(window, text='色差阈值：', \
              font=('Arial', 12), width=16, height=2, justify=tk.LEFT)
l4.place(x=360, y=100)

e4 = tk.Entry(window, width=5)
e4.place(x=480+5, y=115)

scrollbar = tk.Scrollbar(window)
scrollbar.place(x=808, y=368, height=368)

listbox = tk.Listbox(window, yscrollcommand=scrollbar.set, width=108, height=20)
listbox.place(x=48, y=368)

# make images for single pix to 64x64
def make_image(theme):
    output = [[]]
    for pix in theme:
        for i in range(32):
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
        color_tolerance = float(e4.get())
        cluster_tolerance = float(e3.get())
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
    window.update_idletasks()
    
    # show image
    state.set('显示图片中。。。')
    window.update_idletasks()
    img_open = Image.open(e1.get())
    img = img_open.resize((128, 64))
    img = ImageTk.PhotoImage(img)
    lp1.config(image=img)
    lp1.image = img
    window.update_idletasks()
    # show image
    img_open = Image.open(e2.get())
    img = img_open.resize((128, 64))
    img = ImageTk.PhotoImage(img)
    lp2.config(image=img)
    lp2.image = img
    window.update_idletasks()
    
    # resize to speed up
    image_1_RGB = Image.open(image_1_path)
    w_resize = 96
    h_resize = int(w_resize*image_1_RGB.size[1]/image_1_RGB.size[0])
    image_1_RGB = image_1_RGB.resize((w_resize, h_resize))
    image_1_RGB = np.array(image_1_RGB)
    # resize to speed up
    image_2_RGB = Image.open(image_2_path)
    w_resize = 96
    h_resize = int(w_resize*image_2_RGB.size[1]/image_2_RGB.size[0])
    image_2_RGB = image_2_RGB.resize((w_resize, h_resize))
    image_2_RGB = np.array(image_2_RGB)
    
    state.set('转换RGB为LAB中。。。')
    window.update_idletasks()
    image_1_LAB = cv2.cvtColor(image_1_RGB,cv2.COLOR_RGB2LAB)
    image_2_LAB = cv2.cvtColor(image_2_RGB,cv2.COLOR_RGB2LAB)
    
    # image 1
    state.set('第一张图片聚类中。。。')
    window.update_idletasks()
    dbscan1 = DBSCAN(eps=cluster_tolerance)
    h_1, w_1, c_1 = image_1_LAB.shape
    image_1_data = image_1_LAB.reshape((h_1*w_1, c_1))
    dbscan1.fit(image_1_data)
    labels = dbscan1.labels_
    n_clusters_1 = len(set(labels)) - (1 if -1 in labels else 0)
    # find the cluster center
    theme_1 = []
    for i in range(n_clusters_1):
        one_cluster = image_1_data[labels == i]
        km = KMeans(n_clusters=1, max_iter=600)
        km.fit(one_cluster)
        theme_1.append(np.squeeze(km.cluster_centers_))
        pass
    theme_1 = np.array(theme_1)
    # show image
    pic_array = cv2.cvtColor(np.uint8(theme_1.reshape(1, len(theme_1), 3)), cv2.COLOR_LAB2RGB)
    pic_array = make_image(pic_array[0])
    pic = Image.fromarray(pic_array.astype('uint8')).convert('RGB')
    img = ImageTk.PhotoImage(pic)
    lp1c.config(image=img)
    lp1c.image = img
    window.update_idletasks()
    
    # image 2
    state.set('第二张图片聚类中。。。')
    window.update_idletasks()
    dbscan2 = DBSCAN(eps=cluster_tolerance)
    h_2, w_2, c_2 = image_2_LAB.shape
    image_2_data = image_2_LAB.reshape((h_2*w_2, c_2))
    dbscan2.fit(image_2_data)
    labels = dbscan2.labels_
    n_clusters_2 = len(set(labels)) - (1 if -1 in labels else 0)
    # find the cluster center
    theme_2 = []
    for i in range(n_clusters_2):
        one_cluster = image_2_data[labels == i]
        km = KMeans(n_clusters=1, max_iter=600)
        km.fit(one_cluster)
        theme_2.append(np.squeeze(km.cluster_centers_))
        pass
    theme_2 = np.array(theme_2)
    # show image
    pic_array = cv2.cvtColor(np.uint8(theme_2.reshape(1, len(theme_2), 3)), cv2.COLOR_LAB2RGB)
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
    for i in range(n_clusters_1):
        num_same_pixs = 0
        L1 = theme_1[i][0]*100/255
        A1 = theme_1[i][1]-128
        B1 = theme_1[i][2]-128
        LAB1 = [L1, A1, B1]
        for j in range(0, h_1*w_1):
            L2 = image_1_data[j][0]*100/255
            A2 = image_1_data[j][1]-128
            B2 = image_1_data[j][2]-128
            LAB2 = [L2, A2, B2]
            deltaE = calc_chromatism(LAB1, LAB2)
            if deltaE <= color_tolerance:
                num_same_pixs += 1
                pass
            pass
        area = num_same_pixs/(h_1*w_1)
        image1_color_area.append(area)
        state.set('计算图片一各颜色面积占比中。。。'+str(int(100*(i+1)/n_clusters_1))+'%')
        window.update_idletasks()
        pass
    #print(image1_color_area)
    
    # image 2 area
    image2_color_area = []
    state.set('计算图片二各颜色面积占比中。。。'+str(0)+'%')
    window.update_idletasks()
    for i in range(n_clusters_2):
        num_same_pixs = 0
        L1 = theme_2[i][0]*100/255
        A1 = theme_2[i][1]-128
        B1 = theme_2[i][2]-128
        LAB1 = [L1, A1, B1]
        for j in range(0, h_2*w_2):
            L2 = image_2_data[j][0]*100/255
            A2 = image_2_data[j][1]-128
            B2 = image_2_data[j][2]-128
            LAB2 = [L2, A2, B2]
            deltaE = calc_chromatism(LAB1, LAB2)
            if deltaE <= color_tolerance:
                num_same_pixs += 1
                pass
            pass
        area = num_same_pixs/(h_2*w_2)
        image2_color_area.append(area)
        state.set('计算图片二各颜色面积占比中。。。'+str(int(100*(i+1)/n_clusters_2))+'%')
        window.update_idletasks()
        pass
    #print(image2_color_area)
    
    state.set('面积占比计算完成')
    window.update_idletasks()
    
    state.set('共同色选取中。。。')
    window.update_idletasks()
    common_color = []
    common_area = []
    common_uint8_lab = []
    common_color_A = []
    common_color_B = []
    for i in range(n_clusters_1):
        L1 = theme_1[i][0]*100/255
        A1 = theme_1[i][1]-128
        B1 = theme_1[i][2]-128
        LAB1 = [L1, A1, B1]
        for j in range(n_clusters_2):
            L2 = theme_2[j][0]*100/255
            A2 = theme_2[j][1]-128
            B2 = theme_2[j][2]-128
            LAB2 = [L2, A2, B2]
            deltaE = calc_chromatism(LAB1, LAB2)
            if deltaE <= color_tolerance:
                S1 = image1_color_area[i] / (image1_color_area[i] + image2_color_area[j])
                S2 = image2_color_area[j] / (image1_color_area[i] + image2_color_area[j])
                L3 = L1 * S1 + L2 * S2
                A3 = A1 * S1 + A2 * S2
                B3 = B1 * S1 + B2 * S2
                L1 = round(L1, 3)
                A1 = round(A1, 3)
                B1 = round(B1, 3)
                L2 = round(L2, 3)
                A2 = round(A2, 3)
                B2 = round(B2, 3)
                L3 = round(L3, 3)
                A3 = round(A3, 3)
                B3 = round(B3, 3)
                LAB1 = [L1, A1, B1]
                LAB2 = [L2, A2, B2]
                LAB3 = [L3, A3, B3]
                common_color_A.append(LAB1)
                common_color_B.append(LAB2)
                common_color.append(LAB3)
                common_area.append((image1_color_area[i], image2_color_area[j]))
                uint8_lab3 = [L3*255/100, A3+128, B3+128]
                common_uint8_lab.append(uint8_lab3)
                pass
            pass
        pass
    common_uint8_lab = np.uint8(common_uint8_lab)
    #print(common_color)
    #print(common_area)
    state.set('共同色选取完成')
    window.update_idletasks()
    
    title = ' '*22 + 'LAB' + ' '*(48-3) + 'A' + ' '*32 + 'B' + ' '*49 + 'Std Color'
    listbox.delete(0, tk.END)
    listbox.insert(tk.END, title)
    window.update_idletasks()
    
    result_info = []
    for i in range(len(common_color)):
        info = '{:4d}'.format(i+1) + ' '*4
        info += '[{:3.3f} {:3.3f} {:3.3f}]'.format(common_color[i][0], \
                 common_color[i][1], common_color[i][2])
        info += ' '*(36-len(info)) 
        info += '{:3.2f}'.format(100*common_area[i][0]) + '%' + ' '*4 
        info += '[{:3.3f} {:3.3f} {:3.3f}]'.format(common_color_A[i][0], \
                 common_color_A[i][1], common_color_A[i][2])
        info += ' '*(72-len(info))
        info += '{:3.2f}'.format(100*common_area[i][1]) + '%' + ' '*4 
        info += '[{:3.3f} {:3.3f} {:3.3f}]'.format(common_color_B[i][0], \
                 common_color_B[i][1], common_color_B[i][2])
        info += ' '*(108-len(info))
        selected_std_color = select_std_color(common_color[i])
        info += selected_std_color
        LAB1 = std_colors[selected_std_color]
        num_same_pixs = 0
        for n in range(0, h_1*w_1):
            L2 = image_1_data[n][0]*100/255
            A2 = image_1_data[n][1]-128
            B2 = image_1_data[n][2]-128
            LAB2 = [L2, A2, B2]
            deltaE = calc_chromatism(LAB1, LAB2)
            if deltaE <= color_tolerance:
                num_same_pixs += 1
                pass
            pass
        area_A = num_same_pixs/(h_1*w_1)
        num_same_pixs = 0
        for n in range(0, h_2*w_2):
            L2 = image_2_data[n][0]*100/255
            A2 = image_2_data[n][1]-128
            B2 = image_2_data[n][2]-128
            LAB2 = [L2, A2, B2]
            deltaE = calc_chromatism(LAB1, LAB2)
            if deltaE <= color_tolerance:
                num_same_pixs += 1
                pass
            pass
        area_B = num_same_pixs/(h_2*w_2)
        area = [round(100*area_A, 2), round(100*area_B, 2)]
        info += ' '*4 + '[{:3.2f}% {:3.2f}%]'.format(area[0], area[1])
        res = (common_color[i], common_area[i], common_color_A[i], common_color_B[i], selected_std_color)
        result_info.append(res)
        listbox.insert(tk.END, info)
        window.update_idletasks()
        pass
        
    scrollbar.config(command=listbox.yview)
    window.update_idletasks()
    
    pass

# start button
b3 = tk.Button(window, text='开始选取', width=25, height=1, bg='#7F7FFF', command=main) 
b3.place(x=7, y=158) 

# window mainloop
window.mainloop()

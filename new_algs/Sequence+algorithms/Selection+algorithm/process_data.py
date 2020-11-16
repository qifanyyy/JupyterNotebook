import os
import cv2
import pandas as pd
import numpy as np
import math
import random
from sklearn.utils import shuffle

# Global variable
root_path = '../jaffe'
# row start percent/ col start percent/ row width/ row length
feature_location = [
    [0, 0, 0.45, 0.45],
    [0, 0.55, 0.45, 0.45],
    [0, 0.3, 0.4, 0.2],
    [0.4, 0, 0.4, 0.4],
    [0.4, 0.6, 0.4, 0.4],
    [0, 0.42, 0.16, 0.6],
    [0.5, 0.4, 0.2, 0.2],
    [0.6, 0.35, 0.5, 0.25]
]

# help methods
def list_mean(t_list):
    sum = 0
    for i in t_list:
        sum += i
    mean = float(sum / len(t_list) )
    return float('%.4f'%mean)

def list_std(t_list):
    mean = list_mean(t_list)
    SSE = 0
    for i in t_list:
        residual = float(i - mean)
        SSE += residual ** 2
    std = math.sqrt(SSE)
    return float('%.4f'%std)

# Pick up features
def parser_feature_location(img_size):
    '''different shape of matrix should have different pixel located with same range of feature'''
    ret = []
    for location in feature_location:
        location_info = []
        for percent in location:
            info = int(percent * img_size)

            location_info.append(info)
        ret.append(location_info)
    return ret

def pick_feature(row_start,col_start ,width ,length , matrix):
    '''just need statistic do not row pixels    '''
    pixels = []
    feature_matrix = []
    for r in range(0, length):
        new_row = []
        for c in range(0, width):
            pixel = matrix[row_start + r][col_start + c]
            new_row.append(pixel)

            pixels.append(pixel)
        feature_matrix.append(new_row)

    ret = np.array(feature_matrix)
    return ret,pixels

def extract_features(img):
    feature_list = []
    img_size = len(img)
    feature_pixel_loacation = parser_feature_location(img_size-1)

    for info in feature_pixel_loacation:
        row,col, length, width = info[0], info[1], info[2], info[3]
        _,feature = pick_feature(row, col, length, width, img)
        mean, std = list_mean(feature), list_std(feature)
        feature_list.append(mean)
        feature_list.append(std)

    return feature_list

# feature processing, for each feature get the mean and std
def load_images():
    '''get each image save in different list'''

    emotions = os.listdir(root_path)
    labels,total_images = [],[]

    for idx,emotion in enumerate(emotions):
        labels.append(idx)
        images = []
        emotion_path = os.path.join(root_path,emotion)
        image_names = os.listdir(emotion_path)
        for image_name in image_names:
            image_path = os.path.join(emotion_path,image_name)
            image = cv2.imread(image_path)[:,:,0]
            images.append(image)
        total_images.append(images)
    return emotions,total_images,labels

def process_data():
    labels,img_data,_ = load_images()
    data_dict = {}
    data = []
    for i in range(17):
        data.append([])

    for idx,label in enumerate(labels):
        images = img_data[idx]
        for image in images:
            features = extract_features(image)
            for att_idx, feature in enumerate(features):
                data[att_idx].append(feature)
            data[16].append(label)

    for i in range(17):
        if i == 16:
            data_dict['label'] = data[16]
        else:
            data_dict['att%2i' % i] = data[i]

    df = pd.DataFrame(data_dict)
    data_full = df.copy()
    data_full['label'] = pd.factorize(df['label'])[0]
    data = data_full.copy().drop(['label'], axis=1)
    labels = data_full['label']

    return data,labels

def process_data_for_cnn():
    _,images,labels = load_images()
    train_data,train_labels,test_data,test_labels = [],[],[],[]
    for idx,label in enumerate(labels):
        e_images = shuffle(images[idx])
        train_size = len(e_images) - 7
        train_data += e_images[0:train_size]
        for i in range(train_size):
            train_labels.append(label)
        test_data += e_images[train_size:len(e_images)]
        for i in range(7):
            test_labels.append(label)

    return (np.array(train_data),np.array(train_labels)),(np.array(test_data),np.array(test_labels))



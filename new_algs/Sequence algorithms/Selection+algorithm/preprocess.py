import pandas as pd
import numpy as np
from sklearn import preprocessing
import os
from glob import glob

def get_dataframes(is_preprocess = True):
    PATH = os.path.join(os.getcwd(), 'Datasets')
    EXT = '*csv'
    all_csv_files = [file
                     for path, subdir, files in os.walk(PATH)
                     for file in glob(os.path.join(path, EXT))]
                     
    dataframes = []
    for csv_file in all_csv_files:
        df = pd.read_csv(csv_file, encoding='utf-8', header=None)
        if is_preprocess:
            df = preprocess(df)
        dataframes.append((csv_file, df))
    return dataframes

def preprocess(df):
    
    columns_to_remove = []
    columns_to_label_encode = []
    
    for col in df.columns:
        if df[col].nunique() == 1:
            columns_to_remove.append(col)
            continue
        if df[col].nunique() == df.shape[0]:
            columns_to_remove.append(col)
            continue
        if df[col].isna().astype(int).sum() > df.shape[0] * 0.4:
            columns_to_remove.append(col)
            continue
        if df[col].dtype == 'object':
            columns_to_label_encode.append(col)
    
    df = df.drop(columns_to_remove, axis=1)
    df = df.dropna()
    
    for col in columns_to_label_encode:
        le = preprocessing.LabelEncoder()
        df[col] = le.fit_transform(df[col]).astype(int)
    val = df.values #returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(val)
    df = pd.DataFrame(x_scaled, columns=df.columns)
    return df

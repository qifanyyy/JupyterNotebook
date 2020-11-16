import numpy as np
import pandas as pd
from sqlalchemy import create_engine

TRAIN_DATA = '_feature-extraction-min/train-arrays-min.csv'  # 'train-arrays.csv'
FEATURES = []


def reformat_array():
    """
    input: string like '[123 324 567]'
        * transform to a list
        * cast elements to integer
    :return:
    """
    return lambda x: [int(elem) for elem in x[1:-1].split()]


def read_big_data_train_data():
    for df in pd.read_csv(TRAIN_DATA, iterator=True, encoding='latin1', error_bad_lines=False, names=["index", "length", "array"], chunksize=10):
        df.to_sql('train_data', DATABASE, if_exists='append')
        features = feature_extraction(df)
        features.to_sql('train_features_data', DATABASE, if_exists='append')


def read_train_data():
    return pd.read_csv(TRAIN_DATA, encoding='latin1', error_bad_lines=False, names=["ID", "length", "array"])


def feature_extraction(df_train):
    df_train['array'] = df_train['array'].apply(reformat_array())

    for index, row in df_train.iterrows():
        array = np.array(row['array'])
        FEATURES.append({
            'index': row['index'],
            'length': len(array),
            'max': max(array),
            'min': min(array),
            'dist_min_max': max(array) - min(array),
            # Compute the weighted average along the specified axis.
            'average': np.average(array, axis=0),
            # Compute the arithmetic mean along the specified axis
            'mean': np.mean(array, axis=0),  # reduce(lambda x, y: x + y, array) / len(array),
            'q1': np.percentile(array, 25),
            'q2': np.percentile(array, 50),  # median
            'q3': np.percentile(array, 75),
            'std_deviation': np.std(array, axis=0),
            'variance': np.var(array, axis=0),

        })

    return pd.DataFrame(FEATURES)


DATABASE = create_engine('sqlite:///database2.db')
read_big_data_train_data()

print('The end')

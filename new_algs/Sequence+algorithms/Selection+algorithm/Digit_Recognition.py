import pandas as pd
import numpy as np
import datetime
import random
import matplotlib.pyplot as plt

from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import f1_score

seed = 1234
# Freeze the random seed
random.seed(seed)
np.random.seed(seed)


def load_data(filepath):
    data_dict = {}
    data = []
    for i in range(0,50):
        data.append([])

    with open(filepath,'r') as file:
        for line in file:
            values = line.strip().split()
            if len(values) == 50:
                for idx,value in enumerate(values):
                    data[idx].append(value)

    for i in range(0,50):
        if i == 49:
            data_dict['class'] = data[i]
        else:
            title = 'att%i' % (i)
            data_dict[title] = data[i]

    df = pd.DataFrame(data_dict)
    return df

def data_preprocessing(data):
    '''divide data into 50% of training'''
    data_full = data.copy()
    data = data_full.copy().drop(['class'], axis=1)
    labels = data_full['class']

    return data[0:500],labels[0:500],data[500:1000],labels[500:1000]

#predict models
def predict_MLP(train_data,train_labels,test_data):
    clas = MLPClassifier(hidden_layer_sizes=(30,),learning_rate_init=0.04,activation='relu')

    clas.fit(train_data, train_labels)
    predict, prob_predict = clas.predict(test_data), clas.predict_proba(test_data)
    return predict, prob_predict

def predict_KNN(train_data,train_labels,test_data):
    clas = KNeighborsClassifier(n_neighbors=7)
    clas.fit(train_data,train_labels)
    predict, prob_predict = clas.predict(test_data), clas.predict_proba(test_data)
    return predict, prob_predict

def main(filepath):
    # Step 1: Load Data
    data = load_data(filepath)

    # Step 2: Preprocess the data
    train_data, train_labels, test_data, test_labels = data_preprocessing(data)

    # Step 3: Learning Start
    # MLP
    start_time = datetime.datetime.now()  # Track learning starting time
    MLP_predict, MLP_prob_predict = predict_MLP(train_data,train_labels,test_data)
    end_time = datetime.datetime.now()  # Track learning ending time
    MLP_exection_time = (end_time - start_time).total_seconds()  # Track execution time

    # KNN
    start_time = datetime.datetime.now()  # Track learning starting time
    KNN_predict, KNN_prob_predict = predict_KNN(train_data, train_labels, test_data)
    end_time = datetime.datetime.now()  # Track learning ending time
    KNN_exection_time = (end_time - start_time).total_seconds()  # Track execution time

    # Step 4: Results presentation
    MLP_F1 = f1_score(test_labels,MLP_predict,average='weighted')
    KNN_F1 = f1_score(test_labels, KNN_predict, average='weighted')
    return MLP_F1,MLP_exection_time,KNN_F1,KNN_exection_time


if __name__ == '__main__':
    filepath = '../digits/digits'
    tasks = ['00','05','10' ,'15','20','30','40','50','60']

    MLP_F1s,MLP_time, KNN_F1s,KNN_time = [],[],[],[]
    for task in tasks:
        taskpath = filepath + task
        # Settings
        MLP_F1, MLP_exection_time,KNN_F1, KNN_exection_time = main(taskpath)
        print("Now in task noisy ratio = %s%% "%task )
        print('MLP F1= %.4f with %.4f sec' % (MLP_F1, MLP_exection_time))
        print('KNN F1= %.4f with %.4f sec' % (KNN_F1, KNN_exection_time))

        MLP_F1s.append(MLP_F1)
        MLP_time.append(MLP_exection_time)
        KNN_F1s.append(KNN_F1)
        KNN_time.append(KNN_exection_time)

    plt.plot(MLP_F1s, MLP_time, 'r--', label='MLP')
    plt.plot(KNN_F1s, KNN_time, 'g--', label='KNN')
    plt.xlabel('F1 Score')
    plt.ylabel('Time')
    plt.legend(loc='upper right')
    plt.savefig('../part2/result_graph.png')
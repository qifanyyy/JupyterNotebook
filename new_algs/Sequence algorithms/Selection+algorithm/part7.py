import numpy as np
import random
import pandas as pd
import os
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_selection import mutual_info_classif,chi2,RFE
from sklearn.metrics import f1_score
from sklearn.linear_model import SGDClassifier

seed = 422
random.seed(seed)
np.random.seed(seed)

#Global values
root = '../datasets'

def load_wbc_data():
    wbc_title = []
    for i in range(1, 31):
        wbc_title.append('feature%02.i'%i)
    wbc_title.append('label')
    wbc_dir = os.path.join(root, 'wbcd.data')
    df = pd.read_csv(wbc_dir,names=wbc_title)
    return df

def load_sonar_data():
    sonar_title = []
    for i in range(1, 61):
        sonar_title.append('feature%02.i' % i)
    sonar_title.append('label')
    sonar_dir = os.path.join(root, 'sonar.data')
    df = pd.read_csv(sonar_dir, names=sonar_title)
    return df

def data_preprocessing(df):
    data_full = df.copy()
    data_full['label'] = pd.factorize(df['label'])[0]
    data = data_full.copy().drop(['label'], axis=1)
    labels = data_full['label']
    return data,labels

def extract_features(df,attnames):
    '''extract feature by the attribute names'''
    data_full = df.copy()
    data = data_full.loc[:,attnames]
    return data

def NB_accuracy(X,Y):
    clf = GaussianNB()
    clf.fit(X, Y)
    score,f1score = clf.score(X,Y),f1_score(Y,clf.predict(X))
    return score,f1score

def find_top5_by_score(scores,labels):
    attnames,line = [],''
    for score, attname in sorted(zip(scores, labels[:30]), reverse=True)[:5]:
        attnames.append(attname)
        line += str(attname) + ' '
    return attnames,line

def wbc_main():
    wbc_data = load_wbc_data()
    wbc_values, wbc_labels = data_preprocessing(wbc_data)

    #Infomation Gain to select top 5 features
    info_scores = mutual_info_classif(wbc_values, wbc_labels)
    info_names,info_line = find_top5_by_score(info_scores, wbc_data.keys()[:30])
    print('TOP 5 features select using information Gain FOR WBC：')
    print(info_line)

    # chi2 to select top 5 features
    chi2_scores,_ = chi2(wbc_values, wbc_labels)
    chi2_attnames,chi2_line = find_top5_by_score(chi2_scores,wbc_data.keys()[:30])
    print('TOP 5 features select using chi-2 FOR WBC：')
    print(chi2_line)

    print('accuracy of whole features = %.4f, F1 score = %.4f' % NB_accuracy(wbc_values, wbc_labels))
    wbc_info_selected_values = extract_features(wbc_data, info_names)
    print('info -accuracy of TOP 5 features = %.4f, F1 score = %.4f'%NB_accuracy(wbc_info_selected_values,wbc_labels))
    wbc_chi2_selected_values = extract_features(wbc_data, chi2_attnames)
    print('Chi2 -accuracy of TOP 5 features = %.4f, F1 score = %.4f' % NB_accuracy(wbc_chi2_selected_values, wbc_labels))

def sonar_main():
    sonar_data = load_sonar_data()
    sonar_values, sonar_labels = data_preprocessing(sonar_data)

    # Infomation Gain to select top 5 features
    info_scores = mutual_info_classif(sonar_values, sonar_labels)
    info_names, info_line = find_top5_by_score(info_scores, sonar_data.keys()[:60])
    print('TOP 5 features select using information Gain FOR Sonar：')
    print(info_line)

    # chi2 to select top 5 features
    chi2_scores, _ = chi2(sonar_values, sonar_labels)
    chi2_attnames, chi2_line = find_top5_by_score(chi2_scores,  sonar_data.keys()[:60])
    print('TOP 5 features select using chi-2 FOR Sonar：')
    print(chi2_line)

    print('accuracy of whole features = %.4f, F1 score = %.4f' % NB_accuracy(sonar_values, sonar_labels))
    wbc_info_selected_values = extract_features(sonar_data, info_names)
    print(
        'info -accuracy of TOP 5 features = %.4f, F1 score = %.4f' % NB_accuracy(wbc_info_selected_values, sonar_labels))
    wbc_chi2_selected_values = extract_features(sonar_data, chi2_attnames)
    print(
        'Chi2 -accuracy of TOP 5 features = %.4f, F1 score = %.4f' % NB_accuracy(wbc_chi2_selected_values, sonar_labels))

def wbc_wrapper():
    wbc_data = load_wbc_data()
    wbc_values, wbc_labels = data_preprocessing(wbc_data)
    estimator = SGDClassifier(max_iter=1000)
    selector = RFE(estimator,5)
    selector.fit(wbc_values,wbc_labels)
    score, f1score = selector.score(wbc_values,wbc_labels), f1_score(selector.predict(wbc_values), wbc_labels)
    print('WBC-wrapper -accuracy of TOP 5 features = %.4f, F1 score = %.4f' % (score,f1score))

def sonar_wrapper():
    sonar_data = load_sonar_data()
    sonar_values, sonar_labels = data_preprocessing(sonar_data)
    estimator = SGDClassifier(max_iter=1000)
    selector = RFE(estimator,5)
    selector.fit(sonar_values, sonar_labels)
    score, f1score = selector.score(sonar_values, sonar_labels), f1_score(selector.predict(sonar_values), sonar_labels)
    print('Sonar-wrapper -accuracy of TOP 5 features = %.4f, F1 score = %.4f' % (score,f1score))

if __name__ == '__main__':

    wbc_main()
    print('')
    sonar_main()
    print('')
    wbc_wrapper()
    sonar_wrapper()
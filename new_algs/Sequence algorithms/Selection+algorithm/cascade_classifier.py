#!/usr/bin/python
import pandas as pd
import numpy as np
import pickle
import glob
import os

from sklearn.metrics import precision_recall_fscore_support, accuracy_score
from sklearn.datasets import load_svmlight_file
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
from scipy.sparse import csr_matrix

def apply_cascade(datasets_lists, original_dataset, folds=10):
    kf = StratifiedKFold(n_splits=folds, shuffle=True, random_state=0)
    k_scores, k_predicts, k_prob = [], [], []
    k_y, k_ft_import_lists = [], []
    X_data_all, y_data_all = original_dataset
    X_data_1, y_data_1 = datasets_lists[0]
    X_data_2, y_data_2 = datasets_lists[1]
    # Use the same folds as when using the original multi-class dataset
    for (train_idx, test_idx) in kf.split(X_data_all, y_data_all):
        # Firt step - BLS/RO-TS x MMASBI
        X_train_1, X_test_1 = X_data_1[train_idx], X_data_1[test_idx]
        y_train_1 = y_data_1[train_idx]
        clf1 = RandomForestClassifier(n_estimators=100, max_depth=10,
                                      random_state=0)
        clf1.fit(X_train_1, y_train_1)
        ft_import1 = clf1.feature_importances_
        pred_1 = clf1.predict(X_test_1)

        # Second step - BLS x RO-TS
        X_train_2, X_test_2 = X_data_2[train_idx], X_data_2[test_idx]
        y_train_2 = y_data_2[train_idx]
        clf2 = RandomForestClassifier(n_estimators=100, max_depth=10,
                                      random_state=0)
        clf2.fit(X_train_2, y_train_2)
        ft_import2 = clf2.feature_importances_
        pred_2 = clf2.predict(X_test_2)

        # Cascaded results
        y_test = y_data_all[test_idx]
        y_pred = []
        for p1, p2, y in zip(pred_1, pred_2, y_test):
            if p1 == 1:
                y_pred.append(p1)
            else:
                y_pred.append(p2)

        prob1 = np.array(clf1.predict_proba(X_test_1))
        part_prob = prob1[:,0]
        prob2 = np.array(clf2.predict_proba(X_test_2))
        prob = np.column_stack((part_prob * prob2[:,0], prob1[:,1]))
        prob = np.column_stack((prob, part_prob*prob2[:,1]))

        k_y.extend(y_test)
        k_predicts.extend(y_pred)
        k_prob.extend(prob)
        k_scores.append(accuracy_score(y_test, y_pred))
        k_ft_import_lists.append((ft_import1, ft_import2))
    return k_y, k_predicts, k_prob, k_scores, k_ft_import_lists


def save_log(log_filepath, results, features_list):
    with open(log_filepath, 'a') as log_file:
        for i, features in enumerate(features_list):
            line = 'Step: {} - Features: {}'.format(i, features)
            print(line)
            log_file.write(line + '\n')
        line = 'Accuracy: ' + str(accuracy_score(results[0], results[1]))
        print(line)
        log_file.write(line + '\n')
        line = 'Precision, Recall, FScore, Total:'
        print(line)
        log_file.write(line + '\n')
        line = str(precision_recall_fscore_support(results[0],
                                                    results[1]))
        print(line)
        log_file.write(line + '\n')
        print('-' * 50)
        log_file.write('-' * 50 + '\n')


def select_features(X_data, ft_importance_list=None, ft_idx=None, threshold=1):
    ft_labels = ['n', 'fd', 'dd', 'fsp', 'dsp', 'fas', 'das', 'n_opt',
                 'ils_dst', 'ils_fdc', 'bi_dst', 'bi_fdc', 'acc', 'acl']
    if ft_idx:
        labels_list = [ft_labels[i] for i in ft_idx]
    else:
        if not ft_importance_list:
            return X_data, ft_labels
        importances = np.array(ft_importance_list).mean(0)
        ft_idx, labels_list = [], []
        for i, ft_imp in enumerate(importances):
            if ft_imp > threshold:
                ft_idx.append(i)
                labels_list.append(ft_labels[i])

    df = pd.DataFrame(X_data.toarray())
    X_filtered = csr_matrix(pd.DataFrame(df, columns=ft_idx))
    return X_filtered, labels_list


def get_ft_idx(features_list):
    features = ['n', 'fd', 'dd', 'fsp', 'dsp', 'fas', 'das', 'n_opt',
                'ils_dst', 'ils_fdc', 'bi_dst', 'bi_fdc', 'acc', 'acl']
    idx_list = []
    for ft in features_list:
        idx_list.append(features.index(ft))
    return idx_list


datasets_best_features = {
    'dataset_bls+rots_mmasbi': ['fd', 'dd', 'dsp', 'n_opt', 'ils_fdc',
                                'bi_fdc'],
    'dataset_bls_rots': ['n', 'fsp', 'fas', 'n_opt']
}


datasets_names = [
    'dataset_bls+rots_mmasbi',
    'dataset_bls_rots'
]


def main():
    results_dir = 'cascade_results'
    os.system('mkdir -p {0}'.format(results_dir))
    log_filepath = '{0}/performance.log'.format(results_dir)
    results_filepath = '{0}/predicts.dat'.format(results_dir)
    f = open(log_filepath, 'w')
    f.close()
    labels_list = []
    original_dataset_filename = 'datasets/cleansed/dataset_bls_mmasbi_rots.dat'
    original_dataset = load_svmlight_file(original_dataset_filename)
    cascade_datasets = []
    for ds_name in datasets_names:
        ds_path = 'datasets/cascade/{}'.format(ds_name)
        dataset_filename = glob.glob(os.path.join(ds_path, '*.dat'))[0]
        X_data, y_data = load_svmlight_file(dataset_filename)
        best_ft_list = datasets_best_features[ds_name]
        columns = get_ft_idx(best_ft_list)
        X_data, labels = select_features(X_data, ft_idx=columns)
        cascade_datasets.append((X_data, y_data))
        labels_list.append(labels)
    results = apply_cascade(cascade_datasets, original_dataset)
    save_log(log_filepath, results, labels_list)
    with open(results_filepath, 'wb') as results_file:
        pickle.dump(results, results_file)


if __name__ == "__main__":
    main()

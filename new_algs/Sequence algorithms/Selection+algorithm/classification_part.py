'''
Copyright (C) <2015>  <Jorge Silva> <up201007483@alunos.dcc.fc.up.pt>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>

This work was partially supported by national funds through project VOCE 
(PTDC/EEA-ELC/121018/2010), and in the scope of R&D Unit UID/EEA/50008/2013, 
funded by FCT/MEC through national funds and when applicable cofunded
by FEDER/PT2020 partnership agreement.
'''

from __future__ import division

import math
import utils
import multiprocessing as mp
import numpy as np
import time

from collections import Counter

from sklearn import svm
from myClasses import ML_set
from myClasses import data_instance
from sklearn.cross_validation import KFold
from sklearn.metrics import confusion_matrix


def parallel_grid_search(settings, folds, data, features, estimate_g):
    n_tests = settings.grid_tests
    n_proc = settings.number_proc
    ##starts the parameters
    exps_c = [-7, -5, -3, -1, 1, 3, 5, 7, 9, 11, 13, 15]
    if estimate_g: ##in case we have to estimate g we define a range
        exps_g = [-13, -11, -9, -7, -5, -3, -1, 1, 3, 5, 7]
    else: ##in case we dont just define it already
        exps_g = [1]
    params_c = []
    params_g = []
    for e in exps_c:
        params_c.append(2**e)
    for e in exps_g:
        params_g.append(2**e)
    param_grid = [(x, y) for x in params_c for y in params_g]
    
    com = mp.Pipe()
    shared_lock = mp.Lock()
    
    larger_search = True ##first we will search with huge intervals as recomended on the paper then when a larger interval is found we will search on lower intervals inside that interval
    
    while (len(param_grid) != 1): ##while we dont have one set
        ##generates n random subsets
        subsets = utils.generate_random_sets(features, n_tests, 3, len(features))
        division_subsets = utils.divide_list(n_proc, subsets)

    
        ##parallelize work to it becomes faster
        workers = []
        for i in range(1, n_proc):
            p = mp.Process(target=grid_search, args=(i, division_subsets[i], folds, data, param_grid, shared_lock, com, settings.svm_kernel))
            workers.append(p)
            p.start()
    
        grid_search(0, division_subsets[0], folds, data, param_grid, shared_lock, com, settings.svm_kernel)
    
        for w in workers: ##hopefully this waits for every process to finish...
            w.join()
        
        output, input = com
        best_params = output.recv()
    
        if len(best_params) != n_tests: ##either we received the score of every feature or some error happened
            print "Didn't receive best param for every subset. ERROR"
            quit()
        
        param_grid, larger_search = get_top_selected(best_params, larger_search, estimate_g)
    ##returns c and gamma
    return param_grid[0][0], param_grid[0][1]
    
##returns the params that were selected most times
def get_top_selected(best_params, flag, estimate_g):
    c = Counter(best_params)
    aux = c.most_common(1)  ##get the param most selected
    times_sel = aux[0][1] ##get the times it was selected
    ##save all the parameters that were selected the most times
    param_top = []
    
    for param in c:
        if c[param] == times_sel:
            param_top.append(param)
    
    if len(param_top) > 1: ##more than one param was selected, make a test for all the top parameters
        return param_top, flag
    
    ##if only one parameter and we already completed the smal search then return the results
    if not flag:
        return param_top, flag
    else:
        #print Starting Smaller Search
        new_params_c = generate_smaller_search(param_top[0][0])
        if estimate_g: #in case we need to estimage g
            new_params_g = generate_smaller_search(param_top[0][1])
        else: #in case we dont
            new_params_g = [1]
        new_params = [(x, y) for x in new_params_c for y in new_params_g]
        return new_params, False
    
    
##generates the smaller search space for a parameter
def generate_smaller_search(val):
    n_values = 7 ##number of intervals to generate before the val plus 2
    used_exp = np.log2(val)
    search_space = []
    aux_1 = list(np.linspace(2**(used_exp-1), 2**used_exp, n_values))
    aux_2 = list(np.linspace(2**used_exp, 2**(used_exp + 1), n_values))
    
    ##append the first list
    for i in range(1, len(aux_1)-1):
        search_space.append(round(aux_1[i], 5))
    ##append second list, range is different cant do both on same for!!!
    for i in range(0, len(aux_2)-1):
        search_space.append(round(aux_2[i],5))
    
    return search_space
    
    


##function for each woker
def grid_search(id, subsets, folds, data, param_grid, lock, com, svm_kernel):
    best_params = []
    for subset in subsets:
        best_param = 0
        best_score = 0
        for cost, g in param_grid:
            st = time.time()
            score = classify(folds, data, subset, cost, g, svm_kernel)
            if score > best_score:
                best_score = score
                best_param = (cost, g)
            print "time to classify:", time.time() - st
        best_params.append(best_param)
    
    ##send results to main
    lock.acquire() ##mutual exclusion to grant coherency
    output, input = com
    if output.poll(): ##if it has a message
        msg = output.recv() ##add what already was there and append this process results
        best_params = msg + best_params
    input.send(best_params) ##send everything
    lock.release() ##release lock
            
        
        
        
    
    

    

##returns the index for k fold
def get_folds (size, k):
    ##If the data ordering is not arbitrary (e.g. samples with the same label are contiguous), 
    ##shuffling it first may be essential to get a meaningful cross- validation result. 
    ##this is the reason why we may not use the predefined function
    #kf = KFold(size, n_folds = k)
    
    ##my own kfold
    folds = []
    for i in range(0, k):
        folds.append([[],[]]) ## create lists to add
    f = 0
    for i in range(0, size):  ##create folds, each fold receive a feature periodically
        for j in range(0, k):
            if j == f:
                folds[j][1].append(i)
            else:
                folds[j][0].append(i)
        f = (f + 1) % k
    kf = []
    for fold in folds:
        kf.append((fold[0], fold[1]))
    return kf

def classify_final_test(data, features, data_to_classify, cost, g, svm_kernel):
    ##make all data becoming part of the training
    train_set, _ = utils.cut_dataset(range(len(data)), [], data, features)
    _, test_set = utils.cut_dataset([], range(len(data_to_classify)), data_to_classify, features)
    
    if svm_kernel == "linear":
        clf = svm.LinearSVC(C=cost) #used for gissete and madelon
    else:
        clf = svm.SVC(C=cost, gamma=g, kernel='rbf')  
    #
    clf.fit(train_set.fts_values, train_set.fts_pred)
    predictions = clf.predict(test_set.fts_values)
    preds = []
    for i in predictions:
        #print i
        preds.append(int(i))
    return preds




def classify(folds, data, features, cost, gamma, svm_kernel):
    ##train_set, test_set = utils.cut_dataset(n_train, n_test, data, test_subset.features) ##get the features for the subset
    scores = []
    for fold in folds: ##run a classification for each fold
        train, test = fold ##division of data on that fold
        train_set, test_set = utils.cut_dataset(train, test, data, features)
        ##print train_set.fts_pred, test_set.fts_pred
        score = classification_svm(train_set, test_set, cost, gamma, svm_kernel)
        if math.isnan(score):
            #print "nan score"
            score = 0
        scores.append(score)
    
     #print scores
    final_score = sum(scores) / float(len(scores))
    return final_score



def get_sens_and_spec(label_true, label_pred):
    conf_matrix = confusion_matrix(label_true, label_pred)
    #print conf_matrix
    sens = conf_matrix[0][0] / (float(conf_matrix[0][0] + conf_matrix[1][0])) ##calculates sensitivity
    spec = conf_matrix[1][1] / (float(conf_matrix[1][1] + conf_matrix[0][1])) ##calculates specificity
    

    score_1 = 1 - abs(spec - sens)
    score_2 = (spec + sens) / 2
    #return (spec * sens) / (abs(spec - sens)) 
    final_score = score_1 + score_2
    #print "sens: ", sens, " spec: ", spec, " final score: ", final_score
    return round (final_score,4)


def get_hmean(label_true, label_pred):
    ##get accuracy
    #score = check_accuracy_rate(label_pred, label_true)
    ##get score based on specificity and sensitivity
    #score = get_sens_and_spec(label_true, label_pred)

    epsilon=0.00000000001
    cm = confusion_matrix(label_true, label_pred)
    #precision=TP/(TP+FP)
    precision=float(cm[1,1])/(cm[1,1]+cm[0,1]+epsilon)

    #recall=TP/(TP+FN)
    recall=float(cm[1,1])/(cm[1,1]+cm[1,0]+epsilon)

    score=np.sqrt(precision*recall)

    return score


def get_score(label_true, label_pred):
    ##get accuracy
    #score = check_accuracy_rate(label_pred, label_true)
    ##get score based on specificity and sensitivity
    #score = get_sens_and_spec(label_true, label_pred)
    score = get_hmean(label_true, label_pred)
    return score
    
    


def classification_svm (train_set, test_set, cost, g, svm_kernel): ##train a classifier and returns its error rate
    #st = time.time()
    if svm_kernel == "linear":
        clf = svm.LinearSVC(C=cost)
    else:
        clf = svm.SVC(C=cost, gamma=g, kernel='rbf')
    #clf = svm.LinearSVC(C=cost) #used for gissete and madelon
    clf.fit(train_set.fts_values, train_set.fts_pred)
    predictions = clf.predict(test_set.fts_values)
    preds = []
    for i in predictions:
        #print i
        preds.append(int(i))
    ##in case you dont want to use accuracy as the score metric change the following function to return another score
    return get_accuracy_rate(test_set.fts_pred, preds) 
    
                
##calculates the accuracy rate
def get_accuracy_rate(real, pred):
    error_count = 0
    if len(real) != len(pred):
        print "NOT SAME SIZE ON REAL AND PRED VALUES WHILE GETTING ACCURACY RATE"
        quit()
        
    total = float(len(real))
    for i in range(0,len(pred)):
        #print pred[i], " ", real[i]
        if int(pred[i]) != int(real[i]):
            error_count += 1
    error_rate = round(error_count / total, 8)
    #print error_count, " ", error_rate, " ", total
    accuracy = 1 - error_rate
    return round((accuracy * 100),2)
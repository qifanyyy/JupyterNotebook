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

import multiprocessing as mp
import time
from myClasses import ML_set
from myClasses import data_instance
from myClasses import Method_settings
from myClasses import ML_subset
import utils
import classification_part
import random

##generates the probability of each feature improving
def generate_probabilities(settings, features, data, folds, p_work_list, cost, gamma):
    n_proc = settings.number_proc
    ###generate the probability vector
    if settings.estimate_probs:
        com = mp.Pipe()
        share_lock = mp.Lock()
        
        get_improve_prob(features, settings.prob_tests, data, folds, n_proc, p_work_list, share_lock, com, cost, gamma, settings.svm_kernel)
        
        ##gather output
        output, _ = com
        aux = output.recv() ##receive probabilities from the pipe
        if len(aux) != len(features):
            print "ERROR CALCULATING PROBABILITIES"
            quit()
        
        ##convert the list to a dict
        probs = {}
        for p in aux:
            probs[p[0]] = p[1]
    else:
        probs = {} 
    return probs


##receives the features, the number of tests, the datasets the division into train and test, the number of processes and the division of features for proceeses
def get_improve_prob(features, n_tests, dataset, folds, n_proc, p_features, shared_lock, com, cost, gamma, svm_kernel):
    test_sets = utils.generate_random_sets(features, n_tests, 3, 10)
    accs = []
    for test in test_sets:  ##test each dataset agaisnt the classifier
        acc = classification_part.classify(folds, dataset, test, cost, gamma, svm_kernel)
        accs.append(acc)
    ##split tests among processes
    #print "accuracies subsets:", acc
    workers = []
    for i in range(1, n_proc):
        p = mp.Process(target=calculate_improve_prob, args=(i, p_features[i], dataset, test_sets, accs, folds, shared_lock, com, cost, gamma, svm_kernel))
        workers.append(p)
        p.start()
    
    calculate_improve_prob(0, p_features[0], dataset, test_sets, accs, folds, shared_lock, com, cost, gamma, svm_kernel)
    
    for w in workers:
        w.join()
    return
    
def calculate_improve_prob(id, my_features, dataset, test_sets, accuracies, folds, lock, com, cost, gamma, svm_kernel):
    ##my_features returns a list with ml subsets, its easier if we pass all of them to a list of fts
    fts = []
    for i in my_features:
        fts.append(i.features)
    
    probs = []
    for ft in fts: ##for every feature test against every subset
        improvements = 0
        for i in range(0, len(test_sets)):
            new_set = list(test_sets[i])
            if ft in new_set: ##if ft was already on set remove it and check if the accuracy got worse
                new_set.remove(ft)
                added = False
            else: ## if ft was not on the dataset check if accuracy improved
                new_set = new_set + ft
                added = True
            #print new_set
            acc = classification_part.classify(folds, dataset, new_set, cost, gamma, svm_kernel)
            if added:
                if acc > accuracies[i]:
                    improvements += 1
            else:
                if acc < accuracies[i]:
                    improvements += 1
            #print "obtained acc:", acc, "other acc:", accuracies[i], improvements
            
        prob = round((improvements / float(len(test_sets))), 2)
        probs.append((ft[0], prob))
    ##send results to pipe
    lock.acquire()
    output, input = com
    if output.poll():
        msg = output.recv() ##add what already was there and append this process results
        probs = msg + probs
    input.send(probs)
    lock.release()
        

def sampling(work_list, best_score): ##cut work list with a percentage
    st = time.time()
    new_work_list = []
    for w in work_list:
        solution_score = w.parents_scores[-1]
        perc_difference = (best_score - solution_score) / best_score
        perc_difference = round(perc_difference * 100, 2)
        prob_cut = 0
        ##estimate prob
        #print "solution_score: ", solution_score, "diff:", perc_difference, "best:", best_score
        if perc_difference <= 0.50: ##tested solution is near the best score
            prob_cut = 0
        elif perc_difference <= 1.00:
            prob_cut = 25
        elif perc_difference <= 1.50:
            prob_cut = 50
        else:
            prob_cut = 75
        
        ##get a random
        r = random.randint(0,100)
        if prob_cut <= r:
            new_work_list.append(w)
        
    print "received", len(work_list), "took ", time.time() - st, " size list returned ", len(new_work_list)
    
    
    return new_work_list

                    
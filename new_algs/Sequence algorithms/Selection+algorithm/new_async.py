from __future__ import division
import multiprocessing as mp
import time
import pandas as pd
import numpy as np
import sys
import utils
#from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier

from ML_test import ML_test 
from ML_data import ML_instance


max_search_level = 50
expansions_per_worker = 1
expansions_per_level = 5
min_share_work = 3

score_lock = 0
work_lock = 1
total_locks = 2

debug = True

def starter(work, ml_instance, n_workers):
    t = time.time()
    manager = mp.Manager() ##manager creates a new process to handle variables, may not be the best option  
    ##setup for paralelization
    
    locks = []
    for i in range(total_locks):
        locks.append(mp.Lock())
    
    global_info = manager.Namespace() ##manager for variables
    global_info.history = {} ##saves the history
    global_info.expanded_history = []
    global_info.best_scores = {}
    global_info.worklist = work
    
    workers = []

    for i in range (n_workers-1):
        p = mp.Process(target=search, args=(i, locks, ml_instance, global_info)) ##cant pass arguments to evaluator
        workers.append(p)
        p.start()
        
    search(n_workers-1, locks, ml_instance, global_info)
        
    for w in workers:
        w.join()
        
    print "Total time, ", time.time() - t, " tested a total of:", len(global_info.history)
    tester = ML_test()
    tester.history = global_info.history
    tester.save_history(filename="history_async")
    df = pd.DataFrame()
    df["expanded"] = global_info.expanded_history
    df.to_csv("expanded_async.csv", index = False)
    
def update_score(id, subset, score, lock, global_info):
    size = len(subset)
    lock.acquire()
    aux = global_info.best_scores
    if size not in aux:
        aux[size] = []
    if len(aux[size]) < 8 or aux[size][-1][0] < score :
        aux[size].append((score, subset))
    aux[size] = sorted(aux[size], key=lambda tup: tup[0])
    aux[size].reverse()
    aux[size] = aux[size][:8]    
    global_info.best_scores = aux
    lock.release()
    
def expand_stage(id, global_info, ml_instance, score_lock, current_size ):
    t = time.time()
    print id, " nominated to generate work for current_size ", current_size
    if current_size == max_search_level:
        print id , " determined its time to end search"
        aux = []
        for i in range(50): ##append 50 subsets greater than max search level so everyone stops
            aux.append(range(max_search_level+3))
        global_info.worklist = list(aux)
        return
    score_lock.acquire()
    subsets_to_expand = global_info.best_scores[current_size][:expansions_per_level]
    work = []
    hist = global_info.history
    exp_hist = global_info.expanded_history
    for s in subsets_to_expand:
        subset = s[1]
        exp_hist.append(subset)
        for i in ml_instance.features:
            if i not in subset:
                sub = subset + [i]
                sub.sort()
                aux = [str(x) for x in sub]
                aux = ",".join(aux)
                if aux not in hist:
                    work.append(sub) ##add subset for next round
                    hist[aux] = True ##add subset to the testing
    print id, " genereated ", len(work), " new subsets in ", round(time.time() - t, 3), " seconds" 
    global_info.history = hist
    global_info.expanded_history = exp_hist
    global_info.worklist = list(work)
    score_lock.release()
    
    
def search(id, locks, ml_instance, global_info):
    tasks = 0
    task_time = []
    start_t = time.time()
    current_size = 1
    worklist_waste = 0.0
    update_waste = 0.0
    while (True):
        ##mutual exclusion lock to get a subset from worklist
        aux_t = time.time()
        locks[work_lock].acquire()
        worklist_waste += (time.time() - aux_t)
        if global_info.worklist == []:
            expand_stage(id, global_info, ml_instance, locks[score_lock], current_size) ##acquires both locks to prevent strange stuff on the scores
        aux = list(global_info.worklist)
        subset = aux[0]
        del(aux[0])
        global_info.worklist = aux
        locks[work_lock].release()
        
        if tasks % 4 == 0: ##periodicall print
            print id, " processed ", tasks, " remaining work ", len(aux)
            
        if len(subset) > max_search_level: ##search ends
            break
        current_size = len(subset)
        tasks += 1
        t = time.time()
        score = ml_instance.rf_evaluator(subset)
        #score = ml_instance.svm_evaluator(subset)
        
        task_time.append(round(time.time()-t, 2))
        t = time.time()
        update_score(id, subset, score, locks[score_lock], global_info)
        update_waste += (time.time() -t)
    print id, " ending processing ", tasks, " in ", round(time.time()-start_t,0), " seconds"
    print id, " wasted in worklist access ", round(worklist_waste,2), " updating ", round(update_waste,2), " average task time", round(sum(task_time) / len(task_time),2)
        
        
    
    
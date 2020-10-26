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
share_lock = 1
work_lock = 2
total_locks = 3

debug = True

def starter(work, ml_instance, n_workers):
    t = time.time()
    manager = mp.Manager() ##manager creates a new process to handle variables, may not be the best option  
    work_division =  utils.divide_list(n_workers+1, work)
    
    ##setup for paralelization
    
    locks = []
    for i in range(total_locks):
        locks.append(mp.Lock())
    
    global_info = manager.Namespace() ##manager for variables
    global_info.history = {} ##saves the history
    global_info.best_scores = {}
    global_info.search_level = 1
    global_info.expanded_history = {}
    global_info.amount_of_work = [0] * n_workers 
    global_info.public_work = []
    global_info.left_to_change = n_workers - expansions_per_level
    
    pipes = []
    for i in range(n_workers):
        c = mp.Pipe()
        pipes.append(c)
    
    workers = []

    for i in range (n_workers-1):
        p = mp.Process(target=search, args=(i, work_division[i], ml_instance, global_info, pipes, locks)) ##cant pass arguments to evaluator
        workers.append(p)
        p.start()
        
    search(n_workers-1, work_division[n_workers], ml_instance, global_info, pipes, locks)
        
    for w in workers:
        w.join()
        
    print "Total time, ", time.time() - t, " tested a total of:", len(global_info.history)
    tester = ML_test()
    tester.history = global_info.history
    tester.save_history(filename="history_async")
    expanded = []
    for i in global_info.expanded_history:
        for j in global_info.expanded_history[i]:
            expanded.append(j)
    df = pd.DataFrame()
    df["expanded"] = expanded
    df.to_csv("expanded_async.csv", index = False)
    
def update_score(subset, score, score_lock, global_info, lowest_score):
    if score > lowest_score:
        round_size = len(subset)
        score_lock.acquire()
        scores = global_info.best_scores
        if round_size not in scores:
            scores[round_size] = []
        scores[round_size].append([score, subset, 0])
        scores[round_size] = sorted(scores[round_size], key=lambda tup: tup[0])
        scores[round_size].reverse()
        scores[round_size] = scores[round_size][:10]
        lowest_score = scores[round_size][-1][0]
        global_info.best_scores = scores
        score_lock.release()
    return lowest_score

def check_for_work(id, work, pipes):
    my_1, my_2 = pipes[id]
    
    if my_1.poll():        
        asker = my_1.recv()
        asker = int(asker)
    
        print id, " sharing work with ", asker
        new_work = utils.divide_list(2, work)
        my_1.send(new_work[1])
        return new_work[0]
    return work

def ask_for_work(my_id, pipes, id_to_ask):
    print my_id, "asking for work to " , id_to_ask
    #com_in, com_out = pipes[id_to_ask]
    #my_in, my_out = pipes[my_id]
    com_1, com_2 = pipes[id_to_ask]
    #com_in.send(my_id)
    com_2.send(my_id)
    work = com_2.recv()
    print my_id, "received ", len(work)
    return work

def expand_subset(subset, global_info, ml_instance):
    hist = global_info.history
    aux = ml_instance.generate_successors(subset, hist)
    global_info.history = hist
    return aux

def expand_to_next_stage(id, current_size, global_info, score_lock, ml_instance):
    print id, " expanding to next stage ", current_size, " global ", global_info.search_level
    n_fts = len(ml_instance.features)
    t = time.time()
    score_lock.acquire()
    if global_info.search_level == current_size: ## if we are the first then increase global search level
        global_info.search_level = current_size + 1
    
    exp_hist = global_info.expanded_history
    if global_info.search_level not in exp_hist: ##if record for the level doesnt exist then create, could merge this with the increment
        exp_hist[global_info.search_level] = []
    
    if len(exp_hist[global_info.search_level]) >= expansions_per_level: ##alreadu expanded enough subsets
        print id, " No more expansions"
        work = []
    else:
        work = []
        scores = global_info.best_scores
        for i in range(0,expansions_per_worker): #3how many subsets each woerkers expands
            for j in range(0, len(scores[current_size])):
                if scores[current_size][j][2] == 0:
                    scores[current_size][j][2] = 1
                    aux = expand_subset(scores[current_size][j][1], global_info, ml_instance)
                    exp_hist[global_info.search_level].append(scores[current_size][j][1])
                    work = work + aux
                    break ##otherwirse it will expand most of the subsets
        n_workers = len(global_info.amount_of_work)
        my_part = int(((n_fts - current_size) * expansions_per_level) / n_workers)
        aux = list(work)
        work = list(aux[:my_part])
        global_info.public_work += aux[my_part:]
        global_info.best_scores = scores
        print id, " created ", len(work), " to him, to list: ", len(aux[my_part:]), " total: ", len(global_info.public_work)
        #print id, " created ", len(work), " for him and " , len(aux)  new subsets by expanding: ", scores[current_size][j][1]
        
    global_info.expanded_history = exp_hist
    #print id, " expanded subsets" , len(global_info.expanded_history)
    score_lock.release()
    return work, round(time.time()-t, 2)

##verifies if any  worker is overloaded and if that's the case ask it for work
def check_if_overloaded(id, global_info, share_lock, pipes):   
    max_work = max(global_info.amount_of_work)
    print global_info.amount_of_work
    work = []
    w_t = 0.0
    if max_work > min_share_work: ##adjust here if required
        t = time.time()
        share_lock.acquire()
        if max(global_info.amount_of_work) > min_share_work: ##verify if still need to ask for work
            index = global_info.amount_of_work.index(max(global_info.amount_of_work))
            print id, " asking to share ", index, " size of work ", max_work
            work = ask_for_work(id, pipes, index)
            
        share_lock.release()
        w_t = round(time.time()-t, 2)
    return work, w_t

##verifies if theres unassigned public work
def check_unassigned_work(id, global_info, current_size, n_fts, score_lock):
    t = time.time()
    score_lock.acquire()
    work = []
    if global_info.public_work != []:
        n_workers = len(global_info.amount_of_work)
        global_info.left_to_change -= 1
        if global_info.left_to_change == 0: #last process must take all the list
            print id, " was last id in list "
            work = list(global_info.public_work)
            global_info.public_work = []
            global_info.left_to_change = n_workers - expansions_per_level
        else:
            my_part = int(((n_fts - current_size) * expansions_per_level) / n_workers) 
            aux = global_info.public_work
            work = list(aux[:my_part])
            remaining = list(aux[my_part:])
            global_info.public_work = remaining
        print id, " got work from public list ", len(work), " work left", len(global_info.public_work), " ids left: ", global_info.left_to_change 
            
    score_lock.release()
    return work, round(time.time() - t, 3)        
            
        

def check_next_state(id, current_size, global_info, pipes, locks, ml_instance):
    w_t = 0
    e_t = 0
    if (current_size < global_info.search_level): ##if someone already moved to next stage
        if current_size >= max_search_level: ##stop search condition
            return [], False, max_search_level + 1, w_t, e_t
        work, e_t = expand_to_next_stage(id, current_size, global_info, locks[score_lock], ml_instance)
        current_size = global_info.search_level
    else: ##nobody moved lets see if there is any work left for this level
        work, e_t = check_unassigned_work(id, global_info, current_size, len(ml_instance.features), locks[score_lock]) ##check if unassigned work
        if work != []:
            return work, True, current_size, w_t, e_t
        work, w_t = check_if_overloaded(id, global_info, locks[share_lock], pipes) ## check if some worker is overloaded
        if work != []:
            return work, True, current_size, w_t, e_t
        ##if there is no unassigned work and there is nobody overloaded lets expand to next stage
        work, e_t = expand_to_next_stage(id, current_size, global_info, locks[score_lock], ml_instance) 
        current_size = global_info.search_level
    return work, True, current_size, w_t, e_t    
            

def update_amount_of_work(id, global_info, work, locks):
    locks[work_lock].acquire()
    am = global_info.amount_of_work
    am[id] = len(work)
    global_info.amount_of_work = am
    locks[work_lock].release()

def search(id, work, ml_instance, global_info, pipes, locks):
    print id, " just started"
    task_time = []
    tasks = 0
    start_t = time.time()
    shared_time = 0.0
    expanding_time = 0.0
    searching = True
    lowest_score = 0.0
    current_size = 1
    if work == []:
        time.sleep(2) ##if the workers is initialized without anywork just wait a few second so others have time to update amount of work list
    while searching:
        ##verify if anyone needs work
        work = check_for_work(id, work, pipes)
        
        ##if we do not have work, lets analyse what we have to do
        if work == []:
            work, searching, current_size, w_t, e_t = check_next_state(id, current_size, global_info, pipes, locks, ml_instance)
            shared_time += w_t
            expanding_time += e_t
            continue 
            
        ##get a task    
        subset = work[0]
        del(work[0])
        tasks += 1
        
        #update work
        update_amount_of_work(id, global_info, work, locks)
        
        ##process a task and update scores
        t = time.time()
        score = ml_instance.rf_evaluator(subset)
        task_time.append(round(time.time()-t, 2))
        lowest_score = update_score(subset, score, locks[score_lock], global_info, lowest_score)
        
    print id, " finished, total time: ", round(time.time() - start_t, 0), " sharing time: ", round(shared_time, 0), " expanding time ", round(expanding_time, 0)
    print id, "n tasks ", tasks, " average time: ", round(sum(task_time) / len(task_time),2)
         
        
        
        


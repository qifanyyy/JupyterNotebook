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
from sklearn import svm
from sklearn import tree
import time
import multiprocessing as mp
import random

##my modules
from myClasses import ML_set
from myClasses import data_instance
from myClasses import ML_subset
import utils

out_of_work_message = "out_of_work"
send_message = "send"

def wrapper(n_proc, data, features):
    ##division of features for each process, basically this creates the starting work list for every processor
    print "Using ", len(features), " features"
    p_work_list = utils.divide_features(n_proc-1, features)
    ##divide data into train and test set
    n_train, n_test = utils.divide_data_not_random(data)
    
    print "Using ", len(n_train), " instances for train and ", len(n_test), " for test"
    ##spawn processes
    
    data_pipe = mp.Pipe() ##communication pipe to receive work list
    pipes = [] ## each worker has its own pipe   
    workers = []     ##list to keep track of the workers processes
    current_work_list = {}
    ##start workers 
    for i in range(0,n_proc-1):
        #print "sending process:", i
        current_work_list[i] = {}
        pipe = mp.Pipe()
        p = mp.Process(target=worker_classification, args=(i, p_work_list[i], data, features, n_train, n_test, data_pipe, pipe)) ##, p_work_list[i], data, features ))
        workers.append(p)
        pipes.append(pipe)
        p.start()
    
    manage_workers(data_pipe, pipes, workers, current_work_list) ##manage workers
    return


##a partir do tamanho das listas de work que tinha, verifica qual o worker que deve fazer share do trabalho
##senao nenhum worker tiver uma lista maior que 2 retorna -1
def get_worker_to_share(id_receiver, work_size):
    worker = -1
    most_work = 2
    for i in range(0,len(work_size)):
        if work_size[i] > most_work and i != id_receiver:  ##added the condition that the same process cant send to himself
            worker = i
            most_work = work_size[i]
    return worker


##divides work amoung n processes, returns lists of working list for every process that needs work and the remaining list to the sharer
def divide_work(work_list, n_workers_needing_work):
    share_lists = []
    for i in range(0, n_workers_needing_work + 1):
        share_lists.append([])
        
    send_to = 0
    for w in work_list:
        share_lists[send_to].append(w)
        send_to += 1
        send_to = send_to % (n_workers_needing_work + 1)
    
    return share_lists[:len(share_lists)-1], share_lists[len(share_lists)-1]


##sends work to every process needing work, needs to receive the lists to send to each process
def sendWork (pipes, workers_needing_work, share_lists, work_size, best_acc, cur_wl):
    for i in range(0, len(workers_needing_work)):
        output, input = pipes[workers_needing_work[i]]
        input.send((share_lists[i], best_acc))
        aux = transform_work_list_in_hash(share_lists[i])
        cur_wl[workers_needing_work[i]] = dict(aux)
        #print "IMPORTANT 3 ", i, ":", translate_wl(share_lists[i]), "\n", aux.keys()
        work_size[workers_needing_work[i]] = len(share_lists[i])
    
    

##share work amoung processes
def share_work(id_receiver, work_size, pipes, tested_sets, cur_wl, data_out, best_acc):
    print "sharing work requested by ", id_receiver
    workers_needing_work = [id_receiver]
    cur_wl[id_receiver] = {}
    work_size[id_receiver] = 0
    while True:  ##while didnt receive any data
        selected_worker = get_worker_to_share(id_receiver, work_size)
        if selected_worker == -1: ##if there isnt any worker to share then lets stop everything
            stop_workers = []
            for i in workers_needing_work: ##then lets add all the processes that stopped
                output, input = pipes[i]
                work_size[i] = 0 
                input.send(([], best_acc))   ##send a list to every process that is waiting
                stop_workers.append(i)
            return stop_workers, best_acc
        
        sharer_output, sharer_input = pipes[selected_worker] ##open pipes to the sharer
        sharer_input.send(send_message) ##ask him to send
        msg_rcv = data_out.recv()
        #print share_worker, " selected to send"
        if msg_rcv == out_of_work_message:  ##the sharer also ran out of work
            #print "it is also out out work"
            work_size[selected_worker] = 0   ##set his work size as 0
            cur_wl[selected_worker] = {}
            workers_needing_work.append(selected_worker)  ## set him as in need of work        
        else:
            work_list, worker_tested_sets, acc = msg_rcv  ##get the work list
            if acc > best_acc:
                best_acc = acc
            new_work_list, aux_sets = cut_repetitions(selected_worker, work_list, tested_sets, cur_wl)  ##cut repetitions before sharing work
            tested_sets.update(worker_tested_sets) ## update the already tested table
            if len(new_work_list) < len(workers_needing_work) * 2: ##if after cutting repetitions there isnt enough work the just send back the list to process and lets wait for other iteration of that worker
                ##the idea here is to avoid processes to share work all the time amoung them when they are almost running out of work. By doing this, i'll wait for the next iteration of that process to check if 
                ##generated more work that is enough to share or if it stopped
                #print "not enough work to share"
                work_size[selected_worker] = len(new_work_list)
                cur_wl[selected_worker] = dict(aux_sets)
                sharer_input.send((new_work_list, best_acc))
            else: ##there is enough work to share
                #print "IMPORTANT ", len(new_work_list) , "-", len(aux_sets)
                share_lists, remaining_work = divide_work(new_work_list, len(workers_needing_work))
                work_size[selected_worker] = len(remaining_work)
                d_wl = transform_work_list_in_hash(remaining_work)
                cur_wl[selected_worker] = dict(d_wl)
                #print "IMPORTANT2 ", translate_wl(remaining_work), "\n", d_wl.keys()
                sharer_input.send((remaining_work, best_acc)) ## send the list to sharer
                sendWork(pipes, workers_needing_work, share_lists, work_size, best_acc, cur_wl) ##send works to all workers needing work
                return [], best_acc    

def transform_work_list_in_hash(wl):
    aux = {}
    for w in wl:
        cannonical_name = ','.join(str(e) for e in w.features)
        aux[cannonical_name] = True
    return aux    
        

##adds sets to the tested sets dict
def addTestedSets(tested_sets, tests_to_add):
    for test in tests_to_add:
        if test not in tested_sets:
            tested_sets[test] = True  ##bolean is only 1 bit size, so the dict isnt very expensive
    
##filter the work list of a process
def filter_work(id, msg_rcv, tested_sets, cur_wl, input, work_size, best_acc):
    test_time = time.time()
    work_list, worker_tested_sets, acc = msg_rcv  ##need to filter the duplicated data
    if acc > best_acc: ##if this process has found a better accuracy than any other, update the value
        best_acc = acc
    ##workers already filter nodes with their own lists i can send and only add repetitions to manager later to avoid keeping worker waiting
    #print "antes: ", translate_wl(work_list), "\n", worker_tested_sets.keys(), "\n", cur_wl, "\n\n"
    work_list, add_tests = cut_repetitions(id, work_list, tested_sets, cur_wl) ##remove the duplicates
    #print "depois: ", translate_wl(work_list), "\n", add_tests.keys(), "\n", cur_wl, "\n\n"
    work_size[id] = len(work_list) ##update the amount of work that a process has
    input.send((work_list, best_acc))
    
    tested_sets.update(worker_tested_sets) ##add the tests
    cur_wl[id] = dict(add_tests) ##update the current work list
    cut_time = time.time() - test_time
    cut_time = round(cut_time,2)
    print "MANAGER TOOK:", cut_time, "Size", len(tested_sets)
    #print "depois: ", translate_wl(work_list), "\n\n", add_tests.keys(), "\n\n", cur_wl, "\n\n"
    return best_acc
            
##manage all workers
def manage_workers(data_pipe, pipes, workers, current_worklist):
    tested_sets = {}
    stopped_workers = []
    work_size = [] ##guarda o tamanho das linhas de todos os processos
    best_acc = 0 ## to save the best acc found by any process
    for i in range(0, len(workers)): ##inicia o tamanho das listas a 0
        work_size.append(0)
    #rep_counter = 0 ##just to count repetitions
    data_out, data_in = data_pipe
    
    while len(stopped_workers) != len(workers): ##while there are active workers
        for i in range(0,len(workers)):
            if i in stopped_workers:  ##check if worker already stopped
                continue
            output, input = pipes[i]
            input.send(send_message) ## send message
            msg_rcv = data_out.recv()
            #start_send = time.time()
            if msg_rcv == out_of_work_message:  ##worker stopped
                workers_to_stop, best_acc = share_work(i, work_size, pipes, tested_sets, current_worklist, data_out, best_acc)
                stopped_workers += workers_to_stop ## everything that comes here is to stop
                for w in workers_to_stop:
                    workers[w].join()
            else:
                best_acc = filter_work(i, msg_rcv, tested_sets, current_worklist, input, work_size, best_acc)
            
            #print "sent work list to ", i, " and it took ", time.time() - start_send, " to cut ", rep
    
        
##verifica se o manager quer falar com ele em caso positio trocam as listas
def manager_control(id, work_list, tested_sets, data_pipe, com_pipe, acc):
    com_out, com_in = com_pipe
    start = time.time()
    if com_out.poll(): ##check if there is anything to read
        #print "PROCESS ", id , " waiting for manager to send list"
        msg = com_out.recv() ##receive message
        ##print id, " received message ", msg
        if msg == send_message:   
            data_out, data_in = data_pipe
            #print id, " SENT LIST with size ", len(work_list) ," + ", len(tested_sets)
            data_in.send((work_list, tested_sets, acc))  ##send data to the manager
            work_list, acc = com_out.recv()  ##get work list and also the best_acc found so far
            #print id, " RECEIVED LIST and took ", time.time()-start            
            return work_list, True, time.time() - start, acc
    return work_list, False, time.time() - start, acc
    
##pede trabalho ao manager
def ask_for_work(id, data_pipe, com_pipe):
    start = time.time()
    com_out, com_in = com_pipe
    data_out, data_in = data_pipe
    _ = com_out.recv() ##blocks untill manager wants to talk to him
    data_in.send(out_of_work_message) ##send request
    work_list, acc = com_out.recv() ## wait untill receives work
    return work_list, acc, time.time() - start
    
##cut the repetitions on the manager
def cut_repetitions(worker_index, work_list, tested_sets, cur_wl):
    add_sets = {}
    new_list = []
    for w in work_list:
        cannonical_name = ','.join(str(e) for e in w.features)
        new = True
        if cannonical_name in tested_sets:
            new = False
        else:
            for i in cur_wl:
                if i == worker_index: ##cant remove from his own list
                    continue
                if cannonical_name in cur_wl[i]: ##if subset is already on someone's list remove
                    new = False
                    break
        if new:
            add_sets[cannonical_name] = True
            new_list.append(w)
    return new_list, add_sets
            
            
def translate_wl(wl):
    aux = []
    for w in wl:
        aux.append(w.features)
    return aux

##function for each worker to work        
def worker_classification(id, work_list, data, features, n_train, n_test, data_pipe, com_pipe):
    worker_time = time.time() ##to know how much time did the worker work
    best_acc = 0 
    lowest_acc = 0
    wl_dict = {}  ##to keep all the generated subsets on this slave
    best_sets = {}
    last_test_sets = {} ##new test set since last talk com with manager
    total_wasted = 0
    testing = True
    number_of_tests = 0
    comm_rate = 60
    counter_time = time.time()
    
    talk_counter = 0
    talk_avgs = []
    talk_time = time.time()
    #print "started ", id, " with work ", translate_wl(work_list)
    while (testing):        
        if work_list ==  []:
            ##the last test sets will be sent on next talk to the manager
            if number_of_tests < 30:
                print id, " waiting cause ran out of work too soon" 
                time.sleep(10)
            work_list, best_acc, wasted_time = ask_for_work(id, data_pipe, com_pipe)
            total_wasted += wasted_time
            counter = comm_rate#random.randint(50, 150) #Since we need to send the last test sents to manager lets set this to a lower value
            if work_list == []: ##didnt receive work
                testing = False
                break
        
        test_subset = work_list[len(work_list)-1]  ##get the subset to test
        del(work_list[len(work_list)-1]) ##delete the subset from the work list ##according to sources removing from the end oof the list is much faster than removing from the end
        cannonical_name = ','.join(str(e) for e in test_subset.features) ##add the canonical name to the tested_sets
        
        train_set, test_set = utils.cut_dataset(n_train, n_test, data, test_subset.features) ##get the features for the subset
        acc = classification_svm(train_set, test_set) ##train and test the dataset
        test_subset.parents_accuracy.append(acc)
        number_of_tests += 1 
        last_test_sets[cannonical_name] = True ##add to last sets
        
        #debug_data[cannonical_name] = (test_subset.features, test_subset.parents_accuracy)
        if checkExpand(test_subset, best_acc): 
            new_combs, r_counter = get_combinations(work_list, test_subset, features, wl_dict) ##check for new combinantions
            work_list = new_combs + work_list  ##add new combinations to the list

        if acc > lowest_acc:  ##check if the subset is better then the previous ones
            if acc > best_acc: ## if acc is the best one found so far
                best_acc = acc
            lowest_acc = update_best_sets(best_sets, acc, test_subset)
        #counter -= 1
        
        #rts.append(time.time() - round_st)
        if (time.time() - counter_time) > comm_rate and testing: ## try to talk to manager
            checked = False;
            work_list, checked, wasted_time, acc = manager_control(id, work_list, last_test_sets, data_pipe, com_pipe, best_acc)
            wasted_time = 0.0
            total_wasted += wasted_time
            #print "PROCESS ", id , " Number of tests: ", number_of_tests, " in ", round(time.time() - worker_time, 2)
                
            if checked: ##worker communicated with manager
                talk_avgs.append(time.time() - talk_time)
                talk_counter += 1
                #print "PROCESS", id, " WORK SIZE ", len(work_list), "round time: ", rt ," expand count ", expand_count, " best acc:", max(best_sets), " global acc: ", best_acc
                print "PROCESS ", id , " Number of tests: ", number_of_tests
                last_test_sets = {} ##reset the tested list so less information is passed to the manager next time
                talk_time = time.time()
                counter_time = time.time()
     
            
    total_working_time = time.time() - worker_time
    print "PROCESS", id, ",waste_t:", total_wasted, ",work_t:", total_working_time, ",n_test:", number_of_tests, ",best acc:", max(best_sets), "talk_counter:", talk_counter, ",talk_avg:", round(sum(talk_avgs) / float(len(talk_avgs)),2)

    

##updates the top of best sets from each worker and retursn the accuracy of the lowest value on top
def update_best_sets(best_sets, acc, test_set):
    if len(best_sets) < 5:
        best_sets[acc] = test_set
        if len(best_sets) == 5:
            return min(best_sets)
        return 0.0
    min_value = min(best_sets)
    del best_sets[min_value]
    best_sets[acc] = test_set
    return min(best_sets)
    


def get_combinations (work_list, subset, fts, wl_dict): ##check which new subsets may be tested
    new_combs = []
    counter = 0 ##just to cunt repetitions
    combination = subset.features ##features da combinacao
    for ft in fts: ##for all possible tests
        if ft not in combination: ##if it isnt already in the subset
            aux = combination + [ft] ##subset plus one new feature
            aux.sort()
            cannonical_name = ','.join(str(e) for e in aux) ##transform list into string
                
            if cannonical_name not in wl_dict: ##if it has not been tested yet and its not on the work list
                #tested_combinations.append(cannonical_name)
                wl_dict[cannonical_name] = True
                new_list = list(subset.parents_accuracy)  ##to avoid passing a pointer to the same list on all childs!!
                new_combs.append(ML_subset(aux, new_list))  ##add a new set with the parents combination
            else:
                counter += 1 ##one repetition found
    #return tested_combinations, new_combs
    return new_combs, counter


##checks if it worth expand a node based on the previous relations
def checkExpand(subset, global_acc):
    return True
    
    accs = subset.parents_accuracy
    last_acc = accs[len(accs)-1]  
    
    if len(accs) > 10:  ##when we have more than 10 features 
        if last_acc > accs[len(accs)-2]: ##expand while it is still growing
            return True
    else:
        if (last_acc + 1.5) > global_acc: ##expand while we are close from the best
            return True
  
    return False
        

def classification_svm (train_set, test_set): ##train a classifier and returns its error rate
    #st = time.time()
    clf = svm.SVC(C=100)  
    clf.fit(train_set.fts_values, train_set.fts_pred)
    predictions = clf.predict(test_set.fts_values)
    preds = []
    for i in predictions:
        #print i
        preds.append(int(i))
    accuracy = check_accuracy_rate(preds, test_set.fts_pred)
    accuracy = round(accuracy, 2)
 
    return accuracy
    #return time.time()-st, accuracy

def classification_decision_tree (train_set, test_set):
    #st = time.time()
    clf = tree.DecisionTreeClassifier(random_state=0)
    clf = clf.fit(train_set.fts_values, train_set.fts_pred)
    predictions = clf.predict(test_set.fts_values)
    preds = []
    for i in predictions:
        #print i
        preds.append(int(i))
    accuracy = check_accuracy_rate(preds, test_set.fts_pred)
    accuracy = round(accuracy, 2)
    #print "Confusion matrix for Decision trees without train set"
    #print makeConfusionMatrix(test_set.fts_pred, preds)
    #print "Acc: ", accuracy, "\n\n"
    return accuracy
    #return time.time()-st, accuracy


##returns a list with the confusion matrix for an evaluation
def makeConfusionMatrix(real_class, pred_class):
    s_tp = 0  ##stress utterances predicted as stress
    s_fp = 0  ##no stress utterances predicted as stress
    ns_tp = 0 ##no stress utterances predicted as no stress
    ns_fp = 0 ##stress utterances predicted as no stress
    for i in range(0, len(pred_class)):
        if pred_class[i] == 0:
            if real_class[i] == 0:
                ns_tp += 1
            else:
                ns_fp +=1
        else:
            if real_class[i] == 1:
                s_tp += 1
            else:
                s_fp += 1
    return  [s_tp, s_fp, ns_tp, ns_fp]
                
                
##calculates the accuracy rate
def check_accuracy_rate(pred, real):
    error_count = 0
    total = float(len(real))
    for i in range(0,len(pred)):
        #print pred[i], " ", real[i]
        if int(pred[i]) != int(real[i]):
            error_count += 1
    error_rate = round(error_count / total, 4)
    accuracy = 1 - error_rate
    return accuracy * 100
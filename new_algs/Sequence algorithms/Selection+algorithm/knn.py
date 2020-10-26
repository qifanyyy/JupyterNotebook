import decimal
import re
import operator
from map import *
import math
import time

def euclidean(trn,tst,curr):
    dist = 0
    for i in curr:
        dist += math.pow(trn[i]-tst[i],2)
    return math.sqrt(dist)

def KNN(train,test,curr):
    D = []
    for r in train:
        dist = euclidean(r,test,curr)
        D.append([dist,r[0]])
    D.sort(key=operator.itemgetter(0))
    return D[0][1]

def leave_one_out_cross_validation(table,current_feat,feature,choice):

    freq = 0
    current = current_feat[:]
    if choice == 1:
        current.append(feature)
    else:
        current.remove(feature)

    for k in range(0, len(table)):
        train = table[:]
        test = train.pop(k)
        group = KNN(train,test,current)
        if test[0] == group:
            freq += 1
    acc = freq / float(len(table))
    return acc

def forward_selection(table):

    final_features = []
    final_accuracy = 0
    current_features = []
    feature_size = len(table[0])
    accuracies = []
    print "Beginning Search"
    for i in range(1,feature_size):
        #print " On the "+str(i)+"th level of the tree"
        feature_to_add_this_level = -1
        best_accuracy = 0

        for j in range(1,feature_size):
            if j not in current_features:
                #print " Considering adding the "+str(j)+"th feature"
                accuracy = leave_one_out_cross_validation(table,current_features,j,1)
                print "     Using feature(s) ["+str(j)+"] accuracy is "+str(accuracy)
                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    feature_to_add_this_level = j

        if feature_to_add_this_level != -1:
            current_features.append(feature_to_add_this_level)
            print "On level "+str(i)+" I added feature "+ str(feature_to_add_this_level) + " to current set"
            print "Feature set "+ str(current_features)+" was best with accuracy:"+str(best_accuracy)
            accuracies.append(best_accuracy)
        if best_accuracy > final_accuracy:
            final_features = current_features[:]
            final_accuracy = best_accuracy
    print "Finished Search!!!"
    print "Best feature subset is: "
    print final_features
    print "Best accuracy is: "
    print final_accuracy

def leave_one_out_cross_validation_speedup(table,current_feat,feature,best_so_far):

    local_miss = 0
    freq = 0
    current = current_feat[:]
    current.append(feature)
    for k in range(0, len(table)):
        train = table[:]
        test = train.pop(k)
        group = KNN(train,test,current)
        if test[0] == group:
            freq += 1
        else:
            local_miss += 1
            if local_miss > best_so_far:
                return [0,best_so_far]
    best_so_far = local_miss
    acc = freq / float(100)
    return [acc,best_so_far]

def backward_elimination(table):
    final_features = []
    final_accuracy = 0
    current_features = range(1,len(table[0]))
    feature_size = len(table[0])
    accuracies = []
    print "Beginning Search"
    for i in range(1, feature_size):
        # print "On the "+str(i)+"th level of the tree"
        feature_to_remove_this_level = -1

        #best_accuracy = leave_one_out_cross_validation(table,current_features,-1,2)
        best_accuracy = 0
        for j in range(1, feature_size):
            if j in current_features:
                # print "Considering adding the "+str(j)+"th feature"
                accuracy = leave_one_out_cross_validation(table, current_features,j,2)
                print "     Using feature(s) [" + str(j) + "] accuracy is " + str(accuracy)
                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    feature_to_remove_this_level = j

        if feature_to_remove_this_level != -1:
            current_features.remove(feature_to_remove_this_level)
            print "On level " + str(i) + " I removed feature " + str(
                feature_to_add_this_level) + " from current set with accuracy:" + str(best_accuracy)
            accuracies.append(best_accuracy)
        if best_accuracy > final_accuracy:
            final_features = current_features[:]
            final_accuracy = best_accuracy

    print "Finished Search!!!"
    print "Best feature subset is: "
    print final_features
    print "Best accuracy is: "
    print final_accuracy

def speedup(table):

    best_so_far=100
    final_features = []
    final_accuracy = 0
    current_features = []
    feature_size = len(table[0])

    for i in range(1,feature_size):
        #print "On the "+str(i)+"th level of the tree"
        feature_to_add_this_level = -1
        best_accuracy = 0

        for j in range(1,feature_size):
            if j not in current_features:
                #print "Considering adding the "+str(j)+"th feature"
                result = leave_one_out_cross_validation_speedup(table,current_features,j,best_so_far)
                accuracy = result[0]
                best_so_far = result[1]
                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    feature_to_add_this_level = j

        if feature_to_add_this_level != -1:
            current_features.append(feature_to_add_this_level)
            print "On level "+str(i)+" I added feature "+ str(feature_to_add_this_level) + " to current set"

        if best_accuracy > final_accuracy:
            final_features = current_features[:]
            final_accuracy = best_accuracy

    print "Final set of features are: "
    print final_features
    print "Final accuracy is: "
    print final_accuracy

def normalize(activeDataSet):
	dataSet = activeDataSet
	average = [0.00]*(len(dataSet[0])-1)
	stds = [0.00]*(len(dataSet[0])-1)
	#	get averages
	for i in dataSet:
		for j in range (1,(len(i))):
			average[j-1] +=  i[j]
	for i in range(len(average)):
		average[i] = (average[i]/len(dataSet))
	#	get std's sqrt((sum(x-mean)^2)/n)
	for i in dataSet:
		for j in range (1,(len(i))):
			stds[j-1] +=  pow((i[j] - average[j-1]),2)
	for i in range(len(stds)):
		stds[i] = math.sqrt(stds[i]/len(dataSet))
	#	calculate new values (x-mean)/std
	for i in range(len(dataSet)):
		for j in range (1,(len(dataSet[0]))):
			dataSet[i][j] = (dataSet[i][j] - average[j-1])/ stds[j-1]
	return dataSet

def visualize(values):
    import matplotlib.pyplot as plt;
    plt.rcdefaults()
    import numpy as np
    import matplotlib.pyplot as plt

    objects = range(1,11)
    y_pos = np.arange(len(objects))
    performance = [10, 8, 6, 4, 2, 1]

    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Usage')
    plt.title('Programming language usage')

    plt.show()

if __name__ == '__main__':
    file = raw_input("Enter file name:")
    #file = "/Users/harry/Downloads/205_proj2_data/CS205_SMALLtestdata__70.txt"
    with open(file) as f:
        data = f.readlines()
    row = []
    table = []
    data = [x.strip() for x in data]
    for line in data:
        values = re.split(" +",line)
        for v in values:
            val = float(decimal.Decimal(v))
            row.append(val)
        table.append(row)
        row = []
    table = normalize(table)

    print """Enter the algorithm: \n
        1)Forward Selection \n
        2)Backward Selection\n
        3)Original Algorithm
        """
    n = int(input("Enter your choice: "))
    print "This dataset has "+str(len(table[0])-1)+" features(not including class attributes),with "+str(len(table))+" instances."
    print "Please wait While I normalize data.....Done!"
    start_time = time.time()
    if n==1:
        forward_selection(table)
    elif n==2:
        backward_elimination(table)
    elif n==3:
        speedup(table)
    print("--- %s seconds ---" % (time.time() - start_time))

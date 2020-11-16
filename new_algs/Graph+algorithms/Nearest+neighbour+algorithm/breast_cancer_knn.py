'''Python36
Designing a KNN algorithm from scratch and using breast_cancer.txt'''

import numpy as np
import warnings
from collections import Counter
import pandas as pd
import random

def main():
    df = pd.read_csv('breast_cancer.txt')
    df.replace('?', -99999, inplace=True)
    df.drop('id', 1, inplace=True)
    
    # the reason for doing this is because df.head() won't display the complete data in correct format. Plus everything has to be an int or float so it was needed
    # uncomment below line to see the error in displayed data
    #print(df.head())
    full_data = df.astype(int).values.tolist()
    random.shuffle(full_data)
    
    test_size = 0.2
    train_set = {2:[], 4:[]}
    test_set = {2:[], 4:[]}
    # 80 percent train data
    train_data = full_data[:-int(test_size*len(full_data))]
    # 20 percent test data
    test_data = full_data[-int(test_size*len(full_data)):]
    
    # populate the dictionary
    # key is either 2 or 4 in each i
    # and column for the class in the dataset is the last one so address it using -1
    # append data to that key i excluding the last value (class) 
    for i in train_data:
        train_set[i[-1]].append(i[:-1])
    #endfor
    for i in test_data:
        test_set[i[-1]].append(i[:-1])
    #endfor
    
    correct = 0
    total = 0
    for group in test_set:
        for data in test_set[group]:
            vote, confidence = k_nearest_neighbors(train_set, data, k=3)
            # increase the correct count if group in test_set matches the vote from train_set
            if group == vote:
                correct+=1
                print('Vote result: ', vote, 'Match Confidence: ', confidence)
            else:
                print('Vote result: ', vote, 'Not matched confidence: ', confidence)
            #endif
            total+=1 
        #endfor
    #endfor
    
    print('Accuracy: ', correct/total)
    return
#enddef

def k_nearest_neighbors(data, predict, k=3):
    if len(data) >= k:
        warnings.warn('K is set to a value less than total voting groups')
    #endif
    
    # knn algorithm
    distances = []
    for group in data:
        for features in data[group]:
            # applying the euclidean distance from predict point to the features of the group
            #    and then comparing the distances with each point to find which is the shortest
            #    distance in order to classify our predict point as that group
            #        WILL TAKE A LOT OF TIME AND IT'S INEFFICIENT WITH BIGGER DATASETS!
            # and what if the feautures are not 2 dimensional but 3 or more dimensions? Euclidean distance cannot be calculated that easily!
            
            # faster way
            euclidean_distance = np.linalg.norm(np.array(features)-np.array(predict))
            distances.append([euclidean_distance, group])
        #endfor
    #endfor
    
    # getting votes from each group just 3 times as k=3 (we don't care what distances are so just use second column which is the group
    votes = []
    for i in sorted(distances)[:k]:
        votes.append(i[1])
    #endfor
    
    #print("votes: ")
    #print(votes)
    #print("vote count: ")
    print(Counter(votes).most_common(2))
    vote_result = Counter(votes).most_common(1)[0][0]
    
    # confidence is the most common votes divided by the test points k
    confidence = Counter(votes).most_common(1)[0][0]/k
    
    return vote_result, confidence

if __name__ == '__main__':
    main()
#endif
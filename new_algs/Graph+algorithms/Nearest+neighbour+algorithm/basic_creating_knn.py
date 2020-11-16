'''Python36
Designing a KNN algorithm from scratch'''

import numpy as np
import matplotlib.pyplot as plt
import warnings
from matplotlib import style
from collections import Counter
style.use('fivethirtyeight')

def main():
    # making two classes k and r; with their 3 features
    dataset = {'k':[[1,2],[2,3],[4,5],[3,6],[3,8],[4,1]], 'r':[[5,2],[4,9],[5,6],[6,5],[7,7],[8,6]]}
    new_features = [4.2,7]
    
    for i in dataset:
        for ii in dataset[i]:
            plt.scatter(ii[0],ii[1], s=100, color=i)
        #endfor
    #endfor
    
    plt.scatter(new_features[0], new_features[1], s=100)
    plt.title("Predict the blue dot!")
    plt.show()
    
    result = k_nearest_neighbors(dataset, new_features, k=5)
    print("result: ")
    print(result)
    
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
    print("votes: ")
    print(votes)
    print("vote count: ")
    print(Counter(votes).most_common(2))
    vote_result = Counter(votes).most_common(2)[0][0]
    
    return vote_result

if __name__ == '__main__':
    main()
#endif
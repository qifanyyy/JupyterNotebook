import numpy as np
from copy import deepcopy
import pandas as pd
import collections
import matplotlib
import matplotlib.pyplot as plt



# k-means with Manhattan distance
# =============================================================================================

# Initialise cluster centers by randomly selecting the number of k instances from the dataset x
def initial_centroids(x, k):
    initcenters = []
    # generate a list of random integer numbers, size of k
    r = np.random.randint(low=1, high=len(x), size=k)
    # make sure that the generated random numbers in the list are unique
    while (len(r) > len(set(r))):
        r = np.random.randint(low=1, high=len(x), size=k)
    # add selected random k instances into the empty list as initial centroids
    for i in r:
        initcenters.append(x[i])
    return initcenters

# Compute the Manhattan distance between each instance and cluster centers
def manhdist(x, y):
    return sum(abs(a-b) for a, b in zip(x, y))


def manhdist_table(x, centroids):
    dist = []
    for c in centroids:
        temp = []
        for p in x:
            temp.append(manhdist(p, c))
        dist.append(temp)
    return dist



# Assign each instances to the closest cluster center based on the minimum Manhattan distance
def assign_clusters(x, dist_table):
    n = x.shape[0]
    clusters = np.zeros(n) # create zeros list for storing the assignment
    clusters = np.argmin(dist_table, axis = 0)
    return clusters


# K-Means algorithm with Manhattan distance, x represents the data points, and k represents the number of clusters
def kmeans_manhdist(x, k):
    # 1)initialize the random cluster centers
    centroids = initial_centroids(x, k)
    centroids_old = np.zeros(np.shape(centroids)) # to store the old centroids
    centroids_new = deepcopy(centroids) # to store the new centroids

    error = np.linalg.norm(centroids_new - centroids_old) # to determine if the cluster centers change
    num_errors = 0

    while error != 0:
        num_errors += 1
        # 2)compute the Manhattan distance between each instance and cluster centers
        dist_table = manhdist_table(x, centroids_new)

        # 3)assign all instances to the closest cluster center
        clusters_table = assign_clusters(x, dist_table)

        centroids_old = deepcopy(centroids_new) # to independently copy the centroids to the old one after done the assignment

        # 4)update the cluster centers
        for j in range(k):
            centroids_new[j] = np.mean(x[clusters_table == j], axis=0)

        # 5)break if the cluster centers do not change any more, otherwise repeat step 2-4
        error = np.linalg.norm(np.array(centroids_new) - np.array(centroids_old)) # to calculate the error again
    final_clusters = clusters_table
    final_centroids = np.array(centroids_new)
    # to show the final result
    print("======================Final results of k-means with Manhattan distance======================================")
    print("Total number of updates:", num_errors)
    print("Final clusters:")
    print(clusters_table)
    print("Final cluster center:")
    print(np.array(centroids_new))
    return final_clusters, final_centroids


# convert 4 data files into txt file, which are "animals", "countries", "fruits", and "veggies"
# load 4 datasets
df1 = np.loadtxt("animals.txt", dtype = str)
df2 = np.loadtxt("countries.txt", dtype = str)
df3 = np.loadtxt("fruits.txt", dtype = str)
df4 = np.loadtxt("veggies.txt", dtype = str)

# combine 4 datasets into 1 dataset
df = np.concatenate([df1, df2, df3, df4], axis=0)
df = df[:, 1:301]
data = df.astype(np.float) # convert "str" to "float" for k-means implementation


# label 4 categories "animals", "countries", "fruits" and "veggies" as 'a', 'c', 'f', 'v' respectively
label = []
for l in range(df1.shape[0]):
    label.append('a')
for o in range(df2.shape[0]):
    label.append('c')
for p in range(df3.shape[0]):
    label.append('f')
for q in range(df4.shape[0]):
    label.append('v')


# define cluster list for calculating precision, recall, and F-score
def generate_clusterlist (x, k):
    final_clusters = kmeans_manhdist(x, k)[0]
    row_data = {'label':label, 'cluster':final_clusters}

    temp = pd.DataFrame(row_data)

    clusters_list = []
    for j in range(k):
        d = temp.loc[temp['cluster'] == j]

        clusters_list.append(d['label'].values.tolist())
    return clusters_list


# compute precision, recall, and F-score

def precision_recall_f1(x, k):
    # vary k from 1 to 10
    num_cluster = list(range(1, k+1))
    # create empty list for precision, recall, and F-score for plotting
    precision = []
    recall = []
    f1 = []
    for i in num_cluster:
        cluster_list = generate_clusterlist(x, i)
        num_doc = 0
        positives = 0
        negatives = 0
        TP = 0
        FP = 0
        FN = 0
        TN = 0
        c_list = []
        for c in range(0, len(cluster_list)):
            # calculating the number of documents
            num_doc += len(cluster_list[c])

            # calculating all positives
            positives += (len(cluster_list[c]) * (len(cluster_list[c]) - 1)) / 2

            # calculating TP
            c = collections.Counter(cluster_list[c])
            c_list.append(c)
            tp_temp = 0
            for k, v in dict(c).items():
                if v > 1:
                    tp_temp += (v * (v - 1)) / 2
            TP += tp_temp

        FP = positives - TP
        negatives = ((num_doc * (num_doc - 1)) / 2) - positives

        # Add all the cluster together
        sum = collections.Counter()
        for c in c_list:
            sum += c
            # calculating FN
        for ct in c_list:
            fn_temp = 0
            for k, v in dict(ct).items():
                fn_temp += v * (sum[k] - v)
            sum -= ct
            FN += fn_temp
        TN = negatives - FN
        print("k=", i)
        print("num_doc is %d " % num_doc)
        print("positives is %d " % positives)
        print("TP is %d " % TP)
        print("FP is %d " % FP)
        print("FN is %d " % FN)
        print("TN is %d " % TN)

        Precision = TP / (TP + FP)
        print("Precision is %.2f " % Precision)

        Recall = TP / (TP + FN)
        print("Recall is %.2f " % Recall)

        F1 = (2 * Recall * Precision) / (Recall + Precision)
        print("F1 is %.2f " % F1)

        # generate list for plotting
        precision.append(Precision)
        recall.append(Recall)
        f1.append(F1)
    return precision, recall, f1

# Plot k in the horizontal axis and precision, recall and F-score in the vertical axis in the same plot
result = precision_recall_f1(data, 10)

K = list(range(1, 11))
fig = plt.figure()
ax = plt.axes()
plt.plot(K, result[0], label='precision')
plt.plot(K, result[1], label='recall')
plt.plot(K, result[2], label='F1')
plt.title('k-means with Manhattan distance')
plt.xlabel('k: number of cluster')
plt.ylabel('Precision, Recall, F1')
plt.legend()
plt.show()





# k-means with Manhattan distance and l2 normalised feature vectors
# =============================================================================================

def l2_norm(X):
    for i in range(0, X.shape[0]):
        norm = np.sqrt(np.sum(X[i,:] * X[i,:]))
        X[i, :] = X[i, :] / norm
    return X;

l2_data = l2_norm(data)

result_norm = precision_recall_f1(l2_data, 10)
K = list(range(1, 11))
fig1 = plt.figure()
ax1 = plt.axes()
plt.plot(K, result_norm[0], label='precision')
plt.plot(K, result_norm[1], label='recall')
plt.plot(K, result_norm[2], label='F1')
plt.title('k-means with Manhattan distance \nl2 normalised')
plt.xlabel('k: number of cluster')
plt.ylabel('Precision, Recall, F1')
plt.legend()
plt.show()

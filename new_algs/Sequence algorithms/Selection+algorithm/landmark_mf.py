from sklearn.cluster import DBSCAN, KMeans
from Algorithms.dbscan import get_dbscan
from Algorithms.kmeans import get_Kmeans
from sklearn.metrics.cluster import adjusted_rand_score, adjusted_mutual_info_score, completeness_score, fowlkes_mallows_score
from sklearn.metrics import accuracy_score, f1_score
from scipy.stats import skew, kurtosis
from sklearn.tree import DecisionTreeClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
import numpy as np
import time

def get_kmeans_meta_features(dataset_name, df):
    record = {'dataset': dataset_name.split('.')[0]}
    results = []
    for i in range(10):
        model1 = KMeans(n_clusters=3, max_iter=5)
        model1.fit(df)
        model2 = KMeans(n_clusters=3, max_iter=5)
        model2.fit(df)
        results.append(adjusted_rand_score(model1.labels_, model2.labels_))

    results = np.array(results)
    record['KM1'] = np.mean(results)
    record['KM2'] = np.std(results)
    record['KM3'] = np.median(results)
    record['KM4'] = skew(results)
    record['KM5'] = kurtosis(results)

    return record
        
def get_landmarking(dataset_name, df):
    start = time.time()
    record = {'dataset': dataset_name.split('.')[0]}
    results = []
    n_samples = int(len(df)*0.1) if len(df) > 400 else min(df.shape[0], 40)
    data = df.sample(n=n_samples, replace=False)
    labels = get_dbscan(data)
    k = len(np.unique(labels))
    labels2 = get_Kmeans(data, k, 40)
    full_tree = DecisionTreeClassifier()
    full_tree.fit(data, labels)
    worst_attr = np.argmin(full_tree.feature_importances_)

    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.3)
    best_stump = DecisionTreeClassifier(max_depth=1)
    random_stump = DecisionTreeClassifier(splitter="random", max_depth=1)
    worst_stump = DecisionTreeClassifier(max_depth=1)
    elite_knn = KNeighborsClassifier(n_neighbors=1)
    one_knn = KNeighborsClassifier(n_neighbors=1,
            algorithm="auto",
            weights="uniform",
            p=2,
            metric="minkowski")
    nb = GaussianNB()
    lda = LinearDiscriminantAnalysis()
    best_stump.fit(X_train, y_train)
    random_stump.fit(X_train, y_train)
    worst_stump.fit(X_train.iloc[:, worst_attr].values.reshape(-1, 1), y_train)
    elite_knn.fit(X_train, y_train)
    one_knn.fit(X_train, y_train)
    # lda.fit(X_train, y_train)
    nb.fit(X_train, y_train)

    record['LM1'] = np.log2(df.shape[0])
    record['LM2'] = np.log2(df.shape[1])
    record['LM3'] = accuracy_score(best_stump.predict(X_test), y_test)
    # record['LM4'] = f1_score(best_stump.predict(X_test), y_test, average='weighted')
    record['LM5'] = accuracy_score(random_stump.predict(X_test), y_test)
    # record['LM6'] = f1_score(random_stump.predict(X_test), y_test, average='weighted')
    # record['LM7'] = model.inertia_
    record['LM8'] = accuracy_score(elite_knn.predict(X_test), y_test)
    # record['LM9'] = f1_score(elite_knn.predict(X_test), y_test, average='weighted')
    # record['LM10'] = accuracy_score(lda.predict(X_test), y_test)
    # record['LM11'] = f1_score(lda.predict(X_test), y_test, average='weighted')
    record['LM12'] = accuracy_score(nb.predict(X_test), y_test)
    # record['LM13'] = f1_score(nb.predict(X_test), y_test, average='weighted')
    record['LM14'] = accuracy_score(one_knn.predict(X_test), y_test)
    # record['LM15'] = f1_score(one_knn.predict(X_test), y_test, average='weighted')
    record['LM16'] = accuracy_score(worst_stump.predict(X_test.iloc[:, worst_attr].values.reshape(-1, 1)), y_test)
    # record['LM17'] = f1_score(worst_stump.predict(X_test.iloc[:, worst_attr].values.reshape(-1, 1)), y_test, average='weighted')
    record['LM18'] = adjusted_rand_score(labels, labels2)
    record['LM19'] = adjusted_mutual_info_score(labels, labels2)
    record['LM20'] = completeness_score(labels, labels2)
    record['LM21'] = fowlkes_mallows_score(labels, labels2)

    end = time.time()
    return record, (df.shape[0], df.shape[1], end-start)

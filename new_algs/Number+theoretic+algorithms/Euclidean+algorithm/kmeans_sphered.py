import random
import numpy as np
from sklearn.decomposition import PCA

class KMeansSpheredData:
    def __init__(self, k, iterations=1000):
        self.k = k
        self.iterations = iterations
        self.seed = 100
        
    def euclidean_distance(self, u, v):
        """Computes the euclidean distance between two arrays.

        Parameters
        ----------
        u: array-like
            First input array.
        v: array-like 
            Second input array.

        Returns
        -------
        float
            Euclidean distance between vectors u and v.
        """
        return np.sqrt(np.sum(np.square(u - v)))

    def fit(self, dataset):
        """Spheres the dataset and computes k means clustering using Euclidean distance.

        Parameters
        ----------
        dataset: array-like
            Training data.

        Returns
        -------
            References the instance object. 
        """
        #sphered data  
        self.pca = PCA(whiten=True)
        dataset = self.pca.fit_transform(dataset)
        
        #random k elements in the dataset are chosen as initial centroids
        random.seed(self.seed)
        self.centroids = {index:value for index, value in enumerate(random.sample(list(dataset), self.k))}

        for i in range(self.iterations):
            
            #create a empty partition dict to contain each cluster
            self.partitions = {i:[] for i in range(self.k)}
            
            #assign each sample to the cluster given the nearest centroid
            for sample in dataset:
                distances = [self.euclidean_distance(sample, self.centroids[centroid]) for centroid in self.centroids]
                self.partitions[distances.index(min(distances))].append(sample)
                
            #keep the centroids before they're updated        
            old_centroids = dict(self.centroids)

            #update the centroids
            for cluster in self.partitions:
                self.centroids[cluster] = np.mean(self.partitions[cluster], axis=0)

            #compare current centroid with the previous one  
            centroids_comparison = [np.allclose(self.centroids[centroid], old_centroids[centroid]) for centroid in self.centroids]
            
            if False not in centroids_comparison:
                return self
                break
                
        return self
    
    def predict(self, dataset):
        """Assigns each data point in the dataset to the closest cluster.

        Parameters
        ----------
        dataset: array-like
            New data to be assigned to clusters.

        Returns
        -------
        list
            Cluster index each sample belongs to. 
        """
        self.labels = []
        dataset = self.pca.fit_transform(dataset)
        for sample in dataset:
            distances = [self.euclidean_distance(sample, self.centroids[centroid]) for centroid in self.centroids]
            self.labels.append(distances.index(min(distances)))
        return self.labels
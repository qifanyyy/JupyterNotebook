import numpy as np
import math

from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_selection import chi2
from sklearn.metrics import classification_report, precision_score, recall_score, f1_score

import DataSet as ds


class Classifier:
    """
    Class to represent a bernoulli naive bayes classifier. Each instantiation of this is a binary classifier, optionally reducing the number of features in the dataset according to the specified feature selection method
    """
    
    def __init__(self, data_set, label,  number_of_features=None, feature_selection_method=None):
        """
        Instantiate a binary bernoulli naive bayes classifier.
        :data_set: a DataSet object, the reuters dataset read in and stored in the appropriate fashion for use here
        :label: string, the label targeted by the binary classifier. Expected to be one of the items from ds.all_labels - the 10 most common labels in the reuters dataset
        :number_of_features: integer, the number of features to be selected from the possible features. If not given, all features will be used. 
        :feature_selection_method: string, if specified assumed to be one of "freq" frequency-based, "mi" mutual information, or "chisq" chi-squared. If not given, all features will be used
        """
        self.data_set = data_set
        self.method = feature_selection_method
        self.k = number_of_features
        self.label = label  
        
        self.classifier = None  # will later be an instantiation of sklearn bernoulliNB classifier
        
        self.training_labels = np.zeros((len(self.data_set.train_labels),), dtype=np.bool) # will be a binary array, value of each bit representing whether the document at that index belongs to the class self.label
        self.test_labels = np.zeros((len(self.data_set.test_labels),), dtype=np.bool)
        
        self.features = None # will become array of the indices of the features selected from ds.all_features by the specified algorithm
        
        self.training_vectors_selected = None  # will become array of binary arrays, each conceptually the feature vector for that document, given the features that have been selected 
        self.test_vectors_selected = None


        # sort out the appropriate labels and features, then fit the classifier
        self.get_binary_labels()  # we are going to need these for the classifier even if not for feature selection
        self.select_features()
        self.classifier = BernoulliNB()
        self.classifier.fit(self.training_vectors_selected, self.training_labels)


    def get_binary_labels(self):
        """
        From the lists of strings of training and test labels in self.data_set, create binary lists: document at that index is in class self.label or not. Store these in the self.test_labels, self.training_labels arrays
        """
        for i in range(len(self.data_set.train_labels)):
            if self.data_set.train_labels[i] == self.label:
                self.training_labels[i] = 1

        for i in range(len(self.data_set.test_labels)):
            if self.data_set.test_labels[i] == self.label:
                self.test_labels[i] = 1

        # the labels are now 1 for in class "label", else 0


    # These are the "utility measures" to be used in feature selection. Each doesn't return anything, rather sets the value of self.features - an array containing the indices of the features selected 

    def compute_freq_util(self):
        """
        Compute feature utility according to frequency: the number of documents in the class being targeted that contain the term represented by feature i (book section 13.5.3)
        """
        totals =  np.zeros((len(self.data_set.all_features),), dtype="int")  # track the counts of each feature across all the relevant documents
        
        for idx in range(len(self.training_labels)):  # over all the documents
            if self.training_labels[idx] == 1:  # if the document has the label being targeted
                totals += self.data_set.train_vectors[idx]  # add the value of that feature to the total

        self.features =  totals.argsort()[(self.k * -1):]   # argsort gives an array of indices to np array that sort the array ascending, we want the last k indices, corresponding to the k features which are most frequently 1

    def compute_mi_util(self):
        """
        Compute feature utility according to Mutual Information: how much (information-theoretic) information a term contains about the label, by looking at how far the distribution of the term within the class differs from its distribution in the collection as a whole. Maths and notation from book section 13.5.1 eq 13.16
        """
        
        no_training_docs = len(self.training_labels)
        
        # class probabilities
        p_label = np.sum(self.training_labels) / no_training_docs  # this is an int  P(C=1)
        pC = [1 - p_label, p_label]  # P(C=0), P(C=1)
        
        # term probabilities
        count_features = np.sum(self.data_set.train_vectors, axis=0)  # sum all the columns in the array of feature vectors
        p_features = count_features / no_training_docs  # 1d array, P(U=1)
        p_not_features = 1 - p_features
        pU = np.array([p_not_features, p_features])  # 2d array [ [P(U=0)], [P(U=1)] ]

        # conditional probabilities needed for computing joint
        conditional = np.array([ [ 1-self.compute_conditional_prob(0), self.compute_conditional_prob(0) ] ,     # P(U=0|C=0) P(U=1|C=0)
                                 [ 1-self.compute_conditional_prob(1), self.compute_conditional_prob(1) ] ])      # P(U=0|C=1) P(U=1|C=1)  arrays, length = no of features
        
        
        scores = np.zeros((len(self.data_set.all_features),), dtype="int")
        for i in range(len(self.data_set.all_features)):  # itereate over all your features
            score = 0
            for et in [0,1]:  # for all combinations of feature values and label values
                for ec in [0,1]:
                    joint = conditional[ec, et, i] * pC[ec]
                    if joint == 0:  # so you dont try to do log(0)
                        elem = 0
                    else:
                        elem = joint * math.log((joint / (pC[ec] * pU[et][i])), 2) # cf eq 13.16 textbook
                    score += elem
            
            scores[i] = score
        
        self.features = scores.argsort()[(self.k * -1):] 


    def compute_conditional_prob(self, label_value):
        """
        Compute the conditional probability of all features given that the label has the value label_value
        Return a np array of the probability values, corresponding to the features by index
        """

        cumul = np.zeros((len(self.data_set.all_features),), dtype="int")
        
        nused = 0
        for idx in range(len(self.training_labels)):  # over all the feature vectors
            label = self.training_labels[idx]  # the vector is assoclated with this label
            if label == label_value:  # if it is the right label
                cumul += self.data_set.train_vectors[idx]  # add the value of that feature to the total
                nused += 1  # track how many rows we have counted
        
        if nused == 0:  # ie no documents have that label
            p_conditional = 0  # we didnt use any rows
        else:
            p_conditional = cumul / nused  # normalize by how many rows you used to get the conditional 
        
        return p_conditional # P(U=1 | C=label_value)
        


    def compute_chisq_util(self):
        """
        Compute feature utility according to the chi-squared metric: how far observed frequency of a feature in the class deviates from the expected frequency over the whole collection 
        """
        scores = chi2(self.data_set.train_vectors, self.training_labels)
        self.features = scores[0].argsort()[(self.k * -1):] 


    def select_features(self):
        """
        Wse the specified feature utility functions to get an array of the indices of features you want to use in classification, extract just these indices from the whole training and test data feature sets, to get self.training_vectors_selected and self.test_vectors_selected - the new smaller feature vectors for your training and test sets
        """
        if not self.k:
            self.features = None
            self.training_vectors_selected = self.data_set.train_vectors  # use all the features
            self.test_vectors_selected = self.data_set.test_vectors
            return  # since the vectors with all features are already calculated
        
        # compute the feature utility score for each feature, set self.features to this array
        if self.method == "freq":
            self.compute_freq_util()
        elif self.method == "mi":
            self.compute_mi_util()
        elif self.method == "chisq":
            self.compute_chisq_util()
        else:  # unknown method or none specified
            print("Didn't understand that method, so using all the features!")
            self.features = None
            self.training_vectors_selected = self.data_set.train_vectors  # use all the features
            self.test_vectors_selected = self.data_set.test_vectors
            return  # since the vectors with all features are already calculated

        # slice out from the original doc feature vectors the columns corresponding to the features you selected
        self.training_vectors_selected = self.data_set.train_vectors[:, self.features]
        self.test_vectors_selected = self.data_set.test_vectors[:, self.features]
        
        
    def evaluate(self):
        """
        Make predictions on the test set and run the standard set of evaluation metrics on the classifier
        """
        predictions = self.classifier.predict(self.test_vectors_selected)
        true = self.test_labels
        precision = precision_score(true, predictions, average=None)
        recall = recall_score(true, predictions, average=None)
        f1 = f1_score(true, predictions)
        print(classification_report(true, predictions))
        return (precision[0], precision[1], recall[0], recall[1], f1)


'''
Created on Jan 20, 2013

@author: mlukasik

Multi Label classification algorithm: Threshold Multi-Label k Nearest Neighbours.

TML-kNN Classification is a modification of MLkNN algorithm.

The implementation is based on Orange framework for machine learning in Python. 
Major parts are copied from the MLkNNLearner and MultikNNClassifier.

Both ThreshMLkNNLearner and ThreshMLkNNClassifier correspond to MLkNNLearner and MLkNNClassifier
and implement the same interface except for the constructor of ThreshMLkNNLearner requiring 
additional parameter (a function calculating measure based on FN, TN, TP, FP).

The algorithm is implemented as described in: Michal Lukasik, Tomasz Kusmierczyk, Lukasz Bolikowski, 
Hung Son Nguyen. "Hierarchical, Multi-label Classification of Scholarly Publications: Modifications 
of ML-KNN Algorithm" Intelligent Tools for Building a Scientific Information Platform 2013: 343-363

Implementation based on Python2.7 and Orange2.6a2.
'''
import Orange.multilabel
import Orange.multilabel.multiknn as _multiknn
import measures

class TMLkNNLearner(Orange.multilabel.MLkNNLearner):
    """
    Class implementing the TMLkNN (Threshold Multi-Label k Nearest Neighbours)
    algorithm. 
    
    .. attribute:: measure
    
        Function, which based on FN, TN, TP, FP calculates classification measure. 
        Used in threshold selection.
        
    .. attribute:: k
    
        Number of neighbors. The default value is 1 
    
    .. attribute:: smooth
    
        Smoothing parameter controlling the strength of uniform prior 
        (Default value is set to 1 which yields the Laplace smoothing).
    
    .. attribute:: knn
        
        :class:`Orange.classification.knn.FindNearest` for nearest neighbor search
    
    """
    def __new__(cls, measure, instances = None, k=1, smooth = 1.0, weight_id = 0, **argkw):
        """
        Constructor of ThreshMLkNNLearner
        
        :param measure: a function, which based on FN, TN, TP, FP calculates classification measure. 
        Used in threshold selection.
        :type measure: function
        
        :param instances: a table of instances.
        :type instances: :class:`Orange.data.Table`
        
        :param k: number of nearest neighbors used in classification
        :type k: int
        
        :param smooth: Smoothing parameter controlling the strength of uniform prior 
        (Default value is set to 1 which yields the Laplace smoothing).
        :type smooth: Float
        
        :rtype: :class:`MLkNNLearner`
        """
        
        self = _multiknn.MultikNNLearner.__new__(cls, k, **argkw)
        self.measure = measure
        self.smooth = smooth
        
        if instances:
            self.__init__(**argkw)
            return self.__call__(instances,weight_id)
        else:
            return self

    @staticmethod
    def _get_basic_measures(c0, c1, thresh):
        """
        :param c0 array: an array, for each index stores number of negatives 
        with such a number of nearest neighbours with positive class.
        :param c1 array: an array, for each index stores number of positives 
        with such a number of nearest neighbours with positive class.
        :param thresh integer: indices from thresh on (from both c0 and c1) 
        are classified to be positive, the rest as negative.
        
        Returns: 
        :rtype: :quadruple of non-negative integers: False Negatives, 
        True Negatives, True Positives, False Positives
        """
        FN = sum(c1[:thresh])
        TN = sum(c0[:thresh])
        TP = sum(c1[thresh:])
        FP = sum(c0[thresh:])
        return FN, TN, TP, FP

    @staticmethod
    def _compute_thresholds(measure, k, instances, c0, c1):
        '''
        Calculate optimal thresholds by performing linear search.
        '''
        thresholds = {}
        for lvar in instances.domain.class_vars:
            thresholds[lvar] = -1
            bestv = -1
            for thresh in xrange(k+1):
                FN, TN, TP, FP = TMLkNNLearner._get_basic_measures(c0[lvar], c1[lvar], thresh)
                efficiency = measure(FN, TN, TP, FP)
                if efficiency > bestv:
                    bestv = efficiency
                    thresholds[lvar] = thresh
        return thresholds

    def __call__(self, instances, weight_id = 0, **kwds):
        if not Orange.multilabel.is_multilabel(instances):
            raise TypeError("The given data set is not a multi-label data set"
                            " with class values 0 and 1.")
        
        self.__dict__.update(kwds)
        self._build_knn(instances)

        #Computing the prior probabilities P(H_b^l)
        prior_prob = self.compute_prior(instances)
        
        #Computing the posterior probabilities P(E_j^l|H_b^l)
        p0, p1, c0, c1 = self.compute_cond(instances)
        cond_prob = [p0, p1]
        
        thresholds = TMLkNNLearner._compute_thresholds(self.measure, self.k, instances, c0, c1)
        
        return TMLkNNClassifier(instances = instances,
                               prior_prob = prior_prob, 
                               cond_prob = cond_prob,
                               thresholds = thresholds,
                               knn = self.knn,
                               k = self.k,
                               measure = self.measure)

    def compute_cond(self, instances):
        """ Compute posterior probabilities for each label of the training set. """
        k = self.k
        
        def _remove_identical(table, inst):
            try:
                i = [inst1.get_classes() == inst.get_classes() for inst1 in table].index(1)
            except:
                i = -1
            del table[i]
            return table
        
        neighbor_lists = [_remove_identical(self.knn(inst, k+1), inst) for inst in instances]
        p1 = [[0]*(k+1) for _ in instances.domain.class_vars]
        p0 = [[0]*(k+1) for _ in instances.domain.class_vars]

        c1 = {}
        c0 = {}

        for li, lvar in enumerate(instances.domain.class_vars):
            c  = [0] * (k + 1)
            cn = [0] * (k + 1)
            
            for inst, neighbors in zip(instances, neighbor_lists):
                delta = sum(n[lvar].value=='1' for n in neighbors)
                
                (c if inst[lvar].value == '1' else cn)[delta] += 1
                
            for j in range(k+1):
                p1[li][j] = float(self.smooth + c[j]) / (self.smooth * (k+1) + sum(c))
                p0[li][j] = float(self.smooth + cn[j]) / (self.smooth * (k+1) + sum(cn))
            c1[lvar] = c
            c0[lvar] = cn
        
        return p0, p1, c0, c1
 
class TMLkNNClassifier(_multiknn.MultikNNClassifier):      
    def __call__(self, instance, result_type=Orange.classification.Classifier.GetValue):
        """
        :rtype: a list of :class:`Orange.data.Value`, a list of 
        :class:`Orange.statistics.distribution.Distribution`, or a tuple with both
        """
        neighbors = self.knn(instance, self.k)
        
        labels = []
        dists = []
        
        for li, lvar in enumerate(self.instances.domain.class_vars):
            delta = sum(n[lvar].value=='1' for n in neighbors)
    
            #the following is the only added line to MLkNNClassifier.__call__ method:
            y = (delta >= self.thresholds[lvar])
            #in case a user requires probability, the same is returned as for MLKNN:
            p1 = self.prior_prob[li] * self.cond_prob[1][li][delta]
            p0 = (1-self.prior_prob[li]) * self.cond_prob[0][li][delta]
            labels.append(Orange.data.Value(lvar, str(int(y))))
            
            r = p1 / (p0+p1)
            dists.append( Orange.statistics.distribution.Discrete([1-r, r]) )
       
        for d, lvar in zip(dists, self.instances.domain.class_vars):
            d.variable = lvar
        
        if result_type == Orange.classification.Classifier.GetValue:
            return labels
        if result_type == Orange.classification.Classifier.GetProbabilities:
            return dists
        return labels, dists
        
#########################################################################################
# Test the code, run from DOS prompt
# assume the data file is in proper directory

if __name__ == "__main__":
    data = Orange.data.Table("emotions.tab")

    classifier = TMLkNNLearner(measures.acc, data,5,1.0)
    for i in range(10):
        c,p = classifier(data[i],Orange.classification.Classifier.GetBoth)
        print c,p

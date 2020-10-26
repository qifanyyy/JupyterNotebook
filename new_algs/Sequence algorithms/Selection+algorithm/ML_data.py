import numpy as np
from sklearn.ensemble import RandomForestClassifier
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD
from sklearn import svm

from sklearn import metrics
from ML_test import ML_test 


class ML_instance:
    def __init__ (self, d, l, t_indices, te_indices):
        self.data = d
        self.labels = np.array(l)
        self.train_indices = t_indices
        self.test_indices = te_indices
        self.features = range(len(self.data.columns))
        #self.features = self.features[:100]
        #self.features = self.features[:20]
    
        
    def initialize_nn(self, frame_size):
        #code from https://vkolachalama.blogspot.pt/2016/05/keras-implementation-of-mlp-neural.html
#        model = Sequential() # The Keras Sequential model is a linear stack of layers.
#        model.add(Dense(100, init='uniform', input_dim=frame_size)) # Dense layer
#        model.add(Activation('tanh')) # Activation layer
#        model.add(Dropout(0.5)) # Dropout layer
#        model.add(Dense(100, init='uniform')) # Another dense layer
#        model.add(Activation('tanh')) # Another activation layer
#        model.add(Dropout(0.5)) # Another dropout layer
#        model.add(Dense(2, init='uniform')) # Last dense layer
#        model.add(Activation('softmax')) # Softmax activation at the end
#        sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True) # Using Nesterov momentum
#        model.compile(loss='binary_crossentropy', optimizer=sgd, metrics=['accuracy']) # Using logloss
        model = Sequential([
            Dense(75, input_dim=frame_size),
            Dropout(0.5),
            Dense(50, init='uniform'),
            Activation('tanh'),
            Dense(2, init='normal', activation='sigmoid'),
            Activation('softmax'),
        ])
        model.compile(loss='sparse_categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

        return model
        
    def mlp_evaluator (self, subset):
        model = self.initialize_nn(len(subset))
        scores = []
        sample_data = self.data.ix[:,subset]
        for i in range(len(self.train_indices)):
            train_data = sample_data.ix[self.train_indices[i]] ##train sample data
            train_labels = self.labels[self.train_indices[i]] ##train labels
            
            
            test_data = sample_data.ix[self.test_indices[i]] ##test data
            test_labels = self.labels[self.test_indices[i]] ##test labels
            
            train_labels = train_labels.reshape((-1, 1))
            train_data = train_data.as_matrix()
            test_data = test_data.as_matrix()
            
            
            #model.fit(train_data, train_labels)
            model.fit(train_data, train_labels, batch_size=32, nb_epoch=10000, verbose=1, callbacks=[], validation_split=0.2, validation_data=None, shuffle=True, class_weight=None, sample_weight=None)
            
            #clf.fit(train_data, train_labels) ##train model
            #pred_labels = clf.predict(test_data)
            pred_scores = model.predict(test_data)
            print (pred_scores)
            print len(pred_scores), " ", len(test_labels)
            quit()
            acc = round(metrics.accuracy_score(test_labels, pred_labels), 6)
            #print acc
            scores.append(acc)
        score = round(sum(scores)/len(scores),4)
        return score

    def svm_evaluator (self, subset):
        clf = svm.SVC(kernel="linear")
        scores = []
        #print "subset ", subset
        sample_data = self.data.ix[:,subset]
        for i in range(len(self.train_indices)):
            train_data = sample_data.ix[self.train_indices[i]] ##train sample data
            train_labels = self.labels[self.train_indices[i]] ##train labels
            
            test_data = sample_data.ix[self.test_indices[i]] ##test data
            test_labels = self.labels[self.test_indices[i]] ##test labels
            
            clf.fit(train_data, train_labels) ##train model
            pred_labels = clf.predict(test_data)
            
            acc = round(metrics.accuracy_score(test_labels, pred_labels), 6)
            #print acc
            scores.append(acc)
        score = round(sum(scores)/len(scores),4)
        return score
    
       
       
    def rf_evaluator (self, subset):
        rf = RandomForestClassifier(n_estimators = 1)
        scores = []
        #print "subset ", subset
        sample_data = self.data.ix[:,subset]
        for i in range(len(self.train_indices)):
            train_data = sample_data.ix[self.train_indices[i]] ##train sample data
            train_labels = self.labels[self.train_indices[i]] ##train labels
            
            test_data = sample_data.ix[self.test_indices[i]] ##test data
            test_labels = self.labels[self.test_indices[i]] ##test labels
            
            rf.fit(train_data, train_labels) ##train model
            pred_labels = rf.predict(test_data)
            
            acc = round(metrics.accuracy_score(test_labels, pred_labels), 6)
            #print acc
            scores.append(acc)
        score = round(sum(scores)/len(scores),4)
        return score
            

    ## it receis a ML_test class
    def generator(self, tester):
        sorted_results = sorted(tester.round_results, key=lambda tup: tup[0])
        sorted_results.reverse()
        continue_search = False
        #if previous_best[-1][0] < (sorted_results[0][0] + 0.05): ##continuing search condition
        #    continue_search = True
        if len(sorted_results[0][1]) < 50: ##5 for fastertesting
            continue_search = True
        ## merge top results
        aux = tester.best_results + tester.round_results
        aux = sorted(aux, key = lambda tup: tup[0])
        aux.reverse()
        tester.best_results = aux[:10] ##number of best scores to save
        tester.round_subsets = []
        tester.round_results = []
        if not continue_search:
            return tester
        
        top_subsets_round = [x[1] for x in sorted_results[:5]] ## get the top ten sets
        for subset in top_subsets_round:
            tester.expanded.append(subset)
            for i in self.features:
                if i not in subset:
                    sub = subset + [i]
                    sub.sort()
                    aux = [str(x) for x in sub]
                    aux = ",".join(aux)
                    if aux not in tester.history:
                        tester.round_subsets.append(sub) ##add subset for next round
                        tester.history[aux] = True ##add subset to the testing
        return tester
        
            
    def generate_successors(self, subset, history):
        work = []
        for i in self.features:
            if i not in subset:
                sub = subset + [i]
                sub.sort()
                aux = [str(x) for x in sub]
                aux = ",".join(aux)
                if aux not in history:
                    work.append(sub) ##add subset for next round
                    history[aux] = True ##add subset to the testing
        return work
        
    
        
        
      
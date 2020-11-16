"""
A Machine Learning Framework for Stock Selection

Authors:
XingYu Fu; JinHong Du; YiFeng Guo; MingWen Liu; Tao Dong; XiuWen Duan; 

Institutions:
AI&Fintech Lab of Likelihood Technology; 
Gradient Trading;
Sun Yat-sen University;

Contact:
fuxy28@mail2.sysu.edu.cn

All Rights Reserved.
"""


"""Import Modules"""
# Numerical Computation
import numpy as np
from sklearn.metrics import roc_auc_score
# Plot
import matplotlib.pyplot as plt
# Deep Learning
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers.normalization import BatchNormalization
from keras import regularizers
from keras.optimizers import SGD
from keras.utils import to_categorical
# Random Forest 
from sklearn.ensemble import RandomForestRegressor

class EvaluationClass:
    def __init__( self, X_train, Y_train, X_test, Y_test, model_type, save_computaion=False):
        
        if model_type == 1: # Logistic Regression
            input_shape = np.shape(X_train)[1]
            model = Sequential()
            model.add(Dense(1, input_dim=input_shape, activation='sigmoid'))
            sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
            model.compile(loss='binary_crossentropy', optimizer=sgd, metrics=['accuracy'])
            self.model = model
            self.Y_train = Y_train
            self.Y_test = Y_test
            self.X_train = X_train
            self.X_test = X_test
            
        elif model_type == 2: # Deep Learning Model
            input_shape = np.shape(X_train)[1]
            model = Sequential()
            model.add(Dense(input_shape//2, activation='relu', input_dim=input_shape , kernel_regularizer=regularizers.l2(0.01) ) )
            model.add(Dropout(0.5))
            model.add(Dense(input_shape//4, activation='relu', kernel_regularizer=regularizers.l2(0.01)))
            model.add(BatchNormalization())
            model.add(Dense(2, activation='softmax', kernel_regularizer=regularizers.l2(0.01)))
            sgd = SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True) 
            model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
            self.model = model
            self.Y_train = to_categorical(Y_train, num_classes=2)
            self.Y_test = to_categorical(Y_test, num_classes=2)
            self.X_train = X_train
            self.X_test = X_test

        elif model_type == 3: # Random Forest
            model = RandomForestRegressor(n_estimators = 100, max_depth = 4)
            self.model = model
            self.Y_train = Y_train
            self.Y_test = Y_test  
            self.X_train = X_train
            self.X_test = X_test
            
        else : # Stacking
            # NN
            input_shape = np.shape(X_train)[1]
            train_sample_num = np.shape(X_train)[0]
            model1 = Sequential()
            model1.add(Dense(input_shape//2, activation='relu', input_dim=input_shape, kernel_regularizer=regularizers.l2(0.01)))
            model1.add(Dropout(0.5))
            model1.add(Dense(input_shape//4, activation='relu', kernel_regularizer=regularizers.l2(0.01)))
            model1.add(BatchNormalization())
            model1.add(Dense(2, activation='softmax', kernel_regularizer=regularizers.l2(0.01)))
            sgd = SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True) 
            model1.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
            self.model1 = model1
            self.X_train1 = X_train[:-train_sample_num//5]
            self.Y_train1 = to_categorical(Y_train, num_classes=2)[:-train_sample_num//5]
            # RF
            model2 = RandomForestRegressor(n_estimators = 100, max_depth = 4)
            self.model2 = model2
            self.X_train2 = X_train[:-train_sample_num//5]
            self.Y_train2 = Y_train[:-train_sample_num//5]
            # Logstic
            model3 = Sequential()
            model3.add(Dense(1, input_dim=2, activation='sigmoid'))
            sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
            model3.compile(loss='binary_crossentropy', optimizer=sgd, metrics=['accuracy'])
            self.model3 = model3
            self.X_train3 = X_train[-train_sample_num//5:]
            self.Y_train3 = Y_train[-train_sample_num//5:]
            self.X_test = X_test
            self.Y_test = Y_test

        self.model_type = model_type
        self.save_computaion = save_computaion
    
    
    """Definition of the Back Test System"""
    def evalu_sta(self):
    
        """*********************Training*********************"""    
        if (self.model_type == 1) or (self.model_type == 2):
            if self.save_computaion: # For GA Feature Selection
                self.model.fit(self.X_train, self.Y_train, epochs=5, batch_size=128, verbose=0)
            else:
                self.model.fit(self.X_train, self.Y_train, epochs=20, batch_size=128, verbose=1)
        elif self.model_type == 3:
            self.model.fit(self.X_train, self.Y_train)
        else:
            self.model1.fit(self.X_train1, self.Y_train1, epochs=20, batch_size=128, verbose=0)
            self.model2.fit(self.X_train2, self.Y_train2)
            Y1 = self.model1.predict( self.X_train3 )[:,1]
            Y2 = self.model2.predict( self.X_train3 )
            X3 = np.array( [ [ Y1[i], Y2[i]] for i in range(len(Y1))] )
            self.model3.fit(X3, self.Y_train3, epochs=30, batch_size=128, verbose=1)
    
    
        """*********************Prediction*********************"""
        if self.model_type == 1 or self.model_type == 3:
            Y_continuous = self.model.predict( self.X_test )
            Y_test = self.Y_test
        elif self.model_type == 2:
            Y_continuous = self.model.predict( self.X_test )[:,1]
            Y_test = self.Y_test[:,1]
        else:
            Y_continuous1 = self.model1.predict( self.X_test )[:,1]
            Y_continuous2 = self.model2.predict( self.X_test )
            X3 = np.array( [ [ Y_continuous1[i], Y_continuous2[i]] for i in range(len(Y_continuous1))] )
            Y_continuous = self.model3.predict( X3 )
            Y_test = self.Y_test
        Y_discrete = np.round( Y_continuous )
    
        """*********************Statistical Evaluating*********************"""
        if self.save_computaion:
           # AUC
            AUC = roc_auc_score(Y_test, Y_continuous)
            return AUC 
        else:
            # TP; FP; FN; TN
            TP, FP, FN, TN = 0, 0, 0, 0
            for i in range( len(Y_discrete) ):
                if Y_discrete[i] == Y_test[i]:
                    if Y_discrete[i] == 1: 
                        TP += 1
                    else:
                        TN += 1
                else:
                    if Y_discrete[i] == 1:
                        FP += 1
                    else:
                        FN += 1
            
            # Accuracy
            Accuracy = (TP+TN)/(TP+TN+FP+FN)
            # Precision
            Precision = TP/(TP+FP) 
            #Recall
            Recall = TP/(TP+FN)
            # F1-score
            F1 = 2*Precision*Recall/(Precision+Recall)
            # TPR
            TPR = TP/(TP+FN)
            # FPR
            FPR = FP/(FP+TN)
            # AUC
            AUC = roc_auc_score(Y_test, Y_continuous)
            return Accuracy, Precision, Recall, F1, TPR, FPR, AUC
        
    def evalu_por( X_test_portfolio, X_test_portfolio_masked, Y_test_portfolio, model_collection, Q, Start_date):
        
        figure = (plt.figure(figsize=(15,6))).add_subplot(111)
        for i in range(len(model_collection)):
            name, model = model_collection[i]
            if i<=3:
                X = X_test_portfolio
            else:
                X = X_test_portfolio_masked
            if model.model_type == 1 or model.model_type == 3:
                Y_continuous = model.model.predict( X )
            elif model.model_type == 2:
                Y_continuous = model.model.predict( X )[:,1]
            else:
                Y_continuous1 = model.model1.predict( X )[:,1]
                Y_continuous2 = model.model2.predict( X )
                X3 = np.array( [ [ Y_continuous1[i], Y_continuous2[i]] for i in range(len(Y_continuous1))] )
                Y_continuous = model.model3.predict( X3 )
            
            ranking = (-Y_continuous).argsort()
            ranking = ranking[ 0 :np.int( np.round(Q*len(Y_test_portfolio))) ]
            if i == 0 or i == 3 or i == 4 or i==7:
                Y_continuous = np.array([ ( Y_continuous[i][0] if (i in ranking) else 0 ) for i in range(len(Y_continuous))])
            else:
                Y_continuous = np.array([ ( Y_continuous[i] if (i in ranking) else 0 ) for i in range(len(Y_continuous))])
                
            Y_continuous = Y_continuous/sum(Y_continuous)
            curve = EvaluationClass._curve( Y_continuous, Y_test_portfolio)
            figure.plot( curve , label = name )
        Y_continuous = np.ones( len(Y_test_portfolio) ) / len(Y_test_portfolio)
        curve = EvaluationClass._curve( Y_continuous, Y_test_portfolio)
        figure.plot( curve , label = "Average" )
        plt.title("Start Date:" + Start_date )
        plt.xlabel("Time")
        plt.ylabel("Asset Value")
        box = figure.get_position()
        figure.set_position([box.x0,box.y0,box.width*0.8,box.height])
        figure.legend(loc='center left',bbox_to_anchor=(1.0,0.5))
        plt.savefig(Start_date+".png",dpi=300)
        plt.show() 
        
    def _curve( portfolio, price):
        total = 100000
        curve = []
        curve.append( total )
        for i in range( len(price[0])-1 ):
            fluctuation = np.array( [ p[i+1]/p[i] for p in price] )
            total = total*np.dot(portfolio, fluctuation)
            curve.append(total)
        return curve

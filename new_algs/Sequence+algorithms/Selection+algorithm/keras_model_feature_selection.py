#!/usr/bin/python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
from sklearn.model_selection import StratifiedKFold, KFold, train_test_split
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, LeakyReLU
from keras.layers.normalization import BatchNormalization
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.optimizers import SGD
from keras.utils import plot_model
from keras import backend as K
import random
from genetic import Genetic

random.seed()
np.random.seed()

###################################################
#function calculate model for set of features (tab)
###################################################
def modelCV(x, y, tab):
    train = np.random.random_integers( 0, x.shape[0]-1, 500000 )
    model = Sequential()
    model.add(Dense(64, activation='relu', input_dim = np.count_nonzero(tab)))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy',
                optimizer='adam', metrics=['accuracy'])
    callback = [EarlyStopping(monitor='val_loss', patience=3),
                 ModelCheckpoint(filepath='temp_model.h5', monitor='val_loss')]
    history = model.fit(x.iloc[train, tab==1].values, y.iloc[train].values,
                        validation_split=0.2, epochs=50, callbacks=callback, verbose=0)
    result = history.history['val_loss'][-5]
    accuracy = history.history['val_acc'][-5]
    K.clear_session()
    return result, accuracy

###########################
#getting and preparing data
###########################
data_org=pd.read_csv("Downstream_trigger/rawdata.txt",sep="	", header=None)
data = pd.DataFrame(np.array(data_org)[:,1:-1])
columns=["seed_chi2PerDoF", "seed_p", "seed_pt", "seed_nLHCbIDs",
        "seed_nbIT", "seed_nLayers", "seed_x", "seed_y",
         "seed_tx", "seed_ty"]
data[data.shape[1]] = np.sqrt(data[6]*data[6]+data[7]*data[7])
columns.append('seed_r')
data[data.shape[1]] = np.arctan(data[7]/data[6])
columns.append('seed_angle')
data[data.shape[1]] = np.arctanh(data[2]/data[1])
columns.append('seed_pseudorapidity')
data[1] = np.log(data[1])
data[2] = np.log(data[2])
data.columns = columns

sc = preprocessing.StandardScaler()
data = pd.DataFrame(sc.fit_transform(data))

x = pd.DataFrame(np.array(data[:]))
y = pd.DataFrame(np.array(data_org)[:,0])

########################################################
#model with feature selection based on genetic algorithm
########################################################
gen = Genetic( features = x.columns.size, parents = 5, children = 30, mutation_scale = 0.05 )
gen.fit(x, y, 10, modelCV)
print('\n\nGenetic algorithm\nNumber of features %d \nError %.3f \nAccuracy %.3f\n' % (np.count_nonzero(gen.tab[0]), gen.best[-1][0], gen.best[-1][1]))

print('\n============================\n')
print('Set of features from last generation')
print(gen.tab)
print('\n-----------\n')
print('Results of features from last generation (loss)')
print(gen.results)

#ploting results of dimensionality reduction
plt.plot(gen.best.T[0], 'b-')
plt.plot(gen.mean_.T[0], 'r-')
plt.legend(['best', 'mean'])
plt.title('Generic algorithm')
plt.xlabel('generation')
plt.ylabel('loss')
plt.show()

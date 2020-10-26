# Pre_compress.py: implelement different reduction methods for dimensional reduction
#  including PCA, KernelPCA, FactorAnalysis, TruncatedSVD, RandomizedPCA, FastICA,
# MiniBatchSparsePCA, NMF
# Tri Doan
# Date: Jan 21, 2015 , last updated: May 9, 2015
 
import csv
import timeit
import numpy as np
import pandas as pd
from numpy.random import RandomState
from os import listdir
from os.path import isfile, join
from sklearn.decomposition import PCA, KernelPCA, FactorAnalysis, TruncatedSVD, RandomizedPCA, FastICA, NMF
from sklearn.preprocessing import StandardScaler
# http://scikit-learn.org/stable/modules/decomposition.html



def read_csv(file_path, has_header = True):
    """
    read data from csv file path, file required to preprocess if needed and contains only numeric value
    """
    with open(file_path) as f:
        if has_header:  f.readline()
        data = []
        target =[]
        for line in f:
            line = line.strip().split(",")
            data.append([float(x) for x in line[:-1]])
            target.append([line[-1]])
    return data, target

def csv_writer(file_path, data):
    """
    Write data to a CSV file path
    """
    with open(file_path, "a+") as f:
        #writer = csv.writer(f, delimiter=',')
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(data)
    f.close()        

print ('Enter a number of dimension to reduce to: ')
s = raw_input()       
n_attr =int(s)

rng = RandomState(0)
csvfiles = [ f for f in listdir('../no-compress') if isfile(join('../no-compress',f)) and f.endswith(".csv")]

for file in csvfiles :
   runTime=[]
   data,target  = read_csv(join('../no-compress',file))    
   start = timeit.default_timer()
   
   # scale data 
   
   data_scaler = StandardScaler()
   data = data_scaler.fit_transform(data)
   #target = target_scaler.fit_transform(target)
   
  # 1. Implement Probabilistic PCA
   pca = PCA(n_components=n_attr) 
   pca.fit(data)
   dat = pca.transform(data)
   number =1
      #data = np.concatenate([data,target],axis=1)
   # convert to Pandas data frame and write to file
   dat = pd.DataFrame(dat)
   tar = pd.DataFrame(target)
   dta = pd.concat([dat,tar],axis=1)
   header = ['att' +`i` for i in range(n_attr) ]+['Class']
   dta.columns = header
   dta.to_csv(join('../PCA','PCA'+`n_attr`+file),index=False)
   runTime.append(['PCA'+file,timeit.default_timer() - start ])
   start = timeit.default_timer()
   print(' 1. Complete Probabilistic PCA') 
   
   csv_writer("../compresstimeMore.csv",runTime)
   print (' complete PCA and FICA compression methods ',file)  
   
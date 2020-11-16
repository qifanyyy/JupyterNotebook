# generatData.py: Create synthetic/ artificial data using make_classification
# Date: Sept 7
#  Tri Doan
# ver 1.2 allows random number of features, target classes

from sklearn.datasets import make_classification
from sklearn.datasets import make_multilabel_classification
from sklearn.datasets import make_blobs
from pandas import DataFrame, read_csv
from random import randint
import random

# default 4 features
n_f =4
try:
    n_f=int(raw_input('Enter the maximum number of features (default 2): '))
except ValueError:
    print ("Default 4 features will be created")
n_df = 10
try:
    n_df = int(raw_input('Enter the number of synthesis data '))
except ValueError:
    print ("Default 10 artificial data will be used")

ntypes=2
try:
    ntypes = int(raw_input('Enter the maximum number of target classes (default 2)'))
except ValueError:
    print ("Default 2 classes will be created")

def create_synthesis_data(path,nfea,ntypes):
   nfea   = random.randrange(2,nfea+1)
   ntypes = random.randrange(2,ntypes+1)
   nInst  = random.randrange(1000,6000)
   #nexamples = random.randrange(100,50000+1)
   X1, Y1 = make_classification(random_state=2,n_samples=nInst,n_features=nfea, n_redundant=0, n_classes=ntypes,n_clusters_per_class=1,n_informative=nfea)
   #X1, Y1 = make_multilabel_classification(n_features=nfea, n_classes=ntypes,n_labels=8)
   #X1, Y1 = make_blobs(n_samples=nexamples,n_features=nfea, shuffle= True)
   attr   = {}
   for id in range(nfea):
      attr['att%d' %id]=[X1[i][id] for i in range(len(Y1)) ]
   attr['class'] = Y1.tolist()
   #attr.append('class');   
   df = DataFrame(attr)
   df.to_csv(path,index=False,header=True)
   return True


n_ch = len(str(n_df))

for id in range(n_df):
        #path='c:/AlgoSelecMeta/data/df%d.csv' %id
        path= 'c:/AlgoSelecMeta/SyntheticTest/art%s.csv' %str(id).zfill(n_ch)
        if not create_synthesis_data(path,n_f,ntypes):
           print ('Error in creating file')
           break
print ('%d have been created ' %n_df)             
        
    
# attr.keys()
#len(attr['at0'])
#val0 = [X1[i][0] for i in range(size(Y1)) ]
#val1 = [X1[i][1] for i in range(size(Y1)) ]





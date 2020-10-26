from astropy.table import Table
import numpy as np
import matplotlib.pyplot as plt

# Read in training file
data = Table.read('GTR-ADM-QSO-ir-testhighz_findbw_lup_2016_starclean.fits')
Xtrain = np.vstack([ data['ug'], data['gr'], data['ri'], data['iz'], data['zs1'], data['s1s2']]).T
ytrain = np.array(data['labels'])

# Read in test file
data2 = Table.read('GTR-ADM-QSO-ir_good_test_2016.fits')

# Limit test file to Stripe 82 area
ramask = ( ( (data2['ra']>=300.0) & (data2['ra']<=360.0) ) | ( (data2['ra']>=0.0) & (data2['ra']<=60.0) ) )
decmask = ((data2['dec']>=-1.5) & (data2['dec']<=1.5))
dataS82 = data2[ramask & decmask]

# Create test input for sklearn
Xtest = np.vstack([ dataS82['ug'], dataS82['gr'], dataS82['ri'], dataS82['iz'], dataS82['zs1'], dataS82['s1s2']]).T

# "Whiten" the data (both test and training)
from sklearn.preprocessing import StandardScaler 
scaler = StandardScaler()
scaler.fit(Xtrain)  # Use the full training set now
XStrain = scaler.transform(Xtrain)
XStest = scaler.transform(Xtest)

# Instantiate the RF classifier
from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier(n_estimators=10, max_depth=15, min_samples_split=2, n_jobs=-1, random_state=42)
rfc.fit(XStrain, ytrain)

# Determine RF classifications for the test set
ypredRFC = rfc.predict(XStest)


# Instantiate the SVM classifier
from sklearn.svm import SVC
svm = SVC(random_state=42)
svm.fit(XStrain,ytrain)

# Use dask to determing the SVM classifications for the test set

from dask import compute, delayed
import dask.threaded

def processSVM(Xin):
    return svm.predict(Xin)

# Create dask objects
dobjsSVM = [delayed(processSVM)(x.reshape(1,-1)) for x in XStest]

# Actually determine the SVM classifications
ypredSVM = compute(*dobjsSVM, get=dask.threaded.get)

# Reformat the SVM classification output.
ypredSVM = np.array(ypredSVM).reshape(1,-1)[0]


# Instantiate the bagging classifier
from sklearn.ensemble import BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
bag = BaggingClassifier(KNeighborsClassifier(n_neighbors=5), max_samples=0.5, max_features=1.0, n_jobs=-1)
bag.fit(XStrain, ytrain)

# Use dask to determing the bagging classifications for the test set

def processBAG(Xin):
    return bag.predict(Xin)

# Create dask objects
dobjsBAG = [delayed(processBAG)(x.reshape(1,-1)) for x in XStest]

# Actually determine the bagging classifications
ypredBAG = compute(*dobjsBAG, get=dask.threaded.get)

# Reformat the bagging classification output.
ypredBAG = np.array(ypredBAG).reshape(1,-1)[0]


# Add classifications to data array and write output file
dataS82['ypredRFC'] = ypredRFC
dataS82['ypredSVM'] = ypredSVM
dataS82['ypredBAG'] = ypredBAG
dataS82.write('GTR-ADM-QSO-ir_good_test_2016_out_Stripe82all.fits', format='fits')

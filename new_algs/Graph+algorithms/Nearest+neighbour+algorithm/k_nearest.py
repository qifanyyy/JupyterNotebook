import pickle


def predict(data):
    clf_pckl = open('k_clus.pkl', 'rb')
    clf = pickle.load(clf_pckl)
    prediction = clf.predict(data)
    return prediction

#import numpy as np
#from sklearn import preprocessing, cross_validation, neighbors


#The code block below was used for feature extraction during training of the classifier.The required moduls are commented out at the top of this file
#----------------------------------------------------------------------------------------------------------------------
#def run(data,labels):
#    x = np.array(data)
#    y = np.array(labels)
#    #shakeup
#    X_train, X_test, y_train, y_test = cross_validation.train_test_split(x, y, test_size=0.2)
#     #Using standard Kneighbours classifier algorithm
#    clf = neighbors.KNeighborsClassifier()
#    clf.fit(X_train, y_train)
#    with open('k_clus.pkl', 'wb') as f:
#        pickle.dump(clf, f,protocol=2)
#    accuracy = clf.score(X_test, y_test)
#    return accuracy
#-----------------------------------------------------------------------------------------------------------------------


    
    
    
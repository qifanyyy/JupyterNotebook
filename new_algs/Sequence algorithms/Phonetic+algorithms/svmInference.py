from numpy import *
import pandas as pd
from sklearn import svm
from sklearn.metrics import adjusted_rand_score
from multiprocessing import Pool
import igraph
import random
igraph.set_random_number_generator(random)
import numpy.random as nprandom
from collections import defaultdict

try:
    os.stat('inferredCC')
except:
    os.mkdir('inferredCC')       


def infomap_clustering(threshold, matrix, taxa=False, revert=False):
    """
    Compute the Infomap clustering analysis of the data.

    Parameters
    ----------
    threshold : float
        The threshold for clustering you want to use.
    matrix : list
        The two-dimensional matrix passed as list or array.
    taxa : list
        The list of taxon names. If set to "False" a fake list of taxon names
        will be created, giving a positive numerical ID in increasing order for
        each column in the matrix.
    revert : bool
        If set to "False", don't return taxon names but simply the language
        identifiers and their labels as a dictionary. Otherwise returns a
        dictionary with labels as keys and list of taxon names as values.
    
    Requires
    --------
    The igraph package is required, downloadable from http://igraph.org/.

    Returns
    -------
    clusters : dict
        Either a dictionary of taxon identifiers and labels, or a dictionary of
        labels and taxon names.

    Notes
    -----
    Infomap clustering is a community detection method originally proposed by
    :evobib:`Rosvall2008`.
    """
    if not igraph:
        raise ValueError("The package igraph is needed to run this analysis.")
    if not taxa:
        taxa = list(range(1, len(matrix) + 1))

    G = igraph.Graph()
    vertex_weights = []
    for i in range(len(matrix)):
        G.add_vertex(i)
        vertex_weights += [0]
    
    # variable stores edge weights, if they are not there, the network is
    # already separated by the threshold
    for i,row in enumerate(matrix):
        for j,cell in enumerate(row):
            if i < j:
                if cell <= threshold:
                    G.add_edge(i, j)
     
    comps = G.community_infomap(edge_weights=None,
            vertex_weights=None)
    D = {}
    for i,comp in enumerate(comps.subgraphs()):
        vertices = [v['name'] for v in comp.vs]
        for vertex in vertices:
            D[vertex] = i+1

    if revert:
        return D

    clr = defaultdict(list)
    for i,t in enumerate(taxa):
        clr[D[i]] += [t]
    return clr




dDict = {'gloss':unicode,
         'l1':unicode,
         'w1':unicode,
         'cc1':unicode,
         'l2':unicode,
         'w2':unicode,
         'cc2':unicode,
         'feature1':double,
         'feature2':double,
         'feature3':double,
         'feature4':double,
         'feature5':double,
         'lexstat_simAA':double,
         'lexstat_simBB':double,
         'lexstat_simAB':double,
         'feature7':double,
         'target':int,
         'db':unicode}

# read in training data
training = pd.read_csv('trainingData.csv',encoding='utf-8',
                       dtype=dDict)

# compute feature 8
training['feature8'] = 1-((2*training.lexstat_simAB)/(training.lexstat_simAA+training.lexstat_simBB))


# select relevant subset of features
# for feature selection, simply alter this list
features = [
    'feature1',
    'feature4',
    'feature6',
    'feature7',
    'feature8',
    ]

nprandom.seed(1234)
random.seed(1234)
trainingVectors = training.ix[nprandom.permutation(training.index)].drop_duplicates(['db','gloss'])


# vdb is the validation data base, the rest of the training data bases
# are used for training
def svmInfomapCluster(vdb,featureSubset=features,th=.34,C=.82,kernel='linear',gamma=1E-3):
    newWordList = pd.DataFrame()
    fitting = trainingVectors[trainingVectors.db!=vdb]
    validation = training[training.db==vdb].copy()
    X = fitting[featureSubset].values
    y = fitting.target.values
    svClf = svm.SVC(kernel=kernel,C=C,gamma=gamma,
                    probability=True)
    svClf.fit(X,y)
    nprandom.seed(1234)
    random.seed(1234)
    svScores = svClf.predict_proba(validation[featureSubset].values)[:,1]
    validation['svScores'] = svScores
    scores = pd.DataFrame()
    wordlist = pd.DataFrame()
    concepts = validation.gloss.unique()
    taxa = unique(validation[['l1','l2']].values.flatten())
    dataWordlist = vstack([validation[['gloss','l1','w1','cc1']].values,
                           validation[['gloss','l2','w2','cc2']].values])
    dataWordlist = pd.DataFrame(dataWordlist,columns=['concept','doculect',
                                                      'counterpart','cc'])
    dataWordlist = dataWordlist.drop_duplicates()
    dataWordlist.index = ['_'.join(map(unicode,x))
                          for x in
                          dataWordlist[['concept','doculect','counterpart']].values]
    validation['id_1'] = [c+'_'+l+'_'+unicode(w)
                      for (c,l,w) in validation[['gloss','l1','w1']].values]
    validation['id_2'] = [c+'_'+l+'_'+unicode(w)
                      for (c,l,w) in validation[['gloss','l2','w2']].values]
    for c in concepts:
        dataC= validation[validation.gloss==c].copy()
        dataC['id_1'] = [x.replace(' ','').replace(',','') for x in dataC.id_1]
        dataC['id_2'] = [x.replace(' ','').replace(',','') for x in dataC.id_2]
        wlC = dataWordlist[dataWordlist.concept==c].copy()
        if len(wlC)>1:
            wlC.index = [x.replace(' ','').replace(',','') for x in wlC.index]
            svMtx = zeros((len(wlC.index),len(wlC.index)))
            svMtx[pd.match(dataC.id_1,wlC.index),
                     pd.match(dataC.id_2,wlC.index)] = dataC.svScores.values
            svMtx[pd.match(dataC.id_2,wlC.index),
                     pd.match(dataC.id_1,wlC.index)] = dataC.svScores.values
            svDistMtx = log(1-svMtx)
            tth = log(th)-svDistMtx.min()
            svDistMtx -= svDistMtx.min()
            fill_diagonal(svDistMtx,0)
            pDict = infomap_clustering(tth,svDistMtx)
            pArray = vstack([c_[pDict[k],[k]*len(pDict[k])] for k in pDict.keys()])
            partitionIM = pArray[argsort(pArray[:,0]),1]
        else:
            partitionIM = array([1])
        wlC['inferredCC'] = [vdb+':'+c+':'+str(x) for x in partitionIM]
        wlC['db'] = vdb
        newWordList = pd.concat([newWordList,wlC])
    newWordList.index = arange(len(newWordList))
    return newWordList


# cross-validation over training data
def f(x):
    return svmInfomapCluster(x)
pool = Pool()
totalCC = pool.map(f,training.db.unique())
pool.close()
pool.terminate()

for db,wl in zip(training.db.unique(),totalCC):
    wl['fullCC'] = [':'.join(x) for x in wl[['db','concept','cc']].values]
    wl[['db','concept','doculect',
        'counterpart','fullCC','inferredCC']].to_csv('inferredCC/'+db+'.svmCC.csv',
                                                     encoding='utf-8',index=False)


test = pd.read_csv('testData.csv',encoding='utf-8',
                       dtype=dDict)

test['feature8'] = 1-((2*test.lexstat_simAB)/(test.lexstat_simAA+test.lexstat_simBB))


# inference on test data
def testCluster(vdb,featureSubset=features,C=0.82,gamma=9e-04,kernel='linear',th=.34):
    newWordList = pd.DataFrame()
    fitting = trainingVectors
    validation = test[test.db==vdb].copy()
    X = fitting[featureSubset].values
    y = fitting.target.values
    svClf = svm.SVC(kernel=kernel,C=C,gamma=gamma,
                    probability=True)
    svClf.fit(X,y)
    svScores = svClf.predict_proba(validation[featureSubset].values)[:,1]
    validation['svScores'] = svScores
    scores = pd.DataFrame()
    wordlist = pd.DataFrame()
    concepts = validation.gloss.unique()
    taxa = unique(validation[['l1','l2']].values.flatten())
    dataWordlist = vstack([validation[['gloss','l1','w1','cc1']].values,
                           validation[['gloss','l2','w2','cc2']].values])
    dataWordlist = pd.DataFrame(dataWordlist,columns=['concept','doculect',
                                                      'counterpart','cc'])
    dataWordlist = dataWordlist.drop_duplicates()
    dataWordlist.index = ['_'.join(map(unicode,x))
                          for x in
                          dataWordlist[['concept','doculect','counterpart']].values]
    validation['id_1'] = [c+'_'+l+'_'+unicode(w)
                      for (c,l,w) in validation[['gloss','l1','w1']].values]
    validation['id_2'] = [c+'_'+l+'_'+unicode(w)
                      for (c,l,w) in validation[['gloss','l2','w2']].values]
    for c in concepts:
        dataC= validation[validation.gloss==c].copy()
        dataC['id_1'] = [x.replace(' ','').replace(',','') for x in dataC.id_1]
        dataC['id_2'] = [x.replace(' ','').replace(',','') for x in dataC.id_2]
        wlC = dataWordlist[dataWordlist.concept==c].copy()
        if len(wlC)>1:
            wlC.index = [x.replace(' ','').replace(',','') for x in wlC.index]
            svMtx = zeros((len(wlC.index),len(wlC.index)))
            svMtx[pd.match(dataC.id_1,wlC.index),
                     pd.match(dataC.id_2,wlC.index)] = dataC.svScores.values
            svMtx[pd.match(dataC.id_2,wlC.index),
                     pd.match(dataC.id_1,wlC.index)] = dataC.svScores.values
            svDistMtx = log(1-svMtx)
            tth = log(th)-svDistMtx.min()
            svDistMtx -= svDistMtx.min()
            fill_diagonal(svDistMtx,0)
            pDict = infomap_clustering(tth,svDistMtx)
            pArray = vstack([c_[pDict[k],[k]*len(pDict[k])] for k in pDict.keys()])
            partitionIM = pArray[argsort(pArray[:,0]),1]
        else:
            partitionIM = array([1])
        wlC['inferredCC'] = [vdb+':'+c+':'+str(x) for x in partitionIM]
        wlC['db'] = vdb
        newWordList = pd.concat([newWordList,wlC])
    newWordList.index = arange(len(newWordList))
    return newWordList



for db in test.db.unique():
    wl = testCluster(db)
    wl.to_csv('inferredCC/'+db+'.svmCC.csv',
              encoding='utf-8',index=False)


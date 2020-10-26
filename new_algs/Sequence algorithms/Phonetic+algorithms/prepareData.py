from numpy import *
import pandas as pd
from collections import defaultdict
import os
import re

training = ['CognateData/output/Afrasian.tsv',
            'CognateData/output/Huon.tsv',
            'CognateData/output/Kadai.tsv',
            'CognateData/output/Kamasau.tsv',
            'CognateData/output/Lolo-Burmese.tsv',
            'CognateData/output/Mayan.tsv',
            'CognateData/output/Miao-Yao.tsv',
            'CognateData/output/Mixe-Zoque.tsv',
            'CognateData/output/Mon-Khmer.tsv',          
            'mattis_new/output/Bai-110-09.tsv',
            'mattis_new/output/Chinese-140-15.tsv',
            'mattis_new/output/Chinese-180-18.tsv',
            'mattis_new/output/Japanese-200-10.tsv',
            'mattis_new/output/ObUgrian-110-21.tsv',
            'mattis_new/output/Tujia-109-5.tsv']


trainingData = pd.DataFrame()

path = os.getenv('HOME')+'/python/phylogeny/pavelMattis/vector_machines/'


# The following block reads in the feature vectors from 'output/samples/',
# the target values from 'output/targets/', and the original word lists
# from 'data/list_length_project/sets/
# for the training data, adds meta-information (gloss, languages compared,
# words compared) to the vectors and computes feature7.
# The reformatted data for all training sets are combined and saved in
# 'trainingData.csv'. 


for tsvFile in training:
    dataSource = path+'data/list_length_project/sets/'+tsvFile
    fname = dataSource.split('/')[-1]
    db = fname.split('.')[0]
    print db
    # read in wordlist
    wordlist = pd.read_table(dataSource,encoding='utf-8',na_filter=False,dtype=object)
    # keep track of synonyms within the same language
    synDict = defaultdict(lambda: 0)
    synocc = []
    for l,g in wordlist[['language','global_id']].values:
        synDict[l,g] += 1
        synocc.append(unicode(synDict[l,g]))
    wordlist['synonym_number'] = synocc
    dDict = {'sample_id':unicode,
             'feature1':double,
             'feature2':double,
             'feature3':double,
             'feature4':double,
             'feature5':double,
             'feature6':double,
             'feature8':double}
    # read in feature matrix for word pairs
    vectors = pd.read_table(path+'output/samples/'+fname,
                            encoding='utf-8',na_filter=False,dtype=dDict)
    # read in cognacy judgments
    labels = pd.read_table(path+'output/targets/'+fname,
                           encoding='utf-8',na_filter=False,dtype={'sample_id':unicode,
                                                                   'target':int})
    # colect metadata for wordpairs in vectors
    metaRaw = array([x.split('/') for x in vectors.sample_id.values])
    meta = pd.DataFrame(c_[metaRaw[:,0],
                           [x.split(',') for x in metaRaw[:,1]],
                           [x.split(',') for x in metaRaw[:,2]]],
                        columns=['global_id','l1','l2','id1','id2'])
    meta['sample_id'] = vectors.sample_id
    meta1 = pd.merge(wordlist[['global_id','language','gloss','synonym_number',
                               'transcription','cognate_class']],
                     meta,
                     left_on=['global_id','language','synonym_number'],
                     right_on=['global_id','l1','id1'])[['sample_id',
                                                         'global_id',
                                                         'l1','l2',
                                                         'transcription',
                                                         'cognate_class',
                                                         'id2']]
    meta2 = pd.merge(wordlist[['global_id','language','gloss','synonym_number',
                               'transcription','cognate_class']],
                     meta1,
                     left_on=['global_id','language','synonym_number'],
                     right_on=['global_id','l2','id2'])[['sample_id',
                                                         'gloss',
                                                         'l1','transcription_y',
                                                         'cognate_class_y',
                                                         'l2','transcription_x',
                                                         'cognate_class_x']]
    meta2.columns = ['sample_id',u'gloss', 'l1', u'w1', u'cc1', 'l2',
                     u'w2', u'cc2']
    meta2 = meta2.ix[pd.match(vectors.sample_id,meta2.sample_id)]
    concepts = meta2.gloss.unique()
    feature7 = pd.Series([abs(corrcoef(array(vectors[meta2.gloss==c][['feature2',
                                                                      'feature4']].values,
                                             double).T)[0,1])
                          for c in concepts],
                         index=concepts,dtype=double)
    feature7[feature7.isnull()] = 0
    vectors['feature7'] = feature7.ix[meta2.gloss.values].values
    combined = pd.merge(pd.merge(meta2,vectors,on='sample_id'),
                        labels,on='sample_id')
    combined = combined[combined.columns[1:]]
    combined['db'] = db
    trainingData = trainingData.append(combined)

# throw out all data with ambiguous cognate class assignment
trainingData = trainingData[array(['-' not in unicode(x) for x in trainingData.cc1.values])]
trainingData = trainingData[array(['-' not in unicode(x) for x in trainingData.cc2.values])]



trainingData.to_csv('trainingData.csv',encoding='utf-8',index=False)

# The following block does the same for the test data.


test = ['IELex/output/IELex-2016.tsv',
        'abvd2/output/abvd2-part1.tsv',
        'ManniPaper/output/Manni.tsv',]


testData = pd.DataFrame()

for tsvFile in test:
    dataSource = path+'data/list_length_project/sets/'+tsvFile
    fname = dataSource.split('/')[-1]
    db = fname.split('.')[0]
    print db
    wordlist = pd.read_table(dataSource,encoding='utf-8',na_filter=False,dtype=object)
    wordlist['cognate_class'] = [x.split(':')[-1] for x in wordlist.cognate_class.values]
    wordlist['language'] = [re.sub(r",([^ ])","&\\1",w) for w in wordlist.language.values]
    synDict = defaultdict(lambda: 0)
    synocc = []
    for l,g in wordlist[['language','global_id']].values:
        synDict[l,g] += 1
        synocc.append(unicode(synDict[l,g]))
    wordlist['synonym_number'] = synocc
    dDict = {'sample_id':unicode,
             'feature1':double,
             'feature2':double,
             'feature3':double,
             'feature4':double,
             'feature5':double,
             'feature6':double,
             'feature8':double}
    lnameDict = dict()
    for l in wordlist.language.unique():
        if '/' in l:
            lnameDict[l] = l.replace('/','|')
    rep = dict((re.escape(k),v) for k,v in lnameDict.iteritems())
    pattern = re.compile("|".join(rep.keys()))
    vectors = pd.read_table(path+'output/samples/'+fname,
                            encoding='utf-8',na_filter=False,dtype=dDict)
    vectors['sample_id'] = [re.sub(r",([^ ])","&\\1",w)
                            for w in vectors.sample_id.values]
    labels = pd.read_table(path+'output/targets/'+fname,
                           encoding='utf-8',na_filter=False,dtype={'sample_id':unicode,
                                                                   'target':int})
    labels['sample_id'] = [re.sub(r",([^ ])","&\\1",w)
                           for w in labels.sample_id.values]
    if len(lnameDict)>0:
        wordlist['language'] = [pattern.sub(lambda m:rep[re.escape(m.group(0))],w)
                                for w in wordlist.language.values]
        vectors['sample_id'] = [pattern.sub(lambda m:rep[re.escape(m.group(0))],w)
                                for w in vectors.sample_id.values]
        labels['sample_id'] = [pattern.sub(lambda m:rep[re.escape(m.group(0))],w)
                               for w in labels.sample_id.values]
    metaRaw = array([x.split('/') for x in vectors.sample_id.values])
    meta = pd.DataFrame(c_[metaRaw[:,0],
                           [x.split('&') for x in metaRaw[:,1]],
                           [x.split('&') for x in metaRaw[:,2]]],
                        columns=['global_id','l1','l2','id1','id2'])
    meta['sample_id'] = vectors.sample_id
    meta1 = pd.merge(wordlist[['global_id','language','gloss','synonym_number',
                               'transcription','cognate_class']],
                     meta,
                     left_on=['global_id','language','synonym_number'],
                     right_on=['global_id','l1','id1'])[['sample_id',
                                                         'global_id',
                                                         'l1','l2',
                                                         'transcription',
                                                         'cognate_class',
                                                         'id2']]
    meta2 = pd.merge(wordlist[['global_id','language','gloss','synonym_number',
                               'transcription','cognate_class']],
                     meta1,
                     left_on=['global_id','language','synonym_number'],
                     right_on=['global_id','l2','id2'])[['sample_id',
                                                         'gloss',
                                                         'l1','transcription_y',
                                                         'cognate_class_y',
                                                         'l2','transcription_x',
                                                         'cognate_class_x']]
    meta2.columns = ['sample_id',u'gloss', 'l1', u'w1', u'cc1', 'l2',
                     u'w2', u'cc2']
    meta2 = meta2.ix[pd.match(vectors.sample_id,meta2.sample_id)]
    concepts = meta2.gloss.unique()
    feature7 = pd.Series([abs(corrcoef(array(vectors[meta2.gloss==c][['feature2',
                                                                      'feature4']].values,
                                             double).T)[0,1])
                          for c in concepts],
                         index=concepts,dtype=double)
    feature7[feature7.isnull()] = 0
    vectors['feature7'] = feature7.ix[meta2.gloss.values].values
    combined = pd.merge(pd.merge(meta2,vectors,on='sample_id'),
                        labels,on='sample_id')
    combined = combined[combined.columns[1:]]
    combined['db'] = db
    combined['l1'] = [w.replace('|','/') for w in combined.l1.values]
    combined['l2'] = [w.replace('|','/') for w in combined.l2.values]
    testData = testData.append(combined)



testData = testData[array(['-' not in x for x in testData.cc1.values])]
testData = testData[array(['-' not in x for x in testData.cc2.values])]

testData = testData[array([',' not in x for x in testData.cc1.values])]
testData = testData[array([',' not in x for x in testData.cc2.values])]

testData = testData[array(['?' not in x for x in testData.cc1.values])]
testData = testData[array(['?' not in x for x in testData.cc2.values])]

testData = testData[array(['/' not in x for x in testData.cc1.values])]
testData = testData[array(['/' not in x for x in testData.cc2.values])]



testData.to_csv('testData.csv',encoding='utf-8',index=False)



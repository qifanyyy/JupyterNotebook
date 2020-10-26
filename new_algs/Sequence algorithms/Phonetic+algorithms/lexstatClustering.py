from numpy import *
import igraph
import random
igraph.set_random_number_generator(random) 
import codecs
import re
import pandas as pd
import lingpy as lp
from lingpy import rc
from lingpy.algorithm.extra import infomap_clustering
from sklearn.metrics import adjusted_rand_score
import os
#from multiprocessing import Manager,Process


def cleanASJP(word):
    word = re.sub(r",","-",word)
    word = re.sub(r"\%","",word)
    word = re.sub(r"\*","",word)
    word = re.sub(r"\"","",word)
    word = re.sub(r".~","",word)
    word = re.sub(r"(.)(.)(.)\$",r"\2",word)
    word = re.sub(r" ","-",word)
    return word


def asjp2tokens(w):
    wx = re.sub(r"[ -]","",w)
    return list(cleanASJP(wx))



def fscore(x,y):
    precision = mean(x[y==1])
    recall = mean(y[x==1])
    return 2*precision*recall/(precision+recall)


def bcubed(a,b):
    def iprecision(x,y,i):
        return mean((b==b[i])[a==a[i]])
    def irecall(x,y,i):
        return mean((a==a[i])[b==b[i]])
    p = mean([iprecision(a,b,i) for i in xrange(len(a))])
    r = mean([irecall(a,b,i) for i in xrange(len(a))])
    return 2*r*p/(r+p)


try:
    os.stat('reformattedData')
except:
    os.mkdir('reformattedData')       

try:
    os.stat('reformattedData/ipa')
except:
    os.mkdir('reformattedData/ipa')       

try:
    os.stat('reformattedData/asjp')
except:
    os.mkdir('reformattedData/asjp')       


try:
    os.stat('lexstatCC_IM')
except:
    os.mkdir('lexstatCC_IM')       





path = os.getenv('HOME')+'/python/phylogeny/pavelMattis/vector_machines/'


for f in [x for x in os.listdir(path+'data/list_length_project/sets/CognateData/output') if x!='.svn']:
    db = f.split('.')[0]
    data = pd.read_table(path+'data/list_length_project/sets/CognateData/output/'+f,encoding='utf-8')
    data = data[['-' not in unicode(x) for x in data.cognate_class.values]]
    output = pd.DataFrame()
    output['ID'] = arange(len(data))+1
    output['Taxon'] = data.language.astype('string')
    output['Gloss'] = data.gloss.values
    output['GlossID'] = pd.match(data.gloss.values,data.gloss.unique())+1
    output['IPA'] = [re.sub(r"[ -]","",unicode(x)) for x in data.transcription]
    output['Tokens'] = [' '.join(asjp2tokens(unicode(w))) for w in output.IPA]
    cClasses = array([x+':'+unicode(y).strip('?')
                      for (x,y) in data[['gloss','cognate_class']].values])
    output['CogID'] = pd.match(cClasses,unique(cClasses))
    output[['Taxon','Gloss']] = output[['Taxon','Gloss']].astype('string')
    output['dbID'] = [db+'_'+str(x-1) for x in output.ID.values]
    output.to_csv('reformattedData/asjp/'+db+'.tsv',encoding='utf-8',
                  sep='\t',index=False)

for f in [x for x in os.listdir(path+'data/list_length_project/sets/mattis_new/output') if x!='.svn']:
    db = f.split('.')[0]
    data = pd.read_table(path+'/data/list_length_project/sets/mattis_new/output/'+f,encoding='utf-8')
    data = data[['-' not in unicode(x) for x in data.cognate_class.values]]
    output = pd.DataFrame()
    output['ID'] = arange(len(data))+1
    output['Taxon'] = data.language.values
    output['Gloss'] = data.gloss.values
    output['GlossID'] = pd.match(data.gloss.values,data.gloss.unique())+1
    output['IPA'] = [re.sub(r"[ -]","",unicode(x)) for x in data.transcription]
    output['Tokens'] = [' '.join(lp.ipa2tokens(unicode(w))) for w in output.IPA]
    cClasses = array([x+':'+unicode(y).strip('?')
                      for (x,y) in data[['gloss','cognate_class']].values])
    output['CogID'] = pd.match(cClasses,unique(cClasses))
    output[['Taxon','Gloss']] = output[['Taxon','Gloss']]
    output['dbID'] = [db+'_'+str(x-1) for x in output.ID.values]
    output.to_csv('reformattedData/ipa/'+db+'.tsv',encoding='utf-8',
                  sep='\t',index=False)


for f in [x for x in os.listdir(path+'data/list_length_project/sets/abvd2/output') if x!='.svn']:
    db = f.split('.')[0]
    data = pd.read_table(path+'/data/list_length_project/sets/abvd2/output/'+f,encoding='utf-8')
    data = data[['-' not in unicode(x) for x in data.cognate_class.values]]
    data = data[[',' not in unicode(x) for x in data.cognate_class.values]]
    data = data[['?' not in unicode(x) for x in data.cognate_class.values]]
    output = pd.DataFrame()
    output['ID'] = arange(len(data))+1
    output['Taxon'] = data.language.astype('unicode')
    output['Gloss'] = data.gloss.values
    output['GlossID'] = pd.match(data.gloss.values,data.gloss.unique())+1
    output['IPA'] = [re.sub(r"[ -]","",unicode(x)) for x in data.transcription]
    output['Tokens'] = [' '.join(lp.ipa2tokens(unicode(w))) for w in output.IPA]
    cClasses = array([x+':'+unicode(y).strip('?')
                      for (x,y) in data[['gloss','cognate_class']].values])
    output['CogID'] = pd.match(cClasses,unique(cClasses))
    output[['Taxon','Gloss']] = output[['Taxon','Gloss']].astype('unicode')
    output['dbID'] = [db+'_'+str(x-1) for x in output.ID.values]
    output.to_csv('reformattedData/ipa/'+db+'.tsv',encoding='utf-8',
                  sep='\t',index=False)


f = 'IELex-2016.tsv'
db = f.split('.')[0]
data = pd.read_table(path+'/data/list_length_project/sets/IELex/output/'+f,encoding='utf-8')
data = data[['-' not in unicode(x) for x in data.cognate_class.values]]
data = data[[',' not in unicode(x) for x in data.cognate_class.values]]
data = data[['?' not in unicode(x) for x in data.cognate_class.values]]
output = pd.DataFrame()
output['ID'] = arange(len(data))+1
output['Taxon'] = data.language.astype('unicode')
output['Gloss'] = data.gloss.values
output['GlossID'] = pd.match(data.gloss.values,data.gloss.unique())+1
output['IPA'] = [re.sub(r"[ -]","",unicode(x)) for x in data.transcription]
output['Tokens'] = [' '.join(lp.ipa2tokens(unicode(w))) for w in output.IPA]
cClasses = array([x+':'+unicode(y).strip('?')
                  for (x,y) in data[['gloss','cognate_class']].values])
output['CogID'] = pd.match(cClasses,unique(cClasses))
output[['Taxon','Gloss']] = output[['Taxon','Gloss']].astype('unicode')
output['dbID'] = [db+'_'+str(x-1) for x in output.ID.values]
output.to_csv('reformattedData/ipa/'+db+'.tsv',encoding='utf-8',
              sep='\t',index=False)


for f in [x for x in os.listdir(path+'data/list_length_project/sets/ManniPaper/output') if x!='.svn']:
    db = f.split('.')[0]
    data = pd.read_table(path+'data/list_length_project/sets/ManniPaper/output/'+f,encoding='utf-8')
    data = data[['-' not in unicode(x) for x in data.cognate_class.values]]
    data = data[[',' not in unicode(x) for x in data.cognate_class.values]]
    data = data[['?' not in unicode(x) for x in data.cognate_class.values]]
    output = pd.DataFrame()
    output['ID'] = arange(len(data))+1
    output['Taxon'] = data.language
    output['Gloss'] = data.gloss.values
    output['GlossID'] = pd.match(data.gloss.values,data.gloss.unique())+1
    output['IPA'] = [re.sub(r"[ -]","",unicode(x)) for x in data.transcription]
    output['Tokens'] = [' '.join(lp.ipa2tokens(unicode(w))) for w in output.IPA]
    cClasses = array([x+':'+unicode(y).strip('?')
                      for (x,y) in data[['gloss','cognate_class']].values])
    output['CogID'] = pd.match(cClasses,unique(cClasses))
    output[['Taxon','Gloss']] = output[['Taxon','Gloss']]
    output['dbID'] = [db+'_'+str(x-1) for x in output.ID.values]
    output.to_csv('reformattedData/ipa/'+db+'.tsv',encoding='utf-8',
                  sep='\t',index=False)



trainingASJP = ['Afrasian.tsv',
                'Huon.tsv',
                'Kadai.tsv',
                'Kamasau.tsv',
                'Lolo-Burmese.tsv',
                'Mayan.tsv',
                'Miao-Yao.tsv',
                'Mixe-Zoque.tsv',
                'Mon-Khmer.tsv']

trainingIPA = ['Bai-110-09.tsv',
               'Chinese-140-15.tsv',
               'Chinese-180-18.tsv',
               'Japanese-200-10.tsv',
               'ObUgrian-110-21.tsv',
               'Tujia-109-5.tsv']


test = ['IELex-2016.tsv',
        'abvd2-part1.tsv',
        'Manni.tsv']


def lexStatIM_training(th=0.57):
    random.seed(12345)
    scores = []
    lp.rc(schema='asjp')
    for fn in trainingASJP:
        db = fn.split('.')[0]
        print db
        lex = lp.LexStat('reformattedData/asjp/'+fn,
                         check=False)
        lex.get_scorer(preprocessing=False,run=10000)
        lex.cluster(method='lexstat',threshold=th,
                    external_function=lambda x, y: infomap_clustering(y, x, revert=True),
                    ref="lexstat_infomap")
        taxa = array(lex.cols)
        partition = vstack([array([concatenate(lex.get_dict(col=l,entry=entry).values())
                                   for entry in ['concept','doculect','ipa',
                                                 'cogid',
                                                 'lexstat_infomap']]).T for l in taxa])
        partition = pd.DataFrame(partition,columns=['concept','doculect','counterpart',
                                                    'cogid','lpID'])
        partition.to_csv('lexstatCC_IM/'+db+'_lsCC.csv',encoding='utf-8',index=False)
        concepts = partition.concept.unique()
        scoreList = []
        for c in concepts:
            cPartition = partition[partition.concept==c]
            ari = adjusted_rand_score(cPartition.cogid,cPartition.lpID)
            scoreList.append(ari)
        dbAri = mean(scoreList)
        bc = bcubed(array([':'.join(x)
                           for x in partition[['concept','cogid']].values]),
                    array([':'.join(x)
                           for x in partition[['concept','lpID']].values]))
        scores.append((db,dbAri,bc))
    lp.rc(schema='ipa')
    for fn in trainingIPA:
        db = fn.split('.')[0]
        print db
        lex = lp.LexStat('reformattedData/ipa/'+fn,
                         check=False)
        lex.get_scorer(preprocessing=False,run=1000)
        lex.cluster(method='lexstat',threshold=th,
                    external_function=lambda x, y: infomap_clustering(y, x, revert=True),
                    ref="lexstat_infomap")
        taxa = array(lex.cols)
        partition = vstack([array([concatenate(lex.get_dict(col=l,entry=entry).values())
                                   for entry in ['concept','doculect','ipa',
                                                 'cogid',
                                                 'lexstat_infomap']]).T for l in taxa])
        partition = pd.DataFrame(partition,columns=['concept','doculect','counterpart',
                                                    'cogid','lpID'])
        partition.to_csv('lexstatCC_IM/'+db+'_lsCC.csv',encoding='utf-8',index=False)
        concepts = partition.concept.unique()
        scoreList = []
        for c in concepts:
            cPartition = partition[partition.concept==c]
            ari = adjusted_rand_score(cPartition.cogid,cPartition.lpID)
            scoreList.append(ari)
        dbAri = mean(scoreList)
        bc = bcubed(array([':'.join(x)
                           for x in partition[['concept','cogid']].values]),
                    array([':'.join(x)
                           for x in partition[['concept','lpID']].values]))
        scores.append((db,dbAri,bc))
    return scores


def lexStatIM_test(th=.57):
    random.seed(12345)
    scores = []
    lp.rc(schema='ipa')
    for fn in test:
        db = fn.split('.')[0]
        print db
        lex = lp.LexStat('reformattedData/ipa/'+fn,
                         check=False)
        lex.get_scorer(preprocessing=False,run=10000)
        lex.cluster(method='lexstat',threshold=th,
                    external_function=lambda x, y: infomap_clustering(y, x, revert=True),
                    ref="lexstat_infomap")
        taxa = array(lex.cols)
        partition = vstack([array([concatenate(lex.get_dict(col=l,entry=entry).values())
                                   for entry in ['concept','doculect','ipa',
                                                 'cogid',
                                                 'lexstat_infomap']]).T for l in taxa])
        partition = pd.DataFrame(partition,columns=['concept','doculect','counterpart',
                                                    'cogid','lpID'])
        partition.to_csv('lexstatCC_IM/'+db+'_lsCC.csv',encoding='utf-8',index=False)
        concepts = partition.concept.unique()
        scoreList = []
        for c in concepts:
            cPartition = partition[partition.concept==c]
            ari = adjusted_rand_score(cPartition.cogid,cPartition.lpID)
            scoreList.append(ari)
        dbAri = mean(scoreList)
        bc = bcubed(array([':'.join(x)
                           for x in partition[['concept','cogid']].values]),
                    array([':'.join(x)
                           for x in partition[['concept','lpID']].values]))
        scores.append((db,dbAri,bc))
        print scores[-1]
    return scores


trainingResults = lexStatIM_training()

print pd.DataFrame(trainingResults,columns=['db','ARI','bcubed-fscore'])

testResults = lexStatIM_test()


print pd.DataFrame(testResults,columns=['db','ARI','bcubed-fscore'])

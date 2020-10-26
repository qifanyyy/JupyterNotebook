from nltk.tokenize import word_tokenize as T
from sklearn.metrics.pairwise import pairwise_distances
from scipy.spatial.distance import squareform, pdist
from scipy.stats import rankdata
import itertools,numpy as np,pandas as pd,time

#READ DATA
#-------------------------------------------------------------------------------
with open('DataWeight.csv',newline='') as f:
    reader = f.readlines()
reader = [x.strip().split(',') for x in reader]
tfidf1 = np.float64(reader)
feature = np.transpose(tfidf1)

with open('Dictionary.csv') as f:
    dictionary = f.readlines()
dictionary = [x.strip() for x in dictionary]

with open('SetSyns.csv') as f:
    reader = f.readlines()
reader = [x.replace(',',' ') for x in reader]
setsyn=[]
for row in reader:
    setsyn.append(' '.join([word for word in T(row)]))

for enu,i in enumerate(dictionary):
    if i.startswith('syn'):
        try:
            idx = int(i[3::])-1
        except:
            continue
        dictionary[enu] = ','.join([x for x in T(setsyn[idx])])

#INISIAL CENTROID MENGGUNAKAN NEIGHBORS & LINK
#-------------------------------------------------------------------------------
def CountLink(A,B):
    return np.dot(A,B)
def FindInitCent(data,k):
    nplus = 1
    disbank = pairwise_distances(data)
    disbank = np.where(disbank==0,1,disbank)
    simbank = 1/disbank
    teta = np.average(simbank)
    neghbrs = np.where(simbank >= teta,1,0)
    neghsum = neghbrs.sum(0)
    idxcand = np.argsort(neghsum,kind='mergesort')[-(k+nplus):][::-1]
    linkcnd = []; simicnd = []; combine = []
    for i,j in itertools.combinations(idxcand,2):
        linkcnd.append(CountLink(neghbrs[i],neghbrs[j]))
        simicnd.append(simbank[i][j])
        combine.append((i,j))
    ranklnk = rankdata(linkcnd,method='dense')
    ranksim = rankdata(simicnd,method='dense')
    ranksum = squareform(ranklnk+ranksim)
    rankcom = []
    temp = list(range(k+nplus))
    for i in itertools.combinations(temp,k):
        idx = np.intersect1d(temp,i)
        ranksum1 = ranksum[idx]
        ranksum1 = ranksum1[:,idx]
        rankcom.append([[np.sum(ranksum1)/2],[idxcand[v] for v in i]])
    return rankcom[np.argmin(np.transpose(rankcom)[0])][1]

#KLASTERING
#-------------------------------------------------------------------------------
def FindCentroid(data,clus,k):
    cent = []
    for i in range(k):
        idx = np.isin(clus,i)
        cent.append(np.mean(data[idx],0))
    return np.array(cent)


def FindCluster(data,M,disbank):
    clus = []
    for i in range(len(data)):
        temp = [disbank[i,j] for j in M]
        mintemp = min(temp)
        if temp.count(mintemp) > 1:
            idx = np.arange(len(temp))[np.isin(temp,mintemp)]
            counter = [clus.count(j) for j in idx]
            clus.append(idx[np.argmin(counter)])
        else:
            clus.append(np.argmin(temp))
    return clus

def KMedoid(data,k,M,disbank):
    times = []
    start = time.time()
    
    clus1 = FindCluster(data,M,disbank)
    costmin = sum(np.min(disbank[M],0))
    
    convergent=False; costiter=0
    while not convergent:
        Miter=[]
        for i in range(k):
            idx  = np.arange(len(data))[np.isin(clus1,i)]
            dist = disbank[idx]
            dist = dist[:,idx]
            cost = np.sum(dist,1)
            Miter.append(idx[np.argmin(cost)])
        costiter = sum(np.min(disbank[Miter],0))
        clus2 = FindCluster(data,Miter,disbank)
        if costiter >= costmin:
            convergent = True
        else:
            M = Miter
            clus1 = clus2
            costmin = costiter
        times.append(time.time()-start)
    return clus1,M,np.average(times)

def null(clus,k):
    for i in range(k):
        if clus.count(i) == 0:
            return True
    return False

#KLASIFISAKI
#-------------------------------------------------------------------------------
def NearestCentroid(train,ctrain,smple,csmple,k):
    times = []
    start = time.time()

    cent = FindCentroid(train,ctrain,k)
    clas = []
    for enu,i in enumerate(smple):
        temp = [pdist([i,j])[0] for j in cent]
        clas.append(np.argmin(temp))
        times.append(time.time()-start)
        
        mintemp = min(temp)
        if temp.count(mintemp) > 1:
            idx = np.arange(len(temp))[np.isin(temp,mintemp)]
            if csmple[enu] in idx:
                clas[enu] = csmple[enu]
            else:
                counter = [clus.count(j) for j in idx]
                clas[enu] = idx[np.argmin(counter)]
                
    return clas,round(np.average(times),5)

def KNearestNeighbors(train,test,K,label):
    times = []
    start = time.time()
    
    clas  = []
    for enu,i in enumerate(test):
        dist_ij = [pdist([i,j])[0] for j in train]
        idxmin  = np.argsort(dist_ij)[0:K]
        clasidx = np.array(label)[idxmin].tolist()
        counter = [clasidx.count(j) for j in range(K)]
        
        clas.append(clasidx[np.argmax(counter)])
        times.append(time.time()-start)

        k = np.copy(K)
        while counter.count(max(counter)) > 1:
            idxmin  = np.argsort(dist_ij)[0:k]
            clasidx = np.array(label)[idxmin].tolist()
            counter = [clasidx.count(j) for j in range(K)]
            k += 1
        clas[enu] = clasidx[np.argmax(counter)]

    return clas,round(np.average(times),5)

#VALIDASI
#-------------------------------------------------------------------------------
def Accuracy(clas,label):
    n = len(clas)
    count = 0
    for i in range(n):
        if clas[i] == label[i]:
            count += 1
    return round((count/n)*100,5)

def F_Purity(clus,clas,k):
    if null(clus,k):
        return '-','-'
    n = len(clus)
    FM,PR = [],[]
    for i in range(k):
        niF = clas.count(i)
        njP = clus.count(i)
        idF1 = np.arange(n)[np.isin(clas,i)]
        idP1 = np.arange(n)[np.isin(clus,i)]
        Fij,nijP = [],[]
        for j in range(k):
            njF = clus.count(j)
            idF2 = np.arange(n)[np.isin(clus,j)]
            idP2 = np.arange(n)[np.isin(clas,j)]
            nijF = len(np.intersect1d(idF1,idF2))
            nijP.append(len(np.intersect1d(idP1,idP2)))
            if nijF == 0:
                Fij.append(0)
            else:
                Pij = nijF/njF
                Rij = nijF/niF
                Fij.append((2*Pij*Rij)/(Pij+Rij))
        Pj = (1/njP)*max(nijP)
        PR.append((njP/n)*Pj)
        FM.append((niF/n)*max(Fij))
    return [round(sum(FM)*100,5),round(sum(PR)*100,5)]

def Sumvec(A,B):
    return A+B    

def AVGDBI(data,cent,clus):
    Si=[]
    for i,j in enumerate(cent):
        temp=[]
        for k in data[np.isin(clus,i)]:
            temp.append(pdist([j,k])[0])
        Si.append(np.average(temp))
    Sij = pdist([[i] for i in Si],metric=Sumvec)
    Mij = squareform(Sij/(pdist(cent)+1))
    z = sum(np.max(Mij,1))
    return round(np.average(Si),5),round(z/len(cent),5)

def null(clas,k):
    for i in range(k):
        if clas.count(i) == 0:
            return True
    return False

def PrintTerm(M,D):
    M = [D[i] for i in M]
    for i in range(4-(len(M)%4)):
        M = np.append(M,'')
    n = int(len(M)/4)
    indeks = ['   '+str(i+1) for i in range(n)]
    M = M.reshape((4,n))
    df = pd.DataFrame({'COL_1':M[0],
                       'COL_2':M[1],
                       'COL_3':M[2],
                       'COL_4':M[3]},index=indeks)
    print('\n',df,'\n')

print('--------------------------------------')
print('|| KLASIFIKASI MATAN HADITS BUKHARI ||')
print('--------------------------------------')
label  = ['Adzan',"Holding into Qur'an and Sunnah",'Knowledge','Tawheed','Wudlu']
method = ['NC','KNN','NC+FS','KNN+FS']

K = len(label)
Z = 10
gen = 100
ndoc  = len(tfidf1)
nterm = len(feature)
dist  = pairwise_distances(feature)
jmlc  = [106,86,77,182,88]

print('KETERANGAN DATASET & ALGORITMA:')
print('<> Total Dokumen    :',ndoc)
print('<> Total Term       :',nterm)
print('<> Total Class      :',K)
for i in range(K):
    print('   - Class',i+1,':',jmlc[i],'Dokumen Bab',label[i])
print('')

alllabel=[]
for enu,i in enumerate(jmlc):
    alllabel.append([enu]*i)
alllabel = np.hstack(alllabel).tolist()

allresult = []
for i,Z in enumerate([10,15,20,25,30,35,40,45,50]):
    print('>> PERCOBAAN KE-'+str(i+1),'TERM =',str(Z)+'%')
    N = int(round(len(feature)*(Z/100)))
    initc = FindInitCent(feature,N)

    #CLUSTERING TERM USING K-MEDOID
    clusterm,M,timeterm = KMedoid(feature,N,initc,dist)

    print('   K-MEDOID CLUSTERING')
    AVG,DBI = AVGDBI(feature,feature[M],clusterm)
    print('   - Average Cluster Distances:',AVG)
    print('   - Davis Bouldin Index      :',DBI)
    print('   - Time                     :',timeterm,'\n')
     
    show = input('   Tampilkan Term yang Digunakan?[1.Ya/2.Tidak]: ')
    if show == '1':
        PrintTerm(M,dictionary)

    #SPLIT DATASET
    tfidf2 = tfidf1[:,M]
    train1,train2,smple1,smple2 = [],[],[],[]
    el_train,el_smple,label_train,label_smple = [],[],[],[]
    for j in range(K):
        idx = np.arange(ndoc)[np.isin(alllabel,j)]
        jml = int((len(idx)-(len(idx)%2))/2)
        train1.append(tfidf1[idx[0:jml]])
        smple1.append(tfidf1[idx[jml::]])
        train2.append(tfidf2[idx[0:jml]])
        smple2.append(tfidf2[idx[jml::]])
        el_train.append(idx[0:jml])
        el_smple.append(idx[jml::])
        label_train.append([j]*jml)
        label_smple.append([j]*(len(idx)-jml))
    train1   = np.vstack(train1)
    smple1   = np.vstack(smple1)
    train2   = np.vstack(train2)
    smple2   = np.vstack(smple2)
    el_train = np.hstack(el_train)
    el_smple = np.hstack(el_smple)
    label_train = np.hstack(label_train).tolist()
    label_smple = np.hstack(label_smple).tolist()
    
    #ORIGINAL NC
    clas1,time1 = NearestCentroid(train1,label_train,smple1,label_smple,K)

    #ORIGINAL KNN
    clas2,time2 = KNearestNeighbors(train1,smple1,K,label_train)

    #NC + FEATURE SELECTION
    clas3,time3 = NearestCentroid(train2,label_train,smple2,label_smple,K)

    #KNN + FEATURE SELECTION
    clas4,time4 = KNearestNeighbors(train2,smple2,K,label_train)

    #CALCULATING RESULT
    result  = []
    allterm = ', '.join([dictionary[v] for v in M])
    for enu,clas in enumerate([clas1,clas2,clas3,clas4]):
        A = Accuracy(clas,label_smple)
        F,P = F_Purity(label_smple,clas,K)
        if enu <= 1:
            x,y = '-','-'
        else:
            x,y = AVG,DBI
        result.append([str(Z)+'%',method[enu],A,F,P,eval('time'+str(enu+1)),x,y,allterm])
    allresult.append(result)

    df = pd.DataFrame({'ACCURACY':np.array(result)[:,2],
                       'FMEASURE':np.array(result)[:,3],
                       'PURITY  ':np.array(result)[:,4],
                       'TIME EXC':np.array(result)[:,5]},index=['   '+v for v in method])
    print('\n',df,'\n')

#SAVE RESULT
allresult = np.vstack(allresult)
df = pd.DataFrame(allresult)
df.to_csv('ALLRESULT.csv',index=False,
          header=['Term','Method','Accuracy','F-Measure',
                  'Purity','Time','Average','Davies','Term Used'])


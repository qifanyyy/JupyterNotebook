import numpy as np
import matplotlib.pyplot as plt
import math
from sklearn.metrics.cluster import adjusted_rand_score as ARI
from sklearn.cluster import KMeans
import itertools

file = ['10d-4c-no0.dat','10d-4c-no1.dat','10d-10c-no0.dat','10d-10c-no1.dat',
        '10d-20c-no0.dat','10d-20c-no1.dat','10d-40c-no4.dat','10d-40c-no5.dat',
        'brain_cancer.txt','breast-cancer-wisconsin.txt','colon_cancer.txt',
        'lung_cancer.txt','lymphoma_cancer.txt','prostate_cancer.txt','srbct_cancer.txt']

def calculate_delta(a,b):
    return (a+b)/2

def get_w(a,delta):
    g = np.array(a) - delta 
    for i in range(len(g)):
        if g[i]<0:
            g[i]=0
            
    denominator = 0
    for i in g:
        denominator = denominator + i**2
    w = g/(denominator**0.5)
    return w

def get_s(w):
    s = 0
    for i in range(len(w)):
        s = s + abs(w[i])
    return s

def ranges(N, nb):
    step = N / nb
    s = [1]
    for i in range(nb):
        s.append(s[i]+step)
    return s


matrix = np.zeros((len(file),2))
s_selected = []
for f in range(len(file)):
    dataset = str(file[f])
    print('DATASET:',dataset)
    load = np.loadtxt(file[f])
    k = len(np.unique(load[:,load.shape[1]-1]))
    print('k:',k)
    data = load[:,:load.shape[1]-1]
    w = np.array([1/math.sqrt(data.shape[1])] * data.shape[1])

    a = np.zeros((16,data.shape[1]))
    w_per = np.zeros((16,data.shape[1]))
    p_a = np.zeros((16,data.shape[1]))
    
    data_mean = np.mean(data,axis = 0)
    # print(data_mean)
    # print(distance)
    
    s_set = ranges(math.sqrt(data.shape[1])-1,30)
    
    per_data = [data]
    per_data.append(data)
    for i in range(15):
        per_data.append(np.random.permutation(data))
    
    gaps = []
    for m in range(30):
        
        s = s_set[m]
        print('s:',s)
        distance_per =  np.zeros((16,data.shape[0],k))
        cluster_assigned_per = np.zeros((16,data.shape[0]))
        data_mean = np.mean(data,axis = 0)
        for n in range(16):
            print('n:',n)
            cs_new = data[np.random.permutation(data.shape[0])[0:k]]
            for iter1 in range(100):
                
                for i in range(k):
                    distance_per[n][:,i] = np.linalg.norm(w*per_data[n] - w*cs_new[i],axis=1)**2  
                    #print(distance[:,i])

                cluster_assigned_per[n] = np.argmin(np.array(distance_per[n]),axis = 1)
                cs_old = np.array(cs_new)                                        #Calculate Membership

                for i in range(k):
                    cs_new[i] = np.mean(per_data[n][cluster_assigned_per[n]==i],axis=0)
                
                er = np.linalg.norm(cs_new - cs_old)                             #Calculate new cluster centres


                for i in range(data.shape[1]):
                    variance_dist = 0
                    for j in range(data.shape[0]):
                        variance_dist = variance_dist + np.linalg.norm(per_data[n][j][i] - data_mean[i])**2
                    #print('variance_dist',variance_dist)

                    within_cluster_dist = 0
                    for j in range(k):
                        ind = np.where(cluster_assigned_per[n] == j)[0]
                        new_data = np.zeros((31,len(ind),data.shape[1]))
                        for p in range(len(ind)):
                            new_data[n][p] = per_data[n][ind[p]]
                        within_cluster_dist = within_cluster_dist + np.linalg.norm(new_data[n][:,i] - cs_new[j][i])**2
                    #print('within_cluster_dist',within_cluster_dist)

                    a[n][i] = 2*(variance_dist - within_cluster_dist)

                #print('a:',a[n])

                for t in range(data.shape[1]):
                    p_a[n][t] = a[n][t]
                p_a.sort()

                if iter1 == 0:
                    l = 0
                    r = p_a[n][-2]
                    delta = calculate_delta(l,r)
                    w = get_w(a[n],delta)
                    s1 = get_s(w)

                while r-l > 1e-9:
                    if s1>s:
                        l = delta
                    else:
                        r = delta

                    delta = calculate_delta(l,r)
                    w = get_w(a[n],delta)
                    s1 = get_s(w)

                if er < 1e-9:
                    print('#iter', iter1)
                    break
                    
            w_per[n] = w
            print('w:',w_per[n])
            
            print('ARI_sparse:',ARI(cluster_assigned_per[n], load[:,load.shape[1]-1]))
            #matrix[f,0] = ARI(cluster_assigned, load[:,load.shape[1]-1])

            kmeans = KMeans(n_clusters=k, init = 'random', max_iter=100, n_init=1).fit(data)

            print('ARI_Kmeans:',ARI(kmeans.labels_, load[:,load.shape[1]-1]))
            #matrix[f,1] = ARI(kmeans.labels_, load[:,load.shape[1]-1])
            print()
            
        os = np.sum(a*w_per,axis=1)       
        obs_mean = np.log10(os)[1:16].mean()
        gap_s = np.log10(os)[0] - obs_mean
        print('gap_s',gap_s)
        gaps.append(gap_s)
        print()
        
    
    s_selected.append(s_set[np.array(gaps).argmax()])



print('s_selected:',s_selected)



matrix = np.zeros((len(file),2))
for f in range(len(file)):
    dataset = str(file[f])
    print('DATASET:',dataset)
    load = np.loadtxt(file[f])
    k = len(np.unique(load[:,load.shape[1]-1]))
    print('k:',k)
    data = load[:,:load.shape[1]-1]

    s = s_selected[f]                                                              #Degree of sparcity(user defined - we'll tune the s we get in the algo to be closer to this)
    w = np.array([1/math.sqrt(data.shape[1])] * data.shape[1])
    #print('Weights:',w)
    cs_old = np.zeros((k,data.shape[1]))
    cs_new = data[np.random.permutation(data.shape[0])[0:k]]

    #print()
    #print('cs_new:',cs_new)
    a = np.zeros(data.shape[1])
    p = np.zeros(data.shape[1])
    er = np.linalg.norm(cs_new - cs_old)

    distance = np.zeros((data.shape[0],k))
    cluster_assigned = np.zeros(data.shape[0])
    data_mean = np.mean(data,axis = 0)
    # print(data_mean)
    # print(distance)
    for iter1 in range(100):
        for i in range(k):
            distance[:,i] = np.linalg.norm(w*data - w*cs_new[i],axis=1)**2  
            #print(distance[:,i])

        cluster_assigned = np.argmin(np.array(distance),axis = 1)
        cs_old = np.array(cs_new)                                       #Calculate Membership

        for i in range(k):
            cs_new[i] = np.mean(data[cluster_assigned==i],axis=0)
        er = np.linalg.norm(cs_new - cs_old)                             #Calculate new cluster centres


        for i in range(data.shape[1]):
            variance_dist = 0
            for j in range(data.shape[0]):
                variance_dist = variance_dist + np.linalg.norm(data[j][i] - data_mean[i])**2
            #print('variance_dist',variance_dist)

            within_cluster_dist = 0
            for j in range(k):
                ind = np.where(cluster_assigned == j)[0]
                new_data = np.zeros((len(ind),data.shape[1]))
                for m in range(len(ind)):
                    new_data[m] = data[ind[m]]
                within_cluster_dist = within_cluster_dist + np.linalg.norm(new_data[:,i] - cs_new[j][i])**2
            #print('within_cluster_dist',within_cluster_dist)

            a[i] = 2*(variance_dist - within_cluster_dist)

        #print('a:',a)

        for t in range(data.shape[1]):
            p[t] = a[t]
        p.sort()

        if iter1 == 0:
            l = 0
            r = p[-2]
            delta = calculate_delta(l,r)
            w = get_w(a,delta)
            s1 = get_s(w)

        while r-l > 1e-9:
            if s1>s:
                l = delta
            else:
                r = delta

            delta = calculate_delta(l,r)
            #print(delta)
            w = get_w(a,delta)
            #print('w',w)
            s1 = get_s(w)
            #print('l1 w', s1)

#         print('s1:',s1)
#         print('l1:',w)
#         print('er:',er)
#         print('s:',s)
        if er < 1e-9:
            print('#iter', iter1)
            break

    print('ARI_sparse:',ARI(cluster_assigned, load[:,load.shape[1]-1]))
    matrix[f,0] = ARI(cluster_assigned, load[:,load.shape[1]-1])

    kmeans = KMeans(n_clusters=k, init = 'random', max_iter=100, n_init=1).fit(data)

    print('ARI_Kmeans:',ARI(kmeans.labels_, load[:,load.shape[1]-1]))
    matrix[f,1] = ARI(kmeans.labels_, load[:,load.shape[1]-1])
    print()





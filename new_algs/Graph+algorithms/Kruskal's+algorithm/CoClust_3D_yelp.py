import pandas as pd
import numpy as np
from algorithms.coclust_3D_tau import CoClust
from utils import CreateOutputFile, CreateLogger
import os
import sys
from sklearn.metrics import adjusted_rand_score as ari
from sklearn.metrics import normalized_mutual_info_score as nmi
from sklearn.feature_extraction.text import CountVectorizer

if len(sys.argv)> 1 and sys.argv[1] == '-h':
    print('''
    Co-Clustering of tensors extracted from yelp database. Parameters:
        tensor: string.
            Accepted values: TOR or PGH.
        algorithm: string. Optional.
            Accepted values: ALT, AVG, AGG, ALT2, AGG2. Default: ALT2
        level: string. Optional.
            Accepted values: DEBUG, INFO, WARNING, ERROR, CRITICAL
            Default value: WARNING
    ''')
    quit()

tensor = sys.argv[1]
alg = sys.argv[2] if (len(sys.argv)> 2) and (sys.argv[2] in ['ALT','AVG','AGG','ALT2','AGG2']) else 'ALT2'
level = sys.argv[-1] if (len(sys.argv)> 2) and (sys.argv[-1] in ['DEBUG','INFO','WARNING','ERROR','CRITICAL']) else 'WARNING'
logger = CreateLogger(level)

yelp = pd.read_pickle('./resources/yelp/yelp_final_' + tensor + '.pkl')
f = open('./resources/yelp/yelp_vocabulary_' + tensor + '.txt','r+', encoding = 'latin1')
v = dict()
for l in f.readlines():
    a,b = l.replace('\n','').split(',')
    v[a] = int(b)


f.close()

b = len(yelp.business_id.unique())
u = len(yelp.user_id.unique())


vect = CountVectorizer(vocabulary = v)
X_TOR = vect.fit_transform(yelp.text)

print(b,u,X_TOR.shape[1])

T = np.zeros((b,u,X_TOR.shape[1]))
y = np.zeros(b)

for h,r in enumerate(yelp.iterrows()):
    i = r[1].b_label
    j = r[1].u_label
    for k in range(X_TOR.shape[1]):
        T[i,j,k] += X_TOR[h,k]
    if r[1].italian == 1:
        y[i] = 0
    elif r[1].chinese == 1:
        y[i] = 1
    elif r[1].mexican == 1:
        y[i] = 2

sparsity = 1 - (np.sum(T>0) / np.product(T.shape))
f, dt = CreateOutputFile("yelp", date = True)


output_path = f"./output/_yelp/" + dt[:10] + "_" + dt[11:13] + "." + dt[14:16] + "." + dt[17:19] + "/"
directory = os.path.dirname(output_path)
if not os.path.exists(directory):
    os.makedirs(directory)

model = CoClust(np.sum(T.shape) * 10, optimization_strategy = alg, path = output_path)
model.fit(T)

tau = model.final_tau_
nmi_x = nmi(y, model.x_, average_method='arithmetic')
ari_x = ari(y, model.x_)

f.write(f"{T.shape[0]},{T.shape[1]},{T.shape[2]},{len(set(y))},,,,{tau[0]},{tau[1]},{tau[2]},{nmi_x},,,{ari_x},,,{model._n_clusters[0]},{model._n_clusters[1]},{model._n_clusters[2]},{model.execution_time_},{sparsity},{alg}\n")
f.close()

gx = open(output_path + alg + "_assignments_"+ tensor + "_x.txt", 'w')
for i in range(T.shape[0]):
    gx.write(f"{i}\t{model._assignment[0][i]}\n")
gx.close()


gy = open(output_path + alg + "_assignments_"+ tensor + "_y.txt", 'w')
for i in range(T.shape[1]):
    gy.write(f"{i}\t{model._assignment[1][i]}\n")
gy.close()


gz = open(output_path + alg + "_assignments_" + tensor + "_z.txt", 'w')
for i in range(T.shape[2]):
    gz.write(f"{i}\t{model._assignment[2][i]}\n")
gz.close()


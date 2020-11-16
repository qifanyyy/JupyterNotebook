from resources.four_area.DBLP4A_CreateTensor import readTensor
from algorithms.coclust_3D_tau import CoClust
from utils import CreateOutputFile, CreateLogger
from sklearn.metrics import normalized_mutual_info_score as nmi
from sklearn.metrics import adjusted_rand_score as ari
import sys
import os
import numpy as np

#os.environ["OMP_NUM_THREADS"] = '6'
if len(sys.argv)> 1 and sys.argv[1] == '-h':
    print('''
    Co-Clustering of tensor DBLP Four-Areas. Parameters (if you want to specify both, please respect the correct order):
        algorithm: string. Optional.
            Accepted values: ALT, AVG, AGG, ALT2, AGG2.
            Default value: ALT2
        level: string. Optional.
            Accepted values: DEBUG, INFO, WARNING, ERROR, CRITICAL
            Default value: WARNING
    ''')
    quit()

alg = sys.argv[1] if (len(sys.argv)> 1) and (sys.argv[1] in ['ALT','AVG','AGG','ALT2','AGG2']) else 'ALT2'
level = sys.argv[-1] if (len(sys.argv)> 1) and (sys.argv[-1] in ['DEBUG','INFO','WARNING','ERROR','CRITICAL']) else 'WARNING'
logger = CreateLogger(level)

file_name = 'final.pkl'
data_path = './resources/four_area/'
T, y, z, df = readTensor(file_name, data_path)

num_classes_y = len(set(y))
num_classes_z = len(set(z))


f, dt = CreateOutputFile("DBLP4A", date = True)

output_path = f"./output/_DBLP4A/" + dt[:10] + "_" + dt[11:13] + "." + dt[14:16] + "." + dt[17:19] + "/"
directory = os.path.dirname(output_path)
if not os.path.exists(directory):
    os.makedirs(directory)

model = CoClust(np.sum(np.shape(T)) * 10, optimization_strategy = alg, path = output_path)
model.fit(T)
tau = model.final_tau_
nmi_y = nmi(y, model.y_, average_method='arithmetic')
ari_y = ari(y, model.y_)
nmi_z = nmi(z, model.z_, average_method='arithmetic')
ari_z = ari(z, model.z_)

sparsity = 1 - (np.sum(T>0) / np.product(T.shape))

f.write(f"{T.shape[0]},{T.shape[1]},{T.shape[2]},,{num_classes_y},{num_classes_z},,{tau[0]},{tau[1]},{tau[2]},,{nmi_y},{nmi_z},,{ari_y},{ari_z},{model._n_clusters[0]},{model._n_clusters[1]},{model._n_clusters[2]},{model.execution_time_},{sparsity},{alg}\n")
f.close()

gx = open(output_path + alg + "_assignments_x.txt", 'w')
gy = open(output_path + alg + "_assignments_y.txt", 'w')
gz = open(output_path + alg + "_assignments_z.txt", 'w')
for i in range(T.shape[0]):
    gx.write(f"{i}\t{model._assignment[0][i]}\n")
for i in range(T.shape[1]):
    gy.write(f"{i}\t{model._assignment[1][i]}\n")
for i in range(T.shape[2]):
    gz.write(f"{i}\t{model._assignment[2][i]}\n")
gx.close()
gy.close()
gz.close()



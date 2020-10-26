#=========================================Ant colony algorithm for clustering==========================#


#==========import library=================#
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial import distance

#===========Load dataset===================#
dataset = pd.read_csv("/home/nikhil/Desktop/jayraman_sir/iris-species/Iris.csv")
train_data = dataset.drop(["Species","Id"],axis=1)
target = dataset.Species
q0 = 0.7
pheramone_mat = np.random.rand(150,3)
pheramone_mat1 = pd.DataFrame(pheramone_mat)
pheramone_mat1 = pheramone_mat.copy()
#pheramone_mat2 = pheramone_mat.div(pheramone_mat.sum(axis=1),axis=0)
#=============# cluster 0,1,2=============#
#============Start with m ant============#
#============Fix q0=======================#
optimum_min_dist = []
optimum_cluster = []
for i in range(10):
	min_dist = []
	main_cluster = []
	for i in range(50):
		cluster_0 = []
		cluster_1 = []
		cluster_2 = []
		for i in range(pheramone_mat1.shape[0]):
			q = np.random.uniform(0,1)
			if q < q0:
				cluster = np.argmax(pheramone_mat[i])
				cluster_0.append(i) if cluster==0 else cluster_1.append(i) if cluster==1 else cluster_2.append(i)
			else:
				phr_mat = pheramone_mat[i]/sum(pheramone_mat[i])
				phr_cumsm = np.cumsum(phr_mat)
				cluster_0.append(i) if q <= phr_cumsm[0] else cluster_1.append(i) if q <= phr_cumsm[1] else cluster_2.append(i)
			clst_0_ex = train_data.iloc[cluster_0,:]
			clst_1_ex = train_data.iloc[cluster_1,:]
			clst_2_ex = train_data.iloc[cluster_2,:]
			clstr = [clst_0_ex,clst_1_ex,clst_1_ex]
			D = []
			for j in range(pheramone_mat.shape[1]):
				x1,x2,x3,x4 =  clstr[j].SepalLengthCm.mean(),clstr[j].SepalWidthCm.mean(),clstr[j].PetalLengthCm.mean(),clstr[j].PetalWidthCm.mean()
				cord1 = [x1,x2,x3,x4]
				index = clstr[j].index
				dist11 = []
				for k in range(clstr[j].shape[0]):
					cord2 = clstr[j].loc[index[k]].tolist()
					dist = distance.euclidean(cord1,cord2)
					dist11.append(dist)
				avg_dist = np.mean(dist11)
				D.append(avg_dist)
		min_dist.append(sum(D))
		combine_cluster = [cluster_0,cluster_1,cluster_2]
		main_cluster.append(combine_cluster)

	optimum_ant = min(min_dist)
	optim_cluster = main_cluster[np.argmin(min_dist)]
	cluster_0 = optim_cluster[0]
	cluster_1 = optim_cluster[1]
	cluster_2 = optim_cluster[2]
			
	for j in cluster_0:
		pheramone_mat[j] = [pheramone_mat[j][0]*1.1,pheramone_mat[j][1]*0.9,pheramone_mat[j][2]*0.9]

	for k in cluster_1:
		pheramone_mat[k] = [pheramone_mat[k][0]*0.9,pheramone_mat[k][1]*1.1,pheramone_mat[k][2]*0.9]

	for l in cluster_2:
		pheramone_mat[k] = [pheramone_mat[l][0]*0.9,pheramone_mat[l][1]*0.9,pheramone_mat[l][2]*1.1]

	optimum_min_dist.append(optimum_ant)
	optimum_cluster.append(optim_cluster)


min_dist = np.argmin(optimum_min_dist)
print(min(optimum_min_dist))
#==============optimum cluster ===================#
opti_clstr = optimum_cluster[min_dist]




import pandas as pd
import numpy as np
import random
from tqdm import tqdm

import threading
import time
def counter():
	i = 0
	while True:
		i += 1
		print(i)
		time.sleep(1)
t = threading.Thread(target = counter)
t.start()

pd.set_option('display.expand_frame_repr', False)
file = ""

data = pd.read_csv(file)
NormAttList = data["Normal/Attack"]
data = data.drop(["Normal/Attack"], axis= 1) #only numerical data

Nself = len(data.values) # gives you the number of rows.
radius_self = 0.02 # self radius of normal data

def euc_distance(array1, array2):
	return np.power(np.sum((array1 - array2)**2) , 0.5)

def gen_detectors():
	listarray = []
	listarray.append(random.uniform(0, 1))
	listarray.append(random.uniform(0, 1))
	listarray.append(random.choice([0, 0.5 , 1.0]))
	listarray.append(random.choice([0, 0.5 , 1.0]))
	listarray.append(random.choice([0, 0.5 , 1.0]))
	return np.array(listarray)

N = 1
counter = 0
D = [x for x in range(N)]
Dradius = [x for x in range(N)]
pbar = tqdm(total=N, initial = 0, desc= "Generating detectors!")

while counter < N:
	detector = gen_detectors()
	distance_list = []

	for i in data.values:
		distance_list.append(euc_distance(i, detector))
	dmin = np.min(distance_list)
	detector_radius = dmin-radius_self

	if dmin > radius_self:
		D[counter] = detector
		Dradius[counter] = detector_radius
		counter += 1
		pbar.update(1)
pbar.close()

#############################Test Phase#####################################
file2 = "../Step 1 preprocessing data/zone1/normalized_data1_test.csv"
data2 = pd.read_csv(file2)
NormAttListTest = data2["Normal/Attack"]
data2 = data2.drop(["Normal/Attack"], axis= 1)

FP=0
FN=0
TP=0
TN=0
pbar2 = tqdm(total=len(data2.values), initial = 0, desc= "Processing detectors!")

# for i in range(N):
# 	distancelist2 = []
# 	for j,n in enumerate(data2.values): # where j is the index and n is the value
# 		distancelist2.append(euc_distance(n, D[i])) # where n is the array value of data2.value and D[i] is array value of Detectors 
# 		distmin = np.min(distancelist2)
# 		print(distmin)
# 		if distance < Dradius[i] and NormAttListTest[j] == "Attack":
# 			TP += 1
# 		elif distance > Dradius[i] and NormAttListTest[j] == "Attack":
# 			FN += 1
# 		elif distance < Dradius[i] and NormAttListTest[j] == "Normal":
# 			FP += 1
# 		elif distance > Dradius[i] and NormAttListTest[j] == "Normal":
# 			TN += 1
# 	pbar2.update(1)
# pbar2.close()

# for j,n in enumerate(data2.values):
# 	distancelist2 = []
# 	for i in range(N):
# 		distancelist2.append(euc_distance(n, D[i]) - Dradius[i])
# 	distmin = np.min(distancelist2)
# 	if distmin < 0 and NormAttListTest[j] == "Attack":
# 		TP += 1
# 	elif distmin > 0 and NormAttListTest[j] == "Attack":
# 		FN += 1
# 	elif distmin < 0 and NormAttListTest[j] == "Normal":
# 		FP += 1
# 	elif distmin > 0 and NormAttListTest[j] == "Normal":
# 		TN += 1
# 	pbar2.update(1)
# pbar2.close()

AttListTest = np.array([val == 'Attack' for val in NormAttListTest])
print(AttListTest)

testlist = data2.values.tolist()

for i in range(N):
	distance = np.sum((data2 - D[i]) ** 2,axis =1 ) **0.5
	print(distance)
	if np.sum(distance < Dradius[i]) and (AttListTest):
		TP += 1 


print("Detection Rate = ",TP/(TP+FN))
print("False Alarm Rate = ",FP/(FP+TN))
print("Check:", FN+TN+FP+TP)
print("TP = ",TP)
print("FN = ",FN)
print("FP = ",FP)
print("TN = ",TN)





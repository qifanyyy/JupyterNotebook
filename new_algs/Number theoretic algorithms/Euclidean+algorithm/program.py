import math
import copy
from random import randrange
k=10#k for 10cFV

print 'provide file name'
filename=raw_input()
f = open(filename, 'rU') 
tuples=[]
lines=0
if filename=='glass.data':
	for line in f:
		line=(line.rstrip('\n')).split(',')
		tuples.append(line[1:])
		lines=lines+1
else:
	for line in f:
		line=(line.rstrip('\n')).split()
		tuples.append(line[1:])
		lines=lines+1

tuple_len=len(tuples[0])-1	
f.close()	# to close our csv file

	
#------------------normalization starts------------------#	
for z in range (0,tuple_len):#loop for all 7 attributes
	min=float(tuples[0][z])
	max=float(tuples[0][z])
	for data in tuples:#calculating min and max for each attributes
		if float(data[z])<min:
			min=float(data[z])
		if float(data[z])>max:
			max=float(data[z])
	for i in range(0,len(tuples)):
		temp=float((float(tuples[i][z])-min)/float(max-min))# normalized value of attribute for that example data
		tuples[i][z]=float(temp)
#------------------normalization ends------------------#
	
	
training_set=[]			#will hold training examples
testing_set=[]			#will hold testing examples
indices_used=[]			#will store which examples(indices) of our total 336 examples have already been taken in testing examples.

iterations=math.ceil(float(lines)/float(k)) #total no. of examples there will be in our testing_set

def getrandom_index():#self explanatory
	global random_index
	random_index = randrange(0,len(tuples))
	for i in indices_used:#to check the random index we recieved has already been used or not
		if i==random_index:
			getrandom_index()

for i in range(0,int(iterations)):#will populate testing examples set
	global random_index
	getrandom_index()
	indices_used.append(random_index)	
	testing_set.append(tuples[random_index])

for i in range(0,lines):#will populate remaining k-1/k tuples into training set
	flag=1
	for j in indices_used:#checking whether this particular example has been used in testing set or not.
		if i==j:
			flag=0
	if flag==1:#if not used in testing set,insert it into training set
		training_set.append(tuples[i])


print 'choose distance measure'
print '1 for euclidean distance'
print '2 for Polynomial kernel'
print '3 for radial basis kernel'
distance_measure=int(raw_input())#stores which data measure user wants to use

print 'provide value of k, the number of neighbors to use for classification'
neighbour=int(raw_input())#stores the k value

def Kprev(a,b):
	if distance_measure==2:
		power=4
		dotp=0
		for index in range(0,len(a)-1):
			dotp=dotp+(a[index]*b[index])
		result=math.pow((1+dotp),power)	
		return result
	if distance_measure==3:
		euclid_d=0
		sigma_square=2.5
		for index in range(0,len(a)-1):
			euclid_d=euclid_d + (a[index]-b[index])*(a[index]-b[index])
		euclid_d=math.sqrt(euclid_d)
		tempor=(-1*(euclid_d*euclid_d))/sigma_square
		result=math.pow(2.718281,tempor)
		return result
	
		
		
def K(a,b):#implementation of kernel function 
	if distance_measure==2:#implementation of polynomial kernel
		power=4
		dotp=0
		for index in range(0,len(a)-2):
			dotp=dotp+(a[index]*b[index])
		result=math.pow((1+dotp),power)	
		return result
	if distance_measure==3:#implementation of radial basis kernel
		euclid_d=0
		sigma_square=2.5
		for index in range(0,len(a)-2):
			euclid_d=euclid_d + (a[index]-b[index])*(a[index]-b[index])
		euclid_d=math.sqrt(euclid_d)
		tempor=(-1*(euclid_d*euclid_d))/sigma_square
		result=math.pow(2.718281,tempor)
		return result	
		
def euclid_distance(a,b):#implementation of euclidean distance measure
	
	euclid_d=0
	for index in range(0,len(a)-1):
		euclid_d=euclid_d + (a[index]-b[index])*(a[index]-b[index])
	euclid_d=math.sqrt(euclid_d)
	
	return euclid_d

		
def insertionSort(temp_list):#arranges samples in increasing order of distance from example considered for knn.
	for index in range(1,len(temp_list)):
		currentvalue = temp_list[index][:]
		position = index

		while position>0 and temp_list[position-1][-1]>currentvalue[-1]:
			temp_list[position]=temp_list[position-1][:]
			position = position-1

		temp_list[position]=currentvalue[:]	

accuracy=0	
flag=True
if distance_measure==2 or distance_measure==3:#code for calculating class of examples if distance matrix chosen is either polynomial kernel 
#or radial basis kernal	 
	for j in range(0,len(training_set)):
		training_set[j].append(Kprev(training_set[j],training_set[j]))
	for j in range(0,len(testing_set)):
		testing_set[j].append(Kprev(testing_set[j],testing_set[j]))	



	for i in range(0,len(testing_set)):
		temp_training_set=[]
		for looptemp in training_set:
			temp_training_set.append(looptemp[:-1])
		xx=testing_set[i][-1]
					
		for j in range(0,len(temp_training_set)):
			yy=training_set[j][-1]
			xy=K(testing_set[i],training_set[j])
			temp_training_set[j].append(xy)
			dist=math.sqrt(xx-(2*xy)+yy)
			temp_training_set[j].append(dist)
		
		insertionSort(temp_training_set)
		
		temp_training_set=temp_training_set[0:neighbour]
		temp_count=[]
		for k in range(0,len(temp_training_set)):
			count=0
			for l in range(0,len(temp_training_set)):
				if(temp_training_set[k][-3]==temp_training_set[l][-3]):
					count=count+1
			temp_count.append(count)
		
		max=temp_count[0]
		temp_index=[]
		for k in range(0,len(temp_count)):
			if max<=temp_count[k]:
				max=temp_count[k]
			
		for k in range(0,len(temp_count)):
			if temp_count[k]==max:
				temp_index.append(k)
		
		classs=temp_training_set[temp_index[randrange(0,len(temp_index))]][-3]
		if classs==testing_set[i][-2]:
			accuracy=accuracy+1
	
	
if distance_measure==1:#code for calculating class of examples if distance matrix chosen is euclidean distance
	
	
	for i in range(0,len(testing_set)):
		temp_training_set=copy.deepcopy(training_set)
		
		
		for j in range(0,len(temp_training_set)):
			temp_training_set[j].append(euclid_distance(testing_set[i],temp_training_set[j]))
			
		insertionSort(temp_training_set)
		
		temp_training_set=temp_training_set[0:neighbour]
		temp_count=[]
		for k in range(0,len(temp_training_set)):
			count=0
			for l in range(0,len(temp_training_set)):
				if(temp_training_set[k][-2]==temp_training_set[l][-2]):
					count=count+1
			temp_count.append(count)
		
		max=temp_count[0]
		temp_index=[]
		for k in range(0,len(temp_count)):
			if max<=temp_count[k]:
				max=temp_count[k]
		
		for k in range(0,len(temp_count)):
			if temp_count[k]==max:
				temp_index.append(k)
		
		classs=temp_training_set[temp_index[randrange(0,len(temp_index))]][-2]
		
		if classs==testing_set[i][-1]:
			accuracy=accuracy+1

			
accuracy_perc=(float(accuracy)/float(len(testing_set)))*100.0#calculate percentage of samples whose classes were predicted accurate
print accuracy_perc	

import csv
import math
from random import randint
def loadfile(file,trainingset,testset):     # this function divides data into training dataset and test dataset
  with open(file,'r') as a:
    cs=csv.reader(a)
    li=list(cs)
    length=len(li)
    len1=int(length*0.67)     #normally 67% of total data is considered as training dataset
    print len1
    len2=length-len1
    print len2
    count = 0
    while count<len1:
      indx=randint(0,length-1)
      val=li[indx]
      for x in range(4):
        val[x]=float(val[x])
      if val not in trainingset:
        trainingset.append(val)
        count+=1
      else:
        pass  
    for line in li:
      for x in range(4):
        line[x]=float(line[x])
      if line not in trainingset:
        testset.append(line)
      else:
        pass
        
def calc_dist(train,test,k):
  
  no_correct_pred=0
  test_len=len(test)
  for a in range(test_len):
    dist=[]
    to_test=test[a]  #apply kNN algorithm for all test instances
    leng=len(train)  
    for i in range(leng):
      distance=0
      for x in range(4):
        distance+=(((to_test[x])-(train[i][x]))**2)  #finding the EUCLEDIAN distance ---> sqrt((x1-x2)^2+(y1-y2)^2+(z1-z2)^2+(m1-m2)^2) 
      distance=math.sqrt(distance)                   # above formula is four 4 features , hence 4 represented by 4 vertices
      dist.append([distance,train[i][4]])
  #return dist
    for i in range(leng-1):           #applying bubblesort to sort the distances in dist[][]    
      for j in range(leng-1-i):
        if dist[j][0]>dist[j+1][0]:
          dist[j],dist[j+1]=dist[j+1],dist[j]
    count_1=0        #count of iris-setosa
    count_2=0        #count of iris-versicolor
    count_3=0        #count of iris-virginica
    for i in range(k):
      if dist[i][1] == "Iris-setosa":
        count_1+=1
      elif dist[i][1] == "Iris-versicolor":
        count_2+=1
      elif dist[i][1] == "Iris-virginica":
        count_3+=1


    lis=[count_1,count_2,count_3]
    max_val=max(lis)
    if max_val == count_1:
      if to_test[4] == "Iris-setosa":
        no_correct_pred+=1
      print "predicted : Iris-sentosa and actual :",to_test[4]
    elif max_val == count_2:
      if to_test[4] == "Iris-versicolor":
        no_correct_pred+=1  
      print "predicted : Iris-versicolor and actual :",to_test[4]
    elif max_val == count_3:
      if to_test[4] == "Iris-virginica":
        no_correct_pred+=1   
      print "predicted : Iris-virginica and actual :",to_test[4]
  print "no of correct predictions ",no_correct_pred," out of ",len(test)
  accuracy=(float(no_correct_pred)/(test_len))*100   #determine accuracy=(no of correct predictions)/(total predictions)
  print "accuracy of knn alg. is %f percent" %accuracy       
          

trainingset=[]   #stores the training dataset
testset=[]       #stores the test dataset
loadfile("flower.csv",trainingset,testset)
#print trainingset
#print '*'*12
#print testset
print "enter value of k...less than size and smaller,preferably (10-15)",  #normally k=(n)^1/2 where n is no of training data instances
print "of training dataset which here is ",len(trainingset)
k=int(raw_input("k value"))
dist=calc_dist(trainingset,testset,k)



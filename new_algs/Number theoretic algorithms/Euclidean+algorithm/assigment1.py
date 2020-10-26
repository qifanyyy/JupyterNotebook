
import numpy as np
from math import sqrt
#this is function for euclidian distance
def euclidian(x1,y1,x2,y2):
     return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
#this is function for manhattan distance
def manhattan(x1,y1,x2,y2):
    return (abs(x1-x2)+abs(y1-y2))

#this part take data from file as string
with open("C:/Users/salik/OneDrive/Desktop/iris.txt", "r") as file:
   data=file.readlines()

#in this part I define some lists
iris_data=[len(data)]
training_data=[len(iris_data)*3/5]
test_data=[len(iris_data)*2/5]
distance_e=[]#keep ecludian distances
distance_m=[]#keep manhattan distances
c = []#keep ecludian distances
index_e = []#keep minimum euclidian distances index for finding which training sample closest test sample
index_m=[]#keep minimum manhattan distances index for finding which training sample closest test sample
d=[]#keep manhattan distances

#in this part I organize iris data and change iris names with 0,1,2
i=0
while(i<len(data)):
    iris_data.append(data[i].replace('Iris-setosa','0.0').replace('Iris-versicolor', '1.0').replace('Iris-virginica', '2.0').replace(',',' ').split())
    i=i+1
iris_data.pop(0)
i=0;j=0;

#in this part I convert iris data to float because I read it as a string
for i in range (0,len(iris_data)):
    for j in range (0,len(iris_data[0])):
        iris_data[i][j] = float(iris_data[i][j])
        j=j+1;
    i=i+1;
    j=0;

k=0;l=0;
#in this part I separate data as a training set and test set
for i in range (len(iris_data)):
        if(0<=i<30 or 80>i>=50 or 100<=i<130):
            training_data.append(iris_data[i])
        else:
            test_data.append(iris_data[i])
training_data.pop(0)
test_data.pop(0)

true=0;
#taking neighbours number as k and choosing distance method
k = input("Please enter odd k value: ")
if(k%2==0):
    print("Don't enter even k value")
    k = input("Please enter odd k value: ")
i=0
method=input("Please choose distance method 1-Euclidian  2-Manhattan : ")
#this part for euclidian
if(method==1):
    for m in range(len(test_data)):
        for j in range(len(training_data)):#estimating distance value between test data and training data
            distance_e.append(euclidian(test_data[m][0], test_data[m][3], training_data[j][0], training_data[j][3]))

        f = 0;
        while (f < len(distance_e)):#put distances to c list and sort it for finding minimum distances k times
            c.append(distance_e[f])
            f = f + 1;
        c.sort()
        for i in range(0, k):#finding index of minimum distances for finding which training data samples closest test samples
            index_e.append(distance_e.index(c[i]))
            distance_e[distance_e.index(c[i])] = max(distance_e)

        setosa = 0;
        versicolor = 0;
        virginica = 0;
        # this part finding iris name
        for i in range(0, k):#we are looking k neighbours and counting which iris name is max
            if (training_data[index_e[i]][4] == 0):
                setosa = setosa + 1;
            elif (training_data[index_e[i]][4] == 1):
                versicolor = versicolor + 1;
            elif (training_data[index_e[i]][4] == 2):
                virginica = virginica + 1;

        # this part looking if we can find the iris name correctly if it is right we count true results
        if (setosa > versicolor and setosa > virginica):
            if (test_data[m][4] == 0):
                true = true + 1;
        elif (versicolor > setosa and versicolor > virginica):
            if (test_data[m][4] == 1):
                true = true + 1;
        elif (virginica > versicolor and virginica > setosa):
            if (test_data[m][4] == 2):
                true = true + 1;
        # in this part we are cleaning list for use it again
        del c[:]
        del index_e[:]
        del distance_e[:]
    accuracy= ((true/60.00)*100.00)
    print "Euclidian Distance for k=", k
    print "Error count: ",60- true, "/60"
    print "Accuracy Rate: %", accuracy



#this part for manhattan
elif(method==2):
    for m in range(len(test_data)):
        for j in range(0, len(training_data)):#estimating distance value between test data and training data
            distance_m.append(manhattan(test_data[m][0], test_data[m][3], training_data[j][0], training_data[j][3]))
        j = 0;
        while (j < len(distance_m)):#put distances to c list and sort it for finding minimum distances k times
            d.append(distance_m[j])
            j = j + 1;
        d.sort()
        for i in range(0, k):#finding index of minimum distances for finding which training data samples closest test samples
            index_m.append(distance_m.index(d[i]))
            distance_m[distance_m.index(d[i])] = max(distance_m)
        setosa = 0;
        versicolor = 0;
        virginica = 0;
        # this part finding iris name
        for i in range(0, k):#we are looking k neighbours and counting which iris name is max
            if (training_data[index_m[i]][4] == 0):
                setosa = setosa + 1;
            elif (training_data[index_m[i]][4] == 1):
                versicolor = versicolor + 1;
            elif (training_data[index_m[i]][4] == 2):
                virginica = virginica + 1;
        # this part looking if we can find the iris name correctly if it is right we count true results
        if (setosa > versicolor and setosa > virginica):
            if (test_data[m][4] == 0):
                true = true + 1;
        elif (versicolor > setosa and versicolor > virginica):
            if (test_data[m][4] == 1):
                true = true + 1;
        elif (virginica > versicolor and virginica > setosa):
            if (test_data[m][4] == 2):
                true = true + 1;
        # in this part we are cleaning list for use it again
        del d[:]
        del index_m[:]
        del distance_m[:]
    accuracy= ((true/60.00)*100.00)
    print "Manhattan Distance for k=",k
    print "Error count: ",60-true,"/60"
    print "Accuracy Rate: %",accuracy



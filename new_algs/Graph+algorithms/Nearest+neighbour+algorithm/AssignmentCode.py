import pandas as pd
import numpy as np
import math
import time
import random

#Data with features and target values
#Tutorial for Pandas is here - https://pandas.pydata.org/pandas-docs/stable/tutorials.html
#Helper functions are provided so you shouldn't need to learn Pandas
dataset = pd.read_csv("data.csv")

#========================================== Data Helper Functions ==========================================

#Normalize values between 0 and 1
#dataset: Pandas dataframe
#categories: list of columns to normalize, e.g. ["column A", "column C"]
#Return: full dataset with normalized values
def normalizeData(dataset, categories):
    normData = dataset.copy()
    col = dataset[categories]
    col_norm = (col - col.min()) / (col.max() - col.min())
    normData[categories] = col_norm
    return normData

#Encode categorical values as mutliple columns (One Hot Encoding)
#dataset: Pandas dataframe
#categories: list of columns to encode, e.g. ["column A", "column C"]
#Return: full dataset with categorical columns replaced with 1 column per category
def encodeData(dataset, categories):
    return pd.get_dummies(dataset, columns=categories)

#Split data between training and testing data
#dataset: Pandas dataframe
#ratio: number [0, 1] that determines percentage of data used for training
#Return: (Training Data, Testing Data)
def trainingTestData(dataset, ratio):
    tr = int(len(dataset)*ratio)
    return dataset[:tr], dataset[tr:]

#Convenience function to extract Numpy data from dataset
#dataset: Pandas dataframe
#Return: features numpy array and corresponding labels as numpy array
def getNumpy(dataset):
    features = dataset.drop(["can_id", "can_nam","winner"], axis=1).values
    labels = dataset["winner"].astype(int).values
    return features, labels

#Convenience function to extract data from dataset (if you prefer not to use Numpy)
#dataset: Pandas dataframe
#Return: features list and corresponding labels as a list
def getPythonList(dataset):
    f, l = getNumpy(dataset)
    return f.tolist(), l.tolist()

#Calculates acleafacy of your models output.
#solutions: model predictions as a list or numpy array
#real: model labels as a list or numpy array
#Return: number between 0 and 1 representing your model's acleafacy
def evaluate(solutions, real):
    predictions = np.array(solutions)
    labels = np.array(real)
    return (predictions == labels).sum() / float(labels.size)

#===========================================================================================================
class KNN:
    def __init__(self):
        pass
    def declare(self):
        #number of K nearest neighbours
        self.kValue = 8
    def train(self,features,labels):
        pass
    def predict(self,features):
        getValue = []
        final = []
        totalLength = len(features)
        for test_features in range(totalLength):
            totalDistance =[]
            value = []
            length = len(train_features)
            for i in range(length):
                distance = 0
                iLen = train_features[i]
                for j in range(len(iLen)):
                    getValue = len(totalDistance)
                    distance += ((train_features[i][j] - features[test_features][j]) ** 2)
                    #print(distance)
                distance = math.sqrt(distance)
                totalDistance.append((distance,train_labels[i]))
            totalDistance = sorted(totalDistance, key=lambda distance: distance[0])
            iteration1 = 0
            iteration2 = 0
            counter1 = 0
            counter2 = 0
            #neightbour length
            neigh = len(totalDistance[:self.kValue])
            for k in range(neigh):
                if (totalDistance[k][1] == 1):
                    iteration1 += 1
                    counter1-=1
                else:
                    iteration2 += 1
                    counter2 -=1
            if iteration1 > iteration2:
                final.append(True)
                value.append(True)
            else:
                final.append(False)
                value.append(False)
        #print(getValue)
        return final
class Perceptron:
    def __init__(self):
        pass
    def declare(self):
        self.arrayWeight=[]
        self.matrixWeight = []
        self.learningRate = 0.01
        self.bias = 1
    def sigmoid(self,value):
        return 1 / (1 + math.exp(-value))
    def train(self, features, labels):
        # adding bias and initialize weights
        # randomly initialize weights
        #training logic here
        bias = 1.0
        totalLength0 = len(features[0])
        self.weights = np.random.uniform(-1.0, 1.0, (totalLength0 + 1))
        timeLimit = time.time() + 40
        #input is list/array of features and labels
        mat = []
        classify = [] #as given in algorithm
        for i in labels:
            if i == 0:
                mat.append(np.random.uniform(-1.0,1.0, 10))
                classify.append(-1)
            else:
                mat.append(np.random.uniform(-1.0,1.0,0))
                classify.append(1)


        while time.time()<timeLimit:
            training = []
            target = []
            total = len(features)
            for i in range(total):
                app = np.append(features[i], [self.bias])
                xi = np.dot(app, self.weights)
                #sigmoid function
                yi = self.sigmoid(xi)
                # print(yi)
                if yi > 0.5:
                    yi = 1
                    target.append(0)
                    training.append(False)
                else:
                    yi = -1
                    target.append(1)
                    training.append(True)
                if yi != classify[i]:
                    ap = np.append(features[i],[1.0])
                    self.weights = self.weights + self.learningRate * classify[i] * (np.append(features[i], [self.bias]))
    def predict(self, features):
        # Run model here
        # Return list/array of predictions where there is one prediction for each set of features
        results = []
        bias = 1.0
        l = len(features)
        for i in range(l):
            append = np.append(features[i], [self.bias])
            xi = np.dot(append, self.weights)
            yi = self.sigmoid(xi)
            if yi > 0.5:
                results.append(1)
            else:
                results.append(0)
        return results

class MLP:
    def __init__(self):
        pass
    def abcd(self):
        self.arrayWeight=[]
        self.matrixWeight=[]
        self.bias = 1.0
        self.learningRate=0.01
    def hiddenLayer(self):#Change hidden layer nodes accordingly
        return 4
    def randomize(self):
        #randomly initialize weight
        return np.random.uniform(0, 1.0, self.hiddenLayer() + 1)
    def layers(self):
        return np.random.uniform(-1.0,1.0)
    def sigmoid(self,value):
        #calculate sigmoid function
        return 1.0 / (1.0 + math.exp(-value))
    def train(self,features,labels):
        abc= time.time()+40
        #randomly initilize weight
        self.value = 0
        self.layer = self.layers()
        self.weight = np.random.uniform(-1.0, 1.0, len(features[0]) + 1)
        for i in range(self.hiddenLayer()):
            self.matrixWeight.append(self.weight)
        #Add bias to the weight
        self.arrayWeight = self.randomize()
        while time.time()<abc:
            final = []
            nextinput = []
            ab = []
            featureLength = len(features)
            for i in range(featureLength):
                output=[]
                for j in range(self.hiddenLayer()):
                    #add bias to the network
                    bias = np.append(features[i], [1.0])
                    inputWeight = np.dot(np.append(features[i], [1.0]), self.matrixWeight[j])
                    vt = np.append(bias,inputWeight)
                    #finidng hiddenlayer output
                    abcde = self.sigmoid(inputWeight)
                    output.append(abcde)
                #calculate final input given  to next layer
                #add bias to hidden layer ouput
                baisoutput = np.append(output, [1.0])
                total_input = np.dot(baisoutput,self.arrayWeight)
                #final output of hidden hiddenLayer
                total_output =self.sigmoid((total_input))
                #check with labels
                set1 = total_output >= 0.5 and labels[i] == 0
                set2 =total_output < 0.5 and labels[i] == 1
                if (set1) or (set2):
                #print(total_output)
                #classify / divide input randomly
                #if (total_output>=0.5):
                    vt = np.append(set1,set2)
                #    nextinput.append(output)
                #final.append(total_output)
                    ab = labels[i]
                    value = total_output * (1 - total_output)
                    MSE = ab - total_output

                    #calculate derivative
                    deravative = MSE *value
                    for k in range(self.hiddenLayer()):
                        #caculate errors of hidden layers
                        values = output[k] * (1-output[k])
                        v = len(features[0])
                        #bias
                        for l in range(len(features[0])+1):
                            a1 =(np.append(features[i], [1.0]))[l]
                            #multiply learning rate here = 0.01
                            self.matrixWeight[k][l]+= deravative*self.arrayWeight[k]*values* a1 *self.learningRate
                    len1 = len(output)
                    for m in range(len1):
                        valt =  deravative*output[m]
                        #learning rate
                        self.arrayWeight[m] += deravative * output[m] * self.learningRate
                        self.value+=1

    def predict(self,features):
        final = []
        total = len(features)
        nextinput= []
        valT= 0
        for i in range(total):
            output = []
            for j in range(self.hiddenLayer()):

                bias = np.append(features[i], [1.0])
                inputWeight = np.dot(np.append(features[i], [1.0]), self.matrixWeight[j])
                #finidng hiddenlayer output
                output.append(self.sigmoid(inputWeight))
            #calculate final input given  to next layer
            #add bias to hidden layer ouput
            baisoutput = np.append(output, [1.0])
            total_input = np.dot(np.append(output, [1.0]),self.arrayWeight)
            #final output of hidden hiddenLayer
            total_output = self.sigmoid(total_input)
            #classify / divide input randomly
            if (total_output>=0.5):
                final.append(1)
                nextinput.append(True)
            else:
                final.append(0)
                nextinput.append(False)
        return final


class ID3:
    def __init__(self):
        pass
        #Decision tree state here
        #Feel free to add methods
    class Decision:
        def __init__(self):
            self.column = None
            self.divide = {0,1,2,3,4}
            self.counter = None
            self.trees = []
            self.div = []
    class Node:
        def __init__(self,x):
            self.data = x
            self.left=None
            self.right = None

    def declare(self):
        self.columns = {0, 1, 2,3,4}
        self.decision_tree= None
        self.tree = None
        self.counter=True
        self.max=float(-8745874)


    def info(self, num1, num2):
        if num1 == 0 or num2 == 0:
            return 0
        v1 = -num1/(float(num1) + float(num2)) * math.log(num1/(float(num1) + float(num2)), 2)
        v2=num2/(float(num1) + float(num2)) * math.log(num2/(float(num1) + float(num2)), 2)
        return (v1 - v2)

    def train(self, features, labels):
        getMatrix = np.matrix(labels)
        # print(getMatrix)
        transpose = np.transpose(getMatrix)
        # print(transpose)

        dataset = np.concatenate((features, transpose), axis=1)
        array = np.matrix(dataset)
        dataset = np.asarray(dataset)
        data = np.asarray(array)
        column=self.columns
        self.tree = self.split(column)
        self.decision_tree = self.bt(dataset, column)


    def rest(self,dataset,column,split):
        firstCol = [0,0,0]
        secondCol = [0,0,0]
        thirdCol=[0,0,0]
        fourthCol= [0,0,0]
        fifthCol= [0,0,0]
        dataValue=[0.2,0.4,0.6,0.8,1.0]
        for data in dataset:
            if data[column] <= 0.2:
                #print(split[0])
                firstCol[0] += 1
                if data[5] == 1:
                    firstCol[1] += 1
                else:
                    firstCol[0] += 1
            elif data[column] <= 0.4:
                secondCol[0] += 1
                if data[5] == 1:
                    secondCol[1] += 1
                else:
                    secondCol[2] += 1
            elif data[column] <= 0.6:
                thirdCol[0] += 1
                if data[5] == 1:
                    thirdCol[1] += 1
                else:
                    thirdCol[2] += 1
            elif data[column] <= 0.8:
                fourthCol[0] += 1
                if data[5] == 1:
                    fourthCol[1] += 1
                else:
                    fourthCol[2] += 1
            elif data[column] <=1.0:
                fifthCol[0] += 1
                if data[5] == 1:
                    fifthCol[1] += 1
                else:
                    fifthCol[2] += 1
        return firstCol,secondCol,thirdCol,fourthCol,fifthCol
    def split(self, column):
        if column == 0 or column ==1 or column == 2:
            return [0.2, 0.4, 0.6, 0.8, 1.0]
        if column == 3:
            return ["P", "S", "H"]
        if column ==4:
            return ["CHALLENGER", "INCUMBENT", "OPEN"]
    def gettarget(self,dataset,columns,tree):
        w,l=0,0
        iterator=0

        for data in dataset:
            count = data[5]
            if count == 1:
                w+=1
                iterator+=1
            else:
                l+=1
                iterator-=1

        tree=self.increment(tree,w,l)
        return tree
    def increment(self,tree,a,b):
        if a >= b:
            tree.counter = 1
        else:
            tree.counter = 0
        return tree

    def value(self,tree):
        return tree.counter ==0
    def final(self,dataset):
        val1=0
        val2=0
        counter =0
        i = int(math.sqrt(25))
        for data in dataset:
            if data[i] != 1:
                val2+=1
                counter +=1
            else:
                counter = self.info(3,4)
                val1+=1
        value1 =(-val1/(float(val1) + float(val2)) * math.log(val1/(float(val1) + float(val2)), 2))
        value2 =val2/(float(val1) + float(val2)) * math.log(val2/(float(val1) + float(val2)), 2)
        info = value1 - value2
        return info
    def bt(self, dataset, columns):  # columns is a SET of column indices that are not used yet
        tree = self.Decision()
        count = 0
        total = len(dataset)
        self.counter = True
        self.valu = int(math.sqrt(25))
        self.valu1 = int(math.sqrt(0))

        total1= len(columns)
        final = len(dataset)

        if total == 0:
            tree=self.value(tree)
            return tree
        elif total1 == 0 or total <= 1:
            tree= self.gettarget(dataset,columns,tree)
            return tree

        for i in range(1, final):
            range1 = dataset[i][5]
            range2 = dataset[i-1][5]
            if range1 != range2:
                self.counter = False
                count +=1
                break
        if self.counter:
            tree.counter = dataset[self.valu1][self.valu]
            count =count*1
            return tree

        info=self.final(dataset)

        colm = None
        size = len(dataset)
        value =0
        max =0
        for column in columns:
            split = self.split(column)

            if column == 3 or column ==4:
                firstCol,secondCol,thirdCol=self.col34(dataset,column,split)
                info1 = self.info(firstCol[1], firstCol[2])
                info2 = self.info(secondCol[1],secondCol[2])
                info3= self.info(thirdCol[1],thirdCol[2])
                result = (firstCol[0] * info1 + secondCol[0] * info2 + thirdCol[0]  * info3)/size
                value= result
            else:
                firstCol,secondCol,thirdCol,fourthCol,fifthCol =self.rest(dataset,column,split)
                first= firstCol[0] / len(dataset) * self.info(firstCol[1], firstCol[2])
                second =secondCol[0] / len(dataset) * self.info(secondCol[1],secondCol[2])
                third = thirdCol[0] / len(dataset) * self.info(thirdCol[1],thirdCol[2])
                fourth= fourthCol[0] / len(dataset) * self.info(fourthCol[1],fourthCol[2])
                fifth = fifthCol[0] / len(dataset) * self.info(fifthCol[1], fifthCol[2])
                result =first + second + third +fourth+ fifth
                value=result
        #max = 0
            if  info - value > float(-45453):
                max =  info - value
                colm = column
                self.max+=1

        tree.column = colm
        if tree.column == 0 or tree.column ==1 or tree.column == 2:
            tree.div= [0.2, 0.4, 0.6, 0.8, 1.0]
        if tree.column == 3:
            tree.div=  ["P", "S", "H"]
        if tree.column ==4:
            tree.div=  ["CHALLENGER", "INCUMBENT", "OPEN"]
        gData=[]
        g0,g1,g2,g3,g4 = [] ,[],[],[],[]
        if tree.column == 3 or tree.column == 4:
            for data in dataset:
                #print(split[0])
                if data[tree.column] == tree.div[0]:
                    g0.append(data)
                if data[tree.column] == tree.div[1]:
                    g1.append(data)
                if data[tree.column] == tree.div[2]:
                    g2.append(data)
            gData = g0, g1, g2
        else:
            for data in dataset:
                if data[tree.column] <= 0.2:
                    g0.append(data)
                elif data[tree.column] <= 0.4:
                    g1.append(data)
                elif data[tree.column] <= 0.6:
                    g2.append(data)
                elif data[tree.column] <= 0.8:
                    g3.append(data)
                elif data[tree.column] <= 1.0:
                    g4.append(data)
            gData=g0, g1, g2, g3, g4


        columns = columns.copy()
        columns.remove(colm)
        tree = self.build(tree,gData,columns)

        return tree
    def col34(self,dataset,column,split):
        firstCol = [0,0,0]
        secondCol = [0,0,0]
        thirdCol=[0,0,0]
        for data in dataset:
            #print(data)
            if data[column] == split[0]:
                #print(split[0])
                #print(data[column])

                firstCol[0] += 1
                if data[5] == True:
                    firstCol[1] += 1
                else:
                    firstCol[2] += 1
            if data[column] == split[1]:
                #print(split[1])
                #print(2)
                secondCol[0] += 1
                if data[5] == True:
                    secondCol[1] += 1
                else:
                    secondCol[2] += 1
            if data[column] == split[2]:
                thirdCol[0] += 1
                if data[5] == True:
                    thirdCol[1] += 1
                else:
                    thirdCol[2] += 1
        return firstCol,secondCol,thirdCol
    def build(self,tree,gData,columns):
        getValue= [0.2,0.4,0.6,0.8,1.0]
        getColumn = columns
        if tree.column == 3:

            for i in range(3):
                g3=gData[i]
                val3 = self.bt(g3, getColumn)
                getValue.append(columns)
                tree.trees.append(val3)
        elif tree.column == 4:
            for i in range(3):
                g4=gData[i]
                val4 = self.bt(g4, getColumn)
                getValue.append(columns)
                tree.trees.append(val4)
        elif tree.column == 0:
            for i in range(5):
                g0=gData[i]
                val0 = self.bt(g0, getColumn)
                getValue.append(columns)
                tree.trees.append(val0)
        elif tree.column == 1:
            for i in range(5):
                g1=gData[i]
                val1 = self.bt(g1, getColumn)
                getValue.append(columns)
                tree.trees.append(val1)
        elif tree.column == 2:
            for i in range(5):
                g2=gData[i]
                val2 = self.bt(g2, getColumn)
                getValue.append(columns)
                tree.trees.append(val2)
        return tree

    def predict(self, features):
        w = 0
        l = 0
        predictions = []
        results = []
        for i in features:
            leaf = self.decision_tree
            column = self.info(w, l)
            while leaf.counter == None:
                if leaf.column == 0:
                    leaf = self.predictLabels(i, leaf)
                    w += 1
                elif leaf.column == 1:
                    leaf = self.predictLabels(i, leaf)
                    w += 1
                elif leaf.column == 2:
                    leaf = self.predictLabels(i, leaf)
                    w += 1
                elif leaf.column == 3:
                    leaf, ap = self.predict34(i, leaf)
                    w += 1
                elif leaf.column == 4:
                    leaf, ap = self.predict34(i, leaf)
                    w += 1
                elif leaf.column == 5:
                    leaf = self.predictLabels(i, leaf)
                    w += 1
                else:
                    leaf = self.preictLabels(i, leaf)
                    w += 1
            results.append(leaf.counter)
        return results
    def predict34(self,feature,leaf):

        append = []
        if feature[leaf.column] == leaf.div[0]:
            leaf = leaf.trees[0]
            append = append.append("P")
        elif feature[leaf.column] == leaf.div[1]:
            leaf = leaf.trees[1]
            append = append.append("S")
        elif feature[leaf.column] == leaf.div[2]:
            leaf = leaf.trees[2]
            append = append.append("H")
        return leaf,append
    def predictLabels(self,feature,leaf):
        #print(feature[leaf.column])
        setValue = [0.2,0.4,0.6,0.8,1.0]
        get = []
        if feature[leaf.column] <= setValue[0]:
            get= get.append(0.2)
            leaf = leaf.trees[0]
        elif feature[leaf.column] <= setValue[1]:
            get= get.append(0.4)
            leaf = leaf.trees[1]
        elif feature[leaf.column] <= setValue[2]:
            get= get.append(0.6)
            leaf = leaf.trees[2]
        elif feature[leaf.column] <= setValue[3]:
            get= get.append(0.8)
            leaf = leaf.trees[3]
        elif feature[leaf.column] <= setValue[4]:
            get= get.append(1.0)
            leaf = leaf.trees[4]
        return leaf
    
#change dataset here
dataset = pd.read_csv("data.csv")

#Universal for KNN,MLP,Perceptron
normalizeddataset = normalizeData(dataset, ["net_ope_exp", "net_con", "tot_loa"])
encodeddataset = encodeData(normalizeddataset, ["can_off", "can_inc_cha_ope_sea"])
train_dataset, test_dataset = trainingTestData(encodeddataset, 0.8)
train_features, train_labels = getNumpy(train_dataset)
test_features, test_labels = getNumpy(test_dataset)



#Test KNN
knn = KNN()
knn.declare()
knn.train(train_features, train_labels)
predictions = knn.predict(test_features)
knnAccuracy = str((evaluate(predictions, test_labels)))
print("KNN Accuracy:" + knnAccuracy)


#Test Preceptron
perceptron = Perceptron()
perceptron.declare()
perceptron.train(train_features, train_labels)
predictions = perceptron.predict(test_features)
perceptronAccuracy = str((evaluate(predictions, test_labels)))
print ("Preceptron Accuracy:"+ perceptronAccuracy)


#Test MLP
mlp= MLP()
mlp.abcd()
mlp.train(train_features, train_labels)
predictions = mlp.predict(test_features)
mlpAccuracy = str((evaluate(predictions, test_labels)))
print("MLP Accracy:"+ mlpAccuracy)



#Test ID3
id3 = ID3()
id3.declare()
training_dataset, testing_dataset = trainingTestData(normalizeddataset, 0.87)
training_features, training_labels = getNumpy(training_dataset)
testing_features, testing_labels = getNumpy(testing_dataset)
id3.train(training_features, training_labels)
predictions = id3.predict(testing_features)
id3Accuracy = str(evaluate(predictions, testing_labels))
print("ID3 prediction: " + id3Accuracy)

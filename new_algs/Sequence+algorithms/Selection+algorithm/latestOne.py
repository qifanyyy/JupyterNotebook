import pandas as pd
import numpy as np
import random
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from deap import creator, base, tools, algorithms
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
import sys
import math
import time
import warnings
import csv
warnings.filterwarnings("ignore")


def avg(l):
    """
    Returns the average between list elements
    """
    return sum(l)/float(len(l));




def getFitness(individual, X, y):
    """
    Feature subset fitness function
    """

    if(individual.count(0) != len(individual)):
        # get index with value 0
        cols = [index for index in range(len(individual)) if individual[index] == 0]

        # get features subset
        X_parsed = X.drop(X.columns[cols], axis=1)
        X_subset = pd.get_dummies(X_parsed)

        # apply classification algorithm
        clf = DecisionTreeClassifier()


        return (avg(cross_val_score(clf, X_subset, y, cv=10)),)
    else:
        return(0,)


def geneticAlgorithm(X, y, n_population, n_generation):
    """
    Deap global variables
    Initialize variables to use eaSimple
    """
    # create individual
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    # create toolbox
    toolbox = base.Toolbox()
    toolbox.register("attr_bool", random.randint, 0, 1)
    toolbox.register("individual", tools.initRepeat,
                     creator.Individual, toolbox.attr_bool, len(X.columns))
    toolbox.register("population", tools.initRepeat, list,
                     toolbox.individual)
    toolbox.register("evaluate", getFitness, X=X, y=y)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    # initialize parameters
    pop = toolbox.population(n=n_population)
    hof = tools.HallOfFame(n_population * n_generation)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)

    # genetic algorithm
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.6, mutpb=0.2,
                                   ngen=n_generation, stats=stats, halloffame=hof,
                                   verbose=True)

    # return hall of fame
    return hof


def bestIndividual(hof, X, y):
    """
    Get the best individual
    """
    maxAccurcy = 0.0
    for individual in hof:
        g = individual.fitness.values
        if(g[0] > maxAccurcy):
            maxAccurcy = g[0]
            _individual = individual


    _individualHeader = [list(X)[i] for i in range(
        len(_individual)) if _individual[i] == 1]
    return _individual.fitness.values, _individual, _individualHeader


def getArguments():
    """
    Get argumments from command-line
    If pass only dataframe path, pop and gen will be default
    """
    dfPath = sys.argv[1]
    if(len(sys.argv) == 5):
        pop = int(sys.argv[2])
        gen = int(sys.argv[3])
        partitions = int(sys.argv[4])
    else:
        pop = 10
        gen = 2
        partitions = 4
    return dfPath, pop, gen, partitions


if __name__ == '__main__':
    # get dataframe path, population number and generation number from command-line argument
    dataframePath, n_pop, n_gen , partitions= getArguments()
    # read dataframe from csv
    df = pd.read_csv(dataframePath, sep=',')
    output=[]
    #csv_header=[ "Dataset","Feautres before GA","Features after Ga","Accuracy for directly passing dataset to the classifer","accuracy after GA","Majority Voting classifer","Number of blocks","Time taken in sec when entire dataset is passed ","Time for GA", "Time for Majority voting classifier"]
    #with open('OptimalFeatureSelectionOutput.csv', 'w') as csvFile:
    #     writer = csv.writer(csvFile)
        # writer.writerow(csv_header)
    #csvFile.close()

# encode labels column to numbers
    le = LabelEncoder()
    le.fit(df.iloc[:, -1])
    y = le.transform(df.iloc[:, -1])
    X = df.iloc[:, :-1]

    # get accuracy with all features
    t1=time.time()
    individual = [1 for i in range(len(X.columns))]

    totalfeatures=individual.count(1)
    fitval=avg(getFitness(individual, X, y))
    print(("Accuracy with all features: (directly passing dataset)\t" +
          str(fitval)+ "\n"))
    t1=time.time()-t1;

    t2=time.time();
    # apply genetic algorithm
    hof = geneticAlgorithm(X, y, n_pop, n_gen)

    # select the best individual
    #print(hof)
    accuracy, individual, header = bestIndividual(hof, X, y)
    print(('Best Accuracy: \t' + str(accuracy)))
    print(('Number of Features in Datset: \t' + str(individual.count(0)+individual.count(1))))
    print(('Number of Features in Subset: \t' + str(individual.count(1))))
    print(('Individual: \t\t' + str(individual)))
    print(('Feature Subset\t: ' + str(header)))

    genfeatures=individual.count(1)
    print('\n\ncreating a new classifier with the result of genetic algorithm')

    # read dataframe from csv one more time
    df = pd.read_csv(dataframePath, sep=',')

    # with feature subset
    X = df[header]
    #print(header)


    print(individual)
    clf = DecisionTreeClassifier()

    scores = cross_val_score(clf, X, y, cv=10)
    fitval1=avg(scores)
    print(("Accuracy with Feature Subset: \t(after doing geneticAlgoSel)" + str(fitval1) + "\n"))

    t3=time.time()-t2;
    #print((df[header].corr()))
    df1= df[header].corr()
    df1['mean'] = df1.mean(axis=1)
    sorted_df = df1.sort_values(by='mean')
    index_list=list(sorted_df.index.values)
    direction=1
    i=0
    blocks=[[] for i in range(partitions)]
    while i<len(index_list):
             if(direction==1):
                 for j in range(partitions):
                     blocks[j].append(index_list[i])
                     i=i+1
                     if(i>=len(index_list)):
                         break
                 direction=-1
             elif(direction==-1):
                 for j in range(partitions):
                     blocks[partitions-j-1].append(index_list[i])
                     i=i+1
                     if(i>=len(index_list)):
                         break
                 direction=1
    temp=[]
    clf = DecisionTreeClassifier()
    for i in range(partitions):
        dt="dt"+str(i)
        temp.append((dt,clf))
    eclf1 = VotingClassifier(estimators=temp, voting='hard')
    eclf1 = eclf1.fit(X, y)
    scores= cross_val_score(eclf1, X, y,cv=10)
    fitval3=avg(scores)
    print(("Accuracy after Majority Voting: \t" +str(fitval3)   + "\n"))
    t4=time.time()-t2;
    print("Time taken when passed entire dataset: "+str(t1));
    print("Time taken for doing genetic algorithm: "+str(t3));
    print("Time taken for majority votin classifer: "+str(t4));
    output.insert(0,dataframePath)
    output.insert(1,totalfeatures)
    output.insert(2,genfeatures)
    output.insert(3,fitval)
    output.insert(4,fitval1)
    output.insert(5,fitval3)
    output.insert(6,partitions)
    output.insert(7,t1)
    output.insert(8,t3)
    output.insert(9,t4)
    with open('OptimalFeatureSelectionOutput.csv', 'a') as csvFile:
         writer = csv.writer(csvFile)
         writer.writerow(output)
    csvFile.close()

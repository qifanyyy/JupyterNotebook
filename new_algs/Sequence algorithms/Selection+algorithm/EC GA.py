import pandas as pd
import warnings
import random
from sklearn.model_selection import cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import BayesianRidge
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import median_absolute_error
from time import clock
from sklearn.metrics import accuracy_score


def getFitness(individual, df):
    """"
    calculate fitness by using multiple classifier
    """
    X = df.iloc[:, [bool(individual[x]) for x in range(len(individual))]].values
    y = df.iloc[:, -1].values

    if (individual.count(1) == 0): # 一个都没选中
        return 0
    elif(y.dtype=="float64"):
        test = []
        prediction = []
        model = LinearRegression()
        kf = KFold(n_splits=10)  # 分成10份，从前往后
        for train_index, test_index in kf.split(df):
            X_train, X_test = X[train_index], X[
                test_index]  # 一共10次，分别的X_train, X_test, y_train, y_test是从第一个前10，第二个前10，第三个前10...
            y_train, y_test = y[train_index], y[test_index]
            model.fit(X_train, y_train)
            pred = model.predict(X_test)  # 会是很多值，各个预测出来的

            prediction += [pred[x] for x in range(len(pred))]
            test += [y_test[x] for x in range(len(y_test))]

        # error = mean_absolute_error(test, prediction) # mean absolute error
        error = mean_squared_error(test, prediction)**0.5 # root mean squared error
        # error = median_absolute_error(test, prediction) # median absolute error

        return 10**3 / error
    else:
        # Categorical values
        clf = LogisticRegression() #对于continuous value不可以
        knn = KNeighborsClassifier(n_neighbors=5) #对于continue value不可行
        reg = BayesianRidge()
        clft = DecisionTreeClassifier()
        mlp = MLPClassifier(solver='sgd', activation='relu',alpha=1e-4,hidden_layer_sizes=(50,2), random_state=1,max_iter=100,learning_rate_init=.1)

        fit = cross_validate(clft, X, y, cv=10)["test_score"] # 10-cross validate random?

        fitness = (sum(fit) / float(len(fit)))

        return fitness


def geneticAlgorithm(individual, df, pop, gen):
    """"
    select initial gens, randomly generate pop individuals
    generate pop number offsprings by using every 2 individuals for crossover
    for every offspring after crossover, mutate 1 bit, and get the pop number mutations
    calculate each 2 parents and 2 mutations, select 2 with highest fitness as a part of new population
    save the max, min of each generation. print result
    """
    #random generate 20 initially,
    population = []
    for x in range(pop):
        G = [random.randint(0,1) for i in range(len(individual))]
        population.append(G)

    print("gen".ljust(10) + "avg".ljust(20) + "min".ljust(20) + "max".ljust(20) + "best individual in this generation".ljust(20))
    MAX = 0
    GEN = []
    for g in range(gen):
        population = random.sample(population, len(population)) #打乱
        # crossover 生成 相同个数 offspring
        offspring = getCrossover(population,individual)
        # mutation 选择两个进行变异
        mutation = getMutation(offspring,individual)

        population, sum, Max, Min, G = updatePopulation(population, mutation, pop, df)

        avg = sum/pop
        if(Max>MAX):
            MAX = Max
            GEN.clear()
            GEN.append(G)
        elif(Max == MAX):
            for x in range(len(GEN)):
                if(GEN[x]==G):
                    break
                elif(GEN[x]!=G and x == (len(GEN)-1)):
                    GEN.append(G)
        print(str(g+1).ljust(10) + str('%.6f' % avg).ljust(20) + str('%.6f' % Min).ljust(20) + str('%.6f' % Max).ljust(20) + str(G).ljust(20))
    return MAX, GEN

def getCrossover(population,individual):
    offspring = []
    for x in range(len(population) // 2):
        lens = len(individual)  # 5
        r = random.randint(1, lens - 1)  # 选择1到4 #选择不包括父类
        offspring.append(  # 长度：0-random,random-5
            [population[x * 2][i] for i in range(r)] + [population[x * 2 + 1][j] for j in range(r, lens)]
        )
        offspring.append(
            [population[x * 2 + 1][i] for i in range(r)] + [population[x * 2][j] for j in range(r, lens)]
        )
    return offspring

def getMutation(offspring, individual):
    mutation = []
    for i in range(len(offspring)):
        m = [offspring[i][j] for j in range(len(individual))]  # 得到要mutation的对象
        for x in range(1):  # mutate 1 个
            r = random.randint(0, len(individual) - 1)
            m[r] = (m[r] + 1) % 2
        mutation.append(m)
    return mutation

def updatePopulation(population, mutation, pop, df):
    sum = 0
    Max = 0  # 局最大
    Min = getFitness(population[0], df)  # 一代generation里面的最小
    G = []
    for x in range(pop // 2):
        list = []
        list.append(population[x * 2])
        list.append(population[x * 2 + 1])
        list.append(mutation[x * 2])
        list.append(mutation[x * 2 + 1])
        fit = []
        fit.append(getFitness(population[x * 2], df))
        fit.append(getFitness(population[x * 2 + 1], df))
        fit.append(getFitness(mutation[x * 2], df))
        fit.append(getFitness(mutation[x * 2 + 1], df))

        G1 = G2 = Gt = []  # 对应最大值的基因，次大值的基因, 两个变量要跟前面一样，以循环当父类
        max = submax = temp = 0  # 最大值，次大值
        for y in range(4):
            if (fit[y] > max and G1 != list[y]):
                temp = max
                Gt = G1
                max = fit[y]
                G1 = list[y]
                if (max > Max):  # 保留一个generation中最大值
                    G = G1
                    Max = max
                if (temp > submax and Gt != G2):
                    submax = temp
                    G2 = Gt
            elif (fit[y] > submax and G2 != list[y]):
                submax = fit[y]
                G2 = list[y]
            elif (fit[y] < Min):  # 保留全局最小
                Min = fit[y]
        population[x * 2] = G1
        population[x * 2 + 1] = G2
        sum += max + submax
    return population, sum, Max, Min, G


if __name__ == '__main__':
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=Warning)
    # dataframePath = 'datasets/adult.csv'
    # dataframePath = 'datasets/online_shoppers_intention.csv'

    # dataframePath = 'sample/automobile_data.csv'
    dataframePath = 'sample/adult_sample.csv'
    # dataframePath = 'sample/bank_full_sample.csv'
    # dataframePath = 'sample/IMDB_movie_sample.csv'
    pop = 30      # population  how?
    gen = 100       # generation
    df = pd.read_csv(dataframePath, sep=',')

    # df = df.sample(frac=1).reset_index(drop=True) #打乱instance

    #converge nom to num and store
    le = LabelEncoder()
    cols = [df.columns[x] for x in range(len(df.columns))]
    for i in range(len(df.columns)):
        if(df[cols[i]].dtypes == 'object'): #最后一个是否也要labeling？
            temp = le.fit_transform(df[cols[i]])
            m = pd.DataFrame(temp)
            df[cols[i]] = m
    individual = [1 for i in range(len(df.columns)-1)] # select all [1,1,1,1,1,1] 不包括predicted

    fit = getFitness(individual, df)
    if (df.iloc[:, -1].values.dtype == "float64"):
        print("\nFitness of all features: \t" + str('%.6f' % fit).ljust(20) + "(Error: " + str(10 ** 3 / fit) + ")")
    else:
        print("\nAccuracy of all features: \t" + str('%.6f' % fit).ljust(20))

    print("All Features " + str([df.columns[x] for x in range(len(df.columns))]) + "\n")
    print("Population: " + str(pop).ljust(10) + "Generation: " + str(gen))

    start = clock()
    bestAccuracy, individuals = geneticAlgorithm(individual, df, pop, gen) #返回最好的 fitness 跟 同这个精确度的 list[所有元素]
    end = clock()

    print("\nRunning time: " + str('%.4f' % (end - start)) + " s".ljust(10), end='')
    if (df.iloc[:, -1].values.dtype == "float64"):
        print("Best Fitness: " + str('%.6f' % bestAccuracy).ljust(20) + "(Error: " + str(10**3 / bestAccuracy) + ")")
    else:
        print("Best Accuracy: " + str('%.6f' % bestAccuracy).ljust(20))

    for i in range(len(individuals)):
        print("Individual[" + str(i) + "]: ".ljust(10) + "    " + str(individuals[i]) + "Num of Features: ".rjust(30) + str(individuals[i].count(1)))
        I = individuals[i] + [0]
        FS = [df.columns[x] for x in range(len(I)) if I[x] == 1]
        print("Feature Subset[" + str(i) + "]: ".ljust(10) + str(FS))


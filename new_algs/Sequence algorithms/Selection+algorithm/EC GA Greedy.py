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


def getFitness(individual, df):
    """"
    calculate fitness by using multiple classifier
    """
    X = df.iloc[:, [bool(individual[x]) for x in range(len(individual))]].values
    y = df.iloc[:, -1].values

    if (individual.count(1) == 0): # 一个都没选中
        return 0
    elif(y.dtype=="float64"):  # Continue values
        test = []
        prediction = []
        model = LinearRegression()
        kf = KFold(n_splits=10, random_state=5)  # 分成10份，从前往后
        for train_index, test_index in kf.split(df):
            X_train, X_test = X[train_index], X[test_index]  # 一共10次，分别的X_train, X_test, y_train, y_test是从第一个前10，第二个前10，第三个前10...
            y_train, y_test = y[train_index], y[test_index]
            model.fit(X_train, y_train)
            pred = model.predict(X_test)  # 会是很多值，各个预测出来的

            prediction += [pred[x] for x in range(len(pred))]
            test += [y_test[x] for x in range(len(y_test))]

        # error = mean_absolute_error(test, prediction)  # mean absolute error
        error = mean_squared_error(test, prediction)**0.5 # root mean squared error
        # error = median_absolute_error(test, prediction) # median absolute error

        return 10**3 / error
    else:
        clf = LogisticRegression() #对于continuous value不可以
        knn = KNeighborsClassifier(n_neighbors=5) #对于continue value不可行
        reg = BayesianRidge()
        clft = DecisionTreeClassifier()
        mlp = MLPClassifier(solver='sgd', activation='relu', alpha=1e-4, hidden_layer_sizes=(50, 2), random_state=1, max_iter=100, learning_rate_init=.1)

        fit = cross_validate(clft, X, y, cv=10)["test_score"]  # 10-cross validate random?
        fitness = (sum(fit) / float(len(fit)))

        return fitness


def geneticAlgorithm(individual, df, pop, gen):
    """"
    select initial genes, all 1 and all 0
    generate various(pop) offsprings
    randomly select 2 offsprings for mutation
    select parts of offspring and mutation as population (pop-pop//8-1) (pop//8+1)
    calculate all fitness of population, save the max, submax, min, and print result
    max and submax as the 2 parents for the next generation
    """
    #random generate 20 intially.
    G1 = individual
    G2 = [0 for x in range(len(individual))]  #两个父类是不是一定要选入population待定？
    print("gen".ljust(10) + "avg".ljust(20) + "min".ljust(20) + "max".ljust(20) + "best individual in this generation".ljust(20))
    MAX = 0
    GEN = []
    for g in range(gen):
        # crossover 生成 offspring
        offspring = getCrossover(G1,G2) #给两个父类基因，输出一个list的所有子类基因
        # mutation 选择两个进行变异
        m1 = random.choice(offspring)
        m2 = random.choice(offspring)
        # print(str(g1) + str(g2))
        mutation = getMutation(m1, m2)
        # 从 offspring 跟 mutation 里面分别选几个作为population
        population = getPopulation(offspring, mutation)

        G1 = G2 = [] #对应最大值的基因，次大值的基因, 两个变量要跟前面一样，以循环当父类
        max = submax = sum = 0 #最大值，次大值，总和
        min = getFitness(population[0],df) #刚开始最小值先取第零个

        # 计算所有fitness，并保留最大，次大，最小，和，并输出
        for x in range(pop):
            fit = getFitness(population[x],df)
            sum += fit
            if(fit > max and G1 != population[x]): #最大值得到
                temp = max
                Gt = G1
                max = fit
                G1 = population[x]
                if(temp > submax and Gt != G2): #原本最大值退给次大值，原本已包含最大值不等于次大值
                    submax = temp
                    G2 = Gt
            elif(fit > submax and G2 != population[x]): #次大值得到
                submax = fit
                G2 = population[x]
            elif(fit < min): #最小值
                min = fit

        avg = sum/pop
        # 保留全局最大值跟相同fitness的基因型
        if(max > MAX): #全局最大值
            MAX = max
            GEN.clear()
            GEN.append(G1)
        elif(max == MAX):
            for x in range(len(GEN)):
                if(GEN[x]==G1):
                    break
                elif(GEN[x]!=G1 and x == (len(GEN)-1)):
                    GEN.append(G1) #保留相同fitness但是不同基因的gen
        print(str(g+1).ljust(10) + str('%.6f'%avg).ljust(20) + str('%.6f'%min).ljust(20) + str('%.6f'%max).ljust(20) + str(G1).ljust(20))
    return MAX, GEN

def getCrossover(Gen1, Gen2):
    offspring = []
    lens = len(Gen1)
    for i in range(0, lens):    #此时包括父类在内
        offspring.append(
            [Gen1[j] for j in range(i)] + [Gen2[j] for j in range(i, lens)]
        )
        offspring.append(
            [Gen2[j] for j in range(i)] + [Gen1[j] for j in range(i, lens)]
        )
    return offspring

def getMutation(Mut1, Mut2):
    mutation = []
    for i in range(len(Mut1)):
        a = [Mut1[x] for x in range(len(Mut1))]  # 这样就不是指针赋值
        a[i] = (a[i] + 1) % 2  # 把a的其中一个变成0/1
        mutation.append(a)
    for i in range(len(Mut2)):
        a = [Mut2[x] for x in range(len(Mut2))]  # 这样就不是指针赋值
        a[i] = (a[i] + 1) % 2  # 把a的其中一个变成0/1
        mutation.append(a)
    return mutation

def getPopulation(offspring, mutation):
    population = []
    for m in range(pop // 8 + 1):
        population.append(random.choice(mutation))  # 从变异里面取一部分存储在population
    for s in range(pop // 8 + 1, pop):
        population.append(random.choice(offspring))  # 从直接后代里面去一部分存储在population
    return population


if __name__ == '__main__':
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=Warning)
    # dataframePath = 'datasets/adult.csv'

    dataframePath = 'sample/automobile_data.csv'
    # dataframePath = 'sample/adult_sample.csv'
    # dataframePath = 'sample/bank_full_sample.csv'
    pop = 50      # population  how?
    gen = 100       # generation
    df = pd.read_csv(dataframePath, sep=',')

    # df = df.sample(frac=1).reset_index(drop=True)  # 打乱instance

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
        print("\nFitness of all features: \t" + str('%.6f'%fit).ljust(20) + "(Error: " + str(10**3 / fit) + ")")
    else:
        print("\nAccuracy of all features: \t" + str('%.6f'%fit).ljust(20))

    print("All Features " + str([df.columns[x] for x in range(len(df.columns))]) + "\n")
    print("Population: " + str(pop).ljust(10) + "Generation: " + str(gen))

    start = clock()
    bestAccuracy, individuals = geneticAlgorithm(individual, df, pop, gen) #返回最好的 fitness 跟 同这个精确度的 list[所有元素]
    end = clock()

    print("\nRunning time: " + str('%.4f' % (end-start)) + " s".ljust(10), end='')
    if (df.iloc[:, -1].values.dtype == "float64"):
        print("Best Fitness: " + str('%.6f' % bestAccuracy).ljust(20) + "(Error: " + str(10**3 / bestAccuracy) + ")")
    else:
        print("Best Accuracy: " + str('%.6f' % bestAccuracy).ljust(20))

    for i in range(len(individuals)):
        print("Individual[" + str(i) + "]: ".ljust(10) + "    " + str(individuals[i]) + "Num of Features: ".rjust(30) + str(individuals[i].count(1)))
        I = individuals[i] + [0]
        FS = [df.columns[x] for x in range(len(I)) if I[x] == 1]
        print("Feature Subset[" + str(i) + "]: ".ljust(10) + str(FS))


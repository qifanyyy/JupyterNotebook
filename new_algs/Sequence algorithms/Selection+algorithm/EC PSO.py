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
        kf = KFold(n_splits=10, random_state=5)  #分成10份，从前往后
        for train_index, test_index in kf.split(df):
            X_train, X_test = X[train_index], X[test_index] # 一共10次，分别的X_train, X_test, y_train, y_test是从第一个前10，第二个前10，第三个前10...
            y_train, y_test = y[train_index], y[test_index]
            model.fit(X_train,y_train)
            pred = model.predict(X_test) # 会是很多值，各个预测出来的

            prediction += [pred[x] for x in range(len(pred))]
            test += [y_test[x] for x in range(len(y_test))]

        # error = mean_absolute_error(test, prediction) # mean absolute error
        error = mean_squared_error(test, prediction)**0.5 # root mean squared error
        # error = median_absolute_error(test, prediction) # median absolute error

        return 10**3/error
    else:
        # Categorical values
        clf = LogisticRegression() #对于continuous value不可以
        knn = KNeighborsClassifier(n_neighbors=5) #对于continue value不可行
        reg = BayesianRidge()
        clft = DecisionTreeClassifier()
        mlp = MLPClassifier(solver='sgd', activation='relu', alpha=1e-4, hidden_layer_sizes=(50, 2), random_state=1, max_iter=100, learning_rate_init=.1)

        fit = cross_validate(clft, X, y, cv=10)["test_score"] # 10-cross validate random?
        fitness = (sum(fit) / float(len(fit)))

        return fitness


class particle():#初始化位置，速度，pbest位置，pbest值
    # iris: 0.5, 2
    # nuclear: 0.2, 1
    # lung-cancer: 0.2, 0.4
    # automobile_data:
    w = 0.01
    c1 = 0.02
    c2 = 0.02
    def __init__(self, individual, df):
        self.individual = individual #初始化用
        self.df = df

        #初始化位置random，速度0，最好位置，最好值
        self.position = [random.getrandbits(1) for i in range(len(individual))]
        self.velocity = 0 #可以小数？
        self.Pbest_position = [self.position[x] for x in range(len(self.position))] #也可以就用self.position
        self.Pbest_value = getFitness(self.position,self.df)

    def move(self,Gbest_position,Gbest_value):
        r1 = random.random()
        r2 = random.random()
        # print(self.velocity)
        new_velocity = self.w * self.velocity + self.c1*r1*(self.toDeci(self.Pbest_position)-self.toDeci(self.position))\
                       +self.c2*r2*(self.toDeci(Gbest_position)-self.toDeci(self.position)) #转成十进制计算是否好？
        self.velocity = new_velocity    #现在是包含小数
        new_position = self.toBin(self.toDeci(self.position) + self.velocity)   #现在是整数转为二进制list,位数长度满足
        self.position = [new_position[x] for x in range(len(new_position))]
        new_value = getFitness(self.position,self.df) #计算新点的fitness

        if(new_value > self.Pbest_value): #取代局部最优
            self.Pbest_position = [self.position[x] for x in range(len(self.position))]
            self.Pbest_value = new_value
        if(new_value > Gbest_value): #取代整体最优
            Gbest_position = [self.position[x] for x in range(len(self.position))]
            Gbest_value = new_value
        # print(str('%.2f' % self.Pbest_value) + ", ", end = '')
        return Gbest_position, Gbest_value #返回全局最好

    # 二进制list转为十进制int  decimalism
    def toDeci(self,list):
        d = ''
        for x in range(len(list)):
            d += str(list[x])
        b = int(d, 2)
        return b

    # 十进制转二进制list
    def toBin(self,dec):
        if(dec<0):  #值小于零问题
            dec = 0
        t = bin(int(dec)) #先转化为int，再转二进制
        b = [int(t[x]) for x in range(2, len(t))] #二进制消除前面两个 0b，再导出list

        if(len(b)<len(self.individual)): #list没达到原始基因序列位数，补0
            zero = [0 for x in range(len(self.individual)-len(b))]
            return zero + b
        elif(len(b)>len(individual)): #list大于原始基因长度，取最大都是1
            return self.individual
        else: #长度相同
            return b


def psoAlgorithm(individual, df, pop, iter):
    """"
    randomly generate pop number particles
    keep the particle with highest fitness as global best
    every other particle keep pointing to the global best, and save the partial best in its track
    to calculate each velocity by f(past velocity, current position, global best position, partial best position)
    the new position of each particle is the sum of current position and velocity
    save the Global best and its position(gen) in every iteration, print result
    end with the iteration condition, return the best one
    """
    #random generate particles swarm intially,
    population = []
    Gbest_position = individual
    Gbest_value = 0
    individuals = []
    MAX = 0
    print("iter".ljust(10) + "Global best".ljust(20) + "best position in this iteration".ljust(20))

    for i in range(pop):
        population.append(particle(individual,df))
        if(population[i].Pbest_value > Gbest_value):
            Gbest_position = [population[i].position[j] for j in range(len(population[i].position))]
            Gbest_value = population[i].Pbest_value
    individuals.append(Gbest_position)
    MAX = Gbest_value

    for i in range(iter):

        for j in range(pop):    # 全部的population刷一遍
            Gbest_position, Gbest_value = population[j].move(Gbest_position, Gbest_value)

        if(Gbest_value > MAX):
            individuals = []
            individuals.append(Gbest_position)
            MAX = Gbest_value
        elif(MAX == Gbest_value):
            for x in range(len(individuals)):
                if(individuals[x] == Gbest_position):
                    break
                elif(individuals[x] != Gbest_position and x == len(individuals)-1):
                    individuals.append(Gbest_position)

        print(str(i+1).ljust(10) + str('%.6f' % Gbest_value).ljust(20) + str(Gbest_position).ljust(20))

    return MAX, individuals


if __name__ == '__main__':
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=Warning)
    # dataframePath = 'datasets/adult.csv'

    dataframePath = 'sample/automobile_data.csv'
    # dataframePath = 'sample/adult_sample.csv'
    # dataframePath = 'sample/bank_full_sample.csv'
    pop = 50      # population  how?
    iter = 100      # iteration
    df = pd.read_csv(dataframePath, sep=',')

    # df = df.sample(frac=1).reset_index(drop=True) #打乱instance

    #converge nom to num and store
    le = LabelEncoder()
    cols = [df.columns[x] for x in range(len(df.columns))]
    for i in range(len(df.columns)):
        if(df[cols[i]].dtypes == 'object'): #最后一个是否也要labeling？  or i == (len(df.columns)-1)
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
    print("Population: " + str(pop).ljust(10) + "Iteration: " + str(iter))

    start = clock()
    bestAccuracy, individuals = psoAlgorithm(individual, df, pop, iter) #返回最好的 fitness 跟 同这个精确度的 list[所有元素]
    end = clock()

    print("\nRunning time: " + str('%.4f' % (end - start)) + " s".ljust(10), end='')
    if (df.iloc[:, -1].values.dtype == "float64"):
        print("Best Fitness: " + str('%.6f' % bestAccuracy).ljust(20) + "(Error: " + str(10**3/bestAccuracy) + ")")
    else:
        print("Best Accuracy: " + str('%.6f' % bestAccuracy).ljust(20))

    for i in range(len(individuals)):
        print("Individual[" + str(i) + "]: ".ljust(10) + "    " + str(individuals[i]) + "Num of Features: ".rjust(30) + str(individuals[i].count(1)))
        I = individuals[i] + [0]
        FS = [df.columns[x] for x in range(len(I)) if I[x] == 1]
        print("Feature Subset[" + str(i) + "]: ".ljust(10) + str(FS))


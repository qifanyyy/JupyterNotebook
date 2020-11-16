import math
import graph
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import glob
import os

class visualization:
    def __init__(self, filename):
        plt.figure(figsize=(15,8))
        self.cities = None #self.cities_visualization(filename)
        self.ax     = None 
        self.cities_visualization(filename)

    def cities_visualization(self, filename):
        file        = open(filename, "r")
        content     = [ [int(chr) for chr in line.strip("\n").split(" ") if chr != ""] 
                        for line in file.readlines()]
        content     = np.array(content)
        self.cities = content
        self.ax     = sns.scatterplot(content[:,0],content[:,1], s= 700, alpha=0.6, legend=False,hue=content[:,0]*content[:,1])
        for i,point in enumerate(content):
            self.ax.text(point[0], point[1], i, horizontalalignment='center', size='medium', color='black')
        self.ax.set_xticks(range(np.min(content[:,0])-20,np.max(content[:,0])+20,20))
        self.ax.set_yticks(range(np.min(content[:,1])-20,np.max(content[:,1])+20,20))
        self.ax.grid(True,alpha=0.5)

    def offset_points(self, p,q, offset):
        m = (p[1]-q[1]) / (p[0] - q[0])
        x1 = p[0] #+ offset*m*0.005
        #x1 = p[0]
        y1 = m*(x1-p[0])+p[1]
        return [x1,y1]


    def plot_solution(self, solution, n):
        
        sol = [self.cities[i] for i in solution]
        for i in range(n-1):
            # adding a bit of shift to start and end positions            
            start_pos = self.offset_points(sol[i],sol[i+1], 6) 
            end_pos   = self.offset_points(sol[i+1],sol[i], 6)
            self.ax.annotate("",
                    xy=start_pos, 
                    xytext=end_pos, 
                    arrowprops=dict(arrowstyle="<|-",shrinkA=10,shrinkB=10,
                                    connectionstyle="arc3,rad=0."))

class Generating_Euclidean_graphs():
    def __init__(self):
        self.sizeN = [10,25,50,75,100]
        self.create()
    def random_graphs(self, n, mi, ma, name):
        points = np.random.randint(mi,ma,size=(n,2))
        #print(points)
        np.savetxt(name+".txt", points, fmt="%d")
        print(name)

    
    def create(self):
        for i in self.sizeN:
            for j in range(1,6):
                self.random_graphs(i, 0, (10*j)**2,("Graphs\\"+"random_n_"+str(i)+"_r"+str((10*j)**2)))

def RandomSolver():
    # os.walk("Graph//")
    mylist = [f for f in glob.glob("Graphs\\*")]
    total = [[]]*5
    print(total)
    for filename in mylist:
        g = graph.Graph(-1, filename)
        methods =  [(g.swapHeuristic,"Swap Heuristic"),
                    (g.TwoOptHeuristic,"TwoOptHueristic"),
                    (g.Greedy,"Greedy"),
                    (g.twoApproximation,"Minimum Spanning Tree"),
                    (g.christofide,"Christofide")]

        for i, (method, name) in enumerate(methods):
            method()
            # print(name,g.tourValue())
            total[i].append(g.tourValue())
        
        print("--"*50)
    np.savetxt("answers.csv",np.array(total).T,fmt="%d",delimiter =",")

if __name__ == '__main__':
    # Variables to set.
    filename   = "cities50"
    n          = -1
    RandomSolver()
    #Processing.
    #Generating_Euclidean_graphs()
    
    # g = graph.Graph(n, filename)
    # v = visualization(filename)
    # plt.title("Cities 50")
    # plt.show()
    # methods =  [(g.swapHeuristic,"Swap Heuristic"),
    #             (g.TwoOptHeuristic,"TwoOptHueristic"),
    #             (g.Greedy,"Greedy"),
    #             (g.twoApproximation,"Minimum Spanning Tree"),
    #             (g.christofide,"Christofide")]

    # for method, name in methods:
    #     v = visualization(filename)
    #     method()
    #     v.plot_solution(g.perm, g.n)
    #     v.ax.set_title(name)
    #     print(name,g.tourValue())
    #     plt.savefig(name+".png")

    
from tracta_ml.evolve import model_tuner
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pickle

class ModelTuner:

    def __init__(self, model, param_dict, cv, score):
        self.mod = model
        self.param_dict = param_dict
        self.cv = cv
        self.score = score


    def fit(self, X, y, verbose=False, max_back=0.5, tot_gen=2000, known_best=None):
        '''optimizing hyper-params and features for the given model'''

        print("Starting optimization")
        t1 = datetime.now()
        self.best_sol, self.monitor = model_tuner(X, y, self.mod, self.param_dict,\
                                                  self.cv, self.score, verbose,\
                                                  look_back=max_back*tot_gen, n_gen=tot_gen,\
                                                  known_best=known_best)
        t2 = datetime.now()
        print("Time taken : ", t2 - t1)

        print("\n","Best Model Stats: \n",self.best_sol)

        up_param_dict = dict(zip(self.param_dict.keys(), self.best_sol.hpGene))
        self.mod.set_params(**up_param_dict)
        X_trans = X.loc[:,(self.best_sol.featGene==1)]

        pickle.dump(list(X_trans.columns.values), open('best_features.pkl', 'wb'))
        pickle.dump(self.mod, open('best_model.pkl', 'wb'))
        pickle.dump(self.best_sol, open('best_solution.pkl', 'wb'))
        print("\n","Best model & feature set saved to disk")

        return self


    def load_file(self, file):
        return pickle.load(open(file,'rb'))


    def get_best_model(self):
        return self.mod


    def transform(self,X):
        return X.loc[:,(self.best_sol.featGene==1)]


    def get_features(self):
        return self.best_sol.featGene == 1


    def plot_monitor(self,metric):
        fig, ax = plt.subplots()
        plt.plot(self.monitor[metric])
        plt.title(str(metric)+str(" vs Iterations"))
        plt.xlabel("Iterations")
        plt.ylabel(metric)
        ax.set_xlim(xmin=0)
        tick_space = round(len(self.monitor[metric]) / 15)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_space))
        plt.xticks(rotation=45)
        plt.show()
        return














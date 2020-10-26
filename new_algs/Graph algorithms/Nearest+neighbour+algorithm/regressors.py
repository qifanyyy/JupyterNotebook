from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
import sys
sys.path.append("/Users/david/github_datascience/projects/fake_data/")
from fake_data import *
from sklearn import ensemble
from sklearn.isotonic import IsotonicRegression
from sklearn.neural_network import MLPRegressor
import time
import numpy as np
import matplotlib.pylab as plt
from sklearn.tree import export_graphviz
import pydot
from sklearn import linear_model
import prediction_functions.model_selection as ms
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel


class rfr:

    def __init__(self):
        '''
        specify the main timeseries (ymain)
        covariate timeseries (covariates)
        and names of each covariate(feature_list)
        '''
        self.feature_list = None
        self.covariates = None
        self.ymain = None


    def split_train_test(self):
        fnew, labels = self.covariates, self.ymain
        #!########## Split the data into training and testing sets for cross validation #########
        train_features, test_features, train_labels, test_labels = \
        train_test_split(fnew, labels, test_size = 0.25,random_state = 42)
        print('Training Features Shape:', train_features.shape)
        print('Training Labels Shape:', train_labels.shape)
        print('Testing Features Shape:', test_features.shape)
        print('Testing Labels Shape:', test_labels.shape)
        self.train_features = train_features
        self.test_features = test_features
        self.train_labels = train_labels
        self.test_labels = test_labels

    def backup_inputs(self):
        self.backup_train_features = np.array(self.train_features)
        self.backup_test_features = np.array(self.test_features)
        self.backup_train_labels = np.array(self.train_labels)
        self.backup_test_labels = np.array(self.test_labels)
        self.backup_feature_list = list(self.feature_list)
        self.backup_ymain = np.array(self.ymain)

    def restore_inputs(self):
        self.train_features = np.array(self.backup_train_features)
        self.test_features = np.array(self.backup_test_features)
        self.train_labels = np.array(self.backup_train_labels)
        self.test_labels = np.array(self.backup_test_labels)
        self.feature_list = list(self.backup_feature_list)
        self.ymain = np.array(self.backup_ymain)



    def initialize_rf(self):
        # Instantiate model
        self.rf = RandomForestRegressor(n_estimators= 10, random_state=42)

    def initialize_etr(self):
        # Instantiate model
        self.rf = ExtraTreesRegressor(n_estimators= 10, random_state=42)

    def initialize_gbr(self):
        #gradient boosting regressor
        params = {'n_estimators': 500, 'max_depth': 4, 'min_samples_split': 2,
                  'learning_rate': 0.01, 'loss': 'ls'}
        self.rf = ensemble.GradientBoostingRegressor(**params)

    def initialize_mlp(self):
        #multilayer perceptron regressor
        rf = MLPRegressor(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5), random_state=1)
        MLPRegressor(activation='relu', alpha=1e-05, batch_size='auto',
                     beta_1=0.9, beta_2=0.999, early_stopping=False,
                     epsilon=1e-08, hidden_layer_sizes=(5, 2), learning_rate='constant',
                     learning_rate_init=0.001, max_iter=200, momentum=0.9,
                     nesterovs_momentum=True, power_t=0.5, random_state=1, shuffle=True,
                     solver='lbfgs', tol=0.0001, validation_fraction=0.1, verbose=False,
                     warm_start=False)
        self.rf = rf

    def initialize_glm(self):
        #glm not (custom version)
        self.rf = linear_model.LinearRegression()


    def initialize_gpr(self):
        kernel = DotProduct() + WhiteKernel()
        self.rf = GaussianProcessRegressor(kernel = kernel,random_state=0)


    def fit(self,x,y):
        #fit with choice of regressor
        self.rf.fit(y,x)



    def component_selection_trainmodel(self,rf):
        '''
        use aic to select optimum number of components
        order is selected using a greedy algorithm
        :return:
        :param rf:
        :return:
        '''
        labels,covariates = self.ymain,self.covariates
        npoints,ncovariates = np.shape(self.covariates)
        chosen = np.zeros((npoints,0))
        not_chosen = [self.covariates[:,i] for i in range(ncovariates)]
        new_component = np.zeros((npoints,1))
        covariate_now = np.zeros((npoints, 1))
        aic_save = []
        feature_list_notchosen = list(self.feature_list)
        feature_list_chosen = []
        for i in range(ncovariates):
            aic = []
            for i2 in range(len(not_chosen)):
                covariate_now[:,0] = not_chosen[i2]
                now = np.hstack((chosen, covariate_now))
                rf.fit(now,labels)
                aic.append(self.component_selection_predictmodel(rf,now))
            idx_chosen = np.argmin(aic)
            aic_save.append(aic[idx_chosen])
            feature_list_chosen.append(feature_list_notchosen.pop(idx_chosen))
            new_component[:,0] = not_chosen.pop(idx_chosen)
            chosen = np.hstack((chosen,new_component))

        '''
        output the results of component selection as well as the matrix
        of final chosen components
        '''
        idmin = np.argmin(aic_save)
        component_used = np.arange(idmin+1)
        summary = {'name':[feature_list_chosen[c] for c in component_used],
                    'aic':[aic_save[c] for c in component_used],
                   'component matrix':chosen[:,component_used]}

        print(pd.DataFrame( {'name':feature_list_chosen,
                    'aic':aic_save}))
        return(summary)







    def component_selection_predictmodel(self,rf,chosen_features):
        '''
        use aic to select optimum number of components
        order is selected using a greedy algorithm
        :return:
        '''
        predictions = rf.predict(chosen_features)
        k = np.shape(chosen_features)[1]
        aic = ms.aic(self.ymain,predictions,k)
        return(aic)



    def cross_validation_check(self,test_features):
        #use cross validation to assess the model accuracy
        t0 = time.time()
        predictions = self.rf.predict(test_features)
        t1 = time.time()
        # Make predictions and determine the error
        errors = abs(predictions - self.test_labels)
        # Calculate mean absolute percentage error (MAPE)
        mape = 100 * (errors / abs(self.test_labels))
        # Display the performance metrics
        print('Mean Absolute Error:', round(np.mean(errors), 2), 'dollars')
        accuracy = 100 - np.mean(mape)
        print('Accuracy regressor:', np.round(accuracy, 2), '%.')
        print('Mean mape',np.round(np.mean(mape), 2), '%.')
        self.predictions = predictions
        self.errors = errors
        self.mape = mape
        self.accuracy = accuracy


    def plot_CV_results(self):
        #make a plot of the predicted vs actual values
        test_labels = self.test_labels
        predictions = self.predictions
        errors = self.errors
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.scatter(test_labels,predictions,c='r',s=2,label = 'data points')
        idsort = np.argsort(test_labels)
        pr = predictions[idsort]
        tl = test_labels[idsort]
        er = errors[idsort]
        #include running rms
        nres = 100
        pmin, pmax = np.min(pr),np.max(pr)
        pres = np.linspace(pmin,pmax,nres)
        lmin, lmax = np.min(tl),np.max(tl)
        lres = np.linspace(lmin,lmax,nres)
        eres = np.interp(pres,tl,er)
        ares = np.interp(pres,pr,tl)
        xorth = np.mean(tl)
        fit_coef,cov = np.polyfit(tl,pr,deg=1,w=1./er,cov=True)
        print(np.shape(cov))
        sig_coef = np.sqrt(np.diag(cov))
        xplot = lres
        yplot = fit_coef[1]*(xplot - xorth) + fit_coef[0]
        sigplot = np.sqrt((xplot-xorth)**2*sig_coef[1]**2 + sig_coef[0]**2)
        ax1.plot(xplot,yplot,label='least-squares fit')
        ax1.fill_between(xplot,yplot-sigplot,yplot+sigplot,alpha=0.4,label=None)
        ax1.set_xlabel('Actual Sale Price ($)')
        ax1.set_ylabel('Predicted Sale Price ($)')
        xlim = list(ax1.get_xlim())
        ylim = list(ax1.get_ylim())
        ax1.set_title('Predicted vs Actual Sale Price')
        ax1.plot(xlim,ylim,ls='--',color='k',label='one-to-one line')
        plt.legend()
        plt.savefig('fig_actual_vs_predict.pdf')
        plt.clf()

    def plot_single_tree(self):
        #Visualizing a Single Decision Tree
        # Import tools needed for visualization
        from sklearn.tree import export_graphviz
        import pydot

        # Pull out one tree from the forest
        tree = self.rf.estimators_[5]

        # Export the image to a dot file
        export_graphviz(tree, out_file = 'tree.dot', feature_names = self.feature_list, rounded = True, precision = 1)

        # Use dot file to create a graph
        (graph, ) = pydot.graph_from_dot_file('tree.dot')

        # Write graph to a png file
        graph.write_png('tree.png')

        print('The depth of this tree is:', tree.tree_.max_depth)




        #Smaller tree for visualization.
        # Limit depth of tree to 2 levels
        rf_small = RandomForestRegressor(n_estimators=10, max_depth = 3, random_state=42)
        rf_small.fit(train_features, train_labels)

        # Extract the small tree
        tree_small = rf_small.estimators_[5]

        # Save the tree as a png image
        export_graphviz(tree_small, out_file = 'small_tree.dot', feature_names = feature_list, rounded = True, precision = 1)

        (graph, ) = pydot.graph_from_dot_file('small_tree.dot')

        graph.write_png('small_tree_'+np.str(i)+'_'+np.str(iv)+'.png');






    def get_importances(self):
        #!!!!!!!!!! VARIABLE IMPORTANCES !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Get numerical feature importances
        self.importances = list(self.rf.feature_importances_)

        # List of tuples with variable and importance
        feature_importances = [(feature, round(importance, 2)) for feature, importance in
                               zip(self.feature_list, self.importances)]

        # Sort the feature importances by most important first
        self.feature_importances = sorted(self.feature_importances, key = lambda x: x[1], reverse = True)

        # Print out the feature and importances
        #[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances]



    def two_features_only(self):
        #!!!!!!!!!! MODEL WITH TWO MOST IMPORTANT FEATURES !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # New random forest with only the two most important variables
        rf_most_important = RandomForestRegressor(n_estimators= 1000, random_state=42)

        # Extract the two most important features
        important_indices = [self.feature_list.index(self.feature_importances[0][0]),
                             self.feature_list.index(self.feature_importances[1][0])]
        train_important = self.train_features[:, important_indices]
        test_important = self.test_features[:, important_indices]

        # Train the random forest
        rf_most_important.fit(train_important, self.train_labels)

        # Make predictions and determine the error
        predictions = rf_most_important.predict(test_important)
        errors = abs(predictions - self.test_labels)
        # Calculate mean absolute percentage error (MAPE)
        mape = 100 * (errors / self.test_labels)
        # Display the performance metrics
        print('Mean Absolute Error:', round(np.mean(errors), 2), 'dollars')
        accuracy = 100 - mape
        print('Accuracy random forrest 2 important:', np.round(accuracy, 2), '%.')





    def visualisations(self):
    #!!!!!!!!!! vizualisations of 2-component fit!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        #variable importances
        # list of x locations for plotting
        importances = np.array(self.importances)
        idsort = np.argsort(importances)[::-1]
        nplot = 10
        imp = importances[idsort][:nplot]
        fl = [self.feature_list[ids] for ids in idsort][:nplot]

        x_values = list(range(len(imp)))

        # Make a bar chart
        plt.bar(x_values, imp, orientation = 'vertical',color='r')

        # Tick labels for x axis
        plt.xticks(x_values, fl, rotation='vertical')

        # Axis labels and title
        plt.ylabel('Importance'); plt.xlabel('Variable'); plt.title('Variable Importances')


        plt.tight_layout()
        plt.savefig('importances_'+np.str(i)+'_'+np.str(iv)+'.png')



    def test_method(self):
        '''
        suggest a regressor method and perform greedy search to find
        the best combination of components
        :param rf:
        :return:
        '''
        self.backup_inputs()
        component_selection = self.component_selection_trainmodel(self.rf)
        idx_use = np.array([i for i in range(len(self.feature_list)) if
                   self.feature_list[i] in component_selection['name']],dtype=int)
        print(component_selection['name'])
        print(self.feature_list)
        print(idx_use)
        new_components = self.covariates[:,idx_use]
        new_feature_list = [self.feature_list[i] for i in idx_use]
        new_train = self.train_features[:,idx_use]
        new_test = self.test_features[:,idx_use]
        # set required parameters
        self.feature_list = new_feature_list
        self.covariates = new_components
        self.split_train_test()
        self.rf.fit(new_train,self.train_labels)
        self.cross_validation_check(new_test)
        self.method_results['predictions'].append(list(self.predictions))
        self.method_results['true'].append(self.ymain)
        self.method_results['mape'].append(self.mape)
        self.method_results['rms'].append(np.std(self.predictions - self.test_labels))
        self.restore_inputs()





    def test_all_methods(self):
        '''
        test all the regressor methods above to check which minimizes mape
        :return:
        '''
        self.method_results = {'predictions':[],
                          'true':[],
                          'mape':[],
                          'rms':[],
                          'method':[]}

        self.initialize_rf()
        self.test_method()
        self.mape_rfr = self.mape
        self.method_results['method'].append('rfr')
        print('rfr\n')

        self.initialize_etr()
        self.test_method()
        self.mape_rfr = self.mape
        self.method_results['method'].append('etr')
        print('etr\n')

        self.initialize_gbr()
        self.test_method()
        self.mape_rfr = self.mape
        self.method_results['method'].append('GBR')
        print('GBR\n')

        self.initialize_mlp()
        self.test_method()
        self.mape_rfr = self.mape
        self.method_results['method'].append('MLP')
        print('MLP\n')

        self.initialize_glm()
        self.test_method()
        self.mape_rfr = self.mape
        self.method_results['method'].append('GLM')
        print('GLM\n')

        self.initialize_gpr()
        self.test_method()
        self.mape_gpr = self.mape
        self.method_results['method'].append('GPR')
        print('GPR\n')

if __name__ == '__main__':
    '''
    test rfr on some data
    '''
    regressors = ['rf','mpl','gbr']

    #generate fake data
    a = fake_data()
    a.covariates = 100
    a.npoints = 2000
    a.initialise()
    a.add_covariates(importances=[1., 0.0, 0.3, 0.0], iseed=343435)

    #test random forrest regressor
    x = rfr()
    #set required parameters
    x.feature_list = ['component '+np.str(i+1) for i in range(a.covariates)]
    x.covariates = a.extra_covariates
    x.ymain = a.driver

    #perform fit and make plots
    x.split_train_test()

    x.test_all_methods()
    #x.plot_CV_results()
    #x.plot_single_tree()
    #x.get_importances()
    #x.two_features_only()
    #x.visualisations()
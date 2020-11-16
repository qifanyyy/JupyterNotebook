from TPC_Config import *
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm
from scipy import odr

import optunity
import optunity.metrics
import os
from time import time, strftime, gmtime
from sklearn import preprocessing
import logging



def dead_single_opt(pmts,pmts_check, events):
    N = int(len(events)/5)
    Events = [[event[j] for event in events if event[pmts[-1]] > 50][0:N] for j in pmts]
    logging.info('Number of Events Trained: '+str(len(Events[0])))
    logging.info('PMT Used to Train: '+str(pmts[-1]))
    data_train = list(zip(*Events[0:-1]))
    target_train = Events[-1]

    print('Normalizing Data')
    scaler = preprocessing.StandardScaler().fit(data_train)
    data_train = scaler.transform(data_train)

    # we explicitly generate the outer_cv decorator so we can use it twice
    outer_cv = optunity.cross_validated(x=data_train, y=target_train, num_folds=2)
    mse_old = 10e7
    def compute_mse_rbf_tuned(x_train, y_train, x_test, y_test):
        """Computes MSE of an SVR with RBF kernel and optimized hyperparameters."""
        global optimal_parameters, clf
        # define objective function for tuning
        @optunity.cross_validated(x=x_train, y=y_train, num_iter=2, num_folds=2)
        def tune_cv(x_train, y_train, x_test, y_test, C, gamma):
            # sample_weights = my_scaling_odr(y_train)
            # sample_weights = [i / max(Events[-1]) for i in Events[-1]]

            model = svm.SVR(C=C, gamma=gamma).fit(x_train, y_train)#, sample_weight=sample_weights
            predictions = model.predict(x_test)
            return optunity.metrics.mse(y_test, predictions)

        # optimize parameters
        optimal_pars, _, _ = optunity.minimize(tune_cv, 200, C=[1, 4000], gamma=[0, 10], pmap=optunity.pmap)
        logging.info("Optimal hyperparameters: " + str(optimal_pars))
        # sample_weights = my_scaling_odr(y_train)

        tuned_model = svm.SVR(**optimal_pars).fit(x_train, y_train)
        predictions = tuned_model.predict(x_test)
        mse = optunity.metrics.mse(y_test, predictions)
        logging.info('mse: ' + str(mse))
        if mse < mse_old:
            optimal_parameters = optimal_pars
            clf = tuned_model
        return mse


    # wrap with outer cross-validation
    compute_mse_rbf_tuned = outer_cv(compute_mse_rbf_tuned)
    print('Beginning Cross-Validated Optimization of HyperParameters')
    compute_mse_rbf_tuned()
    Events_check = [[event[j] for event in events if event[pmts_check[-1]] > 50] for j in pmts_check]
    logging.info('Number of Events Trained: '+str(len(Events_check[0])))
    logging.info('PMT Used to Train Final Function: '+str(pmts_check[-1]))
    X_Span = list(zip(*Events_check[:-1]))
    X_Span = scaler.transform(X_Span)
    print('Predicting Data Now')
    pmt_estimate = clf.predict(X_Span)

    # print('Plotting Guessed Data Now')

    diff = [(pmt_estimate[i] - Events_check[-1][i]) / (Events_check[-1][i] + 1) for i in range(0, len(Events_check[-1]))]
    # print(np.mean(diff), np.std(diff))
    # print(np.mean(np.abs(diff)), np.std(np.abs(diff)))
    logging.critical('Final Average Absolute Relative Error: ' + str(round(np.mean(np.abs(diff)),3))
                     + '+-' +str(round(np.std(np.abs(diff)), 3)))

    # plt.figure()
    # plt.plot(Events_check[-1], pmt_estimate, '*')
    # plt.plot([0, max(Events_check[-1])], [0, max(Events_check[-1])], 'r', label='Error = 0%')
    # plt.xlabel('Actual PMT Value')
    # plt.ylabel('Estimated PMT Value')
    # plt.show()

    return clf, scaler


def exponential_func(params, x):
    return params[0]*np.exp(-1*params[1]*(x))

def my_scaling_odr(data):
    y, x = np.histogram(data, bins=int(np.sqrt(len(data))*3), range=[0, 400])
    x = [(x[i]+x[i+1])/2 for i in range(0, len(x)-1)]
    scaling_model = odr.Model(exponential_func)
    scaling_data = odr.RealData(x, y)
    scaling_odr = odr.ODR(scaling_data, scaling_model, beta0=[len(data), 20])
    output = scaling_odr.run()
    beta= output.beta
    red_chi = output.res_var
    sample_weights = [1/np.sqrt(exponential_func(beta, i)) for i in data]

    return sample_weights, red_chi


def fix_dead_pmts(dead_pmts, comp_pmts,comp_pmts_check, event_dataframe):
    start = time()
    logging.info('Operation Type: Preprocessing')
    events = event_dataframe['s2_area_array'].tolist()
    for i in range(0,len(dead_pmts)):
        logging.critical('Interpolating PMT #'+str(dead_pmts[i][-1]))
        dead_fit, scaler = dead_single_opt(comp_pmts[i], comp_pmts_check[i], events)
        logging.info('Finished Optimization and Fitting: '+str((time()-start)/60)+' min')
        Events = [[event[j] for event in events] for j in dead_pmts[i]]
        PMT_features = list(zip(*Events[:-1]))
        PMT_features = scaler.transform(PMT_features)
        pmt_estimate = dead_fit.predict(PMT_features)
        events = np.array(events)
        events[:, dead_pmts[i][-1]] = pmt_estimate
        events = events.tolist()
    return events


import numpy as np
from numpy import linalg as la
from matrixmath import randn

from ltimultgen import gen_system_mult
from policygradient import PolicyGradientOptions, run_policy_gradient
from ltimult import dlyap_obj

from matplotlib import pyplot as plt

from time import time,sleep

import os
from utility import create_directory

from pickle_io import pickle_import,pickle_export


def set_initial_gains(SS,K0_method):
    # Initial gains
    if K0_method=='random':
        K0 = randn(*SS.Kare.shape)
        SS.setK(K0)
        while not SS.c < np.inf:
            K0 = randn(*SS.Kare.shape) # May take forever
            SS.setK(K0)
    elif K0_method=='random_olmss':
        K0 = randn(*SS.Kare.shape)
        SS.setK(K0)
        while not SS.c < np.inf:
            K0 = 0.9*K0 # Only guaranteed to work if sys open loop mean-square stable
            SS.setK(K0)
    elif K0_method=='are':
        K0 = SS.Kare
        print('Initializing at the ARE solution')
    elif K0_method=='are_perturbed':
        perturb_scale = 10.0/SS.n  # scale with 1/n as rough heuristic
        safety_scale = 10.0
        Kp = randn(SS.Kare.shape[0],SS.Kare.shape[1])
        K0 = SS.Kare + perturb_scale*Kp
        SS.setK(K0)
        while not SS.c < safety_scale*SS.ccare:
            perturb_scale *= 0.2
            K0 = SS.Kare + perturb_scale*Kp
            SS.setK(K0)
        while not SS.c > safety_scale*SS.ccare:
            perturb_scale *= 1.01
            K0 = SS.Kare + perturb_scale*Kp
            SS.setK(K0)
        perturb_scale /= 1.01
        K0 = SS.Kare + perturb_scale*Kp
        SS.setK(K0)
    elif K0_method=='zero':
        K0 = np.zeros([SS.m,SS.n])
        SS.setK(K0)
        P = dlyap_obj(SS,algo='iterative',show_warn=False)
        if P is not None:
            print('Initializing with zero gain solution')
        else:
            print('System not open-loop mean-square stable, use a different initial gain setting')
    SS.setK(K0)
    return K0


def policy_gradient_setup(SS,eta,step_direction,max_iters):
    # Gradient descent options

    # Convergence threshold
    epsilon = (1e-1)*SS.Kare.size # Scale by number of gain entries as rough heuristic

    stepsize_method = 'constant'
    stop_crit = 'fixed'

    PGO = PolicyGradientOptions(epsilon=epsilon,
                                eta=eta,
                                max_iters=max_iters,
                                disp_stride=1,
                                keep_hist=True,
                                opt_method='gradient',
                                keep_opt='last',
                                step_direction=step_direction,
                                stepsize_method=stepsize_method,
                                exact=True,
                                regularizer=None,
                                regweight=0,
                                stop_crit=stop_crit,
                                fbest_repeat_max=0,
                                display_output=True,
                                display_inplace=True,
                                slow=False)
    return PGO



def load_system(timestr):
    # Import
    dirname_in = os.path.join('systems_keepers',timestr)
    filename_only = 'system_init.pickle'
    SS = pickle_import(os.path.join(dirname_in,filename_only))
    #Export
    timestr = str(time()).replace('.','p')
    dirname_out = os.path.join('systems',timestr)
    SS.dirname = dirname_out
    filename_out = os.path.join(dirname_out,filename_only)
    pickle_export(dirname_out, filename_out, SS)
    return SS



def plot_data(all_dict,dirname_in):
    img_dirname_out = os.path.join(dirname_in,'analysis_plots')
    create_directory(img_dirname_out)

    nSS = len(all_dict['gradient']['costnorm'])

    lw = 3
    fs = 14
    markerdict = {'gradient': 'o',
                  'natural_gradient':'v',
                  'gauss_newton':'^'}
    ms = 8
    pmax = 100
    pmin = 0

    quant_list = ['costnorm','gradnorm']
    for quant in quant_list:
        plt.figure(figsize=(4.5,2.5))
        plt.yscale('log')
        xlab = 'Iteration'
        plt.xlabel(xlab,fontsize=fs)

        if quant=='costnorm':
            ylab = 'Normalized cost diff.'
        elif quant=='gradnorm':
            ylab = 'Fro. norm of gradient'
        plt.ylabel(ylab,fontsize=fs)

        for step_direction in all_dict:
            max_iters = all_dict[step_direction][quant][0].size
            quant_all = np.zeros([nSS,max_iters])
            for i in range(nSS):
                quant_all[i] = all_dict[step_direction][quant][i]
            quant_mean = quant_all.mean(axis=0)

            x = np.arange(max_iters)+1
            upr = np.percentile(quant_all,pmax,axis=0)
            lwr = np.percentile(quant_all,pmin,axis=0)
            mid = quant_mean
            plt.fill_between(x,lwr,upr,alpha=0.5)
            plt.plot(x,mid,linewidth=lw,marker=markerdict[step_direction],markersize=ms,markevery=499)
        leg = ['Gradient','Natural gradient','Gauss-Newton']
        plt.legend(leg,loc='lower right')

        plt.show()
        filename_out = 'plot_'+quant+'_vs_iteration_random'
        path_out = os.path.join(img_dirname_out,filename_out)
        plt.savefig(path_out,dpi=300,bbox_inches='tight')

        plt.figure(figsize=(4.5,2.5))
        plt.yscale('log')

        plt.xlabel(xlab,fontsize=fs)
        plt.ylabel(ylab,fontsize=fs)

        for step_direction in all_dict:
            max_iters = all_dict[step_direction][quant][0].size
            quant_all = np.zeros([nSS,max_iters])
            for i in range(nSS):
                quant_all[i] = all_dict[step_direction][quant][i]
            quant_mean = quant_all.mean(axis=0)

            max_iters_partial = 10

            x = np.arange(max_iters_partial)+1
            upr = np.percentile(quant_all,pmax,axis=0)[0:max_iters_partial]
            lwr = np.percentile(quant_all,pmin,axis=0)[0:max_iters_partial]
            mid = quant_mean[0:max_iters_partial]
            plt.fill_between(x,lwr,upr,alpha=0.5)
            plt.plot(x,mid,linewidth=lw,marker=markerdict[step_direction],markersize=ms)
            plt.xticks(ticks=1+np.arange(max_iters_partial))
        leg = ['Gradient','Natural gradient','Gauss-Newton']
        plt.legend(leg,bbox_to_anchor=[0.5, 0.55],loc='center left')

        plt.show()
        filename_out = 'plot_'+quant+'_vs_iteration_random_zoom'
        path_out = os.path.join(img_dirname_out,filename_out)
        plt.savefig(path_out,dpi=300,bbox_inches='tight')


def routine_gen():
    folderstr = 'systems'
    timestr = str(time()).replace('.','p')
    dirname_in = os.path.join(folderstr,timestr)
    create_directory(dirname_in)

    nSS = 20 # Number of independent runs/systems

    all_dict = {'gradient': {'costnorm':[],'gradnorm':[]},
                'natural_gradient':{'costnorm':[],'gradnorm':[]},
                'gauss_newton':{'costnorm':[],'gradnorm':[]}}

    for i in range(nSS):
        SS = gen_system_mult(n=10,
                             m=10,
                             safety_margin=0.3,
                             noise='olmss_weak',
                             mult_noise_method='random',
                             SStype='random',
                             seed=-1,
                             saveSS=False)

        # Policy gradient setup
        K0_method = 'zero'
        K0 = set_initial_gains(SS,K0_method=K0_method)

        step_direction_dict = {'gradient': {'eta':1e-5,'max_iters':5000},
                               'natural_gradient':{'eta':1e-4,'max_iters':2000},
                               'gauss_newton':{'eta':1/2,'max_iters':10}}

        sleep(1)

        for step_direction in step_direction_dict:
            SS.setK(K0)
            t_start = time()
            eta = step_direction_dict[step_direction]['eta']
            max_iters = step_direction_dict[step_direction]['max_iters']
            PGO = policy_gradient_setup(SS,eta,step_direction,max_iters)
            t_end = time()
            print('Initialization completed after %.3f seconds' % (t_end-t_start))

            SS,histlist = run_policy_gradient(SS,PGO)

            costnorm = (histlist[2]/SS.ccare)-1
            gradnorm = la.norm(histlist[1],ord='fro',axis=(0,1))

            all_dict[step_direction]['costnorm'].append(costnorm)
            all_dict[step_direction]['gradnorm'].append(gradnorm)

    filename_out = 'monte_carlo_all_dict.pickle'
    path_out = os.path.join(dirname_in,filename_out)
    pickle_export(dirname_in,path_out,all_dict)

    plot_data(all_dict,dirname_in)



def routine_load():
    folderstr = 'systems_keepers'
    timestr = '1558543320p7456546_example_random_monte_carlo'
    dirname_in = os.path.join(folderstr,timestr)
    filename_in = os.path.join(dirname_in,'monte_carlo_all_dict.pickle')
    all_dict = pickle_import(filename_in)
    plot_data(all_dict,dirname_in)



###############################################################################
if __name__ == "__main__":
    routine_gen()
#    routine_load()
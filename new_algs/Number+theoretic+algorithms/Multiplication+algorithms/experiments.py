import numpy as np
import numpy.random as npr
import numpy.linalg as la
import matplotlib.pyplot as plt
from time import time
import os

from system_definitions import (random_system,
                                example_system_scalar,
                                example_system_twostate,
                                example_system_twostate_diagonal)
from system_identification import generate_sample_data, collect_rollouts, estimate_model, estimate_model_var_only, ctrb
from plotting import (plot_trajectories,
                      plot_model_estimates,
                      plot_estimation_error,
                      plot_estimation_error_multi)
from pickle_io import pickle_import, pickle_export


def experiment_fixed_rollout(n, m, A, B, SigmaA, SigmaB, nr, ell):
    # Generate sample data
    u_mean_hist, u_covr_hist, u_hist, Anoise_hist, Bnoise_hist = generate_sample_data(n, m, SigmaA, SigmaB, nr, ell)

    # Collect rollout data
    x_hist = collect_rollouts(n, m, A, B, nr, ell, Anoise_hist, Bnoise_hist, u_hist)
    t_hist = np.arange(ell+1)

    # Estimate the model
    Ahat, Bhat, SigmaAhat, SigmaBhat = estimate_model(n, m, A, B, SigmaA, SigmaB, nr, ell, x_hist, u_mean_hist, u_covr_hist)

    # Plotting
    plot_trajectories(nr,ell,t_hist,x_hist)
    plot_model_estimates(A,B,SigmaA,SigmaB,Ahat,Bhat,SigmaAhat,SigmaBhat)

    timestr = str(time()).replace('.','p')
    # dirname_out = os.path.join("experiments",timestr)
    # filename_out = os.path.join(dirname_out,"problem_data.pickle")
    # pickle_export(dirname_out, filename_out, problem_data)
    # filename_out = os.path.join(dirname_out,"experiment_data.npy")
    # np.save(filename_out, experiment_data)
    return timestr, Ahat, Bhat, SigmaAhat, SigmaBhat

def experiment_fixed_rollout_var_only(n, m, A, B, SigmaA, SigmaB, varAi, varBj, Ai, Bj, nr, ell, split=False):
    # Generate sample data
    u_mean_hist, u_covr_hist, u_hist, Anoise_hist, Bnoise_hist = generate_sample_data(n, m, SigmaA, SigmaB, nr, ell)

    # Collect rollout data
    x_hist = collect_rollouts(n, m, A, B, nr, ell, Anoise_hist, Bnoise_hist, u_hist)
    t_hist = np.arange(ell+1)

    # Estimate the model
    Ahat, Bhat, SigmaAhat, SigmaBhat, varAi_hat, varBj_hat = estimate_model_var_only(n, m, A, B, SigmaA, SigmaB, varAi, varBj, Ai, Bj,
                                                                                     nr, ell, x_hist, u_mean_hist, u_covr_hist,
                                                                                     detailed_outputs=True)

    # Plotting
    fig1, ax1 = plot_trajectories(nr, ell, t_hist, x_hist)
    fig2, ax2 = plot_model_estimates(A, B, SigmaA, SigmaB, Ahat, Bhat, SigmaAhat, SigmaBhat, split=split)

    timestr = str(time()).replace('.','p')
    # dirname_out = os.path.join("experiments",timestr)
    # filename_out = os.path.join(dirname_out,"problem_data.pickle")
    # pickle_export(dirname_out, filename_out, problem_data)
    # filename_out = os.path.join(dirname_out,"experiment_data.npy")
    # np.save(filename_out, experiment_data)
    return timestr, Ahat, Bhat, SigmaAhat, SigmaBhat, varAi_hat, varBj_hat, [fig1, fig2], [ax1, ax2]


def experiment_increasing_rollout_length(n,m,A,B,SigmaA,SigmaB,nr,ell):
    from system_identification import groupdot
    # Generate sample data
    u_mean_hist, u_covr_hist, u_hist, Anoise_hist, Bnoise_hist = generate_sample_data(n, m, SigmaA, SigmaB, nr, ell)

    # Collect rollout data
    x_hist = np.zeros([ell + 1, nr, n])
    # Initialize the state
    x_hist[0] = npr.randn(nr, n)
    estimate_stride = 1
    ns = round(ell / estimate_stride)
    t_hist = np.arange(ell + 1)
    s_hist = estimate_stride * np.arange(ns)
    Ahat_error_hist = np.full(ns, np.nan)
    Bhat_error_hist = np.full(ns, np.nan)
    SigmaAhat_error_hist = np.full(ns, np.nan)
    SigmaBhat_error_hist = np.full(ns, np.nan)
    k = 0
    for t in range(ell):
        # Transition the state
        x_hist[t+1] = groupdot(A+Anoise_hist[t],x_hist[t]) + groupdot(B+Bnoise_hist[t],u_hist[t])

        if t % estimate_stride == 0:
            Ahat,Bhat,SigmaAhat,SigmaBhat = estimate_model(n,m,A,B,SigmaA,SigmaB,nr,t,x_hist[0:t+1],u_mean_hist[0:t],u_covr_hist[0:t])
            Ahat_error_hist[k] = la.norm(A-Ahat)/la.norm(A)
            Bhat_error_hist[k] = la.norm(B-Bhat)/la.norm(B)
            SigmaAhat_error_hist[k] = la.norm(SigmaA-SigmaAhat)/la.norm(SigmaA)
            SigmaBhat_error_hist[k] = la.norm(SigmaB-SigmaBhat)/la.norm(SigmaB)
            k += 1

    # Plotting
    plot_trajectories(nr,ell,t_hist,x_hist)
    plot_estimation_error(s_hist, Ahat_error_hist, Bhat_error_hist, SigmaAhat_error_hist, SigmaBhat_error_hist, xlabel_str="Time step")
    plot_model_estimates(A,B,SigmaA,SigmaB,Ahat,Bhat,SigmaAhat,SigmaBhat)
    plt.show()


def experiment_increasing_rollout_count(n,m,A,B,SigmaA,SigmaB,nr,ell,u_mean_var,u_covr_var,ns,s_hist,print_updates=True):
    u_mean_hist,u_covr_hist,u_hist,Anoise_hist,Bnoise_hist = generate_sample_data(n,m,SigmaA,SigmaB,nr,ell,u_mean_var,u_covr_var)

    # Collect rollout data
    x_hist = collect_rollouts(n,m,A,B,nr,ell,Anoise_hist,Bnoise_hist,u_hist,print_updates=print_updates)
    t_hist = np.arange(ell+1)

    # Estimate the model for increasing numbers of rollouts
    Ahat_error_hist = np.full(ns,np.nan)
    Bhat_error_hist = np.full(ns,np.nan)
    SigmaAhat_error_hist = np.full(ns,np.nan)
    SigmaBhat_error_hist = np.full(ns,np.nan)
    k = 0
    if print_updates:
        header_str = "# of rollouts |   A error   |   B error   | SigmaA error | SigmaB error"
        print(header_str)
    for r in np.arange(1,nr+1):
        if r == s_hist[k]:
            Ahat,Bhat,SigmaAhat,SigmaBhat = estimate_model(n,m,A,B,SigmaA,SigmaB,r,ell,x_hist[:,0:r],u_mean_hist,u_covr_hist)
            Ahat_error_hist[k] = la.norm(A-Ahat)/la.norm(A)
            Bhat_error_hist[k] = la.norm(B-Bhat)/la.norm(B)
            SigmaAhat_error_hist[k] = la.norm(SigmaA-SigmaAhat)/la.norm(SigmaA)
            SigmaBhat_error_hist[k] = la.norm(SigmaB-SigmaBhat)/la.norm(SigmaB)
            if print_updates:
                update_str = "%13d    %.3e     %.3e      %.3e      %.3e" % (r,Ahat_error_hist[k],Bhat_error_hist[k],SigmaAhat_error_hist[k],SigmaBhat_error_hist[k])
                print(update_str)
            k += 1

    if print_updates:
        from system_identification import prettyprint
        print("FINAL ESTIMATES")
        prettyprint(Ahat, "Ahat")
        prettyprint(A, "A   ")
        prettyprint(Bhat, "Bhat")
        prettyprint(B, "B   ")
        prettyprint(SigmaAhat, "SigmaAhat")
        prettyprint(SigmaA, "SigmaA   ")
        prettyprint(SigmaBhat, "SigmaBhat")
        prettyprint(SigmaB, "SigmaB   ")

    return np.vstack([Ahat_error_hist, Bhat_error_hist, SigmaAhat_error_hist, SigmaBhat_error_hist])


def multi_experiment_increasing_rollout_count(n,m,A,B,SigmaA,SigmaB,ne,ns,s_hist,nr,ell,u_mean_var,u_covr_var,print_updates=False):
    experiment_data = np.zeros([4,ns,ne])
    for i in range(ne):
        experiment_data[:,:,i] = experiment_increasing_rollout_count(n,m,A,B,SigmaA,SigmaB,nr,ell,u_mean_var,u_covr_var,ns,s_hist,print_updates=print_updates)
        print("Experiment %d / %d completed" % (i+1,ne))
    problem_data = {'n': n,
                    'm': m,
                    'A': A,
                    'B': B,
                    'SigmaA': SigmaA,
                    'SigmaB': SigmaB,
                    'ne': ne,
                    'ns': ns,
                    's_hist': s_hist,
                    'nr': nr,
                    'ell': ell,
                    'u_mean_var': u_mean_var,
                    'u_covr_var': u_covr_var}
    timestr = str(time()).replace('.','p')
    dirname_out = os.path.join("experiments",timestr)
    filename_out = os.path.join(dirname_out,"problem_data.pickle")
    pickle_export(dirname_out, filename_out, problem_data)
    filename_out = os.path.join(dirname_out,"experiment_data.npy")
    np.save(filename_out, experiment_data)
    return timestr


def parameter_study(variable_parameter,variable_parameter_list,nominal_parameters):
    # Scalar experiment
    seed = 1
    npr.seed(seed)

    # Number of rollouts
    nr = int(1e4)

    # Rollout length
    ell = 4

    # Model estimation points
    estimation_points = 'log'
    ns = 100
    if estimation_points == 'linear':
        s_hist = np.round(np.linspace(0, nr, ns + 1)).astype(int)[1:]
    elif estimation_points == 'log':
        s_hist = np.round(np.logspace(0,np.log10(nr),ns+1,base=10)).astype(int)[1:]
        s_hist = np.unique(s_hist)
        ns = s_hist.size

    # Number of experiments
    ne = 20

    # System definition
    Sa = nominal_parameters["Sa"]
    Sb = nominal_parameters["Sb"]

    # Input design hyperparameters
    u_mean_var = nominal_parameters["u_mean_std"]
    u_covr_var = nominal_parameters["u_covr_std"]

    for parameter_val in variable_parameter_list:
        if variable_parameter == "Sa":
            Sa = parameter_val
        elif variable_parameter == "Sb":
            Sb = parameter_val
        elif variable_parameter == "u_mean_std":
            u_mean_var = parameter_val
        elif variable_parameter == "u_covr_std":
            u_covr_var = parameter_val
        n,m,A,B,SigmaA,SigmaB = example_system_scalar(Sa,Sb)
        multi_experiment_increasing_rollout_count(n,m,A,B,SigmaA,SigmaB,ne,ns,s_hist,nr,ell,u_mean_var,u_covr_var)


def multiple_parameter_study():
    nominal_parameters = {"Sa": 0.5, "Sb": 0.5, "u_mean_std": 1.0, "u_covr_std": 0.1}

    parameter_list = {"Sa": np.logspace(-3, 1, 3, base=10),
                      "Sb": np.logspace(-3, 1, 3, base=10),
                      "u_mean_std": np.logspace(-3, 1, 3, base=10),
                      "u_covr_std": np.logspace(-3, 1, 3, base=10)}

    for key in nominal_parameters.keys():
        print("----Performing parameter study on %s ----" % key)
        parameter_study(key, parameter_list[key], nominal_parameters)
        print('')


def load_plot_multi_experiment(timestr):
    dirname_in = os.path.join("experiments",timestr)
    filename_in = os.path.join(dirname_in,'problem_data.pickle')
    problem_data = pickle_import(filename_in)
    filename_in = os.path.join(dirname_in,'experiment_data.npy')
    experiment_data = np.load(filename_in)
    n,m = problem_data['n'],problem_data['m']
    s_hist = problem_data['s_hist']
    plot_estimation_error_multi(n,m,s_hist, experiment_data, xlabel_str="Number of rollouts")
    plt.tight_layout()
    filename_out = os.path.join(dirname_in,"twostate_error_convergence.png")
    plt.savefig(filename_out,dpi=600)
    # plt.close()
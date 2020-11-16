import numpy as np
from numpy import linalg as la
from matrixmath import randn,vec

from ltimultgen import gen_system_mult
from policygradient import PolicyGradientOptions, run_policy_gradient, Regularizer
from ltimult import dlyap_obj,check_olmss

from matplotlib import pyplot as plt

from time import time

import os
from utility import create_directory
from pickle_io import pickle_import,pickle_export


def calc_sparsity(K,thresh,PGO):
    if PGO is None:
        regstr = 'vec1'
    else:
        if PGO.regularizer is None:
            regstr = 'vec1'
        else:
            regstr = PGO.regularizer.regstr

    # Calculate vals
    if regstr == 'vec1' or PGO.regularizer.regstr == 'vec_huber':
        vals = np.abs(vec(K))
    elif regstr == 'mr':
        vals = np.abs(K).max(1)
    elif regstr == 'mc':
        vals = np.abs(K).max(0)
    elif regstr == 'glr'or regstr == 'glr_huber':
        vals = la.norm(K,ord=2,axis=1)
    elif regstr == 'glc'or regstr == 'glc_huber':
        vals = la.norm(K,ord=2,axis=0)

    binmax = np.max(vals)
    bin1 = thresh*binmax
    sparsity = np.sum(vals<bin1)/vals.size
    print('Sparsity = %.3f' % sparsity)

    # Calculate black and white sparsity matrix
    Kbw = np.zeros_like(K)
    if regstr == 'vec1' or regstr == 'vec_huber':
        Kbw = np.abs(K)>bin1
    elif regstr == 'mr' or regstr == 'glr' or regstr == 'glr_huber':
        for i in range(K.shape[0]):
            if vals[i] > bin1:
                Kbw[i,:] = 1
    elif regstr == 'mc' or regstr == 'glc' or regstr == 'glc_huber':
        for j in range(K.shape[1]):
            if vals[j] > bin1:
                Kbw[:,j] = 1

    return vals,sparsity,binmax,bin1,Kbw


def plot_sparse(dirname,filename_pre,K,c,thresh,PGO,are_flag=False):
    # Sparsity visualizations
    vals,sparsity,binmax,bin1,Kbw = calc_sparsity(K,thresh,PGO)
    bins = np.hstack([np.array([0,bin1]),np.linspace(bin1,binmax,10)])

    if PGO is not None and not are_flag:
        title0str = 'Gain matrix entry abs values'
        title0str_bw = 'Gain matrix sparsity pattern'
        title1str = 'Regularizer weight = %.2f, Sparsity = %.2f%%,\nClosed-loop LQR cost = %.2f' % (PGO.regweight,100*sparsity,c)
    else:
        title0str = 'ARE gain matrix entry abs values'
        title0str_bw = 'ARE gain matrix sparsity pattern'
        title1str = 'Regularizer weight = 0, Sparsity = %.2f%%,\nClosed-loop LQR cost = %.2f' % (100*sparsity,c)

    fig_im, ax_im = plt.subplots()
    fig_im_bw, ax_im_bw = plt.subplots()
    fig_hist, ax_hist = plt.subplots()
    fig_im.set_size_inches((5, 4))
    fig_im_bw.set_size_inches((5, 4))
    fig_hist.set_size_inches((5, 4))

    # Color sparsity pattern plot
    img = ax_im.imshow(np.abs(K),aspect='equal')
    cbar = fig_im.colorbar(img,ax=ax_im)
    ax_im.set_title(title0str)
    filename_post = '_pattern.png'
    filename_out = filename_pre+filename_post
    path_out = os.path.join(dirname,filename_out)
    fig_im.savefig(path_out,dpi=300,bbox_inches='tight')


    # Black and white sparsity pattern plot
    if np.all(Kbw):
        img_bw = ax_im_bw.imshow(Kbw,cmap='gray',aspect='equal')
    else:
        img_bw = ax_im_bw.imshow(Kbw,cmap='Greys',aspect='equal')

    # Minor ticks
    ax_im_bw.set_xticks(np.arange(-.5, K.shape[1], 1), minor=True)
    ax_im_bw.set_yticks(np.arange(-.5, K.shape[0], 1), minor=True)

    # Gridlines based on minor ticks
    ax_im_bw.grid(which='minor',color=[0.5,0.5,0.5],linestyle='-',linewidth=1)

    ax_im_bw.set_title(title0str_bw)
    filename_post = '_pattern_bw.png'
    filename_out = filename_pre+filename_post
    path_out = os.path.join(dirname,filename_out)
    fig_im_bw.savefig(path_out,dpi=300,bbox_inches='tight')

    # Histogram
    ax_hist.hist(vals,bins=bins,rwidth=0.8)
#    ax_hist.set_ylim(0,K.size)
    ax_hist.set_title(title1str)
    filename_post = '_histogram.png'
    filename_out = filename_pre+filename_post
    path_out = os.path.join(dirname,filename_out)
    fig_hist.savefig(path_out,dpi=300,bbox_inches='tight')

    return ax_im,ax_im_bw,ax_hist,img,img_bw,cbar,sparsity


def set_initial_gains(SS,K0_method):
    # Initial gains
    if K0_method=='random':
        K0 = randn(SS.Kare.shape)
        SS.setK(K0)
        while not SS.c < np.inf:
            K0 = 0.9*K0 # Only guaranteed to work if sys open loop mean-square stable
            SS.setK(K0)
    if K0_method=='are':
        K0 = SS.Kare
        print('Initializing at the ARE solution')

    elif K0_method=='perturbed_are_safe':
        perturb_scale = float(10)/float(SS.n)  # scale with 1/n as rough heuristic
        safety_scale = float(10)
        Kp = randn(SS.Kare.shape[0],SS.Kare.shape[1])
        K0 = SS.Kare + perturb_scale*Kp
        SS.setK(K0)
        while not SS.c < safety_scale*SS.ccare:
            perturb_scale *= 0.5
            K0 = SS.Kare + perturb_scale*Kp
    elif K0_method=='zero':
        K0 = np.zeros([SS.m,SS.n])
        SS.setK(K0)
        P = dlyap_obj(SS,algo='iterative',show_warn=False)
        if P is not None:
            print('Initializing with zero gain solution')
        else:
            print('System not open-loop mean-square stable, use a different initial gain setting')
    elif K0_method=='user':
            K0[K1_subs] = 7.2
            K0[K2_subs] = -0.37
    SS.setK(K0)


def policy_gradient_setup(SS,optiongroup='gradient'):
    # Gradient descent options

    show_cost_surf = False
    if show_cost_surf:
        # Cost surface plot options
        # Set nominal gains
        Knom = SS.Kare
        # Select gain matrix entries to vary
        K1_subs = (1,1)
        K2_subs = (1,3)
        # Number of sample gain matrices
        # Create sample gain matrices
        nk1 = 100
        nk2 = nk1
        lim_scale = 40
        CSO = CostSurfaceOptions(Knom,K1_subs,K2_subs,lim_scale,nk1,nk2)
        CSO,c_grid,K1_grid,K2_grid = plot_cost_surf(SS,CSO)

    # Convergence threshold
    epsilon = (1e-2)*SS.Kare.size # Scale by number of gain entries as rough heuristic

    # Optimization method
#    opt_method = 'gradient'
#    opt_method = 'proximal'

    # Step size
#    eta = 1e-6

    # Step direction
#    step_direction = 'gradient'
#    step_direction = 'natural_gradient'
#    step_direction = 'gauss_newton'
#    step_direction = 'policy_iteration'

#    stepsize_method = 'constant'
#    stepsize_method = 'backtrack' # Fewer iterations but ~same runtime due to dlyap evals
#    stepsize_method = 'square_summable' # a/(b+k)
#    stepsize_method = 'nonsummable_diminishing' # a/np.sqrt(k)

    # Regularizer
#    regstr = 'vec1'
#    regstr = 'vecinf'
#    regstr = 'mr'
#    regstr = 'glr'
#    regstr = 'sglr'

#    regstr = 'vec_huber'
#    regstr = 'glr_huber'
#    regstr = 'vec_huber'
#    regstr = 'mr_huber'

    regstr = 'vec1'
#    regstr = 'glr'


    eta = 1e-5

    regweight = 1.0

    max_iters = 1000
    fbest_repeat_max = 100
    stepsize_method = 'constant'

    if optiongroup == 'gradient':
        opt_method = 'gradient'
        step_direction = 'gradient'
        stop_crit = 'gradient'
        keep_opt = 'last'
        if regstr == 'vec1':
            regstr = 'vec_huber'
        elif regstr == 'glr':
            regstr = 'glr_huber'

    elif optiongroup == 'subgradient':
        opt_method = 'gradient'
        step_direction = 'gradient'
        stop_crit = 'fbest'
        keep_opt = 'best'

    elif optiongroup == 'proximal_gradient':
        opt_method = 'proximal'
        step_direction = 'gradient'
        stop_crit = 'fixed'
        keep_opt = 'last'




    elif optiongroup == 'proximal_gradient_NPG':
        opt_method = 'proximal'
        step_direction = 'natural_gradient'
        stop_crit = 'Kchange'
        keep_opt = 'last'
    elif optiongroup == 'proximal_gradient_GN':
        opt_method = 'proximal'
        step_direction = 'gauss_newton'
        eta = 1e-2
        stop_crit = 'fixed'
        max_iters = 300
        keep_opt = 'last'
        regweight *= 0.001
    elif optiongroup == 'proximal_gradient_GN_PI':
        opt_method = 'proximal'
        step_direction = 'policy_iteration'
        eta = 0.5
        stop_crit = 'fixed'
        max_iters = 30
        keep_opt = 'last'
        regweight *= 0.0001



    mu = 0.7
    soft = False
    thresh1 = 0.001 # Should be between 0 (very hard) and 1 (very soft), units are nondimensional
    thresh2 = 0.001 # Should be between 0 (very hard) and large (very soft), units are gain
    regularizer = Regularizer(regstr,mu,soft,thresh1,thresh2)
#    regularizer = None
#    regweight = float(0.1)

#    stop_crit = 'gradient'
#    stop_crit = 'fbest'
#    fbest_repeat_max = 100
#    stop_crit = 'fixed'
#    keep_opt = 'last'
#    keep_opt = 'best'

#    opt_method = 'proximal'
#    step_direction = 'policy_iteration'
#    stepsize_method = 'constant'
#    eta = 0.5
#    stop_crit = 'fixed'
#    fbest_repeat_max = 100
#    keep_opt = 'last'
#    max_iters = 20
#    regweight = float(0.1)

#    opt_method = 'proximal'
#    step_direction = 'gradient'
#    stepsize_method = 'constant'
#    eta = 1e-4
##    stop_crit = 'fbest'
#    fbest_repeat_max = 100
#    stop_crit = 'gradient'
##    stop_crit = 'fixed'
#    keep_opt = 'last'
#    max_iters = 10000
#    regweight = float(1)

    PGO = PolicyGradientOptions(epsilon=epsilon,
                                eta=eta,
                                max_iters=max_iters,
                                disp_stride=1,
                                keep_hist=True,
                                opt_method=opt_method,
                                keep_opt=keep_opt,
                                step_direction=step_direction,
                                stepsize_method=stepsize_method,
                                exact=True,
                                regularizer=regularizer,
                                regweight=regweight,
                                stop_crit=stop_crit,
                                fbest_repeat_max=fbest_repeat_max,
                                display_output=True,
                                display_inplace=True,
                                slow=False)
    return PGO


def traverse_sparsity(SS,PGO,optiongroup,optiongroup_dir):
    # Sparsity traversal settings
    sparsity_required = 0.95
    sparse_thresh = 0.001

    plt.ioff()

    img_folder = 'sparsity_images'
    img_dirname_out = os.path.join(optiongroup_dir,img_folder)
    create_directory(img_dirname_out)

    filename_out_pre = 'sparsity_are'
    plot_sparse(img_dirname_out,filename_out_pre,SS.Kare,SS.ccare,sparse_thresh,PGO,are_flag=True)


    regweight_ratio = np.sqrt(2)
    if optiongroup=='proximal_gradient_GN_PI':
        eta_ratio = 1
    else:
        eta_ratio = (1/regweight_ratio)**np.sqrt(regweight_ratio) # empirically works well

    sparsity_data = []
    img_pattern = 'sparsity%02d'

    iterc = 0
    iterc_max = 18

    stop = False
    sparsity_prev = 0
    sparsity_max = 0
    while not stop:
        # Policy gradient
        t_start = time()
        SS,hist_list = run_policy_gradient(SS,PGO)
        t_end = time()
        filename_out = 'system_%d_regweight_%.3f.pickle' % (iterc,PGO.regweight)
        filename_out = filename_out.replace('.','p')
        path_out = os.path.join(optiongroup_dir,filename_out)
        pickle_export(optiongroup_dir,path_out,SS)

        # Plotting
        filename_out_pre = img_pattern % iterc
        ax_im,ax_im_bw,ax_hist,img,img_bw,cbar,sparsity = plot_sparse(img_dirname_out,filename_out_pre,SS.K,SS.c,sparse_thresh,PGO)
        plt.close('all')

        sparsity_data.append([PGO.regweight,sparsity,SS.K,SS.c,t_end-t_start,hist_list])

        if sparsity > sparsity_required:
            stop = True
#        if sparsity < sparsity_prev:
#            stop = True
#        if sparsity_max > 0.60 and sparsity < 0.05:
#            stop = True
        if sparsity_max > 0.60 and sparsity < sparsity_prev:
            stop = True

        if iterc >= iterc_max-1:
            stop = True

        PGO.eta *= eta_ratio
        PGO.regweight *= regweight_ratio

        sparsity_prev = sparsity
        sparsity_max = np.max([sparsity,sparsity_max])
        iterc += 1

#        input("Press [enter] to continue.")

#    vidname = 'sparsity_evolution'
#    vidsave(img_folder,img_pattern,vidname)

    filename_out = 'sparsity_data.pickle'
    path_out = os.path.join(optiongroup_dir,filename_out)
    pickle_export(optiongroup_dir,path_out,sparsity_data)

    return sparsity_data



def load_system(timestr):
    # Import
    dirname_in = os.path.join('example_systems',timestr)
    filename_only = 'system_init.pickle'
    SS = pickle_import(os.path.join(dirname_in,filename_only))
    #Export
    timestr = str(time()).replace('.','p')
    dirname_out = os.path.join('systems',timestr)
    SS.dirname = dirname_out
    filename_out = os.path.join(dirname_out,filename_only)
    pickle_export(dirname_out, filename_out, SS)
    return SS



###############################################################################
if __name__ == "__main__":
    SS = gen_system_mult(n=20,m=20,safety_margin=0.3,noise='olmsus',
                         mult_noise_method='random',SStype='random')


#    timestr = '1556656014p3178775_n50_olmss_vec1'
#    SS = load_system(timestr)

    check_olmss(SS)

    optiongroup_list = ['gradient','subgradient','proximal_gradient']

#    optiongroup_list = ['gradient']
#    optiongroup_list = ['subgradient']
#    optiongroup_list = ['proximal_gradient']

    for optiongroup in optiongroup_list:
        optiongroup_dir = os.path.join(SS.dirname,optiongroup)
        create_directory(optiongroup_dir)

        # Policy gradient setup
        t_start = time()
        K0_method = 'are'
        set_initial_gains(SS,K0_method=K0_method)
        PGO = policy_gradient_setup(SS,optiongroup)
        filename_out = 'policy_gradient_options.pickle'
        path_out = os.path.join(optiongroup_dir,filename_out)
        pickle_export(optiongroup_dir,path_out,PGO)
        t_end = time()
        print('Initialization completed after %.3f seconds' % (t_end-t_start))

        # Sparsity traversal
        traverse_sparsity(SS,PGO,optiongroup, optiongroup_dir)

#        run_policy_gradient(SS,PGO)
import numpy as np
import numpy.linalg as la
import numpy.random as npr
#from matrixmath import is_pos_def,mdot,specrad,minsv,sympart,dlyap,dare,solveb

import sys
sys.path.append("..")
from ltimult import LQRSys,LQRSysMult

from pickle_io import pickle_export
from time import time
import os

from utility import printout, create_directory

def gradient_estimate_variance(noise,textfile,seed=1):
    npr.seed(seed)
    # Generate the system
    # Two states, diffusion w/ friction and multiplicative noise
    n = 2
    m = 1
    A = np.array([[0.8,0.1],[0.1,0.8]])
    B = np.array([[1.0],[0.0]])
    a = np.array([[0.1]])
    Aa = np.array([[0.0,1.0],[1.0,0.0]])[:,:,np.newaxis]
    b = np.array([[0.0]])
    Bb = np.array([[0.0],[0.0]])[:,:,np.newaxis]
    Q = np.eye(2)
    R = np.eye(1)
    S0 = np.eye(2)

    if noise:
        SS = LQRSysMult(A,B,a,Aa,b,Bb,Q,R,S0)
    else:
        SS = LQRSys(A,B,Q,R,S0)

    # Initialize
#    K0 = 0.01*np.ones([m,n])
    K0 = np.zeros([m,n])
    SS.setK(K0)
    K = np.copy(SS.K)

    print(SS.c)

    # Number of gradient estimates to collect for variance analysis
    n_iterc = 10

    # Rollout length
    nt = 40

    # Number of rollouts
    nr = int(1e4)

    # Exploration radius
    ru = 1e-2

    G_est_all = np.zeros([n_iterc,m,n])
    error_angle_all = np.zeros(n_iterc)
    error_scale_all = np.zeros(n_iterc)
    error_norm_all = np.zeros(n_iterc)

    headerstr_list = []
    headerstr_list.append('    trial ')
    headerstr_list.append('error angle (deg)')
    headerstr_list.append('  error scale ')
    headerstr_list.append(' error norm')
    headerstr_list.append('true gradient norm')
    headerstr = " | ".join(headerstr_list)
    printout(headerstr,textfile)

    t_start = time()

    for iterc in range(n_iterc):
        # Estimate gradient using zeroth-order optimization

        # Draw random gain deviations and scale to Frobenius norm ball
        Uraw = npr.normal(size=[nr,SS.m,SS.n])
        U = ru*Uraw/la.norm(Uraw,'fro',axis=(1,2))[:,None,None]

        # Stack dynamics matrices into a 3D array
        Kd = K + U

        # Simulate all rollouts together
        c = np.zeros(nr)

        # Draw random initial states
        x = npr.multivariate_normal(np.zeros(SS.n),SS.S0,nr)

        for t in range(nt):
            # Accumulate cost
            c += np.einsum('...i,...i',x,np.einsum('jk,...k', SS.QK, x))

            # Calculate closed-loop dynamics
            AKr = SS.A + np.einsum('...ik,...kj',SS.B,Kd)

            if noise:
                for i in range(SS.p):
                    AKr += (SS.a[i]**0.5)*npr.randn(nr)[:,np.newaxis,np.newaxis]*np.repeat(SS.Aa[np.newaxis,:,:,i], nr, axis=0)
                for j in range(SS.q):
                    AKr += np.einsum('...ik,...kj',(SS.b[j]**0.5)*npr.randn(nr)[:,np.newaxis,np.newaxis]*np.repeat(SS.Bb[np.newaxis,:,:,j], nr, axis=0),Kd)

            # Transition the state
            x = np.einsum('...jk,...k', AKr, x)


        # Estimate gradient
        Glqr = np.einsum('i,i...', c, U)
        Glqr *= K.size/(nr*(ru**2))

        G_est = Glqr
        G_act = SS.grad

        error_angle = (360/(2*np.pi))*np.arccos(np.sum((G_est*G_act))/(la.norm(G_est)*la.norm(G_act)))
        error_scale = (la.norm(G_est)/la.norm(G_act))
        error_norm = la.norm(G_est-G_act)

        G_est_all[iterc] = G_est
        error_angle_all[iterc] = error_angle
        error_scale_all[iterc] = error_scale
        error_norm_all[iterc] = error_norm

        # Print iterate messages
        printstrlist = []
        printstrlist.append("{0:9d}".format(iterc+1))
        printstrlist.append("   {0:6.2f} / 360".format(error_angle))
        printstrlist.append("{0:8.4f} / 1".format(error_scale))
        printstrlist.append("{0:9.4f}".format(error_norm))
        printstrlist.append("{0:9.4f}".format(la.norm(G_act)))
        printstr = '  |  '.join(printstrlist)
        printout(printstr,textfile)

    t_end = time()
    printout('',textfile)
    printout('mean of error angle',textfile)
    printout('%f' % np.mean(error_angle_all),textfile)
    printout('mean of error scale',textfile)
    printout('%f' % np.mean(error_scale_all),textfile)
    printout('mean of error norm',textfile)
    printout('%f' % np.mean(error_norm_all),textfile)
#    printout('standard deviation of raw gradient estimate, entrywise',textfile)
#    printout('%f' % np.std(G_est_all,0),textfile)
    printout('average time per gradient estimate (s)',textfile)
    printout("%.3f" % ((t_end-t_start)/n_iterc),textfile)
    printout('',textfile)

    return G_act, G_est_all,error_angle_all,error_scale_all,error_norm_all

###############################################################################
# Main
###############################################################################
timestr = str(time()).replace('.','p')
dirname_out = timestr
create_directory(dirname_out)

textfilename_only = "noiseless.txt"
textfile_out = os.path.join(dirname_out,textfilename_only)
textfile = open(textfile_out,"w+")
data_noiseless = gradient_estimate_variance(noise=False,textfile=textfile)
textfile.close()
filename_only = 'data_noiseless.pickle'
filename_out = os.path.join(dirname_out,filename_only)
pickle_export(dirname_out, filename_out, data_noiseless)

textfilename_only = "noisy.txt"
textfile_out = os.path.join(dirname_out,textfilename_only)
textfile = open(textfile_out,"w+")
data_noisy = gradient_estimate_variance(noise=True,textfile=textfile)
textfile.close()
filename_only = 'data_noisy.pickle'
filename_out = os.path.join(dirname_out,filename_only)
pickle_export(dirname_out, filename_out, data_noisy)
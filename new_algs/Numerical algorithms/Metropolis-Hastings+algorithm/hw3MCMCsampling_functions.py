import scipy as sc
import scipy.io as scio
import scipy.io.wavfile as wav
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from numpy import shape
import scipy.linalg as lin
import scipy.stats as st
import math
import os
from xlwt import Row
from astropy.table import row
import matplotlib.cm as cm
import matplotlib.colors as clrs
from matplotlib.colors import Colormap
from matplotlib import pylab
from blz.bfuncs import arange

def p(x):
    # calculate and return p(x) as given in the hw3 assignment handout:
    return .3*(st.norm(-25, 10).pdf(x)) + .7*(st.norm(20, 10).pdf(x))

def p_nDims(x):
    # establish the pre-determined mu1, mu2, cov1, and cov2 for our target multivariate distribution:
    mu1 = np.array([4.0,2.0])
    mu2 = np.array([-7.0,5.0])
    cov1 = np.array([8.0, 15.0, 5.0, 25.0])
    cov1 = np.reshape(cov1, (2,2))
    cov2 = np.array([12.0, 5.0, 0.0, 3.0])
    cov2 = np.reshape(cov2, (2,2))
    # calculate and return p(x) for a multidimensional guassian mixture distribution:
    return .65*(st.multivariate_normal.pdf(x, mu1, cov1)) + .35*(st.multivariate_normal.pdf(x, mu2, cov2))

def q(x, mu, sigma):
    # calculate and return q(x) as given in the hw3 assignment handout:
    return st.norm(mu, sigma).pdf(x)

def q_nDims(x, mu, cov):
    # calculate and return q(x) for a multidimensional proposal distribution:
    return st.multivariate_normal.pdf(x, mu, cov)

def runMetropolisHastings_1Dim(n, mu_initial, sigma, err_interval, num_bins, print_accept_rt_interval):
    # REFERENCE NOTE: This algorithm is based on the description and pseudocode provided in the Marsland Textbook (Chp 15):
    u = np.random.rand(n)
    samples = np.empty(n)
    samples[0] = np.random.normal(mu_initial, sigma)
    errs = list()
    accepted = list()
    accept_rt = float(0)
    accept_rt_list = list()
    for i in xrange(0, n-1):
        if (i != 0 and i % err_interval == 0):
            err = calcError_1Dim(samples[0:i], num_bins)
            errs.append(err)
            print(str(i) + ": err = " + str(err))
        if (i != 0 and i % print_accept_rt_interval == 0):
            print(str(i) + ": accept_rt = " + str(accept_rt))
        candidate = np.random.normal(samples[i], sigma)
        acceptance_rate = min(1, (p(candidate)*q(samples[i], candidate, sigma))/(p(samples[i])*q(candidate, samples[i], sigma)))
        if u[i] < acceptance_rate:
            samples[i+1] = candidate
            accepted.append(1)
        else:
            samples[i+1] = samples[i]
            accepted.append(0)
        if i < 2000:
            accept_rt = float(sum(accepted))/float(i+1)
        else:
            accept_rt = float(sum(accepted[(i-2000):i]))/(float(2000))        
        accept_rt_list.append(accept_rt)
    return samples, errs, accept_rt, accept_rt_list

def runMetropolisHastings_nDim(n, dim, mu, cov, err_interval, num_bins, norm_const, print_accept_rt_interval):
    # REFERENCE NOTE: This algorithm is based on the description and pseudocode provided in the Marsland Textbook (Chp 15):
    u = np.random.rand(n)
    samples = np.empty((dim, n))
    samples[:,0] = np.random.multivariate_normal(mu, cov)
    errs = list()
    accepted = list()
    accept_rt = float(0)
    accept_rt_list = list()
    for j in xrange(0, n-1):
        if (j != 0 and j % err_interval == 0):
            err = calcError_2Dim(samples[:,0:j], num_bins, norm_const)
            errs.append(err)
            print(str(j) + ": err = " + str(err))
        if (j != 0 and j % print_accept_rt_interval == 0):
            print(str(j) + ": accept_rt = " + str(accept_rt))
        candidate = np.random.multivariate_normal(mu, cov)
        acceptance_rate = min(1, (p_nDims(candidate)*q_nDims(samples[:,j], candidate, cov))/(p_nDims(samples[:,j])*q_nDims(candidate, samples[:,j], cov)))
        if u[j] < acceptance_rate:
            samples[:,j+1] = candidate
            accepted.append(1)
        else:
            samples[:,j+1] = samples[:,j]
            accepted.append(0)
        if j < 2000:
            accept_rt = float(sum(accepted))/float(j+1)
        else:
            accept_rt = float(sum(accepted[(j-2000):j]))/(float(2000))
        accept_rt_list.append(accept_rt)
    return samples, errs, accept_rt, accept_rt_list
        
def plotProposalDistVsTargetDist():
    a = float(-70)
    b = float(70)
    random_inputs = (b-a)*np.random.rand(1000) + a
    random_inputs[0] = a
    random_inputs[1] = b
    random_inputs_sorted = sorted(random_inputs)
    plt.plot(random_inputs_sorted, p(random_inputs_sorted), linewidth=2, color='r')
    sigmas = [15, 17.5, 20, 22.5]
    for sigma in xrange(0,len(sigmas)):
        plt.plot(random_inputs_sorted, q(random_inputs_sorted, 20, sigmas[sigma]), linewidth=1, color='b')
    plt.xlim(a, b)
    fig = plt.figure(1)
    plt.show()
    plt.close()


def showAndSaveHistogram_1Dim(samples, num_bins, expID, path, D, proposal_dist, sigma, n, burn_in, keep_every, num_samples_fnl, err_fnl):
    a = float(-70)
    b = float(70)
    count, bins, ignored = plt.hist(samples, num_bins, normed=True)
    random_inputs = (b-a)*np.random.rand(1000) + a
    random_inputs[0] = a
    random_inputs[1] = b
    random_inputs_sorted = sorted(random_inputs)
    plt.plot(random_inputs_sorted, p(random_inputs_sorted), linewidth=2, color='r')
    plt.xlim(a, b)
    fig = plt.figure(1)
        
    title = "HISTOGRAM  exp" + str(expID) +"   "\
        + str(D) + "D"  +"   "\
        + "Q=" + str(proposal_dist) +"   "\
        + "sigma=" + str(sigma)
    fig.suptitle(title, fontsize='20')    
        
    txt = "exp" + str(expID) +"  "\
        + str(D) + "D\n"\
        + "Q=" + str(proposal_dist) +"  "\
        + "sigma=" + str(sigma) +"\n"\
        + "n=" + str(n) +"  "\
        + "burn_in=" + str(burn_in) +"\n"\
        + "keep_every=" + str(keep_every) +"\n"\
        + "num_samples_fnl=" + str(num_samples_fnl) +"\n"\
        + "err_fnl=" + str(round(err_fnl, 8))
    plt.text(a + 5, .021, txt, style='italic', bbox={'facecolor':'blue', 'alpha':0.1, 'pad':10})
    
    plt.xlabel('generated samples, x', fontsize=16)
    plt.ylabel('p(x)', fontsize=16)
    os.chdir(path)
    
    save_name = "HIST_exp" + str(expID) +"_"\
        + str(D) +"D_"\
        + str(proposal_dist) +"_"\
        + "sigma" + str(sigma) +"_"\
        + "n" + str(n) +"_"\
        + "burn" + str(burn_in) +"_"\
        + str(keep_every) +"th_"\
        + "err" + str(round(err_fnl, 5)) +"."  
    plt.savefig(save_name)
    plt.show() 
    plt.close()
    

def showAndSaveHistogram_2Dim(samples, num_bins, expID, path, D, proposal_dist, sigma, n, burn_in, keep_every, num_samples_fnl, err_fnl):  
    # get figure and axes in 3D:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # set min and max for figure:
    x1_min = -20
    x1_max = 15
    x2_min = -15
    x2_max = 20
    # create a surface_plot of our target mulitvariate Guassian Mixture distribution:
    x1_surface = np.arange(x1_min, x1_max+1, .25)
    x2_surface = np.arange(x2_min, x2_max+1, .25)
    X1_surface, X2_surface = np.meshgrid(x1_surface, x2_surface)
    Z_surface = np.empty_like(X1_surface)
    for i in xrange (0, len(X1_surface)):
        for j in xrange(0, len(X1_surface)):
            Z_surface[i,j] = p_nDims([X1_surface[i,j], X2_surface[i,j]])
    ax.plot_surface(X1_surface, X2_surface, Z_surface, rstride=5, cstride=5, alpha=0.4)
    
    # set labels, etc. for 3D surface plot:
    axis_label_fontdict = {'fontsize':25, 'fontweight':'bold', 'color':'r'}
    ax.set_xlabel('X1', fontdict=axis_label_fontdict)
    ax.set_xlim(-20, 15)
    ax.set_ylabel('X2', fontdict=axis_label_fontdict)
    ax.set_ylim(-15, 20)
    ax.set_zlabel('Z', fontdict=axis_label_fontdict)

    x1 = samples[0,:]
    x2 = samples[1,:]
    
    rng = [[x1_min,x1_max],[x2_min,x2_max]] 
    # REFERENCE NOTE: the second half of this function for plottingin 3D was adapted from an online source:
    # http://matplotlib.org/examples/mplot3d/hist3d_demo.html
    hist, x1edges, x2edges = np.histogram2d(x1, x2, bins=50, range=rng, normed=True)
    elements = (len(x1edges) - 1) * (len(x2edges) - 1)
    x1pos, x2pos = np.meshgrid(x1edges[:-1], x2edges[:-1])
    x1pos = x1pos.flatten()
    x2pos = x2pos.flatten()
    zpos = np.zeros(elements)
    dx1 = 0.5 * np.ones_like(zpos)
    dx2 = dx1.copy()
    dz = hist.flatten()
    # REFERENCE NOTE: this technique for setting the colormap was adapted from matplotlib's online demo repository:
    # http://matplotlib.org/examples/...
    offset = dz + np.abs(dz.min())
    fracs = offset.astype(float)/offset.max()
    norm = clrs.Normalize(fracs.min(), fracs.max())
    my_colors = cm.coolwarm(norm(fracs))
    # plot the histogram2d data as a bar3d on the same axes:
    ax.bar3d(x1pos, x2pos, zpos, dx1, dx2, dz, color=my_colors, zsort='average', alpha=.4)

    title = "2D HISTOGRAM  exp" + str(expID) +"   "\
        + str(D) + "D"  +"   "\
        + "Q=" + str(proposal_dist) +"   "\
        + "\nsigma=" + str(sigma[0,:]) + str(sigma[1,:])
    fig.suptitle(title, fontsize='20')    

    txt = "exp" + str(expID) +"  "\
        + str(D) + "D\n"\
        + "Q=" + str(proposal_dist) +"  "\
        + "sigma=" + str(sigma[0,:]) + str(sigma[1,:]) +"\n"\
        + "n=" + str(n) +"  "\
        + "burn_in=" + str(burn_in) +"\n"\
        + "keep_every=" + str(keep_every) +"\n"\
        + "num_samples_fnl=" + str(num_samples_fnl) +"\n"\
        + "err_fnl=" + str(round(err_fnl, 8))
    plt.figtext(0, 0, txt, style='italic', bbox={'facecolor':'blue', 'alpha':0.1, 'pad':10}, figure=fig)

    os.chdir(path)
     
    save_name = "3DHIST_exp" + str(expID) +"_"\
        + str(D) +"D_"\
        + str(proposal_dist) +"_"\
        + "n" + str(n) +"_"\
        + "burn" + str(burn_in) +"_"\
        + str(keep_every) +"th_"\
        + "err" + str(round(err_fnl, 5)) +"."  
    plt.savefig(save_name)

    # display the histogram2d by itself in a new figure:
    fig1 = plt.figure()
    ax1 = fig1.add_subplot()
    count, xedges, yedges, image = plt.hist2d(x1, x2, num_bins, normed=True)    
    pylab.colorbar()
    
    fig1.suptitle(title, fontsize='20')    
    plt.figtext(0, 0, txt, style='italic', bbox={'facecolor':'blue', 'alpha':0.1, 'pad':10}, figure=fig1)
    
    save_name2 = "2DHIST_exp" + str(expID) +"_"\
        + str(D) +"D_"\
        + str(proposal_dist) +"_"\
        + "n" + str(n) +"_"\
        + "burn" + str(burn_in) +"_"\
        + str(keep_every) +"th_"\
        + "err" + str(round(err_fnl, 5)) +"."  
    plt.savefig(save_name2)

    plt.show() 
    plt.close()
    
      
def showAndSaveWalk_1Dim(samples, full_kept, num_bins, expID, path, D, proposal_dist, sigma, n, burn_in, keep_every, num_samples_fnl, err_fnl):
    a = float(-70)
    b = float(70)
    
    plt.clf()
    iterations = xrange(0, len(samples))
    plt.plot(iterations, samples, linewidth=.25, color='b')
    plt.xlim(0, len(iterations))
    plt.ylim(a, b + 20)
    fig = plt.figure(1)
    
    if full_kept == "full":
        title = "FULL WALK PTRN  exp" + str(expID) +"   "\
            + str(D) + "D"  +"   "\
            + "Q=" + str(proposal_dist) +"   "\
            + "sigma=" + str(sigma)
    else:
        title = "WALK PTRN  exp" + str(expID) +"   "\
            + str(D) + "D"  +"   "\
            + "Q=" + str(proposal_dist) +"   "\
            + "sigma=" + str(sigma)
    fig.suptitle(title, fontsize='20')    
        
    txt = "exp" + str(expID) +"  "\
        + str(D) + "D\n"\
        + "Q=" + str(proposal_dist) +"  "\
        + "sigma=" + str(sigma) +"\n"\
        + "n=" + str(n) +"  "\
        + "burn_in=" + str(burn_in) +"\n"\
        + "keep_every=" + str(keep_every) +"\n"\
        + "num_samples_fnl=" + str(num_samples_fnl) +"\n"\
        + "err_fnl=" + str(round(err_fnl, 8))
    plt.text(100, 45, txt, style='italic', bbox={'facecolor':'blue', 'alpha':0.1, 'pad':10})
    
    plt.xlabel('iterations', fontsize=16)
    plt.ylabel('generated samples, x', fontsize=16)
    os.chdir(path)
    
    if full_kept == "full":
        save_name = "FL_WALK_exp" + str(expID) +"_"\
            + str(D) +"D_"\
            + str(proposal_dist) +"_"\
            + "sigma" + str(sigma) +"_"\
            + "n" + str(n) +"_"\
            + "burn" + str(burn_in) +"_"\
            + str(keep_every) +"th_"\
            + "err" + str(round(err_fnl, 5)) +"."
    else:
        save_name = "WALK_exp" + str(expID) +"_"\
            + str(D) +"D_"\
            + str(proposal_dist) +"_"\
            + "sigma" + str(sigma) +"_"\
            + "n" + str(n) +"_"\
            + "burn" + str(burn_in) +"_"\
            + str(keep_every) +"th_"\
            + "err" + str(round(err_fnl, 5)) +"."       
    plt.savefig(save_name)
    plt.show() 
    plt.close() 

def get1DimHist(samples, num_bins):
    count, bins, ignored = plt.hist(samples, num_bins, normed=True)
    plt.close()
    return count, bins

def get2DimHist(samples, num_bins):
    x1 = samples[0,:]
    x2 = samples[1,:]
    count, x1edges, x2edges, image = plt.hist2d(x1, x2, num_bins, normed=True)
    plt.close()
    return count, x1edges, x2edges

def calcError_1Dim(samples, num_bins):
    count, bins = get1DimHist(samples, num_bins)
    sse = float(0)
    for j in xrange(0, len(count)):
        sse += (p(bins[j]) - count[j])**2
    return sse    
    
def calcError_2Dim(samples, num_bins, norm_const):
    norm_factor = (num_bins[0]*num_bins[1])/norm_const
    count, x1edges, x2edges = get2DimHist(samples, num_bins)
    sse = float(0)
    for i in xrange(0, len(x1edges) - 1):
        for j in xrange(0, len(x2edges) - 1):
            sse += (((p_nDims([x1edges[i], x2edges[j]]) - count[i,j])**2)/norm_factor)
    return sse  

# auxillary function...not used though:
def scale_min_max(M):
    K = np.array(M)
    K_scaled = np.empty_like(K)
    for i in xrange(0, len(K[:,0])):
        row = K[i,:]
        max = np.amax(row)
        min = np.amin(row)
        scaled_row = (row - min)/(max - min)
        K_scaled[i,:] = scaled_row
    return K_scaled



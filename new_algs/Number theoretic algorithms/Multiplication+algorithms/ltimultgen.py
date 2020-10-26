import numpy as np
from numpy import linalg as la
from numpy import random as npr
from ltimult import LQRSysMult, dare_mult, dlyap_mult
import scipy

import random

from matplotlib import pyplot as plt
from matplotlib import patches
from matplotlib.patheffects import withStroke
from matplotlib.collections import PatchCollection
from matplotlib.collections import LineCollection

from pickle_io import pickle_export
from time import time
import os
from utility import create_directory

seed = 3187
rng = np.random.RandomState(seed)

def set_rng_seed(seed=-1):
    if seed < 0:
        seed = random.randint(0,2**32-1)
    global rng
    rng = np.random.RandomState(seed)

def rand(*args):
    return rng.rand(*args)

def randn(*args):
    return rng.randn(*args)

def randint(*args):
    return rng.randint(*args)


###############################################################################
# System generation functions
###############################################################################
def gen_system_mult(n=8, m=8, safety_margin=0.3, noise='weak',
                    mult_noise_method='random', SStype='ER',
                    seed=None, saveSS=True):

    timestr = str(time()).replace('.','p')
    dirname_out = os.path.join('systems',timestr)

    if seed is not None:
        set_rng_seed(seed)

    if SStype == 'random':
        A,B = gen_system_AB_rand(n,m,safety_margin)
    elif SStype == 'ER':
        A,B = gen_system_AB_erdos_renyi(n,dirname_out=dirname_out)
        m = B.shape[1]
    elif SStype == 'example':
        A = np.array([[0.8,0.3],[-0.2,0.7]])
        B = np.array([[0.5,0.3]]).T
        Q = np.eye(2)
        R = np.eye(1)
        S0 = np.eye(2)
        Aa = np.array([[0.2,0.3],[0.2,0.3]])
        Aa = Aa[:,:,np.newaxis]
        Bb = np.array([[0.2,0.3]]).T
        Bb = Bb[:,:,np.newaxis]
        a = np.array([[0.3]])
        b = np.array([[0.3]])
        SS = LQRSysMult(A,B,a,Aa,b,Bb,Q,R,S0)
        SS.dirname = dirname_out
        filename_only = 'system_init.pickle'
        filename_out = os.path.join(dirname_out,filename_only)
        pickle_export(dirname_out, filename_out, SS)
        return SS

    # LQR cost matrices
    Q = np.eye(n)
    # Q = randn(n,n)
    # Q = np.dot(Q,Q')

    R = np.eye(m)
    # R = randn(m,m)
    # R = np.dot(R,R')

    # Initial state distribution covariance
    # S0 = randn(n,n)
    # S0 = np.dot(S0,S0')
    S0 = np.eye(n)

    # Multiplicative noise data
    p = 2  # Number of multiplicative noises on A
    q = 2  # Number of multiplicative noises on B

    if mult_noise_method == 'random':
        Aa = randn(n,n,p)
        Bb = randn(n,m,q)
    elif mult_noise_method == 'rowcol':
        # Pick a random row and column
        Aa = np.zeros([n,n,p])
        Bb = np.zeros([n,m,q])

        Aa[randint(n),:,0] = np.ones(n)
        Aa[:,randint(n),1] = np.ones(n)

        Bb[randint(n),:,0] = np.ones(m)
        Bb[:,randint(m),1] = np.ones(n)
    elif mult_noise_method == 'random_plus_rowcol':
        Aa = 0.3*randn(n,n,p)
        Bb = 0.3*randn(n,m,q)
        # Pick a random row and column
        Aa[randint(n),:,0] = np.ones(n)
        Aa[:,randint(n),1] = np.ones(n)
        Bb[randint(n),:,0] = np.ones(m)
        Bb[:,randint(m),1] = np.ones(n)

    incval = 1.05
    decval = 1.00*(1/incval)
    weakval = 0.90

    # a = randn([p,1])
    # b = randn([q,1])
    a = np.ones([p,1])
    b = np.ones([q,1])
    a = a*(float(1)/(p*n**2))  # scale as rough heuristic
    b = b*(float(1)/(q*m**2))  # scale as rough heuristic

#    noise = 'weak'
    if noise=='weak' or noise=='critical':
        # Ensure near-critically mean square stabilizable
        # increase noise if not
        P,Kare = dare_mult(A,B,a,Aa,b,Bb,Q,R,show_warn=False)
        mss = True
        while mss:
            if Kare is None:
                mss = False
            else:
                a = incval*a
                b = incval*b
                P,Kare = dare_mult(A,B,a,Aa,b,Bb,Q,R,show_warn=False)
        # Extra mean square stabilizability margin
        a = decval*a
        b = decval*b
        if noise == 'weak':
#            print('Multiplicative noise set weak')
            a = weakval*a
            b = weakval*b
    elif noise=='olmss_weak' or noise=='olmss_critical':
        # Ensure near-critically open-loop mean-square stable
        # increase noise if not
        K0 = np.zeros([m,n])
        P = dlyap_mult(A,B,K0,a,Aa,b,Bb,Q,R,S0,matrixtype='P')
        mss = True
        while mss:
            if P is None:
                mss = False
            else:
                a = incval*a
                b = incval*b
                P = dlyap_mult(A,B,K0,a,Aa,b,Bb,Q,R,S0,matrixtype='P')
        # Extra mean square stabilizability margin
        a = decval*a
        b = decval*b
        if noise == 'olmss_weak':
#            print('Multiplicative noise set to open-loop mean-square stable')
            a = weakval*a
            b = weakval*b
    elif noise=='olmsus':
        # Ensure near-critically open-loop mean-square unstable
        # increase noise if not
        K0 = np.zeros([m,n])
        P = dlyap_mult(A,B,K0,a,Aa,b,Bb,Q,R,S0,matrixtype='P')
        mss = True
        while mss:
            if P is None:
                mss = False
            else:
                a = incval*a
                b = incval*b
                P = dlyap_mult(A,B,K0,a,Aa,b,Bb,Q,R,S0,matrixtype='P')
#        # Extra mean square stabilizability margin
#        a = decval*a
#        b = decval*b
#        print('Multiplicative noise set to open-loop mean-square unstable')
    elif noise=='none':
        print('MULTIPLICATIVE NOISE SET TO ZERO!!!')
        a = np.zeros([p,1])  # For testing only - no noise
        b = np.zeros([q,1])  # For testing only - no noise
    else:
        raise Exception('Invalid noise setting chosen')

    SS = LQRSysMult(A,B,a,Aa,b,Bb,Q,R,S0)

    if saveSS:
        SS.dirname = dirname_out
        filename_only = 'system_init.pickle'
        filename_out = os.path.join(dirname_out,filename_only)
        pickle_export(dirname_out, filename_out, SS)

    return SS




def gen_system_AB_rand(n=8,m=8,safety_margin=0.3):
    # Nominal system parameters
    A = randn(n,n)
    B = randn(n,m)

    # Normalize A such that max(abs(eig(A))) < 1
    # This way the system is open-loop stable so we can always find a
    # stabilizing controller i.e. zero gain

    # Force A to be open loop ~robustly stable i.e. safety margin > 0
    # Not good from a generalization standpoint but oh well for now

#    safety_margin = 0.30
    scale = (1-safety_margin)/np.max(np.abs(la.eig(A)[0]))
    A = A*scale

    return A,B


def gen_system_AB_erdos_renyi(n,dc=1.0,lc=0.05,fix_one_node=True,leaky=False,dirname_out='.'):

    crp = 7.0
    # ER probability
#    mean_degree = 5.0 # should be > 1 for giant component to exist
#    erp = mean_degree/(n+1.0-1.0)
    erp = (np.log(n+1)+crp)/(n+1) # almost surely connected prob=0.999
#    dc = 1.0 # Diffusion constant

    # Create random Erdos-Renyi graph
    if fix_one_node:
        adj = np.zeros([n+1,n+1])
        for i in range(n+1):
            for j in range(i+1,n+1):
                if rand() < erp:
                    adj[i,j] = 1
                    adj[j,i] = 1
        deg = np.diag(adj.sum(0))
        Ap1 = -dc*(deg-adj) # graph
        # Remove the first row and column to get rid of the zero eigenvalue
        A = Ap1[1:,1:]
        visualize_graph_ring(adj,n+1,dirname_out) # Plot
    else:
        adj = np.zeros([n,n])
        for i in range(n):
            for j in range(i+1,n):
                if rand() < erp:
                    adj[i,j] = 1
                    adj[j,i] = 1
        deg = np.diag(adj.sum(0))
        A = -dc*(deg-adj) # graph
        visualize_graph_ring(adj,n,dirname_out) # Plot
    if leaky:
        A = A - lc*np.eye(n)

    B = np.eye(n)
    C = np.eye(n)
    D = np.zeros([n,n])
    sysc = (A,B,C,D)
    sysd = scipy.signal.cont2discrete(sysc,dt=1,method='bilinear')
    A = np.array(sysd[0])
    B = np.array(sysd[1])
    return A,B




def visualize_graph_ring(adj,n,dirname_parent):
    fig,ax = plt.subplots()

    # Scatter plot all the center points
    t = np.arange(0,2*np.pi,2*np.pi/n)
    x = np.cos(t)
    y = np.sin(t)
    plt.scatter(x,y,s=50,alpha=1.0,zorder=21)
    plt.scatter(x[0],y[0],s=60,alpha=1.0,zorder=110,marker='s') # Highlight the reference node
    # Draw edge lines
    linecolor = (0.1,0.1,0.1)
    lines = []

    for i in range(n):
        for j in range(i+1,n):
            if adj[i,j] > 0:
                line = ((x[i],y[i]),(x[j],y[j]))
                lines.append(line)

    linecol = LineCollection(lines,linewidths=1,alpha=0.5,colors=linecolor,zorder=10)
    ax.add_collection(linecol)

    # Plot options
    plt.axis('scaled')
    plt.axis('equal')
    plt.axis('off')
    plt.ion()
    plt.show()

    dirname_out = os.path.join(dirname_parent,'network_images')
    create_directory(dirname_out)
    filename_out = 'network.png'
    path_out = os.path.join(dirname_out,filename_out)
    plt.savefig(path_out,dpi=300)
    plt.close()


def gen_system_example_suspension():
    n = 4
    m = 1

    m1 = 500
    m2 = 100
    k1 = 5000
    k2 = 20000
    b1 = 200
    b2 = 4000

    A = np.array([[0,1,0,0],
                  [-(b1*b2)/(m1*m2),0,((b1/m1)*((b1/m1)+(b1/m2)+(b2/m2)))-(k1/m1),-(b1/m1)],
                  [b2/m2,0,-((b1/m1)+(b1/m2)+(b2/m2)),1],
                  [k2/m2,0,-((k1/m1)+(k1/m2)+(k2/m2)),0]])

    B = 1000*np.array([[0],
                       [1/m1],
                       [0],
                       [(1/m1)+(1/m2)]])


    C = np.eye(n)
    D = np.zeros([n,m])

    sysc = (A,B,C,D)
    sysd = scipy.signal.cont2discrete(sysc,dt=0.5,method='bilinear')

    A = sysd[0]
    B = sysd[1]

    # Multiplicative noise data
    p = 4
    q = 1

    a = 0.1*np.ones(p)
    b = 0.2*np.ones(q)

    Aa = np.zeros([n,n,p])
    for i in range(p):
        Aa[:,i,i] = np.ones(n)


    Bb = np.zeros([n,m,q])
    for j in range(q):
        Bb[:,j,j] = np.ones(n)


    Q = np.eye(n)
    R = np.eye(m)
    S0 = np.eye(n)

    # Ensure near-critically mean square stabilizable - increase noise if not
    mss = False
    SS = LQRSysMult(A,B,a,Aa,b,Bb,Q,R,S0)

    while not mss:
        if SS.ccare < np.inf:
            mss = True
        else:
            a = a*0.95
            b = b*0.95
            SS = LQRSysMult(A,B,a,Aa,b,Bb,Q,R,S0)

    timestr = str(time()).replace('.','p')
    dirname_out = os.path.join('systems',timestr)
    SS.dirname = dirname_out
    filename_only = 'system_init.pickle'
    filename_out = os.path.join(dirname_out,filename_only)
    pickle_export(dirname_out, filename_out, SS)
    return SS


def gen_system_erdos_renyi(n, diffusion_constant=1.0, leakiness_constant=0.1, time_constant=0.05,
                               leaky=True, seed=None, detailed_outputs=False, dirname_out='.'):
    npr.seed(seed)
    timestr = str(time()).replace('.','p')
    dirname_out = os.path.join('systems', timestr)

    # ER probability
    # crp = 7.0
    # erp = (np.log(n+1)+crp)/(n+1)  # almost surely connected prob=0.999

    mean_degree = 4.0 # should be > 1 for giant component to exist
    erp = mean_degree/(n-1.0)

    n_edges = 0
    # Create random Erdos-Renyi graph
    # Adjacency matrix
    adjacency = np.zeros([n, n])
    for i in range(n):
        for j in range(i+1, n):
            if npr.rand() < erp:
                n_edges += 1
                adjacency[i, j] = npr.randint(low=1, high=4)
                adjacency[j, i] = np.copy(adjacency[i, j])

    # Degree matrix
    degree = np.diag(adjacency.sum(axis=0))
    # Graph Laplacian
    laplacian = degree-adjacency
    # Continuous-time dynamics matrices
    Ac = -laplacian*diffusion_constant
    Bc = np.eye(n)/time_constant # normalize just to make B = np.eye(n) later in discrete-time

    if leaky:
        Fc = leakiness_constant*np.eye(n)
        Ac = Ac - Fc

    # Plot
    visualize_graph_ring(adjacency, n, dirname_out)

    # Forward Euler discretization
    A = np.eye(n) + Ac*time_constant
    B = Bc*time_constant
    n = np.copy(n)
    m = np.copy(n)

    # Multiplicative noises
    a = 0.005*npr.randint(low=1, high=5, size=n_edges)*np.ones(n_edges)
    Aa = np.zeros([n, n, n_edges])
    k = 0
    for i in range(n):
        for j in range(i+1, n):
            if adjacency[i, j] > 0:
                Aa[i, i, k] = 1
                Aa[j, j, k] = 1
                Aa[i, j, k] = -1
                Aa[j, i, k] = -1
                k += 1

    b = 0.05*npr.randint(low=1, high=5, size=n)*np.ones(n)
    Bb = np.zeros([n, m, m])
    for i in range(n):
        Bb[i, i, i] = 1

    Q = np.eye(n)
    R = np.eye(m)
    S0 = np.eye(n)

    SS = LQRSysMult(A, B, a, Aa, b, Bb, Q, R, S0)
    SS.dirname = dirname_out
    filename_only = 'system_init.pickle'
    filename_out = os.path.join(dirname_out, filename_only)
    pickle_export(dirname_out, filename_out, SS)
    return SS


if __name__ == "__main__":
#    SS = gen_system_mult()

    # SS = gen_system_mult(n=50,m=8,safety_margin=0.3,noise='olmsus',
    #                 mult_noise_method='random',SStype='ER')

    SS = gen_system_erdos_renyi(n=4, seed=1)

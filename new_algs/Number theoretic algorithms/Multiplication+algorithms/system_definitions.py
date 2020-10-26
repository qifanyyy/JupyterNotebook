import numpy as np
import numpy.random as npr
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import os

from matrixmath import specrad, vec
from utility import create_directory


def random_system(n=2,m=1,seed=0):
    npr.seed(seed)
    A = npr.randn(n,n)
    A = A*0.8/specrad(A)
    B = npr.randn(n,m)
    SigmaA_basevec = 0.1*npr.randn(n*n)
    SigmaB_basevec = 0.1*npr.randn(n*m)
    SigmaA = np.outer(SigmaA_basevec, SigmaA_basevec)
    SigmaB = np.outer(SigmaB_basevec, SigmaB_basevec)
    return n, m, A, B, SigmaA, SigmaB


def example_system_scalar(Sa=0.5,Sb=0.5):
    n = 1
    m = 1
    A = np.array([[-0.5]])
    B = np.array([[1]])
    SigmaA = np.array([[Sa]])
    SigmaB = np.array([[Sb]])
    return n,m,A,B,SigmaA,SigmaB


def example_system_twostate():
    n = 2
    m = 1
    A = np.array([[-0.2, 0.3],
                  [-0.4, 0.8]])
    B = np.array([[-1.8],
                  [-0.8]])
    SigmaA = 0.1*np.array([[  0.8, -0.2,  0.0,  0.0],
                            [-0.2,  1.6,  0.2,  0.0],
                            [ 0.0,  0.2,  0.2,  0.0],
                            [ 0.0,  0.0,  0.0,  0.8]])
    SigmaB = 0.1*np.array([[ 0.5, -0.2],
                           [-0.2,  2.0]])
    return n,m,A,B,SigmaA,SigmaB

def example_system_twostate_diagonal():
    n = 2
    m = 2
    A = np.array([[-0.2, 0.3],
                  [-0.4, 0.8]])
    B = np.array([[-1.8, 0.3],
                  [-0.8, 0.6]])
    SigmaA = 0.1*np.eye(n*n)
    SigmaB = 0.1*np.eye(n*m)
    return n, m, A, B, SigmaA, SigmaB


def example_system_erdos_renyi(n, diffusion_constant=1.0, leakiness_constant=0.1, time_constant=0.05,
                               leaky=True, seed=None, detailed_outputs=False, dirname_out='.'):
    npr.seed(seed)
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
    varAi = 0.005*npr.randint(low=1, high=5, size=n_edges)*np.ones(n_edges)
    Ai = np.zeros([n_edges, n, n])
    k = 0
    for i in range(n):
        for j in range(i+1, n):
            if adjacency[i, j] > 0:
                Ai[k, i, i] = 1
                Ai[k, j, j] = 1
                Ai[k, i, j] = -1
                Ai[k, j, i] = -1
                k += 1

    varBj = 0.05*npr.randint(low=1, high=5, size=n)*np.ones(n)
    Bj = np.zeros([n, n, m])
    for i in range(n):
        Bj[i, i, i] = 1

    SigmaA = np.sum([varAi[i]*np.outer(vec(Ai[i]), vec(Ai[i])) for i in range(n_edges)], axis=0)
    SigmaB = np.sum([varBj[j]*np.outer(vec(Bj[j]), vec(Bj[j])) for j in range(n)], axis=0)

    if detailed_outputs:
        outputs = n, m, A, B, SigmaA, SigmaB, varAi, varBj, Ai, Bj
    else:
        outputs = n, m, A, B, SigmaA, SigmaB

    return outputs

def visualize_graph_ring(adj, n, dirname_parent):

    fig, ax = plt.subplots(figsize=(4, 4))

    # Scatter plot all the center points
    t = np.arange(0,2*np.pi,2*np.pi/n)
    x = np.cos(t)
    y = np.sin(t)
    plt.scatter(x, y, s=600, alpha=1.0, zorder=21)
    # plt.scatter(x[0],y[0],s=60,alpha=1.0,zorder=110,marker='s') # Highlight the reference node
    # Draw edge lines
    linecolor = (0.1,0.1,0.1)
    lines = []
    linewidths = []

    for i in range(n):
        for j in range(i+1,n):
            if adj[i,j] > 0:
                line = ((x[i],y[i]),(x[j],y[j]))
                lines.append(line)
                linewidths.append(4*adj[i,j])

    linecol = LineCollection(lines,linewidths=linewidths,alpha=0.5,colors=linecolor,zorder=10)
    ax.add_collection(linecol)

    # Plot options
    plt.axis('scaled')
    plt.axis('equal')
    plt.axis('off')
    plt.ion()
    plt.tight_layout()
    plt.show()

    dirname_out = os.path.join(dirname_parent,'network_images')
    create_directory(dirname_out)
    filename_out = 'network.png'
    path_out = os.path.join(dirname_out,filename_out)
    plt.savefig(path_out,dpi=300)
    plt.close()

if __name__ == "__main__":
    n, m, A, B, SigmaA, SigmaB = example_system_erdos_renyi(n=10)
    plt.imshow(SigmaA)
"""
The example 01 solve the problem of Nearest Neighbors Problem with the next conditions:
a) Distribution of points in domain
    a1) Normal Gaussian Distribution points (ngd)
    a2) Regular Distribution points (rdp)
b) Algorithm of Searching NN:
    b1) kNN brute Force with K-D Tree (bf)
    b2) Ball Tree with K-D Tree (bt)
    b4) Nearest Centroid
c) The shape of the Mesh: By Default is rectangle, but it's possible make others shapes


@autor: Leonardo Ledesma Domínguez
Creation date: 27/05/2018
Modification date: 06/05/2018 add Laplace equation
"""

# ----------------------------------------------------------------------------------------
# Library Imports
# ----------------------------------------------------------------------------------------

import Domain as dm
import Distribution as dt
import Neighbor as nb
import matplotlib.pyplot as plt
import time
import warnings
import numpy as np
from RBF import Multiquadric2D
from RBF import GrammMatrix
from RBF import Solver
from RBF import CS_RBF2D
from Plotter import plotter

# ----------------------------------------------------------------------------------------
# Painter Function
# ----------------------------------------------------------------------------------------

def painter(neighborhood):
    #bandera = 0
    for key in neighborhood:
        #if bandera == 10:
        # print(key, neighborhood[key])
        for ng in neighborhood[key]:
            x1 = key[0]
            x2 = ng[0][0]
            xp = [x1, x2]
            y1 = key[1]
            y2 = ng[0][1]
            yp = [y1, y2]
            plt.plot(xp, yp, '-')
        #bandera += 1


def main():
    # ----------------------------------------------------------------------------------------
    # Attributes of Mesh
    # the value dp  is result of equation w(dp) * h(dp) = num_nodes
    # you have to change this value manually in order to have the same number of node
    # ----------------------------------------------------------------------------------------

    width = 2
    height = 4
    num_nodes = 200
    dp = 5
    radius = 1.0
    D = 1
    T1 = 100

    # ----------------------------------------------------------------------------------------
    # Create Domain Regular
    # ----------------------------------------------------------------------------------------

    d1 = dm.Domain(width, height)
    d1.createSquare(dp=dp)
    xd1 = d1.nodes_x()
    yd1 = d1.nodes_y()
    dst = dt.Distribution(domain=d1, dp=dp)

    # ----------------------------------------------------------------------------------------
    # show boundary of Domain
    # ----------------------------------------------------------------------------------------

    fig, ax = plt.subplots(nrows=1, ncols=1)
    plt.plot(d1.nodes_x()[0][0], d1.nodes_y()[0][0])
    plt.plot(d1.nodes_x()[1][0], d1.nodes_y()[1][0])
    plt.plot(d1.nodes_x()[2][0], d1.nodes_y()[2][0])
    plt.plot(d1.nodes_x()[3][0], d1.nodes_y()[3][0])

    # ----------------------------------------------------------------------------------------
    # Make the knots of Domain: ngd (gaussian distribution) or rdp (regular)
    # ----------------------------------------------------------------------------------------

    dst.calcDist(shape='ngd', nodes=num_nodes, width=width, height=height, bx=d1.nodes_x(), by=d1.nodes_y(), dp=dp)
    #dst.calcDist(shape='rdp', width=width, height=height, bx=xd1, by=yd1, dp=dp, nodes=num_nodes)

    # ----------------------------------------------------------------------------------------
    # Kernel selection
    # ----------------------------------------------------------------------------------------

    kernel = Multiquadric2D(1/np.sqrt(dst.nodes()))

    # ----------------------------------------------------------------------------------------
    # Gramm matrix allocation
    # ----------------------------------------------------------------------------------------

    matrix = GrammMatrix(dst)
    matrix.fillMatrixLaplace2D(kernel, D)

    # ----------------------------------------------------------------------------------------
    # Dirichlet boundary condition
    # ----------------------------------------------------------------------------------------

    matrix.setDirichletRegular(T1, 3)
    # print(dst.NI(), dst.NB(), test[dst.NI():], len(test[dst.NI():]), len(test[0:dst.NI()]))

    # ----------------------------------------------------------------------------------------
    # Gram matrix solution
    # ----------------------------------------------------------------------------------------

    solv = Solver(matrix, 'linalg')
    solv.solve()
    solv.evaluate(kernel)

    # ----------------------------------------------------------------------------------------
    # Solution storage(optional)
    # ----------------------------------------------------------------------------------------

    zx = solv.interpolate(kernel)
    u = solv.getSol()
    lam = solv.lam()

    # ----------------------------------------------------------------------------------------
    # Solution and point cloud plotting
    # ----------------------------------------------------------------------------------------
    title = 'Heat difussion in two dimensional domain'
    xlabel = 'Lx [m]'
    ylabel = 'Ly [m]'
    barlabel = 'Temparature °C'
    plot = plotter (solv, kernel)
    # plot.regularMesh2D (title='Spatial created grid', xlabel=xlabel, ylabel=ylabel)
    plot.surface3D (title=title, xlabel=xlabel, ylabel=ylabel, barlabel=barlabel)
    plot.levelplot (title=title, xlabel=xlabel, ylabel=ylabel, barlabel=barlabel)

    plt.spy (matrix.getMatrix (), markersize=1.0)
    plt.show ()


    # ----------------------------------------------------------------------------------------
    # Select the search method and time of execution
    # ----------------------------------------------------------------------------------------
    nn = nb.Neighbor (method='bf', x=dst.a (), y=dst.b (), r=radius)
    neighborhood = nn.nearest_neighbors ()
    nn = nb.Neighbor (method='bt', x=dst.a (), y=dst.b (), r=radius)
    neighborhood = nn.nearest_neighbors ()
    nn = nb.Neighbor(method='ball', x=dst.a(), y=dst.b(), r=radius)
    neighborhood = nn.nearest_neighbors()
    #print (neighborhood)
    #print (nn.location())
    start_time = time.time()
    painter(neighborhood)
    print("Painter Time in NN method:")
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Data Domain")
    print('_' * 20)
    print("number points: ", len(dst.a()))
    plt.scatter(dst.a(), dst.b())
    plt.grid()
    plt.axis([-2, width+2, -1, height+1])
    warnings.filterwarnings("ignore")
    #ax.set_axis_bgcolor("lightslategray")
    plt.show()

    # ----------------------------------------------------------------------------------------
    # Gramm matrix allocation with NN
    # ----------------------------------------------------------------------------------------

    matrixNN = GrammMatrix (dst)
    matrixNN.fillMatrixLapace2D_CSupported (kernel, D,nn.location())

    # ----------------------------------------------------------------------------------------
    # Dirichlet boundary condition
    # ----------------------------------------------------------------------------------------

    matrixNN.setDirichletRegular (T1, 3)
    # print(dst.NI(), dst.NB(), test[dst.NI():], len(test[dst.NI():]), len(test[0:dst.NI()]))

    # ----------------------------------------------------------------------------------------
    # Gram matrix solution with NN
    # ----------------------------------------------------------------------------------------

    solvnn = Solver (matrixNN, 'linalg')
    solvnn.solve ()
    solvnn.evaluate (kernel)
    # ----------------------------------------------------------------------------------------
    # Solution storage(optional)
    # ----------------------------------------------------------------------------------------

    zx = solvnn.interpolate (kernel)
    u = solvnn.getSol ()
    lam = solvnn.lam ()

    # ----------------------------------------------------------------------------------------
    # Solution and point cloud plotting
    # ----------------------------------------------------------------------------------------
    title = 'Heat difussion in two dimensional domain'
    xlabel = 'Lx [m]'
    ylabel = 'Ly [m]'
    barlabel = 'Temparature °C'
    plot = plotter (solvnn, kernel)
    # plot.regularMesh2D (title='Spatial created grid', xlabel=xlabel, ylabel=ylabel)
    plot.surface3D (title=title, xlabel=xlabel, ylabel=ylabel, barlabel=barlabel)
    plot.levelplot (title=title, xlabel=xlabel, ylabel=ylabel, barlabel=barlabel)

    plt.spy (matrixNN.getMatrix (), markersize=1.0)
    plt.show ()

    print(matrixNN.N(), matrixNN.NI())




main()

__author__ = 'AlexLlamas'
import numpy as np
from matplotlib import gridspec
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
from CorrelationMesures import *
from pandas import *

class Samples:

    def __init__(self, tipo=-1):
        self.tipo = tipo
        return

    def get(self, numberSam, noise):
        if self.tipo == 0:
            return self.get_sin(numberSam, noise)

        elif self.tipo == 1:
            return self.get_square(numberSam, noise)

        elif self.tipo == 2:
            return self.get_blur(numberSam, noise)

        elif self.tipo == 3:
            return self.get_cuadratic(numberSam, noise)

        elif self.tipo == 4:
            return self.get_diagonal_line(numberSam, noise)

        elif self.tipo == 5:
            return self.get_horizontal_line(numberSam, noise)

        elif self.tipo == 6:
            return self.get_vertical_line(numberSam, noise)

        elif self.tipo == 7:
            return self.get_x(numberSam, noise)

        elif self.tipo == 8:
            return self.get_circle(numberSam, noise)

        elif self.tipo== 9:
            return self.get_curve_x(numberSam, noise)

        elif self.tipo == 10:
            return self.get_diagonal_line2(numberSam, noise)

        elif self.tipo == 11:
            return self.get_dependent(numberSam)

        elif self.tipo == 12:
            return self.get_independent(numberSam)

        elif self.tipo == 13:
            return self.get_corr(numberSam, noise)

        elif self.tipo == 14:
            return self.get_file()

        else:
            print 'Error'

    @staticmethod
    def get_file():
        #data = read_csv('Data\X-Y-Independientes.txt')
        data = read_csv('Data\ejemplo.csv')
        z = np.zeros((data.shape[0],2))
        # order X,W,Y,Z,T
        z[:,0] = np.array(data.ix[:,0])
        z[:,1] = np.array(data.ix[:,2])
        return z

    @staticmethod
    def get_sin(numSamples, noise):
        x = np.linspace(-10,10,numSamples)
        y = np.random.normal(np.sin(x), noise)
        z = np.zeros((numSamples,2))
        z[:,0] = x
        z[:,1] = y
        return z

    @staticmethod
    def get_square(numSamples, noise):
        x = np.random.uniform(-10,10,numSamples)
        y = np.random.uniform(-10,10,numSamples)
        z = np.zeros((numSamples,2))
        z[:,0] = x
        z[:,1] = y
        return z

    @staticmethod
    def get_blur(numSamples, noise):
        mean = [0,0]
        cov = [[noise, 0],[0, noise]]
        x, y = np.random.multivariate_normal(mean, cov, numSamples).T
        z = np.zeros((numSamples,2))
        z[:,0] = x
        z[:,1] = y
        return z

    @staticmethod
    def get_cuadratic(numSamples, noise):
        x = np.linspace(-10,10,numSamples)
        y = np.random.normal(np.power(x,2), noise)
        z = np.zeros((numSamples,2))
        z[:,0] = x
        z[:,1] = y
        return z

    @staticmethod
    def get_diagonal_line(numSamples, noise):
        x = np.linspace(-10,10,numSamples)
        y = np.random.normal(x, noise)
        z = np.zeros((numSamples,2))
        z[:,0] = x
        z[:,1] = y
        return z

    @staticmethod
    def get_horizontal_line(numSamples, noise):
        x = np.linspace(-10,10,numSamples)
        y = np.random.normal((x-x), noise)
        z = np.zeros((numSamples,2))
        z[:,0] = x
        z[:,1] = y
        z[0,0], z[0,1] = -10, -10
        z[1,0], z[1,1] = 10, 10
        return z

    @staticmethod
    def get_vertical_line(numSamples, noise):
        x = np.linspace(-10,10,numSamples)
        y = np.random.normal((x-x), noise)
        z = np.zeros((numSamples,2))
        z[:,0] = y
        z[:,1] = x
        z[0,0], z[0,1] = -10, -10
        z[1,0], z[1,1] = 10, 10
        return z

    @staticmethod
    def get_x(numSamples, noise):
        x = np.linspace(-10,10,numSamples/2)
        y1 = np.random.normal(x, noise)
        y2 = np.random.normal(-x, noise)
        z = np.zeros((numSamples,2))
        z[:,0] = np.concatenate((x,x),axis=0)
        z[:,1] = np.concatenate((y1,y2),axis=0)
        return z

    @staticmethod
    def get_circle(numSamples, noise):
        x = np.linspace(-4,4,numSamples/2)
        y1 = np.random.normal(np.sqrt(16-np.power(x,2)), noise)
        y2 = -np.random.normal(np.sqrt(16-np.power(x,2)), noise)
        z = np.zeros((numSamples,2))
        z[:,0] = np.concatenate((x,x),axis=0)
        z[:,1] = np.concatenate((y1,y2),axis=0)
        return z

    @staticmethod
    def get_curve_x(numSamples, noise):
        x = np.linspace(-10,10,numSamples/2)
        y1 = np.random.normal(np.power(x, 2), noise)
        y2 = -np.random.normal(np.power(x, 2), noise)
        z = np.zeros((numSamples,2))
        z[:,0] = np.concatenate((x,x),axis=0)
        z[:,1] = np.concatenate((y1,y2),axis=0)
        return z

    @staticmethod
    def get_diagonal_line2(numSamples, noise):
        x = np.linspace(-10,10,numSamples)
        y = np.random.normal(-x, noise)
        z = np.zeros((numSamples,2))
        z[:,0] = x
        z[:,1] = y
        return z

    @staticmethod
    def get_dependent(numSamples):
        x = np.linspace(-10,10,numSamples)
        y = np.linspace(-10,10,numSamples)
        z = np.zeros((numSamples,2))
        z[:,0] = x
        z[:,1] = y
        return z


    @staticmethod
    def get_independent(numSamples):
        z = np.zeros((numSamples*numSamples,2))
        for i in range(0, numSamples):
            for j in range(0, numSamples):
                z[i*numSamples + j, 0] = i
                z[i*numSamples + j, 1] = j
        return z

    @staticmethod
    def get_corr(numSamples, p=0.8):
        u = np.random.uniform(-10,10,numSamples)
        v = np.random.uniform(-10,10,numSamples)
        x = u
        y = p*u + math.sqrt(1-math.pow(p,2))*v
        z = np.zeros((numSamples,2))
        z[:,0] = x
        z[:,1] = y
        return z

    @staticmethod
    def plot_partition(samples, numBinx, numBiny):
        # Plot the histogram of the samples structure

        x, y = samples[:,0], samples[:,1]
        H, xedges, yedges = np.histogram2d(y, x, bins=(numBinx, numBiny))
        X, Y = np.meshgrid(xedges, yedges)
        fig5 = plt.figure(5)
        plt.pcolormesh(X, Y, H)
        fig5.show()


    @staticmethod
    def plot_propose(samples, numBinx):
        # Calcula el valor de la dependecia mutua para diferentes Grids ixi
        # este calculo no mantiene la significancia al cambiar el tamano del Grid.
        # use numbinx to define the max i in the for loop

        x, y = samples[:,0], samples[:,1]
        PMD = np.zeros(numBinx)
        for i in range(2, numBinx):
            PMD[i] = propuesta_mutual_dependency(x, y, i, i)

        fig4 = plt.figure(4)
        plt.plot(PMD)
        plt.xlabel('Grid size ixi')
        plt.ylabel('Mutual dependency uniform')
        fig4.show()

    def plot_compare2(self, maxBinx, maxBiny, noise, step):
        # 3d plot
        # compara diferentes tipos de Grid MANTENIENDO la significancia

        sig = 0.95  # significancia
        v = 10 # muestras por bloque deseadas 5 para squere
        samPerBlock =  (v*sig)/math.sqrt(1-math.pow(sig,2))

        size = maxBinx*maxBiny
        xp = np.zeros(size)
        yp = np.zeros(size)

        nmi = np.zeros(size)
        md = np.zeros(size)
        md2 = np.zeros(size)

        max_md2 = 0.0
        max_md = 0.0
        for i in range(2, maxBinx, step):
            for j in range(2, maxBiny, step):
                numSamples = int(i*j*samPerBlock)
                samples = self.get(numSamples, noise)
                x, y = samples[:,0], samples[:,1]
                pos = i*maxBiny + j

                xp[pos] = i
                yp[pos] = j

                nmi[pos] = norm_MI(x, y, i, j)
                md[pos] = propuesta_mutual_dependency(x, y, i, j)
                if md[pos] > max_md:
                    max_md = md[i*maxBiny + j]
                md2[pos] = propuesta2_mutual_dependency(x, y, i, j)
                if md2[pos] > max_md2:
                    max_md2 = md[pos]

        print 'Maximal Mutual dependency: ' + str(max_md)
        print 'Maximal Mutual dependency: ' + str(max_md)

        fig2 = plt.figure(2)
        axi1 = fig2.gca(projection='3d')
        axi1.plot_trisurf(xp, yp, md, cmap=cm.jet, linewidth=0.2)
        plt.title('Uniform Mutual Dependency (UMD)')
        plt.xlabel('Number of bins in X')
        plt.ylabel('Number of bins in Y')
        fig2.show()

        fig6 = plt.figure(6)
        axi2 = fig6.gca(projection='3d')
        axi2.plot_trisurf(xp, yp, md2, cmap=cm.jet, linewidth=0.2)
        plt.title('Comparative Mutual Dependency (CMD)')
        fig6.show()

        fig3 = plt.figure(3)
        axi2 = fig3.gca(projection='3d')
        axi2.plot_trisurf(xp, yp, nmi, cmap=cm.jet, linewidth=0.2)
        plt.title('Mutual Information (MI)')
        fig3.show()

    """
    @staticmethod
    def plot_compare(samples, numBinx, numBiny, step):
        # 3d plot
        # compara diferentes dimensiones de Grid con el mismo nuemro de muestras. es decir sin mantener la significancia.

        x, y = samples[:,0], samples[:,1]
        xp = np.zeros(numBinx*numBiny)
        yp = np.zeros(numBinx*numBiny)
        nmi = np.zeros(numBinx*numBiny)
        md = np.zeros(numBinx*numBiny)
        md2 = np.zeros(numBinx*numBiny)
        max_md2 = 0.0
        max_md = 0.0
        for i in range(2, numBinx, step):
            for j in range(2, numBiny, step):
                xp[i*numBiny + j] = i
                yp[i*numBiny + j] = j
                nmi[i*numBiny + j] = norm_MI(x, y, i, j)
                md[i*numBiny + j] = propuesta_mutual_dependency(x, y, i, j)
                if md[i*numBiny + j] > max_md:
                    max_md = md[i*numBiny + j]
                md2[i*numBiny + j] = propuesta2_mutual_dependency(x, y, i, j)
                if md2[i*numBiny + j] > max_md2:
                    max_md2 = md[i*numBiny + j]

        print 'Maximal Mutual dependency: ' + str(max_md)
        print 'Maximal Mutual dependency: ' + str(max_md)

        fig2 = plt.figure(2)
        axi1 = fig2.gca(projection='3d')
        axi1.plot_trisurf(xp, yp, md, cmap=cm.jet, linewidth=0.2)
        plt.title('Propose mutual dependency')
        fig2.show()

        fig3 = plt.figure(3)
        axi2 = fig3.gca(projection='3d')
        axi2.plot_trisurf(xp, yp, nmi, cmap=cm.jet, linewidth=0.2)
        plt.title('Mutual information')
        fig3.show()

        fig6 = plt.figure(6)
        axi2 = fig6.gca(projection='3d')
        axi2.plot_trisurf(xp, yp, md2, cmap=cm.jet, linewidth=0.2)
        plt.title('Propose mutual dependency 2')
        fig6.show()
    """

    @staticmethod
    def plot_sample(samples, numBinx, numBiny, step):
        x, y = samples[:,0], samples[:,1]
        fig = plt.figure(1)
        gs = gridspec.GridSpec(4,4)
        ax1 = fig.add_subplot(gs[:3, :3])
        ax1.scatter(x, y, color='blue')
        ax1.set_yticklabels([])
        ax1.set_xticklabels([])
        ax1.set_xlabel('X axis')
        ax1.set_ylabel('Y axis')
        ax2 = fig.add_subplot(gs[3,:3])
        ax2.hist(x, numBinx, facecolor='g')
        ax2.set_xticklabels([])
        ax2.yaxis.set_visible(False)
        ax2.set_xlabel('Histogram of X')
        ax3 = fig.add_subplot(gs[:3, 3])
        ax3.hist(y, numBiny, orientation='horizontal', facecolor='g')
        ax3.set_yticklabels([])
        ax3.xaxis.set_visible(False)
        ax3.set_ylabel('Histogram of Y')
        """
        ax4 = fig.add_subplot(gs[3, 3])
        H, xedges, yedges = np.histogram2d(y, x, bins=(numBinx, numBiny))
        X, Y = np.meshgrid(xedges, yedges)
        ax4.pcolormesh(X, Y, H)
        ax4.set_aspect('equal')
        ax4.xaxis.set_visible(False)
        ax4.yaxis.set_visible(False)
        """
        gs.update(wspace=0.5, hspace=0.5)
        fig.show()
        H, xedges, yedges = np.histogram2d(y, x, bins=(numBinx, numBiny))
        print str(H)























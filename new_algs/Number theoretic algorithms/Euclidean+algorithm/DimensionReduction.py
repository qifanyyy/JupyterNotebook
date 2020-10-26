from TPC_Config import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from time import gmtime, strftime
from sklearn import manifold

import logging


class Reduction:

    def __init__(self, plot_path):
        self.edm = []
        self.edm_distribution = []
        self.plot_path = plot_path
        self.time = 0
        logging.info('Beginning Dimensional Reduction')


    def save_edm_distribution(self,time):
        np.save(self.plot_path+time+'/EDM_Distribution', self.edm_distribution)

    def load_edm(self, time):
        # self.time = time
        self.edm = np.array(np.load(self.plot_path+time+'/'+'EDM.npy'))

    def sklearn_mds(self):
        logging.info('Reconstructed with MDS')
        seed = np.random.RandomState(seed=3)
        nmds = manifold.MDS(n_components=2, metric=False, max_iter=2000, eps=1e-12,
                            dissimilarity="precomputed", random_state=seed, n_jobs=1,
                            n_init=5)

        mds = manifold.MDS(n_components=2, max_iter=2000, eps=1e-12, random_state=seed,
                           dissimilarity="precomputed", n_jobs=1,n_init = 10)
        npos = mds.fit_transform(self.edm) #.embedding_

        # pos = mds.fit(self.edm).embedding_
        # npos = nmds.fit_transform(self.edm, init=pos)

        plt.figure(figsize=(10, 10))
        plt.scatter(npos[:, 0], npos[:, 1], color='darkorange', lw=0, label='NMDS')
        plt.title('MDS Recon')
        plt.savefig(self.plot_path+'MDS' + strftime("%m_%d_%H:%M:%S", gmtime()) + '.png')

        self.edm_distribution = npos

    def sklearn_nmds(self):
        logging.info('Reconstructed with NMDS')
        seed = np.random.RandomState(seed=3)
        nmds = manifold.MDS(n_components=2, metric=False, max_iter=2000, eps=1e-12,
                            dissimilarity="precomputed", random_state=seed, n_jobs=1,
                            n_init=5)

        mds = manifold.MDS(n_components=2, max_iter=2000, eps=1e-12, random_state=seed,
                           dissimilarity="precomputed", n_jobs=1,n_init = 10)

        pos = mds.fit(self.edm).embedding_
        npos = nmds.fit_transform(self.edm, init=pos)

        plt.figure(figsize=(10, 10))
        plt.scatter(npos[:, 0], npos[:, 1], color='darkorange', lw=0, label='NMDS')
        plt.title('NMDS Recon')
        plt.savefig(self.plot_path+'NMDS' + strftime("%m_%d_%H:%M:%S", gmtime()) + '.png')

        self.edm_distribution = npos

    def sklearn_iso(self, n_neighbors):
        logging.info('Reconstructed with Isomap')

        model = manifold.Isomap(n_neighbors=n_neighbors, n_components=2,
                                                eigen_solver='dense')
        out = model.fit_transform(self.edm)
        plt.figure(figsize=(10,10))
        plt.scatter(out[:, 0], out[:, 1], color='darkorange', lw=0, label='NMDS')
        plt.title('IsoMap Recon')
        plt.savefig(self.plot_path+'ISO' + strftime("%m_%d_%H:%M:%S", gmtime()) + '.png')

        self.edm_distribution = out

    def sklearn_local_linear(self, n_neighbors):
        logging.info('Reconstructed with LLE')
        model = manifold.LocallyLinearEmbedding(n_neighbors=n_neighbors, n_components=2,
                                       eigen_solver='dense')

        out = model.fit_transform(self.edm)
        plt.figure(figsize=(10, 10))
        plt.scatter(out[:, 0], out[:, 1], color='darkorange', lw=0, label='NMDS')
        plt.title('LLE Recon')
        plt.savefig(self.plot_path + 'LLE' + strftime("%m_%d_%H:%M:%S", gmtime()) + '.png')

        self.edm_distribution = out

    def get_distribution(self):
        return self.edm_distribution

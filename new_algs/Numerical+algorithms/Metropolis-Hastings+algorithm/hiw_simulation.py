# -*- coding: utf-8 -*-
# Author : xiequanbin
# Date:  18-05-30
# Email:  xquanbin072095@gmail.com

"""
 Samples the HIW(delta, phi) distribution on a graph G on p nodes，
 for details, see carlos, "Simulation of Hyper-Inverse Wishart Distributions in Graphical Models".
"""

import time
import numpy as np
from scipy.stats import invwishart, multivariate_normal


def get_seperators(sorted_cliques):
    clique_num = len(sorted_cliques)
    seperators = [[]]
    for i in range(1, clique_num):
        temp_set = set([])
        for j in range(0, i):
            temp_set = temp_set | set(sorted_cliques[j])
        seperators.append(sorted(list(temp_set & set(sorted_cliques[i]))))

    return seperators


def hiw_sim(cliques, delta, phi, sample_num):
    # set a random seed
    np.random.seed(12345)

    p = len(phi)
    clique_num = len(cliques)
    seperators = get_seperators(cliques)

    # initializing the array will be returned
    sigma = np.zeros([sample_num, p, p])
    omega = np.zeros([sample_num, p, p])

    # MC sampling
    c1 = cliques[0]
    for n in range(0, sample_num):
        sigma_n = np.zeros([p, p])
        sigma_n[np.ix_(c1, c1)] = invwishart.rvs(delta + len(c1) - 1, phi[np.ix_(c1, c1)])

        for i in range(1, clique_num):
            c_id = cliques[i]
            s_id = seperators[i]
            R_i = list(set(c_id) - set(s_id))

            DS_i = np.linalg.inv(phi[np.ix_(s_id, s_id)])
            DRS_i = phi[np.ix_(R_i, R_i)] - np.dot(np.dot(phi[np.ix_(R_i, s_id)], DS_i), phi[np.ix_(s_id, R_i)])
            DRS_i = (DRS_i + DRS_i.T) / 2.
            mu_i = np.dot(phi[np.ix_(R_i, s_id)], DS_i)

            sigmaRS_i = invwishart.rvs(delta + len(c_id) - 1, DRS_i)
            if len(R_i) * len(s_id):
                U_i = multivariate_normal.rvs(np.reshape(mu_i, len(R_i) * len(s_id)), np.kron(sigmaRS_i, DS_i))
                sigma_n[np.ix_(R_i, s_id)] = np.dot(np.reshape(U_i, (len(R_i), -1)), sigma_n[np.ix_(s_id, s_id)])
                sigma_n[np.ix_(s_id, R_i)] = sigma_n[np.ix_(R_i, s_id)].T
            else:
                sigma_n[np.ix_(R_i, s_id)] = np.dot(np.zeros([len(R_i), len(s_id)]), sigma_n[np.ix_(s_id, s_id)])
                sigma_n[np.ix_(s_id, R_i)] = sigma_n[np.ix_(R_i, s_id)].T

            sigma_n[np.ix_(R_i, R_i)] = sigmaRS_i + np.dot(np.dot(sigma_n[np.ix_(R_i, s_id)],
                                                                  np.linalg.inv(sigma_n[np.ix_(s_id, s_id)])),
                                                           sigma_n[np.ix_(s_id, R_i)])

        # completion operation for sampled variance matrix
        H = c1
        for i in range(1, clique_num):
            c_id = cliques[i]
            s_id = seperators[i]
            R_i = list(set(c_id) - set(s_id))
            A_i = list(set(H) - set(s_id))
            sigma_n[np.ix_(R_i, A_i)] = np.dot(np.dot(sigma_n[np.ix_(R_i, s_id)],
                                                      np.linalg.inv(sigma_n[np.ix_(s_id, s_id)])),
                                               sigma_n[np.ix_(s_id, A_i)])
            sigma_n[np.ix_(A_i, R_i)] = sigma_n[np.ix_(R_i, A_i)].T
            H = list(set(c_id) | set(H))

        sigma[n] = sigma_n

        # computing the corresponding sampled precision matrix
        caux = np.zeros([clique_num, p, p])
        saux = np.zeros([clique_num, p, p])
        caux[0][np.ix_(c1, c1)] = np.linalg.inv(sigma_n[np.ix_(c1, c1)])
        for i in range(1, clique_num):
            c_id = cliques[i]
            s_id = seperators[i]
            caux[i][np.ix_(c_id, c_id)] = np.linalg.inv(sigma_n[np.ix_(c_id, c_id)])
            saux[i][np.ix_(s_id, s_id)] = np.linalg.inv(sigma_n[np.ix_(s_id, s_id)])

        omega[n] = np.sum(caux, axis=0) - np.sum(saux, axis=0)
        # print"{} sample(s) have been drawn!".format(n+1)
    # End of sampling

    return sigma, omega


if __name__ == "__main__":

    # a example
    # load test data
    data = np.loadtxt('./input/test_data.txt')
    (T, p) = data.shape

    # assume sigma is subjected to HIW(delta, phi)
    delta = 3
    tau = 0.0001
    rho = 0
    mh_steps = 1000
    beta = 2. / (p - 1)
    phi = tau * rho * (np.ones([p, p]) - np.eye(p)) + tau * np.eye(p)

    # draw a graph using metropolis-hasting algorithm and get a perfect ordering of cliques
    import metropolis as mt
    import networkx as nx
    G = mt.metropolis_hastings(data, delta, tau, rho, mh_steps)
    cliques = list(nx.find_cliques(G))
    sorted_cliques_ = mt.get_perfect_ordering_of_cliques(G, cliques)

    """
    # a perfect ordering of cliques
    sorted_cliques_ = [[0, 1, 8], [1, 3, 6, 8, 10], [1, 4, 6, 8, 10], [1, 3, 6, 8, 14], [4, 6, 10, 11], 
                       [2, 4, 8], [4, 5, 10], [3, 9, 10], [8, 10, 12], [0, 7], [12, 13]]
    """

    # the post distribution of sigma is HIW(delta + T, phi + data.T * data), draw 1000 samples from it
    start_time = time.time()
    post_delta = delta + T
    post_phi = phi + np.dot(data.T, data)
    test_sigma, test_omega = hiw_sim(sorted_cliques_, post_delta, post_phi, 1000)
    end_time = time.time()
    print "time cost: {}s".format(round(end_time - start_time, 2))

    mean_sigma = np.mean(test_sigma, axis=0)
    print "the mean of 1000 covariance samples:\n", mean_sigma   # the true covariance is np.cov(data.T)
    mean_omega = np.mean(test_omega, axis=0)
    print "\n"
    print "the mean of 1000 precision matrix samples:\n", mean_omega

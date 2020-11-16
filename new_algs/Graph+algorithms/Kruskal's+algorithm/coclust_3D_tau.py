import logging
from random import choice
from random import randint
from time import time
from typing import List

import numpy as np
import scipy
from scipy.sparse import issparse
from sklearn.base import BaseEstimator
from sklearn.base import ClusterMixin
from sklearn.base import TransformerMixin
from sklearn.utils import check_array


class CoClust(BaseEstimator, ClusterMixin, TransformerMixin):
    """
    CoClust is a co-clustering algorithm created to deal with 3D-tensor data.
    It finds automatically the best number of row / column / slice clusters.

    Parameters
    ------------

    n_iterations : int, optional, default: 300
        The number of iterations to be performed.

    optimization strategy: {'ALT', 'AVG', 'AGG', 'ALT2', 'AGG2'}, optional, default: 'ALT2'
        The version of the algorithm. The possible values are:
            

    min_n_x_clusters : int, optional, default: 2,
        The number of clusters for the first mode, should be at least 2

    min_n_y_clusters : int, optional, default: 2,
        The number of clusters for the second mode, should be at least 2

    min_n_z_clusters : int, optional, default: 2,
        The number of clusters for the third mode, should be at least 2

    n_threshold : int, optional, default: 0,
        The number of iterations without moves after which the object selection strategy changes.
        If 0, the number is set equal to the dimension of the highest-dimensional mode

    path : string, optional, default: None,
        If a path is specified, the algorithm prints in the specified path a file every 100 iterations containing
        the partial results.

    compute_tau_list : boolean, optional, default : False,
        If True, the value of taus after each iteration is saved in a parameter "tau_vector_".
    

    Attributes
    -----------

    x_ : array, length dimension on the first mode
        Results of the clustering on x mode. `x_[i]` is `c` if
        object `i` is assigned to cluster `c`. Available only after calling ``fit``.

    y_ : array, length dimension on the second mode
        Results of the clustering on y mode. `y_[i]` is `c` if
        object `i` is assigned to cluster `c`. Available only after calling ``fit``.

    z_ : array, length dimension on the third mode
        Results of the clustering on z mode. `z_[i]` is `c` if
        object `i` is assigned to cluster `c`. Available only after calling ``fit``.

    execution_time_ : float
        The execution time.

    initial_tau_ : tuple, length 3
        Initial values of tau_x, tau_y, tau_z, when the co-clustering is
        the discrete one. Available only after calling ``fit``.

    final_tau_ : tuple, length 3
        Values of tau_x, tau_y, tau_z corresponding to the final
        co-clustering solution. Available only after calling ``fit``.

    tau_vector_ : list, length actual number of iterations
        values of (tau_x, tau_y, tau_Z) after each iteration. Available only if compute_tau_list == True.



    References
    ----------

    * Battaglia, Pensa: A parameter-less algorithm for tensor co-clustering.

    """

    def __init__(self, n_iterations=500, optimization_strategy = 'ALT2', min_n_x_clusters=2, min_n_y_clusters=2, min_n_z_clusters=2, n_threshold = 0, path = None, compute_tau_list = False):
        """
        Create the model object and initialize the required parameters.

        :type n_iterations: int
        :param n_iterations: the max number of iterations to perform
        :type optimization_strategy: string, one of {'ALT', 'AVG', 'AGG', 'ALT2', 'AGG2'}
        :param optimization_strategy: version of the algorithm
        :type min_n_x_clusters, min_y_clusters, min_z_clusters: int
        :param min_n_x_clusters, min_n_y_clusters, min_n_z_clusters: the minimum number of clusters (per mode)
        :type n_threshold: int
        :param n_threshold: max number of iterations without any move before changing object selection strategy
        :type path: string
        :param path: if not None, path where to save intermediate results
        :type compute_tau_list: boolean
        :param compute_tau_list: if True, save the value of tau function after each iteration
        """

        self.n_iterations = n_iterations
        self.min_n_clusters = np.array([max(min_n_x_clusters, 2), max(min_n_y_clusters, 2), max(min_n_z_clusters, 2)])
        self.n_threshold = n_threshold
        self.path = path
        self.compute_tau_list = compute_tau_list
        self.optimization_strategy = optimization_strategy

        # these fields will be available after calling fit
        self.x_ = None
        self.y_ = None
        self.z_ = None

        self.initial_tau_ = None
        self.final_tau_ = None

        np.seterr(all='ignore')

    def _init_all(self, V):
        """
        Initialize all variables needed by the model.

        :param V: the dataset
        :return:
        """
        # verify that all matrices are correctly represented
        # check_array is a sklearn utility method
        self._dataset = None

        self._dataset = check_array(V, accept_sparse='csr', ensure_2d = False, allow_nd = True, dtype=[np.float64, np.float32, np.int32])

        self._csc_dataset = None
        if issparse(self._dataset):
            # transform also to csc
            self._csc_dataset = self._dataset.tocsc()
            
        # final number of iterations
        self._last_iteration = 0
        
        # dimensions in each mode
        self._n = self._dataset.shape

        # set the default value of the threshold to max(dimension)
        if self.n_threshold == 0:
            self.n_threshold = np.max(self._n)

        # the number of clusters on each mode
        self._n_clusters = np.array([0,0,0])

        # for each mode, an array containing the number of cluster to which each element has been assigned
        self._assignment = [np.zeros(self._n[0]), np.zeros(self._n[1]), np.zeros(self._n[2])]

        # T is the contingency tensor
        self._T = None

        # computation time
        self.execution_time_ = 0

	#(tau_x, tau_y, tau_z)
        self.initial_tau_ = (0,0,0)
        self.final_tau_ = (0,0,0)

        # number of performed moves on each mode
        self._performed_moves = np.array([0,0,0])

        # number of iterations with no moves
        self._iterations_without_moves = 0
        
        # initialize all 
        self._discrete_initialization()

        self._update_intermediate_values_after_z_move()

        


        ############
        
        self.tau_vector_ = list()

        
        logging.debug("[INFO] X's initialization: {0}".format(list(self._assignment[0])))
        logging.debug("[INFO] Y's initialization: {0}".format(list(self._assignment[1])))
        logging.debug("[INFO] Z's initialization: {0}".format(list(self._assignment[2])))



    def fit(self, V, y=None):
        """
        Fit CoClust to the provided data.

        Parameters
        -----------

        V : np.array with three modes

        y : unused parameter

        Returns
        --------

        self

        """

        # Initialization phase
        self._init_all(V)

        start_time = time()

        # Execution phase
        actual_n_iterations = 0

        self.initial_tau_ = self._compute_taus()

        while actual_n_iterations != self.n_iterations:
            
            # each iterations performs a move on rows and n_view moves on columns

            iter_start_time = time()
            logging.debug("[INFO] ##############################################\n" +
                         "\t\t### Iteration {0}".format(actual_n_iterations))
            #logging.debug("[INFO] X assignment: {0}".format(self._assignment[0]))
            #logging.debug("[INFO] Y assignment: {0}".format(self._assignment[1]))
            #logging.debug("[INFO] Z assignment: {0}".format(self._assignment[2]))


            # perform a move in each dimension
            for i in range(3):
                logging.debug("[INFO] Dimension {0}".format(i))
                
                if self._iterations_without_moves == 3 * self.n_threshold:
                    self._actual_item = [randint(1, self._n[0] * 100) % self._n[0], randint(1, self._n[1] * 100) % self._n[1], randint(1, self._n[2] * 100) % self._n[2]]
                    self._special_case = 0
                elif self._iterations_without_moves > 3 * self.n_threshold:
                    self._special_case += 1
                else:
                    self._special_case = -1
                    
                if int(self._special_case / 3) < self._n[i]:
                    self._perform_move(i)
                else:
                    self._update_intermediate_values_after_move(i)
                
            if self.compute_tau_list:
                tau = self._compute_taus()
                self.tau_vector_.append(tau)
                
            iter_end_time = time()

            
            if actual_n_iterations % 100 == 0:
                logging.info("Iteration #{0}".format(actual_n_iterations))
                logging.info("[INFO] # x clusters: {0}; # y clusters: {1}; # z clusters: {2}".format(self._n_clusters[0], self._n_clusters[1], self._n_clusters[2]))
                tau = self._compute_taus()
                logging.info("[INFO] Taus: {0}".format(tau))
                logging.info("[INFO] Iteration time: {0}".format(iter_end_time - iter_start_time))
            

            if self.path != None:
                if actual_n_iterations % 1000 == 0:
                    f = open(self.path + 'assignments_' + str(actual_n_iterations) + '.txt', 'w+')
                    f.write('##### x #####\n')
                    for i in range(self._n[0]):
                        f.write(f"{i}\t{self._assignment[0][i]}\n")
                    f.write('##### y #####\n')
                    for i in range(self._n[1]):
                        f.write(f"{i}\t{self._assignment[1][i]}\n")
                    f.write('##### z #####\n')
                    for i in range(self._n[2]):
                        f.write(f"{i}\t{self._assignment[2][i]}\n")
                    f.close()
                
            actual_n_iterations += 1
            if int(self._special_case / 3) == np.max(self._n):
                logging.info("[INFO] All moves have been tried. Taus can't be improved by moving any element.")
                self._last_iteration = actual_n_iterations
                actual_n_iterations = self.n_iterations

        end_time = time()

        execution_time = end_time - start_time
        self.final_tau_ = self._compute_taus()
        
        logging.info('#####################################################')
        logging.info("[INFO] Execution time: {0}".format(execution_time))

        # clone cluster assignments and transform in lists
        self.x_ = np.copy(self._assignment[0]).tolist()
        self.y_ = np.copy(self._assignment[1]).tolist()
        self.z_ = np.copy(self._assignment[2]).tolist()
        self.execution_time_ = execution_time

        logging.info("[INFO] Number of x clusters found: {0}".format(self._n_clusters[0]))
        logging.info("[INFO] Number of y clusters found: {0}".format(self._n_clusters[1]))
        logging.info("[INFO] Number of z clusters found: {0}".format(self._n_clusters[2]))
        logging.info("[INFO] Number of moves performed on x: {0} / {1}".format(self._performed_moves[0], self.n_iterations))
        logging.info("[INFO] Number of moves performed on y: {0} / {1}".format(self._performed_moves[1], self.n_iterations))
        logging.info("[INFO] Number of moves performed on z: {0} / {1}".format(self._performed_moves[2], self.n_iterations))

        return self

    def _discrete_initialization(self):
        """
        The initialization method assign each element on each mode to a new cluster.

        :param:

        :return:
        """

        # simple assign each element to a cluster in each mode
        self._n_clusters[0] = self._n[0]
        self._n_clusters[1] = self._n[1]
        self._n_clusters[2] = self._n[2]

        # assign each element to a cluster
        for i in range(3):
            self._assignment[i] = np.arange(self._n[i])

        self._T = self._init_contingency_matrix()

                
        # init the T-derived fields for further computations
        self._init_T_derived_fields()

            
    def _init_contingency_matrix(self):
        """
        Initialize the T contingency tensor
        of shape _n_clusters
        For the moment the only initialization method available is the discrete one,
        so the initial contingency tensor coincides to the input tensor V

        :return: array with three modes
        """
        logging.debug("[INFO] Compute the contingency matrix...")

        new_t = np.zeros(self._n_clusters, dtype=float)

        for di in range(self._n[0]):
            x_cluster_of_c = self._assignment[0][di]

            for ci in range(self._n[1]):
                y_cluster_of_c = self._assignment[1][ci]

                for ei in range(self._n[2]):
                    z_cluster_of_c = self._assignment[2][ei]
                    new_t[x_cluster_of_c][y_cluster_of_c][z_cluster_of_c] += self._dataset[di][ci][ei]


        logging.debug("[INFO] End of contingency matrix computation...")
        
        
        return new_t

    
    def _init_T_derived_fields(self):
        """
        Initialize the vlaues that will be used in the computation of Delta tau

        :return:
        """

        logging.debug("[INFO] Init fields derived by the contingency matrix...")

        # square of the T matrix (tij^2)
        self._t_square = np.power(self._T, 2)

        # sum of data values per row cluster (t1.., ..., tm..)
        self._tot_t_per_x = np.sum(self._T, axis = (1,2))

        # sum of data values per col cluster (t.1., ..., t.n.)
        self._tot_t_per_y = np.sum(self._T, axis = (0,2))

        # sum of data values per z cluster (t..1, ..., t..r)
        self._tot_t_per_z = np.sum(self._T, axis = (0,1))

        # sum of data values per xy clusters (tij.) It is a Matrix of dimension num_x_clust * num_y_clust
        self._tot_t_per_xy = np.sum(self._T, axis = 2)

        # sum of data values per xz clusters (ti.k) It is a Matrix of dimension num_x_clust * num_z_clust
        self._tot_t_per_xz = np.sum(self._T, axis = 1)

        # sum of data values per yz clusters (t.jk) It is a Matrix of dimension num_y_clust * num_z_clust
        self._tot_t_per_yz = np.sum(self._T, axis = 0) 

        # sum of (data values ^ 2) per xy cluster (serve per il calcolo di gamma_r e gamma_c)
        self._tot_t_square_per_xy = np.sum(self._t_square, axis = 2)

        # sum of (data values ^ 2) per xz cluster (serve per il calcolo di gamma_r e gamma_c)
        self._tot_t_square_per_xz = np.sum(self._t_square, axis = 1)

        # sum of (data values ^ 2) per yz cluster (serve per il calcolo di gamma_r e gamma_c)
        self._tot_t_square_per_yz = np.sum(self._t_square, axis = 0)

        # total (T)
        self._tot = np.sum(self._tot_t_per_x)
        #.astype(np.float64)
        
        # total^2 (T^2)
        self._square_tot = np.power(self._tot, 2)

        # 2 / total (2/T)
        self._two_divided_by_tot = 2 / self._tot
  

    def _update_intermediate_values_after_move(self, dimension):
        """
        Calls one of the following functions, according to the considered mode (x, y, or z):

        - self._update_intermediate_values_after_x_move
        - self._update_intermediate_values_after_y_move
        - self._update_intermediate_values_after_z_move
        
        :type dimension: int (0, 1, 2)
        :param dimension: the mode we are considering (x = 0, y = 1, z = 2)

        """
        
        l = [self._update_intermediate_values_after_x_move, self._update_intermediate_values_after_y_move, self._update_intermediate_values_after_z_move]
        l[dimension]()

    def _update_intermediate_values_after_z_move(self):
        """
        TO BE USED ALSO BEFORE THE FIRST ITERATION
        Updates the following instance values:

        - self._omega_0, double,
        - self._omega_1, double,
        - self._omega_2, double
        - self._gamma, double,

        :return:
        """

        # omega_x
        numerator_0 = np.nansum(np.power(self._tot_t_per_x, 2))
        self._omega_0 = 1 - np.true_divide(numerator_0, self._square_tot)

        # omega_y, omega_z
        if self.optimization_strategy in ['AVG', 'ALT', 'ALT2']:
            numerator_1 = np.nansum(np.power(self._tot_t_per_y, 2))
            numerator_2 = np.nansum(np.power(self._tot_t_per_z, 2))
            self._omega_1 = 1 - np.true_divide(numerator_1, self._square_tot)
            self._omega_2 = 1 - np.true_divide(numerator_2, self._square_tot)

        # omega_yz
        else:
            numerator_1 = np.nansum(np.power(self._tot_t_per_yz, 2))
            self._omega_1 = 1 - (numerator_1 / self._square_tot)

                   
        # gamma
        numerator_gamma = np.nansum(np.true_divide(self._tot_t_square_per_yz, self._tot_t_per_yz))
        self._gamma = 1 - np.true_divide(numerator_gamma, self._tot)
                                      

    def _update_intermediate_values_after_x_move(self):
        """
        Updates the following values:

        - self._omega_0, double,
        - self._omega_1, double,
        - self._omega_2, double
        - self._gamma, double,
        
        :return:
        """
        

               
        # omega_y
        numerator_0 = np.nansum(np.power(self._tot_t_per_y, 2))
        self._omega_0 = 1 - (numerator_0 / self._square_tot)

        # omega_x, omega_z
        if self.optimization_strategy in ['AVG', 'ALT', 'ALT2']:
            numerator_1 = np.nansum(np.power(self._tot_t_per_x, 2))
            numerator_2 = np.nansum(np.power(self._tot_t_per_z, 2))
            self._omega_1 = 1 - np.true_divide(numerator_1, self._square_tot)
            self._omega_2 = 1 - np.true_divide(numerator_2, self._square_tot)

        # omega_xz
        else:
            numerator_1 = np.nansum(np.power(self._tot_t_per_xz, 2))
            self._omega_1 = 1 - (numerator_1 / self._square_tot)
        
        # gamma
        numerator_gamma = np.nansum(np.true_divide(self._tot_t_square_per_xz, self._tot_t_per_xz))
        self._gamma = 1 - (numerator_gamma / self._tot)

    def _update_intermediate_values_after_y_move(self):
        """
        Updates the following values:

        - self._omega_0, double,
        - self._omega_1, double,
        - self._omega_2, double
        - self._gamma, double,
        
        :return:
        """

        # omega_z
        numerator_0 = np.nansum(np.power(self._tot_t_per_z, 2))
        self._omega_0 = 1 - (numerator_0 / self._square_tot)

        # omega_x, omega_y
        if self.optimization_strategy in ['AVG', 'ALT', 'ALT2']:
            numerator_1 = np.nansum(np.power(self._tot_t_per_x, 2))
            numerator_2 = np.nansum(np.power(self._tot_t_per_y, 2))
            self._omega_1 = 1 - np.true_divide(numerator_1, self._square_tot)
            self._omega_2 = 1 - np.true_divide(numerator_2, self._square_tot)

        # omega_xy
        else:
            numerator_1 = np.nansum(np.power(self._tot_t_per_xy, 2))
            self._omega_1 = 1 - (numerator_1 / self._square_tot)

        # gamma
        numerator_gamma = np.nansum(np.true_divide(self._tot_t_square_per_xy, self._tot_t_per_xy))
        self._gamma = 1 - (numerator_gamma / self._tot)



    def _perform_move(self, dimension):
        """
        Perform a single move to improve the partition on rows.

        :param dimension: the mode we are considering (x = 0, y = 1, z = 2)
        :return:
        """

        logging.debug("[INFO] Special Case: {0}".format(self._special_case))
        if self._special_case >= 0:
            self._actual_item[dimension] += 1
            selected_element = (self._actual_item[dimension]) % self._n[dimension]
            selected_source_cluster = self._assignment[dimension][selected_element]
            #logging.debug("[INFO] selected_source_cluster: {0}".format(selected_source_cluster))
            #logging.debug("[INFO] number of elements in the cluster: {0}".format(np.shape(np.where(self._assignment[dimension] == selected_source_cluster)[0])))

        else:
            # select a random x cluster
            selected_source_cluster = randint(1, self._n_clusters[dimension] * 100) % self._n_clusters[dimension]
            logging.debug("[INFO] selected_source_cluster: {0}".format(selected_source_cluster))
            logging.debug("[INFO] number of elements in the cluster: {0}".format(np.shape(np.where(self._assignment[dimension] == selected_source_cluster)[0])))

            # select a random element of selected_cluster
            selected_element = choice(np.where(self._assignment[dimension]== selected_source_cluster)[0])
            #print(selected_element)
            logging.debug("[INFO] selected_element: {0}".format(selected_element))

        lambdas, sum_lambdas = self._compute_lambdas(selected_element, dimension)
        #logging.debug("[INFO] lambdas: {0}".format(lambdas))
        #logging.debug("[INFO] sum_lambdas: {0}".format(sum_lambdas))

        if self.optimization_strategy in ['AVG', 'ALT', 'ALT2']:
            computed_tau, delta_tau_0 = self._delta_tau(sum_lambdas, lambdas, selected_source_cluster, dimension)
        else:
            computed_tau, delta_tau_0 = self._delta_tau_agg(sum_lambdas, lambdas, selected_source_cluster, dimension)
        e_min = self._choose_cluster(computed_tau, delta_tau_0, selected_source_cluster)

        if e_min == selected_source_cluster:
            assignment = self._n_clusters[dimension]
        else:
            assignment = e_min

        go_on_normally = True
        if self._n_clusters[dimension] == self.min_n_clusters[dimension]:
            # if the number of row cluster is already equal to min check that the move will not delete a cluster
            go_on_normally = self._check_clustering_size(selected_source_cluster, dimension)
            logging.debug("[INFO] go_on_normally: {0}".format(go_on_normally))

        if go_on_normally and e_min >= 0:
            # go with the move
            self._assignment[dimension][selected_element] = assignment
            self._modify_cluster(lambdas, selected_source_cluster, e_min, dimension)
            self._iterations_without_moves = 0
            
			
        else:
            logging.debug("[INFO] Ignored move of row {2} from row cluster {0} to {1}".format(selected_source_cluster,
                                                                                             e_min, selected_element))
            self._iterations_without_moves += 1
        self._update_intermediate_values_after_move(dimension)



        
    def _compute_lambdas(self, selected_element, dimension):
        """
        Compute lambda values related to the selected element.

        In particular:
        * lambdas, matrix, shape = (#clusters on the first other mode, #clusters on the second other mode)
                    contains, for each couple of clusters on the two other modes, the sum of data related to the selected element;
        * sum_lambdas, float
                    contains the sum of lambdas

        :param selected_element: int, the id of the selected element
        :param dimension: the mode we are considering (x = 0, y = 1, z = 2)
        :return: a pair (lambdas, sum_lambdas),
                    see the method description for more details
        """

        lambdas = self._sum_data_per_clusters(selected_element, dimension)
        sum_lambdas = np.sum(lambdas)

        return lambdas, sum_lambdas

    def _sum_data_per_clusters(self, index, dimension):
        """
        Fixed an element, computes for each couple of clusters on the two other modes,
        the sum of data related to the selected element;

        :param index: int, the index of the element to consider
        :param dimension: the mode we are considering (x = 0, y = 1, z = 2)
        :return:
        """

        other_dimensions = [i for i in range(3) if i != dimension]
        
        sum_m = np.zeros(self._n_clusters[other_dimensions])
        temp_T = np.take(self._dataset, index, axis = dimension)
        for i in range(self._n[other_dimensions[0]]):
            for j in range(self._n[other_dimensions[1]]):                    
                sum_m[self._assignment[other_dimensions[0]][i],self._assignment[other_dimensions[1]][j]] += temp_T[i,j]

        return sum_m

    def _delta_tau(self, sum_lambdas, lambdas, original_cluster, dimension):
        """
        Compute the delta tau values. Fixed a source_cluster computes the delta tau values
        for each of the other existent cluster (plus the empty one)
      
        :param sum_lambdas: the sum of lambdas
        :param lambdas: matrix related to the element that should be moved
        :param original_cluster: the cluster currently containing the element
        :param dimension: int, the mode in wich perform the move (x = 0, y = 1, z = 2)
        :return: list of int, the tau value for each row cluster
        """
       
        if dimension == 0:
            _T = np.copy(self._T)
            sum_01 = np.copy(self._tot_t_per_xy)
            sum_02 = np.copy(self._tot_t_per_xz)
            sum_12 = np.copy(self._tot_t_per_yz)
            #logging.debug("[INFO] shape(_T): {0}".format(_T.shape))
        elif dimension == 1:
            _T = np.transpose(self._T, (1,0,2))
            sum_01 = np.copy(self._tot_t_per_xy.T)
            sum_02 = np.copy(self._tot_t_per_yz)
            sum_12 = np.copy(self._tot_t_per_xz)
            #logging.debug("[INFO] shape(_T): {0}".format(_T.shape))
        else:
            _T = np.transpose(self._T, (2,0,1))
            sum_01 = np.copy(self._tot_t_per_xz.T)
            sum_02 = np.copy(self._tot_t_per_yz.T)
            sum_12 = np.copy(self._tot_t_per_xy)
            #logging.debug("[INFO] shape(_T): {0}".format(_T.shape))

        temp_T = np.copy(_T)
        temp_T[original_cluster] = 0
        #print(f"Original cluster: {original_cluster}")
        temp_tot_per_x = np.sum(temp_T, axis = (1,2))
        temp_tot_per_xy = np.sum(temp_T, axis = 2)
        temp_tot_per_xz = np.sum(temp_T, axis = 1)
        #logging.debug("[INFO] temp_tot_per_x: {0}".format(temp_tot_per_x))


        division_two = np.nan_to_num(np.true_divide(np.multiply(sum_lambdas, 2), self._square_tot)) # 2 lambda.. / T^2
        division_one = np.nan_to_num(np.true_divide(lambdas, sum_12)) #(lambda_jk / t.jk) matrix of dimension num_y_clust * num_z_clust
        subtraction_one = np.subtract(_T[original_cluster], lambdas) #(tb11, ..., tbml) - (lambda_11, ..., lambda_ml) matrix of dimension num_y_clust * num_z_clust

        a1 = np.subtract(subtraction_one, temp_T) #tensor num_x_clusters * num_y_clusters * num_z_clusters
        a2 = np.sum(np.multiply(division_one, a1), axis = (1,2)) # vector of dimension num_x_clusters
        b = temp_tot_per_x - np.nansum(subtraction_one) # vector of dimension num_x_clusters

        denominator = self._omega_0**2 -self._omega_0 * b * division_two

        delta_tau_0 = np.nan_to_num(np.true_divide(np.true_divide(2 * self._omega_0, self._tot) * a2 + (self._gamma * division_two) * b, denominator))


        
        k = np.sum(np.subtract(np.nan_to_num(np.true_divide(np.power(_T[original_cluster], 2), sum_02[original_cluster])),
                                     np.nan_to_num(np.true_divide(np.power(subtraction_one, 2), np.sum(subtraction_one, axis = 0)))))#scalar
        k2 = np.sum(np.subtract(np.nan_to_num(np.true_divide(np.sum(np.power(_T[original_cluster], 2), axis = 1), sum_01[original_cluster])),
                                     np.nan_to_num(np.true_divide(np.sum(np.power(subtraction_one, 2), axis =1), np.sum(subtraction_one, axis = 1)))))#scalar

        

        
        T1 = temp_T + lambdas #tensor num_x_clusters * num_y_clusters * num_z_clusters
        d1 = np.sum(np.power(T1, 2), axis = 1) # matrix of dimension num_x_clusters * num_z_clusters
        d2 = np.sum(np.nan_to_num(np.true_divide(d1, temp_tot_per_xz + np.sum(lambdas, axis = 0))), axis = 1) # vector of dimension num_x_clusters
        
        temp_tot_per_xz[original_cluster] = 1
        c1 = np.sum(np.power(temp_T, 2), axis = 1) # matrix of dimension num_x_clusters * num_z_clusters
        c2 = np.sum(np.nan_to_num(np.true_divide(c1, temp_tot_per_xz)), axis = 1) # vector of dimension num_x_clusters


        delta_tau_1 = np.nan_to_num(np.true_divide(c2 - d2 + k,  self._omega_1 * self._tot))

        e1 = np.sum(np.power(T1, 2), axis = 2) # matrix of dimension num_x_clusters * num_y_clusters
        e2 = np.sum(np.nan_to_num(np.true_divide(e1, temp_tot_per_xy + np.sum(lambdas, axis = 1))), axis = 1) # vector of dimension num_x_clusters
        
        temp_tot_per_xy[original_cluster] = 1
        f1 = np.sum(np.power(temp_T, 2), axis = 2) # matrix of dimension num_x_clusters * num_y_clusters
        f2 = np.sum(np.nan_to_num(np.true_divide(f1, temp_tot_per_xy)), axis = 1) # vector of dimension num_x_clusters


        delta_tau_2 = np.nan_to_num(np.true_divide(f2 - e2 + k2,  self._omega_2 * self._tot))
        
        computed_taus = delta_tau_0 + delta_tau_1 + delta_tau_2

        #logging.debug("[INFO] taus : {0}".format((delta_tau_0, delta_tau_1, delta_tau_2)))


        # check if the source is a singleton cluster and force useless move to empty cluster to 0.0
        is_singleton = not self._check_clustering_size(original_cluster, dimension)
        if is_singleton:
            computed_taus[original_cluster] = 0.0  

        if self.optimization_strategy == 'ALT2':
            d0 = delta_tau_0 < 0
            d1 = delta_tau_0 == 0
            d2 = computed_taus < 0
            d = d0 + (d1 * d2) # clusters with delta_tau_0 <0 and computed_taus < 0, or delta_tau_0 negative
            computed_taus = computed_taus * d

        return computed_taus, delta_tau_0

    def _delta_tau_agg(self, sum_lambdas, lambdas, original_cluster, dimension):
        """
        Compute the delta tau values for row clusters. Fixed a source_cluster computes the delta tau values
        for each of the other existent cluster (plus the empty one)

        :param tot_t_per_cc: the sum of t values grouped by column cluster
        :param sum_lambdas: the sum of lambdas per view
        :param lambdas: for each view and column cluster the difference due to the move of the element
        :param original_cluster: the cluster currently containing the element
        :return: list of int, the tau value for each row cluster
        """

        if dimension == 0:
            _T = np.copy(self._T)
            sum_0 = self._tot_t_per_x[original_cluster] #tb.. scalare
            sum_12 = np.copy(self._tot_t_per_yz) #t.jk matrice
            #logging.debug("[INFO] shape(_T): {0}".format(_T.shape))
        elif dimension == 1:
            _T = np.transpose(self._T, (1,0,2))
            sum_0 = self._tot_t_per_y[original_cluster]
            sum_12 = np.copy(self._tot_t_per_xz)
            #logging.debug("[INFO] shape(_T): {0}".format(_T.shape))
        else:
            _T = np.transpose(self._T, (2,0,1))
            sum_0 = self._tot_t_per_z[original_cluster]
            sum_12 = np.copy(self._tot_t_per_xy)
            #logging.debug("[INFO] shape(_T): {0}".format(_T.shape))

        temp_T = np.copy(_T)
        temp_T[original_cluster] = 0
        #print(f"Original cluster: {original_cluster}")
        temp_tot_per_x = np.sum(temp_T, axis = (1,2))
        #print(temp_tot_per_rc, self._tot_t_per_rc)
        #print(f"sum_labdas: {sum_lambdas}")

        division_two = np.nan_to_num(np.true_divide(np.multiply(sum_lambdas, 2), self._square_tot)) # 2 lambda. / T^2
        #logging.debug("[INFO] division_two: {0}".format(division_two))
        division_one = np.nan_to_num(np.true_divide(lambdas, sum_12)) #(lambda_j / t.jk) matrix of dimension num_y_clust * num_z_clust
        #logging.debug("[INFO] division_one: {0}".format(division_one))
        subtraction_one = np.subtract(_T[original_cluster], lambdas) #(tb1, ..., tbm) - (lambda_1, ..., lambda_m) matrix of dimension num_y_clust * num_z_clust
        #logging.debug("[INFO] subtraction_one: {0}".format(subtraction_one))
        k = np.sum(np.subtract(np.nan_to_num(np.true_divide(np.power(_T[original_cluster], 2), sum_0)),
                                     np.nan_to_num(np.true_divide(np.power(subtraction_one, 2), sum_0 + sum_lambdas))))#scalare
        #logging.debug("[INFO] k: {0}".format(k))
        
        a1 = np.subtract(subtraction_one, temp_T) #tensor num_x_clusters * num_y_clusters * num_z_clusters
        #logging.debug("[INFO] a1: {0}".format(a1))
        a2 = np.sum(np.multiply(division_one, a1), axis = (1,2)) # vector of dimension num_x_clusters
        #logging.debug("[INFO] a2: {0}".format(a2))
        b = temp_tot_per_x - np.nansum(subtraction_one) # vector of dimension num_x_clusters
        #logging.debug("[INFO] b: {0}".format(b))

        delta_tau_0 = np.nan_to_num(np.true_divide((2 * self._omega_0 / self._tot) * a2 + (self._gamma * division_two) * b, self._omega_0**2 -self._omega_0 * b * division_two))
        #logging.debug("[INFO] delta_tau_0: {0}".format(delta_tau_0))
        
        T1 = temp_T + lambdas #tensor num_x_clusters * num_y_clusters * num_z_clusters
        #logging.debug("[INFO] T1: {0}".format(T1))
        d1 = np.sum(np.power(T1, 2), axis = (1,2)) # vector of dimension num_x_clusters
        #logging.debug("[INFO] d1: {0}".format(d1))
        d2 = np.nan_to_num(np.true_divide(d1, temp_tot_per_x + sum_lambdas)) # vector of dimension num_x_clusters
        #logging.debug("[INFO] d2: {0}".format(d2))
            
        c1 = np.sum(np.power(temp_T, 2), axis = (1,2)) # vector of dimension num_x_clusters * num_z_clusters
        #logging.debug("[INFO] c1: {0}".format(c1))
        c2 = np.nan_to_num(np.true_divide(c1, temp_tot_per_x)) # vector of dimension num_x_clusters
        #logging.debug("[INFO] c2: {0}".format(c2))

        
        delta_tau_1 = np.nan_to_num(np.true_divide(c2 - d2 + k,  self._omega_1 * self._tot))
       
        #logging.debug("[INFO] delta_tau_1: {0}".format(delta_tau_1))

        computed_taus = np.add(delta_tau_0, delta_tau_1)

        
        # check if the source is a singleton cluster and force useless move to empty cluster to 0.0
        is_singleton = not self._check_clustering_size(original_cluster, dimension)
        if is_singleton:
            computed_taus[original_cluster] = 0.0

        if self.optimization_strategy == 'AGG2':

            d0 = delta_tau_0 < 0
            d1 = delta_tau_0 == 0
            d2 = computed_taus < 0
            d = d0 + (d1 * d2) # clusters with delta_tau_0 == 0 and computed_taus < 0, or delta_tau_0 negative
            computed_taus = computed_taus * d

        return computed_taus, delta_tau_0


    def _choose_cluster(self, computed_tau, delta_tau_0, selected_source_cluster):
        """
        It chooses the cluster where to move the selected element
        """
        e_min = -1
        if self.optimization_strategy in ['AVG','AGG']:
            min_delta_tau = np.min(computed_tau)
            if min_delta_tau < 0:
                equal_solutions = np.where(min_delta_tau == computed_tau)[0]
                if len(equal_solutions) > 1:
                    min_tau_0 = np.min(delta_tau_0[equal_solutions])
                    e_min = np.where(min_tau_0 == delta_tau_0)[0][0]
                else:
                    e_min = equal_solutions[0]
            elif min_delta_tau == 0:
                equal_solutions = np.where(min_delta_tau == computed_tau)[0]
                min_tau_0 = np.min(delta_tau_0[equal_solutions])
                if min_tau_0 < 0:
                    if len(equal_solutions) > 1:
                        e_min = np.where(min_tau_0 == delta_tau_0)[0][0]
                    else:
                        e_min = equal_solutions[0]
                

                
        elif self.optimization_strategy in ['ALT2','AGG2']:
            if np.all(computed_tau == 0):
                e_min = -1
            else:
                min_delta_tau = np.min(computed_tau[computed_tau != 0])
                equal_solutions = np.where(min_delta_tau == computed_tau)[0]
                if len(equal_solutions) > 1:
                    min_tau_0 = np.min(delta_tau_0[equal_solutions])
                    e_min = np.where(min_tau_0 == delta_tau_0)[0][0]
                else:
                    e_min = equal_solutions[0]

        else:
            min_delta_0 = np.min(delta_tau_0)
            if min_delta_0 < 0:
                equal_solutions = np.where(min_delta_0 == delta_tau_0)[0]
                if len(equal_solutions) > 1:
                    min_delta_tau = np.min(computed_tau[equal_solutions])
                    e_min = np.where(min_delta_tau == computed_tau)[0][0]
                else:
                    e_min = equal_solutions[0]
            elif min_delta_0 == 0:
                equal_solutions = np.where(min_delta_0 == delta_tau_0)[0]
                min_delta_tau = np.min(computed_tau[equal_solutions])
                if min_delta_tau < 0:
                    if len(equal_solutions) > 1:
                        e_min = np.where(min_delta_tau == computed_tau)[0][0]
                    else:
                        e_min = equal_solutions[0]

        return e_min
        

    
    
    def _modify_cluster(self, lambda_t, source_c, destination_c, dimension):
        """
        It calls one of the following functions, according to the mode considered:

        - self._modify_x_cluster
        - self._modify_y_cluster
        - self._modify_z_cluster

        :param lambda_t: matrix, values of the element we want to move
        :param source_c: int, the id of the original cluster
        :param destination_c: int, the id of the destination cluster
        :param dimension: int, the mode in wich perform the move (x = 0, y = 1, z = 2)
        :return:
        """
        l = [self._modify_x_cluster, self._modify_y_cluster, self._modify_z_cluster]
        l[dimension](lambda_t, source_c, destination_c)

        
    def _modify_x_cluster(self, lambda_t, source_c, destination_c):
        """
        Updates the T contingency tensor in order to move one element x from a source cluster to a destination cluster.

        :param lambda_t: matrix, values of the element we want to move
        :param source_c: int, the id of the original cluster
        :param destination_c: int, the id of the destination cluster
        :return:
        """
        logging.debug("[INFO] Move element from cluster {0} to {1}".format(source_c, destination_c))

        lambda_tot = np.sum(lambda_t)
        lambda_y = np.sum(lambda_t, axis = 1)
        lambda_z = np.sum(lambda_t, axis = 0)
        
        if destination_c == source_c:
            # case 1) the destination cluster is a new one
            logging.debug("[INFO] Create new cluster {0}".format(destination_c))

            # add one dimension on the first mode for the new cluster
            self._T = np.concatenate((self._T, np.reshape(lambda_t, (1, lambda_t.shape[0], lambda_t.shape[1]))), axis=0)

            # update the source
            self._T[source_c] -= lambda_t

            self._tot_t_per_x[source_c] -= lambda_tot
            self._tot_t_per_x = np.concatenate((self._tot_t_per_x, [lambda_tot]))
            self._tot_t_per_xy[source_c] -= lambda_y
            self._tot_t_per_xz[source_c] -= lambda_z
            self._tot_t_per_xy = np.concatenate((self._tot_t_per_xy, np.reshape(lambda_y, (1, lambda_y.shape[0]))), axis = 0)
            self._tot_t_per_xz = np.concatenate((self._tot_t_per_xz, np.reshape(lambda_z, (1, lambda_z.shape[0]))), axis = 0)

            self._n_clusters[0] += 1
        else:
            # case 2) the destination cluster already exists
            # we move the object x from the original cluster to the destination cluster
            self._T[source_c] -= lambda_t
            self._T[destination_c] += lambda_t

            lambda_tot = np.sum(lambda_t)


            self._tot_t_per_x[source_c] -= lambda_tot
            self._tot_t_per_x[destination_c] += lambda_tot
            self._tot_t_per_xy[source_c] -= lambda_y
            self._tot_t_per_xz[source_c] -= lambda_z
            self._tot_t_per_xy[destination_c] += lambda_y
            self._tot_t_per_xz[destination_c] += lambda_z


            # check that the original cluster has at least one remaining element
            is_empty = not self._check_clustering_size(source_c,dimension = 0, min_number_of_elements=1)

            if is_empty:
                # compact the contingency matrix
                # delete the source cluster
                self._T = np.delete(self._T, source_c, 0)
                
                # update the total values removing the source cluster item
                self._tot_t_per_x = np.delete(self._tot_t_per_x, source_c)
                self._tot_t_per_xy = np.delete(self._tot_t_per_xy, source_c, axis = 0)
                self._tot_t_per_xz = np.delete(self._tot_t_per_xz, source_c, axis = 0)

                # update the assignments to reflect the new cluster ids
                for di in range(self._n[0]):
                    if self._assignment[0][di] > source_c:
                        self._assignment[0][di] -= 1

                self._n_clusters[0] -= 1
        # for squares we recompute the tensor
        self._t_square = np.power(self._T, 2) #OK

        # sum of (data values ^ 2) per xy cluster 
        self._tot_t_square_per_xy = np.sum(self._t_square, axis = 2)

        # sum of (data values ^ 2) per xz cluster 
        self._tot_t_square_per_xz = np.sum(self._t_square, axis = 1)

        # sum of (data values ^ 2) per yz cluster
        self._tot_t_square_per_yz = np.sum(self._t_square, axis = 0)

        self._performed_moves[0] += 1

    def _modify_y_cluster(self, lambda_t, source_c, destination_c):
        """
        Updates the T contingency tensor in order to move one element x from a source cluster to a destination cluster.

        :param lambda_t: matrix, values of the element we want to move
        :param source_c: int, the id of the original cluster
        :param destination_c: int, the id of the destination cluster
        :return:
        """
        logging.debug("[INFO] Move element from cluster {0} to {1}".format(source_c, destination_c))

        lambda_tot = np.sum(lambda_t)
        lambda_x = np.sum(lambda_t, axis = 1)
        lambda_z = np.sum(lambda_t, axis = 0)
        
        if destination_c == source_c:
            # case 1) the destination cluster is a new one
            logging.debug("[INFO] Create new cluster {0}".format(destination_c))

            # add one dimension on the second mode for the new cluster
            self._T = np.concatenate((self._T, np.reshape(lambda_t, (lambda_t.shape[0], 1, lambda_t.shape[1]))), axis=1)

            # update the source
            self._T[:,source_c] -= lambda_t

            self._tot_t_per_y[source_c] -= lambda_tot
            self._tot_t_per_y = np.concatenate((self._tot_t_per_y, [lambda_tot]))
            self._tot_t_per_xy[:,source_c] -= lambda_x
            self._tot_t_per_yz[source_c] -= lambda_z
            self._tot_t_per_xy = np.concatenate((self._tot_t_per_xy, np.reshape(lambda_x, (lambda_x.shape[0], 1))), axis = 1)
            self._tot_t_per_yz = np.concatenate((self._tot_t_per_yz, np.reshape(lambda_z, (1, lambda_z.shape[0]))), axis = 0)

            self._n_clusters[1] += 1
        else:
            # case 2) the destination cluster already exists
            # we move the object x from the original cluster to the destination cluster
            self._T[:,source_c] -= lambda_t
            self._T[:,destination_c] += lambda_t

            self._tot_t_per_y[source_c] -= lambda_tot
            self._tot_t_per_y[destination_c] += lambda_tot
            self._tot_t_per_xy[:,source_c] -= lambda_x
            self._tot_t_per_yz[source_c] -= lambda_z
            self._tot_t_per_xy[:,destination_c] += lambda_x
            self._tot_t_per_yz[destination_c] += lambda_z


            # check that the original cluster has at least one remaining element
            is_empty = not self._check_clustering_size(source_c,dimension = 1, min_number_of_elements=1)

            if is_empty:
                # compact the contingency matrix
                # delete the source cluster
                self._T = np.delete(self._T, source_c, 1)
                
                # update the total values removing the source cluster item
                self._tot_t_per_y = np.delete(self._tot_t_per_y, source_c)
                self._tot_t_per_xy = np.delete(self._tot_t_per_xy, source_c, axis = 1)
                self._tot_t_per_yz = np.delete(self._tot_t_per_yz, source_c, axis = 0)

                # update the assignments to reflect the new row cluster ids
                for di in range(self._n[1]):
                    if self._assignment[1][di] > source_c:
                        self._assignment[1][di] -= 1

                self._n_clusters[1] -= 1
        # for squares we recompute the tensor
        self._t_square = np.power(self._T, 2) #OK

        # sum of (data values ^ 2) per xy cluster 
        self._tot_t_square_per_xy = np.sum(self._t_square, axis = 2)

        # sum of (data values ^ 2) per xz cluster
        self._tot_t_square_per_xz = np.sum(self._t_square, axis = 1)

        # sum of (data values ^ 2) per yz cluster
        self._tot_t_square_per_yz = np.sum(self._t_square, axis = 0)

        self._performed_moves[1] += 1
        
    def _modify_z_cluster(self, lambda_t, source_c, destination_c):
        """
        Updates the T contingency tensor in order to move one element x from a source cluster to a destination cluster.

        :param lambda_t: matrix, values of the element we want to move
        :param source_c: int, the id of the original cluster
        :param destination_c: int, the id of the destination cluster
        :return:
        """
        logging.debug("[INFO] Move element from cluster {0} to {1}".format(source_c, destination_c))

        lambda_tot = np.sum(lambda_t)
        lambda_x = np.sum(lambda_t, axis = 1)
        lambda_y = np.sum(lambda_t, axis = 0)

        
        if destination_c == source_c:
            # case 1) the destination cluster is a new one
            logging.debug("[INFO] Create new cluster {0}".format(destination_c))

            # add one dimension on the third mode for the new cluster
            self._T = np.concatenate((self._T, np.reshape(lambda_t, (lambda_t.shape[0], lambda_t.shape[1], 1))), axis=2)

            # update the source
            self._T[:, :, source_c] -= lambda_t

            self._tot_t_per_z[source_c] -= lambda_tot
            self._tot_t_per_z = np.concatenate((self._tot_t_per_z, [lambda_tot]))
            self._tot_t_per_yz[:,source_c] -= lambda_y
            self._tot_t_per_xz[:,source_c] -= lambda_x
            self._tot_t_per_xz = np.concatenate((self._tot_t_per_xz, np.reshape(lambda_x, (lambda_x.shape[0], 1))), axis = 1)
            self._tot_t_per_yz = np.concatenate((self._tot_t_per_yz, np.reshape(lambda_y, (lambda_y.shape[0], 1))), axis = 1)


            self._n_clusters[2] += 1
        else:
            # case 2) the destination cluster already exists
            # we move the object x from the original cluster to the destination cluster
            self._T[:,:,source_c] -= lambda_t
            self._T[:,:,destination_c] += lambda_t
            
            lambda_tot = np.sum(lambda_t)


            self._tot_t_per_z[source_c] -= lambda_tot
            self._tot_t_per_z[destination_c] += lambda_tot
            self._tot_t_per_xz[:,source_c] -= lambda_x
            self._tot_t_per_yz[:,source_c] -= lambda_y
            self._tot_t_per_xz[:,destination_c] += lambda_x
            self._tot_t_per_yz[:,destination_c] += lambda_y


            # check that the original cluster has at least one remaining element
            is_empty = not self._check_clustering_size(source_c,dimension = 2, min_number_of_elements=1)

            if is_empty:
                # compact the contingency matrix
                # delete the source cluster
                self._T = np.delete(self._T, source_c, 2)
                
                # update the total values removing the source cluster item
                self._tot_t_per_z = np.delete(self._tot_t_per_z, source_c)
                self._tot_t_per_xz = np.delete(self._tot_t_per_xz, source_c, axis = 1)
                self._tot_t_per_yz = np.delete(self._tot_t_per_yz, source_c, axis = 1)

                # update the assignments to reflect the new row cluster ids
                for di in range(self._n[2]):
                    if self._assignment[2][di] > source_c:
                        self._assignment[2][di] -= 1

                self._n_clusters[2] -= 1
        # for squares we recompute the tensor
        self._t_square = np.power(self._T, 2) #OK

        # sum of (data values ^ 2) per xy cluster 
        self._tot_t_square_per_xy = np.sum(self._t_square, axis = 2)

        # sum of (data values ^ 2) per xz cluster
        self._tot_t_square_per_xz = np.sum(self._t_square, axis = 1)

        # sum of (data values ^ 2) per yz cluster
        self._tot_t_square_per_yz = np.sum(self._t_square, axis = 0)

        self._performed_moves[2] += 1

    def _check_clustering_size(self, cluster_id, dimension, min_number_of_elements=2):
        """
        Check if the specified cluster has at least min_number_of_elements elements.
        Returns True if the cluster contains at least the specified number of elements, False otherwise.

        :param cluster_id: int, the id of the cluster that contains the element at this moment
        :param dimension: the mode we are considering (x = 0, y = 1, z = 2)
        :param min_number_of_elements: int, default 2, the min number of elements that the cluster should have
        :return: boolean, True if the cluster has at least min_number_of_elements elements, False otherwise
        """

        for rc in self._assignment[dimension]:
            if rc == cluster_id:
                min_number_of_elements -= 1
            if min_number_of_elements <= 0:
                # stop when the min number is found
                return True

        return False

    def _compute_taus(self):
        """
        Compute the value of tau_x, tau_y and tau_z

        :return: a tuple (tau_x, tau_y, tau_z)
        """

        a_x = np.sum(np.nan_to_num(np.true_divide(np.sum(self._t_square, axis = 0), self._tot_t_per_yz))) # scalar
        b_x = np.true_divide(np.sum(np.power(self._tot_t_per_x, 2)), self._square_tot) #scalar
        self._tau_x = np.nan_to_num(np.true_divide(np.true_divide(a_x, self._tot) - b_x, 1 - b_x))

        a_y = np.sum(np.nan_to_num(np.true_divide(np.sum(self._t_square, axis = 1), self._tot_t_per_xz))) # scalar
        b_y = np.true_divide(np.sum(np.power(self._tot_t_per_y, 2)), self._square_tot) #scalar
        self._tau_y = np.nan_to_num(np.true_divide(np.true_divide(a_y, self._tot) - b_y, 1 - b_y))

        a_z = np.sum(np.nan_to_num(np.true_divide(np.sum(self._t_square, axis = 2), self._tot_t_per_xy))) # scalar
        b_z = np.true_divide(np.sum(np.power(self._tot_t_per_z, 2)), self._square_tot) #scalar
        self._tau_z = np.nan_to_num(np.true_divide(np.true_divide(a_z, self._tot) - b_z, 1 - b_z))

        #logging.debug("[INFO] a_x, a_y, a_z, b_x, b_y, b_z: {0},{1}, {2}, {3}, {4}, {5}".format(a_x, a_y, a_z, b_x, b_y, b_z))

        return self._tau_x, self._tau_y, self._tau_z
    

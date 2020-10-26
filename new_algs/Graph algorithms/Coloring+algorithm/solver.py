import logging
import sys

import cvxpy
from mosek.fusion import *

from algorithm_helper import *


def compute_vector_coloring(graph, sdp_type, verbose, iteration=-1):
    """Computes sdp_type vector coloring of graph using Cholesky decomposition.

        Args:
            graph (nx.Graph): Graph to be processed.
            sdp_type (string): Non-strict, Strict or Strong coloring.
            verbose (bool): Solver verbosity.
            iteration (int): Number of main algorithm iteration. Used for vector coloring loading or saving.
        Returns:
              2-dim matrix: Rows of this matrix are vectors of computed vector coloring.
        """

    def cholesky_factorize(M):
        """Returns L such that M = LL^T.

            According to https://en.wikipedia.org/wiki/Cholesky_decomposition#Proof_for_positive_semi-definite_matrices
                if L is positive semi-definite then we can turn it into positive definite by adding eps*I.

            We can also perform LDL' decomposition and set L = LD^(1/2) - it works in Matlab even though M is singular.

            It sometimes returns an error if M was computed with big tolerance for error.

            Args:
                M (2-dim matrix): Positive semidefinite matrix to be factorized.

            Returns:
                L (2-dim matrix): Cholesky factorization of M such that M = LL^T.
            """

        logging.info('Starting Cholesky factorization...')

        # eps = 0#1e-7
        # for i in range(M.shape[0]):
        #    M[i, i] = M[i, i] + eps

        try:
            M = np.linalg.cholesky(M)
        except:
            eps = 1e-7
            for i in range(M.shape[0]):
                M[i, i] = M[i, i] + eps
            M = np.linalg.cholesky(M)

        logging.info('Cholesky factorization computed')
        return M

    def compute_matrix_coloring(graph, sdp_type, verbose):
        """Finds matrix coloring M of graph using Mosek solver.

        Args:
            graph (nx.Graph): Graph to be processed.
            sdp_type (string): Non-strict, Strict or Strong vector coloring.
            verbose (bool): Sets verbosity level of solver.

        Returns:
            2-dim matrix: Matrix coloring of graph G.

        Notes:
            Maybe we can add epsilon to SDP constraints instead of 'solve' parameters?

            For some reason optimal value of alpha is greater than value computed from M below if SDP is solved with big
                tolerance for error

            TODO: strong vector coloring
        """

        logging.info('Computing matrix coloring of graph with {0} nodes and {1} edges...'.format(
            graph.number_of_nodes(), graph.number_of_edges()
        ))

        result = None
        alpha_opt = None

        if config.solver_name == 'mosek':
            with Model() as Mdl:

                # Variables
                n = graph.number_of_nodes()
                alpha = Mdl.variable(Domain.lessThan(0.))
                m = Mdl.variable(Domain.inPSDCone(n))

                if n <= 50:
                    sdp_type = 'strong'

                # Constraints
                Mdl.constraint(m.diag(), Domain.equalsTo(1.0))
                for i in range(n):
                    for j in range(n):
                        if i > j and has_edge_between_ith_and_jth(graph, i, j):
                            if sdp_type == 'strict' or sdp_type == 'strong':
                                Mdl.constraint(Expr.sub(m.index(i, j), alpha),
                                               Domain.equalsTo(0.))
                            elif sdp_type == 'nonstrict':
                                Mdl.constraint(Expr.sub(m.index(i, j), alpha),
                                               Domain.lessThan(0.))
                        elif i > j and sdp_type == 'strong':
                            Mdl.constraint(Expr.add(m.index(i, j), alpha),
                                           Domain.greaterThan(0.))

                # Objective
                Mdl.objective(ObjectiveSense.Minimize, alpha)

                # Set solver parameters
                # Mdl.setSolverParam("intpntCoTolRelGap", 1e-4)
                # Mdl.setSolverParam("intpntCoTolPfeas", 1e-5)
                # Mdl.setSolverParam("intpntCoTolMuRed", 1e-5)
                # Mdl.setSolverParam("intpntCoTolInfeas", 1e-7)
                # Mdl.setSolverParam("intpntCoTolDfeas", 1e-5)

                # mosek_params = {
                #     'MSK_DPAR_INTPNT_CO_TOL_REL_GAP': 1e-4,
                #     'MSK_DPAR_INTPNT_CO_TOL_PFEAS': 1e-5,
                #     'MSK_DPAR_INTPNT_CO_TOL_MU_RED': 1e-5,
                #     'MSK_DPAR_INTPNT_CO_TOL_INFEAS': 1e-7,
                #     'MSK_DPAR_INTPNT_CO_TOL_DFEAS': 1e-5,
                #     'MSK_DPAR_SEMIDEFINITE_TOL_APPROX': 1e-10
                # }

                # with open(config.logs_directory() + 'logs', 'w') as outfile:
                if verbose:
                    Mdl.setLogHandler(sys.stdout)

                # moze stworz jeden model na caly algorytm i tylko usuwaj ograniczenia?

                Mdl.solve()

                alpha_opt = alpha.level()[0]
                level = m.level()
                result = [[level[j * n + i] for i in range(n)] for j in range(n)]
                result = np.array(result)
        else:
            n = graph.number_of_nodes()

            # I must be doing something wrong with the model definition - too many constraints and variables

            # Variables
            alpha = cvxpy.Variable()
            Mat = cvxpy.Variable((n, n), PSD=True)

            # Constraints (can be done using trace as well)
            constraints = []
            for i in range(n):
                constraints += [Mat[i, i] == 1]

            for i in range(n):
                for j in range(n):
                    if i > j and has_edge_between_ith_and_jth(graph, i, j):
                        constraints += [Mat[i, j] <= alpha]

            # Objective
            objective = cvxpy.Minimize(alpha)

            # Create problem instance
            problem = cvxpy.Problem(objective, constraints)

            # Solve
            mosek_params = {
                'MSK_DPAR_INTPNT_CO_TOL_REL_GAP': 1e-4,
                'MSK_DPAR_INTPNT_CO_TOL_PFEAS': 1e-5,
                'MSK_DPAR_INTPNT_CO_TOL_MU_RED': 1e-5,
                'MSK_DPAR_INTPNT_CO_TOL_INFEAS': 1e-7,
                'MSK_DPAR_INTPNT_CO_TOL_DFEAS': 1e-5,
                'MSK_DPAR_SEMIDEFINITE_TOL_APPROX': 1e-10
            }

            mosek_params_default = {
                'MSK_DPAR_INTPNT_CO_TOL_REL_GAP': 1e-7,
                'MSK_DPAR_INTPNT_CO_TOL_PFEAS': 1e-8,
                'MSK_DPAR_INTPNT_CO_TOL_MU_RED': 1e-8,
                'MSK_DPAR_INTPNT_CO_TOL_INFEAS': 1e-10,
                'MSK_DPAR_INTPNT_CO_TOL_DFEAS': 1e-8,
                'MSK_DPAR_SEMIDEFINITE_TOL_APPROX': 1e-10
            }

            try:
                problem.solve(
                    solver=cvxpy.MOSEK,
                    verbose=config.solver_verbose,
                    warm_start=True,
                    mosek_params=mosek_params)
                alpha_opt = alpha.value
                result = Mat.value
            except cvxpy.error.SolverError:
                print '\nerror in mosek, changing to cvxopt\n'
                problem.solve(
                    solver=cvxpy.CVXOPT,
                    verbose=config.solver_verbose,
                    warm_start=True)
                alpha_opt = alpha.value
                result = Mat.value

        logging.info('Found matrix {0}-coloring'.format(1 - 1 / alpha_opt))

        return result

    # if config.use_previous_sdp_result and iteration == 1 and vector_coloring_in_file(graph, sdp_type):
    #     L = read_vector_coloring_from_file(graph, sdp_type)
    # else:
    M = compute_matrix_coloring(graph, sdp_type, verbose)
    L = cholesky_factorize(M)
    # if config.use_previous_sdp_result and iteration == 1:
    if iteration == 1:
        save_vector_coloring_to_file(graph, sdp_type, L)

    return L

# def compute_vector_coloring_2(graph, sdp_type, verbose, queue, iteration=-1):
#     """Computes sdp_type vector coloring of graph using Cholesky decomposition.
#
#         Args:
#             graph (nx.Graph): Graph to be processed.
#             sdp_type (string): Non-strict, Strict or Strong coloring.
#             verbose (bool): Solver verbosity.
#             iteration (int): Number of main algorithm iteration. Used for vector coloring loading or saving.
#         Returns:
#               2-dim matrix: Rows of this matrix are vectors of computed vector coloring.
#         """
#
#     def cholesky_factorize(M):
#         """Returns L such that M = LL^T.
#
#             According to https://en.wikipedia.org/wiki/Cholesky_decomposition#Proof_for_positive_semi-definite_matrices
#                 if L is positive semi-definite then we can turn it into positive definite by adding eps*I.
#
#             We can also perform LDL' decomposition and set L = LD^(1/2) - it works in Matlab even though M is singular.
#
#             It sometimes returns an error if M was computed with big tolerance for error.
#
#             Args:
#                 M (2-dim matrix): Positive semidefinite matrix to be factorized.
#
#             Returns:
#                 L (2-dim matrix): Cholesky factorization of M such that M = LL^T.
#             """
#
#         logging.info('Starting Cholesky factorization...')
#
#         eps = 1e-7
#         for i in range(M.shape[0]):
#             M[i, i] = M[i, i] + eps
#
#         M = np.linalg.cholesky(M)
#
#         logging.info('Cholesky factorization computed')
#         return M
#
#     def compute_matrix_coloring(graph, sdp_type, verbose):
#         """Finds matrix coloring M of graph using Mosek solver.
#
#         Args:
#             graph (nx.Graph): Graph to be processed.
#             sdp_type (string): Non-strict, Strict or Strong vector coloring.
#             verbose (bool): Sets verbosity level of solver.
#
#         Returns:
#             2-dim matrix: Matrix coloring of graph G.
#
#         Notes:
#             Maybe we can add epsilon to SDP constraints instead of 'solve' parameters?
#
#             For some reason optimal value of alpha is greater than value computed from M below if SDP is solved with big
#                 tolerance for error
#
#             TODO: strong vector coloring
#         """
#
#         logging.info('Computing matrix coloring of graph with {0} nodes and {1} edges...'.format(
#             graph.number_of_nodes(), graph.number_of_edges()
#         ))
#
#         result = None
#         alpha_opt = None
#
#         if config.solver_name == 'mosek':
#             with Model() as Mdl:
#
#                 # Variables
#                 n = graph.number_of_nodes()
#                 alpha = Mdl.variable(Domain.lessThan(0.))
#                 m = Mdl.variable(Domain.inPSDCone(n))
#
#                 # Constraints
#                 Mdl.constraint(m.diag(), Domain.equalsTo(1.0))
#                 for i in range(n):
#                     for j in range(n):
#                         if i > j and has_edge_between_ith_and_jth(graph, i, j):
#                             if sdp_type == 'strict' or sdp_type == 'strong':
#                                 Mdl.constraint(Expr.sub(m.index(i, j), alpha),
#                                              Domain.equalsTo(0.))
#                             elif sdp_type == 'nonstrict':
#                                 Mdl.constraint(Expr.sub(m.index(i, j), alpha),
#                                              Domain.lessThan(0.))
#                         elif sdp_type == 'strong':
#                             Mdl.constraint(Expr.add(m.index(i, j), alpha),
#                                          Domain.greaterThan(0.))
#
#                 # Objective
#                 Mdl.objective(ObjectiveSense.Minimize, alpha)
#
#                 # Set solver parameters
#                 #M.setSolverParam("numThreads", 1)
#
#                 # with open(config.logs_directory() + 'logs', 'w') as outfile:
#                 if verbose:
#                     Mdl.setLogHandler(sys.stdout)
#
#                 # moze stworz jeden model na caly algorytm i tylko usuwaj ograniczenia?
#
#                 Mdl.solve()
#
#                 alpha_opt = alpha.level()[0]
#                 level = m.level()
#                 result = [[level[j * n + i] for i in range(n)] for j in range(n)]
#                 result = np.array(result)
#         else:
#             n = graph.number_of_nodes()
#
#             # I must be doing something wrong with the model definition - too many constraints and variables
#
#             # Variables
#             alpha = cvxpy.Variable()
#             Mat = cvxpy.Variable((n, n), PSD=True)
#
#             # Constraints (can be done using trace as well)
#             constraints = []
#             for i in range(n):
#                 constraints += [Mat[i, i] == 1]
#
#             for i in range(n):
#                 for j in range(n):
#                     if i > j and has_edge_between_ith_and_jth(graph, i, j):
#                         constraints += [Mat[i, j] <= alpha]
#
#             # Objective
#             objective = cvxpy.Minimize(alpha)
#
#             # Create problem instance
#             problem = cvxpy.Problem(objective, constraints)
#
#             # Solve
#             mosek_params = {
#                 'MSK_DPAR_INTPNT_CO_TOL_REL_GAP': 1e-4,
#                 'MSK_DPAR_INTPNT_CO_TOL_PFEAS': 1e-5,
#                 'MSK_DPAR_INTPNT_CO_TOL_MU_RED': 1e-5,
#                 'MSK_DPAR_INTPNT_CO_TOL_INFEAS': 1e-7,
#                 'MSK_DPAR_INTPNT_CO_TOL_DFEAS': 1e-5,
#                 'MSK_DPAR_SEMIDEFINITE_TOL_APPROX': 1e-10
#             }
#
#             mosek_params_default = {
#                 'MSK_DPAR_INTPNT_CO_TOL_REL_GAP': 1e-7,
#                 'MSK_DPAR_INTPNT_CO_TOL_PFEAS': 1e-8,
#                 'MSK_DPAR_INTPNT_CO_TOL_MU_RED': 1e-8,
#                 'MSK_DPAR_INTPNT_CO_TOL_INFEAS': 1e-10,
#                 'MSK_DPAR_INTPNT_CO_TOL_DFEAS': 1e-8,
#                 'MSK_DPAR_SEMIDEFINITE_TOL_APPROX': 1e-10
#             }
#
#             try:
#                 problem.solve(
#                     solver=cvxpy.MOSEK,
#                     verbose=config.solver_verbose,
#                     warm_start=True,
#                     mosek_params=mosek_params)
#                 alpha_opt = alpha.value
#                 result = Mat.value
#             except cvxpy.error.SolverError:
#                 print '\nerror in mosek, changing to cvxopt\n'
#                 problem.solve(
#                     solver=cvxpy.CVXOPT,
#                     verbose=config.solver_verbose,
#                     warm_start=True)
#                 alpha_opt = alpha.value
#                 result = Mat.value
#
#         logging.info('Found matrix {0}-coloring'.format(1 - 1 / alpha_opt))
#
#         return result
#
#     # if config.use_previous_sdp_result and iteration == 1 and vector_coloring_in_file(graph, sdp_type):
#     #     L = read_vector_coloring_from_file(graph, sdp_type)
#     # else:
#     M = compute_matrix_coloring(graph, sdp_type, verbose)
#     L = cholesky_factorize(M)
#     # if config.use_previous_sdp_result and iteration == 1:
#     #     save_vector_coloring_to_file(graph, sdp_type, L)
#
#     queue.put(L)
#     sys.exit()

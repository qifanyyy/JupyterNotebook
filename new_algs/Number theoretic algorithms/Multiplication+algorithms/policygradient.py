import numpy as np
from numpy import linalg as la
from scipy.special import huber, pseudo_huber
from matrixmath import solveb, vec, mdot, rngg
from utility import inplace_print

from time import time,sleep
import warnings
from warnings import warn
from copy import copy

class PolicyGradientOptions:
    def __init__(self,
                 epsilon, # Convergence threshold
                 eta, # Step size
                 max_iters=1e6, # Max number of steps to take
                 disp_stride=1, # INWORK # How many iterations between plot updates
                 wait_time=1.0/20, #INWORK #From MATLAB - Ensure this is above 1/refresh_rate for your monitor
                 keep_hist=False,  # Record history during optimization?
                 opt_method='gradient',
                 keep_opt='last',
                 step_direction='gradient',
                 stepsize_method='constant',
                 exact=True, # Exact (model-known) or estimated (model-free) system parameters?
                 regularizer=None,
                 regweight=0,
                 stop_crit='gradient',
                 fbest_repeat_max=0,
                 display_output=True,
                 display_inplace=False,
                 slow=0.05,
                 nt=None, # Rollout length
                 nr=None, # Number of rollouts
                 ru=None  # Exploration radius
                 ):
        self.epsilon = epsilon
        self.eta = 0.5 if step_direction=='policy_iteration' else eta
        self.max_iters = max_iters
        self.disp_stride = disp_stride
        self.wait_time = wait_time
        self.keep_hist = keep_hist
        self.opt_method = opt_method
        self.keep_opt = keep_opt
        self.step_direction = step_direction
        self.stepsize_method = stepsize_method
        self.exact = exact
        self.regularizer = regularizer
        self.regweight = regweight
        self.stop_crit=stop_crit
        self.fbest_repeat_max=fbest_repeat_max
        self.display_output = display_output
        self.display_inplace = display_inplace
        self.slow = slow
        self.nt = nt
        self.nr = nr
        self.ru = ru


class Regularizer:
    def __init__(self, regstr, mu=0, soft=False, thresh1=0, thresh2=0):
        self.regstr = regstr
        self.mu = mu
        self.soft = soft
        self.thresh1 = thresh1
        self.thresh2 = thresh2

    def rfun(self, K):
        return regularizer_fun(K,self.regstr,self.mu,self.thresh1,self.thresh2)

    def rgrad(self, K):
        return regularizer_grad(K,self.regstr,self.mu,self.soft,self.thresh1,self.thresh2)

def regularizer_fun(K, regstr, mu=0, thresh1=0, thresh2=0):
    # VECTOR NORMS
    if regstr == 'vec1': # Vector 1-norm
        val = np.abs(K).sum()
    if regstr == 'vec2': # Vector 2-norm
        val = la.norm(K,'fro')
    if regstr == 'vecinf': # Vector inf-norm
        val = np.abs(K).max()

    # SQUARED VECTOR NORMS
    if regstr == 'vec1sq': # Squared vector 1-norm
        val = np.square(np.abs(K).sum())
    if regstr == 'vec2sq': # Squared vector 2-norm
        val = np.square(K).sum()
    if regstr == 'vecinfsq': # Squared vector inf-norm
        val = np.square(np.abs(K).max())

    if regstr == 'vec_huber': # Vector Huber-norm
        val = huber_norm(thresh2,K)
    if regstr == 'vec_pseudo_huber': # Vector Huber-norm
        val = pseudo_huber_norm(thresh2,K)

    if regstr == 'vec_hubersq': # Squared vector Huber-norm
        val = np.square(huber_norm(thresh2,K))
    if regstr == 'vec_pseudo_hubersq': # Squared vector pseudo-Huber-norm
        val = np.square(pseudo_huber_norm(thresh2,K))

    # MATRIX NORMS
    if regstr == 'mr': # Row norm
        val = la.norm(K,ord=np.inf,axis=1).sum()
    if regstr == 'mc': # Column norm
        val = la.norm(K,ord=np.inf,axis=0).sum()
    if regstr == 'glr': # Group lasso on rows
        val = la.norm(K,ord=2,axis=1).sum()
    if regstr == 'glc': # Group lasso on columns
        val = la.norm(K,ord=2,axis=0).sum()
    if regstr == 'sglr': # Sparse group lasso on rows
        val = (1-mu)*la.norm(K,ord=1,axis=1).sum() + mu*la.norm(K,ord=2,axis=1).sum()
    if regstr == 'sglc': # Sparse group lasso on columns
        val = (1-mu)*la.norm(K,ord=1,axis=0).sum() + mu*la.norm(K,ord=2,axis=0).sum()

    # HUBER MATRIX NORMS
    if regstr == 'mr_huber':
        val = 0
        for i in range(K.shape[0]):
            val += p_huber_norm(K[i,:],p=np.inf,thresh=thresh2)
    if regstr == 'mc_huber':
        val = 0
        for j in range(K.shape[1]):
            val += p_huber_norm(K[:,j],p=np.inf,thresh=thresh2)
    if regstr == 'glr_huber':
        val = 0
        for i in range(K.shape[0]):
            val += p_huber_norm(K[i,:],p=2,thresh=thresh2)
    if regstr == 'glc_huber':
        val = 0
        for j in range(K.shape[1]):
            val += p_huber_norm(K[:,j],p=2,thresh=thresh2)
    return val


def regularizer_grad(K,regstr,mu=0,soft=False,thresh1=0,thresh2=0):
    # VECTOR NORMS
    if regstr == 'vec1': # Vector 1-norm
        grad = np.sign(K)
    if regstr == 'vec2': # Vector 1-norm
        grad = K/la.norm(K,'fro')
    if regstr == 'vecinf': # Vector inf-norm
        if not soft:
            grad = infnormgrad(K)
        else:
            grad = infnormgrad(K,thresh1)

    # HUBER VECTOR NORMS
    if regstr == 'vec_huber': # Vector Huber-norm
        grad = softsign(K,thresh2)

    # SQUARED VECTOR NORMS
    if regstr == 'vec1sq': # Squared vector 1-norm
        grad = 2*la.norm(vec(K),ord=1)*np.sign(K)
    if regstr == 'vec2sq': # Squared vector 2-norm
        grad = 2*K
    if regstr == 'vecinfsq': # Squared vector inf-norm
        if not soft:
            grad = infnormgradsq(K)
        else:
            grad = infnormgradsq(K,thresh1)
    if regstr == 'vec_hubersq': # Squared vector Huber-norm
        grad = 2*huber_norm(thresh2,K)*softsign(K,thresh2)

    # MATRIX NORMS
    if regstr == 'mr': # Row norm
        grad = np.zeros_like(K)
        for i in range(K.shape[0]):
            if not soft:
                grad[i,:] = infnormgrad(K[i,:])
            else:
                grad[i,:] = infnormgrad(K[i,:],thresh1)
    if regstr == 'mc': # Column norm
        grad = np.zeros_like(K)
        for j in range(K.shape[1]):
            if not soft:
                grad[:,j] = infnormgrad(K[:,j])
            else:
                grad[:,j] = infnormgrad(K[:,j],thresh1)
    if regstr == 'glr': # Group lasso on rows
        grad = np.zeros_like(K)
        for i in range(K.shape[0]):
                grad[i,:] = K[i,:]/la.norm(K[i,:],2)
    if regstr == 'glc': # Group lasso on columns
        grad = np.zeros_like(K)
        for j in range(K.shape[1]):
                grad[:,j] = K[:,j]/la.norm(K[:,j],2)
    if regstr == 'sglr': # Sparse group lasso on rows
        grad = (1-mu)*regularizer_grad(K,'vec1') + mu*regularizer_grad(K,'glr')
    if regstr == 'sglc': # Sparse group lasso on columns
        grad = (1-mu)*regularizer_grad(K,'vec1') + mu*regularizer_grad(K,'glc')

    # HUBER MATRIX NORMS
    if regstr == 'mr_huber':
        grad = np.zeros_like(K)
        for i in range(K.shape[0]):
                a = la.norm(K[i,:],np.inf)
                if a > thresh2:
                    grad[i,:] = infnormgrad(K[i,:])
                else:
                    grad[i,:] = (0.5/thresh2)*infnormgradsq(K[i,:])


    if regstr == 'glr_huber':
        grad = np.zeros_like(K)
        for i in range(K.shape[0]):
                a = la.norm(K[i,:],2)
                if a > thresh2:
                    grad[i,:] = K[i,:]/a
                else:
                    grad[i,:] = (1/thresh2)*K[i,:]
    if regstr == 'glc_huber':
        grad = np.zeros_like(K)
        for j in range(K.shape[1]):
                a = la.norm(K[:,j],2)
                if a > thresh2:
                    grad[:,j] = K[:,j]/a
                else:
                    grad[:,j] = K[:,j]/thresh2

    # SQUARED MATRIX NORMS
    if regstr == 'mrsq': # Squared row norm
        grad = np.zeros_like(K)
        subs = []
        subsmax = []
        for i,im in enumerate(np.argmax(K,axis=1)):
            subsmax.append((i,im))
        if not soft:
            subs = subsmax.copy()
        else:
            for i,row in enumerate(K):
                for j,colj in enumerate(row):
                    if colj >= (1-thresh1)*K[subsmax[i]]:
                        subs.append((i,j))
        for sb in subs:
            if not soft:
                grad[sb] = 2*regularizer_fun(K,'mr')*softsignscalar(K[sb])
            else:
                grad[sb] = 2*regularizer_fun(K,'mr')*softsignscalar(K[sb],thresh2)

    return grad


def infnormgrad(x,thresh=0):
    if thresh == 0:
        y = np.zeros_like(x)
        y[np.unravel_index(np.argmax(np.abs(x)),x.shape)] = np.sign(x[np.unravel_index(np.argmax(np.abs(x)),x.shape)])
    elif thresh > 0:
        y = np.sign(copy(x))
        y[np.where(np.abs(x)<(1-thresh)*np.abs(x[np.unravel_index(np.argmax(np.abs(x)),x.shape)]))] = 0
    else:
        raise Exception('Threshold for soft norm must be set nonnegative!')
    return y

def infnormgradsq(x,thresh=0):
    if thresh == 0:
        y = np.zeros_like(x)
        y[np.unravel_index(np.argmax(np.abs(x)),x.shape)] = x[np.unravel_index(np.argmax(np.abs(x)),x.shape)]
    elif thresh > 0:
        y = copy(x)
        y[np.where(np.abs(x)<(1-thresh)*np.abs(x[np.unravel_index(np.argmax(np.abs(x)),x.shape)]))] = 0
    else:
        raise Exception('Threshold for soft norm must be set nonnegative!')
    return y

def huber_norm(delta,x):
    return (huber(delta,x)/delta).sum()

def pseudo_huber_norm(delta,x):
    return (pseudo_huber(delta,x)/delta).sum()

def softsign(x,thresh=0):
    y = np.array(np.sign(x))
    if thresh > 0:
        y[np.where(np.abs(x)<thresh)] = (float(1)/thresh)*x[np.where(np.abs(x)<thresh)]
    elif thresh < 0:
        raise Exception('Threshold for soft norm must be set nonnegative!')
    return y

def softsignscalar(x,thresh=0):
    y = np.sign(x)
    if thresh > 0:
        if np.abs(x) < thresh:
            y = (float(1)/thresh)*x
    elif thresh < 0:
        raise Exception('Threshold for soft norm must be set nonnegative!')
    return y

def p_huber_norm(x,p,thresh=0):
    a = la.norm(x,p)
    if a > thresh:
        return a-0.5*thresh
    else:
        return (0.5/thresh)*np.square(a)


def backtrack(SS, w, REG, G, V, alpha=0.01, beta=0.5, eta0=1, PGO=None, rng=None):
    """Backtracking line search"""

    def cost(K):
        if PGO.exact:
            SStemp = copy(SS)
            SStemp.setK(K)
            cost_base = SStemp.c
        else:
            cost_base = estimate_cost(K, SS, PGO, rng)

        # TESTING TODO remove
        # SStemp = copy(SS)
        # SStemp.setK(K)
        # cost_base = SStemp.c


        cost_reg = w*REG.rfun(K0) if REG is not None else 0
        return cost_base + cost_reg

    eta = eta0 # Stepsize
    K0 = SS.K
    Knew = K0 + eta*V
    c0 = cost(K0)
    cnew = cost(Knew)
    while cnew > c0 + alpha*eta*np.multiply(G,V).sum():
        eta *= beta
        Knew = K0 + eta*V
        cnew = cost(Knew)
    SS.setK(Knew)
    return SS, eta


def prox(SS, PGO):
    """Proximal operation"""
    Knew = np.copy(SS.K)

    # Soft thresholding operator (elementwise) on K
    if PGO.regularizer.regstr == 'vec1':
        Knew = np.maximum(0,Knew-PGO.regweight*PGO.eta)-np.maximum(0,-Knew-PGO.regweight*PGO.eta)

    # Block soft thresholding operator (row-wise) on K,
    # corresponds to actuator selection
    if PGO.regularizer.regstr == 'glr':
        for i in range(SS.K.shape[0]):
            Knew[i,:] *= np.max(1-PGO.regweight*PGO.eta/la.norm(Knew[i,:],ord=2),0)

    # Block soft thresholding operator (column-wise) on K,
    # corresponds to sensor selection
    if PGO.regularizer.regstr == 'glc':
        for j in range(SS.K.shape[1]):
            Knew[:,j] *= np.max(1-PGO.regweight*PGO.eta/la.norm(Knew[:,j],ord=2),0)

    return Knew



def estimate_gradient(K, SS, PGO, rng):
    # Estimate gradient for zeroth-order optimization
    # Follows "Algorithm 1" in the paper

    # Rollout length
    nt = PGO.nt

    # Number of rollouts
    nr = PGO.nr

    # Exploration radius
    ru = PGO.ru

    # Draw random initial states
    x = rng.multivariate_normal(np.zeros(SS.n), SS.S0, nr)

    # Draw random gain deviations and scale to Frobenius norm ball
    Uraw = rng.normal(size=[nr,SS.m,SS.n])
    U = ru*Uraw/la.norm(Uraw,'fro',axis=(1,2))[:,None,None]

    # Stack dynamics matrices into a 3D array
    Kd = K + U
    KdT = np.transpose(Kd, (0, 2, 1))
    QKr = SS.Q + np.einsum('...ik,...kj', KdT, np.einsum('...ik,...kj', SS.R, Kd))

    # Simulate all rollouts together
    c = np.zeros(nr)
    AKrNom = SS.A + np.einsum('...ik,...kj', SS.B, Kd)
    for t in range(nt):
        # Accumulate cost
        c += np.einsum('...i,...i', x, np.einsum('...jk,...k', QKr, x))

        # Calculate noisy closed-loop dynamics
        AKr = np.copy(AKrNom)
        for i in range(SS.p):
            AKr += (SS.a[i]**0.5)*rng.randn(nr)[:,np.newaxis,np.newaxis]*np.repeat(SS.Aa[np.newaxis,:,:,i], nr, axis=0)
        for j in range(SS.q):
            AKr += np.einsum('...ik,...kj',(SS.b[j]**0.5)*rng.randn(nr)[:,np.newaxis,np.newaxis]*np.repeat(SS.Bb[np.newaxis,:,:,j], nr, axis=0),Kd)

        # Transition the state
        x = np.einsum('...jk,...k', AKr, x)

    # Estimate gradient
    Glqr = np.einsum('i,i...', c, U)
    Glqr *= K.size/(nr*(ru**2))

    # # TESTING
    # G_est = Glqr
    # G_act = SS.grad
    #
    # print('estimated gradient: ')
    # print(G_est)
    # print('actual gradient: ')
    # print(G_act)
    # print('error angle')
    # print(np.arccos(np.sum((G_est*G_act))/(la.norm(G_est)*la.norm(G_act))))
    # print('error scale')
    # print((la.norm(G_est)/la.norm(G_act)))

    return Glqr


def estimate_cost(K, SS, PGO, rng):
    # Estimate cost for zeroth-order optimization
    # Use same parameters as for gradient estimation to ensure cost estimates are of similar quality

    # Rollout length
    nt = PGO.nt

    # Number of rollouts
    nr = PGO.nr

    # Draw random initial states
    x = rng.multivariate_normal(np.zeros(SS.n), SS.S0, nr)

    # TESTING: TODO remove
    # nr = 2*SS.n
    # x = (SS.n**0.5)*np.vstack([np.eye(SS.n), -np.eye(SS.n)])
    # nr = SS.n
    # x = np.eye(SS.n)

    # Simulate all rollouts together
    c = np.zeros(nr)
    AKnom = SS.A + np.dot(SS.B, K)
    for t in range(nt):
        # Accumulate cost
        c += np.einsum('...i,...i', x, np.einsum('jk,...k', SS.QK, x))

        # Calculate noisy closed-loop dynamics
        AK = np.repeat(AKnom[None,:], nr, axis=0)
        for i in range(SS.p):
            AK += (SS.a[i]**0.5)*rng.randn(nr)[:,np.newaxis,np.newaxis]*np.repeat(SS.Aa[np.newaxis,:,:,i], nr, axis=0)
        for j in range(SS.q):
            AK += np.einsum('...ik,...kj',(SS.b[j]**0.5)*rng.randn(nr)[:,np.newaxis,np.newaxis]*np.repeat(SS.Bb[np.newaxis,:,:,j], nr, axis=0), K)

        # Transition the state
        x = np.einsum('...jk,...k', AK, x)

    # Estimate cost
    c_est = np.mean(c)

    # TESTING: TODO remove
    # if c_est > 1e6:
    #     c_est = np.inf
    #
    # SS.setK(K)
    # print('actual cost: %f  estimated cost: %f' % (SS.c, c_est))

    return c_est


def run_policy_gradient(SS, PGO):
    # run_policy_gradient  Run policy gradient descent on a system
    #
    # Inputs:
    # SS is an LQRSysMult instance with an initial gain matrix K
    # PGO is a PolicyGradientOptions instance
    #
    # K1_subs is the subscripts of the first gain entry varied in surf plot
    # K2_subs is the subscripts of the first gain entry varied in surf plot
    # ax is the axes to plot in
    #
    # Outputs:
    # SS with closed-loop properties at the post-optimization configuration
    # histlist, a list of data histories over optimization iterations


    # TODO: Move into an options class/object or get rid of this
    Kmax = np.max(np.abs(vec(SS.K)))
    bin1 = 0.01*Kmax


    # Initialize
    stop = False
    converged = False
    stop_early = False
    iterc = 0
    sleep(0.5)
    t_start = time()

    headerstr = 'Iteration | Stop quant / threshold |  Curr obj |  Best obj | Norm of gain delta | Stepsize  '
    if PGO.regularizer is not None:
        headerstr = headerstr+'| Sparsity'
    print(headerstr)

    K = np.copy(SS.K)
    Kbest = np.copy(SS.K)
    objfun_best = np.inf
    Kold = np.copy(SS.K)

    P = SS.P
    S = SS.S

    fbest_repeats = 0

    # Initialize history matrices
    if PGO.keep_hist:
        mat_shape = list(K.shape)
        mat_shape.append(PGO.max_iters)
        mat_shape = tuple(mat_shape)
        K_hist = np.full(mat_shape, np.inf)
        grad_hist = np.full(mat_shape, np.inf)
        c_hist = np.full(PGO.max_iters, np.inf)
        objfun_hist = np.full(PGO.max_iters, np.inf)

    rng = rngg()

    # Iterate
    while not stop:
        if PGO.exact:
            # Calculate gradient (G)
            # Do this to get combined calculation of P and S,
            # pass previous P and S to warm-start dlyap iterative algorithm
            SS.calc_PS(P,S)
            Glqr = SS.grad
            P = SS.P
            S = SS.S
        else:
            if PGO.step_direction in ['gradient', 'natural_gradient', 'gauss_newton', 'policy_iteration']:
                Glqr = estimate_gradient(K, SS, PGO, rng)


#INWORK
#                if step_direction=='natural_gradient' or step_direction=='gauss_newton' or step_direction=='policy_iteration':
#                    # Estimate S
#                    if step_direction=='policy_iteration':
#                        # Estimate R_K
#
#                        # NOTE!!!!! only valid for zero multiplicative noise
#                        # for now - also need to estimate the noise terms? or
#                        # are they known a priori?
#
#                        # Also need to finish the True "coarse-ID" estimation
#                        # which takes uncertainty into account to ensure the
#                        # estimated optimal gain is stabilizing so P_K is well
#                        # defined
#
#                        # Also for the theory we need estimates of error of R_K
#
#
#                        # Model-based estimation
#                        [Ahat,Bhat] = lsqr_lti(SS)
#                        P_Khat = dlyap_mult(Ahat,Bhat,SS.a,SS.Aa,SS.b,SS.Bb,SS.Q,SS.R,SS.S0,K)
#                        R_K = SS.R + Bhat.T*P_Khat*Bhat
#
#                        # Model-free estimation
#                        # Rollout length
#                        nt = 20
#
#                        # Number of rollouts
#                        nr = 10000
#
#                        # Random initial state standard deviation
#                        xstd = 1
#
#                        # Random control input standard deviation
#                        ustd = 1
#
#                        # Random disturbance input standard deviation
#                        # wstd = 0.01
#                        wstd = 0
#
#                        [~,H21hat,H22hat] = lsqr_lti_qfun(SS,xstd,ustd,wstd,nt,nr)
#                        H22=H22hat
#                        H21=H21hat



        # Calculate step direction (V)
        if PGO.regularizer is None or PGO.opt_method=='proximal':
            G = Glqr
        else:
            Greg = PGO.regularizer.rgrad(SS.K)
            G = Glqr + PGO.regweight*Greg

        if PGO.regularizer is None or PGO.opt_method=='proximal':
            if PGO.step_direction=='gradient':
                V = G
            elif PGO.step_direction=='natural_gradient':
                V = solveb(SS.grad,SS.S)
            elif PGO.step_direction=='gauss_newton':
                V = solveb(la.solve(SS.RK,SS.grad),SS.S)
        else:
            if PGO.step_direction=='gradient':
                V = G
#            # Variant 1 - seems more elegant but why should it work?
#            elif PGO.step_direction=='natural_gradient':
#                V = solveb(G,SS.S)
#            elif PGO.step_direction=='gauss_newton':
#                V = solveb(la.solve(SS.RK,G),SS.S)
#            # Variant 2 - seems more justifiable
#            elif PGO.step_direction=='natural_gradient':
#                V = solveb(SS.grad,SS.S) + PGO.regweight*PGO.regularizer.rgrad(SS.K)
#            elif PGO.step_direction=='gauss_newton':
#                V = solveb(la.solve(SS.RK,SS.grad),SS.S) + PGO.regweight*PGO.regularizer.rgrad(SS.K)

        # Check if mean-square stable
        if SS.c == np.inf:
            raise Exception('ITERATE WENT UNSTABLE DURING GRADIENT DESCENT')

        if PGO.regularizer is None:
            objfun = SS.c
        else:
            objfun = SS.c + PGO.regweight*PGO.regularizer.rfun(SS.K)

        # Record current iterate
        if PGO.keep_hist:
            K_hist[:,:,iterc] = SS.K
            grad_hist[:,:,iterc] = SS.grad
            c_hist[iterc] = SS.c
            objfun_hist[iterc] = objfun

        if iterc == 0:
            Kchange = np.inf
        else:
            Kchange = la.norm(K-Kold,'fro')/la.norm(K,'fro')
        Kold = K

        # Check for stopping condition
        if PGO.stop_crit=='gradient':
            normgrad = la.norm(G)
            stop_quant = normgrad
            stop_thresh = PGO.epsilon
            if normgrad < PGO.epsilon:
                converged = True
        elif PGO.stop_crit=='Kchange':
            stop_quant = Kchange
            stop_thresh = PGO.epsilon
            if Kchange < PGO.epsilon:
                converged = True
        elif PGO.stop_crit=='fbest':
            stop_quant = fbest_repeats
            stop_thresh = PGO.fbest_repeat_max
            if fbest_repeats > PGO.fbest_repeat_max:
                converged = True
        elif PGO.stop_crit=='fixed':
            stop_quant = iterc
            stop_thresh = PGO.max_iters

        if iterc >= PGO.max_iters-1:
            stop_early = True
        else:
            iterc += 1

        stop = converged or stop_early

        if PGO.display_output and PGO.regularizer is not None:
            Kmax = np.max(np.abs(vec(SS.K)))
            bin1 = 0.05*Kmax
            sparsity = np.sum(np.abs(SS.K)<bin1)/SS.K.size

        # Record current best (subgradient method)
        if objfun < objfun_best:
            objfun_best = objfun
            Kbest = SS.K
            fbest_repeats = 0
        else:
            fbest_repeats += 1

        # Update iterate
        if PGO.opt_method == 'gradient':
            if PGO.step_direction=='policy_iteration':
                eta = 0.5 # for printing only
                H21 = la.multi_dot([SS.B.T,SS.P,SS.A])
                H22 = SS.RK
                if PGO.regularizer is None:
                    K = -la.solve(H22,H21)
                    SS.setK(K)
                else:
                    if PGO.stepsize_method=='constant':
                        K = -la.solve(H22,H21) - PGO.eta*PGO.regweight*Greg # This might not work, it is sequential GN then grad desc regularizer
                        SS.setK(K)
                    elif PGO.stepsize_method=='backtrack':
                        raise Exception("Invalid stepsize option, choose constant")
            else:
                # Calculate step size
                if PGO.stepsize_method=='constant':
                    eta = PGO.eta
                    K = SS.K - eta*V
                    SS.setK(K)
                elif PGO.stepsize_method=='backtrack':
                    SS, eta = backtrack(SS, PGO.regweight, PGO.regularizer, G, -V, eta0=PGO.eta, PGO=PGO, rng=rng)
                    K = SS.K
                elif PGO.stepsize_method=='square_summable': # INWORK
                    eta = PGO.eta/(1.0+iterc)
                    K = SS.K - eta*V
                    SS.setK(K)
        elif PGO.opt_method == 'proximal':
            # Gradient step on LQR cost
            if PGO.step_direction=='policy_iteration':
                eta = 0.5 # for printing only
                H21 = la.multi_dot([SS.B.T,SS.P,SS.A])
                H22 = SS.RK
                K = -la.solve(H22,H21)
                SS.setK(K)
            else:
                # Calculate step size
                if PGO.stepsize_method=='constant':
                    eta = PGO.eta
                    K = SS.K - eta*V
                    SS.setK(K)
                elif PGO.stepsize_method=='backtrack':
                    SS, eta = backtrack(SS, PGO.regweight, PGO.regularizer, G, -V, eta0=PGO.eta, PGO=PGO, rng=rng)
                    K = SS.K
                elif PGO.stepsize_method=='square_summable': # INWORK
                    eta = PGO.eta/(1.0+iterc)
                    K = SS.K - eta*V
                    SS.setK(K)
            # Prox step on regularizer
            K = prox(SS,PGO)
            SS.setK(K)

        if hasattr(PGO,'slow'):
            if PGO.slow is not None:
                sleep(PGO.slow)

        # Printing
        if PGO.display_output:
            # Print iterate messages
            printstr0 = "{0:9d}".format(iterc+1)
            printstr1 = " {0:5.3e} / {1:5.3e}".format(stop_quant, stop_thresh)
            printstr2a = "{0:5.3e}".format(objfun)
            printstr2b = "{0:5.3e}".format(objfun_best)
            printstr3 = "         {0:5.3e}".format(Kchange)
            printstr4 = "{0:5.3e}".format(eta)
            printstr = printstr0+' | '+printstr1+' | '+printstr2a+' | '+printstr2b+' | '+printstr3+' | '+printstr4
            if PGO.regularizer is not None:
                printstr5 = "{0:6.2f}%".format(100*sparsity)
                printstr = printstr+' | '+printstr5
            if PGO.display_inplace:
                if iterc==0:
                    print(" " * len(printstr),end='')
                inplace_print(printstr)
            else:
                print(printstr)
            if stop: # Print stopping messages
                print('')
                if converged:
                    print('Optimization converged, stopping now')
                if stop_early:
#                    warnings.simplefilter('always', UserWarning)
#                    warn('Max iterations exceeded, stopping optimization early')
                    print('Max iterations exceeded, stopping optimization')

    if PGO.keep_hist:
        # Trim empty parts from preallocation
        K_hist = K_hist[:,:,0:iterc+1]
        grad_hist = grad_hist[:,:,0:iterc+1]
        c_hist = c_hist[0:iterc+1]
        objfun_hist = objfun_hist[0:iterc+1]
    else:
        K_hist = None
        grad_hist = None
        c_hist = None
        objfun_hist = None

    if PGO.keep_opt == 'best':
        SS.setK(Kbest)

    t_end = time()

    hist_list = [K_hist, grad_hist, c_hist, objfun_hist]

    print('Policy gradient descent optimization completed after %d iterations, %.3f seconds' % (iterc+1,t_end-t_start))
    return SS, hist_list
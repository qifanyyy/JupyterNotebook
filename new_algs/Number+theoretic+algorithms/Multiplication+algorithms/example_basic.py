import numpy as np
from policygradient import PolicyGradientOptions,run_policy_gradient,Regularizer
from ltimult import LQRSysMult

if __name__ == "__main__":
    # System problem data
    A = np.array([[0.7,0.3,0.2],[-0.2,0.4,0.5],[-0.4,0.2,-0.3]])
    B = np.array([[0.5,-0.3],[0.8,0.3],[0.1,0.9]])
    Q = np.eye(3)
    R = np.eye(2)
    S0 = np.eye(3)
    Aa = 0.1*np.array([[2,9,-6],[9,9,4],[-9,-2,5]])
    Aa = Aa[:,:,np.newaxis]
    Bb = 0.1*np.array([[8,8],[3,3],[-6,6]])
    Bb = Bb[:,:,np.newaxis]
    a = np.array([[0.1]])
    b = np.array([[0.1]])
    SS = LQRSysMult(A,B,a,Aa,b,Bb,Q,R,S0)

    # Start with an initially stabilizing (feasible) controller;
    # for this example the system is open-loop mean-square stable
    SS.setK(np.zeros([SS.m,SS.n]))

    # Policy gradient options
    PGO = PolicyGradientOptions(epsilon=(1e-2)*SS.Kare.size,
                                eta=1e-3,
                                max_iters=1000,
                                disp_stride=1,
                                keep_hist=True,
                                opt_method='proximal',
                                keep_opt='last',
                                step_direction='gradient',
                                stepsize_method='constant',
                                exact=True,
                                regularizer=Regularizer('vec1'),
                                regweight=1.0,
                                stop_crit='gradient',
                                fbest_repeat_max=0,
                                display_output=True,
                                display_inplace=True,
                                slow=False)

    # Run (regularized) policy gradient
    run_policy_gradient(SS,PGO)

    # Print the regularized optimal gains (from proximal gradient optimization)
    # and the unregularized optimal gains (from solving a Riccati equation)
    print('Optimized sparse gains')
    print(SS.K)
    print('Riccati gains')
    print(SS.Kare)
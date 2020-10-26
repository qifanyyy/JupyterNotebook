import numpy as np
from numpy import linalg as la
from matrixmath import is_pos_def,vec,sympart,kron,randn,dlyap,dare,mdot

import warnings
from warnings import warn
from copy import copy

###############################################################################
# Developer notes
###############################################################################
# MAKE SURE TO ADD ANY PROPERTIES TO THE DELETER METHODS TO ENSURE PROPER
# IDIOT-PROOFING WHEN (RE)SETTING SYSTEM PROPERTIES


###############################################################################
# Variables
###############################################################################
# A is the state-to-state transition matrix
# B is the input-to-state transition matrix
# a and Aa are the random scalars and matrices associated with uncertainty
# on the entries of the state-to-state transition matrix A
# b and Bb are the random scalars and matrices associated with uncertainty
# on the entries of the input-to-state transition matrix B
# Q and R are the LQR cost matrices
# S0 is the initial state covariance matrix
# K is the gain matrix
#
# RK is the closed-loop augmented R matrix
# EK is a closed-loop intermediate quantity
# grad is the cost (policy) gradient

###############################################################################
# LTI and LQR system classes
###############################################################################

class LTISys:
    def __init__(self,A,B,dirname=None):
        self._A = A
        self._B = B
        self._n = self._A.shape[1]
        self._m = self._B.shape[1]

    def set_A(self,A):
        self.del_cl()
        self._A = A
        self._n = self._A.shape[1]
        return self._A

    def set_B(self,B):
        self.del_cl()
        self._B = B
        self._m = self._B.shape[1]
        return self._B

    def setK(self,K):
        self.del_cl()
        self._K = K
        return self._K

    @property
    def A(self):
        return self._A

    @property
    def B(self):
        return self._B

    @property
    def n(self):
        return self._n

    @property
    def m(self):
        return self._m

    @property
    def K(self):
        return self._K

    @property
    def AK(self):
        if not hasattr(self,'_AK'):
            self.calc_AK()
        return self._AK

    @property
    def mss(self):
        if not hasattr(self,'_mss'):
            self.calc_mss()
        return self._mss

    def calc_AK(self):
        self._AK = self.A + np.dot(self.B,self.K)
        return self._AK

    def calc_mss(self):
        self._mss = check_mss_obj(self)
        return self._mss

    def sim_ol(self,x0,nt):
        return sim_traj_obj(self,x0,nt,feedback=False)

    def sim_cl(self,x0,nt):
        return sim_traj_obj(self,x0,nt,feedback=True)

    def del_lti_cl(self):
        if hasattr(self,'_AK'):
            del self._AK
        if hasattr(self,'_mss'):
            del self._mss

    def del_cl(self):
        self.del_lti_cl()


class LQRSys(LTISys):
    def __init__(self,A,B,Q,R,S0):
        LTISys.__init__(self,A,B)
        self._Q = Q
        self._R = R
        self._S0 = S0

    def set_Q(self,Q):
        self.del_lqr_cl()
        self._Q = Q
        return self._A

    def set_R(self,R):
        self.del_lqr_cl()
        self._R = R
        return self._R

    def set_S0(self,S0):
        self.del_lqr_cl()
        self._S0 = S0
        return self._S0

    @property
    def Q(self):
        return self._Q

    @property
    def R(self):
        return self._R

    @property
    def S0(self):
        return self._S0

    @property
    def QK(self):
        if not hasattr(self,'_QK'):
            self.calc_QK()
        return self._QK

    @property
    def P(self):
        if not hasattr(self,'_P'):
            self.calc_P()
        return self._P

    @property
    def S(self):
        if not hasattr(self,'_S'):
            self.calc_S()
        return self._S

    @property
    def c(self):
        if not hasattr(self,'_c'):
            self.calc_c()
        return self._c

    @property
    def Pare(self):
        if not hasattr(self,'_Pare'):
            self.calc_PKare()
        return self._Pare

    @property
    def Kare(self):
        if not hasattr(self,'_Kare'):
            self.calc_PKare()
        return self._Kare

    @property
    def ccare(self):
        if not hasattr(self,'_ccare'):
            self.calc_ccare()
        return self._ccare

    @property
    def grad(self):
        if not hasattr(self,'_grad'):
            self.calc_grad()
        return self._grad

    @property
    def RK(self):
        if not hasattr(self,'_RK'):
            self.calc_grad()
        return self._RK

    @property
    def EK(self):
        if not hasattr(self,'_EK'):
            self.calc_grad()
        return self._EK

    def calc_QK(self):
        self._QK = self.Q + mdot(self.K.T,self.R,self.K)
        return self._QK

    def calc_P(self):
        self._P = dlyap_obj(self,matrixtype='P')
        return self._P

    def calc_S(self):
        self._S = dlyap_obj(self,matrixtype='S')
        return self._S

    def calc_PS(self,P00=None,S00=None,algo='iterative'):
        self._P,self._S = dlyap_obj(self,matrixtype='PS',algo=algo,P00=P00,S00=S00)
        return self._P,self._S

    def calc_c(self):
        if is_pos_def(self.P):
            self._c = np.trace(np.dot(self.P,self.S0))
        else:
            self._c = np.inf
        return self._c

    def calc_PKare(self):
        self._Pare,self._Kare = dare_obj(self)
        return self._Pare,self._Kare

    def calc_ccare(self):
        if is_pos_def(self.Pare):
            self._ccare = np.trace(np.dot(self.Pare,self.S0))
        else:
            self._ccare = np.inf
        return self._ccare

    def calc_grad(self):
        if (not hasattr(self,'_P')) and (not hasattr(self,'_S')):
            self.calc_PS() # This is to save on dlyap iterations
        self._grad,self._RK,self._EK = lqr_gradient(self)
        return self._grad,self._RK,self._EK

    def del_lqr_cl(self):
        if hasattr(self,'_QK'):
            del self._QK
        if hasattr(self,'_P'):
            del self._P
        if hasattr(self,'_S'):
            del self._S
        if hasattr(self,'_c'):
            del self._c
        if hasattr(self,'_Pare'):
            del self._Pare
        if hasattr(self,'_Kare'):
            del self._Kare
        if hasattr(self,'_ccare'):
            del self._ccare
        if hasattr(self,'_grad'):
            del self._grad
        if hasattr(self,'_RK'):
            del self._RK
        if hasattr(self,'_EK'):
            del self._EK

    def del_cl(self):
        self.del_lti_cl()
        self.del_lqr_cl()


class LTISysMult(LTISys):
    def __init__(self,A,B,a,Aa,b,Bb):
        LTISys.__init__(self,A,B)
        self._a = a
        self._Aa = Aa
        self._b = b
        self._Bb = Bb
        self._p = len(self._a)
        self._q = len(self._b)

    def set_a(self,a):
        self.del_ltimult_Arand()
        self.del_cl()
        self._a = a
        self._p = len(self._a)
        return self._a

    def set_Aa(self,Aa):
        self.del_ltimult_Arand()
        self.del_cl()
        self._Aa = Aa
        self._p = self._Aa.shape[2]
        return self._Aa

    def set_b(self,b):
        self.del_ltimult_Brand()
        self.del_cl()
        self._b = b
        self._q = len(self._b)
        return self._b

    def set_Bb(self,Bb):
        self.del_ltimult_Brand()
        self.del_cl()
        self._Bb = Bb
        self._q = self._Bb.shape[2]
        return self._Bb

    @property
    def a(self):
        return self._a

    @property
    def Aa(self):
        return self._Aa

    @property
    def b(self):
        return self._b

    @property
    def Bb(self):
        return self._Bb

    @property
    def p(self):
        return self._p

    @property
    def q(self):
        return self._q

    @property
    def Arand(self):
        if not hasattr(self,'_Arand'):
            self.sample_Arand()
        return self._Arand

    @property
    def Brand(self):
        if not hasattr(self,'_Brand'):
            self.sample_Brand()
        return self._Brand

    @property
    def AKrand(self):
        if not hasattr(self,'_AKrand'):
            self.sample_AKrand()
        return self._AKrand

    def sample_Arand(self):
        self._Arand = np.copy(self.A)
        for i in range(self.p):
            self._Arand += (self.a[i]**0.5)*randn()*self.Aa[:,:,i]
        return self._Arand

    def sample_Brand(self):
        self._Brand = np.copy(self.B)
        for j in range(self.q):
            self._Brand += (self.b[j]**0.5)*randn()*self.Bb[:,:,j]
        return self._Brand

    def sample_AKrand(self):
        self.sample_Arand()
        self.sample_Brand()
        self._AKrand = self.Arand+np.dot(self.Brand,self.K)
        return self._AKrand

    def del_ltimult_Arand(self):
        if hasattr(self,'_Arand'):
            del self._Arand

    def del_ltimult_Brand(self):
        if hasattr(self,'_Brand'):
            del self._Brand

    def del_ltimult_cl(self):
        if hasattr(self,'_AKrand'):
            del self._AKrand

    def del_cl(self):
        self.del_lti_cl()
        self.del_ltimult_cl()


class LQRSysMult(LTISysMult,LQRSys):
    def __init__(self,A,B,a,Aa,b,Bb,Q,R,S0):
        LQRSys.__init__(self,A,B,Q,R,S0)
        LTISysMult.__init__(self,A,B,a,Aa,b,Bb)

    def del_cl(self):
        self.del_lti_cl()
        self.del_ltimult_cl()
        self.del_lqr_cl()

###############################################################################
# Dynamics math functions
###############################################################################

# Simulate a trajectory of the system
def sim_traj_obj(obj,x0,nt,feedback=False):
    # Initialize
    X = np.zeros([obj.n,nt])
    X[:,0] = x0

    # Iterate
    if not feedback:
        if isinstance(obj,LTISys) and not isinstance(obj,LTISysMult):
            for i in range(nt-1):
                # Transition the state
                X[:,i+1] = np.dot(obj.A,X[:,i])
        elif isinstance(obj,LTISys) and isinstance(obj,LTISysMult):
            for i in range(nt-1):
                # Randomly sample using multiplicative noise
                obj.sample_Arand()
                # Transition the state using multiplicative noise
                X[:,i+1] = np.dot(obj.Arand,X[:,i])
    else:
        if isinstance(obj,LTISys) and not isinstance(obj,LTISysMult):
            for i in range(nt-1):
                # Transition the state using feedback
                X[:,i+1] = np.dot(obj.AK,X[:,i])
        elif isinstance(obj,LTISys) and isinstance(obj,LTISysMult):
            for i in range(nt-1):
                # Randomly sample using multiplicative noise
                obj.sample_AKrand()
                # Transition the state using feedback and multiplicative noise
                X[:,i+1] = np.dot(obj.AKrand,X[:,i])
    return X

def dlyap_obj(obj,matrixtype='P',algo='iterative',show_warn=False,check_pd=False,P00=None,S00=None):
    # obj is a LQRSys or LQRSysMult instance
    if isinstance(obj,LQRSys) and not isinstance(obj,LQRSysMult):
        if matrixtype=='P':
            AA = obj.AK.T
            QQ = obj.Q + sympart(mdot(obj.K.T,obj.R,obj.K))
            P = dlyap(AA,QQ)
            if check_pd:
                if not is_pos_def(P):
                    P = np.full_like(P,np.inf)
        elif matrixtype=='S':
            AA = obj.AK
            QQ = obj.S0
            S = dlyap(AA,QQ)
            if check_pd:
                if not is_pos_def(S):
                    S = np.full_like(S,np.inf)
        elif matrixtype=='PS':
            P = dlyap_obj(obj,'P',algo,show_warn,check_pd,P00,S00)
            S = dlyap_obj(obj,'S',algo,show_warn,check_pd,P00,S00)
        if matrixtype=='P':
            return P
        elif matrixtype=='S':
            return S
        elif matrixtype=='PS':
            return P,S
    elif isinstance(obj,LQRSys) and isinstance(obj,LQRSysMult):
        return dlyap_mult(obj.A,obj.B,obj.K,obj.a,obj.Aa,obj.b,
                          obj.Bb,obj.Q,obj.R,obj.S0,matrixtype=matrixtype,
                          algo=algo,show_warn=show_warn,check_pd=check_pd,
                          P00=P00,S00=S00)
def dlyap_mult(A,B,K,a,Aa,b,Bb,Q,R,S0,matrixtype='P',algo='iterative',show_warn=False,check_pd=False,P00=None,S00=None):
    n = A.shape[1]
    n2 = n*n
    p = len(a)
    q = len(b)
    AK = A + np.dot(B,K)
    stable = True
    stable2 = True
    if algo=='linsolve':
        if matrixtype=='P':
            # Intermediate terms
            Aunc_P = np.zeros([n2,n2])
            for i in range(p):
                Aunc_P = Aunc_P + a[i]*kron(Aa[:,:,i].T)
            BKunc_P = np.zeros([n2,n2])
            for j in range(q):
                BKunc_P = BKunc_P + b[j]*kron(np.dot(K.T,Bb[:,:,j].T))
            # Compute matrix and vector for the linear equation solver
            Alin_P = np.eye(n2) - kron(AK.T) - Aunc_P - BKunc_P
            blin_P = vec(Q) + np.dot(kron(K.T),vec(R))
            # Solve linear equations
            xlin_P = la.solve(Alin_P,blin_P)
            # Reshape
            P = np.reshape(xlin_P,[n,n])
            if check_pd:
                stable = is_pos_def(P)
        elif matrixtype=='S':
            # Intermediate terms
            Aunc_S = np.zeros([n2,n2])
            for i in range(p):
                Aunc_S = Aunc_S + a[i]*kron(Aa[:,:,i])
            BKunc_S = np.zeros([n2,n2])
            for j in range(q):
                BKunc_S = BKunc_S + b[j]*kron(np.dot(Bb[:,:,j],K))
            # Compute matrix and vector for the linear equation solver
            Alin_S = np.eye(n2) - kron(AK) - Aunc_S - BKunc_S
            blin_S = vec(S0)
            # Solve linear equations
            xlin_S = la.solve(Alin_S,blin_S)
            # Reshape
            S = np.reshape(xlin_S,[n,n])
            if check_pd:
                stable = is_pos_def(S)
        elif matrixtype=='PS':
            P = dlyap_mult(A,B,K,a,Aa,b,Bb,Q,R,S0,matrixtype='P',algo='linsolve')
            S = dlyap_mult(A,B,K,a,Aa,b,Bb,Q,R,S0,matrixtype='S',algo='linsolve')

    elif algo=='iterative':
        # Implicit iterative solution to generalized discrete Lyapunov equation
        # Inspired by https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7553367
        # In turn inspired by https://pdf.sciencedirectassets.com/271503/1-s2.0-S0898122100X0020X/1-s2.0-089812219500119J/main.pdf?x-amz-security-token=AgoJb3JpZ2luX2VjECgaCXVzLWVhc3QtMSJIMEYCIQD#2F00Re8b3wnBnFpZQrjkOeXrNI4bYZ1J6#2F9BcJptZYAAIhAOQjTsZX573uFFEr7QveHx4NaZYWxlZfRN6hr5h1GJWWKuMDCOD#2F#2F#2F#2F#2F#2F#2F#2F#2F#2FwEQAhoMMDU5MDAzNTQ2ODY1IgxqkGe6i8wGmEj6YAwqtwNDKbotYDExP2D6PO8MrlIKYmHCtJhTu1CXLv0N5NKsYT90H2rJTNU0MvqsUsnXtbn6C9t9ed31XTf#2BHc7KrGmpOils7zgrjV1QG4LP0Fu2OcT4#2F#2FOGLWNvVjWY9gOLEHSeG5LhvBbxJiZVrI#2Bm1QAIVz5dxH5DVB27A2e9OmRrswrpPWuxQV#2BUvLkz2dVM4qSkvaDA#2F3KEJk9s0XE74mjO4ZHX7d9Q2aYwxsvFbII6Hms#2FZmB6125tBTwzd0K5xDit5kaoiYadOetp3M#2FvCdaiO0QeQwkV4#2FUaprOIIQGwJaMJuMNe7xInQxF#2B#2FmER81JhWEpBHBmz#2F5p0d2tU7F2oTDc2OR#2BV5dTKab47zgUw648fDT7ays0TQzqTMGnGcX9wIQpxSCam2E8Bhg6tsEs0#2FudddgnsiId368q70xai6ucMfabMSCqnv7O0OZqPVwY5b7qk4mxKIehpIzV6rrtXSAGrH95WGlgGz#2Fhmg9Qq6AUtb8NSqyYw0uZ00E#2FPZmNTnI3nwxjOA5qhyEbw3uXogRwYrv0dLkd50s7oO3mlYFeJDBurhx11t9p94dFqQq7sDY70m#2F4xMNCcmuUFOrMBY1JZuqtQ7QFBVbgzV#2B4xSHV6#2FyD#2F4ezttczZY3eSASJpdC4rjYHXcliiE7KOBHivchFZMIYeF3J4Nvn6UykX5sNfRANC2BDPrgoCQUp95IE5kgYGB8iEISlp40ahVXK62GhEASJxMjJTI9cJ2M#2Ff#2BJkwmqAGjTsBwjxkgiLlHc63rBAEJ2e7xoTwDDql3FSSYcvKzwioLfet#2FvXWvjPzz44tB3#2BTvYamM0uq47XPlUFcTrw#3D&AWSAccessKeyId=ASIAQ3PHCVTYWXNG3EKG&Expires=1554423148&Signature=Ysi80usGGEjPCvw#2BENTSD90NgVs#3D&hash=e5cf30dad62b0b57d7b7f5ba524cccacdbb36d2f747746e7fbebb7717b415820&host=68042c943591013ac2b2430a89b270f6af2c76d8dfd086a07176afe7c76c2c61&pii=089812219500119J&tid=spdf-a9dae0e9-65fd-4f31-bf3f-e0952eb4176c&sid=5c8c88eb95ed9742632ae57532a4a6e1c6b1gxrqa&type=client
        # Faster for large systems i.e. >50 states
        # Options
        max_iters = 1000
        epsilon_P = 1e-5
        epsilon_S = 1e-5
        # Initialize
        if matrixtype=='P' or matrixtype=='PS':
            if P00 is None:
                P = np.copy(Q)
            else:
                P = P00
        if matrixtype=='S' or matrixtype=='PS':
            if S00 is None:
                S = np.copy(S0)
            else:
                S = S00
        iterc = 0
        converged = False
        stop = False
        while not stop:
            if matrixtype=='P' or matrixtype=='PS':
                P_prev = P
                APAunc = np.zeros([n,n])
                for i in range(p):
                    APAunc += a[i]*mdot(Aa[:,:,i].T,P,Aa[:,:,i])
                BPBunc = np.zeros([n,n])
                for j in range(q):
                    BPBunc += b[j]*mdot(K.T,Bb[:,:,j].T,P,Bb[:,:,j],K)
                AAP = AK.T
                QQP = sympart(Q + mdot(K.T,R,K) + APAunc + BPBunc)
                P = dlyap(AAP,QQP)
                if np.any(np.isnan(P)) or np.any(np.isinf(P)) or not is_pos_def(P):
                    stable = False
                try:
                    converged_P = la.norm(P-P_prev,2)/la.norm(P_prev,2) < epsilon_P
                    stable2 = True
                except:
                    # print(P)
                    # print(P_prev)
                    # print(P-P_prev)
                    # print(la.norm())
                    stable2 = False
                    # print('')
            if matrixtype=='S' or matrixtype=='PS':
                S_prev = S
                ASAunc = np.zeros([n,n])
                for i in range(p):
                    ASAunc += a[i]*mdot(Aa[:,:,i],S,Aa[:,:,i].T)
                BSBunc = np.zeros([n,n])
                for j in range(q):
                    BSBunc = b[j]*mdot(Bb[:,:,j],K,S,K.T,Bb[:,:,j].T)
                AAS = AK
                QQS = sympart(S0 + ASAunc + BSBunc)
                S = dlyap(AAS,QQS)
                if np.any(np.isnan(S)) or not is_pos_def(S):
                    stable = False
                converged_S = la.norm(S-S_prev,2)/la.norm(S,2) < epsilon_S
            # Check for stopping condition
            if matrixtype=='P':
                converged = converged_P
            elif matrixtype=='S':
                converged = converged_S
            elif matrixtype=='PS':
                converged = converged_P and converged_S
            if iterc >= max_iters:
                stable = False
            else:
                iterc += 1
            stop = converged or not stable or not stable2
#        print('\ndlyap iters = %s' % str(iterc))

    elif algo=='finite_horizon':
        P = np.copy(Q)
        Pt = np.copy(Q)
        S = np.copy(Q)
        St = np.copy(Q)
        converged = False
        stop = False
        while not stop:
            if matrixtype=='P' or matrixtype=='PS':
                APAunc = np.zeros([n,n])
                for i in range(p):
                    APAunc += a[i]*mdot(Aa[:,:,i].T,Pt,Aa[:,:,i])
                BPBunc = np.zeros([n,n])
                for j in range(q):
                    BPBunc += b[j]*mdot(K.T,Bb[:,:,j].T,Pt,Bb[:,:,j],K)
                Pt = mdot(AK.T,Pt,AK)+APAunc+BPBunc
                P += Pt
                converged_P = np.abs(Pt).sum() < 1e-15
                stable = np.abs(P).sum() < 1e10
            if matrixtype=='S' or matrixtype=='PS':
                ASAunc = np.zeros([n,n])
                for i in range(p):
                    ASAunc += a[i]*mdot(Aa[:,:,i],St,Aa[:,:,i].T)
                BSBunc = np.zeros([n,n])
                for j in range(q):
                    BSBunc = b[j]*mdot(Bb[:,:,j],K,St,K.T,Bb[:,:,j].T)
                St = mdot(AK,Pt,AK.T)+ASAunc+BSBunc
                S += St
                converged_S = np.abs(St).sum() < 1e-15
                stable = np.abs(S).sum() < 1e10
            if matrixtype=='P':
                converged = converged_P
            elif matrixtype=='S':
                converged = converged_S
            elif matrixtype=='PS':
                converged = converged_P and converged_S
            stop = converged or not stable
    if not stable:
        P = None
        S = None
        if show_warn:
            warnings.simplefilter('always', UserWarning)
            warn('System is possibly not mean-square stable')
    if matrixtype=='P':
        return P
    elif matrixtype=='S':
        return S
    elif matrixtype=='PS':
        return P,S

def dare_obj(obj):
    if isinstance(obj,LQRSys) and not isinstance(obj,LQRSysMult):
        Pare = dare(obj.A,obj.B,obj.Q,obj.R)
        Kare = -la.solve((obj.R+mdot(obj.B.T,Pare,obj.B)),
                         mdot(obj.B.T,Pare,obj.A))
        return Pare,Kare
    elif isinstance(obj,LQRSys) and isinstance(obj,LQRSysMult):
        return dare_mult(obj.A,obj.B,obj.a,obj.Aa,obj.b,obj.Bb,obj.Q,obj.R)

def dare_mult(A,B,a,Aa,b,Bb,Q,R,algo='iterative',show_warn=False):
    if algo=='iterative':
        # Options
        max_iters = 1000
        epsilon = 1e-6
        Pelmax = 1e20
        n = A.shape[1]
        m = B.shape[1]
        p = len(a)
        q = len(b)
        # Initialize
        P = Q
        iterc = 0
        stop_early = False
        converged = False
        stop = False

        while not stop:
            # Record previous iterate
            P_prev = P
            # Certain part
            APAcer = mdot(A.T,P,A)
            BPBcer = mdot(B.T,P,B)
            # Uncertain part
            APAunc = np.zeros([n,n])
            for i in range(p):
                APAunc += a[i]*mdot(Aa[:,:,i].T,P,Aa[:,:,i])
            BPBunc = np.zeros([m,m])
            for j in range(q):
                BPBunc += b[j]*mdot(Bb[:,:,j].T,P,Bb[:,:,j])
            APAsum = APAcer+APAunc
            BPBsum = BPBcer+BPBunc
            # Recurse
            P = Q + APAsum - mdot(A.T,P,B,la.solve(R+BPBsum,B.T),P,A)
            # Check for stopping condition
            if la.norm(P-P_prev,'fro')/la.norm(P,'fro') < epsilon:
                converged = True
            if iterc >= max_iters or np.any(np.abs(P)>Pelmax):
                stop_early = True
            else:
                iterc += 1
            stop = converged or stop_early
        # Compute the gains
        if stop_early:
            if show_warn:
                warnings.simplefilter('always', UserWarning)
                warn("Recursion failed, ensure system is mean square stabilizable "
                     "or increase maximum iterations")
            P = None
            K = None
        else:
            K = -mdot(la.solve(R+BPBsum,B.T),P,A)
    return P,K


def lqr_gradient(obj):
    """Calculate the cost (policy) gradient of an LQR system"""
    # obj is a LQRSys or LQRSysMult instance

    if obj.P is None:
        raise Exception('Attempted to compute gradient of system with undefined cost P matrix!')

    if isinstance(obj, LQRSys) and not isinstance(obj, LQRSysMult):
        RK = obj.R + mdot(obj.B.T,obj.P,obj.B)
    elif isinstance(obj, LQRSys) and isinstance(obj, LQRSysMult):
        # Uncertain part
        BPBunc = np.zeros([obj.m,obj.m])
        for j in range(obj.q):
            BPBunc += obj.b[j]*mdot(obj.Bb[:,:,j].T, obj.P, obj.Bb[:,:,j])
        RK = obj.R + mdot(obj.B.T, obj.P, obj.B) + BPBunc
    EK = np.dot(RK,obj.K) + mdot(obj.B.T,obj.P,obj.A)
    # Compute gradient
    grad = 2*np.dot(EK,obj.S)
    return grad, RK, EK


def check_mss_obj(obj):
    """Check whether or not system is closed-loop mean-square stable"""
    # Options
    max_iters = 1000
    epsilon = 1e-6
    # Initialize
    iterc = 0
    stop_early = False
    converged = False
    stop = False
    x0 = np.ones([obj.n,1])
    S00 = np.dot(x0,x0.T)
    S00n = la.norm(S00,'fro')
    S = S00
#    norm_hist = np.zeros(max_iters+1)
    while not stop:
        # Record previous iterate
        S_prev = S
#        norm_hist[iterc] = la.norm(S)
        # Recurse
        if isinstance(obj,LQRSys) and not isinstance(obj,LQRSysMult):
            S = mdot(obj.AK,S,obj.AK.T)
        elif isinstance(obj,LQRSys) and isinstance(obj,LQRSysMult):
            # Intermediate expressions
            ASAunc = np.zeros([obj.n,obj.n])
            for i in range(obj.p):
                ASAunc += obj.a[i]*mdot(obj.Aa[:,:,i],S,obj.Aa[:,:,i].T)
            BSBunc = np.zeros([obj.n,obj.n])
            for j in range(obj.q):
                BSBunc += obj.b[j]*mdot(obj.Bb[:,:,j],obj.K,S,obj.K.T,obj.Bb[:,:,j].T)
            S = mdot(obj.AK,S,obj.AK.T) + ASAunc + BSBunc
        # Check for stopping condition
        if la.norm(S-S_prev,'fro')/S00n < epsilon:
            converged = True
        if iterc >= max_iters:
            stop_early = True
        else:
            iterc += 1
        stop = converged or stop_early
#    norm_hist = norm_hist[0:iterc]
    return converged


def check_olmss(obj):
    """"Check whether or not system is open-loop mean-square stable"""
    # Check if open-loop mss
    K00 = np.zeros([obj.m,obj.n])
    SS00 = copy(obj)
    SS00.setK(K00)
    P = dlyap_obj(SS00,algo='iterative',show_warn=False)
    if P is None:
        print('System is NOT open-loop mean-square stable')
        olmss = False
    else:
        print('System is open-loop mean-square stable')
        olmss = True
    return olmss


def mateqn_test(obj):
    from time import time
    # Matrix equation tests
    t_start = time()
    obj.Kare
    t_end = time()
    print('Kare calculated by Riccati equation after %.3f seconds' % (t_end-t_start))

    obj.setK(obj.Kare)
    t_start = time()
    obj.P
    t_end = time()
    print('P calculated by dlyap equation after %.3f seconds' % (t_end-t_start))
#    print('difference')
#    print(obj.P-obj.Pare)
#    print(la.norm(obj.P-obj.Pare))
    print(obj.mss)



###############################################################################
# Main
###############################################################################
if __name__ == "__main__":

    from ltimultgen import gen_system_mult
    from plotting import plot_traj

    SS = gen_system_mult()
    SS.setK(SS.Kare)
    print(SS.mss)

#    # Test parameter resets
#    SS.setK(Kz)
#    print(SS.P)
#    SS.set_A(0.9*Az)
#    print(SS.P)
#    SS.set_B(0.9*Bz)
#    print(SS.P)
#    SS.set_Q(0.9*Qz)
#    print(SS.P)
#    SS.set_R(1.1*Rz)
#    print(SS.P)
#    SS.set_a(0.9*az)
#    print(SS.P)
#    SS.set_b(0.9*bz)
#    print(SS.P)
#    SS.set_Aa(0.9*Aaz)
#    print(SS.P)
#    SS.set_Bb(0.9*Bbz)
#    print(SS.P)
#    SS.set_S0(np.random.rand(nz,nz))
#    print(SS.P)


    nt = 20
    nr = 10
    Xall_ol = np.zeros([SS.n,nt,nr])
    Xall_cl = np.zeros([SS.n,nt,nr])

    # Simulate trajectories
    for i in range(nr):
        x0 = np.ones(SS.n)
#        x0 = randn(nz)
#        x0 = x0/la.norm(x0)
        Xall_ol[:,:,i] = SS.sim_ol(x0,nt)
        Xall_cl[:,:,i] = SS.sim_cl(x0,nt)

    # Plot trajectories
    plot_type='split'
    plot_traj(Xall_ol,plot_type=plot_type)
    plot_traj(Xall_cl,plot_type=plot_type)
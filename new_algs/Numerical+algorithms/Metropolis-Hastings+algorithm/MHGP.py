import GPy
import GPyOpt
import numpy as np
from math import *
import pickle
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF

#This is an accelerated Metropolis-Hastings algorithm based on Bayesian optimization and Gaussian process.
class MHGP(object):
    
    def __init__(self, f, bounds, xInit, GPVariance = 0.1, GPLengthScale = 0.1, GPNoiseVariance = 0.01, BO_max_iteration = 100, 
                 GPTrainIteration = 1000, totalIteration = 100000, threshold = 0.005, isVerbose = 1):
        self.posterior = f
        self.suppliedBounds = bounds
        self.numberOfFuncEvals = 0
        #parameters for the program
        self.gpVariance = GPVariance
        self.gpLengthscale = GPLengthScale
        self.gpNoisevariance = GPNoiseVariance
        self.bo_max_iter = BO_max_iteration
        self.endofBurnin = GPTrainIteration
        self.n = totalIteration
        self.threshold = threshold
        self.isVerbose = isVerbose
        self.convertForBounds = True
        self.lowerbounds = np.array([c[0] for c in bounds])
        self.upperbounds = np.array([c[1] for c in bounds])
        self.initialX = None
        self.initialY = None
        if xInit is not None:
            self.initialX = self.xT(xInit, self.lowerbounds, self.upperbounds)
            self.initialY = np.apply_along_axis(self.getTransformedPosteriorValue, 1, self.initialX)
            self.initialY = self.initialY.reshape(self.initialY.size, 1)
            print(self.initialX)
            print(self.initialY)
        self.kernel = RBF(self.gpLengthscale, (1e-3,1e3))
        self.gp = GaussianProcessRegressor(kernel = self.kernel, n_restarts_optimizer=10, alpha=self.gpNoisevariance)
        
    
    def getPosteriorValue(self, x_val):
        self.numberOfFuncEvals += 1
        return self.posterior(x_val)
    
    def getTransformedPosteriorValue(self, x_T):
        addTerm1 = np.sum(np.log(self.upperbounds-self.lowerbounds)) 
        addTerm2 = np.sum(x_T)
        addTerm3 = 2*np.sum(np.log(np.exp(x_T) + 1))
        x = self.xInvT(x_T)
        return self.getPosteriorValue(x) + addTerm1 + addTerm2 - addTerm3
    
    def logit(self, x):
        return np.log(x/(1-x))

    def logitInv(self, x):
        return np.exp(x)/(np.exp(x)+1) #1.0/(1+np.exp(-x))

    def xT(self, x, a, b):
        return self.logit((x-a)/(b-a))

    def xInvT(self, x, a = None, b = None):
        if a is None:
            a = self.lowerbounds
        if b is None:
            b = self.upperbounds
        return a + (b-a)*self.logitInv(x)

    def logposterior_BO(self, x):
        retval = np.empty([1,1])
        currXT = x[0,:]
        retval[0,0] = self.getTransformedPosteriorValue(currXT)
        return -retval
    
    
    def sigmaInverse(self, diagValues,dim):
        s = np.zeros((dim,dim))
        for i in range(dim):
            for j in range(dim):
                if i==j:
                    s[i,j] = 1.0/diagValues
        return s


    def hessianAtPoint(self, pt,lscale,ker_variance,gp_noise,gpx,gpy):
        print('inside hessian calculation')
        print(lscale/1.0)
        print(ker_variance/1.0)
        print(gp_noise/1.0)
        D = pt.size
        H = np.zeros((D,D))
        N = gpy.size
        print(gpx.shape)
        print(gpy.shape)
        lscale = lscale[0]**2
        ker_variance = ker_variance[0]
        sigmaInv = self.sigmaInverse(lscale,D)
        K = np.zeros((N,N))
        print('sigma inverse done', sigmaInv)
        for i in range(N):
            for j in range(N):
                diff = gpx[i,:] - gpx[j,:]
                diffT = np.transpose(diff)
                K[i,j] = ker_variance * np.exp(-0.5*np.dot(np.dot(diffT,sigmaInv),diff))
                if i==j:
                    K[i,j] = K[i,j] + gp_noise
        print('K: ', K)
        Kinv = np.linalg.pinv(K)
        KinvTimesY = np.dot(Kinv,gpy)
        print('Before final n^2 loop')
        for i in range(D):
            for k in range(D):
                if i==k:
                    t = np.zeros(N)
                    for j in range(N):
                        diff = pt - gpx[j,:]
                        diffT = np.transpose(diff)
                        t[j] = ker_variance * np.exp(-0.5*np.dot(np.dot(diffT,sigmaInv),diff))*(1.0/(lscale))*((((gpx[j,i]-pt[i])**2)/(lscale)) -1)
                    H[i,k] = np.dot(t,KinvTimesY)
                else:
                    t = np.zeros(N)
                    for j in range(N):
                        diff = pt - gpx[j,:]
                        diffT = np.transpose(diff)
                        t[j] = ker_variance * np.exp(-0.5*np.dot(np.dot(diffT,sigmaInv),diff))*((gpx[j,i]-pt[i])/(lscale))*((gpx[j,k]-pt[k])/(lscale))
                    H[i,k] = np.dot(t,KinvTimesY)
        print(H)
        return H


    
    def covarianceOfProposal(self, meanPoint,lscale,ker_variance,gp_noise,gpx,gpy):
        return np.linalg.inv(-self.hessianAtPoint(meanPoint,lscale,ker_variance,gp_noise[0],gpx,gpy))

    def factorCovariance(self, cov, highscale):
        maxval = np.max(np.diag(cov))
        factor = highscale/maxval
        return np.multiply(cov, factor)


    def evaluate(self, candidate, gpx, gpy):#, kernel, addToGP = True):
        gpx = np.vstack([gpx,candidate])
        likelihood = self.getTransformedPosteriorValue(candidate)
        gpy = np.vstack([gpy, likelihood])
        self.gp.fit(gpx, gpy)
        
        
    def shouldRecalculate(self, new_val,new_mse,old_val,old_mse,cov_new_old):
        mse = new_mse + old_mse - 2*cov_new_old
        return np.sqrt((np.exp(mse)-1)) > self.threshold # SD/mean of the log normal distribution gives this

    def acceptanceRatio(self, new_val,new_mse,old_val,old_mse,cov_new_old):
        mse = new_mse + old_mse - 2*cov_new_old
        return np.exp(new_val - old_val + (mse/2))


    def RunMHGP(self):
        bounds = []
        i = 0
        for i in range(len(self.upperbounds)):
            lower = self.xT(self.lowerbounds[i] + 0.0000001, self.lowerbounds[i], self.upperbounds[i])
            upper = self.xT(self.upperbounds[i] - 0.0000001, self.lowerbounds[i], self.upperbounds[i])
            bounds.append({'name': 'x' + str(i), 'type': 'continuous', 'domain': (lower, upper)})
            i = i + 1  
        print(bounds)
        
        initY = None
        if self.initialY is not None:
            initY = -self.initialY
        myProblem = GPyOpt.methods.BayesianOptimization(self.logposterior_BO, domain=bounds,
                                                      X=self.initialX, Y=initY,
                                                      model_type = 'GP',
                                                      acquisition_type='EI', num_cores=4)
        myProblem.run_optimization(self.bo_max_iter)
        gpx = myProblem.X
        gpy = -myProblem.Y
        bo_max_point = np.copy(myProblem.x_opt)
        print('BO max point', bo_max_point)
        
        f = open('dump_gpx_gpy.pickle','wb')
        pickle.dump({'gpx':gpx, 'gpy':gpy, 'bo_max_point':bo_max_point}, f, pickle.HIGHEST_PROTOCOL)
        f.close()
            
        kernel = GPy.kern.RBF(input_dim=len(self.suppliedBounds), variance=self.gpVariance, lengthscale=self.gpLengthscale)
        m = GPy.models.GPRegression(gpx,gpy,kernel,noise_var=self.gpNoisevariance)
        m.rbf.lengthscale.constrain_bounded(0.001,10)
        m.rbf.variance.constrain_bounded(0.001, 1000)
        m.Gaussian_noise.variance.constrain_fixed(self.gpNoisevariance)
        m.optimize(clear_after_finish=True)    
        
        covProposal = self.covarianceOfProposal(bo_max_point,kernel.lengthscale, kernel.variance, m.Gaussian_noise, gpx, gpy)
        print('Covariance of Proposal', covProposal)
        W,v = np.linalg.eig(covProposal)
        print('Eigens',W,v)
        xT = bo_max_point 
        x = self.xInvT(xT)
        
        samplesTaken = np.array([x]) #initialize the samples vector. this first point will be discarded while plotting
        allSamples = np.array([x]) #this is only for plotting sequence of samples
        sampleChainMHGP = np.array([x])
        sampleChainTransSpace = np.array([xT])
        
        acceptanceProbability = 0
        wasXReadFromGP = False
        isCandidateReadFromGP = False
        isOldReadFromGP = False

        self.gp.fit(gpx, gpy)
        
        for i in range(1, self.n):
            sampleChainMHGP = np.vstack([sampleChainMHGP,x])
            sampleChainTransSpace = np.vstack([sampleChainTransSpace,xT])
            
            candidateT = np.random.multivariate_normal(xT,covProposal) # generate random number from multivariate Gaussian with mean at previous point
            candidate = self.xInvT(candidateT)
            
            meanVal, mse = self.gp.predict(np.vstack([candidateT,xT]), return_cov=True)#gp.predict(np.vstack([candidate,x]),True)
            
            if i < self.endofBurnin and self.shouldRecalculate(meanVal[0,0],mse[0,0],meanVal[1,0],mse[1,1],mse[0,1]): 
                if wasXReadFromGP == False: # if last x was evaluated then evaluate candidate too
                    self.evaluate(candidateT, gpx, gpy)   
                    isCandidateReadFromGP = False
                else:
                    self.evaluate(xT, gpx, gpy) # last x was read from GP, now evaluate x
                    wasXReadFromGP = False
                    meanVal, mse = self.gp.predict(np.vstack([candidateT,xT]), return_cov=True)
                    # see if candidate still has high variance, if yes then evaluate candidate
                    if self.shouldRecalculate(meanVal[0,0],mse[0,0],meanVal[1,0],mse[1,1],mse[0,1]): 
                        self.evaluate(candidateT, gpx, gpy)
                        isCandidateReadFromGP = False
                    else:
                        isCandidateReadFromGP = True
            elif i < self.endofBurnin:
                isCandidateReadFromGP = True
            
            meanVal, mse = self.gp.predict(np.vstack([candidateT,xT]), return_cov=True)
            accratio = self.acceptanceRatio(meanVal[0,0],mse[0,0],meanVal[1,0],mse[1,1],mse[0,1])
            acceptanceProbability = min([1.,accratio])  

            if i%100==0 and i<=self.endofBurnin and self.isVerbose == 1: #print information after each 200 iteration. for debugging purposes.
                print('iteration:'+str(i)+' calls:'+str(self.numberOfFuncEvals))
                print('candidate:'+str(candidate)+' x:'+str(x))
                print(meanVal)
                print(mse)
                print(accratio)

            u = np.random.uniform(0,1)
            allSamples = np.vstack([allSamples,candidate]) # this is only for plotting sequence of samples
            if u < acceptanceProbability:
                xT = candidateT
                x = self.xInvT(xT)
                wasXReadFromGP = isCandidateReadFromGP
                if i > self.endofBurnin: # only second half of the iterations are taken and burn-ins are thrown away
                    samplesTaken = np.vstack([samplesTaken,candidate])                    

        return samplesTaken, self.numberOfFuncEvals, covProposal, myProblem.x_opt, sampleChainMHGP, sampleChainTransSpace





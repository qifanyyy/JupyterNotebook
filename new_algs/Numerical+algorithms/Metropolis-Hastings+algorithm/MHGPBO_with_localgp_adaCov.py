import GPy
import GPyOpt
import numpy as np
from math import *
import pickle
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from pandas import pandas as pd
import scipy.stats as st

#This is an accelerated Metropolis-Hastings algorithm based on Bayesian optimization and Gaussian process.
class MHGPBO(object):
    
    def __init__(self, f, dim, lowerbounds, upperbounds, xInit = None, 
                 GPVariance = 0.1, GPLengthScale = 0.1, GPNoiseVariance = 0.01, 
                 BO_max_iteration = 100, GPTrainIteration = 1000, totalIteration = 100000, burninPeriod = 1000,
                 threshold = 0.005, maxEntryofCov = 0.0001, isVerbose = 1, logData = True):
        self.posterior = f
        self.dim = dim
        self.numberOfFuncEvals = 0
        #parameters for the program
        self.gpVariance = GPVariance
        self.gpLengthscale = GPLengthScale
        self.gpNoisevariance = GPNoiseVariance
        self.bo_max_iter = BO_max_iteration
        self.endofBurnin = burninPeriod
        self.gpTrainPeriod = GPTrainIteration
        self.n = totalIteration
        self.threshold = threshold
        self.maxEntryofCov = maxEntryofCov
        self.localGPradius = np.sqrt(maxEntryofCov)*6 #radius of local GP is 6 times the maximum standard deviation of proposal
        self.isVerbose = isVerbose
        self.lowerbounds = lowerbounds
        self.upperbounds = upperbounds
        self.gpx = None
        self.gpy = None
        self.localgpx = None
        self.localgpy = None
        self.initialX = None
        self.initialY = None
        if xInit is not None:
            self.initialX = xInit
            self.initialY = self.getPosteriorValue(xInit)                       
        self.kernel = RBF(self.gpLengthscale, (1e-3,1e3))
        self.localgp = GaussianProcessRegressor(kernel = self.kernel, n_restarts_optimizer=10, alpha=self.gpNoisevariance)
        self.df = None
        self.shouldLogData = logData
        self.collist = None
        self.acceptCount = 0
        self.posteriorValues = []
        self.covProposal = None
        
    
    def getPosteriorValue(self, x_val):
        self.numberOfFuncEvals += 1
        return self.posterior(x_val)
    
    def logposterior_BO(self, x):
        retval = np.empty([1,1])
        currX = x[0,:]
        retval[0,0] = self.getPosteriorValue(currX)
        return -retval
    
    
    def sigmaInverse(self, diagValues,dim):
        s = np.zeros((dim,dim))
        for i in range(dim):
            for j in range(dim):
                if i==j:
                    s[i,j] = 1.0/diagValues[i]
        return s

    #This method calculates the Hessian of the GP at the mode (obtained from Bayesian optimization)
    def hessianAtPoint(self, pt,lscale,ker_variance,gp_noise,gpx,gpy):
        D = pt.size
        H = np.zeros((D,D))
        N = gpy.size
        lscale = lscale**2
        if lscale.ndim == 1:
            lscale = np.repeat(lscale, D)
        ker_variance = ker_variance[0]
        sigmaInv = self.sigmaInverse(lscale,D)
        K = np.zeros((N,N))
        for i in range(N):
            for j in range(N):
                diff = gpx[i,:] - gpx[j,:]
                diffT = np.transpose(diff)
                K[i,j] = ker_variance * np.exp(-0.5*np.dot(np.dot(diffT,sigmaInv),diff))
                if i==j:
                    K[i,j] = K[i,j] + gp_noise
        Kinv = np.linalg.pinv(K)
        KinvTimesY = np.dot(Kinv,gpy)
        for i in range(D):
            for k in range(D):
                if i==k:
                    t = np.zeros(N)
                    for j in range(N):
                        diff = pt - gpx[j,:]
                        diffT = np.transpose(diff)
                        t[j] = ker_variance * np.exp(-0.5*np.dot(np.dot(diffT,sigmaInv),diff))*(1.0/(lscale[i]))*((((gpx[j,i]-pt[i])**2)/(lscale[i])) -1)
                    H[i,k] = np.dot(t,KinvTimesY)
                else:
                    t = np.zeros(N)
                    for j in range(N):
                        diff = pt - gpx[j,:]
                        diffT = np.transpose(diff)
                        t[j] = ker_variance * np.exp(-0.5*np.dot(np.dot(diffT,sigmaInv),diff))*((gpx[j,i]-pt[i])/(lscale[i]))*((gpx[j,k]-pt[k])/(lscale[k]))
                    H[i,k] = np.dot(t,KinvTimesY)
        return H


    
    def covarianceOfProposal(self, meanPoint,lscale,ker_variance,gp_noise,gpx,gpy):
        return np.linalg.inv(-self.hessianAtPoint(meanPoint,lscale,ker_variance,gp_noise[0],gpx,gpy))

    def logData(self, i, x, candidate, meanVal, mse, secmeanVal, secmse, accratio, isaccepted):
        if self.df is None:
            self.collist = ['pred1_mean_cand','pred1_mean_x','pred1_mse_cand','pred1_mse_x','pred1_mse_cov',
                       'pred2_mean_cand','pred2_mean_x','pred2_mse_cand','pred2_mse_x','pred2_mse_cov',
                       'accratio','isaccepted','evaluationSoFar']
            self.df = pd.DataFrame(index = range(self.n), 
                                   columns = self.collist + ['x'+ str(i) for i in range(self.dim)] + 
                                             ['cand' + str(i) for i in range(self.dim)])
        self.df.iloc[i, :5] = meanVal[0,0], meanVal[1,0], mse[0,0], mse[1,1], mse[0,1]
        self.df.iloc[i, 5:10] = secmeanVal[0,0], secmeanVal[1,0], secmse[0,0], secmse[1,1], secmse[0,1]
        self.df.iloc[i, 10] = accratio
        self.df.iloc[i, 11] = isaccepted
        self.df.iloc[i, 12] = self.numberOfFuncEvals
        self.df.iloc[i, len(self.collist):len(self.collist)+self.dim] = x
        self.df.iloc[i, len(self.collist)+self.dim:] = candidate

    def printInfo(self, i, x, candidate, meanVal, mse, accratio):
        print('iteration:'+str(i)+' calls:'+str(self.numberOfFuncEvals) + ' acceptcount:' + str(self.acceptCount))
        print('candidate:'+str(candidate)+' x:'+str(x))
        print('Global GP size:'+str(self.gpx.shape[0])+' Local GP size:'+str(self.localgpx.shape[0]))
        print(meanVal)
        print(mse)
        print(accratio)        


    def setLocalGPvarsAround(self, point1, point2):
        numrows = self.gpx.shape[0]
        extraradius = 0.0
        while True:
            uppers = point1 + self.localGPradius + extraradius
            lowers = point1 - self.localGPradius - extraradius
            firstfilter = np.repeat(True, numrows)
            for i in range(self.gpx.shape[1]):
                firstfilter = firstfilter & (self.gpx[:,i] > lowers[i]) & (self.gpx[:,i] < uppers[i])
            uppers = point2 + self.localGPradius
            lowers = point2 - self.localGPradius
            secondfilter = np.repeat(True, numrows)
            for i in range(self.gpx.shape[1]):
                secondfilter = secondfilter & (self.gpx[:,i] > lowers[i]) & (self.gpx[:,i] < uppers[i])
            filterdIndices = firstfilter | secondfilter
            self.localgpx = self.gpx[filterdIndices]
            self.localgpy = self.gpy[filterdIndices]
            if self.localgpx.shape[0] > 150:
                randrows = np.random.choice(self.localgpx.shape[0], 150, replace = False)
                self.localgpx = np.copy(self.localgpx[randrows,:])
                self.localgpy = np.copy(self.localgpy[randrows,:])
            if self.localgpx.shape[0] == 0:
                extraradius += self.localGPradius/2
            else:
                break


    def evaluate(self, candidate):
        self.gpx = np.vstack([self.gpx,candidate])
        self.localgpx = np.vstack([self.localgpx,candidate])
        likelihood = self.getPosteriorValue(candidate)
        self.gpy = np.vstack([self.gpy, likelihood])
        self.localgpy = np.vstack([self.localgpy, likelihood])
        self.localgp.fit(self.localgpx, self.localgpy)
        
    
    def checkCandidateForBounds(self, candidate):
        if self.lowerbounds is not None and not np.all(candidate > self.lowerbounds):
            return False
        if self.upperbounds is not None and not np.all(candidate < self.upperbounds):
            return False
        return True
    
        
    def shouldRecalculate(self, new_val,new_mse,old_val,old_mse,cov_new_old):
        mse = new_mse + old_mse - 2*cov_new_old
        calcval = np.sqrt((np.exp(mse)-1))
        return calcval > self.threshold # SD/mean of the log normal distribution gives this

    def acceptanceRatio(self, new_val,new_mse,old_val,old_mse,cov_new_old):
        mse = new_mse + old_mse - 2*cov_new_old
        return np.exp(new_val - old_val + (mse/2))

    def getGPprediction(self, x, cand, setLocalGPbounds = False):
        meanVal, mse = self.localgp.predict(np.vstack([cand,x]), return_cov=True)
        # if current local GP is too uncertain then recalculate the bounds of local GP and then refit, given setLocalGPbounds param is True
        if setLocalGPbounds and self.shouldRecalculate(meanVal[0,0],mse[0,0],meanVal[1,0],mse[1,1],mse[0,1]):
            self.setLocalGPvarsAround(x, cand)
            self.localgp.fit(self.localgpx, self.localgpy)
            meanVal, mse = self.localgp.predict(np.vstack([cand,x]), return_cov=True)
        return meanVal, mse

    def scaleCovariance(self, multiplyFactor = 1.0):
        factor = self.maxEntryofCov/np.max(self.covProposal)
        #self.localGPradius = np.sqrt(self.maxEntryofCov*multiplyFactor)*6
        return factor*multiplyFactor*self.covProposal

    def getCovMultiplyFactor(self, curpostval):
        return 10**((100 - st.percentileofscore(self.posteriorValues, curpostval) - 50)/50)

    def performBayesianOptimization(self):
        bounds = []
        for i in range(self.dim):            
            bounds.append({'name': 'x' + str(i), 'type': 'continuous', 'domain': (self.lowerbounds[i], self.upperbounds[i])})            
        
        foundPosDefProposal = False
        borun = 0
        while not foundPosDefProposal:
            initY = None
            if self.initialY is not None:
                initY = -self.initialY
            myProblem = GPyOpt.methods.BayesianOptimization(self.logposterior_BO, domain=bounds,
                                                      X=self.initialX, Y=initY,
                                                      model_type = 'GP',
                                                      acquisition_type='EI', num_cores=4)
            myProblem.run_optimization(self.bo_max_iter)
            bo_max_point = np.copy(myProblem.x_opt)        
        
            kernel = GPy.kern.RBF(input_dim=self.dim, variance=self.gpVariance, lengthscale=self.gpLengthscale[0])#, ARD=True)
            m = GPy.models.GPRegression(myProblem.X, -myProblem.Y, kernel, noise_var=self.gpNoisevariance)
            m.rbf.lengthscale.constrain_bounded(0.001,10)
            m.rbf.variance.constrain_bounded(0.001, 1000)
            m.Gaussian_noise.variance.constrain_fixed(self.gpNoisevariance)
            m.optimize(clear_after_finish=True)   
            print('kernel lengthscale') 
            print(kernel.lengthscale)
            self.covProposal = self.covarianceOfProposal(bo_max_point,kernel.lengthscale, kernel.variance, m.Gaussian_noise, myProblem.X, -myProblem.Y)                        
            foundPosDefProposal = np.all(np.linalg.eigvals(self.covProposal) >= 0)
            borun += 1
            print('Bayesian optimization has run for ' + str(borun * self.bo_max_iter) + ' iterations.')

        covProposal = self.scaleCovariance()
        print(covProposal)    
        covProposal.dump('covProposal_localgp')
        bo_max_point.dump('bo_max_point_localgp')
        return bo_max_point, myProblem.X, -myProblem.Y, covProposal

    
    def RunMHGP(self):
        bo_max_point, self.gpx, self.gpy, covProposal = self.performBayesianOptimization()
        self.localgpx = np.copy(self.gpx)
        self.localgpy = np.copy(self.gpy)
        self.localgp.fit(self.localgpx, self.localgpy)
        print('BO max point', bo_max_point)
        x = bo_max_point 
        samplesTaken = np.array([x]) #initialize the samples vector. this first point will be discarded while plotting
        allSamples = np.array([x]) #this is only for plotting sequence of samples
        sampleChainMHGP = np.array([x])
        
        wasXReadFromGP = False
        isCandidateReadFromGP = False        
        
        for i in range(self.n):
            sampleChainMHGP = np.vstack([sampleChainMHGP,x])
            candidateOK = False
            candidate = None
            while not candidateOK:
                # generate random number from multivariate Gaussian with mean at previous point
                candidate = np.random.multivariate_normal(x,covProposal) 
                candidateOK = self.checkCandidateForBounds(candidate)

            meanVal, mse = self.getGPprediction(x, candidate, True) # last param 'True' to ensure bound recalculation and refitting of local GP if current one is too uncertain  
            isaccepted = 0 #For logging purpose
            if i < self.gpTrainPeriod and self.shouldRecalculate(meanVal[0,0],mse[0,0],meanVal[1,0],mse[1,1],mse[0,1]): 
                if wasXReadFromGP == False: # if last x was evaluated then evaluate candidate too
                    self.evaluate(candidate)   
                    isCandidateReadFromGP = False
                else:
                    self.evaluate(x) # last x was read from GP, now evaluate x
                    wasXReadFromGP = False
                    meanVal, mse = self.getGPprediction(x, candidate) 
                    # see if candidate still has high variance, if yes then evaluate candidate
                    if self.shouldRecalculate(meanVal[0,0],mse[0,0],meanVal[1,0],mse[1,1],mse[0,1]): 
                        self.evaluate(candidate)
                        isCandidateReadFromGP = False
                    else:
                        isCandidateReadFromGP = True
            elif i < self.gpTrainPeriod:
                isCandidateReadFromGP = True
            
            secmeanVal, secmse = self.getGPprediction(x, candidate)            
            accratio = self.acceptanceRatio(secmeanVal[0,0],secmse[0,0],secmeanVal[1,0],secmse[1,1],secmse[0,1])            
            acceptanceProbability = min([1.,accratio])  

            if i%100==0 and i<=self.gpTrainPeriod and self.isVerbose == 1: #print information after each 100 iteration. for debugging purposes.
                self.printInfo(i, x, candidate, meanVal, mse, accratio)
                
            u = np.random.uniform(0,1)
            allSamples = np.vstack([allSamples,candidate]) # this is only for plotting sequence of samples
            oldx = x #For logging purpose
            if u < acceptanceProbability:
                self.acceptCount += 1
                self.posteriorValues.append(secmeanVal[0,0])
                covProposal = self.scaleCovariance(self.getCovMultiplyFactor(secmeanVal[0,0]))
                isaccepted = 1 #For logging purpose
                x = candidate
                wasXReadFromGP = isCandidateReadFromGP
                if i > self.endofBurnin: # only part of the iterations are taken and burn-ins are thrown away
                    samplesTaken = np.vstack([samplesTaken,candidate])   
            if self.shouldLogData:  
            	self.logData(i, oldx, candidate, meanVal, mse, secmeanVal, secmse, accratio, isaccepted)                      

        if self.shouldLogData and self.df is not None:
            self.df.to_pickle('mhgp_data_localgp_withARD_withAdacov_thresh0.1_maxcov0.001.pickle')
        return samplesTaken





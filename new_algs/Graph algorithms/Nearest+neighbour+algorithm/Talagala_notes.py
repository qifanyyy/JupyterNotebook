
# coding: utf-8

# Thank you for inviting me to share my thoughts on this publication. I will attempt to talk through the paper and identify the key points, making use of the figures to illustrate these as much as possible but if you have specific questions please feel free to chime in at any point.
# 
# 
# 
# Ok so lets begin. This article is all about studying efficient and robust methods for outlier detection (or anomaly detection) in time series data
# 

# \section{Background}
# 
# \subsection{Nomenclature and types of time series anomalies}
# 
# 
# \begin{itemize}
# \item \textbf{Time series data}: anything where a quantity is measured repeatedly at a series of different times. A collection of such data is known as a time-series. These are very useful for and have applications in a huge range of fields, weather forecasting, software development, monitoring hospital patients, jet engines and manufacturing processes. In astrophysics these are known as light curves and I use them to measure the masses of black holes in distant galaxies. Also can be used to hunt for planets around other stars and look for signs of extra-terrestrial life.
# 
# \item \textbf{Anomaly:} Anything that doesn’t fit with the rest of the time series. A more mathematical definition is any point in the time-series that is very unlikely assuming some background distribution (Figure 2a for example).
# \end{itemize}
# 

# This paper consider three types of outliers (Figure 2).
# 
# \begin{enumerate}
# \item \textbf{Contextual Anomalies within a given time-series:} A few rogue points amongst many examples of ‘ordinary’ behavior
# 
# \item \textbf{Anomalous sub-sequences within a given time series:} Have a period of anomalous behavior rather than just a few points.
# 
# \item \textbf{Anomalous series within a space of collection of series:} Rather than rogue points within a time series, have an entire anomalous time-series relative to normally behaved time-series.
# 
# \end{enumerate}
# 

# Having identified three types of outliers, the paper now discusses two sources of time series data and challenges of dealing with each.
# 
# 
# \begin{enumerate}
# \item \textbf{Batch processing:} Here the entire time series is available and outliers can be identified after the observations.
# 
# \item \textbf{Data Streams:} Here the time series is continuously evolving and the outlier detection algorithm must be able to adaapt to new 'typical' behaviour as it scans for outliers. Problems include 'concept drift' where the background model might eveolve with time (non stationarity).
# 
# \end{enumerate}
# 

# \textbf{Section 2.3: Extreme value theory for anomaly detection}
# 
# \par
# 
# This paper proposes a new method for anomaly detection in data streams (where observations are continously evolving with new data). The model requires some understandin of extreme value theory. A key concept here is that of the Fisher-Tippett theorem. \par
# 
# \textbf{Fisher-Tippett theorem:} If you take M subsamples from any parent distribution, calculate the maximum value in the subsample and repeat. The distribution of maximum values will tend toward one of three distributions
# 
# \begin{enumerate}
# \item \textbf{Frechet Distribution:} $\frac{\alpha}{s} \left( \frac{x - m}{s} \right)^{-1-\alpha} e^{- \left( \frac{x-m}{s} \right)^{-\alpha}}$
# 
# \item \textbf{Weibull Distribution:} $\frac{k}{\lambda} \left( \frac{x}{\lambda} \right)^{k-1} e^{ -(x/\lambda )^k }$
# 
# \item \textbf{Gumbell Distribution:} $\frac{1}{\beta} e^{- \left( \frac{x - \mu}{\beta} + e^{-\frac{x - \mu}{\beta}} \right)}$
# 
# \end{enumerate}
# 
# 
# The code below illustrates several of these PDF's.
# 
# 
# 
# 
# 
# 
# 

# In[13]:


import numpy as np
import matplotlib.pylab as plt
import warnings
import matplotlib.gridspec as gridspec
warnings.filterwarnings('ignore')

def gumbell_pdf(x,mu,beta):
    z   = (x - mu)/beta
    pdf = 1./beta * np.exp(-(z + np.exp(-z)))
    return(pdf)

def frechet_pdf(x,alpha,m,s):
    z = (x-m)/s
    pdf = alpha/s * z**(-1.-alpha) * np.exp(-z**(-alpha))
    return(pdf)

def weibull_pdf(x,k,lamda):
    nx  = np.shape(x)[0]
    pdf = np.zeros(nx)
    idx = np.where(x>0)[0]
    pdf[idx] = k/lamda * (x[idx]/lamda)**(k-1) * np.exp(-(x[idx]/lamda)**k)
    return(pdf)



#make plots of example pdfs of each distribution
#gumbel
mu = [2,4,8]
beta = [1,2,3]
x = np.arange(0,20,0.1)
pdf_gum = []
for i in range(len(mu)):
    pdf_gum.append(gumbell_pdf(x,mu[i],beta[i]))
fig = plt.figure()
ax1 = fig.add_subplot(111)
[ ax1.plot(x,pdf_gum[i],label=r'$\mu ='+np.str(mu[i])+'$ $ \\beta='+np.str(beta[i])+'$') for i in range(len(pdf_gum)) ]
ax1.set_title('Gumbel distribution')
plt.legend()
plt.show()


#Frechet
alpha = [1,2,3,6]
m = [0,0,0,0]
s = [1,1,1,3]
pdf_fre = []
for i in range(len(m)):
    pdf_fre.append(frechet_pdf(x,alpha[i],m[i],s[i]))
fig = plt.figure()
ax1 = fig.add_subplot(111)
[ ax1.plot(x,pdf_fre[i],label=r'$m ='+np.str(m[i])+'$ $ \\alpha='+np.str(alpha[i])+'$ $ s='+np.str(s[i])+'$') for i in range(len(pdf_fre)) ]
ax1.set_title('Frechet distribution')
ax1.set_xlim([0,6])
plt.legend()
plt.show()   



#Weibull
k = [0.5,1,1.5]
lamda = [1,1,1]
pdf_wei = []
for i in range(len(k)):
    pdf_wei.append(weibull_pdf(x,k[i],lamda[i]))
fig = plt.figure()
ax1 = fig.add_subplot(111)
[ ax1.plot(x,pdf_wei[i],label=r'$k ='+np.str(k[i])+'$ $ \\lambda='+np.str(lamda[i])+'$') for i in range(len(pdf_wei)) ]
ax1.set_title('Weibull distribution')
ax1.set_xlim([0,6])
plt.legend()
plt.show()      
    


# \textbf{Section 2.3.1: Existing work for anomaly detection based on extreme value theory}
# Anomalies tend to be defined either by distance or density. Distance refers to a point that is beyond some distance of either its nearest neighbours or a fiducial model. Density-based anomaly detectors will flag points or clusters of points that have a very low chance of occurance.
# 
# 

# \textbf{Section 3: Methodology}
# 
# A new method for time series anomaly detection in streaming multivariate (rather than comparing a single timeseries we are cross comparing many).
# 
# \textbf{Drawbacks of previous method}
# \begin{enumerate}
# \item The method is an updated version of two methods proposed by Hyndman, Wang, Laptev (2015) and Wilkinson (2018) that suffer from the drawback that HWL identifies the most unusual timeseries within a large collection of time series whether or not they are anomalous.
# 
# \item The methods do not do well in multivariate time series with anomalies that vary gradually from the standard behaviour. Figure 4 shows an example of this where current methods will correctly identify outliers in the multivariate case where the adjacent light curve sensors are independent of one another. In the right plot the time series are co-dependent (not independent) where an anomaly in a single time-series will affect adjacent time series.
# \end{enumerate}
# 
# The new algorithm overcomes this problem by using a 'training' data set of the systems standard behaviour
# 

# In[28]:


#generate random multivariate timeseries from Guassian distribution
n_epoch  = 1000
n_timeseries = 100
data_y = np.reshape( np.random.randn(n_epoch * n_timeseries), (n_epoch,n_timeseries) )

#rolling mean function
def movingaverage(x,y, window):
  weights = np.repeat(1.0, window)/window
  sma = np.convolve(y, weights, 'valid')
  sma_x = x[:]
  sma_y = np.concatenate((np.ones(window-1)*sma[0],sma))
  return(sma_x,sma_y)

#calculate each of the features
def features(data_y,window = 10):
    nfeatures = 9
    
    nepoch,nts = np.shape(data_y)
    features = np.zeros((nts,nfeatures))
    
    #f1 mean
    f1 = np.mean(data_y,axis=0)
    
    
    #f2 variance
    f2 = np.var(data_y,axis=0)
    
    
    #f3 lumpiness devide into chunks defined by window size and calculate the variance of the variances
    nwindow = np.int(np.ceil(1.*nepoch/window))
    lump = np.zeros((0,nts))
    for i in range(nwindow):
     ilo = i*window
     ihi = min(ilo+window,nepoch-1)
     var = np.var(data_y[ilo:ihi,:],axis=0)
     lump = np.vstack((lump,var))
    f3 = np.var(lump,axis=0)
    
    #f4 A function to calculate Level shift using rolling window The 'level shift' is defined as the maximum difference in mean
    # between consecutive blocks of 10 observations measure6 - Level shift using rolling window
    f4 = []
    for i in range(nts):
     runmean = movingaverage(np.arange(nepoch),data_y[:,i], window)[1]
     d_runmean = runmean[1:]-runmean[:-1]
     f4.append(np.max(d_runmean))
    f4 = np.array(f4)

    #f5 calculate the rolling variance
    import pandas as pd 
    f5 = []
    for i in range(nts):
     s = pd.Series(data_y[:,i])
     run_var = np.array(s.rolling(window).var())
     d_runvar = run_var[1:]-run_var[:-1]
     f5.append(np.nanmax(d_runvar))
    f5 = np.array(f5)
    
    
    #f6 fano factor (burstiness of time series - var/mean)
    f6 = f2/f1
    
    #f7, f8 maximum and minimum of time series
    f7 = np.nanmax(data_y,axis=0)
    f8 = np.nanmin(data_y,axis=0)
    
    #f9 high to low mu ratio of means of the data that are above and below the true mean
    f9 = []
    for i in range(nts):
        mean = f1[i]
        idup = np.where(data_y[:,i]>mean)[0]
        meanhi = np.mean(data_y[idup,i])
        idlo = np.where(data_y[:,i]<mean)[0]
        meanlo = np.mean(data_y[idlo,i])
        f9.append(meanhi/meanlo)    
    f9 = np.array(f9)
    
    features[:,0]=f1
    features[:,1]=f2
    features[:,2]=f3
    features[:,3]=f4
    features[:,4]=f5
    features[:,5]=f6
    features[:,6]=f7
    features[:,7]=f8
    features[:,8]=f9
    
    labels = ['mean','variance','lumpiness','level shift mean','level shift variance',
              'burstiness','maximum','minimum','hightolowmu']
    
    
    #make diagnostic plot
    gs1 = gridspec.GridSpec(nfeatures, 1)
    gs1.update(left=0.1, right=0.9, bottom=0.1,top = 0.9, wspace=0.05,hspace = 0.0)
    for i in range(nfeatures):
     ax1 = plt.subplot(gs1[i, 0])
     ax1.plot(features[:,i],label=labels[i])
     #ax1.set_ylabel(labels[i])
     if (i == nfeatures - 1):
      ax1.set_xlabel('Time series ID')
     ax1.text(1.1,0.5,labels[i],ha='left',transform=ax1.transAxes)
    plt.show()
     
    return(features,labels)


op = features(data_y,window = 10)
    


# Now we have the features. Normalize the matrix and perform PCA

# In[34]:


#normalise the feature matrix
f,flab = op

nts,nfeatures = np.shape(f)
fop = np.array(f)
for i in range(nfeatures):
    fop[:,i] = (f[:,i] - np.mean(f[:,i]))/np.std(f[:,i])         
#perform PCA
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
fop_pca = pca.fit(fop)
                
#make a scatter plot
fop_pca


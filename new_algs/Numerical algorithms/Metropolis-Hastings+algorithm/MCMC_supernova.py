import matplotlib.pyplot as plt
import datetime as DT
import numpy as np
import sys
import optparse
from scipy.optimize import curve_fit
import scipy as sp
import math
import array
from numpy.linalg import inv

np.random.seed(seed=1)

#input arguments
parser=optparse.OptionParser(usage="Usage: %prog Data Covariance_Matrix")
options,arguments=parser.parse_args()

# Load data from text files.
data = str(sys.argv[1])
cov_matrix = str(sys.argv[2])

# Extract data for the observed redshift of the supernova and the distance modulus.
DistMod = np.genfromtxt(data, delimiter=None, skip_header=1, comments = 'T')
z_redshift = DistMod[:,0]
mu = DistMod[:,1]

# 31 × 31 covariance matrix of the data.
CovMatrix1D = np.genfromtxt(cov_matrix, delimiter=None, skip_header=0, comments = 'T')
CovMatrix = CovMatrix1D.reshape(31,31)

# Calculate the matrix inverse to use in the likelihood function.
CovMatrixInv = inv(CovMatrix)

def Mu(z,h,omega):
	"""Calculate distance modulus, mu, using the formula for luminosity distance Dl."""
	s = ((1-omega)/omega)**(1./3)
	nu1 = 2*np.sqrt((s**3)+1)*\
		((1-0.1540*s+0.4304*(s**2)+0.19097*(s**3)+0.066941*(s**4))**(-(1./8)))
	nu2 = 2*np.sqrt((s**3)+1)*\
		(((1/(1/(1+z))**4)-0.1540*(s/(1/(1+z))**3)+0.4304*((s**2)/(1/(1+z))**2)+0.19097*((s**3)/(1/(1+z)))+0.066941*(s**4))**(-(1./8)))
	Dl = 3000.0*(1+z)*(nu1-nu2)
	mu_th = 25.0 - 5.0*np.log10(h) + 5.0*np.log10(Dl)
	return mu_th

def Likelihood(z,mu,h,Omega):
	"""Calculate likelihood."""
	InnerSum = 0
	for i in np.arange(0, 31, 1):
		for j in np.arange(0,31,1):
			InnerSum = InnerSum + (mu[i] - Mu(z_redshift[i], h, Omega)) * \
				CovMatrixInv[i, j] * (mu[j] - Mu(z_redshift[j], h, Omega))
			Lhd = np.exp(-0.5 * InnerSum)
	return Lhd

# Set number of draws K.
K = 400

# Define initial arrays filled with zeros.
h = np.zeros(K)
Omega = np.zeros(K)
Probability = np.zeros(K)

# Set starting values for h and Omega.
h[0] = 0.5
Omega[0] = 0.5
Probability[0] =  Likelihood(z_redshift, mu, h[0], Omega[0])

# Standard deviations for normally distrbuted priors for h and Omega.
sigma_h = 0.01
sigma_Omega = 0.01

# Metropolis algorithm
for k in np.arange(1,K,1):
	print('Taking step %5.0f' % k)
	
	# Propose a new point from a normal distribution where h[k-1] is the mean,
	# sigma_h is standard deviation, and one sample (for h).
	h_star = np.random.normal(h[k-1], sigma_h, 1)
	Omega_star = np.random.normal(Omega[k-1], sigma_Omega, 1)
	
	# Calculate likelihood for a newly proposed point.
	Probability_star = Likelihood(z_redshift, mu, h_star, Omega_star)
	Probability[k-1] = Likelihood(z_redshift, mu, h[k-1], Omega[k-1])
	
	# Accept/reject point based on parameter p randomely drawn from
	# uniform distribution in [0.001, 0.999].
	p = np.random.uniform(0.001, 0.999, 1)
	if p <= Probability_star/Probability[k-1]:
		h[k] = h_star
		Omega[k] = Omega_star
		Probability[k] = Probability_star
	else:
		h[k] = h[k-1]
		Omega[k] = Omega[k-1]

np.savetxt('parameters_output.txt', np.transpose([h,Omega]))

plt.figure(1)
plt.subplot(211)
plt.rc('font', family='serif')
plt.scatter(np.arange(0,K,1), h, color='red', marker = '*', s=10, label = 'h')
plt.xlabel('number of samples', fontsize = 14)
plt.ylabel('h', fontsize = 14)
plt.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))
plt.grid()
plt.legend(loc=0, fontsize = 14)

plt.subplot(212)
plt.rc('font', family='serif')
plt.scatter(np.arange(0,K,1), Omega, color='black', marker = '*', s=10, label = 'Omega')
plt.xlabel('number of samples', fontsize = 14)
plt.ylabel('Omega', fontsize = 14)
plt.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))
plt.grid()
plt.legend(loc=0, fontsize = 14)

plt.show()

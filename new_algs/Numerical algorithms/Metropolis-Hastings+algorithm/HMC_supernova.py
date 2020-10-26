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

# Extracting data for the observed redshift of the supernova and the distance modulus.
DistMod = np.genfromtxt(data, delimiter=None, skip_header=1, comments = 'T')
z_data = DistMod[:,0]
mu_data = DistMod[:,1]

# 31 × 31 covariance matrix of the data.
CovMatrix1D = np.genfromtxt(cov_matrix, delimiter=None, skip_header=0, comments = 'T')
CovMatrix = CovMatrix1D.reshape(31,31)

# Calculating the matrix inverse to use in the likelihood function.
CovMatrixInv = inv(CovMatrix)

# Define all necessary functions to calculate distance modulus, Hamiltonian and potential.
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

def Hamiltonian(h,Omega,u1, u2):
	"""Calculate Hamiltonian H = − ln L + K, where K = u · u/2, where u is momentum."""

	Lhd = 0
	for i in np.arange(0, 31, 1):
		for j in np.arange(0,31,1):
			Lhd = Lhd + 0.5 * (mu_data[i] - Mu(z_data[i], h, Omega)) * \
				CovMatrixInv[i, j] * (mu_data[j] - Mu(z_data[j], h, Omega))
			K = 0.5 * (u1*u1 + u2*u2)
			Hamiltonian = 0.5 *(Lhd + K)

	return Hamiltonian

def Ufunc(h,Omega):
	"""Calculate potential."""

	Sum = 0
	for i in np.arange(0, 31, 1):
		for j in np.arange(0,31,1):
			Sum = Sum + (mu_data[i] - Mu(z_data[i], h, Omega)) * \
				CovMatrixInv[i, j] * (mu_data[j] - Mu(z_data[j], h, Omega))
			Ufunc = 0.5 * Sum

	return Ufunc

def grad_U_h(h, Omega, delta_h):
	"""Calculate discrete derivative of potential with respect to h."""

	dU_h = (Ufunc(h + delta_h, Omega) - Ufunc(h-delta_h, Omega))/(2*delta_h)

	return dU_h

def grad_U_Omega(h, Omega, delta_Omega):
	"""Calculate discrete derivative of potential with respect to Omega."""

	dU_Omega = (Ufunc(h, Omega + delta_Omega) - Ufunc(h, Omega - delta_Omega))/(2*delta_h)

	return dU_Omega

# Setting number of samples and parameters for the leapfrog algorithm.
Nsamples = 400
Nleapfrog = 40
eps_h = 0.002
eps_Omega = 0.002

# Define initial arrays filled with zeros.
h = np.zeros(Nsamples)
Omega = np.zeros(Nsamples)

# Set starting values for h and Omega.
h[0] = 0.5
Omega[0] = 0.5

# Set discretization parameters to calculate derivatives.
delta_h = 0.01
delta_Omega = 0.01

# Hamiltonian Monte Carlo algorithm.
for i in np.arange(1,Nsamples,1):
	u1_rand = np.random.normal(0.001, 0.999, 1)
	u2_rand = np.random.normal(0.001, 0.999, 1)
	h_start_initial = np.array(h[i-1])
	h_start = np.array(h[i-1])
	Omega_start_initial = np.array(Omega[i-1])
	Omega_start = np.array(Omega[i-1])
	u1_start_initial = u1_rand
	u2_start_initial = u2_rand
	u1_start = u1_rand
	u2_start = u2_rand
	
	# Leapfrog propagation of parameters and momenta.
	for j in np.arange(1,Nleapfrog,1):
		u1_start_staggered = u1_start - \
							0.5 * eps_h * grad_U_h(float(h_start), float(Omega_start), delta_h)
		u2_start_staggered = u2_start - \
							0.5 * eps_Omega * grad_U_Omega(float(h_start), float(Omega_start), delta_Omega)

		h_start = h_start + eps_h * u1_start_staggered
		Omega_start = Omega_start + eps_Omega * u2_start_staggered

		u1_start = u1_start_staggered - \
					0.5 * eps_h * grad_U_h(float(h_start), float(Omega_start), delta_h)
		u2_start = u2_start_staggered - \
					0.5 * eps_Omega * grad_U_Omega(float(h_start), float(Omega_start), delta_Omega)

	print('Taking step %5.0f' % i)
	h_start_new = h_start
	print(h_start_new)
	Omega_start_new = Omega_start
	print(Omega_start_new)
	u1_start_new = u1_start
	u2_start_new = u2_start

	# Accept / reject a new sample using Hamiltonian defined at initial point where we started
	# leapfrog propagation and the newly proposed point.
	alpha = np.random.uniform(0.001, 0.999, 1)
	if alpha < min(1,np.exp(-(Hamiltonian(h_start_new, Omega_start_new, u1_start_new, u2_start_new) - Hamiltonian(h_start_initial, Omega_start_initial, u1_start_initial, u2_start_initial)))):
		h[i] = h_start_new
		Omega[i] = Omega_start_new
	else:
		h[i] = h[i-1]
		Omega[i] = Omega[i-1]

np.savetxt('HMC_parameters_output.txt', np.transpose([h,Omega]))

plt.figure(1)
plt.subplot(211)
plt.rc('font', family='serif')
plt.scatter(np.arange(0,Nsamples,1), h, color='red', marker = '*', s=10, label = 'h')
plt.xlabel('number of samples', fontsize = 14)
plt.ylabel('h', fontsize = 14)
plt.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))
plt.grid()
plt.legend(loc=0, fontsize = 14)

plt.subplot(212)
plt.rc('font', family='serif')
plt.hist(h, bins='auto')
plt.xlabel('auto_bins', fontsize = 14)
plt.ylabel('h', fontsize = 14)
plt.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))
plt.legend(loc=0, fontsize = 14)

plt.figure(2)
plt.subplot(211)
plt.rc('font', family='serif')
plt.scatter(np.arange(0,Nsamples,1), Omega, color='black', marker = '*', s=10, label = 'Omega')
plt.xlabel('number of samples', fontsize = 14)
plt.ylabel('Omega', fontsize = 14)
plt.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))
plt.grid()
plt.legend(loc=0, fontsize = 14)

plt.subplot(212)
plt.rc('font', family='serif')
plt.hist(Omega, bins='auto')
plt.xlabel('auto_bins', fontsize = 14)
plt.ylabel('h', fontsize = 14)
plt.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))
plt.legend(loc=0, fontsize = 14)

plt.show()


''' File: metro.py '''
''' Copyright: Loic Le Tiran, 2014 '''
''' Contact: loic.le-tiran@obspm.fr '''
''' Licence: GNU GPL v3 '''

''' Description: '''
''' Simple Metropolis-Hastings algorithm for fitting a gaussian line '''

import numpy as np
import scipy
import matplotlib.pyplot as plt

# Simple gaussian function
def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2. * np.power(sig, 2.)))


''' Create a gaussian line with some noise '''

N = 100. # nb points
x = np.arange(N) # axis

# parameters of the initial gaussian
sigma = 5.
position = 50.
maxi = 1.

# parameter of the noise (here gaussian noise sampled relatively to the signal maximum).
noiselevel = maxi / 10.

# Creates the signal (g) and the noise
g = maxi  * gaussian(x, position, sigma)
noise = noiselevel * np.random.normal(0,1,N)
signal = g + noise

''' Fit '''
# Take a 'step 0' fit parameters (it is obviously not a fit, it is just the model)
# In this example only sigma and the position vary. The max is constant. To be changed.

# Fit parameters
sigma_fit = 4.0
position_fit = 60.
maxi_fit = 1.00

# Fit array
fit = maxi_fit * gaussian(x, position_fit, sigma_fit)


# Plots the signal and its random fit
plt.plot(x, signal)
plt.plot(x, fit)
#plt.show() # Uncomment to show graph on screen
#plt.savefig("signal.png") # Uncomment to save graph on disk
plt.close()



''' Likelihood Calculation for these initial parameters' fit '''
lnL_old = - sum( (signal - fit) * (signal - fit) ) / (2. * noiselevel * noiselevel)


# Only variations in position and sigma at this time

# Number of iterations of the algorithm
Ntries = 15000

# Initialization of arrays
sigmas = []
lnLs = []
positions = []

old_sigma_fit = sigma_fit
old_position_fit = position_fit


# Mean dispersion of a random walk.
sig_trajet = 0.5

''' Core of the algo '''
# Makes new 'fit' with a random walk in the parameters' space from the last position.
# Check if the new fit has a better likelihood.
# If yes, keep the new parameters.
# If no, the probability to keep the new parameters is a function of the likelihood weights (here priors = 1).

for i in np.arange(Ntries) :

		# new parameters, fit, and likelihood
        new_sigma_fit = old_sigma_fit + (np.random.normal(0,sig_trajet,1))[0]
        new_position_fit = old_position_fit + (np.random.normal(0,sig_trajet,1))[0]

        new_fit = maxi_fit * gaussian(x, new_position_fit, new_sigma_fit)

        lnL_new = - sum( (signal - new_fit) * (signal - new_fit) ) / (2. * noiselevel * noiselevel)


		# Conditional probability for keeping the new parameters
        probab = np.exp(lnL_new - lnL_old) * 1.

        if  probab >=  np.random.uniform(0,1): # In the case where the new likelihood is better than the old one, this is always true. In the opposite case, the output depends on the probability.
				# New is now old.
                old_position_fit = new_position_fit
                old_sigma_fit = new_sigma_fit
                lnL_old = lnL_new
                # Saves the data about the walk in the parameters space.
                sigmas.append(old_sigma_fit)
                lnLs.append(lnL_old)
                positions.append(old_position_fit)



''' A few graphs '''

# Sigma and positions as a function of the likelihoods
plt.plot(sigmas, lnLs, '+b', label ='Sigmas')
plt.plot(positions, lnLs, '+r', label ='Positions')
plt.legend()
plt.xlabel("Sigma/Position")
plt.ylabel("Likelihood")
#plt.show()
plt.close()

# Walk in the Position - Sigma space
plt.plot(sigmas, positions)
plt.xlabel("Sigma")
plt.ylabel("Position")
plt.show()
plt.close()




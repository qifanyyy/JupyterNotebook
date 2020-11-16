import numpy as np
import pandas as pd
from scipy.stats import norm, sem
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------------------ Problem 2 ------------------------------------------
'''
Here we use a logistic regression model to answer whether the status of an HMO affects the
emergency room choice.
a) Verify likelihood function (written).
b) Run a standard GLM on the data and get the estimated mean and variance of a, b, and c.
c) Use normal candidate densities with mean and variance at the GLM estimates in a
Metropolis-Hastings algorithm sampling from the likelihood.
Get histograms of the parameter values.
'''
np.random.seed(42)

# b) run GLM on data and get estimated mean and variance of a, b, and c
with open('LogisticData.txt', 'r') as f:
    content = f.readlines()
content = np.array([x.strip().split() for x in content][1:])
n_samples = content.shape[0]
print('content:', np.shape(content))

_np = np.array([int(x) for x in content[:, 1]])
metq = np.array([int(x) for x in content[:, 2]])
erodd = np.array([int(x) for x in content[:, 4]])

df = pd.DataFrame({'erodd': erodd, 'metq': metq, 'np': _np})
model = sm.formula.glm(formula='erodd ~ metq+_np', data=df, family=sm.families.Binomial()).fit()
print(model.summary())
print('covariance matrix:\n', model.cov_params())

am = -1.9739 # coef (mean)
_as = 0.221 # std err
bm = 0.1622
bs = 0.080
cm = 0.2844
cs = 0.093



# c) use normal candidate densities with mean and variance at the GLM estimates in a
# Metropolis-Hastings algorithm sampling from the likelihood.
# Get histograms of  the parameter values.
def log_likelihood(a, b, c):
    return np.sum(erodd * (a + b*_np + c*metq) - np.log(1 + np.exp(a + b*_np + c*metq)))

def get_tr_dens(a, b, c):
    a_pdf = norm.logpdf(a, am, _as)
    b_pdf = norm.logpdf(b, bm, bs)
    c_pdf = norm.logpdf(c, cm, cs)
    return a_pdf + b_pdf + c_pdf

n_sim = 100000
a_hat = np.zeros(n_sim + 1)
b_hat = np.zeros(n_sim + 1)
c_hat = np.zeros(n_sim + 1)
a_hat[0] = np.random.normal(loc=am, scale=_as, size=1)
b_hat[0] = np.random.normal(loc=bm, scale=bs, size=1)
c_hat[0] = np.random.normal(loc=cm, scale=cs, size=1)
for j in range(1, n_sim):
    a = a_hat[j-1]
    b = b_hat[j-1]
    c = c_hat[j-1]
    a_tr = np.random.normal(loc=am, scale=_as, size=1)
    b_tr = np.random.normal(loc=bm, scale=bs, size=1)
    c_tr = np.random.normal(loc=cm, scale=cs, size=1)

    tr_logl = log_likelihood(a_tr, b_tr, c_tr)
    logl = log_likelihood(a, b, c)
    A = tr_logl - logl

    dens  = get_tr_dens(a, b, c)
    tr_dens = get_tr_dens(a_tr, b_tr, c_tr)
    B = dens - tr_dens

    P = np.exp(A + B)
    rho = np.random.uniform() < min(P, 1)
    a_hat[j] = a_tr*rho + a_hat[j-1]*(1-rho)
    b_hat[j] = b_tr*rho + b_hat[j-1]*(1-rho)
    c_hat[j] = c_tr*rho + c_hat[j-1]*(1-rho)
a_hat = np.delete(a_hat, -1)
b_hat = np.delete(b_hat, -1)
c_hat = np.delete(c_hat, -1)



# parameter a histogram and density estimate
fig = plt.figure()
plt.hist(a_hat, bins=30, density=True, label='a (intercept)', color='green', edgecolor='black')
plt.grid()
plt.xlabel('a')
plt.ylabel('Value')
plt.title('Histogram of Parameter a (Intercept)')
plt.legend(['a'])
fig.savefig('a_histogram.png', dpi=300)
plt.show()

fig = plt.figure()
sns.distplot(a_hat, hist=True, kde=True, color='green', hist_kws={'edgecolor':'black'},
            kde_kws={'linewidth': 4})
plt.xlabel('a')
plt.ylabel('Density')
plt.title('Kernel Density Estimate of Parameter a (Intercept)')
plt.legend(['a'])
fig.savefig('a_density_estimate.png', dpi=300)
plt.show()

# parameter b histogram and density estimate
fig = plt.figure()
plt.hist(b_hat, bins=30, density=True, label='c', color='darkblue', edgecolor='black')
plt.grid()
plt.xlabel('b')
plt.ylabel('Value')
plt.title('Histogram of Parameter b (for HMO Type)')
plt.legend(['b'])
fig.savefig('b_histogram.png', dpi=300)
plt.show()

fig = plt.figure()
sns.distplot(b_hat, hist=True, kde=True, color='darkblue', hist_kws={'edgecolor':'black'},
            kde_kws={'linewidth': 4})
plt.xlabel('b')
plt.ylabel('Density')
plt.title('Kernel Density Estimate of Parameter b (for HMO Type)')
plt.legend(['b'])
fig.savefig('b_density_estimate.png', dpi=300)
plt.show()

# parameter c histogram and density estimate
fig = plt.figure()
plt.hist(c_hat, bins=30, density=True, label='c', color='red', edgecolor='black')
plt.grid()
plt.xlabel('c')
plt.ylabel('Value')
plt.title('Histogram of Parameter c (for Health Status)')
plt.legend(['c'])
fig.savefig('b_histogram.png', dpi=300)
plt.show()

fig = plt.figure()
sns.distplot(c_hat, hist=True, kde=True, color='red', hist_kws={'edgecolor':'black'},
            kde_kws={'linewidth': 4})
plt.xlabel('c')
plt.ylabel('Density')
plt.title('Kernel Density Estimate of Parameter c (for Health Status)')
plt.legend(['c'])
fig.savefig('c_density_estimate.png', dpi=300)
plt.show()

den = range(1, n_sim + 1)
a_mean = np.cumsum(a_hat) / den
b_mean = np.cumsum(b_hat) / den
c_mean = np.cumsum(c_hat) / den
print('a_mean:', a_mean[-1])
print('b_mean:', b_mean[-1])
print('c_mean:', c_mean[-1])

a_variance = np.var(a_hat)
b_variance = np.var(b_hat)
c_variance = np.var(c_hat)
print('a_variance:', a_variance)
print('b_variance:', b_variance)
print('c_variance:', c_variance)

a_std_err = sem(a_hat)
b_std_err = sem(b_hat)
c_std_err = sem(c_hat)
print('a_std_err:', a_std_err)
print('b_std_err:', b_std_err)
print('c_std_err:', c_std_err)

# fig = plt.figure()
# plt.plot(a_mean, color='red')
# plt.plot(b_mean, color='red')
# plt.plot(c_mean, color='red')
# plt.grid()
# plt.xlabel('')
# plt.ylabel('')
# plt.title('')
# plt.legend(['', '', ''])
# fig.savefig('abc_means.png', dpi=300)
# plt.show()

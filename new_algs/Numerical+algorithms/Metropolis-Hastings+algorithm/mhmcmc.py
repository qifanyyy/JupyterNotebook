
def mh1d(fn, X0, parms, scale= 1.0, N=100):
    from numpy import log, zeros
    from numpy.random import uniform, normal
    f0 = fn(X0, parms)
    chain = zeros(N+1)
    Xprev = X0
    chain[0] = X0
    for i in range(1,N+1):
        propo = Xprev + uniform(low = -scale/2, high=scale/2)
        # propo = Xprev + normal(scale=scale)
        f1 = fn(propo, parms)
        lgR = f1 - f0
        lgU = log(uniform())
        if lgU < lgR:
            chain[i] = propo
            Xprev, f0  = propo, f1   # swap for next iteration 
        else:
            chain[i] = Xprev
    return chain

def lgbeta(X, parms):
    from numpy import log
    a, b = parms
    return (a - 1)*log(X) + (b - 1)*log(1 - X)

def mhmc(fn, ndim, X0, parms, scale= 1.0, N=100 ):
    """Multidim MH MCMC: X0 initial vector, parms for fn (vector) 
    
    fn should take two args: vector X0 (ndim) and parms (vector of however many)
    scale is scale for proposal distribution, N -number of points
    returns array of ndim rows, N columns.
    Be careful:
    Here this is the probability density definition, X corresponds to the 
    dimensionality of the random variable, parms are imposed (constant).
    Will need some thinking and rearranging for Bayesian inference.
    """
    from numpy import log, zeros
    from numpy.random import uniform, normal
    accept = reject = 0
    dz = zeros(ndim)
    f0 = fn(X0, parms)
    chain = zeros((ndim, N+1))
    Xprev = X0
    chain[:,0] = X0
    propo = Xprev
    for i in range(1,N+1):
        # Just change one parameter at a time
        delta = dz
        delta[(i % ndim)] = uniform(low = -scale/2, high=scale/2)
        propo = Xprev +  delta
        # propo = Xprev + normal(scale=scale) # gaussian proposal dist.
        f1 = fn(propo, parms)
        lgR = f1 - f0
        lgU = log(uniform())
        # print(lgR, lgU)
        if lgU < lgR:
            chain[:,i] = propo
            Xprev, f0  = propo, f1   # swap for next iteration 
            accept += 1
        else:
            chain[:,i] = Xprev
            reject += 1
    # print("Acceptance fraction: ", accept/(accept+reject))
    return chain

def bvn(X, p):
    """simple bivariate normal (log) X and p are vectors"""
    x,y = X
    mx, sx, my, sy = p
    return -0.5*( ((x-mx)/sx)**2 + ((y-my)/sy)**2)



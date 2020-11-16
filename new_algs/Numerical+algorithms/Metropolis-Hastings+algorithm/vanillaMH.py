import numpy as np

def vanillaMH(func, init_x, n, burn_in, diag_of_proposal):
    samplesMH = np.array([init_x])    
    x = init_x
    for i in range(1,n):
        candidate = np.random.multivariate_normal(x,np.diag(diag_of_proposal)) #candidate
        aprob = min([1.,func(candidate)/func(x)]) #acceptance probability
        u = np.random.uniform(0,1)        
        if u < aprob:
            x = candidate
            if i>burn_in:
                samplesMH = np.vstack([samplesMH,candidate])
    return samplesMH
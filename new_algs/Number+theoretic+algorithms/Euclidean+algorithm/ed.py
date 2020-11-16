"""
Python implementation of UCR-ED algorithm from:

Rakthanmanon, T., Campana, B., Mueen, A., Batista, G., Westover, B., Zhu, Q., et al. (2012). 
Searching and mining trillions of time series subsequences under dynamic time warping (pp. 262–9). 
Presented at the the 18th ACM SIGKDD international conference, New York, New York, USA: ACM Press. 
http://doi.org/10.1145/2339530.2339576

!!! Left out the file reading and the algorithm's optimization regarding it.
"""

from numpy import abs, sqrt, inf, mean, std

def distance(Q, T, j, m, _mean, _std, order, bsf):
    _sum = 0.
    for i in range(m):
        if _sum < bsf:
            x = ( T[order[i]+j]-_mean )/_std
            _sum += (x-Q[i])*(x-Q[i])
        else: 
            break
    
    return _sum

def ED(Q, T):
    loc = 0
    bsf = inf
    Q_m = len(Q)
    Q_mean = mean(Q)
    Q_std = std(Q)
    
    order = {}
    Q_tmp = []
    """ z-normalization on Q """
    for i in range(len(Q)):
        Q[i] = (Q[i] - Q_mean)/Q_std # z-norm
        Q_tmp.append([Q[i], i]) # store value/index tuples
        
    Q_tmp.sort(key=lambda p:p[0], reverse=True) # quicksort by value
    
    for i in range(len(Q)):
        Q[i] = Q_tmp[i][0] # overwrite Q with sorted Q
        order[i] = Q_tmp[i][1] # store new index to old index pairs
        
    """ ED of z-norm(Q) and T, being z-normalized on the fly """
    T_tmp = [0.]*2*Q_m
    dist = 0.
    j = 0
    ex = ex2 = 0.
    for idx,t in enumerate(T):
        ex += t
        ex2 += t*t
        T_tmp[idx%Q_m] = t
        T_tmp[(idx%Q_m)+Q_m] = t
        
        # if there is enough data in T, ED can be calculated
        if idx >= Q_m-1:
            # current starting location of T
            j = (idx+1)%Q_m
            
            # z-norm of T[i] will be calculated on the fly
            T_mean = ex/Q_m
            T_std = ex2/Q_m
            T_std = sqrt(T_std-T_mean*T_mean)
            
            # calculate ED
            dist = distance(Q,T_tmp,j,Q_m,T_mean,T_std,order,bsf)
            if dist < bsf:
                bsf = dist
                loc = idx-Q_m+1
                
            ex -= T_tmp[j]
            ex2 -= T_tmp[j]**2
    
    return loc, sqrt(bsf)
        
    
    
    
    
#implementation of Brent's algorithm for detecting a cycle - credit to Wikipedia

def brenter(f, x0):
    pow = 1 
    lam = 1
    tort = x0
    hare = f[x0]
    
    while tort != hare:
        if pow == lam:
            tort = hare 
            pow *= 2
            lam = 0
        hare = f[hare]
        lam += 1

    # Find the position of the first repetition of length λ
    tort = hare = x0
    for i in range(lam):
    # range(lam) produces a list with the values 0, 1, ... , lam-1
        hare = f[hare]
    # The distance between the hare and tortoise is now λ.

    mu = 0
    while tort != hare:
        tort = f[tort]
        hare = f[hare]
        mu += 1

    return lam, mu


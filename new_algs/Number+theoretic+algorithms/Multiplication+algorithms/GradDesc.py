import math

def f(params, *args): 
    '''simple function to test approximate gradient descent minimization'''
    x, y, z = params
    k1, k2  = args
    return (x-1)**2 + (y-2)**2 + (z-3)**2 + k1 + k2

def gradDesc(f, init, args):
    '''simple implementation of an approximate gradient descent algorithm via finite symmetric differences
    @params:
        - f[function]: function to be minimized - the function's first argument must be a sequence of input values
        - init[list]:  initial function input values to kick off the optimization search - can have an effect on the solution
        - args[tuple]: other positional arguments (outside main function inputs) to pass to the function being minimized
    @return:
        - i[int]:    number of iterations until convergence
        - x[list]:   function input values at the minimum
        - fx[float]: minimum function value
    sample call:
        result = gradDesc(f, [0, 0, 0], (arg1, arg2))'''

    hval = 0.001 # x-distance to use when estimating the current gradient via finite symmetric differences
    step = 0.01  # step size to use when traveling in the negative gradient direction for the next iterative X
    curX = init  # initialize current X values with function input
    norm = 9999  # initialize norm between current and previous X (used to test convergence criterion)
    thld = 1e-8  # threshold convergence criterion (distance between old/new x values)

    i = 0
    while (norm > thld):

        gradient = [None for x in curX]
        for x in range(len(gradient)):
            stepXP = curX[:x] + [(curX[x] + hval)] + curX[x+1:]
            stepXN = curX[:x] + [(curX[x] - hval)] + curX[x+1:]
            gradient[x] = (f(stepXP, *args) - f(stepXN, *args))/(2*hval)

        oldX = curX
        curX = [curX[x] - step*gradient[x] for x in range(len(gradient))]
        norm = math.sqrt(sum([(curX[x]-oldX[x])**2 for x in range(len(gradient))]))
        i += 1

    return {'i': i, 'x': curX, 'fx': f(curX, *args)}

init = [0, 0, 0]
print(gradDesc(f, init, (5, 10)))

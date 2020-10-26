'''
    branin function as toy example
    given function values are encoded in the instance name
    Call:
    python braninWrapper.py x1_1 blub 1 1 1 -x2 1
'''

import sys
import math
import numpy as np

def _get_har3(x1, x2, x3):
    """3d Hartmann test function
    constraints:
    0 <= xi <= 1, i = 1..3
    global optimum at (0.114614, 0.555649, 0.852547)
    where har3 = -3.86278
    source: https://github.com/automl/HPOlib/blob/master/HPOlib/benchmark_functions.py
    """

    value = np.array([x1, x2, x3])

    a = np.array([[3.0, 10, 30],
               [.1, 10, 35],
               [3.0, 10, 30],
               [0.1, 10, 35]])
    
    c = np.array([1.0, 1.2, 3.0, 3.2])
    
    p = np.array([[0.3689, 0.1170, 0.2673],
                  [0.4699, 0.4387, 0.7470],
                  [0.1091, 0.8732, 0.5547],
                  [0.0381, 0.5743, 0.8828],
                  ])
    s = 0
    for i in [0,1,2,3]:
        sm = a[i,0]*(value[0]-p[i,0])**2
        sm += a[i,1]*(value[1]-p[i,1])**2
        sm += a[i,2]*(value[2]-p[i,2])**2
        s += c[i]*np.exp(-sm)
        
    result = -s
    return result

# Format Assumption: <instance> <specifics> <runtime cutoff> <runlength> <seed> <solver parameters>

inst = sys.argv[1]
spec = sys.argv[2] # ignored
time_ = sys.argv[3] # ignored
runlength = sys.argv[4] # ignored
seed = sys.argv[5] # ignored
params = sys.argv[6:]

config_dict = dict((name.lstrip("-"), value.strip("'")) for name, value in zip(params[::2], params[1::2]))

# fixed function values encoded in instance name: e.g., x1_1_x2_10 -> "x1":1, "x2":10

instance_split = inst.split("_")
instance_dict = dict((name, value.strip("'")) for name, value in zip(instance_split[::2], instance_split[1::2]))

config_dict.update(instance_dict)

#print(config_dict)
y = _get_har3(float(config_dict["x1"]), float(config_dict["x2"]), float(config_dict["x3"]))

print("Result for ParamILS: SAT, 0.001, 1, %.4f, %s" % (y, str(seed)))

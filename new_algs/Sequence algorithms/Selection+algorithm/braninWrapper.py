'''
    branin function as toy example
    given function values are encoded in the instance name
    Call:
    python braninWrapper.py x1_1 blub 1 1 1 -x2 1
'''

import sys
import math

def _get_branin_value(x1, x2):
        '''
            Evaluates the Branin test function with arguments x1 and x2.
            You can replace this with your own function to minimize.
        '''
        return math.pow(x2 - (5.1 / (4 * math.pi * math.pi)) *x1*x1 + (5 / (math.pi)) *x1 -6,2) + 10*(1- (1 / (8 * math.pi))) * math.cos(x1) + 10


# Format Assumption: <instance> <specifics> <runtime cutoff> <runlength> <seed> <solver parameters>

inst = sys.argv[1]
spec = sys.argv[2] # ignored
print "Unique SMAC identifier: " + str(spec)
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
y = _get_branin_value(float(config_dict["x1"]), float(config_dict["x2"]))

print("Result for ParamILS: SAT, 0.001, 1, %.4f, %s" % (y, str(seed)))

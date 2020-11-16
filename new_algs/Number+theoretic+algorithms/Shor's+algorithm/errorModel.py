import simulation as sim
from myAlgo import *
N = 15
a = 4
qc = adder(3, 4, 4)
print(sim.ind_mySim(qc, 0))
print(sim.noise_sim(qc))
print(sim.ind_mySim(qc, 1))

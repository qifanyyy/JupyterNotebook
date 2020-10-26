from myAlgo import shorSequential, shorSequential_rev2
import simulation as sim
#print(shorSequential(15, 4))
qc = shorSequential_rev2(15, 4)
res = sim.mySim(qc)
print(res)

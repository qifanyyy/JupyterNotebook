from qiskit.circuit.library import QFT
from qiskit import QuantumRegister,QuantumCircuit
from qiskit.visualization import plot_histogram
import simulation as sim
import argparse
from gateSet import myR

args = sim.process_command()
qc = QFT(3)

for i in range(3):
    qr=QuantumRegister(3)
    qc = QuantumCircuit(qr)
    qc.x(qr[0])
    qc.x(qr[2])
    gate = QFT(3,approximation_degree=i)
    inv = QFT(3,inverse=True,approximation_degree=i)
    qc.append(gate,qargs=qr[:])
    qc.append(inv,qargs=qr[:])
    print(qc)
    qc.measure_all()
    res=sim.mySim(qc,args)
    plot_histogram(res).savefig(f'testQFT_{i}.png')
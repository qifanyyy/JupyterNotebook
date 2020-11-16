from qiskit_fast_shor import Shor
from qiskit import Aer, IBMQ

IBMQ.load_account()

a, N = 2, 21

backend = Aer.get_backend('qasm_simulator')
# provider = IBMQ.load_account()
# backend = provider.get_backend('ibmq_qasm_simulator')

if N == 33:
    job_id = "5ecaeb4bd2d11d001a1aaf72"
elif N == 15:
    job_id = "5ecae5ed4f56e200131772af"
else:
    job_id = None
shor = Shor(N, a, quantum_instance=backend, job_id=job_id)
print("Constructing...")
circuit = shor.construct_circuit()
print("Running...")
res = shor.run()
p, q = res["factors"][0]
print("p, q = {}, {}".format(p, q))
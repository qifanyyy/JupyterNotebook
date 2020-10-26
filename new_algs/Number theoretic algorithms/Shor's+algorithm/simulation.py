from qiskit.providers.aer.noise import NoiseModel
#from qiskit_qcgpu_provider import QCGPUProvider
import argparse
import os
import matplotlib.pyplot as plt
import time
import qiskit as qk
import numpy as np
import math
from psutil import virtual_memory
mem = virtual_memory()
allo_mem = math.ceil(mem.available*0.9)
qk.IBMQ.load_account()


def sort_by_key(result):
    bitlen = len(next(iter(result.keys())))
    sorted_result = [('{n:0{b}b}'.format(n=i, b=bitlen),
                      result.get('{n:0{b}b}'.format(n=i, b=bitlen), 0))
                     for i in range(2**bitlen)]
    return sorted_result


def sort_by_prob(result):
    return sorted([(k, result[k]) for k in result.keys()], key=lambda x: x[1],
                  reverse=True)


def noise_sim(cir):
    provider = qk.IBMQ.get_provider('ibm-q-hub-ntu')
    backend = provider.get_backend('ibmq_cambridge')
    noise_model = NoiseModel.from_backend(backend, gate_error=False)

    coupling_map = backend.configuration().coupling_map
    basis_gates = noise_model.basis_gates
    result = qk.execute(cir, qk.Aer.get_backend('qasm_simulator'),
                        coupling_map=coupling_map,
                        basis_gates=basis_gates,
                        noise_model=noise_model, shots=8192).result()
    counts = result.get_counts()
    return counts


def ind_mySim(cir, ctrl):
    provider = qk.IBMQ.get_provider('ibm-q-hub-ntu')
    if ctrl:
        backend = qk.Aer.get_backend('qasm_simulator')
    else:
        backend = provider.get_backend('ibmq_cambridge')

    sim_res = qk.execute(cir, backend, shots=8192, optimization_level=1)
    # qk.tools.job_monitor(sim_res)
    sim_result = sim_res.result()
    counts = sim_result.get_counts()

    return counts


def single_mySim(cir):
    provider = qk.IBMQ.get_provider('ibm-q-hub-ntu')
    backend = qk.Aer.get_backend('qasm_simulator')
    #backend = provider.get_backend('ibmq_qasm_simulator')

    sim_res = qk.execute(cir, backend, shots=1, optimization_level=1)
    qk.tools.job_monitor(sim_res)
    sim_result = sim_res.result()
    counts = sim_result.get_counts()

    return counts


def mySim(cir, args=None, method='qasm'):

    provider = qk.IBMQ.get_provider('ibm-q-hub-ntu')
    sim_type = method+'_simulator'
    if args == None:
        backend = qk.Aer.get_backend('qasm_simulator')
        backend_options = {"method": "statevector"}
        sim_res = qk.execute(cir, backend, shots=8192,
                             optimization_level=1, backend_options=backend_options)
        qk.tools.job_monitor(sim_res)
        return sim_res.result().get_counts()
    if args.real:
        backend = provider.get_backend('ibmq_cambridge')
    else:
        if args.simulation == 'local':

            backend = qk.Aer.get_backend(sim_type)
        elif args.simulation == 'ibmq':
            backend = provider.get_backend('ibmq_qasm_simulator')
        else:
            print("Choose default backend...local.")
            backend = qk.Aer.get_backend(sim_type)

    try:
        beg = time.time()
        if args.gpu:
            backend_options = {"method": "statevector_gpu"}
        else:
            backend_options = {"method": "statevector"}
        sim_res = qk.execute(cir, backend, shots=8192,
                             optimization_level=1, backend_options=backend_options)
        end = time.time()
        # qk.tools.job_monitor(sim_res)
        sim_result = sim_res.result()
        job_uid = sim_res.job_id()

        counts_result = sim_result.get_counts()
        
        print(f"Time cost: {end-beg} s")
    except Exception as e:
        print(e)
        if e == Exception('IBMQJobFailureError'):
            print(sim_res.error_message())

    # print(counts_result)
    return counts_result


def gpuSim(cir):

    backend_options = {"method": "statevector_gpu", "max_memory_mb": allo_mem}
    backend = qk.Aer.get_backend("qasm_simulator")

    beg = time.time()
    # Compile and run the Quantum circuit on a simulator backend
    job_sim = qk.execute(cir, backend,
                         backend_options=backend_options)
    qk.tools.job_monitor(job_sim)
    end = time.time()
    sim_result = job_sim.result()

    # Show the results

    time_cost = np.round(end-beg, 5)
    print(f"GPU sim time: {time_cost}")
    print(sim_result.get_counts())
    return time_cost


def cpuSim(cir):
    backend_options = {"method": "statevector"}
    backend = qk.Aer.get_backend("qasm_simulator")

    beg = time.time()
    # Compile and run the Quantum circuit on a simulator backend
    job_sim = qk.execute(cir, backend, backend_options=backend_options)
    sim_result = job_sim.result()

    # Show the results
    # print(sim_result.get_counts())
    end = time.time()
    time_cost = np.round(end-beg, 5)
    print(f"CPU sim time: {time_cost}")
    return time_cost


def timeCMP(gtime, ctime):
    if gtime < ctime:
        print(f"The GPU is faster by {100-100*np.round((gtime/ctime),3)}%")
    if gtime >= ctime:
        print(f"The GPU is slower by {100-100*np.round((ctime/gtime),3)}%")


def process_command():
    parser = argparse.ArgumentParser()
    method = parser.add_mutually_exclusive_group()
    method.add_argument('--simulation', '--sim', '-s', metavar='local/ibmq')
    method.add_argument('--real', '-r', action='store_true')
    parser.add_argument('--simcmp', action='store_true')
    parser.add_argument('--gpu', action='store_true')
    gate = parser.add_mutually_exclusive_group(required=True)
    gate.add_argument('--adder', nargs=3, type=int, metavar=('a', 'b', 'n'))
    gate.add_argument('--phimod', nargs=4, type=int,
                      metavar=('n', 'b', 'a', 'N'))
    gate.add_argument('--cmult', nargs=5, type=int,
                      metavar=('n', 'x', 'b', 'a', 'N'))
    gate.add_argument('--cu', nargs=4, type=int, metavar=('n', 'x', 'a', 'N'))
    gate.add_argument('--nor', nargs=2, type=int, metavar=('N', 'a'))
    gate.add_argument('--seq', nargs=2, type=int, metavar=('N', 'a'))

    #parser.add_argument('--test','-t',required=True, metavar='gate/algo')
    parser.add_argument('--output', '-o', action='store_true')
    parser.add_argument('--draw', '-d', action='store_true')
    parser.add_argument('--log', '-l', action='store_true')
    # parser.add_argument('--parameter','--para','-p',required=True,metavar='parameter')
    return parser.parse_args()

import numpy as np, matplotlib.pyplot as plt
from shors_quantum import periodFind
from pprint import pprint
from numpy import kron, sqrt, pi, dot, exp, squeeze, cos, sin, log2, binary_repr as binr
from numpy.random import randint
from progressbar import ProgressBar

# DECLARE STATIC GATES
H_mat = np.matrix([
    [1/sqrt(2), 1/sqrt(2)],
    [1/sqrt(2), -1/sqrt(2)]
])
I = np.identity(2)
CNOT_mat = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
])
SWAP_mat = np.array([
    [1, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1]
])

N = 15
x = 7
num_wires = int(np.ceil(log2(N)))
num_wires = 8
num_wires_phase = int(num_wires)
num_wires_phase = 4
mat_size = int(2 ** num_wires)
mat_size_phase = int(2 ** num_wires_phase)
# print(mat_size)

# 1 IDENTITY
# 2 HADAMARD
# 3 CNOT
# 4 PHASE
# 5 CPHASE
# 6 SWAP
# print(periodFind(3, 7))

def Hadamard(circuit, target_wire):
    inp = np.zeros((mat_size, 1))
    inp[11] = 1
    # Build a list of everything to kron
    stage = np.zeros((mat_size, 1))
    stage.fill(1)
    # Keep track of stages
    total_gate = np.identity(mat_size)

    gate = np.matrix([[1]])
    stage[target_wire] = 2

    for i in stage:
        if i == 1:
            gate = kron(gate, I)
        elif i == 2:
            gate = kron(gate, H_mat)

    unitary = gate
    print(unitary)
    if not circuit:
        new = unitary
    else:
        new = dot(circuit, unitary)
    return new


def CNOT(circuit, input_bit, cbit):
    inp = np.zeros((mat_size, 1))
    inp[11] = 1
    swap_count = abs(input_bit-cbit)
    # Build a list of everything to kron
    state = np.zeros((mat_size-1, 1))
    # Keep track of stages
    total_gate = np.identity(mat_size)

    # SWAP DOWNWARDS
    for s in range(0, swap_count):
        gate = np.matrix([[1]])
        state.fill(1)
        if s == swap_count-1:
            state[input_bit-1, 0] = 3
            swap_down = total_gate
        else:
            state[cbit+s, 0] = 6
        print(state)
        for i in state:
            if i == 1:
                gate = kron(gate, I)
            elif i == 3:
                gate = kron(gate, CNOT_mat)
            elif i == 6:
                gate = kron(gate, SWAP_mat)

    cnot = gate
    swap_up = np.conj(swap_down).T
    result = (swap_up @ (cnot @ swap_down)) @ inp
    unitary = np.conj(swap_down).T @ (cnot @ swap_down)
    print(result)

    if not circuit:
        new = unitary
    else:
        new = dot(circuit, unitary)
    return new


def CPhase(circuit, target_wire, cbit, phase):
    CPhase_mat = np.matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, exp(1j*float(phase))]
    ])
    inp = np.zeros((mat_size, 1))
    inp[11] = 1
    swap_count = abs(target_wire-cbit)
    # Build a list of everything to kron
    stage = np.zeros((mat_size-1, 1))
    # Keep track of stages
    total_gate = np.identity(2**mat_size)

    # SWAP DOWNWARDS
    for s in range(0, swap_count):
        gate = np.matrix([[1]])
        stage.fill(1)
        if s == swap_count-1:
            stage[target_wire-1, 0] = 5
            swap_down = total_gate
        else:
            stage[cbit+s, 0] = 6
        print(stage)
        for i in stage:
            if i == 1:
                gate = kron(gate, I)
            elif i == 5:
                gate = kron(gate, CPhase_mat)
            elif i == 6:
                gate = kron(gate, SWAP_mat)

    cphaseU = gate
    swap_up = np.conj(swap_down).T
    result = (swap_up @ (cphaseU @ swap_down)) @ inp
    unitary = np.conj(swap_down).T @ (cphaseU @ swap_down)

    if not circuit:
        new = unitary
    else:
        new = dot(circuit, unitary)
    return new

# CNOT([], 3, 0)
# CPhase([], 2, 0, pi)


def QFT(circuit):
    print(num_wires)
    unitaries = np.identity(mat_size)
    for i in range(num_wires, -1, -1):
        for R in range(num_wires-i, 0, -1):
            target_wire, cbit = i+R, i
            phase = pi/(2**(num_wires-(target_wire)))
            print('R', target_wire, cbit, phase)
            unitary = CPhase([], target_wire, cbit, phase)
            unitaries = unitaries @ unitary

        # MAKE HADAMARD
        print('H', i)
        unitaries = kron(kron(np.conj(Hadamard([], i) @ unitaries).T, I), I)
        circuit = circuit @ unitaries
    return circuit

# handles the hadamards and control unitaries
def controlXYmodN(circuit, cbit, target1, num_targets):
    uni = np.identity(mat_size_phase)
    hads = np.matrix([[1]])
    for i in range(0, num_wires_phase):
        hads = kron(hads, H_mat)
    uni = uni @ hads
    num_unis = 2**(target1-cbit-1)
    for count in range(0, num_unis):
        mat = np.zeros((mat_size_phase, mat_size_phase))
        # +1 for the adjacent cbit
        for j in range(0, 2**(num_targets+1)):
            bin_j = binr(j, num_wires_phase)
            print(bin_j)

            if bin_j[cbit] == '0':
                mat[j, j] = 1
            elif bin_j[cbit] == '1':
                print(x*int(bin_j[target1:], 2) % N)
                mat[(x*int(bin_j[target1:], 2) % N), j] = 1
        uni = uni @ mat
    if not circuit:
        new = uni
    else:
        new = circuit @ uni
    return new

def Phase(circuit, qbit, shift):
    P_mat = np.matrix([
        [1, 0],
        [0, exp(1j*float(shift))]
    ])
    if qbit == 0:
        gate = kron(kron(P_mat, I), I)
    elif qbit == 1:
        gate = kron(kron(I, P_mat), I)
    elif qbit == 2:
        gate = kron(kron(I, I), P_mat)
    else:
        print('Invalid wire')

    if circuit == []:
        new = gate
    else:
        new = dot(circuit, gate)
    return new


def Pauli(circuit, qbit, type):
    if type == 'X':
        Pauli_mat = np.matrix([
        [0, 1],
        [1, 0]
    ])
    elif type == 'Y':
        Pauli_mat = np.matrix([
            [0, -1j],
            [-1j, 0]
        ])
    else:
        Pauli_mat = np.matrix([
            [1, 0],
            [0, -1]
        ])

    if qbit == 0:
        gate = kron(kron(Pauli_mat, I), I)
    elif qbit == 1:
        gate = kron(kron(I, Pauli_mat), I)
    elif qbit == 2:
        gate = kron(kron(I, I), Pauli_mat)
    else:
        print('Invalid wire')

    if circuit == []:
        new = gate
    else:
        new = dot(circuit, gate)
    return new


def Rotate(circuit, qbit, type, theta):
    if type == 'X':
        R_mat = np.matrix([
        [cos(theta/2), -j*sin(theta/2)],
        [-j*sin(theta/2), cos(theta/2)]
    ])
    elif type == 'Y':
        R_mat = np.matrix([
            [cos(theta/2), -1*sin(theta/2)],
            [sin(theta/2), cos(theta/2)]
        ])
    else:
        R_mat = np.matrix([
            [exp(-1j*theta/2), 0],
            [0, exp(1j*theta/2)]
        ])

    if qbit == 0:
        gate = kron(kron(R_mat, I), I)
    elif qbit == 1:
        gate = kron(kron(I, R_mat), I)
    elif qbit == 2:
        gate = kron(kron(I, I), R_mat)
    else:
        print('Invalid wire')

    if circuit == []:
        new = gate
    else:
        new = dot(circuit, gate)
    return new


def genRandCircuit(num_gates):
    gate_nums = [randint(0,3) for x in range(0, num_gates)]
    myInput = []
    
    for gate_num in gate_nums:
        if gate_num == 0:
            myInput.append(['H', randint(0,3)])
        if gate_num == 1:
            firstwire = randint(1,3)
            myInput.append(['CNOT', firstwire, firstwire-1])
        if gate_num == 2:
            myInput.append(['P', randint(0,3), randint(0, 2*pi*100)/100])
    myInput.append(['Measure'])
    return myInput


def ReadDescription(fileName):
    myInput_lines=open(fileName).readlines()
    myInput=[]
    numberOfWires=int(myInput_lines[0])
    for line in myInput_lines[1:]:
        myInput.append(line.split())
    return (numberOfWires,myInput)


def ReadInput(fileName):
    myInput_lines=open(fileName).readlines()
    myInput = []
    for line in myInput_lines:
        myInput.append(complex(float(line.split()[0]), float(line.split()[1])))
    myInput = np.array(myInput, dtype=complex)
    return myInput


def measure(result):
    p_list = [x**2 for x in result]
    plt.plot([x for x in range(0,8)], p_list)
    plt.show()

    return


def genCircuit(myInput, inverse):
    circuit = []
    if inverse:
        if myInput[-1] == ['Measure']:
            myInput = myInput[len(myInput)-2::-1]
            myInput.append(['Measure'])
        else: 
            myInput = myInput[::-1]
    print(myInput)
        
    for gate in myInput:
        if gate[0] == 'H':
            circuit = Hadamard(circuit, int(gate[1]))
        elif gate[0] == 'PX':
            circuit = Pauli(circuit, int(gate[1]), 'X')
        elif gate[0] == 'PY':
            circuit = Pauli(circuit, int(gate[1]), 'Y')
        elif gate[0] == 'PZ':
            circuit = Pauli(circuit, int(gate[1]), 'Z')
        elif gate[0] == 'RX':
            circuit = Rotate(circuit, int(gate[1]), 'X', int(gate[2]))
        elif gate[0] == 'RY':
            circuit = Rotate(circuit, int(gate[1]), 'Y', int(gate[2]))
        elif gate[0] == 'CFUNC':
            circuit = controlXYmodN(circuit, int(gate[1]), int(gate[2]), int(gate[3]))
        elif gate[0] == 'RZ':
            circuit = Rotate(circuit, int(gate[1]), 'Z')
        elif gate[0] == 'CNOT':
            circuit = CNOT(circuit, int(gate[1]), int(gate[2]))
        elif gate[0] == 'R':
            circuit = CPhase(circuit, int(gate[1]), int(gate[2]), float(gate[3]))
        elif gate[0] == 'P':
            if inverse:
                circuit = Phase(circuit, -1*gate[2], int(gate[1]))
            else:
                circuit = Phase(circuit, gate[2], int(gate[1]))
        elif gate[0] == 'Measure':
            result = np.reshape(squeeze(np.asarray(
                dot(inputState,circuit)
                    )), 
                (8,1)
            ).flatten()
            
    return circuit, result

# myInput = ReadDescription("circuit_desc.txt")


# inputState = np.array(ReadInput('myInputState.txt'))

# myInput = genRandCircuit(24)
# circuit, result = genCircuit(myInput, False)
# inv_circuit = genCircuit(myInput, True)[0]

#inv_circuit = np.linalg.inv(circuit)
# print(dot(result, inv_circuit))

import qutip

def graph(vec):
    b=qutip.Bloch()
    up=qutip.basis(2,0)
    down=qutip.basis(2,1)
    b.add_states(vec[0]*up+vec[1]*down)
    b.show()

np.set_printoptions(threshold=np.nan)

in_state = np.zeros((1, 16))
in_state[0, 15] = 1

circuit = controlXYmodN([], 0, 1, 3)
circuit = QFT(circuit)
print(circuit)

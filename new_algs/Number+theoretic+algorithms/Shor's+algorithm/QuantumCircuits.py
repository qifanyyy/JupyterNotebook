from qiskit import QuantumProgram
from qiskit import QuantumCircuit
from qiskit import QuantumRegister
from qiskit import ClassicalRegister
from IPython.display import clear_output
from math import sqrt; from itertools import count, islice
from qiskit import Result
import PrintUtils
import QConfig
import random
import math

class Circuits:
    # String constants for circuit names
    PERIOD = "circuit_period" # find_period() quantum circuit

class QRegs:
    # String constants for quantum register names
    PERIOD = "qreg_period" # find_period() quantum register

class CRegs:
    # String constants for classical register names
    PERIOD = "creg_period" # find_period() classical register

class QuantumPrograms:
    PROGRAMS = {
        "find_period": "Takes two integers, a and N, and finds the period of the modular exponentiation function.",
        "factorize_N": "Takes an integer N and finds factors of N using Shor's algorithm."
    }
    """
    A class containing quantum circuits used in Shor's algorithm.
    Constructor takes an instance of a QuantumProgram object from QISKit module
    in order to create the circuits/run code on the IBM Quantum Experience hardware.
    """

    def __init__(self, quantum_program: QuantumProgram, qconfig: QConfig):
        """Store QuantumProgram instance in self."""
        self.qp = quantum_program
        self.qconf = qconfig
    
    def gcd(self, a, b):
        """Find Greatest Common Divisor (GCD) using Euclid's algorithm"""
        while b != 0:
            (a, b) = (b, a % b)
        return a
    
    def isPrime(self, n):
        return n > 1 and all(n%i for i in islice(count(2), int(sqrt(n)-1)))

    def factorize_N(self, N, numRetries=0):
        """Factorize N using Shor's algorithm."""
        PrintUtils.printInfo(f"Factorizing N={N}...")
        if numRetries > 0:
            clear_output()
            if numRetries > 1:
                PrintUtils.delete_last_lines(6)
            else:
                PrintUtils.delete_last_lines(5)
            PrintUtils.printInfo(f"Factorizing N={N}...")
            PrintUtils.printWarning(f"Chose unlucky 'a' value, trying again with new 'a' value ({PrintUtils.toOrdinal(numRetries + 1)} try so far)...")
        
        # Step 1: check if N is even; if so, simply divide by 2 and return the factors
        if N % 2 == 0:
            return [2, int(N/2)]
        # Step 2: choose random value for 'a' between 2..(N-1)
        a = random.randint(2, N-1)
        PrintUtils.printInfo(f"Selected random value a={a} to find period.")
        # Step 3: determine if common period exists
        t = self.gcd(N, a)
        if t > 1:
            PrintUtils.printInfo(f"Found common period between N={N} and a={a}")
            PrintUtils.printSuccess(f"Took {numRetries + 1} guesses for 'a' value.             ")
            return [t, int(N/t)]
        # Step 4: t=1, thus, N and a do not share common period. Find period using Shor's method.
        PrintUtils.printInfo("Using Shor's method to find period...")
        r = self.find_period(a, N)
        factor1 = self.gcd((a**(r/2))+1, N)
        if factor1 % N == 0 or factor1 == 1 or factor1 == N or not(self.isPrime(factor1)):
            return self.factorize_N(N, numRetries + 1)
        factor2 = N/factor1
        if not self.isPrime(factor2):
            return self.factorize_N(N, numRetries + 1)
        PrintUtils.printSuccess(f"Took {numRetries + 1} guesses for 'a' value.             ")
        return [int(factor1), int(factor2)]
    
    def find_period(self, a, N):
        """
        Find the period of the modular exponentiation function, 
        i.e. find r where (a^x) % N=(a^[x + r]) % N where x is any integer.
        For example:
        (7^2) % 15 = 4 % 15 = 4
        (7^3) % 15 = (4 * 7) % 15 = 13 % 15 = 13
        (7^4) % 15 = (13 * 7) % 15 = 91 % 15 = 1
        Thus, for a=7 and N=15, the periodic sequence is  (7^x) % 15 = (7^[x + 4]) % 15 for any integer x;
        therefore, the period for the modular exponentiation function for a=7 and N=15 is r=4.
        Returns a tuple containing the value of r and the number of iterations required to find r,
        (r, iterCount)
        """
        self.create_modular_multiplication_circuit()
        iterCount = 0
        r = math.inf # initialize r to infinity 
        while not ((r%2 == 0) and (((a**(r/2))+1)%N != 0) and (r != 0) and (r != 8)):
            iterCount += 1
            result: Result = self.qp.execute([Circuits.PERIOD], backend=self.qconf.backend, shots=self.qconf.shots, timeout=self.qconf.timeout)
            # print(result)
            data = result.get_counts(Circuits.PERIOD)
            # print(data)
            data = list(data.keys())
            # print(data)
            r = int(data[0])
            # print(r)
            l = self.gcd(2**3, r)
            # print(l)
            r = int((2**3)/l)
            # print(r)
        return r

    def create_modular_multiplication_circuit(self):
        qr = self.qp.create_quantum_register(QRegs.PERIOD, 5)
        cr = self.qp.create_classical_register(CRegs.PERIOD, 3)
        self.qp.create_circuit(Circuits.PERIOD, [qr], [cr])
        # re-fetch circuit and registers by name 
        circuit: QuantumCircuit  = self.qp.get_circuit(Circuits.PERIOD)
        qreg: QuantumRegister = self.qp.get_quantum_register(QRegs.PERIOD)
        creg: ClassicalRegister = self.qp.get_classical_register(CRegs.PERIOD)
        
        ## Set up the quantum circuit
        # Initialize: set qreg[0] to |1> and 
        # create superposition on top 8 qbits
        circuit.x(qreg[0])

        ## Step 1: apply a^4 % N
        circuit.h(qreg[2])
        # Controlled Identity gate
        circuit.h(qreg[2])
        circuit.measure(qreg[2], creg[0]) # store the result
        # Reinitialize to |0>
        circuit.reset(qreg[2])
        ## Step 2: apply a^2 % N
        circuit.h(qreg[2])
        # Controlled Identity gate 
        if creg[0] == 1:
            circuit.u1(math.pi/2.0, qreg[2])
        circuit.h(qreg[2])
        circuit.measure(qreg[2], creg[1]) # store the result
        # Reinitialize to |0>
        circuit.reset(qreg[2])
        ## step 3: apply a % N
        circuit.h(qreg[2])
        # Controlled NOT (C-NOT) gate in between remaining gates
        circuit.cx(qreg[2], qreg[1])
        circuit.cx(qreg[2], qreg[4])

        ## Feed forward 
        if creg[1] == 1:
            circuit.u1(math.pi/2.0, qreg[2])
        if creg[0] == 1:
            circuit.u1(math.pi/4.0, qreg[2])
        circuit.h(qreg[2])
        circuit.measure(qreg[2], creg[2]) # store the result
        # print(circuit.qasm()) # print QASM code


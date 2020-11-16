#!/usr/bin/env python
# coding: utf-8

# In[14]:


# -*- coding: utf-8 -*-
# (C) Copyright IBM 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
#
#
# **** IMPORTANT NOTE****
#
# The original code is part of Qiskit and it can be found in the link below: 
# https://qiskit.org/documentation/_modules/qiskit/aqua/algorithms/single_sample/shor/shor.html#Shor
# 
# This is an alternative code that implements 
# the Sequential Fourier Transform (one qubit instead of 2*n). 
#The methods that they were modified are "construct_circuit" and "run"

"""
The Shor's Factoring algorithm.  This implementation is based on the following paper:
S. Parker and M.B. Plenio (2000), "Efficient factorization with a single pure qubit and logN mixed qubits",
Phys. Rev. Lett., 85, pp. 3049-3052
"""

import math
import array
import fractions
import logging
import numpy as np
import itertools

from qiskit import IBMQ, ClassicalRegister, QuantumCircuit, QuantumRegister, Aer, execute

from qiskit.aqua.utils.arithmetic import is_power
from qiskit.aqua import AquaError, Pluggable, QuantumInstance
from qiskit.aqua.utils import get_subsystem_density_matrix
from qiskit.aqua.algorithms import QuantumAlgorithm
from qiskit.aqua.circuits import FourierTransformCircuits as ftc
from qiskit.aqua.circuits.gates import mcu1  # pylint: disable=unused-import
from qiskit.aqua.utils import summarize_circuits


logger = logging.getLogger(__name__)

# pylint: disable=invalid-name


class Shor(QuantumAlgorithm):
    """
    The Shor's Factoring algorithm.

    Adapted from https://github.com/ttlion/ShorAlgQiskit
    """

    PROP_N = 'N'
    PROP_A = 'a'

    CONFIGURATION = {
        'name': 'Shor',
        'description': "The Shor's Factoring Algorithm",
        'input_schema': {
            '$schema': 'http://json-schema.org/draft-07/schema#',
            'id': 'shor_schema',
            'type': 'object',
            'properties': {
                PROP_N: {
                    'type': 'integer',
                    'default': 15,
                    'minimum': 3
                },
                PROP_A: {
                    'type': 'integer',
                    'default': 2,
                    'minimum': 2
                },
            },
            'additionalProperties': False
        },
        'problems': ['factoring'],
    }

    def __init__(self, N=15, a=2):
        """
        Constructor.

        Args:
            N (int): The integer to be factored.
            a (int): A random integer a that satisfies a < N and gcd(a, N) = 1
         Raises:
            AquaError: invalid input
        """
        self.validate(locals())
        super().__init__()
        self._n = None
        self._up_qreg = None
        self._down_qreg = None
        self._aux_qreg = None
        self._quantum_instance = None

        # check the input integer
        if N < 1 or N % 2 == 0:
            raise AquaError('The input needs to be an odd integer greater than 1.')

        self._N = N

        if a >= N or math.gcd(a, self._N) != 1:
            raise AquaError('The integer a needs to satisfy a < N and gcd(a, N) = 1.')

        self._a = a

        self._ret = {'factors': []}

        # check if the input integer is a power
        # for example for N = 15 --> False, 15, 1
        # for N = 16 --> True, 4, 2
        tf, b, p = is_power(N, return_decomposition=True)
        if tf:
            logger.info('The input integer is a power: %s=%s^%s.', N, b, p)
            self._ret['factors'].append(b)
    
    # A class method is a method that is bound to a class rather than its object. 
    # It doesn't require creation of a class instance
    @classmethod
    def init_params(cls, params, algo_input):
        # Always use self for the first argument to instance methods.
        # Always use cls for the first argument to class methods.
        
        """
        Initialize via parameters dictionary and algorithm input instance.

        Args:
            params (dict): parameters dictionary
            algo_input (AlgorithmInput): input instance
        Returns:
            Shor: instance of this class
        Raises:
            AquaError: invalid input
        """

        if algo_input is not None:
            raise AquaError("Input instance not supported.")

        shor_params = params.get(Pluggable.SECTION_KEY_ALGORITHM)
        N = shor_params.get(Shor.PROP_N)

        return cls(N)


    def _get_angles(self, a):
        """
        Calculate the array of angles to be used in the addition in Fourier Space
        """
        s = bin(int(a))[2:].zfill(self._n + 1)
        angles = np.zeros([self._n + 1])
        for i in range(0, self._n + 1):
            for j in range(i, self._n + 1):
                if s[j] == '1':
                    angles[self._n - i] += math.pow(2, -(j - i))
            angles[self._n - i] *= np.pi
        return angles
    
    """Function that calculates the angle of a phase shift in the sequential QFT based on the binary digits of a."""
    """a represents a possile value of the classical register"""
    def get_angle(self, a, N):
        """convert the number a to a binary string with length N"""
        s=bin(int(a))[2:].zfill(N) 
        angle = 0
        for i in range(0, N):
            """if the digit is 1, add the corresponding value to the angle"""
            if s[N-1-i] == '1': 
                angle += math.pow(2, -(N-i))
        angle *= np.pi
        return angle

    def _phi_add(self, circuit, q, inverse=False):
        """
        Creation of the circuit that performs addition by a in Fourier Space
        Can also be used for subtraction by setting the parameter inverse=True
        """
        angle = self._get_angles(self._N)
        for i in range(0, self._n + 1):
            circuit.u1(-angle[i] if inverse else angle[i], q[i])

    def _controlled_phi_add(self, circuit, q, ctl, inverse=False):
        """
        Single controlled version of the _phi_add circuit
        """
        angles = self._get_angles(self._N)
        for i in range(0, self._n + 1):
            angle = (-angles[i] if inverse else angles[i]) / 2

            circuit.u1(angle, ctl)
            circuit.cx(ctl, q[i])
            circuit.u1(-angle, q[i])
            circuit.cx(ctl, q[i])
            circuit.u1(angle, q[i])

    def _controlled_controlled_phi_add(self, circuit, q, ctl1, ctl2, a, inverse=False):
        """
        Doubly controlled version of the _phi_add circuit
        """
        angle = self._get_angles(a)
        for i in range(self._n + 1):
            # ccphase(circuit, -angle[i] if inverse else angle[i], ctl1, ctl2, q[i])
            circuit.mcu1(-angle[i] if inverse else angle[i], [ctl1, ctl2], q[i])

    def _controlled_controlled_phi_add_mod_N(self, circuit, q, ctl1, ctl2, aux, a):
        """
        Circuit that implements doubly controlled modular addition by a
        """
        self._controlled_controlled_phi_add(circuit, q, ctl1, ctl2, a)
        self._phi_add(circuit, q, inverse=True)
        ftc.construct_circuit(
            circuit=circuit,
            qubits=[q[i] for i in reversed(range(self._n + 1))],
            do_swaps=False,
            inverse=True
        )
        circuit.cx(q[self._n], aux)
        ftc.construct_circuit(
            circuit=circuit,
            qubits=[q[i] for i in reversed(range(self._n + 1))],
            do_swaps=False
        )
        self._controlled_phi_add(circuit, q, aux)

        self._controlled_controlled_phi_add(circuit, q, ctl1, ctl2, a, inverse=True)
        ftc.construct_circuit(
            circuit=circuit,
            qubits=[q[i] for i in reversed(range(self._n + 1))],
            do_swaps=False,
            inverse=True
        )
        circuit.u3(np.pi, 0, np.pi, q[self._n])
        circuit.cx(q[self._n], aux)
        circuit.u3(np.pi, 0, np.pi, q[self._n])
        ftc.construct_circuit(
            circuit=circuit,
            qubits=[q[i] for i in reversed(range(self._n + 1))],
            do_swaps=False
        )
        self._controlled_controlled_phi_add(circuit, q, ctl1, ctl2, a)

    def _controlled_controlled_phi_add_mod_N_inv(self, circuit, q, ctl1, ctl2, aux, a):
        """
        Circuit that implements the inverse of doubly controlled modular addition by a
        """
        self._controlled_controlled_phi_add(circuit, q, ctl1, ctl2, a, inverse=True)
        ftc.construct_circuit(
            circuit=circuit,
            qubits=[q[i] for i in reversed(range(self._n + 1))],
            do_swaps=False,
            inverse=True
        )
        circuit.u3(np.pi, 0, np.pi, q[self._n])
        circuit.cx(q[self._n], aux)
        circuit.u3(np.pi, 0, np.pi, q[self._n])
        ftc.construct_circuit(
            circuit=circuit,
            qubits=[q[i] for i in reversed(range(self._n + 1))],
            do_swaps=False
        )
        self._controlled_controlled_phi_add(circuit, q, ctl1, ctl2, a)
        self._controlled_phi_add(circuit, q, aux, inverse=True)
        ftc.construct_circuit(
            circuit=circuit,
            qubits=[q[i] for i in reversed(range(self._n + 1))],
            do_swaps=False,
            inverse=True
        )
        circuit.cx(q[self._n], aux)
        ftc.construct_circuit(
            circuit=circuit,
            qubits=[q[i] for i in reversed(range(self._n + 1))],
            do_swaps=False
        )
        self._phi_add(circuit, q)
        self._controlled_controlled_phi_add(circuit, q, ctl1, ctl2, a, inverse=True)

    def _controlled_multiple_mod_N(self, circuit, ctl, q, aux, a):
        """
        Circuit that implements single controlled modular multiplication by a
        """
        ftc.construct_circuit(
            circuit=circuit,
            qubits=[aux[i] for i in reversed(range(self._n + 1))],
            do_swaps=False
        )

        for i in range(0, self._n):
            self._controlled_controlled_phi_add_mod_N(
                circuit,
                aux,
                q[i],
                ctl,
                aux[self._n + 1],
                (2 ** i) * a % self._N
            )
        ftc.construct_circuit(
            circuit=circuit,
            qubits=[aux[i] for i in reversed(range(self._n + 1))],
            do_swaps=False,
            inverse=True
        )

        for i in range(0, self._n):
            circuit.cswap(ctl, q[i], aux[i])

        def modinv(a, m):
            def egcd(a, b):
                if a == 0:
                    return (b, 0, 1)
                else:
                    g, y, x = egcd(b % a, a)
                    return (g, x - (b // a) * y, y)

            g, x, _ = egcd(a, m)
            if g != 1:
                raise Exception('modular inverse does not exist')

            return x % m

        a_inv = modinv(a, self._N)
        ftc.construct_circuit(
            circuit=circuit,
            qubits=[aux[i] for i in reversed(range(self._n + 1))],
            do_swaps=False
        )

        for i in reversed(range(self._n)):
            self._controlled_controlled_phi_add_mod_N_inv(
                circuit,
                aux,
                q[i],
                ctl,
                aux[self._n + 1],
                math.pow(2, i) * a_inv % self._N
            )
        ftc.construct_circuit(
            circuit=circuit,
            qubits=[aux[i] for i in reversed(range(self._n + 1))],
            do_swaps=False,
            inverse=True
        )

    def construct_circuit(self):
        """Construct circuit.
            It is an implementation of Sequantial Fourier transform with only one qubit. 
        Returns:
            Dict: a dictionary with binary numbers such that are the best estimate of j/r.
            See report page 2
        """
        
        # Get n value used in Shor's algorithm, to know how many qubits are used
        self._n = math.ceil(math.log(self._N, 2))

        # quantum register where every gate is applied to
        self._up_qreg = QuantumRegister(1, name='up')
        # quantum register where the multiplications are made
        self._down_qreg = QuantumRegister(self._n, name='down')
        # auxiliary quantum register used in addition and multiplication
        self._aux_qreg = QuantumRegister(self._n + 2, name='aux')
        # classical register that hosts qubit's state
        self._up_cqreg = ClassicalRegister(1, name='m')
        
        # Create Quantum Circuit
        circuit = QuantumCircuit(self._up_qreg, self._down_qreg, self._aux_qreg, self._up_cqreg)
        
        # Initialize down register to 1.
        circuit.u3(np.pi, 0, np.pi, self._down_qreg[0])

        # a list that hosts the result of each measurement (0 or 1)
        # These elements are used for calculating the R'j gates
        m = []
        
        # a list with all the binary numbers with 2*n digits.
        # After every measurement elements are deleted
        binary_list = [list(i) for i in itertools.product([0, 1], repeat=2*self._n)]
        
        # Apply the multiplication gates as showed in
        # the report in order to create the exponentiation
        for i in range(2 * self._n-1, -1, -1):
            print(i)
            self._controlled_multiple_mod_N(
                circuit,
                self._up_qreg[0],
                self._down_qreg,
                self._aux_qreg,
                int(pow(self._a, pow(2, i)))
            )

            # Apply the Hadamard gate
            circuit.u2(0, np.pi, self._up_qreg)
            
            # Calculate the φ'j angle as it is written at the report
            angle = 0
            iter_j = 2*self._n - i
            
            for k in range(2, iter_j+1):
                if m[iter_j - k] == '1':
                    angle += math.pow(2, -k) 
            
            # Apply the R'j gate.
            circuit.u1(np.pi*angle, self._up_qreg[0])
            
            # Add measurement
            circuit.measure(self._up_qreg, self._up_cqreg)

            # Run the circuit with a classical computer
            backend = Aer.get_backend('qasm_simulator')
            results = execute(circuit, backend=backend).result()
            counts = results.get_counts()
            #print(counts)
            
            # Every measurement returns a dictionary. In this case "counts"
            # e.g. counts = {'1': 512, '0':512}
            # 1 and 0 will be always the keys.
            # The following numbers depend on the measurment.
            v = list(counts.values())
            k = list(counts.keys())
            
            # Decide which state will be add in m[] list
            if len(counts)>1:
                if v[0] > v[1]:
                    zero_wins = False
                    m.append(k[0])     
                else:
                    zero_wins = True
                    m.append(k[1])
                
                # Simulations and Quantum Computers are not perfect. 
                # We keep the binary numbers that they have 1 at position i
                # if state 1 is measured 128 times more than state 0, and vice versa.
                # 128 is a reference number when executing the circuit 1024 times.
                if abs(v[0] - v[1]) > 128:
                    if zero_wins:
                        binary_list = [x for x in binary_list if x[i]==0]
                    else:
                        binary_list = [x for x in binary_list if x[i]==1]          
            else:
                # in case that the dictionary has just one element.
                # e.g. counts = {'1': 1024}
                m.append(k[0])
                binary_list = [x for x in binary_list if x[i]==int(k[0])]
            
            # Remove measurement and add classical register back to the circuit.
            # Quantum Computers cannot run circuits when they have measuments gates before other gates.
            circuit.remove_final_measurements()
            circuit.add_register(self._up_cqreg)
            
        # A dictionary that holds all the possible binary numbers for the continuing fractions.
        # Keys (Binary numbers) are in string format and their value is always 1.
        # Value is useless
        # e.g. answer = {'01001010': 1}
        answer = {}

        for x in binary_list:
            answer["".join(map(str, x))] = 1  
        
        return answer
        
    def _get_factors(self, output_desired, t_upper):
        """
        Apply the continued fractions to find r and the gcd to find the desired factors.
        """
        x_value = int(output_desired, 2)
        logger.info('In decimal, x_final value for this result is: %s.', x_value)

        if x_value <= 0:
            self._ret['results'][output_desired] = 'x_value is <= 0, there are no continued fractions.'
            return False

        logger.debug('Running continued fractions for this case.')

        # Calculate T and x/T
        T = pow(2, t_upper)
        x_over_T = x_value / T

        # Cycle in which each iteration corresponds to putting one more term in the
        # calculation of the Continued Fraction (CF) of x/T

        # Initialize the first values according to CF rule
        i = 0
        b = array.array('i')
        t = array.array('f')

        b.append(math.floor(x_over_T))
        t.append(x_over_T - b[i])

        while i >= 0:

            # From the 2nd iteration onwards, calculate the new terms of the CF based
            # on the previous terms as the rule suggests
            if i > 0:
                b.append(math.floor(1 / t[i - 1]))
                t.append((1 / t[i - 1]) - b[i])

            # Calculate the CF using the known terms
            aux = 0
            j = i
            while j > 0:
                aux = 1 / (b[j] + aux)
                j = j - 1

            aux = aux + b[0]

            # Get the denominator from the value obtained
            frac = fractions.Fraction(aux).limit_denominator()
            denominator = frac.denominator

            logger.debug('Approximation number %s of continued fractions:', i + 1)
            logger.debug("Numerator:%s \t\t Denominator: %s.", frac.numerator, frac.denominator)

            # Increment i for next iteration
            i = i + 1

            if denominator % 2 == 1:
                if i >= self._N:
                    self._ret['results'][output_desired] = 'unable to find factors after too many attempts.'
                    return False
                logger.debug('Odd denominator, will try next iteration of continued fractions.')
                continue

            # If denominator even, try to get factors of N
            # Get the exponential a^(r/2)
            exponential = 0

            if denominator < 1000:
                exponential = pow(self._a, denominator / 2)

            # Check if the value is too big or not
            if math.isinf(exponential) or exponential > 1000000000:
                self._ret['results'][output_desired] = 'denominator of continued fraction is too big.'
                return False

            # If the value is not to big (infinity),
            # then get the right values and do the proper gcd()
            putting_plus = int(exponential + 1)
            putting_minus = int(exponential - 1)
            one_factor = math.gcd(putting_plus, self._N)
            other_factor = math.gcd(putting_minus, self._N)

            # Check if the factors found are trivial factors or are the desired factors
            if one_factor == 1 or one_factor == self._N or                     other_factor == 1 or other_factor == self._N:
                logger.debug('Found just trivial factors, not good enough.')
                # Check if the number has already been found,
                # use i-1 because i was already incremented
                if t[i - 1] == 0:
                    self._ret['results'][output_desired] = 'the continued fractions found exactly x_final/(2^(2n)).'
                    return False
                if i >= self._N:
                    self._ret['results'][output_desired] = 'unable to find factors after too many attempts.'
                    return False
            else:
                logger.debug('The factors of %s are %s and %s.', self._N, one_factor, other_factor)
                logger.debug('Found the desired factors.')
                self._ret['results'][output_desired] = (one_factor, other_factor)
                factors = sorted((one_factor, other_factor))
                if factors not in self._ret['factors']:
                    self._ret['factors'].append(factors)
                return True
        
    def _run(self):
        if not self._ret['factors']:
            logger.debug('Running with N=%s and a=%s.', self._N, self._a)
            
            # Running the code when the quantum instance is a state vector was removed.
            # See original code instead.
            counts = self.construct_circuit()
            self._ret['results'] = dict()

            # For each simulation result, print proper info to user
            # and try to calculate the factors of N
            for output_desired in list(counts.keys()):
                # Get the x_value from the final state qubits
                logger.info("------> Analyzing result %s.", output_desired)
                self._ret['results'][output_desired] = None
                success = self._get_factors(output_desired, int(2 * self._n))
                if success:
                    logger.info('Found factors %s from measurement %s.',
                                self._ret['results'][output_desired], output_desired)
                else:
                    logger.info('Cannot find factors from measurement %s because %s',
                                output_desired, self._ret['results'][output_desired])

        return self._ret

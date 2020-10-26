#!../venv/Scripts/python.exe
# -*- encoding : utf-8 -*-

"""
@Description:  quantum.py provides quantum materials to perform period finding research algorithm
@Author: Quentin Delamea
@Copyright: Copyright 2020, PyShor
@Credits: [Quentin Delamea]
@License: MIT
@Version: 0.0.1
@Maintainer: Quentin Delamea
@Email: qdelamea@gmail.com
@Status: Dev
"""

# External libs imports
import numpy as np
import qat.lang.AQASM.qftarith
from qat.core import Job
from qat.lang.AQASM import Program, H, X
from qat.lang.AQASM.arithmetic import modular_exp
from qat.lang.AQASM.qftarith import QFT
from qat.qpus import PyLinalg

# Local imports
from .classicalg import continued_fraction_expansion


def build_quantum_program(n: int, x: int) -> Job:
    """
    Creates the quantum circuit used to solve the period-finding problem.

    :param n: (int) the integer to be factoring
    :param x: (int) the random number used to solve the period-finding problem

    :return: (Job) the quantum job to send to the QPU
    """

    # Create the quantum program
    quantum_program = Program()

    # Create the two quantum registers
    nbqbits_reg1 = int(np.trunc(np.log2(n ** 2))) + 1
    nbqbits_reg2 = int(np.trunc(np.log2(n)) + 1)

    reg1 = quantum_program.qalloc(nbqbits_reg1)
    reg2 = quantum_program.qalloc(nbqbits_reg2)

    # Initialize the quantum registers
    for qbit in reg1:
        quantum_program.apply(H, qbit)

    quantum_program.apply(X, reg2[-1])

    # Apply modular exponentiation on both registers
    quantum_program.apply(modular_exp(nbqbits_reg1, nbqbits_reg2, x, n), reg1, reg2)

    # Apply QFT on reg1
    quantum_program.apply(QFT(nbqbits_reg1), reg1)

    # Build quantum circuit
    circuit = quantum_program.to_circ(link=[qat.lang.AQASM.qftarith])

    # Return the job specifying that reg1 has to measured at the end of the execution of the quantum program
    return circuit.to_job(qubits=reg1, nbshots=1)


def period_finder(n: int, x: int) -> int:
    """
    Solves the period finding problem.

    :param n: (int) the integer to be factoring
    :param x: (int) the random number used to solve the period finding problem

    :return: (int) the period of the function f: a -> x^a mod n
    """

    # Create the job using the above function
    job = build_quantum_program(n, x)

    # Initialize the quantum simulator
    qpu = PyLinalg()

    # The probability to find the right period with Shor's algorithm is greater than 1/2, so we execute the quantum
    # program until to find a consistent period
    while True:
        # If the period found by Shor's quantum algorithm is wrong then an exception is raised
        try:
            # Submit the job and retrieve the result
            print('Job submitted')
            measure = qpu.submit(job)

            # Extract the period from the measurement
            r = continued_fraction_expansion(n, measure.raw_data[0].state.int, int(np.trunc(np.log2(n ** 2))) + 1)
            print('State : ', measure.raw_data[0].state.int)
            print('Period : ', r)

            # Check the period is valid
            if x ** r % n == 1:
                print('Invalid period')
                return r

        # A ValueError exception has been caught which means the period is not extractable from the previous measurement
        except ValueError:
            continue

import Qubit
import numpy as np
import math 

#########################################################################################
############ Generic Classes and Functions ##############################################
#########################################################################################

# countermeasure for foreseeable floating point issues when doing tensor products.
def append_last_p(p):
    return np.append(p, [1.0 - sum(p)])

# Noise class that holds an array of possible transforms and probabilities of each. I is auto 
# generated and need not be included.
class Noise:

    def __init__(self, n, probabilities, transforms):
        """
        :n:             gate dimension
        :probabilities: k vector. k probabilities of each transform. sum(probabilities) < 1.0
        :transforms:    k x 2^n x 2^n ndarray. k transorms of dimension 2^n x 2^n

        No verifications / validations done atm
        """
        # Add I transform if one does not exist
        lastindex = len(transforms) - 1
        if lastindex < 0 or not np.allclose(transforms[lastindex], np.eye(transforms[lastindex].shape[0])):
            transforms = np.concatenate([transforms, [np.eye(2**n)]])

        self.t = transforms
        self.p = probabilities # not adding probability of I due to potential floating point issues
        self.k = len(self.p)
        self.n = n

    def __mul__(self, other):
        """
        :other: The other element...
        """
        if not isinstance(other, Noise):
            raise TypeError('Cannot multiply type Gate with ' + type(other).__name__)

        t = np.kron(self.t, other.t)
        p = np.kron(append_last_p(self.p), append_last_p(other.p))[:-1] # remove I probability because...
        n = self.n + other.n
        return Noise(n, p, t)


    # Randomly chooses a noise transformation to be applied. Watch out for those nasty floating point errors!
    def eval(self):
        """
        :return: transform matrix 2^n x 2^n
        """
        row_i = np.random.choice(len(self.t), p=append_last_p(self.p))
        return self.t[row_i]

# Generic Gate class. by default it is Identity with default noise model
class Gate:
    def __init__(self, n, transform = None, noise = None):
        """
        :n:          gate dimension
        :transform:  2^n x 2^n unitary matrix
        :noise:      noise channel to apply after gate

        No verifications / validations done on transform(unitary) matrix atm
        """
        if noise is None:
            noise = NoNoise(n)

        if transform is None:
            transform = np.eye(2**n)

        self.u = transform
        self.noise = noise
        self.n = n

    # Tensor product of two gates.
    def __mul__(self, other):
        """
        :other: Its the other element...
        """
        if not isinstance(other, Gate):
            raise TypeError('Cannot multiply type Gate with ' + type(other).__name__)

        u = np.kron(self.u, other.u)
        t = self.noise * other.noise 
        n = self.n + other.n
        return Gate(n, u, t) # had to do it

    # Apply the gate to a given register.
    def apply(self, register):
        """
        :register: Register object to apply gate

        :return: Register returned. Or maybe vector. Same thing....
        """
        if self.noise:
            vec = self.noise.eval() @ self.u @ register.as_vec()
        else:
            vec = self.u @ register.as_vec()
        return Qubit.Register(n=len(vec), amplitudes=vec)

#########################################################################################
############ Functional Noise Models ####################################################
#########################################################################################

# No Noise class. Essentially an I matrix with probability 1
class NoNoise(Noise):
    def __init__(self, n):
        super().__init__(n, np.empty(0), np.empty((0, 2**n, 2**n)))

# Bit flip noise on n bits (apply X)
class XNoise(Noise):
    def __init__(self, n, p):
        if p < 0.0 or p > 1.0:
            raise ValueError("probability out of range [0.0, 1.0]")

        pi = [p, 1.0 - p]
        ti = [Qubit.X, np.eye(2)]
        p = pi
        t = ti

        for _ in range(n-1):
            pi = np.kron(p, pi)
            ti = np.kron(t, ti)

        super().__init__(n, pi[:-1], ti)

# Y noise on n bits (apply Y)
class YNoise(Noise):
    def __init__(self, n, p):
        if p < 0.0 or p > 1.0:
            raise ValueError("probability out of range [0.0, 1.0]")
        
        pi = [p, 1.0 - p]
        ti = [Qubit.Y, np.eye(2)]
        p = pi
        t = ti

        for _ in range(n-1):
            pi = np.kron(p, pi)
            ti = np.kron(t, ti)

        super().__init__(n, pi[:-1], ti)

# dephasing noise on n bits (apply Z)
class ZNoise(Noise):
    def __init__(self, n, p):
        if p < 0.0 or p > 1.0:
            raise ValueError("probability out of range [0.0, 1.0]")
        
        pi = [p, 1.0 - p]
        ti = [Qubit.Z, np.eye(2)]
        p = pi
        t = ti

        for _ in range(n-1):
            pi = np.kron(p, pi)
            ti = np.kron(t, ti)

        super().__init__(n, pi[:-1], ti)


# Depolarization / Pauli noise independently on n bits.
class PauliNoise(Noise):
    def __init__(self, n, px, py, pz):
        if px < 0.0 or py < 0.0 or pz < 0.0 or px + py + pz > 1.0:
            raise ValueError("probability out of range [0.0, 1.0]")

        pi = []
        ti = []

        if px:
            pi += [px]
            ti += [Qubit.X]
        if py:
            pi += [py]
            ti += [Qubit.Y]
        if pz:
            pi += [pz]
            ti += [Qubit.Z]

        pi += [1.0 - sum(pi)]
        ti += [np.eye(2)]
        p = pi
        t=ti

        for _ in range(n-1):
            pi = np.kron(p, pi)
            ti = np.kron(t, ti)

        super().__init__(n, pi[:-1], ti)

# Amplitude Damping error
class DampingNoise(Noise):
    def __init__(self, n, p):
        if p < 0.0 or p > 1.0:
            raise ValueError("probability out of range [0.0, 1.0]")

        pi = [p, 1.0 - p]
        K_0 = np.sqrt([[1, np.sqrt(p)], [0, np.sqrt(1-p)]])
        ti = [K_0, np.eye(2)]
        p = pi
        t = ti

        for _ in range(n-1):
            pi = np.kron(p, pi)
            ti = np.kron(t, ti)

        super().__init__(n, pi[:-1], ti)
#########################################################################################
############ Functional Gates ###########################################################
#########################################################################################

# Hadamard on one qubit
class Hadamard(Gate):
    def __init__(self, noise = None):
        super().__init__(1, Qubit.H, noise)

# Walsh on n qubits
class Walsh(Gate):
    def __init__(self, n, noise = None):

        t = Qubit.H
        for _ in range(n-1):
            t = np.kron(Qubit.H, t)

        super().__init__(n, t, noise)

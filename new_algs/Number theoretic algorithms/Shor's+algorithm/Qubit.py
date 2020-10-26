import numpy as np
import warnings
import random
import Gate

warnings.filterwarnings('ignore')

# Hadamard Gate
H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]])

# X, Y, Z Pauli Matrices
X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.array([[1, 0], [0, -1]])


# Constructs a qubit using numpy array architecture.
def _make_qubit(alpha, beta):
    """
    :param alpha: amplitude corresponding to |0>
    :param beta: amplitude corresponding to |1>
    :return qubit: numpy array with entries alpha and beta
    """
    Q = np.zeros(2)
    Q[0] = alpha
    Q[1] = beta
    return Q.view(Qubit)


# Constructs a quantum register using a numpy array of QUBIT objects
def _make_register(amplitudes):
    """
    :param amplitudes:  numpy array of tuples corresponding to the amplitudes of each qubit in the register
    :return register: numpy array of qubits
    """
    size = len(amplitudes)
    q = np.array(amplitudes[0]).view(Qubit)
    for i in range(size - 1):
        q = np.kron(q, np.array(amplitudes[i + 1]).view(Qubit))
    return Register(amplitudes=q)


def binaryToDecimal(binary):
    decimal, i, n = 0, 0, 0
    while binary != 0:
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary // 10
        i += 1
    return decimal


def dec_to_bin(x):
    return int(bin(x)[2:])


bell_state_names = ['phi_plus', 'phi_minus', 'psi_plus', 'psi_minus']


################################################################################
################################################################################


# Qubit() with no arguments gives the |0> state by default
# We assume use of the computational basis by default
class Qubit(np.ndarray):

    def __new__(cls, name=None, vec=(1, 0), noise=0):
        """
        :param vec: a tuple of ALPHA and BETA, the amplitudes of states |0> and |1>, respectively
        :param shape: ensures the qubit is a 2D vector (i.e. sets the size of the numpy array to 2x1)
        :return: a quantum state with amplitudes ALPHA and BETA
        """
        valid_names = ['+', '-', 'plus', 'minus']
        if name == 'plus' or name == '+': return _make_qubit(1 / np.sqrt(2), 1 / np.sqrt(2))
        if name == 'minus' or name == '-': return _make_qubit(1 / np.sqrt(2), -1 / np.sqrt(2))
        alpha = vec[0]
        beta = vec[1]
        return _make_qubit(alpha, beta)

    def __init__(self, name=None, vec=(1, 0), noise=0):
        if name == 'plus' or name == '+':
            vec = (1 / np.sqrt(2), 1 / np.sqrt(2))
        if name == 'minus' or name == '-':
            vec = (1 / np.sqrt(2), -1 / np.sqrt(2))
        self.alpha = vec[0]
        self.beta = vec[1]
        self.n = 1
        if noise == 1:
            self.noise = Gate.XNoise
        elif noise == 2:
            self.noise = Gate.YNoise
        elif noise == 3:
            self.noise = Gate.ZNoise
        elif noise == 4:
            self.noise = Gate.PauliNoise
        elif noise == 5:
            self.noise = Gate.DampingNoise
        else:
            self.noise = None

    def __mul__(self, matrix):
        x = np.matmul(self, matrix)[0]
        a = x[0]
        b = x[1]
        return Qubit(vec=(a, b))

    def __repr__(self):
        nonzero = [self.alpha, self.beta]
        ret = ""
        for i in range(2):
            if nonzero[i] == 0:
                continue
            ret += '(' + str(nonzero[i]) + ')' + '|' + str(i) + '>'
            if nonzero[1] != 0 and i != 1:
                ret += ' + '
        return ret

    ### NOISELESS SINGLE-QUBIT METHODS ###
    def pauli(self, op):
        if op == 'X':
            p = np.matmul(self, X)
        elif op == 'Y':
            p = np.matmul(self, Y)
        elif op == 'Z':
            p = np.matmul(self, Z)
        else:
            raise ValueError('Argument must be either X, Y, or Z as string')
        return Qubit(vec=(p[0], p[1]))

    def Hadamard(self, noise_prob=0):
        if self.noise is None:
            p = np.matmul(self, H)
        else:
            p = np.matmul(self.Gate.Hadamard(self.noise(self.n, noise_prob)))
        return Qubit(vec=(p[0], p[1]))

    def measure(self):
        x = np.random.random()
        if self.alpha ** 2 <= x:
            return 0
        return 1


class Register(np.ndarray):

    def __new__(cls, n=2, name=None, qubits=None, amplitudes=None, ket=True, noise=0):
        """
        :param n: 2 by default. Returns an n-qubit register initialized to |000...0>
        :param name: Passing in the name of a bell state gives that bell state. More names to come.
        :param qubits: Returns the register formed by taking the tensor product of all of the QUBIT
                       objects passed through in the order they were given
        :param amplitudes: Returns a register with the amplitudes given. Length of AMPLITUDES must be
                           a power of two (raises ASSERTION ERROR) and its l2 norm must be equal to 1 (raises
                           ASSERTION ERROR)
        :param ket: True/False. Whether the Register in question should be a ket or a bra
        :param noise: See module GATE.PY for details.
                        1: XNoise
                        2: YNoise
                        3: ZNoise
                        4: PauliNoise
                        5: DampingNoise
        :return: a new Register object
        """
        if name in bell_state_names:
            return Register._make_bell_state(name)
        if qubits is not None:
            return _make_register(qubits)
        if amplitudes is not None:
            L = np.array(amplitudes)
            x = np.log2(L.size)
            assert x // 1 == x, 'The size of the register should be a power of 2.'
            return np.asarray(amplitudes).view(Register)
        if name is None:
            return _make_register([(1, 0)] * n)

    def __init__(self, n=2, name=None, qubits=None, amplitudes=None, ket=True, noise=0):
        self.name = name
        self.n = n
        self.amplitudes = amplitudes
        self.qubits = qubits
        self.ket = ket
        if name in bell_state_names:
            self.name = name
            self.n = 2
        if amplitudes is not None:
            L = np.array(amplitudes)
            self.n = int(np.log2(L.size))
        if qubits is not None:
            self.n = len(qubits)

        if not self.ket:
            self.bra()
        self.amplitudes = np.asarray([i for i in self])

        if noise == 1:
            self.noise = Gate.XNoise
        elif noise == 2:
            self.noise = Gate.YNoise
        elif noise == 3:
            self.noise = Gate.ZNoise
        elif noise == 4:
            self.noise = Gate.PauliNoise
        elif noise == 5:
            self.noise = Gate.DampingNoise
        else:
            self.noise = None

    # Define multiplication of states
    # <x|y> is valid, |x><y| is valid, but multiplication of kets/bras is not, and scaling kets/bras is not
    # because the norm of the state must be equal to 1.
    def __mul__(self, other):
        if other.ket and self.ket:
            raise TypeError('Multiplication of two kets is not defined')
        if not other.ket and not self.ket:
            raise TypeError('Multiplication of two bras is not defined')
        s = self.reshape((1, (2 ** self.n)))
        o = other.reshape((1, (2 ** other.n)))
        if self.ket:
            prod = s.T @ o
        else:
            prod = s @ o.T
        if prod.size == 1:
            p = prod.view(np.ndarray)
            return p[0][0]
        else:
            return prod.view(np.ndarray)

    # Use to view the vector form of the register rather than the Bra-ket form
    def as_vec(self):
        return np.asarray(self)

    # Conjugate transpose. |x> --> <x|
    def bra(self):
        for i in range(len(self)):
            self.amplitudes[i] = np.conj(self[i])
        self.ket = False
        return self

    # Changes the representation of the Register to KET sum formalism
    # (e.g. (a_1)|000...> + (a_2)|00...01> + ... + (a_2^n)|111...1> )
    def __repr__(self):
        N = int(np.log2(self.size))
        nonzero_indices = []
        for i in range(self.size):
            if self[i] != 0:
                nonzero_indices.append(i)
        bins = [dec_to_bin(i) for i in nonzero_indices]
        ret = ""
        if self.ket:
            for i in range(len(bins)):
                ret += ('(' + str(self[nonzero_indices[i]]) + ')' + '|' + str(bins[i]).zfill(N) + '>')
                if i != len(bins) - 1:
                    ret += ' + '
        else:
            for i in range(len(bins)):
                ret += ('(' + str(self[nonzero_indices[i]]) + ')' + '<' + str(bins[i]).zfill(N) + '|')
                if i != len(bins) - 1:
                    ret += ' + '
        return ret

    # measure function for shor's; returns int
    def measure(self):
        probs = [abs(x) ** 2 for x in self.amplitudes]
        sample = np.random.random()
        cumul_prob = 0
        for i in range(2 ** self.n):
            cumul_prob += probs[i]
            if sample < cumul_prob and probs[i] != 0:
                return i

    # controls on the first (leftmost) qubit and targets the second (second from left) qubit by default
    def CNOT(self, control=0, target=1):
        N = int(np.log2(self.size))
        v = self.as_vec()
        skip = []
        for i in range(2 ** N):
            if i in skip:
                continue
            bitstring = str(dec_to_bin(i)).zfill(N)
            x = i
            if bitstring[control] == '1':
                if bitstring[target] == '0':
                    x ^= 1 << N - target - 1
                else:
                    x ^= 0 << N - target - 1
                index = binaryToDecimal(x)
                temp = v[i]
                v[i] = v[index]
                v[index] = temp
        return Register(amplitudes=v)

    @classmethod
    def _make_bell_state(cls, name):
        if name == 'phi_plus':
            x = _make_register([(1, 0), (1, 0)])
        elif name == 'phi_minus':
            x = _make_register([(0, 1), (1, 0)])
        elif name == 'psi_plus':
            x = _make_register([(1, 0), (0, 1)])
        elif name == 'psi_minus':
            x = _make_register([(0, 1), (0, 1)])
        else:
            raise NameError('Name {} '.format(name) + 'is not recognized.')
        H_I = np.kron(H, np.identity(2))
        x = np.matmul(H_I, x)
        register = Register(amplitudes=x.CNOT())
        return register

    # Returns |000...0> of length n
    @classmethod
    def zeros(cls, n):
        return _make_register([(1, 0)] * n)

    # Returns |111...1> of length n
    @classmethod
    def ones(cls, n):
        return _make_register([(0, 1)] * n)

    # Converts a numpy array or a python list to a REGISTER object
    @classmethod
    def as_register(cls, x):
        if type(x) is not np.ndarray and type(x) is not list:
            raise TypeError('Cannot convert {}'.format(type(x)) + 'to Register.'
                                                                  ' Data type must be Python list or numpy ndarray.')
        x = np.asarray(x)
        if np.linalg.norm(x) - 1 >= 1e-9:
            raise ValueError('Cannot convert to Register. Squared amplitudes must sum to 1.')
        return Register(amplitudes=x)

    # Performs Walsh-Hadamard on the register
    def walsh(self, noise_prob=0):
        if self.noise is None:
            vec = self.reshape(2 ** self.n)
            w = H
            for i in range(self.n - 1):
                w = np.kron(w, H)
            return Register(amplitudes=np.around(np.matmul(w, vec), 9), ket=self.ket)
        else:
            w = Gate.Walsh(self.n, self.noise(self.n, noise_prob))
            return w.apply(self)

    # Quantum Fourier Transform operation
    def QFT(self):
        const = 1 / np.sqrt((2 ** self.n))
        amps = []
        for k in range(2 ** self.n):
            total = 0
            for p in range(2 ** self.n):
                total += self[p] * np.exp((2 * np.pi * 1j * p * k) / (2 ** self.n))
            amps.append(total)
        amps = np.asarray(amps)
        amps *= const
        return Register(amplitudes=amps, ket=self.ket, noise=self.noise)

    @property
    def purity(self):
        return np.real(np.trace(self.density @ self.density))

    @property
    def density(self):
        N = 2 ** self.n
        rho = np.zeros((N, N), dtype=complex)
        for i in range(N):
            x = [0] * N
            x[i] = self.amplitudes[i]
            ket = Register(amplitudes=x)
            bra = Register(amplitudes=x)
            bra.bra()
            rho += (ket * bra)
        return rho

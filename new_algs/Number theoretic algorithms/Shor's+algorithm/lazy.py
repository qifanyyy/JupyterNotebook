import numpy as np
from scipy import stats
import lazyarray
from lazyarray import larray
from utilities import *

"""
Optimised implementation of Gates using lazy matrices.
As seen at https://lazyarray.readthedocs.io/en/latest/
"""

class LMatrix:
    """Abstract parent class for all lazily defined quantum objects
    """
    def __init__(self, typ):
        """Set the type of object: Gate or Qubit
        """
        self.type = str(typ)
        
    def __mul__(self,other):
        """Method to perform matrix multiplication. Combines gates sequentially
        and acts gates on registers. Multiplied objects must have the same size

        """
        
        #multiplication order:
        #    Gate*Qubit
        #    Gate*Scalar
        #    Qubit*Scalar
        
        if (type(other)==int):
            if (self.type=="Gate"):
                return Gate(self.array*other)
            else:
                return Qubit(self.array*other)

        elif (self.type=="Gate") and (other.type=="Gate"):
            assert self.array.shape==other.array.shape, "Gates must be of same size"
            return Gate(lazy_mul_gate(self.array,other.array))

        elif (self.type=="Qubit") and (other.type=="Qubit"):
            assert self.array.shape==other.array.shape, "Qubit registers must have same size"
            return Gate(lazy_mul(self.array,other.array))

        else:
            assert (self.type=="Gate") and (other.type=="Qubit"), "Gate must act on Qubit register"
            #assert self.array.shape[0]==other.array.shape[0], "Qubit register and gate must be of same size"
            return Qubit(lazy_mul(self.array,other.array))
        
    def get(self,n):
        return str(self.array[n])


    def __str__(self):
        """Returns string of contents of quantum object. Not 'realistic', as
        quantum states cannot be fully observed without collapsing qubit register
        to 1 state. For that, use Qubit.measure()
        """
        return str(self.array.evaluate())


    def __len__(self):
        """Returns the size of gate or qubit register, in number of qubits
        """
        return int(np.log2(self.array.shape[1]))


    def __and__(self,other):
        """Method to perform tensor products of quantum objects. Combines
        gates in parallel. Combines qubits into qubit registers, or qubit registers
        into bigger qubit registers. Cannot combine qubit (registers) with gates
        """
        assert self.type==other.type, "Cannot tensor a Gate with a Qubit register"
        if (self.type=="Gate") and (other.type=="Gate"):
            
            return Gate(tensor_lazy(self.array,other.array))
        elif (self.type=="Qubit") and (other.type=="Qubit"):
            return Qubit(tensor_lazy(self.array,other.array))

    def ret(self):
        """Returns array of contents of quantum object. Not 'realistic', as
        quantum states cannot be fully observed without collapsing qubit register
        to 1 state. For that, use Qubit.measure()
        """
        return self.array.evaluate()

#####################################################################################
# Single Qubit Gates

class Hadamard(LMatrix):
    """Hadamard gate. Takes 0 or 1 state qubit and sets it to equal probability
    superposition.
    """
    def __init__(self,n=1):
        """Initialisation method. n defines number of qubits to act on. Alternatively single qubit
        Hadamards can be tensored together
        """
        LMatrix.__init__(self,"Gate")
        h = larray([[1,1],[1,-1]])
        hn = h
        for i in range(n-1):
            hn = tensor_lazy(h,hn)
        hn = hn*(2**(-0.5*n))
        self.array = larray(hn)

class V(LMatrix):
    """V gate. Special case of the Phase gate, with phase=pi/2
    """
    def __init__(self):
        LMatrix.__init__(self,"Gate")
        self.array = larray([[1,0],[0,1j]])

class Phase(LMatrix):
    """Phase gate. Applies complex phase shift to qubit. 
    """
    def __init__(self,phase,n=1):
        """Initialisation method. Phase input defines 
        size of phase shift, n defines number of qubits to act on.
        """
        LMatrix.__init__(self,"Gate")
        self.phase = phase
        ph = larray([[1,0],[0,np.exp(1j*phase)]])
        phn = ph
        for i in range(n-1):
            ph = tensor_lazy(ph,phn)
        self.array = larray(ph)

class Identity(LMatrix):
    """Identity gate. Leaves qubit register unchanged. Use to represent 'empty' wires
    in quantum circuit diagrams. Typically used by tensoring to other gates
    """
    def __init__(self,n=1):
        """Initialisation method. n defines number of qubits to act on. Alternatively single qubit
        Identity gates can be tensored together
        """
        LMatrix.__init__(self,"Gate")
        self.array = larray(np.identity(2**n))


class PauliX(LMatrix):
    """Pauli X gate. Rotates qubit register pi radians about the X axis of the bloch sphere
    Classicaly analogous to NOT gate.
    """
    def __init__(self,n=1):
        
        LMatrix.__init__(self,"Gate")
        self.array = larray(np.flipud(np.identity(2**n)))
        
class PauliY(LMatrix):
    """Pauli Y gate. Rotates qubit register pi radians about the Y axis of the bloch sphere
    """
    def __init__(self):
        """Initialisation method
        """
        LMatrix.__init__(self,"Gate")
        self.array = larray([[0,-1j],
                             [1j,0]])
        
class PauliZ(LMatrix):
    """Pauli Z gate. Rotates qubit register pi radians about the Z axis of the bloch sphere.
    Special case of Phase shift gate, with phase=pi
    """
    def __init__(self):
        LMatrix.__init__(self,"Gate")
        self.array = larray([[1,0],
                             [0,-1]])
##############################################################################################
#Control Gates

class Controlled(LMatrix):
    """Generalised controlled gate. Generates controlled versions of any 1 qubit gate,
    where other_gate is another quantum object with type="Gate". 
    """
    def __init__(self,other_gate,n=2):
        """Initialisation method. n defines the number of
        total qubits for the gate (n-1 control qubits + 1 target qubit)
        """
        LMatrix.__init__(self,"Gate")
        self.array = (np.identity(2**n))
        t = other_gate.array.evaluate()
        self.array[2**n-2,2**n-2] = t[0,0]
        self.array[2**n-1,2**n-1] = t[1,1]
        self.array[2**n-1,2**n-2] = t[1,0]
        self.array[2**n-2,2**n-1] = t[0,1]
        self.array = larray(self.array)

class CNot(LMatrix):
    """Generalised controlled gate. Generates controlled versions of any 1 qubit gate,
    where other_gate is another quantum object with type="Gate". 
    """
    def __init__(self,n=2):
        """Initialisation method. n defines the number of
        total qubits for the gate (n-1 control qubits + 1 target qubit)
        """
        LMatrix.__init__(self,"Gate")
        self.array = np.identity(2**n)
        self.array[2**n-2,2**n-2] = 0
        self.array[2**n-1,2**n-1] = 0
        self.array[2**n-1,2**n-2] = 1
        self.array[2**n-2,2**n-1] = 1
        self.array = larray(self.array)


class CPhase(LMatrix):
    """Controlled phase shift gate. Equivalent to Controlled(Phase()).
    Used a lot for the Quantum Fourier Transform in Shors algorithm
    """
    def __init__(self,phase,n=2):
        """Initialisation method. phase defines phase shift on phase gate, 
        defines the number of total qubits for the gate (n-1 control qubits 
        + 1 target qubit)
        """
        LMatrix.__init__(self,"Gate")
        self.array = np.identity(2**n,dtype=complex)
        self.array[2**n-1,2**n-1]=np.exp(1j*phase)
        self.array = larray(self.array)

class Swap(LMatrix):
    """Swaps the contents of any 2 qubits. Works on entangled qubit registers
    without collapsing them. Mainly useful for shifting qubits around to perform
    controlled gates
    """
    def __init__(self,n=2,index1=0,index2=1):
        """Initialisation method. n defines the total number of qubits being acted on,
        index1 and index2 define the 2 qubits to be swapped
        """
        LMatrix.__init__(self,"Gate")
        self.array = larray(perm_matrix(n,index1,index2))


class Toffoli(LMatrix):
    """Controlled CNot gate. Equivalent to Controlled(PauliX(),3)
    """
    def __init__(self):
        LMatrix.__init__(self,"Gate")
        self.array = larray([[1,0,0,0,0,0,0,0],
                                    [0,1,0,0,0,0,0,0],
                                    [0,0,1,0,0,0,0,0],
                                    [0,0,0,1,0,0,0,0],
                                    [0,0,0,0,1,0,0,0],
                                    [0,0,0,0,0,1,0,0],
                                    [0,0,0,0,0,0,0,1],
                                    [0,0,0,0,0,0,1,0]])

########################################################################
#Possible LMatrix types:

class Gate(LMatrix):
    """Generic gate class. Use for defining your own gates. Used by functions that return gates,
    such as multiplication or tensor products.
    """
    def __init__(self,data):
        """Initialise generic gate. data is a matrix. Although no checks are performed,
        matrices must be: Unitary, Hermitian, and size 2^n * 2^n.
        If an input matrix does not satisfy these constraints, unpredictable and wrong 
        things may happen.
        """
        LMatrix.__init__(self,"Gate")
        self.array = larray(data)

class Qubit(LMatrix):
    """Generic Qubit class. Used to define qubits. Used as outputs to function such as gate*qubit
    multiplication.
    """
    def __init__(self,data,fock=0):
        """Initialise a qubit or qubit register. If data is an array, set qubit register to that.
        if data is an int, use it as size of qubit register and intialise with optional fock space input
        """
        LMatrix.__init__(self,"Qubit")
        if type(data) is int:
            self.array = np.zeros((2**data,1))
            self.array[fock] = 1
            #self.array = [self.array]
            self.array = larray(self.array)
        else:
            #self.array = [self.array]
            self.array = data


    def normalise(self):
        """Renormalise qubit register such that probabilities sum to 1
        """
        div = np.sqrt(np.sum(np.square(self.array)))
        a = np.empty(len(self.array))
        a.fill(div)
        self.array = larray(np.divide(self.array,a))

    def measure(self):
        """Measure qubit register. Collapses to 1 definite state. Simulates real measurement, as 
        intermediate values of qubit registers during computation remain unknown.
        """
        data = self.array.evaluate()
        pos = np.arange(len(data))
        probs = np.abs(np.square(data))
        #If probs is not normalised (usually due to rounding errors), re-normalise
        probs = probs/np.sum(probs)
        dist = stats.rv_discrete(values=(pos,probs))
        self.array = np.zeros(data.shape)
        self.array[dist.rvs()] = 1
        self.array = larray(self.array)
        

    def split_register(self):
        """Splits entangle qubit register into individual qubit states. Only works after measurement
        has been acted on a qubit register. Returns a binary string representing the states of each qubit
        """
        outs = np.arange(0,len(self.array),1)
        res = np.array(np.sum(outs*self.array.astype(int)))
        return np.binary_repr(res)




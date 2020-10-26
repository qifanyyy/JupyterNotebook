import numpy as np
from scipy import stats
from scipy import sparse as sp
import math
import cmath
from utilities import *


"""
Optimised implementation of Gates using scipy.sparse matrices.
Works because most (but not all) of the matrices representing
quantum gates are very sparse. User interfacing with this is 
identical to un-optimised implementation.
"""



class SMatrix:
    """Abstract parent class for all sparsely defined quantum objects
    """

    def __init__(self, typ):
        """Set the type of object: Gate or Qubit
        """
        self.type = str(typ)

    def __mul__(self,other):
        """Method to perform matrix multiplication. Combines gates sequentially
        and acts gates on registers. Multiplied objects must have the same size

        """
        
        if (type(other)==int):
            if (self.type=="Gate"):
                return Gate(self.array*other)
            else:
                return Qubit(self.array*other)

        elif (self.type=="Gate") and (other.type=="Gate"):
            assert self.array.shape==other.array.shape, "Gates must be of same size"
            return Gate(self.array*other.array)

        elif (self.type=="Qubit") and (other.type=="Qubit"):
            assert self.array.shape==other.array.shape, "Qubit registers must have same size"
            return Gate(sp.outer(self.array,other.array))

        else:
            assert (self.type=="Gate") and (other.type=="Qubit"), "Gate must act on Qubit register"
            #assert self.array.shape[0]==other.array.shape[0], "Qubit register and gate must be of same size"
            return Qubit(other.array*self.array)



    def __str__(self):
        """Returns string of contents of quantum object. Not 'realistic', as
        quantum states cannot be fully observed without collapsing qubit register
        to 1 state. For that, use Qubit.measure()
        """
        return str(self.array.toarray())


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
            return Gate(tensor_sparse_gate(self.array,other.array))     
        elif (self.type=="Qubit") and (other.type=="Qubit"):
            return Qubit(tensor_sparse_qubit(self.array,other.array))
            
    def ret(self):
        """Returns array of contents of quantum object. Not 'realistic', as
        quantum states cannot be fully observed without collapsing qubit register
        to 1 state. For that, use Qubit.measure()
        """
        return self.array.toarray()

    def ret_mod(self):
        """Returns array of probabilities of quantum states. Not 'realistic', as
        quantum states cannot be fully observed without collapsing qubit register
        to 1 state. For that, use Qubit.measure()
        """
        return np.abs(np.square(self.array.toarray()))[0]


#####################################################################################
# Single Qubit Gates




class Hadamard(SMatrix):
    """Hadamard gate. Takes 0 or 1 state qubit and sets it to equal probability
    superposition.
    """
    def __init__(self,n=1):
        """Initialisation method. n defines number of qubits to act on. Alternatively single qubit
        Hadamards can be tensored together
        """
        SMatrix.__init__(self,"Gate")
        h = sp.bsr_matrix([[1,1],[1,-1]])
        hn = h
        for i in range(n-1):
            hn = tensor_sparse_gate(h,hn)
        hn = hn*(2**(-0.5*n))
        self.array = sp.bsr_matrix(hn)


class V(SMatrix):
    """V gate. Special case of the Phase gate, with phase=pi/2
    """
    def __init__(self):
        """Initialisation method
        """
        SMatrix.__init__(self,"Gate")
        self.array = sp.bsr_matrix([[1,0],[0,1j]])

class Phase(SMatrix):
    """Phase gate. Applies complex phase shift to qubit. 
    """
    def __init__(self,phase,n=1):
        """Initialisation method. Phase input defines 
        size of phase shift, n defines number of qubits to act on.
        """
        SMatrix.__init__(self,"Gate")
        ph = sp.bsr_matrix([[1,0],[0,np.exp(1j*phase)]])
        phn = ph
        for i in range(n-1):
            ph = tensor_sparse_gate(ph,phn)
        self.array = sp.bsr_matrix(ph)

class Identity(SMatrix):
    """Identity gate. Leaves qubit register unchanged. Use to represent 'empty' wires
    in quantum circuit diagrams. Typically used by tensoring to other gates
    """
    def __init__(self,n=1):
        """Initialisation method. n defines number of qubits to act on. Alternatively single qubit
        Identity gates can be tensored together
        """
        SMatrix.__init__(self,"Gate")
        self.array = sp.identity(2**n)

class PauliZ(SMatrix):
    """Pauli Z gate. Rotates qubit register pi radians about the Z axis of the bloch sphere.
    Special case of Phase shift gate, with phase=pi
    """
    def __init__(self):
        """Initialisation method
        """
        SMatrix.__init__(self,"Gate")
        self.array = sp.bsr_matrix([[1,0],
                                    [0,-1]])

class PauliY(SMatrix):
    """Pauli Y gate. Rotates qubit register pi radians about the Y axis of the bloch sphere
    """
    def __init__(self):
        """Initialisation method
        """
        SMatrix.__init__(self,"Gate")
        self.array = sp.bsr_matrix([[0,-1j],
                                    [1j,0]])


class PauliX(SMatrix):
    """Pauli X gate. Rotates qubit register pi radians about the X axis of the bloch sphere
    Classicaly analogous to NOT gate.
    """
    def __init__(self,n=1):
        """Initialisation method
        """
        SMatrix.__init__(self,"Gate")
        self.array = sp.bsr_matrix(np.flipud(np.identity(2**n)))



##############################################################################################
#Control Gates

class Controlled(SMatrix):
    """Generalised controlled gate. Generates controlled versions of any 1 qubit gate,
    where other_gate is another quantum object with type="Gate". 
    """
    def __init__(self,other_gate,n=2):
        """Initialisation method. n defines the number of
        total qubits for the gate (n-1 control qubits + 1 target qubit)
        """
        SMatrix.__init__(self,"Gate")
        assert other_gate.type=="Gate","Controlled must have Gate type input"
        self.array = sp.lil_matrix(sp.identity(2**n,dtype="complex"))
        t = other_gate.array.toarray()
        self.array[2**n-2,2**n-2] = t[0,0]
        self.array[2**n-1,2**n-1] = t[1,1]
        self.array[2**n-1,2**n-2] = t[1,0]
        self.array[2**n-2,2**n-1] = t[0,1]
        self.array = sp.bsr_matrix(self.array)




class CNot(SMatrix):
    """Controlled not gate. Equivalent to Controlled(PauliX()).
    """
    def __init__(self,n=2):
        """Initialisation method. n defines the number of
        total qubits for the gate (n-1 control qubits + 1 target qubit)
        """
        SMatrix.__init__(self,"Gate")
        self.array = sp.csr_matrix(sp.identity(2**n))
        self.array[2**n-2,2**n-2] = 0
        self.array[2**n-1,2**n-1] = 0
        self.array[2**n-1,2**n-2] = 1
        self.array[2**n-2,2**n-1] = 1
        self.array = sp.bsr_matrix(self.array)


class Toffoli(SMatrix):
    """Controlled CNot gate. Equivalent to Controlled(PauliX(),3)
    """
    def __init__(self):
        """Initialisation methods
        """
        SMatrix.__init__(self,"Gate")
        self.array = sp.bsr_matrix([[1,0,0,0,0,0,0,0],
                                    [0,1,0,0,0,0,0,0],
                                    [0,0,1,0,0,0,0,0],
                                    [0,0,0,1,0,0,0,0],
                                    [0,0,0,0,1,0,0,0],
                                    [0,0,0,0,0,1,0,0],
                                    [0,0,0,0,0,0,0,1],
                                    [0,0,0,0,0,0,1,0]])


class CPhase(SMatrix):
    """Controlled phase shift gate. Equivalent to Controlled(Phase()).
    Used a lot for the Quantum Fourier Transform in Shors algorithm
    """
    def __init__(self,phase,n=2):
        """Initialisation method. phase defines phase shift on phase gate, 
        defines the number of total qubits for the gate (n-1 control qubits 
        + 1 target qubit)
        """
        SMatrix.__init__(self,"Gate")
        self.array = sp.csr_matrix(sp.identity(2**n),dtype=complex)
        self.array[2**n-1,2**n-1]=np.exp(1j*phase)
        self.array = sp.bsr_matrix(self.array,dtype=complex)

################################################################################
#Other useful gates

class Swap(SMatrix):
    """Swaps the contents of any 2 qubits. Works on entangled qubit registers
    without collapsing them. Mainly useful for shifting qubits around to perform
    controlled gates
    """
    def __init__(self,n=2,index1=0,index2=1):
        """Initialisation method. n defines the total number of qubits being acted on,
        index1 and index2 define the 2 qubits to be swapped
        """
        SMatrix.__init__(self,"Gate")
        self.array = sp.bsr_matrix(perm_matrix(n,index1,index2))

        

class Diffusion(SMatrix):
    """Hard coded diffusion gates for Grovers
    """
    def __init__(self,n):
        SMatrix.__init__(self,"Gate")
        N = 2**n
        c = 2.0/N
        self.array = sp.bsr_matrix(np.full((N, N), c) - np.identity(N))




class Oracle(SMatrix):
    """Hard coded Oracle gate for Grovers
    """
    def __init__(self,reg_size,target):
        SMatrix.__init__(self,"Gate")
        diags = np.ones(2**reg_size)
        #offsets = np.arange(0,2**reg_size,1)
        diags[target] = -1
        self.array = sp.csr_matrix(sp.identity(2**reg_size))
        self.array[target,target] = -1
        self.array = sp.bsr_matrix(self.array)
        #self.array = sp.dia_matrix(diags)


class Noisy(SMatrix):
    """Returns a copy of a Gate, with random noise added. An attempt to more accurately
    simulate real quantum computers, as noise issues are a big deal. However this doesn't
    accurately model how the noise on a real quantum computer emerges, this is just a rough
    attempt. With high amounts of noise, this can break the hermitian and unitary properties
    of gates, and can lead to unpredictable results
    """
    def __init__(self,other_gate,a=0.5):
        """Initialisation method. other_gate is any other quantum gate. a is a float
        between 0 and 1. 0 -> no noise, 1 -> all noise
        """
        SMatrix.__init__(self,"Gate")
        self.array = other_gate.array
        noise = sp.random(self.array.shape[0],self.array.shape[0],density=a)
        noise = noise + 1j*sp.random(self.array.shape[0],self.array.shape[0],density=a)
        self.array = (1-a)*self.array +a*noise






class Gate(SMatrix):
    """Generic gate class. Use for defining your own gates. Used by functions that return gates,
    such as multiplication or tensor products.
    """
    def __init__(self,data):
        """Initialise generic gate. data is a matrix. Although no checks are performed,
        matrices must be: Unitary, Hermitian, and size 2^n * 2^n.
        If an input matrix does not satisfy these constraints, unpredictable and wrong 
        things may happen.
        """
        SMatrix.__init__(self,"Gate")
        self.array = sp.bsr_matrix(data)


class Qubit(SMatrix):
    """Generic Qubit class. Used to define qubits. Used as outputs to function such as gate*qubit
    multiplication.
    """
    def __init__(self,data,fock=0):
        """Initialise a qubit or qubit register. If data is an array, set qubit register to that.
        if data is an int, use it as size of qubit register and intialise with optional fock space input
        """
        SMatrix.__init__(self,"Qubit")
        if type(data) is int:
            self.array = np.zeros(2**data)
            self.array[fock] = 1
            self.array = sp.bsr_matrix(self.array) 
        else:
            self.array = sp.bsr_matrix(data)


    def normalise(self):
        """Renormalise qubit register such that probabilities sum to 1
        """
        div = np.sqrt(np.dot(self.array.toarray()[0],np.conjugate(self.array.toarray()[0])))
        self.array = self.array/div


    def measure(self):
        """Measure qubit register. Collapses to 1 definite state. Simulates real measurement, as 
        intermediate values of qubit registers during computation remain unknown.
        """
        self.normalise()
        data = self.array.toarray()[0]
        pos = np.arange(len(data))
        probs = probs = data * np.conjugate(data)
        #If probs is not normalised (usually due to rounding errors), re-normalise
        #probs = probs/np.sum(probs)
        dist = stats.rv_discrete(values=(pos,probs))
        self.array = np.zeros(data.shape)
        self.array[dist.rvs()] = 1
        r = self.array
        self.array = sp.bsr_matrix(self.array)
        return r

    def measure_cheat(self):
        #Measure but ignore 0 state, for debugging shors
        data = self.array.toarray()[0]
        pos = np.arange(len(data))
        probs = np.abs(np.square(data))
        probs[0] = 0
        #If probs is not normalised (usually due to rounding errors), re-normalise
        probs = probs/np.sum(probs)
        #print(probs)
        dist = stats.rv_discrete(values=(pos,probs))
        self.array = np.zeros(data.shape)
        self.array[dist.rvs()] = 1
        self.array = sp.bsr_matrix(self.array)

    def split_register(self):
        """Splits entangle qubit register into individual qubit states. Only works after measurement
        has been acted on a qubit register. Returns a binary string representing the states of each qubit
        """
        t = self.array.toarray()[0]
        outs = np.arange(0,len(t),1)
        res = np.array(np.sum(outs*t.astype(int)))
        return np.binary_repr(res)




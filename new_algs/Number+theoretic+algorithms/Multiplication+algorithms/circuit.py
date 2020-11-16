"""
Implementation of arithmetic gates and an arithmetic circuit.
Gate object is a general gate. Circuit is a set of gates with connections between them.
"""

from serializer import *
from operator import add, mul

class Gate(object):
    """General gate object. Every gate has a label & a single uninitialized output.
    Every gate must implementation of a gate has to implement the
    gate's calculation function named _calc.
    """
    def __init__(self, label):
        self._label = label
        self.reset()
    
    def reset(self):
        self.output = None

    def calculate(self, *inputs):
        self.output = self._calc(*inputs)
        return self.output
    
    def get_label(self):
        return self._label
    
    def set_value(self, value):
        self.output = value
    
    def __serialize__(self):
        return self.output, (self._label,)
    
    @classmethod
    def __unserialize__(cls, serialized):
        output, args = serialized
        ret = cls(*args)
        ret.output = output
        return ret

class AdditionGate(Gate):
    """Adds the given inputs. Supports arbitrary number of inputs"""
    def __init__(self, label=None):
        Gate.__init__(self, label)
        
    def _calc(self, *pins):
        return reduce(add, pins)

class MultiplicationGate(Gate):
    """Multiplies the given inputs. Supports exactly two inputs"""
    def __init__(self, label=None):
        Gate.__init__(self, label)
        
    def _calc(self, pinA, pinB):
        return pinA * pinB

class ScalarMultGate(Gate):
    """Multiplies the input by the gate's scalar. Supports exactly one inputs"""
    def __init__(self, scalar, label=None):
        Gate.__init__(self, label)
        self._scalar = scalar
        
    def _calc(self, pinA):
        return self._scalar * pinA
    
    def __serialize__(self):
        scalar_s = serialize(self._scalar)
        return self.output, scalar_s, self._label
    
    @classmethod
    def __unserialize__(cls, serialized):
        output, scalar_s, label = serialized
        scalar = unserialize(scalar_s)
        ret = cls(scalar, label)
        ret.output = output
        return ret

class NullGate(Gate):
    """Does nothing: output=input. Supports is_initialized to check if input was set"""
    def __init__(self, label=None, x=None):
        Gate.__init__(self, label)
        self.set_value(x)
    
    def is_initialized(self):
        """@retrun True if an input was set"""
        return self.output is not None
    
    def _calc(self, pinA):
        self.set_value(pinA)
        return self.output


class Circuit(object):
    """A general arithmetic circuit, made of Gate-s.
    A circuit has an arbitrary number of inputs and a single output.
    A circuit with @n_inputs inputs has INPUT0,... defined as it's inputs.
    The circuit's output label is OUTPUT.
    Gates may be added to the circuit, using previous added gates / INPUTs as inputs.
    After building the gate and defining the last gate used as output,
    evaluation of the circuit or some gates are possible. The eval_order method will
    return the order gates can be evaluated in order to evaluate the whole circuit.
    Supports serialization and unserialization of the circuit to a str.
    """
    OUTPUT = "OUTPUT"
    INPUT  = "INPUT"
    
    def __init__(self, n_inputs=1):
        """Initialize a circuit with @n_inputs inputs"""
        self._gates = {}
        self._conns = {}
        self._n_inputs = n_inputs
        for i in xrange(n_inputs):
            label = Circuit.INPUT + str(i)
            self._gates[label] = NullGate(label=label)
        self._gates[Circuit.OUTPUT] = NullGate(label=Circuit.OUTPUT)
        self._out_connected = False
        self._order = []
    
    def get_num_inputs(self):
        """@return the number of inputs of the circuit"""
        return self._n_inputs
    
    def add_gate(self, gate, inputs, is_output=False):
        """Add a new gate to the circuit.
        @gate - a Gate object to be added.
        @inputs - a list of already added gate labels to be used as inputs. INPUTx are allowed here.
        @is_output - is this the circuits final output? Only one gate per circuit may be its output
        """
        # If we previously calculated circuit's eval order - delete it
        self._order = []
        
        gate_label = gate.get_label()
        assert self.is_input(gate_label) == False, "Reserved label name"
        assert gate_label != Circuit.OUTPUT, "Reserved label name"
        assert gate_label not in self._gates, "Gate %s already exists!" % gate_label
        
        for inp in inputs:
            assert inp in self._gates, "Input gate '%s' not defined yet" % inp
        self._gates[gate_label] = gate
        self._conns[gate_label] = list(inputs)
        
        if is_output:
            assert self._out_connected == False, "Only one output possible!"
            self._conns[Circuit.OUTPUT] = [gate.get_label()]
            self._out_connected = True
    
    def is_input(self, gate):
        """
        Check if the given gate object / name (str) is an input NullGate / input name
        @return True if INPUT0,...INPUT{n_inputs}, else False
        """
        if isinstance(gate, Gate):
            gate = gate.get_label()
        
        if gate.startswith(Circuit.INPUT) == False:
            return False
        try:
            i = int(gate[len(Circuit.INPUT) : ])
            assert 0 <= i < self._n_inputs
        except:
            return False
            
        return True
    
    def gate_type(self, gate_name):
        """Translate @gate_name into its type"""
        return type(self._gates[gate_name])
    
    def set_gate_output(self, gate_name, value):
        """Set @gate_name-'s output to @value"""
        self._gates[gate_name].set_value(value)
    
    def init_input(self, i, value):
        """Initialize input gate @i (INPUT{i}) to @value"""
        assert 0 <= i < self._n_inputs, "Invalid input number %d" % i
        self._gates[Circuit.INPUT + str(i)].set_value(value)
    
    def init_all_inputs(self, inputs):
        """Initialize all input gates according to the list of @inputs. Resets all inner state of the circuit"""
        assert len(inputs) == self._n_inputs, "Inputs wrong length"
        self.reset()
        for i, v in enumerate(inputs):
            self.init_input(i, v)

    def __serialize__(self):
        """Return a printable encoding of the circuit (including its internal state)"""
        s_gates = {label : serialize(gate) for label,gate in self._gates.items()}
        return s_gates, self._conns, self._n_inputs, self._out_connected
    
    @classmethod
    def __unserialize__(cls, serialized):
        """Creates a new circuit object by unserializing given @serialized string"""
        s_gates, conns, n_inputs, out_connected = serialized
        self = cls(n_inputs)
        self._gates = {label : unserialize(s) for label,s in s_gates.items()}
        self._conns = conns
        self._out_connected = out_connected
        return self
    
    def eval_order(self):
        """Returns a list of all circuit's gates (their labels)
        in a proper order that guarantees a valid order for evaluation.
        The list ends with the OUTPUT NullGate.
        """
        if self._order != []:
            return self._order
        assert self._out_connected, "Output not connected"
        self._order = []
        self._eval_order_inner(Circuit.OUTPUT)
        return self._order
    
    def _eval_order_inner(self, gate):
        """The implementation of eval_order using a recursive walk on the circuit
        The circuit is traversed post-order as a tree with OUTPUT as its root.
        Because the circuit is not a tree, visited gates are skipped. Post-order
        ensures that skipped gates are calculated before all their 'parents'.
        """
        if self.is_input(gate) or gate in self._order:
            # We already calculated this gate in the past
            return
        else:
            # Eval order of all sons
            for g in self._conns[gate]:
                self._eval_order_inner(g)
            self._order.append(gate)
    
    def reset(self):
        """Reset all the circuit's state - resets all gates of the circuit, including inputs"""
        for g in self._gates:
            self._gates[g].reset()
    
    def evaluate_gate(self, gate_name):
        """Evaluates a single gate in the circuit.
        Note that this changes the state of the circuit.
        Returns the gate's output
        """
        input_gates = self._conns[gate_name]
        inputs = [self._gates[g].output for g in input_gates]
        assert None not in inputs, "Cannot evaluate %s, input %s undefined" % (gate_name, input_gates[inputs.index(None)])
        output = self._gates[gate_name].calculate(*inputs)
        return output
    
    def evaluate(self, inputs):
        """Evaluate the whole circuit.
        @inputs - A list of all inputs
        @return the output of the circuit's evaluation
        """
        self.init_all_inputs(inputs)
        order = self.eval_order()
        for cur_gate in order:
            self.evaluate_gate(cur_gate)
        return self._gates[Circuit.OUTPUT].output
    
    def get_output(self):
        """Get the output of the circuit. Assumes circuit was evaluated / OUTPUT is manually set"""
        assert self._gates[Circuit.OUTPUT].is_initialized(), "Circuit not fully evaluated!"
        return self._gates[Circuit.OUTPUT].output

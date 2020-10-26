"""
A module for Master dispatcher and controller of Nodes (parties).
Initializes and coordinates parties so a correct BGW MPC will be executed.
"""

from utils import log
from serializer import *
from debugger import check_debugging
from node import Node
from messenger import Server, Message
from gf import FF
from circuit import Circuit, MultiplicationGate
from config import Config

class Master(object):
    """The Master initializes and coordinates the BGW computation.
    The dispatches Nodes, initializes them (circuit, messaging, inputs if needed etc'),
    and finally coordinates the computation of the Nodes.
    The Master is not part of the computation itself and it has nothing to do with
    the actual secrets / shares of the Nodes. It merely instructs the parties what
    steps should be taken next for computation.
    """
    def __init__(self, n_parties, circuit, tranformation=None, ss_args=None, ss2_args=None):
        """
        Creates a new Master and Nodes.
        @parties - Number of parties
        @circuit - the circuit to be calculated
        @ss_args - a iterable/mapping of arguments for the inner secret sharing schemes (could be empty or None)
        """
        self._n_parties = n_parties
        self._circuit = circuit
        self._mult_transformation = tranformation
        self._dik_next_dealer = 0
        self._ss_args = ss_args
        self._ss2_args = ss2_args
        self.reset()
    
    def reset(self):
        """Reinitialize the Master. Creates new party nodes"""
        # Messenger variables
        self._server = Server(self._n_parties)
        self._io = self._server.get_master()
        self._id = self._io.get_id()
        
        # Debugging variables
        self._debugging_on = False
        self._debug_countdown = None
        
        # Circuit variables
        self._circuit_order = self._circuit.eval_order()
        self._cur_gate = 0
        self._done = False
        
        # Dispatch all party Nodes
        self._parties = {}
        for pid in xrange(self._n_parties):
            party = self._server.get_client(pid)
            n = Node(pid, party, self._n_parties, self._id)
            self._parties[pid] = n
    
    def init(self, secrets):
        """Initialize parties' circuit, inputs and truncinator.
        Parties share their inputs according to SSS.
        @secrets may be either a mapping party->secret, or a Finite Field object.
        In case of FF (Zmod/Extension) - parties will choose random secrets in field.
        After init has finished - all parties should be in RUNNING state.
        """
        # Set circuit
        self.send_and_run_all(Message.TYPE.SetCircuit, serialize(self._circuit))
        
        # Set secret sharing schemes
        self.send_and_run_all(Message.TYPE.SetSecretSharing, serialize((self._ss_args, self._ss2_args)))
        
        # Set Truncinator / Resampler for multiplication
        if Config.MULT_METHOD == Config.MULT_METHODS.BGW:
            self.send_and_run_all(Message.TYPE.SetTruncinator, serialize(self._mult_transformation))
        elif Config.MULT_METHOD == Config.MULT_METHODS.DIK:
            self.send_and_run_all(Message.TYPE.SetResampler, serialize(self._mult_transformation))
        
        # Init inputs
        if isinstance(secrets, FF):
            gf = secrets
            self.send_and_run_all(Message.TYPE.SetRandInput, serialize(gf))
        else:
            for pid in xrange(self._n_parties):
                self.send_single(pid, Message.TYPE.SetInput, serialize(secrets[pid]))
            self.run_all()
        
        # Do DIK random masks preprocessing
        if Config.MULT_METHOD == Config.MULT_METHODS.DIK:
            # Count number of multiplication gates -> number of bulks needed
            is_mult = lambda g : self._circuit.gate_type(g) is MultiplicationGate
            n_mult = len(filter(is_mult, self._circuit_order))
            n_bulks, remainder = divmod(n_mult, self._mult_transformation.dst_len())
            if remainder > 0:
                n_bulks += 1
            log.info("DIK masks: Generating %d bulks" % n_bulks)
            for i in xrange(n_bulks):
                self.send_and_run_all(Message.TYPE.GenBulkMulMasks, runs=2)
        
        # Share inputs, another run to collect input shares
        self.send_and_run_all(Message.TYPE.ShareInput, runs=2)
        
    def run(self, steps = None):
        """Perform the main computation of the MPC - gate by gate
        @steps - amount of gates to evaluate.
        When all gates are evaluated - output is reconstruct by parties.
        """
        
        # Check if there's what to do
        if self._done == True:
            log.info("Already finished, not running!")
            return
        
        # Calculate what is our last step
        if steps is not None:
            limit = min(self._cur_gate + steps, len(self._circuit_order))
        else:
            limit = len(self._circuit_order)
        
        # Eval gate-by-gate
        while self._cur_gate < limit:
            g = self._circuit_order[self._cur_gate]
            
            # Multiplication gate?
            if self._circuit.gate_type(g) is MultiplicationGate:
                
                if Config.MULT_METHOD == Config.MULT_METHODS.BGW:
                    # Run1: Choose a random polynomial with free factor zero, and share it
                    # Run2: Collect shares, calculate F(k) = f_1(k) + ... + f_n(k) , add F(k) to a_k*b_k
                    self.send_and_run_all(Message.TYPE.EvalMulGateInit, g, runs=2)
                    
                    # Run1: Share this F(k) + a_k*b_k
                    # Run2: Collect these shares, calculate degree reduction (linear circuit)
                    self.send_and_run_all(Message.TYPE.EvalMulGateReduce, runs=2)
                    
                    # Run1: Send back the result of the degree reduction
                    # Run2: Collect my shares and reconstruct a_k*b_k
                    self.send_and_run_all(Message.TYPE.EvalMulGateFinalize, runs=2)
                
                elif Config.MULT_METHOD == Config.MULT_METHODS.DIK:
                    # Run1: All parties send the arbitrary "dealer" their masked local multiplication share
                    # Run2 (dealer only): Dealer recovers the masked secret and reshares in low deg
                    # Run3: Parties remove the mask from their new share - done
                    dealer = self._dik_next_dealer
                    self._dik_next_dealer = (self._dik_next_dealer + 1) % self._n_parties
                    self.send_and_run_all(Message.TYPE.EvalMulGateDIK, serialize((g, dealer)))
                    self.run_single(dealer)
                    self.run_all()
                
                else:
                    raise AssertionError("Unknown configured multiplication method %s" % Config.MULT_METHODS.reverse_mapping[Config.MULT_METHOD])
            
            else:
                # Linear gate
                self.send_and_run_all(Message.TYPE.EvalGate, g)
            
            self._cur_gate += 1
        
        # Final output share phase?
        if self._cur_gate == len(self._circuit_order):
            # Send everybody our output, another run to collect all of other's output shares
            self.send_and_run_all(Message.TYPE.EvalOutput, runs=2)
            self._done = True
        
    @check_debugging
    def send_single(self, pid, msg_type, msg=""):
        """Send a single Message of type @msg_type to @pid.
        @msg - Optional for Message data.
        """
        m = Message(self._id, pid, msg_type, msg)
        self._io.send(m)
    
    @check_debugging
    def run_single(self, pid, inner_runs=1):
        """Let party @pid run @innner_runs times"""
        self._parties[pid].run(inner_runs)
    
    def send_all(self, msg_type, msg=""):
        """Send all parties a Message of type @msg_type.
        @msg - Optional for Message data.
        """
        for pid in xrange(self._n_parties):
            self.send_single(pid, msg_type, msg)
    
    def run_all(self, runs=1, inner_runs=1):
        """Let the parties run @runs times, each party running @inner_runs consecutive times on every run"""
        for i in xrange(runs):
            for pid in xrange(self._n_parties):
                self.run_single(pid, inner_runs)
    
    def send_and_run_single(self, pid, msg_type, msg="", inner_runs=1):
        """Send a single Message of type @msg_type to @pid, then let the party run for @inner_runs steps.
        @msg - Optional for Message data.
        """
        self.send_single(pid, msg_type, msg)
        self.run_single(pid, inner_runs)
    
    def send_and_run_all(self, msg_type, msg="", runs=1, inner_runs=1):
        """Send all parties a Message of type @msg_type, then let the parties run.
        @msg - Optional for Message data.
        @runs - how many rounds to let the parties runs (round robin)
        @inner_runs - how many consecutive runs to run each party
        """
        self.send_all(msg_type, msg)
        self.run_all(runs, inner_runs)
        
    def toggle_step_by_step(self, turn_on=None):
        """Toggle debugging on/off"""
        if turn_on is None:
            self._debugging_on = not self._debugging_on
        else:
            self._debugging_on = turn_on
